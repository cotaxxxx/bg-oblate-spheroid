"""C gap 2 endpoint-only orchestrator, not an authorization to calculate.

The driver is shared control-flow; producer/checker call DIFFERENT frozen
kernels and recompute all g/Gt intervals in their own precision.
Do not execute until external Judge FREEZE and L0(c) authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

from gap2_analysis import sealed_contract as seal

CPU_CAP_NS = 48 * 3600 * 1_000_000_000
NODE_CAP = seal.EXPECTED_UNCLAMPED * (2**4 - 1)
MAX_ENDPOINT_CELLS = 1_048_576
OUTPUT_CAP = 10 * 1024**3
ROOT_DEFAULT = "/home/daybreak/basepoint-geometry-artifacts/C1b"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def atomic_lines(path: Path, lines: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise RuntimeError("RUN_DIR_ALREADY_EXISTS_NO_AUTO_RESUME")
    blob = b"".join(canonical(line) + b"\n" for line in lines)
    if len(blob) > OUTPUT_CAP:
        raise RuntimeError("OUTPUT_RESOURCE_CAP")
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as fh:
        fh.write(blob)
        fh.flush()
        os.fsync(fh.fileno())
    temp.replace(path)
    return hashlib.sha256(blob).hexdigest(), len(blob)


def _static_check(kernel, gating):
    # Pure identity checks. This operation never opens sealed inputs or
    # executes g_box/gt_box on any mathematical domain.
    assert kernel.BITS in (160, 192) and kernel.DEG == 50
    assert kernel.ENDPOINT_SEED_PANELS == kernel.ENDPOINT_GT_PANELS == 8192
    assert kernel.MAX_DEPTH == 3
    assert kernel.ENDPOINT_DT == Fraction(1, 512)
    assert callable(kernel.endpoint_partition) and callable(kernel.endpoint_gate)
    assert callable(gating.gap2_endpoint_record)
    assert kernel.endpoint_partition(Fraction(31, 32))[0] == [
        (Fraction(31, 32) + Fraction(j, 512),
         Fraction(31, 32) + Fraction(j + 1, 512)) for j in range(16)]
    assert kernel.endpoint_partition(Fraction(993, 1024))[0][-1][1] == 1
    assert len(kernel.endpoint_partition(Fraction(993, 1024))[0]) == 16
    assert len(kernel.endpoint_partition(Fraction(63, 64))[0]) == 8
    assert len(kernel.endpoint_partition(Fraction(1023, 1024))[0]) == 1
    return {
        "role_precision": kernel.BITS,
        "degree": kernel.DEG,
        "panels": kernel.ENDPOINT_SEED_PANELS,
        "lambda_max_depth": kernel.MAX_DEPTH,
        "static_partition_check": "PASS",
        "NOTE": "no sealed data opened; no numerical integrals run",
    }


def _resource_guard(start_cpu, attempted, cells, output_count):
    if time.process_time_ns() - start_cpu > CPU_CAP_NS:
        raise RuntimeError("RESOURCE_CAP_CPU_CORE_HOURS")
    if attempted > NODE_CAP or cells > MAX_ENDPOINT_CELLS or output_count > OUTPUT_CAP:
        raise RuntimeError("RESOURCE_CAP")
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 32 * 1024**2:
        raise RuntimeError("RESOURCE_CAP_MEMORY")


def full_run(kernel, gating, role, parent_dir, run_dir, ruling_sha):
    if run_dir.is_relative_to(parent_dir) or run_dir.is_relative_to(Path("/run/media")):
        raise RuntimeError("SEALED_INPUT_WRITE_PROHIBITED")
    if run_dir.exists():
        raise RuntimeError("RUN_DIR_ALREADY_EXISTS_NO_AUTO_RESUME")
    if run_dir.parent.exists() and not os.access(run_dir.parent, os.W_OK):
        raise RuntimeError("RUN_DIR_NOT_WRITABLE")

    # L0(c)/(d): sealed hash chains, accepted 159, clamped 35, unclamped 124,
    # producer/checker matching, right exterior certified covering.
    parents, inputs, receipt = seal.load_verified_parents(parent_dir)
    _static_check(kernel, gating)
    kernel.ctx.prec = kernel.BITS
    kernel.base.ctx.prec = kernel.BITS
    started = time.process_time_ns()
    entries = []
    attempted, cells, total_work = 0, 0, 0

    try:
        for parent in parents:
            # Preserve PARENT t_e for all children. Right child first, same as run4.
            stack = [kernel.Slab(parent.key[0], 0, parent.ll, parent.lr)]
            while stack:
                _resource_guard(started, attempted, cells, len(canonical(entries)))
                slab = stack.pop()
                attempted += 1
                item = gating.gap2_endpoint_record(kernel, slab, parent.t_e, parent.id)
                ev = item["evidence"]
                if ev["endpoint_seed_t"] != str(parent.t_e) and ev["endpoint_seed_t"] != parent.t_e:
                    raise RuntimeError("CHILD_SEED_INHERITANCE_FAIL")
                cells += len(ev["endpoint_gt_boxes"])
                total_work += item["work"]
                if item["decision"] == "ACCEPT":
                    item["decision"] = "ACCEPT"
                elif slab.depth < kernel.MAX_DEPTH:
                    item["decision"] = "REFINE"
                    left, right = slab.children()
                    stack.extend((left, right))  # LIFO: RIGHT FIRST
                else:
                    item["decision"] = "ABORT"
                    entries.append(item)
                    raise RuntimeError("ENDPOINT_CERTIFICATE_FAILED")
                entries.append(item)
    except Exception as exc:
        # Fail-closed: retain any attempted candidate records, labelled NOT_EVIDENCE.
        # Never substitute a weaker sign test or auto-restart on failure.
        if entries:
            abort = {
                "schema": "C_GAP2_V4R2_RUN_V1", "role": role,
                "status": "ABORT_NOT_EVIDENCE", "reason": str(exc),
                "judge_ruling_sha256": ruling_sha,
                "input_sha256": inputs, "attempted": attempted,
                "gt_boxes": cells, "panel_work": total_work,
            }
            digest, size = atomic_lines(run_dir / "ledger.jsonl", entries)
            abort["ledger_sha256"], abort["ledger_bytes"] = digest, size
            (run_dir / "manifest.json").write_bytes(canonical(abort) + b"\n")
        raise

    if attempted > NODE_CAP or cells > MAX_ENDPOINT_CELLS:
        raise RuntimeError("RESOURCE_CAP")
    manifest = {
        "schema": "C_GAP2_V4R2_RUN_V1",
        "status": "CANDIDATE_NOT_JUDGE_ACCEPTED",
        "role": role,
        "judge_ruling_sha256": ruling_sha,
        "input_sha256": inputs,
        "receipt": receipt,
        "expected_parent_slabs": seal.EXPECTED_UNCLAMPED,
        "accepted_parent_slabs": len(parents),
        "attempted": attempted,
        "gt_boxes": cells,
        "panel_work": total_work,
        "cpu_time_ns": time.process_time_ns() - started,
        "exterior_verified_by_both_lineages": True,
    }
    # Each role writes only to its own caller-supplied fresh run directory.
    digest, nbytes = atomic_lines(run_dir / "ledger.jsonl", entries)
    manifest["ledger_sha256"] = digest
    manifest["ledger_bytes"] = nbytes
    (run_dir / "manifest.json").write_bytes(canonical(manifest) + b"\n")
    return manifest


def main(role, kernel, gating):
    parser = argparse.ArgumentParser(description="C gap2 prototype: NOT FROZEN")
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
    # No L0(c) read is possible unless BOTH explicit environment and pinned
    # authoritative Judge FREEZE ruling file have been provided.
    ruling = seal.require_judge_authorization(args.judge_ruling, args.judge_ruling_sha256)
    result = full_run(kernel, gating, role,
                      Path(args.sealed_parent).resolve(), Path(args.run_dir).resolve(), ruling)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
