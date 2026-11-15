"""Two-lineage synthetic endpoint preflight; never opens C1b sealed ledgers.

Preflight only (NOT_EVIDENCE), to be run AFTER chat's static diff audit.
Producer & checker evaluate the *new* t_e != 31/32 branch at:
    lambda in [1/2, 1/2 + 1/1600], t_e in {993/1024, 63/64}.
Their signed Arb enclosures must overlap, gate verdicts must agree.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

LAMBDA_LO = Fraction(1, 2)
LAMBDA_HI = LAMBDA_LO + Fraction(1, 1600)
SEEDS = (Fraction(993, 1024), Fraction(63, 64))


def exact(x):
    return str(x)


def read_bounds(kernel, ball):
    if not kernel._arb_bounds_finite(ball):
        raise RuntimeError("SYNTHETIC_NONFINITE")
    lo = kernel._arb_exact_fraction(ball.lower())
    hi = kernel._arb_exact_fraction(ball.upper())
    if lo > hi:
        raise RuntimeError("SYNTHETIC_BAD_BOUNDS")
    return [exact(lo), exact(hi)]


def emit(role):
    if role == "producer":
        from gap1_producer import global_axial_c1b_kernel as kernel
    else:
        from gap1_checker import global_axial_c1b_kernel as kernel
    kernel.ctx.prec = kernel.BITS
    kernel.base.ctx.prec = kernel.BITS
    slab = kernel.Slab(0, 0, LAMBDA_LO, LAMBDA_HI)
    records = []
    for te in SEEDS:
        assert te != Fraction(31, 32)
        boxes, ok = kernel.endpoint_partition(te)
        if not ok or not boxes:
            raise RuntimeError("SYNTHETIC_PARTITION_FAILED")
        # The gate is the actual generalized runtime code, not a mock.
        verdict, evidence, work = kernel.endpoint_gate(slab, t_e=te)
        if evidence["endpoint_seed_t"] != te or len(evidence["endpoint_gt_boxes"]) != len(boxes):
            raise RuntimeError("SYNTHETIC_GATE_NOT_GENERALIZED")
        if evidence.get("endpoint_reason") == "ENDPOINT_NONFINITE":
            raise RuntimeError("SYNTHETIC_GATE_NONFINITE")
        seed, _ = kernel.g_box(te, te, slab.ll, slab.lr, kernel.ENDPOINT_SEED_PANELS)
        seed_interval = read_bounds(kernel, seed)
        derivative_intervals = []
        for (lo, hi), entry in zip(boxes, evidence["endpoint_gt_boxes"]):
            val, charts, _ = kernel.gt_box(lo, hi, slab.ll, slab.lr, kernel.ENDPOINT_GT_PANELS)
            derivative_intervals.append(read_bounds(kernel, val))
            if entry["upper"] is None:
                raise RuntimeError("SYNTHETIC_GT_UPPER_MISSING")
            if kernel._arb_exact_fraction(val.upper()) != entry["upper"]:
                raise RuntimeError("SYNTHETIC_GT_REPLAY_MISMATCH")
        records.append({
            "t_e": exact(te), "lambda_lo": exact(LAMBDA_LO),
            "lambda_hi": exact(LAMBDA_HI),
            "boxes": [[exact(a), exact(b)] for a, b in boxes],
            "seed_interval": seed_interval,
            "gt_intervals": derivative_intervals,
            "gate_pass": verdict,
            "gate_reason": evidence["endpoint_reason"],
            "seed_upper": exact(evidence["endpoint_seed_g_upper"]) if evidence["endpoint_seed_g_upper"] is not None else None,
            "cumulative_upper": exact(evidence["endpoint_cumulative_mvt_upper"]) if evidence["endpoint_cumulative_mvt_upper"] is not None else None,
            "work": work,
        })
    return {"schema": "GAP2_SYNTHETIC_PREFLIGHT_V1", "role": role,
            "status": "NOT_EVIDENCE", "cases": records}


def overlap(a, b):
    lo = max(Fraction(a[0]), Fraction(b[0]))
    hi = min(Fraction(a[1]), Fraction(b[1]))
    return lo <= hi


def compare(a, b):
    if {a.get("role"), b.get("role")} != {"producer", "checker"}:
        raise RuntimeError("SYNTHETIC_LINEAGE_MISSING")
    if a.get("status") != "NOT_EVIDENCE" or b.get("status") != "NOT_EVIDENCE":
        raise RuntimeError("SYNTHETIC_WRONG_STATUS")
    assert len(a["cases"]) == len(b["cases"]) == 2
    for u, v in zip(a["cases"], b["cases"]):
        if u["t_e"] != v["t_e"] or u["boxes"] != v["boxes"]:
            raise RuntimeError("SYNTHETIC_PARTITION_MISMATCH")
        if u["gate_pass"] != v["gate_pass"]:
            raise RuntimeError("SYNTHETIC_GATE_DECISION_DIFFER")
        if not overlap(u["seed_interval"], v["seed_interval"]):
            raise RuntimeError("SYNTHETIC_SEED_INTERVAL_DISJOINT")
        if len(u["gt_intervals"]) != len(v["gt_intervals"]):
            raise RuntimeError("SYNTHETIC_GT_GRID_DIFFER")
        if any(not overlap(x, y) for x, y in zip(u["gt_intervals"], v["gt_intervals"])):
            raise RuntimeError("SYNTHETIC_GT_INTERVAL_DISJOINT")
        if u["seed_upper"] is not None and v["seed_upper"] is not None:
            if (Fraction(u["seed_upper"]) < 0) != (Fraction(v["seed_upper"]) < 0):
                raise RuntimeError("SYNTHETIC_SEED_SIGN_DIFFER")
        if u["cumulative_upper"] is not None and v["cumulative_upper"] is not None:
            if (Fraction(u["cumulative_upper"]) < 0) != (Fraction(v["cumulative_upper"]) < 0):
                raise RuntimeError("SYNTHETIC_CUM_SIGN_DIFFER")
    return {"status": "PASS_NOT_EVIDENCE", "cases": 2}


def main():
    parser = argparse.ArgumentParser(description="NOT_EVIDENCE synthetic preflight")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--role", choices=("producer", "checker"))
    group.add_argument("--compare", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--producer", type=Path)
    parser.add_argument("--checker", type=Path)
    a = parser.parse_args()
    if a.compare:
        if not a.producer or not a.checker:
            raise SystemExit("SYNTHETIC_COMPARISON_INPUT_MISSING")
        result = compare(json.loads(a.producer.read_text()), json.loads(a.checker.read_text()))
    else:
        result = emit(a.role)
    if a.output:
        if a.output.exists():
            raise SystemExit("SYNTHETIC_OUTPUT_ALREADY_EXISTS")
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"role": result.get("role", "comparison"),
                      "status": result["status"], "cases": len(result.get("cases", [])) if not a.compare else 2}))


if __name__ == "__main__":
    main()
