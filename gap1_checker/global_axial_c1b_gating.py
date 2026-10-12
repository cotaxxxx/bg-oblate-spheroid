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

from gap1_analysis import c1b_resumable_driver as persistence

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


GAP1_ALLOWED_R_MODES = ("fixed_replay", None)

GAP1_PREDICTOR_ROOT_FIELDS = ("predictor_mode", "t_c", "T_star", "left_clamp", "right_clamp", "t_minus",
                              "t_plus", "T_0", "sup_error", "root_reason", "tube_stage", "middle_partition")

def _gap1_value(value):
    if isinstance(value, Fraction):
        return persistence.rational_text(value)
    if isinstance(value, dict):
        return {str(key): _gap1_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_gap1_value(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    return str(value)

def gap1_failure_class(reason):
    # Method/enclosure failure class of one attempt; none of them is a mathematical counterexample.
    # Resource-cap stops are classified separately by gap1_mark_decision (failure_class = RESOURCE_CAP).
    if reason == "PASS":
        return None
    text = str(reason)
    if text.startswith("ENDPOINT:"):
        code = text.split(":", 1)[1]
        return code if code in ("ENDPOINT_NONFINITE", "ENDPOINT_PARTITION_MISMATCH") else "CERTIFICATE_INCONCLUSIVE/" + code
    if "NONFINITE" in text:
        return "NONFINITE"
    return "CERTIFICATE_INCONCLUSIVE/" + text.replace(":", "_") + "_INCONCLUSIVE"

def _gap1_attempt_reason(result):
    # the attempt's own reason, also after gap1_mark_decision replaced result["reason"] by RESOURCE_CAP:<cap>
    return (result.get("gap1") or {}).get("attempt_reason", result.get("reason"))

def gap1_root_outcome(kernel, region, result):
    # [DIFF-E] certified root outcome of one attempt: the region label only when the whole attempt holds
    # (attempt reason PASS: region body and endpoint gate), else UNRESOLVED. The X label never means "no root";
    # R additionally needs a certified T_star of target width (C1b rule).
    if _gap1_attempt_reason(result) != "PASS":
        return "UNRESOLVED"
    if region in ("L", "X"):
        return kernel.GAP1_ROOT_COUNT_LABELS[region]
    if result.get("T_star") is not None and result.get("root_reason") == "TARGET_WIDTH":
        return kernel.GAP1_ROOT_COUNT_LABELS["R"]
    return "UNRESOLVED"

GAP1_CLOSURE_DIRECT_ONLY = "DIRECT_G_BOX_ONLY"
GAP1_CLOSURE_DIRECT_AND_MONO = "DIRECT_G_BOX_AND_MONO_CLOSURE_G0_E1_V3"
GAP1_L_RULES = {
    GAP1_CLOSURE_DIRECT_ONLY:
        "g<0 on [1/2,31/32] by direct g_box enclosures only (every terminal box: g_box upper < 0); "
        "endpoint gate on [31/32,1]",
    GAP1_CLOSURE_DIRECT_AND_MONO:
        "g<0 on [1/2,31/32] by direct g_box enclosures and mono closure (box [t_l,t_r] closed by Gt<0 on "
        "[1/2,t_r] and the certified wall g(1/2)<0; d/dt g = int Gt by G0/E1 v3); endpoint gate on [31/32,1]",
}

def gap1_negative_block_closure(guards):
    # [DIFF-E] Judge ruling F4: how the terminal boxes of the L/X negative block were closed, per stage E0/E1/E2,
    # counted from the guards the exterior machinery itself recorded (baseline eval_exterior for L: direct sign
    # guards and *_MONO guards; x_negative_eval for X: X_DIRECT_G guards only). No evaluation is repeated.
    stages = {}
    for label, kind, _tl, _tr, _ll, _lr, truth in guards:
        stage = stages.setdefault(label, {"direct_g_box_evaluated": 0, "direct_g_box_closed": 0,
                                          "mono_closure_attempted": 0, "mono_closure_closed": 0})
        if str(kind).endswith("_MONO"):
            stage["mono_closure_attempted"] += 1
            stage["mono_closure_closed"] += 1 if truth else 0
        else:
            stage["direct_g_box_evaluated"] += 1
            stage["direct_g_box_closed"] += 1 if truth else 0
    direct = sum(x["direct_g_box_closed"] for x in stages.values())
    mono = sum(x["mono_closure_closed"] for x in stages.values())
    return {"stages": stages, "direct_g_box_closed": direct, "mono_closure_closed": mono,
            "method": GAP1_CLOSURE_DIRECT_AND_MONO if mono else GAP1_CLOSURE_DIRECT_ONLY}

def gap1_root_count_record(kernel, region, result, closure=None):
    # [DIFF-E] Judge ruling F2: machine-readable root count of the attempt. L: 0 roots once certified. X: NOT
    # root-free; per lambda 0 roots where g(1/2,lambda) <= 0 and one simple root in (1/2,5/8) where
    # g(1/2,lambda) > 0, the sign fixed by the C1a receipt and gate D (no T_star, no lambda_x approximation),
    # so root_count stays null. R: one root with a certified T_star. `certified` is the attempt's certificate;
    # whether the slab counts is `accepted` (set by gap1_mark_decision). F4: the L rule names the method that
    # actually closed the negative block (closure["method"]).
    label = gap1_root_outcome(kernel, region, result)
    certified = label != "UNRESOLVED"
    method = None if closure is None else closure["method"]
    if region == "L":
        return {"label": label, "certified": certified, "accepted": None, "root_count": 0 if certified else None,
                "method": method, "rule": GAP1_L_RULES[method] if (certified and method is not None) else None}
    if region == "X":
        return {"label": label, "certified": certified, "accepted": None, "root_count": None, "method": method,
                "rule": kernel.GAP1_X_ROOT_COUNT_RULE, "c1a_receipt_blob": kernel.C1A_RECEIPT_BLOB,
                "c1a_signs": [[persistence.rational_text(a), s] for a, s in kernel.C1A_GATING_SIGNS],
                "gate_D": kernel.C1A_GATE_D, "t_star_constructed": False, "lambda_x_approximation_used": False}
    return {"label": label, "certified": certified, "accepted": None, "root_count": 1 if certified else None,
            "rule": "certified T_star (root localization, TARGET_WIDTH) and attempt PASS"}

def gap1_cap_exceeded(kernel, global_work, accepted_count, accepted_work, attempted):
    # [DIFF-E] Judge ruling F3: one resource-cap test shared by the live loops, resume and replay. Caps are
    # tested in the fixed order kernel.GAP1_RESOURCE_CAPS; a cap is exceeded when value > ceiling.
    values = {"GLOBAL_ATTEMPT_WORK_CEILING": (global_work, kernel.GLOBAL_ATTEMPT_WORK_CEILING),
              "MAX_ACCEPTED": (accepted_count, kernel.MAX_ACCEPTED),
              "ACCEPTED_WORK_CEILING": (accepted_work, kernel.ACCEPTED_WORK_CEILING),
              "MAX_ATTEMPTED": (attempted, kernel.MAX_ATTEMPTED)}
    for cap in kernel.GAP1_RESOURCE_CAPS:
        value, ceiling = values[cap]
        if value > ceiling:
            return cap
    return None

def gap1_cap_stop(cap, attempt_failure_class):
    # [DIFF-E] segment_end fields of a resource-cap stop.
    return {"reason": "RESOURCE_CAP", "failure_class": "RESOURCE_CAP", "resource_cap": cap,
            "abort_cause": "RESOURCE_CAP", "attempt_failure_class": attempt_failure_class}

GAP1_NON_CAP_ABORT_CAUSES = ("MAX_DEPTH_EXHAUSTED", "PRODUCER_PLAN_ABORT")

def gap1_mark_decision(result, decision, cap, abort_cause):
    # [DIFF-E] record why a slab_record is terminal. The attempt's own reason and class stay in
    # gap1.attempt_reason / gap1.attempt_failure_class. A cap stop sets reason = RESOURCE_CAP:<cap> and
    # failure_class = RESOURCE_CAP; no record ever pairs reason PASS with an ABORT. Returns segment_end fields.
    gap1 = result["gap1"]
    gap1["attempt_reason"] = result.get("reason")
    gap1["attempt_failure_class"] = gap1["failure_class"]
    gap1["abort_cause"] = None
    gap1["resource_cap"] = None
    gap1["root_count"]["accepted"] = decision == "ACCEPT"
    if cap is not None:
        if decision != "ABORT":
            raise SystemExit("CONTRACT_MISMATCH:CAP_WITHOUT_ABORT")
        gap1["abort_cause"] = "RESOURCE_CAP"
        gap1["resource_cap"] = cap
        gap1["failure_class"] = "RESOURCE_CAP"
        result["reason"] = "RESOURCE_CAP:" + cap
        return gap1_cap_stop(cap, gap1["attempt_failure_class"])
    if decision != "ABORT":
        return None
    if abort_cause not in GAP1_NON_CAP_ABORT_CAUSES:
        raise SystemExit("CONTRACT_MISMATCH:ABORT_WITHOUT_CAUSE")
    if gap1["attempt_reason"] == "PASS":
        if abort_cause != "PRODUCER_PLAN_ABORT":
            raise SystemExit("CONTRACT_MISMATCH:ABORT_WITHOUT_CAUSE")
        # checker: the producer stopped on this slab, the checker's own attempt passed and no cap of the
        # checker's own counters explains the stop -> recorded as a contract mismatch, never as PASS.
        gap1["failure_class"] = "CONTRACT_MISMATCH"
        result["reason"] = "CONTRACT_MISMATCH:PLAN_ABORT_NOT_REPRODUCED"
    gap1["abort_cause"] = abort_cause
    return {"reason": "failure", "failure_class": gap1["failure_class"], "resource_cap": None,
            "abort_cause": abort_cause, "attempt_failure_class": gap1["attempt_failure_class"]}

def gap1_terminal_abort(kernel, terminal, decision_key):
    # [DIFF-E] resume / replay: a terminal ABORT record is re-classified from its own counters with the same
    # cap test; the stored classification must match, and the stop is re-raised with it.
    for payload in terminal:
        if payload.get(decision_key) != "ABORT":
            continue
        if payload is not terminal[-1]:
            raise SystemExit("CONTRACT_MISMATCH:ABORT_NOT_LAST")
        result = payload["result"]
        gap1 = result["gap1"]
        attempt_reason = gap1.get("attempt_reason")
        cap = gap1_cap_exceeded(kernel, int(payload["cumulative_work_after"]), int(payload["cap_test_accepted_count"]),
                                int(payload["cap_test_accepted_work"]), int(payload["attempted_count"]))
        cause = gap1.get("abort_cause")
        if cap is not None:
            expected = ("RESOURCE_CAP", cap, "RESOURCE_CAP", "RESOURCE_CAP:" + cap)
        elif cause == "MAX_DEPTH_EXHAUSTED" and int(payload["refinement_depth"]) >= kernel.MAX_DEPTH and attempt_reason != "PASS":
            expected = (cause, None, gap1.get("attempt_failure_class"), attempt_reason)
        elif cause == "PRODUCER_PLAN_ABORT" and decision_key == "checker_decision":
            expected = (cause, None, "CONTRACT_MISMATCH", "CONTRACT_MISMATCH:PLAN_ABORT_NOT_REPRODUCED")                 if attempt_reason == "PASS" else (cause, None, gap1.get("attempt_failure_class"), attempt_reason)
        else:
            raise SystemExit("CONTRACT_MISMATCH:ABORT_CLASSIFICATION")
        stored = (cause, gap1.get("resource_cap"), gap1.get("failure_class"), result.get("reason"))
        if stored != expected or gap1.get("attempt_failure_class") != gap1_failure_class(attempt_reason)                 or (gap1.get("root_count") or {}).get("accepted") is not False:
            raise SystemExit("CONTRACT_MISMATCH:ABORT_CLASSIFICATION")
        raise SystemExit("LEDGER_TERMINAL_ABORT:" + ("RESOURCE_CAP:" + cap if cap is not None else cause))

def gap1_counts_accepted(payload):
    # [DIFF-E] F5 / B2: a slab_record counts as accepted iff decision is ACCEPT and (checker) the checker itself
    # did not stop on it. The same rule is used by the driver's resume_state.
    return payload["decision"] == "ACCEPT" and payload.get("checker_decision", "REPLAYED") != "ABORT"

def gap1_ledger_count_audit(records):
    # [DIFF-E] F5: walk the ledger in order and rebuild attempted / global work / accepted count / accepted work
    # exactly as persistence.resume_state does; every slab_record must carry the same values, and an ABORT record
    # must leave the accepted counters unchanged (its candidate values live in cap_test_*).
    attempted = global_work = accepted_count = accepted_work = 0
    for record in records:
        kind, payload = record["record_type"], record["payload"]
        if kind == "attempt_begin":
            attempted += 1
        elif kind == "interrupted_attempt_charge":
            global_work += int(payload["charged_work"])
        elif kind == "slab_record":
            if payload.get("checker_decision", "REPLAYED") not in ("REPLAYED", "ABORT"):
                raise SystemExit("CONTRACT_MISMATCH:CHECKER_DECISION_VALUE:" + str(payload["attempt_sequence"]))
            work = int(payload["result"]["work_total"])
            global_work += work
            if gap1_counts_accepted(payload):
                accepted_count += 1
                accepted_work += work
            stored = (int(payload["attempted_count"]), int(payload["cumulative_work_after"]),
                      int(payload["accepted_count"]), int(payload["accepted_work"]))
            if stored != (attempted, global_work, accepted_count, accepted_work):
                raise SystemExit("CONTRACT_MISMATCH:LEDGER_COUNT_AUDIT:" + str(payload["attempt_sequence"]))
            if (payload["result"]["gap1"]["root_count"] or {}).get("accepted") is not gap1_counts_accepted(payload):
                raise SystemExit("CONTRACT_MISMATCH:ACCEPTED_FLAG:" + str(payload["attempt_sequence"]))
    return {"attempted": attempted, "global_work": global_work,
            "accepted_count": accepted_count, "accepted_work": accepted_work}

def gap1_serialize_record(kernel, slab, rec, tc, mode, work, reason, trace):
    # [DIFF-E] U1 ledger record: baseline fields (R keeps the executed C1b serialization; L/X keep every
    # predictor/root field null) plus region, diff categories, region guards and the endpoint certificate.
    region = kernel.gap1_region(slab.ll, slab.lr)
    if region == "R":
        result = serialize_record(rec, tc, mode, work, reason, trace)
    else:
        result = serialize_record(None, None, None, work, reason, trace)
        for key in GAP1_PREDICTOR_ROOT_FIELDS:
            if result.get(key) is not None:
                raise SystemExit("CONTRACT_MISMATCH:LX_PREDICTOR_FIELD_NONNULL:" + key)
        if result.get("root_mv_steps") or tc is not None or mode is not None:
            raise SystemExit("CONTRACT_MISMATCH:LX_PREDICTOR_FIELD_NONNULL")
        if rec is not None:
            result["exterior_guards"] = [_serialize_guard(x) for x in rec.get("exterior_guards", ())]
            result["exterior_nonfinite"] = [_serialize_nonfinite(x) for x in rec.get("exterior_nonfinite", ())]
    if region == "R" and result.get("predictor_mode") not in GAP1_ALLOWED_R_MODES:
        raise SystemExit("PREDICTOR_RULE_MISMATCH:" + str(result.get("predictor_mode")))
    gap1 = {
        "region": region,
        "diff_categories_used": list(kernel.GAP1_DIFF_CATEGORIES_BY_REGION[region]),
        "region_pieces": None,
        "x_lower_tube_stage": None, "x_lower_tube_guards": [], "x_lower_tube_nonfinite": [],
        "endpoint": None,
        "root_count": None,
        "failure_class": gap1_failure_class(reason),
    }
    closure = None
    if rec is not None and region in ("L", "X"):
        closure = gap1_negative_block_closure(rec.get("exterior_guards", ()))
        if region == "X" and (closure["mono_closure_closed"] or any(
                x["mono_closure_attempted"] for x in closure["stages"].values())):
            raise SystemExit("CONTRACT_MISMATCH:X_MONO_CLOSURE")
    gap1["negative_block_closure"] = closure
    gap1["root_count"] = gap1_root_count_record(kernel, region, result, closure)
    if rec is not None:
        if region in ("L", "X"):
            gap1["region_pieces"] = _gap1_value(rec.get("pieces"))
        if region == "X":
            gap1["x_negative_method"] = rec.get("x_negative_method")
            gap1["x_lower_tube_stage"] = rec.get("x_lower_tube_stage")
            gap1["x_lower_tube_guards"] = [_serialize_guard(x) for x in rec.get("x_lower_tube_guards", ())]
            gap1["x_lower_tube_nonfinite"] = [_serialize_nonfinite(x) for x in rec.get("x_lower_tube_nonfinite", ())]
        if rec.get("endpoint") is not None:
            gap1["endpoint"] = _gap1_value(rec["endpoint"])
    result["gap1"] = gap1
    return result

def gap1_exact_union(accepted, kernel):
    # [DIFF-E] exact union of the accepted slabs over [2/5,9/20], independent of processing order.
    ordered = sorted(accepted, key=lambda p: Fraction(p["lambda_lo"]))
    ok = bool(ordered)
    if ok:
        ok = ordered[0]["lambda_lo"] == persistence.rational_text(kernel.GAP1_LAMBDA_LO)
        ok = ok and ordered[-1]["lambda_hi"] == persistence.rational_text(kernel.GAP1_LAMBDA_HI)
        ok = ok and all(a["lambda_hi"] == b["lambda_lo"] for a, b in zip(ordered, ordered[1:]))
    return ok

def gap1_boundary_overlap(accepted, kernel):
    # [DIFF-E] owners and overlap checks: 83/200 X owner / L overlap (root count 0 both sides, g(1/2)<0);
    # 703/1600 R owner / X overlap (root count 1 both sides, R T_* meets (1/2,5/8)); 9/20 consistency only.
    def touching(edge, side):
        key = "lambda_hi" if side == "below" else "lambda_lo"
        return [p for p in accepted if Fraction(p[key]) == edge]
    signs = dict(kernel.C1A_GATING_SIGNS)
    out = {}
    below, above = touching(kernel.GAP1_X_LO, "below"), touching(kernel.GAP1_X_LO, "above")
    ok1 = (len(below) == 1 and len(above) == 1 and below[0]["result"]["gap1"]["region"] == "L"
           and above[0]["result"]["gap1"]["region"] == "X" and signs[kernel.GAP1_C1A_NEG_POINT] < 0)
    out["lambda_83_200"] = {"owner": "X", "overlap": "L", "root_count_owner": 0 if signs[kernel.GAP1_C1A_NEG_POINT] < 0 else None,
                              "root_count_overlap": 0, "g_half_sign_owner_c1a": signs[kernel.GAP1_C1A_NEG_POINT],
                              "g_half_sign_overlap_certificate": -1, "pass": bool(ok1)}
    below, above = touching(kernel.GAP1_X_HI, "below"), touching(kernel.GAP1_X_HI, "above")
    star = None if len(above) != 1 else above[0]["result"].get("T_star")
    meets = False
    if star is not None:
        a, b = Fraction(star[0]), Fraction(star[1])
        meets = max(a, kernel.T_LO) < min(b, kernel.GAP1_X_SPLIT_T)
    ok2 = (len(below) == 1 and len(above) == 1 and below[0]["result"]["gap1"]["region"] == "X"
           and above[0]["result"]["gap1"]["region"] == "R" and signs[kernel.GAP1_C1A_POS_POINT] > 0 and meets)
    out["lambda_703_1600"] = {"owner": "R", "overlap": "X", "root_count_owner": 1 if star is not None else None,
                             "root_count_overlap": 1 if signs[kernel.GAP1_C1A_POS_POINT] > 0 else None,
                             "owner_T_star": star, "T_star_meets_open_1_2_5_8": bool(meets), "pass": bool(ok2)}
    top = touching(kernel.GAP1_LAMBDA_HI, "below")
    endpoint_ok = (len(top) == 1 and top[0]["result"]["gap1"]["region"] == "R"
                   and (top[0]["result"]["gap1"].get("endpoint") or {}).get("endpoint_pass") is True)
    out["lambda_9_20"] = {"owner": "C1b_or_gap2", "role": "boundary_consistency_only",
                          "bob_sign_consistency": "CONSISTENT" if endpoint_ok else "NOT_ESTABLISHED",
                          "bob_receipt_blob": kernel.BOB_RECEIPT_BLOB, "pass": bool(endpoint_ok)}
    return out

def gap1_overlap_failure(overlap):
    if overlap is None:
        return None
    if not (overlap["lambda_83_200"]["pass"] and overlap["lambda_703_1600"]["pass"]):
        return "CONTRACT_MISMATCH:BOUNDARY_OVERLAP"
    if not overlap["lambda_9_20"]["pass"]:
        return "BOB_SIGN_CONSISTENCY_FAILED"
    return None

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

def _serialize_nonfinite(rec):
    tl, tr = rec["t"]; ll, lr = rec["lambda"]
    return {
        "kind": rec["kind"], "detail": rec.get("detail"),
        "evaluator": rec["evaluator"], "side": rec["side"], "stage": rec["stage"],
        "depth": int(rec["depth"]),
        "t_lo": persistence.rational_text(tl), "t_hi": persistence.rational_text(tr),
        "lambda_lo": persistence.rational_text(ll), "lambda_hi": persistence.rational_text(lr),
    }

def _serialize_root_refinement(refinements):
    out = []
    for ref in refinements:
        item = {
            "cell_index": int(ref["cell_index"]),
            "parent_t_cell": _rr(ref["parent_t_cell"]),
            "levels": [],
        }
        for level in ref.get("levels", []):
            item["levels"].append({
                "level": int(level["level"]),
                "children": [{
                    "t_cell": _rr(child["t_cell"]),
                    "Gt": child["Gt"],
                    "guard": bool(child["guard"]),
                    "work": int(child["work"]),
                } for child in level.get("children", [])],
            })
        out.append(item)
    return out


def _serialize_tube_refinement(refinements):
    out = []
    for ref in refinements:
        item = {
            "parent_t_cell": _rr(ref["parent_t_cell"]),
            "closed_depth": None if ref.get("closed_depth") is None else int(ref["closed_depth"]),
            "levels": [],
        }
        for level in ref.get("levels", []):
            children = []
            for child in level.get("children", []):
                children.append({
                    "role": str(child["role"]),
                    "t_cell": _rr(child["t_cell"]),
                    "all_finite": bool(child["all_finite"]),
                    "all_guard": bool(child["all_guard"]),
                    "subcells": [{
                        "t_cell": _rr(cell["t_cell"]),
                        "lambda_cell": _rr(cell["lambda_cell"]),
                        "finite": bool(cell["finite"]),
                        "Gt_upper": cell["Gt_upper"],
                        "guard": bool(cell["guard"]),
                        "work": int(cell["work"]),
                    } for cell in child.get("subcells", [])],
                })
            item["levels"].append({"level": int(level["level"]), "children": children})
        out.append(item)
    return out

def _serialize_gl_corner_certificate(cert):
    if cert is None:
        return None
    def convert(value):
        if isinstance(value, Fraction):
            return persistence.rational_text(value)
        if isinstance(value, dict):
            return {key: convert(item) for key, item in value.items()}
        if isinstance(value, list):
            return [convert(item) for item in value]
        if isinstance(value, tuple):
            return [convert(item) for item in value]
        return value
    return convert(cert)

def serialize_mv_step(step):
    if int(step["step"]) == 0:
        return {
            "step": 0,
            "step_work": int(step["step_work"]),
            **({"Gl_corner_certificate": _serialize_gl_corner_certificate(step["Gl_corner_certificate"])}
               if "Gl_corner_certificate" in step else {}),
        }
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
            "final_guard": bool(cell.get("final_guard", cell["guard"])),
            "corner_hull": int(cell["corner_hull"]),
            "work": int(cell["work"]),
        } for cell in step.get("Gt_cells", [])],
        "Gt_refinement": _serialize_root_refinement(step.get("Gt_refinement", [])),
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
        "nonfinite": step.get("nonfinite"),
        **({"Gl_corner_certificate": _serialize_gl_corner_certificate(step["Gl_corner_certificate"])}
           if "Gl_corner_certificate" in step else {}),
    }

def serialize_record(rec, tc, mode, work, reason, trace):
    empty = {
        "predictor_mode": mode,
        "t_c": None if tc is None else persistence.rational_text(tc),
        "T_star": None, "left_clamp": None, "right_clamp": None,
        "t_minus": None, "t_plus": None, "T_0": None,
        "root_gt_t_cells": 16, "corner_hull": None, "corner_boxes": [],
        "tube_stage": None, "tube_guards": [], "tube_nonfinite": [], "tube_refinement": [],
        "exterior_guards": [], "exterior_nonfinite": [], "predictor_nonfinite": [],
        "sup_error": None, "middle_partition": None,
        "work": {k: int(v) for k, v in work.items()},
        "work_total": int(sum(work.values())), "reason": reason, "trace": trace,
        "root_mv_steps": [], "root_reason": None,
    }
    if rec is None:
        return empty
    empty["predictor_nonfinite"] = [_serialize_nonfinite(x) for x in rec.get("predictor_nonfinite", ())]
    if rec.get("predictor_only"):
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
        "tube_nonfinite": [_serialize_nonfinite(x) for x in rec.get("tube_nonfinite", ())],
        "tube_refinement": _serialize_tube_refinement(rec.get("tube_refinement", [])),
        "exterior_guards": [_serialize_guard(x) for x in rec.get("exterior_guards", ())],
        "exterior_nonfinite": [_serialize_nonfinite(x) for x in rec.get("exterior_nonfinite", ())],
        "sup_error": None if rec["sup_error"] is None else persistence.rational_text(rec["sup_error"]),
        "root_mv_steps": [serialize_mv_step(x) for x in rec.get("root_steps", [])],
        "root_reason": rec.get("root_reason"),
        "middle_partition": [[kind, persistence.rational_text(lo), persistence.rational_text(hi)] for kind, lo, hi in rec["pieces"]],
    })
    return empty

REPLAY_SCHEMA = "GAP1_A1_REPLAY_V0"
REPLAY_KEYS = {
    "schema", "attempt_sequence", "coarse_index", "refinement_depth",
    "lambda_lo", "lambda_hi", "tree_node", "t_c", "left_clamp",
    "right_clamp", "t_minus", "t_plus", "T_0", "root_gt_t_cells",
    "producer_accept_root_outcome", "decision",
}
FORBIDDEN_REPLAY_KEYS = {"T_star", "G0", "Gt", "Gl", "Gpar", "N_k", "root_mv_steps"}

def gap1_plan_order_audit(plan, kernel):
    # [DIFF-A] independent audit of the producer tree order: decreasing-lambda coarse queue and
    # right-child-first REFINE insertion, recomputed from exact rationals and the plan decisions only.
    slabs, ok = kernel.gap1_coarse_slabs()
    if not ok:
        raise SystemExit("CONTRACT_MISMATCH:GAP1_COARSE_LEDGER")
    queue = [(s.coarse, s.depth, s.ll, s.lr) for s in reversed(slabs)]
    for line_no, item in enumerate(plan, 1):
        if not queue:
            raise SystemExit(f"CONTRACT_MISMATCH:PLAN_EXTRA_SLAB line={line_no}")
        coarse, depth, ll, lr = queue.pop(0)
        if (int(item["coarse_index"]), int(item["refinement_depth"]),
                Fraction(item["lambda_lo"]), Fraction(item["lambda_hi"])) != (coarse, depth, ll, lr):
            raise SystemExit(f"CONTRACT_MISMATCH:PLAN_ORDER line={line_no}")
        if item["decision"] == "REFINE":
            mid = (ll + lr) / 2
            queue = [(coarse, depth + 1, mid, lr), (coarse, depth + 1, ll, mid)] + queue
    print("GAP1_PLAN_ORDER_AUDIT", "PASS", "items", len(plan), "remaining", len(queue))

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

def verify_gap1_lx_fields(item, result):
    # [DIFF-E] L/X replay items carry no predictor/root data on either side.
    for key in ("t_c", "left_clamp", "right_clamp", "t_minus", "t_plus", "T_0", "producer_accept_root_outcome"):
        if item.get(key) is not None:
            raise SystemExit("CONTRACT_MISMATCH:LX_REPLAY_FIELD_NONNULL:" + key)
    if result.get("t_c") is not None or result.get("T_star") is not None:
        raise SystemExit("CONTRACT_MISMATCH:LX_RESULT_FIELD_NONNULL")

def slab_from_plan(item, kernel):
    return kernel.Slab(int(item["coarse_index"]), int(item["refinement_depth"]),
                       Fraction(item["lambda_lo"]), Fraction(item["lambda_hi"]))

def replay_state(records, plan, kernel):
    persisted = persistence.resume_state(records)
    terminal = persisted["terminal"]
    gap1_ledger_count_audit(records)
    gap1_terminal_abort(kernel, terminal, "checker_decision")
    if len(terminal) > len(plan):
        raise SystemExit("CHECKER_LEDGER_EXCEEDS_REPLAY_PLAN")
    previous_root = None
    for index, payload in enumerate(terminal):
        item = plan[index]
        if payload.get("plan_attempt_sequence") != item["attempt_sequence"]:
            raise SystemExit("A1_REPLAY_PLAN_ATTEMPT_SEQUENCE_MISMATCH")
        for key in ("coarse_index", "refinement_depth", "lambda_lo", "lambda_hi"):
            if payload.get(key) != item[key]:
                raise SystemExit("A1_REPLAY_SLAB_MISMATCH")
        if payload.get("decision") != item["decision"]:
            raise SystemExit("A1_REPLAY_DECISION_MISMATCH")
        if item["decision"] == "ACCEPT":
            root = payload["result"].get("T_star")
            if root is None and payload["result"]["gap1"]["region"] == "R":
                raise SystemExit("CHECKER_REPLAY_UNRESOLVED")
            previous_root = None if root is None else tuple(Fraction(x) for x in root)
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
    root = kernel.ROOT_GL_CORNER_WALL_PANELS + kernel.ROOT_MV_STEPS * (kernel.ROOT_G_PANELS + kernel.ROOT_GT_T_CELLS * kernel.ROOT_GT_PANELS + kernel.ROOT_GL_T_CELLS * kernel.ROOT_GL_PANELS)
    e0 = kernel.E0_TBOXES * kernel.E0_LBOXES * kernel.E_STAGES[0][1]
    early = kernel.GAP1_N_COARSE * (predictor + t0 + root + e0)
    no_refine_late = kernel.GAP1_N_COARSE * (
        predictor + kernel.ATTEMPT_WORK_CEILING
    )
    return {
        "coarse_slabs": kernel.GAP1_N_COARSE,
        "predictor_per_attempt": predictor,
        "T0_E0_early_pass_one_lineage": early,
        "T2_E2_no_refinement_one_lineage": no_refine_late,
        "accepted_gating_ceiling": kernel.ACCEPTED_WORK_CEILING,
        "global_attempted_gating_ceiling": kernel.GLOBAL_ATTEMPT_WORK_CEILING,
    }


def gap1_header(kernel):
    # [DIFF-K] U1 contract metadata transcribed into the ledger header.
    return {
        "contract_id": kernel.GAP1_CONTRACT_ID,
        "authority_sha256": dict(kernel.GAP1_AUTHORITY_SHA256),
        "baseline_commit": kernel.GAP1_BASELINE_COMMIT,
        "baseline_blobs": dict(kernel.GAP1_BASELINE_BLOBS),
        "import_closure_17": dict(kernel.GAP1_IMPORT_CLOSURE_17),
        "regions": [["L", persistence.rational_text(kernel.GAP1_LAMBDA_LO), persistence.rational_text(kernel.GAP1_X_LO), 48],
                    ["X", persistence.rational_text(kernel.GAP1_X_LO), persistence.rational_text(kernel.GAP1_X_HI), 78],
                    ["R", persistence.rational_text(kernel.GAP1_X_HI), persistence.rational_text(kernel.GAP1_LAMBDA_HI), 34]],
        "dlambda": persistence.rational_text(kernel.GAP1_DLAM),
        "coarse": kernel.GAP1_N_COARSE,
        "direction": kernel.GAP1_DIRECTION,
        "refine_order": "right_child_first",
        "x_split_t": persistence.rational_text(kernel.GAP1_X_SPLIT_T),
        "x_t_stages": [list(x) for x in kernel.GAP1_X_T_STAGES],
        "endpoint": {"partition_id": kernel.ENDPOINT_PARTITION_ID,
                     "seed_t": persistence.rational_text(kernel.ENDPOINT_T_SEED),
                     "dt": persistence.rational_text(kernel.ENDPOINT_DT), "boxes": kernel.ENDPOINT_N_BOXES,
                     "seed_panels": kernel.ENDPOINT_SEED_PANELS, "gt_panels": kernel.ENDPOINT_GT_PANELS},
        "c1a": {"receipt_blob": kernel.C1A_RECEIPT_BLOB,
                "signs": [[persistence.rational_text(a), s] for a, s in kernel.C1A_GATING_SIGNS],
                "gate_D": kernel.C1A_GATE_D},
        "ownership": {"83/200": "X", "703/1600": "R", "9/20": "consistency_only",
                      "t=5/8": "X_negative_block", "t=31/32": "endpoint_seed"},
        "failure_codes": list(kernel.GAP1_FAILURE_CODES),
        "diff_categories_by_region": {k: list(v) for k, v in kernel.GAP1_DIFF_CATEGORIES_BY_REGION.items()},
        "x_negative_method": kernel.GAP1_X_NEGATIVE_METHOD,
        "root_count_labels": dict(kernel.GAP1_ROOT_COUNT_LABELS),
        "x_root_count_rule": kernel.GAP1_X_ROOT_COUNT_RULE,
        "resource_caps_priority": list(kernel.GAP1_RESOURCE_CAPS),
        "read_only_pins": dict(kernel.GAP1_READ_ONLY_PINS),
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
        "lambda_domain": [persistence.rational_text(kernel.GAP1_LAMBDA_LO), persistence.rational_text(kernel.GAP1_LAMBDA_HI)],
        "gap1": gap1_header(kernel),
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
            "coarse": kernel.GAP1_N_COARSE,
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
    gap1_plan_order_audit(plan, kernel)
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
    state = replay_state(ledger.records, plan, kernel)
    full_charge = kernel.ATTEMPT_WORK_CEILING + 513 * 2 * kernel.PRED_SCAN_PANELS
    for seq in state["unmatched"]:
        ledger.append("interrupted_attempt_charge", {
            "attempt_sequence": seq, "charged_work": full_charge,
            "charged_attempt_unit": 1, "utc": persistence.utc_now(),
        })
    if state["unmatched"]:
        state = replay_state(ledger.records, plan, kernel)
    # [DIFF-E] resume-time cap test moved after segment_begin so that the stop is recorded (F3).
    segment_index = persistence.next_segment_index(ledger.records)
    next_item = None if state["plan_index"] >= len(plan) else plan[state["plan_index"]]
    ledger.append("segment_begin", {
        "segment_index": segment_index, "utc": persistence.utc_now(), "pin_check": "PASS",
        "identity": identity, "replay_sha256": replay_sha256,
        "producer_ledger_sha256": producer_ledger_sha256,
        "cumulative_work": state["global_work"], "attempted": state["attempted"],
        "next_slab": None if next_item is None else slab_payload(slab_from_plan(next_item, kernel)),
    })
    gap1_stop = None  # [DIFF-E] segment_end fields of a terminal ABORT / resource-cap stop (F3)
    def append_segment_end(reason, cumulative_work, attempted, **extra):
        post_identity = persistence.environment_snapshot(pins[lineage])
        persistence.verify_identity(post_identity, pins[lineage])
        payload = {
            "segment_index": segment_index, "utc": persistence.utc_now(), "reason": reason,
            "cumulative_work": cumulative_work, "attempted": attempted, "post_pin_check": "PASS",
            "post_identity": post_identity, "replay_sha256": replay_sha256,
            "producer_ledger_sha256": producer_ledger_sha256,
        }
        payload.update(extra)
        # [DIFF-E] F3: a terminal stop adds its classification; after a RESOURCE_CAP segment_end the run stops here.
        if gap1_stop is not None:
            payload.update(gap1_stop)
        ledger.append("segment_end", payload)
        if gap1_stop is not None and gap1_stop["abort_cause"] == "RESOURCE_CAP":
            raise SystemExit("RESOURCE_CAP:" + gap1_stop["resource_cap"])
    resume_cap = gap1_cap_exceeded(kernel, state["global_work"], len(state["accepted"]),
                                   state["accepted_work"], state["attempted"])
    if resume_cap is not None:
        gap1_stop = gap1_cap_stop(resume_cap, None)
        append_segment_end("failure", state["global_work"], state["attempted"])
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
        next_cap = gap1_cap_exceeded(kernel, global_work, accepted_count, accepted_work, attempted + 1)
        if next_cap is not None:
            gap1_stop = gap1_cap_stop(next_cap, None)
            append_segment_end("failure", global_work, attempted, next_slab=slab_payload(slab_from_plan(item, kernel)))
        slab = slab_from_plan(item, kernel)
        attempted += 1; attempt_sequence = attempted
        expected_tc = None if item["t_c"] is None else Fraction(item["t_c"])
        ledger.append("attempt_begin", {
            "attempt_sequence": attempt_sequence, "plan_attempt_sequence": item["attempt_sequence"], **slab_payload(slab),
            "replay_decision": item["decision"], "previous_root": serialize_root(previous_root),
            "cumulative_work_before": global_work, "utc": persistence.utc_now(),
        })
        tee = Tee(sys.stdout)
        with contextlib.redirect_stdout(tee):
            ok, rec, root, tc, work, reason = kernel.attempt_replay_gap1(slab, previous_root, expected_tc)
        trace = parse_trace(tee.lines)
        result = gap1_serialize_record(kernel, slab, rec, tc, None if rec is None else rec["mode"], work, reason, trace)
        region = result["gap1"]["region"]
        if region == "R":
            verify_a1_fields(item, result)
        else:
            verify_gap1_lx_fields(item, result)
        attempt_work = result["work_total"]; global_work += attempt_work
        fixed_decision = item["decision"]
        root_outcome = gap1_root_outcome(kernel, region, result)
        cap = gap1_cap_exceeded(kernel, global_work, accepted_count, accepted_work, attempted)
        # [DIFF-E] F5: candidate counters for the cap test; the committed counters advance only on acceptance.
        cap_test_accepted_count, cap_test_accepted_work = accepted_count, accepted_work
        if cap is None and fixed_decision == "ACCEPT":
            if root_outcome != kernel.GAP1_ROOT_COUNT_LABELS[region]:
                raise SystemExit("CHECKER_REPLAY_UNRESOLVED")
            if not ok:
                raise SystemExit("CHECKER_REPLAY_ACCEPT_FAILURE:" + reason)
            cap_test_accepted_count, cap_test_accepted_work = accepted_count + 1, accepted_work + attempt_work
            cap = gap1_cap_exceeded(kernel, global_work, cap_test_accepted_count, cap_test_accepted_work, attempted)
            if cap is None:
                accepted_count, accepted_work = cap_test_accepted_count, cap_test_accepted_work
                previous_root = root
        plan_abort_cause = None
        if cap is None and fixed_decision == "ABORT":
            # [DIFF-E] F3/F5: the producer stopped on this slab. A passing checker attempt is cap-tested on the
            # candidate counters exactly as the producer tests them (never committed); a failing one at depth 3 is
            # MAX_DEPTH_EXHAUSTED; anything the checker's own counters do not explain is PRODUCER_PLAN_ABORT.
            if ok:
                cap_test_accepted_count, cap_test_accepted_work = accepted_count + 1, accepted_work + attempt_work
                cap = gap1_cap_exceeded(kernel, global_work, cap_test_accepted_count, cap_test_accepted_work, attempted)
            plan_abort_cause = ("MAX_DEPTH_EXHAUSTED" if (not ok and slab.depth >= kernel.MAX_DEPTH)
                                else "PRODUCER_PLAN_ABORT")
        checker_decision = "ABORT" if (cap is not None or fixed_decision == "ABORT") else "REPLAYED"
        gap1_stop = gap1_mark_decision(result, "ABORT" if checker_decision == "ABORT" else fixed_decision, cap,
                                       plan_abort_cause)
        payload = {
            "attempt_sequence": attempt_sequence, "plan_attempt_sequence": item["attempt_sequence"], **slab_payload(slab),
            "decision": fixed_decision, "checker_decision": checker_decision,
            "checker_full_ok": bool(ok), "checker_reason": result["reason"],
            "checker_root_outcome": root_outcome, "result": result,
            "accepted_count": accepted_count, "accepted_work": accepted_work,
            "cap_test_accepted_count": cap_test_accepted_count, "cap_test_accepted_work": cap_test_accepted_work,
            "cumulative_work_after": global_work, "attempted_count": attempted,
            "a1_label": "A1_EXACT_EQUALITY",
            "a2_label": "A2_LINEAGE_INDEPENDENT",
            "utc": persistence.utc_now(),
        }
        ledger.append("slab_record", payload)
        index += 1
        if gap1_stop is not None:
            append_segment_end("failure", global_work, attempted)
            raise SystemExit("CHECKER_TERMINAL_ABORT:" + gap1_stop["abort_cause"])
    accepted_plan = [x for x in plan if x["decision"] == "ACCEPT"]
    union_ok = gap1_exact_union(accepted_plan, kernel)
    checker_accepted = [r["payload"] for r in ledger.records if r["record_type"] == "slab_record"
                        and r["payload"]["decision"] == "ACCEPT"]
    overlap = gap1_boundary_overlap(checker_accepted, kernel) if union_ok else None
    overlap_failure = gap1_overlap_failure(overlap)
    union_ok = union_ok and overlap_failure is None
    append_segment_end("completed" if union_ok else "failure", global_work, attempted,
                       accepted=accepted_count, exact_union=union_ok, gap1_boundary_overlap=overlap,
                       final_record_hash_before_end=ledger.last_hash)
    print("C1B_CHECKER_FIXED_REPLAY_FINAL", "PASS" if union_ok else "UNRESOLVED",
          "accepted", accepted_count, "attempted", attempted, "work", global_work,
          "ledger_hash", ledger.last_hash, "replay_sha256", replay_sha256,
          "producer_ledger_sha256", producer_ledger_sha256)
    if overlap_failure is not None:
        raise SystemExit(overlap_failure)
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
