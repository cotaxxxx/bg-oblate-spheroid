#!/usr/bin/env python3
"""Lineage gating and numerical orchestration for the C1b producer."""
from __future__ import annotations

import argparse
import contextlib
import io
import hashlib
import json
import re
import signal
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from pathlib import Path

from analysis import c1b_resumable_driver as persistence

_stop_requested = False

def decimal_directed(a, b, rounding):
    with localcontext() as dc:
        dc.prec = max(120, len(a) + len(b) + 20)
        dc.rounding = rounding
        return str(Decimal(a) + Decimal(b))


def arb_parts(mid, rad):
    return {
        "mid": mid,
        "rad": rad,
        "lower": decimal_directed(mid, "-" + rad, ROUND_FLOOR),
        "upper": decimal_directed(mid, rad, ROUND_CEILING),
    }


_ARB_RE = re.compile(r"^\[?\s*([^\s\]]+)\s*\+/-\s*([^\s\]]+)\s*\]?$")


def arb_decimal_record(text):
    """Normalize an Arb decimal rendering without binary float conversion."""
    s = text.strip()
    if s == "None":
        return None
    if s.startswith("[+/-"):
        rad = s[len("[+/-"):].strip().rstrip("]").strip()
        mid = "0"
        return arb_parts(mid, rad)
    m = _ARB_RE.match(s)
    if m:
        mid, rad = m.group(1), m.group(2)
        return arb_parts(mid, rad)
    # Exact decimal Arb rendering.
    return {"mid": s, "rad": "0", "lower": s, "upper": s}



class Tee(io.TextIOBase):
    def __init__(self, target):
        self.target = target
        self.lines = []
        self.partial = ""

    def write(self, text):
        self.target.write(text)
        self.target.flush()
        self.partial += text
        while "\n" in self.partial:
            line, self.partial = self.partial.split("\n", 1)
            self.lines.append(line)
        return len(text)

    def flush(self):
        self.target.flush()


def parse_trace(lines):
    result = {
        "predictor": [],
        "tube_stages": [],
        "root_steps": [],
        "root_enclosure": [],
        "acceptance": [],
        "exterior_stages": [],
        "middle_partition": [],
    }
    tube = re.compile(
        r"^C1B_TUBE_STAGE\s+\d+\s+\d+\s+\S+\s+\S+\s+(T[0-2]).*?"
        r"gt_bad\s+(\d+)\s+left_bad\s+(\d+)\s+right_bad\s+(\d+).*?"
        r"gt_worst_upper\s+(.*?)\s+left_worst_lower\s+(.*?)\s+right_worst_upper\s+(.*)$"
    )
    exterior = re.compile(
        r"^C1B_EXTERIOR_STAGE\s+\d+\s+\d+\s+(E[0-2]).*?"
        r"unresolved\s+(\d+).*?worst_left_lower\s+(.*?)\s+worst_right_upper\s+(.*)$"
    )
    for line in lines:
        if line.startswith("C1B_PREDICTOR "):
            result["predictor"].append(line)
        elif line.startswith("C1B_ROOT_STEP ") or line.startswith("C1B_ROOT_MV_STEP "):
            result["root_steps"].append(line)
        elif line.startswith("C1B_ROOT_ENCLOSURE "):
            result["root_enclosure"].append(line)
        elif line.startswith("C1B_PREDICTOR_ACCEPT "):
            result["acceptance"].append(line)
        elif line.startswith("C1B_MIDDLE_T_PARTITION "):
            result["middle_partition"].append(line)
        else:
            m = tube.match(line)
            if m:
                result["tube_stages"].append({
                    "stage": m.group(1),
                    "gt_unresolved": int(m.group(2)),
                    "left_unresolved": int(m.group(3)),
                    "right_unresolved": int(m.group(4)),
                    "gt_worst_upper": arb_decimal_record(m.group(5)),
                    "left_worst_lower": arb_decimal_record(m.group(6)),
                    "right_worst_upper": arb_decimal_record(m.group(7)),
                })
                continue
            m = exterior.match(line)
            if m:
                result["exterior_stages"].append({
                    "stage": m.group(1),
                    "unresolved": int(m.group(2)),
                    "worst_left_lower": arb_decimal_record(m.group(3)),
                    "worst_right_upper": arb_decimal_record(m.group(4)),
                })
    return result


def serialize_root(root):
    if root is None:
        return None
    return [persistence.rational_text(root[0]), persistence.rational_text(root[1])]


def slab_payload(slab):
    return {
        "coarse_index": int(slab.coarse),
        "refinement_depth": int(slab.depth),
        "lambda_lo": persistence.rational_text(slab.ll),
        "lambda_hi": persistence.rational_text(slab.lr),
    }


def _rr(pair):
    return None if pair is None else [persistence.rational_text(pair[0]), persistence.rational_text(pair[1])]

def _serialize_guard(guard):
    label, kind, tl, tr, ll, lr, truth = guard
    return {
        "stage": label, "kind": kind,
        "t_lo": persistence.rational_text(tl), "t_hi": persistence.rational_text(tr),
        "lambda_lo": persistence.rational_text(ll), "lambda_hi": persistence.rational_text(lr),
        "truth": bool(truth),
    }

def serialize_mv_step(step):
    return {
        "step": int(step["step"]),
        "T_k": _rr(step["T_k"]),
        "t_ref": persistence.rational_text(step["t_ref"]),
        "lambda_c": persistence.rational_text(step["lambda_c"]),
        "G0": step["G0"],
        "Gt": step["Gt"],
        "Gt_cells": [{
            "t_cell": _rr(cell["t_cell"]),
            "Gt": cell["Gt"],
            "guard": bool(cell["guard"]),
            "corner_hull": int(cell["corner_hull"]),
            "work": int(cell["work"]),
        } for cell in step.get("Gt_cells", [])],
        "Gl": step["Gl"],
        "Gpar": step["Gpar"],
        "N_k": step["N_k"],
        "T_next": _rr(step["T_next"]),
        "width": persistence.rational_text(step["width"]),
        "division_guard": bool(step["division_guard"]),
        "empty_intersection": bool(step.get("empty_intersection", False)),
        "gt_charts": {str(k): int(v) for k, v in step["gt_charts"].items()},
        "gl_stats": {str(k): int(v) for k, v in step["gl_stats"].items()},
        "step_work": int(step["step_work"]),
    }

def serialize_record(rec, tc, mode, work, reason, trace):
    empty = {
        "predictor_mode": mode,
        "t_c": None if tc is None else persistence.rational_text(tc),
        "T_star": None, "left_clamp": None, "right_clamp": None,
        "t_minus": None, "t_plus": None, "T_0": None,
        "root_gt_t_cells": 16, "corner_hull": None, "corner_boxes": [],
        "tube_stage": None, "tube_guards": [], "exterior_guards": [],
        "sup_error": None, "middle_partition": None,
        "work": {k: int(v) for k, v in work.items()},
        "work_total": int(sum(work.values())), "reason": reason, "trace": trace,
        "root_mv_steps": [], "root_reason": None,
    }
    if rec is None:
        return empty
    empty.update({
        "predictor_mode": rec["mode"],
        "t_c": persistence.rational_text(rec["tc"]),
        "T_star": serialize_root(rec["root"]),
        "left_clamp": bool(rec["left_clamp"]), "right_clamp": bool(rec["right_clamp"]),
        "t_minus": persistence.rational_text(rec["tm"]),
        "t_plus": persistence.rational_text(rec["tp"]),
        "T_0": [persistence.rational_text(rec["tm"]), persistence.rational_text(rec["tp"])],
        "root_gt_t_cells": 16, "corner_hull": int(rec["corner_hull"]),
        "corner_boxes": [[persistence.rational_text(v) for v in box] for box in rec.get("corner_boxes", ())],
        "tube_stage": rec["tube_stage"],
        "tube_guards": [_serialize_guard(x) for x in rec.get("tube_guards", ())],
        "exterior_guards": [_serialize_guard(x) for x in rec.get("exterior_guards", ())],
        "sup_error": None if rec["sup_error"] is None else persistence.rational_text(rec["sup_error"]),
        "root_mv_steps": [serialize_mv_step(x) for x in rec.get("root_steps", [])],
        "root_reason": rec.get("root_reason"),
        "middle_partition": [[kind, persistence.rational_text(lo), persistence.rational_text(hi)] for kind, lo, hi in rec["pieces"]],
    })
    return empty

REPLAY_SCHEMA = "C1B_A1_REPLAY_V2_4_2"
REPLAY_KEYS = {
    "schema", "attempt_sequence", "coarse_index", "refinement_depth",
    "lambda_lo", "lambda_hi", "tree_node", "t_c", "left_clamp",
    "right_clamp", "t_minus", "t_plus", "T_0", "root_gt_t_cells",
    "producer_accept_root_outcome", "decision",
}
FORBIDDEN_REPLAY_KEYS = {"T_star", "G0", "Gt", "Gl", "Gpar", "N_k", "root_mv_steps"}

def load_replay_plan(path):
    data = Path(path).read_bytes()
    plan = []
    for line_no, raw in enumerate(data.splitlines(), 1):
        obj = json.loads(raw.decode("utf-8"))
        if set(obj) != REPLAY_KEYS or obj.get("schema") != REPLAY_SCHEMA:
            raise SystemExit(f"REPLAY_SCHEMA_FAIL line={line_no}")
        if FORBIDDEN_REPLAY_KEYS.intersection(obj):
            raise SystemExit(f"REPLAY_A2_FIELD_LEAK line={line_no}")
        if obj["decision"] not in ("ACCEPT", "REFINE", "ABORT"):
            raise SystemExit(f"REPLAY_DECISION_FAIL line={line_no}")
        expected_node = f'{obj["coarse_index"]}:{obj["refinement_depth"]}:{obj["lambda_lo"]}:{obj["lambda_hi"]}'
        if obj["tree_node"] != expected_node:
            raise SystemExit(f"REPLAY_TREE_NODE_FAIL line={line_no}")
        plan.append(obj)
    if not plan:
        raise SystemExit("REPLAY_PLAN_EMPTY")
    return plan, hashlib.sha256(data).hexdigest()

def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def slab_from_plan(item, kernel):
    return kernel.Slab(int(item["coarse_index"]), int(item["refinement_depth"]),
                       Fraction(item["lambda_lo"]), Fraction(item["lambda_hi"]))

def replay_state(records, plan):
    persisted = persistence.resume_state(records)
    terminal = persisted["terminal"]
    if len(terminal) > len(plan):
        raise SystemExit("CHECKER_LEDGER_EXCEEDS_REPLAY_PLAN")
    previous_root = None
    for index, payload in enumerate(terminal):
        item = plan[index]
        if payload.get("attempt_sequence") != item["attempt_sequence"]:
            raise SystemExit("A1_REPLAY_ATTEMPT_SEQUENCE_MISMATCH")
        for key in ("coarse_index", "refinement_depth", "lambda_lo", "lambda_hi"):
            if payload.get(key) != item[key]:
                raise SystemExit("A1_REPLAY_SLAB_MISMATCH")
        if payload.get("decision") != item["decision"]:
            raise SystemExit("A1_REPLAY_DECISION_MISMATCH")
        if item["decision"] == "ACCEPT":
            root = payload["result"].get("T_star")
            if root is None:
                raise SystemExit("CHECKER_REPLAY_UNRESOLVED")
            previous_root = tuple(Fraction(x) for x in root)
    return {"plan_index": len(terminal), "previous_root": previous_root, **persisted}

def verify_a1_fields(item, result):
    if result.get("t_c") != item["t_c"]:
        raise SystemExit("A1_REPLAY_FIELD_MISMATCH:t_c")
    if item["t_minus"] is not None:
        checks = ("left_clamp", "right_clamp", "t_minus", "t_plus", "T_0",
                  "root_gt_t_cells")
        for key in checks:
            if result.get(key) != item[key]:
                raise SystemExit("A1_REPLAY_FIELD_MISMATCH:" + key)
    if item["decision"] == "ACCEPT":
        if item["producer_accept_root_outcome"] != "RESOLVED_WITH_CERTIFIED_T_STAR":
            raise SystemExit("A1_PRODUCER_ACCEPT_ROOT_OUTCOME_INVALID")
        if result.get("T_star") is None or result.get("root_reason") != "TARGET_WIDTH":
            raise SystemExit("CHECKER_REPLAY_UNRESOLVED")

def estimates(kernel):
    predictor = 513 * 2 * kernel.PRED_SCAN_PANELS
    t0 = 8 * 4 * 4096 + 2 * 4 * 4096
    root = kernel.ROOT_MV_STEPS * (kernel.ROOT_G_PANELS + kernel.ROOT_GT_T_CELLS * kernel.ROOT_GT_PANELS + kernel.ROOT_GL_T_CELLS * kernel.ROOT_GL_PANELS)
    e0 = kernel.E0_TBOXES * kernel.E0_LBOXES * kernel.E_STAGES[0][1]
    early = kernel.N_COARSE * (predictor + t0 + root + e0)
    no_refine_late = kernel.N_COARSE * (
        predictor + kernel.ATTEMPT_WORK_CEILING
    )
    return {
        "coarse_slabs": kernel.N_COARSE,
        "predictor_per_attempt": predictor,
        "T0_E0_early_pass_one_lineage": early,
        "T2_E2_no_refinement_one_lineage": no_refine_late,
        "accepted_gating_ceiling": kernel.ACCEPTED_WORK_CEILING,
        "global_attempted_gating_ceiling": kernel.GLOBAL_ATTEMPT_WORK_CEILING,
    }


def header_payload(kernel, lineage, pins, identity, replay_sha256, producer_ledger_sha256):
    return {
        "chain_version": persistence.CHAIN_VERSION,
        "lineage": lineage,
        "created_utc": persistence.utc_now(),
        "identity": identity,
        "precision_bits": kernel.BITS,
        "degree": kernel.DEG,
        "u_star": persistence.rational_text(kernel.USTAR),
        "lambda_domain": [persistence.rational_text(kernel.L_LO), persistence.rational_text(kernel.L_HI)],
        "stages": {
            "T": [list(x) for x in kernel.T_STAGES],
            "ROOT_MV": {
                "steps": kernel.ROOT_MV_STEPS,
                "g_panels": kernel.ROOT_G_PANELS,
                "gt_panels_per_cell": kernel.ROOT_GT_PANELS,
                "gt_t_cells": kernel.ROOT_GT_T_CELLS,
                "gl_panels_per_cell": kernel.ROOT_GL_PANELS,
                "gl_t_cells": kernel.ROOT_GL_T_CELLS,
                "target": persistence.rational_text(kernel.ROOT_TARGET),
            },
            "E": [list(x) for x in kernel.E_STAGES],
        },
        "caps": {
            "coarse": kernel.N_COARSE,
            "accepted": kernel.MAX_ACCEPTED,
            "attempted": kernel.MAX_ATTEMPTED,
            "depth": kernel.MAX_DEPTH,
        },
        "budgets": {
            "attempt": kernel.ATTEMPT_WORK_CEILING,
            "accepted": kernel.ACCEPTED_WORK_CEILING,
            "global": kernel.GLOBAL_ATTEMPT_WORK_CEILING,
            "predictor": 513 * 2 * kernel.PRED_SCAN_PANELS,
        },
        "estimates": estimates(kernel),
        "pin_manifest": pins,
        "phase": "checker_fixed_tree_replay",
        "replay_schema": REPLAY_SCHEMA,
        "replay_sha256": replay_sha256,
        "producer_ledger_sha256": producer_ledger_sha256,
    }


def request_stop(signum, frame):
    global _stop_requested
    _stop_requested = True


def verify_resume_header(stored, current):
    """Compare every immutable header field; only creation UTC may differ."""
    stored_static = dict(stored)
    current_static = dict(current)
    stored_static.pop("created_utc", None)
    current_static.pop("created_utc", None)
    if stored_static != current_static:
        raise SystemExit("RESUME_HEADER_CONTRACT_MISMATCH")


def run_full(kernel, lineage, run_dir, replay_plan_path, producer_ledger_path):
    pins = persistence.load_pins()
    if pins is None:
        raise SystemExit("RESUMABLE_PIN_MANIFEST_MISSING")
    plan, replay_sha256 = load_replay_plan(replay_plan_path)
    producer_ledger_sha256 = file_sha256(producer_ledger_path)
    identity = persistence.environment_snapshot(pins[lineage])
    persistence.verify_identity(identity, pins[lineage])
    run_dir = Path(run_dir)
    ledger = persistence.Ledger(run_dir / "ledger.jsonl")
    current_header = header_payload(kernel, lineage, pins[lineage], identity, replay_sha256, producer_ledger_sha256)
    if not ledger.records:
        ledger.append("header", current_header)
    else:
        if ledger.records[0]["record_type"] != "header":
            raise SystemExit("LEDGER_HEADER_MISSING")
        verify_resume_header(ledger.records[0]["payload"], current_header)
    state = replay_state(ledger.records, plan)
    full_charge = kernel.ATTEMPT_WORK_CEILING + 513 * 2 * kernel.PRED_SCAN_PANELS
    for seq in state["unmatched"]:
        ledger.append("interrupted_attempt_charge", {
            "attempt_sequence": seq, "charged_work": full_charge,
            "charged_attempt_unit": 1, "utc": persistence.utc_now(),
        })
    if state["unmatched"]:
        state = replay_state(ledger.records, plan)
    persistence.check_ceiling(state["attempted"], kernel.MAX_ATTEMPTED, "MAX_ATTEMPTED_SLABS_EXCEEDED")
    segment_index = persistence.next_segment_index(ledger.records)
    next_item = None if state["plan_index"] >= len(plan) else plan[state["plan_index"]]
    ledger.append("segment_begin", {
        "segment_index": segment_index, "utc": persistence.utc_now(), "pin_check": "PASS",
        "identity": identity, "replay_sha256": replay_sha256,
        "producer_ledger_sha256": producer_ledger_sha256,
        "cumulative_work": state["global_work"], "attempted": state["attempted"],
        "next_slab": None if next_item is None else slab_payload(slab_from_plan(next_item, kernel)),
    })
    def append_segment_end(reason, cumulative_work, attempted, **extra):
        post_identity = persistence.environment_snapshot(pins[lineage])
        persistence.verify_identity(post_identity, pins[lineage])
        payload = {
            "segment_index": segment_index, "utc": persistence.utc_now(), "reason": reason,
            "cumulative_work": cumulative_work, "attempted": attempted, "post_pin_check": "PASS",
            "post_identity": post_identity, "replay_sha256": replay_sha256,
            "producer_ledger_sha256": producer_ledger_sha256,
        }
        payload.update(extra); ledger.append("segment_end", payload)
    signal.signal(signal.SIGTERM, request_stop); signal.signal(signal.SIGINT, request_stop)
    kernel.ctx.prec = kernel.BITS; kernel.base.ctx.prec = kernel.BITS; kernel.preflight()
    previous_root = state["previous_root"]
    accepted_work = state["accepted_work"]; global_work = state["global_work"]
    attempted = state["attempted"]; accepted_count = len(state["accepted"])
    index = state["plan_index"]
    while index < len(plan):
        item = plan[index]
        if _stop_requested:
            append_segment_end("requested_stop", global_work, attempted,
                               next_slab=slab_payload(slab_from_plan(item, kernel)))
            return
        if attempted >= kernel.MAX_ATTEMPTED:
            raise SystemExit("MAX_ATTEMPTED_SLABS_EXCEEDED")
        slab = slab_from_plan(item, kernel)
        attempted += 1; attempt_sequence = attempted
        expected_tc = None if item["t_c"] is None else Fraction(item["t_c"])
        ledger.append("attempt_begin", {
            "attempt_sequence": attempt_sequence, **slab_payload(slab),
            "replay_decision": item["decision"], "previous_root": serialize_root(previous_root),
            "cumulative_work_before": global_work, "utc": persistence.utc_now(),
        })
        tee = Tee(sys.stdout)
        with contextlib.redirect_stdout(tee):
            ok, rec, root, tc, work, reason = kernel.attempt_replay(slab, previous_root, expected_tc)
        trace = parse_trace(tee.lines)
        result = serialize_record(rec, tc, None if rec is None else rec["mode"], work, reason, trace)
        verify_a1_fields(item, result)
        attempt_work = result["work_total"]; global_work += attempt_work
        if global_work > kernel.GLOBAL_ATTEMPT_WORK_CEILING:
            raise SystemExit("GLOBAL_ATTEMPT_WORK_CEILING_EXCEEDED")
        fixed_decision = item["decision"]
        root_outcome = ("RESOLVED_WITH_CERTIFIED_T_STAR"
                        if result.get("T_star") is not None and result.get("root_reason") == "TARGET_WIDTH"
                        else "UNRESOLVED")
        if fixed_decision == "ACCEPT":
            if root_outcome != "RESOLVED_WITH_CERTIFIED_T_STAR":
                raise SystemExit("CHECKER_REPLAY_UNRESOLVED")
            if not ok:
                raise SystemExit("CHECKER_REPLAY_ACCEPT_FAILURE:" + reason)
            accepted_count += 1; accepted_work += attempt_work; previous_root = root
            if accepted_count > kernel.MAX_ACCEPTED or accepted_work > kernel.ACCEPTED_WORK_CEILING:
                raise SystemExit("CHECKER_ACCEPTED_CEILING_EXCEEDED")
        payload = {
            "attempt_sequence": attempt_sequence, **slab_payload(slab),
            "decision": fixed_decision, "checker_full_ok": bool(ok), "checker_reason": reason,
            "checker_root_outcome": root_outcome, "result": result,
            "accepted_count": accepted_count, "accepted_work": accepted_work,
            "cumulative_work_after": global_work, "attempted_count": attempted,
            "a1_label": "A1_EXACT_EQUALITY",
            "a2_label": "A2_LINEAGE_INDEPENDENT",
            "utc": persistence.utc_now(),
        }
        ledger.append("slab_record", payload)
        index += 1
    accepted_plan = [x for x in plan if x["decision"] == "ACCEPT"]
    union_ok = bool(accepted_plan)
    if union_ok:
        union_ok = accepted_plan[0]["lambda_lo"] == persistence.rational_text(kernel.L_LO)
        union_ok = union_ok and accepted_plan[-1]["lambda_hi"] == persistence.rational_text(kernel.L_HI)
        union_ok = union_ok and all(a["lambda_hi"] == b["lambda_lo"] for a,b in zip(accepted_plan, accepted_plan[1:]))
    append_segment_end("completed" if union_ok else "failure", global_work, attempted,
                       accepted=accepted_count, exact_union=union_ok,
                       final_record_hash_before_end=ledger.last_hash)
    print("C1B_CHECKER_FIXED_REPLAY_FINAL", "PASS" if union_ok else "UNRESOLVED",
          "accepted", accepted_count, "attempted", attempted, "work", global_work,
          "ledger_hash", ledger.last_hash, "replay_sha256", replay_sha256,
          "producer_ledger_sha256", producer_ledger_sha256)
    if not union_ok:
        raise SystemExit("C1B_EXACT_UNION_FAIL")

def main(kernel, lineage):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-only", action="store_true")
    parser.add_argument("--run-dir")
    parser.add_argument("--replay-plan")
    parser.add_argument("--producer-ledger")
    args = parser.parse_args()
    kernel.ctx.prec = kernel.BITS; kernel.base.ctx.prec = kernel.BITS
    if args.ledger_only:
        kernel.preflight()
        print("C1B_PREFLIGHT_ESTIMATES", persistence.canonical_bytes(estimates(kernel)).decode("ascii"))
        print("C1B_LEDGER_ONLY_WRITES_REPOSITORY", False)
        return
    if not args.run_dir or not args.replay_plan or not args.producer_ledger:
        raise SystemExit("--run-dir --replay-plan --producer-ledger required")
    run_full(kernel, lineage, args.run_dir, args.replay_plan, args.producer_ledger)
