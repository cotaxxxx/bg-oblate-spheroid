"""Run4 regression comparator for C gap 2 generalized endpoint gate.

This is a POST-STATIC-AUDIT preflight harness, not an unattended job.
Input is the PUBLIC run4 frozen ledger, NEVER the C1b sealed ledger.
Use the corresponding run4 producer/checker ledger separately.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction
from pathlib import Path

from gap1_analysis import c1b_resumable_driver as persistence


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--role", choices=("producer", "checker"), required=True)
    p.add_argument("--run4-ledger", type=Path, required=True)
    a = p.parse_args()
    if a.role == "producer":
        from gap1_producer import global_axial_c1b_kernel as kernel
        from gap1_producer import global_axial_c1b_gating as gating
    else:
        from gap1_checker import global_axial_c1b_kernel as kernel
        from gap1_checker import global_axial_c1b_gating as gating

    ledger = persistence.Ledger(a.run4_ledger)  # NOT A SEALED C1b INPUT
    candidates = [
        p["payload"] for p in ledger.records
        if p["record_type"] == "slab_record"
        and p["payload"]["decision"] == "ACCEPT"
        and (p["payload"]["result"].get("gap1", {}).get("endpoint") or {}).get("endpoint_pass") is True
    ]
    if len(candidates) < 3:
        raise SystemExit("RUN4_REGRESSION_CANDIDATES_MISSING")
    # Deterministic sample selection: ledger order, first/middle/last.
    kernel.ctx.prec = kernel.BITS
    kernel.base.ctx.prec = kernel.BITS
    for ix in (0, len(candidates) // 2, len(candidates) - 1):
        src = candidates[ix]
        slab = kernel.Slab(int(src["coarse_index"]), int(src["refinement_depth"]),
                           Fraction(src["lambda_lo"]), Fraction(src["lambda_hi"]))
        ok, rec, work = kernel.endpoint_gate(slab, t_e=Fraction(31, 32))
        expected = src["result"]["gap1"]["endpoint"]
        actual = gating._gap1_value(rec)
        if not ok or rec.get("endpoint_partition_id") != kernel.ENDPOINT_PARTITION_ID:
            raise SystemExit("REGRESSION_MISMATCH_PARTITION")
        if actual != expected:
            # Full recursive equality includes all exact fraction strings, chart
            # records, per-panel work, order, and U_cum. Never normalize floats.
            raise SystemExit("REGRESSION_MISMATCH_DATA:" + str(ix))
        old_work = src["result"]["work"]["endpoint"]
        if int(work) != int(old_work):
            raise SystemExit("REGRESSION_MISMATCH_WORK:" + str(ix))
        print(json.dumps({"role":a.role,"sample_index":ix,"lambda_lo":src["lambda_lo"],
                          "lambda_hi":src["lambda_hi"],"work":work,"verdict":"PASS"},
                         sort_keys=True))
    print("REGRESSION 3/3 PASS",a.role)


if __name__ == "__main__":
    main()
