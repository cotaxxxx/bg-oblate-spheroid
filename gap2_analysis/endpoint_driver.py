"""C gap 2 endpoint-only driver — pre-Judge implementation, NOT_EVIDENCE.

Producer and checker independently evaluate frozen lineage-specific g/Gt
sources. The sealed C1b inputs may not be opened without Judge FREEZE.
Output is chained and fail-closed; no automatic resume is authorized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import time
from fractions import Fraction
from pathlib import Path

from gap1_analysis import c1b_resumable_driver as persistence
from gap2_analysis import sealed_contract as seal
from gap2_analysis.runtime_identity import runtime_identity, verify_end_identity

CPU_CAP_NS = 48 * 3600 * 1_000_000_000
NODE_CAP = seal.EXPECTED_UNCLAMPED * (2**4 - 1)
MAX_ENDPOINT_CELLS = 1_048_576
OUTPUT_CAP = 10 * 1024**3
ROOT_DEFAULT = "/home/daybreak/basepoint-geometry-artifacts/C1b"


def canonical(obj):
    return persistence.canonical_bytes(obj)


def _static_check(kernel, gating):
    """Pure rational/static operations. NEVER reads sealed inputs or calls g_box."""
    assert kernel.BITS in (160, 192) and kernel.DEG == 50
    assert kernel.ENDPOINT_SEED_PANELS == kernel.ENDPOINT_GT_PANELS == 8192
    assert kernel.MAX_DEPTH == 3
    assert kernel.ENDPOINT_DT == Fraction(1, 512)
    assert callable(kernel.endpoint_partition) and callable(kernel.endpoint_gate)
    assert callable(gating.gap2_endpoint_record)
    # A generic equal-partition construction must recover legacy run4 exactly.
    def general(te):
        n0 = Fraction(1, 1) - te
        q = 512 * n0
        n = -(-q.numerator // q.denominator)
        delta = n0 / n
        return [(te + j * delta, te + (j + 1) * delta) for j in range(n)]
    run4 = [(Fraction(31, 32) + Fraction(j, 512),
             Fraction(31, 32) + Fraction(j + 1, 512)) for j in range(16)]
    assert general(Fraction(31, 32)) == run4
    assert kernel.endpoint_partition(Fraction(31, 32)) == (run4, True)
    for te, count in ((Fraction(993, 1024), 16),
                      (Fraction(63, 64), 8),
                      (Fraction(1023, 1024), 1)):
        got, ok = kernel.endpoint_partition(te)
        assert ok and got == general(te) and len(got) == count
    return {"role_precision": kernel.BITS, "degree": kernel.DEG,
            "panels": kernel.ENDPOINT_SEED_PANELS,
            "lambda_max_depth": kernel.MAX_DEPTH,
            "generic_equals_run4": True, "static_partition_check": "PASS",
            "NOTE": "no sealed data opened; no numerical integrals run"}


def _resource_guard(start_cpu, attempted, cells, bytes_written):
    if time.process_time_ns() - start_cpu > CPU_CAP_NS:
        raise RuntimeError("RESOURCE_CAP_CPU_CORE_HOURS")
    if attempted > NODE_CAP or cells > MAX_ENDPOINT_CELLS or bytes_written > OUTPUT_CAP:
        raise RuntimeError("RESOURCE_CAP")
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 32 * 1024**2:
        raise RuntimeError("RESOURCE_CAP_MEMORY")


def _parents_table(parents):
    table = []
    for p in parents:
        table.append({
            "parent_id": p.id, "coarse_index": p.key[0],
            "c1b_original_depth": p.key[1],
            "lambda_lo": str(p.ll), "lambda_hi": str(p.lr),
            "t_plus": str(p.t_plus), "t_e": str(p.t_e),
        })
    return table


def _ledger_digest(path):
    with path.open("rb") as h:
        digest = hashlib.file_digest(h, "sha256").hexdigest()
    return digest, path.stat().st_size


def _write_manifest(path, payload):
    if path.exists():
        raise RuntimeError("MANIFEST_ALREADY_EXISTS")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".json.tmp")
    with temp.open("xb") as h:
        h.write(canonical(payload) + b"\n")
        h.flush()
        os.fsync(h.fileno())
    temp.replace(path)


def full_run(kernel, gating, role, parent_dir, run_dir, ruling_sha):
    """Authorized SEALED route: identity first; L0(c) only after Judge FREEZE."""
    if run_dir.is_relative_to(parent_dir) or run_dir.is_relative_to(Path("/run/media")):
        raise RuntimeError("SEALED_INPUT_WRITE_PROHIBITED")
    _static_check(kernel, gating)
    # F2: pin provenance before touching the sealed ledger.
    identity_before = runtime_identity(kernel)
    parents, inputs, receipt = seal.load_verified_parents(parent_dir)
    return run_parent_set(kernel, gating, role, parents, inputs, receipt, run_dir,
                          ruling_sha, mode="SEALED", identity_before=identity_before)


def run_parent_set(kernel, gating, role, parents, inputs, receipt, run_dir,
                   ruling_sha, *, mode, identity_before=None,
                   synthetic_forced_abort=False):
    """Common real kernel/gating/Ledger/manifest path for sealed and synthetic inputs.

    SYNTHETIC uses ONLY in-memory parents, never the sealed loader or Judge
    authorization; every artifact is permanently marked NOT_EVIDENCE.
    """
    if mode not in ("SEALED", "SYNTHETIC_NOT_EVIDENCE"):
        raise RuntimeError("UNKNOWN_RUN_MODE")
    if mode == "SEALED" and (len(parents) != seal.EXPECTED_UNCLAMPED or synthetic_forced_abort):
        raise RuntimeError("SEALED_PARENT_COUNT_OR_TEST_HOOK_FORBIDDEN")
    if mode == "SYNTHETIC_NOT_EVIDENCE" and len(parents) != 2:
        raise RuntimeError("SYNTHETIC_PARENT_COUNT_MISMATCH")
    if run_dir.is_relative_to(Path("/run/media")) or run_dir.is_relative_to(Path(ROOT_DEFAULT)):
        raise RuntimeError("SEALED_INPUT_WRITE_PROHIBITED")
    if run_dir.exists():
        raise RuntimeError("RUN_DIR_ALREADY_EXISTS_NO_AUTO_RESUME")
    if run_dir.parent.exists() and not os.access(run_dir.parent, os.W_OK):
        raise RuntimeError("RUN_DIR_NOT_WRITABLE")
    _static_check(kernel, gating)
    if identity_before is None:
        identity_before = runtime_identity(kernel)
    header_parents = _parents_table(parents)
    kernel.ctx.prec = kernel.BITS
    kernel.base.ctx.prec = kernel.BITS
    started = time.process_time_ns()
    run_dir.mkdir(parents=True, exist_ok=False)
    ledger = persistence.Ledger(run_dir / "ledger.jsonl")
    ledger.append("header", {
        "schema": "C_GAP2_V4R2_RUN_V1", "lineage": role, "mode": mode,
        "judge_ruling_sha256": ruling_sha,
        "sealed_input_sha256": inputs,
        "identity_before": identity_before,
        "parents": header_parents,
        "lambda_refinement_depth": "0..3 RELATIVE TO C1b PARENT (right-first)",
    })
    attempted, cells, total_work = 0, 0, 0

    def make_manifest(status, reason, identity_after):
        sha, size = _ledger_digest(ledger.path)
        return {
            "schema": "C_GAP2_V4R2_RUN_V1", "role": role, "mode": mode,
            "status": status, "reason": reason,
            "judge_ruling_sha256": ruling_sha, "input_sha256": inputs,
            "receipt": receipt,
            # F7 auxiliary-only candidate values are visible in the manifest,
            # not a condition for L0(c) or a mathematical sign certificate.
            "receipt_counts": receipt.get("receipt_counts") if isinstance(receipt, dict) else None,
            "parents": header_parents,
            "expected_parent_slabs": seal.EXPECTED_UNCLAMPED if mode == "SEALED" else 2,
            "accepted_parent_slabs": len(parents),
            "attempted": attempted, "gt_boxes": cells,
            "panel_work": total_work,
            "cpu_time_ns": time.process_time_ns() - started,
            "ledger_sha256": sha, "ledger_bytes": size,
            "identity_before": identity_before, "identity_after": identity_after,
        }

    try:
        for parent in parents:
            # Parent t_e is inherited by all lambda children, regardless of depth.
            stack = [kernel.Slab(parent.key[0], 0, parent.ll, parent.lr)]
            while stack:
                _resource_guard(started, attempted, cells, ledger.path.stat().st_size)
                slab = stack.pop()
                attempted += 1
                item = gating.gap2_endpoint_record(kernel, slab, parent.t_e, parent.id)
                ev = item["evidence"]
                # G1: gating serializes Fraction to "p/q" text.
                if (Fraction(ev["endpoint_seed_t"]) != parent.t_e
                        or Fraction(item["t_e"]) != parent.t_e):
                    raise RuntimeError("CHILD_SEED_INHERITANCE_FAIL")
                if synthetic_forced_abort:
                    # G2: exercise the REAL gate and the real ABORT/manifest
                    # path. Synthetic data only, never available in SEALED.
                    item["decision"] = "ABORT"
                    ledger.append("slab_record", item)
                    raise RuntimeError("SYNTHETIC_FORCED_ABORT_NOT_EVIDENCE")
                cells += len(ev["endpoint_gt_boxes"])
                total_work += item["work"]
                if item["decision"] == "ACCEPT":
                    pass
                elif slab.depth < kernel.MAX_DEPTH:
                    item["decision"] = "REFINE"
                    left, right = slab.children()
                    stack.extend((left, right))  # LIFO: RIGHT FIRST
                else:
                    item["decision"] = "ABORT"
                    ledger.append("slab_record", item)
                    raise RuntimeError("ENDPOINT_CERTIFICATE_FAILED")
                # F4: SHA-256 chain append immediately after every completed node.
                ledger.append("slab_record", item)
                _resource_guard(started, attempted, cells, ledger.path.stat().st_size)

        identity_after = verify_end_identity(identity_before, kernel)
        ledger.append("segment_end", {
            "reason": "COMPLETED", "attempted": attempted,
            "gt_boxes": cells, "panel_work": total_work,
            "identity_after": identity_after,
        })
        status = ("CANDIDATE_NOT_JUDGE_ACCEPTED" if mode == "SEALED"
                  else "SYNTHETIC_COMPLETE_NOT_EVIDENCE")
        result = make_manifest(status, "COMPLETED", identity_after)
        _write_manifest(run_dir / "manifest.json", result)
        return result
    except Exception as exc:
        try:
            identity_after = runtime_identity(kernel)
        except Exception as snap_exc:
            identity_after = {"error": str(snap_exc)}
        ledger.append("segment_end", {
            "reason": "ABORT", "error": str(exc),
            "attempted": attempted, "gt_boxes": cells,
            "identity_after": identity_after,
        })
        abort = make_manifest("ABORT_NOT_EVIDENCE", str(exc), identity_after)
        _write_manifest(run_dir / "manifest.json", abort)
        raise


def main(role, kernel, gating):
    parser = argparse.ArgumentParser(description="C gap2 static candidate: NOT FROZEN")
    parser.add_argument("--static-preflight", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--sealed-parent", default=ROOT_DEFAULT)
    parser.add_argument("--run-dir")
    parser.add_argument("--judge-ruling")
    parser.add_argument("--judge-ruling-sha256")
    args = parser.parse_args()
    if args.static_preflight and not args.execute:
        print(json.dumps(_static_check(kernel, gating), ensure_ascii=False, sort_keys=True))
        return
    if not args.execute or not args.run_dir:
        raise SystemExit("EXECUTION_PROHIBITED_NOT_FROZEN")
    # Judge FREEZE and an explicit opt-in are required BEFORE L0(c).
    ruling = seal.require_judge_authorization(args.judge_ruling, args.judge_ruling_sha256)
    result = full_run(kernel, gating, role,
                      Path(args.sealed_parent).resolve(), Path(args.run_dir).resolve(), ruling)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
