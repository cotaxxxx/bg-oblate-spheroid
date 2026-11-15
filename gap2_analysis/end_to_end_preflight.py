"""C gap 2 REAL driver end-to-end preflight on TWO SYNTHETIC parents.

No sealed input reads. This script invokes run_parent_set (the identical
numerical/ledger/manifest/provenance execution function as formal full_run),
with real lineage-specific kernel/gating and the genuinely new variable-t_e
branch. Results are always NOT_EVIDENCE. Run only after chat diff audit.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

from gap1_analysis import c1b_resumable_driver as persistence
from gap2_analysis import sealed_contract as seal
from gap2_analysis.endpoint_driver import run_parent_set
from gap2_analysis.lineage_compare import (
    SYNTHETIC_INPUT_SHA, SYNTHETIC_RULING, compare,
)

NO_EVIDENCE = "SYNTHETIC_PRE_FREEZE_NOT_EVIDENCE"


def parents():
    a, w = Fraction(1, 2), Fraction(1, 1600)
    return [
        seal.Parent((99000, 0, a, a + w), a, a + w,
                    Fraction(993, 1024), tuple()),
        seal.Parent((99001, 0, a + w, a + 2*w), a + w, a + 2*w,
                    Fraction(63, 64), tuple()),
    ]


def choose_role(role):
    if role == "producer":
        from gap1_producer import global_axial_c1b_kernel as kernel
        from gap1_producer import global_axial_c1b_gating as gating
    elif role == "checker":
        from gap1_checker import global_axial_c1b_kernel as kernel
        from gap1_checker import global_axial_c1b_gating as gating
    else:
        raise RuntimeError("SYNTHETIC_INVALID_ROLE")
    return kernel, gating


def run(role, run_dir, *, force_abort=False):
    kernel, gating = choose_role(role)
    assert len(parents()) == 2
    assert all(Fraction(31, 32) < p.t_e < 1 for p in parents())
    if run_dir.exists():
        raise RuntimeError("RUN_DIR_ALREADY_EXISTS")
    try:
        result = run_parent_set(
            kernel, gating, role, parents(), SYNTHETIC_INPUT_SHA,
            {"synthetic": "NO_REAL_RECEIPT"}, run_dir,
            SYNTHETIC_RULING, mode="SYNTHETIC_NOT_EVIDENCE",
            synthetic_forced_abort=force_abort,
        )
    except RuntimeError as exc:
        if not force_abort or str(exc) != "SYNTHETIC_FORCED_ABORT_NOT_EVIDENCE":
            raise
        manifest = json.loads((run_dir / "manifest.json").read_text())
        ledger = persistence.Ledger(run_dir / "ledger.jsonl")
        end = [x for x in ledger.records if x["record_type"] == "segment_end"]
        slabs = [x for x in ledger.records if x["record_type"] == "slab_record"]
        assert len(end) == 1 and len(slabs) == 1
        assert slabs[0]["payload"]["decision"] == "ABORT"
        assert end[0]["payload"]["reason"] == "ABORT"
        assert manifest["status"] == "ABORT_NOT_EVIDENCE"
        assert manifest["reason"] == "SYNTHETIC_FORCED_ABORT_NOT_EVIDENCE"
        assert manifest["attempted"] == 1
        assert manifest["identity_before"] == manifest["identity_after"]
        print(json.dumps({
            "role": role, "status": "ABORT_PATH_PASS_NOT_EVIDENCE",
            "recorded_attempts": 1, "segment_end": "ABORT",
            "real_gate_called": True,
        }, sort_keys=True))
        return
    if force_abort:
        raise RuntimeError("SYNTHETIC_FORCED_ABORT_NOT_TRIGGERED")
    if result["status"] != "SYNTHETIC_COMPLETE_NOT_EVIDENCE":
        raise RuntimeError("SYNTHETIC_BAD_SUCCESS_STATUS")
    if result["attempted"] < 2 or result["accepted_parent_slabs"] != 2:
        raise RuntimeError("SYNTHETIC_INCOMPLETE_PARENTS")
    if result["identity_before"] != result["identity_after"]:
        raise RuntimeError("SYNTHETIC_RUNTIME_IDENTITY_CHANGED")
    ledger = persistence.Ledger(run_dir / "ledger.jsonl")
    assert sum(r["record_type"] == "slab_record" for r in ledger.records) == result["attempted"]
    print(json.dumps({
        "role": role, "status": "TWO_REAL_DRIVER_PARENTS_PASS_NOT_EVIDENCE",
        "attempted": result["attempted"], "gt_boxes": result["gt_boxes"],
        "real_gate_called": True,
    }, sort_keys=True))


def main():
    p = argparse.ArgumentParser(description="Pre-Judge NOT_EVIDENCE driver preflight")
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument("--role", choices=("producer", "checker"))
    m.add_argument("--compare", action="store_true")
    p.add_argument("--run-dir", type=Path)
    p.add_argument("--force-abort", action="store_true",
                   help="Synthetic ONLY. Evaluate real first gate then record ABORT.")
    p.add_argument("--producer-run", type=Path)
    p.add_argument("--checker-run", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    if a.compare:
        if not a.producer_run or not a.checker_run:
            raise SystemExit("SYNTHETIC_COMPARISON_DIRS_MISSING")
        result = compare(a.producer_run, a.checker_run, synthetic=True)
        if result["parent_count"] != 2:
            raise RuntimeError("SYNTHETIC_COMPARE_COUNT_MISMATCH")
        if a.output:
            if a.output.exists():
                raise SystemExit("SYNTHETIC_COMPARISON_OUTPUT_EXISTS")
            a.output.write_text(json.dumps(result, sort_keys=True) + "\n")
        print(json.dumps({
            "status": result["verdict"], "parents": result["parent_count"],
        }, sort_keys=True))
    else:
        if a.run_dir is None:
            raise SystemExit("RUN_DIR_REQUIRED")
        if a.run_dir.is_relative_to(Path("/run/media")):
            raise SystemExit("USB_WRITE_PROHIBITED")
        run(a.role, a.run_dir.resolve(), force_abort=a.force_abort)


if __name__ == "__main__":
    main()
