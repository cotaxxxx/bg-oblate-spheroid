#!/usr/bin/env python3
"""Fail-closed A.1/A.2/A.3 comparison for the two-phase C1b replay."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from analysis import c1b_resumable_driver as persistence

REPLAY_SCHEMA = "C1B_A1_REPLAY_V2_3_1"
PRED_ACCEPT = Fraction(1, 64)
ROOT_TARGET = Fraction(1, 128)
ROOT_GT_T_CELLS = 16
A1_KEYS = (
    "attempt_sequence", "tree_node",
    "coarse_index", "refinement_depth", "lambda_lo", "lambda_hi", "decision",
    "t_c", "left_clamp", "right_clamp", "t_minus", "t_plus", "T_0",
    "root_gt_t_cells", "corner_boxes", "tube_stage", "tube_guards", "exterior_guards",
)
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_plan(path):
    data = Path(path).read_bytes()
    out = []
    for line_no, raw in enumerate(data.splitlines(), 1):
        obj = json.loads(raw.decode("utf-8"))
        if obj.get("schema") != REPLAY_SCHEMA:
            raise SystemExit(f"COMPARE_REPLAY_SCHEMA_FAIL line={line_no}")
        forbidden = {"T_star", "G0", "Gt", "Gl", "Gpar", "N_k", "root_mv_steps"}
        if forbidden.intersection(obj):
            raise SystemExit(f"COMPARE_REPLAY_A2_LEAK line={line_no}")
        out.append(obj)
    if not out:
        raise SystemExit("COMPARE_REPLAY_EMPTY")
    return out


def slab_records(ledger):
    return [r["payload"] for r in ledger.records if r["record_type"] == "slab_record"]
def exact_mid(root):
    return (Fraction(root[0]) + Fraction(root[1])) / 2


def a3_record(plan_item, producer_result, checker_result):
    proot = producer_result.get("T_star")
    croot = checker_result.get("T_star")
    if proot is None or croot is None:
        raise SystemExit("A3_MISSING_T_STAR")
    plo, phi = map(Fraction, proot)
    clo, chi = map(Fraction, croot)
    overlap = max(plo, clo) <= min(phi, chi)
    tc = Fraction(plan_item["t_c"])
    perr = abs(tc - exact_mid(proot))
    cerr = abs(tc - exact_mid(croot))
    pacc = perr <= PRED_ACCEPT
    cacc = cerr <= PRED_ACCEPT
    if not overlap:
        raise SystemExit("A3_DISJOINT_T_STAR")
    if not (pacc and cacc):
        raise SystemExit("A3_DUAL_PREDICTOR_ACCEPT_FAIL")
    return {
        "T_star_intersection_nonempty": overlap,
        "producer_midpoint_error": persistence.rational_text(perr),
        "checker_midpoint_error": persistence.rational_text(cerr),
        "producer_midpoint_accept": pacc,
        "checker_midpoint_accept": cacc,
        "threshold": persistence.rational_text(PRED_ACCEPT),
    }
def compare_one(index, plan_item, producer_payload, checker_payload):
    pr = producer_payload["result"]
    cr = checker_payload["result"]
    a1 = {}
    for key in A1_KEYS:
        expected = plan_item.get(key)
        if key == "tree_node":
            pv = f'{producer_payload["coarse_index"]}:{producer_payload["refinement_depth"]}:{producer_payload["lambda_lo"]}:{producer_payload["lambda_hi"]}'
            cv = f'{checker_payload["coarse_index"]}:{checker_payload["refinement_depth"]}:{checker_payload["lambda_lo"]}:{checker_payload["lambda_hi"]}'
        else:
            pv = producer_payload.get(key) if key in producer_payload else pr.get(key)
            cv = checker_payload.get(key) if key in checker_payload else cr.get(key)
        if pv != expected:
            raise SystemExit(f"A1_PRODUCER_PLAN_MISMATCH index={index} key={key}")
        if key == "exterior_guards" and plan_item["decision"] != "ACCEPT" and not expected:
            pass
        elif cv != expected:
            raise SystemExit(f"A1_CHECKER_MISMATCH index={index} key={key}")
        a1[key] = expected
    if checker_payload.get("decision") != plan_item["decision"]:
        raise SystemExit(f"A1_DECISION_MISMATCH index={index}")
    if plan_item["root_gt_t_cells"] != ROOT_GT_T_CELLS:
        raise SystemExit(f"A1_ROOT_GT_T_CELLS_FAIL index={index}")
    a2 = {
        "producer_root_outcome": "RESOLVED_WITH_CERTIFIED_T_STAR" if pr.get("T_star") is not None and pr.get("root_reason") == "TARGET_WIDTH" else "UNRESOLVED",
        "checker_root_outcome": checker_payload.get("checker_root_outcome"),
        "producer_root_mv_steps": pr.get("root_mv_steps", []),
        "checker_root_mv_steps": cr.get("root_mv_steps", []),
        "producer_work": pr.get("work"),
        "checker_work": cr.get("work"),
    }
    a3 = None
    if plan_item["decision"] == "ACCEPT":
        if plan_item.get("producer_accept_root_outcome") != "RESOLVED_WITH_CERTIFIED_T_STAR":
            raise SystemExit(f"A1_ACCEPT_ROOT_OUTCOME_FAIL index={index}")
        if checker_payload.get("checker_root_outcome") != "RESOLVED_WITH_CERTIFIED_T_STAR":
            raise SystemExit("CHECKER_REPLAY_UNRESOLVED")
        a1["root_localization_outcome"] = "RESOLVED_WITH_CERTIFIED_T_STAR"
        a3 = a3_record(plan_item, pr, cr)
    return {
        "A1_EXACT_EQUALITY": a1,
        "A2_LINEAGE_INDEPENDENT": a2,
        "A3_CROSS_LINEAGE_CONSISTENCY": a3,
    }
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer-ledger", required=True)
    parser.add_argument("--checker-ledger", required=True)
    parser.add_argument("--replay-plan", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    producer_ledger = persistence.Ledger(args.producer_ledger)
    checker_ledger = persistence.Ledger(args.checker_ledger)
    plan = load_plan(args.replay_plan)
    producer = slab_records(producer_ledger)
    checker = slab_records(checker_ledger)
    if not (len(plan) == len(producer) == len(checker)):
        raise SystemExit("COMPARE_RECORD_COUNT_MISMATCH")

    rows = [compare_one(i, plan[i], producer[i], checker[i]) for i in range(len(plan))]
    summary = {
        "status": "PASS",
        "schema": "C1B_CROSS_LINEAGE_COMPARISON_V2_3_1",
        "producer_ledger_sha256": sha256_file(args.producer_ledger),
        "checker_ledger_sha256": sha256_file(args.checker_ledger),
        "replay_plan_sha256": sha256_file(args.replay_plan),
        "attempts": len(rows),
        "accepted": sum(1 for x in plan if x["decision"] == "ACCEPT"),
        "labels": ["A1_EXACT_EQUALITY", "A2_LINEAGE_INDEPENDENT", "A3_CROSS_LINEAGE_CONSISTENCY"],
    }
    output = Path(args.output)
    data = persistence.canonical_bytes(summary) + b"\n"
    data += b"".join(persistence.canonical_bytes(row) + b"\n" for row in rows)
    output.write_bytes(data)
    print("C1B_CROSS_LINEAGE_COMPARISON", "PASS", "attempts", len(rows),
          "accepted", summary["accepted"], "output_sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
