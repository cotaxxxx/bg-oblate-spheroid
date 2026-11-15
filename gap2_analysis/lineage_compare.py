"""C gap 2 independent-lineage comparison; fail-closed, exact rational checks.

Only reads run outputs (never C1b sealed inputs). A single-lineage PASS is
always NOT_EVIDENCE. This is an independent coverage/consistency checker,
not a second implementation of the numerical g_box or gt_box.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from gap1_analysis.c1b_resumable_driver import Ledger
from gap2_analysis import sealed_contract as seal

EXPECTED_PARENTS = 124
SYNTHETIC_PARENTS = 2
SYNTHETIC_INPUT_SHA = {"SYNTHETIC_INPUT_ONLY": "NOT_SEALED_C1B"}
SYNTHETIC_RULING = "SYNTHETIC_NO_JUDGE_FREEZE"


def stop(message):
    raise RuntimeError("C_GAP2_LINEAGE_COMPARE_FAIL:" + message)


def sha256(path):
    with path.open("rb") as fp:
        return hashlib.file_digest(fp, "sha256").hexdigest()


def exact(value):
    if not isinstance(value, str):
        stop("INVALID_EXACT_FRACTION")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError):
        stop("INVALID_EXACT_FRACTION")


def read_lineage(run_dir, role, *, synthetic=False, judge_ruling_sha256=None):
    manifest_path = run_dir / "manifest.json"
    ledger_path = run_dir / "ledger.jsonl"
    m = json.loads(manifest_path.read_text())
    manifest_sha256 = sha256(manifest_path)  # reported in the cross-lineage verdict
    if m.get("role") != role or m.get("schema") != "C_GAP2_V4R2_RUN_V1":
        stop("MANIFEST_SCHEMA:" + role)
    target_status = ("SYNTHETIC_COMPLETE_NOT_EVIDENCE" if synthetic
                     else "CANDIDATE_NOT_JUDGE_ACCEPTED")
    target_mode = "SYNTHETIC_NOT_EVIDENCE" if synthetic else "SEALED"
    expected_count = SYNTHETIC_PARENTS if synthetic else EXPECTED_PARENTS
    if m.get("status") != target_status or m.get("mode") != target_mode:
        stop("LINEAGE_NOT_COMPLETED:" + role)
    if synthetic and (m.get("input_sha256") != SYNTHETIC_INPUT_SHA
                      or m.get("judge_ruling_sha256") != SYNTHETIC_RULING):
        stop("SYNTHETIC_NOT_EVIDENCE_PINS_REQUIRED")
    if not synthetic:
        # H1: independently pin all four sealed inputs to the predeclared
        # full-length SHA256 values, never just to each other's manifests.
        if m.get("input_sha256") != seal.PINNED:
            stop("SEALED_INPUT_FIXED_SHA_MISMATCH:" + role)
        if (not isinstance(judge_ruling_sha256, str)
                or re.fullmatch(r"[0-9a-f]{64}", judge_ruling_sha256) is None):
            stop("JUDGE_FREEZE_SHA_REQUIRED")
        if m.get("judge_ruling_sha256") != judge_ruling_sha256:
            stop("JUDGE_FREEZE_SHA_MISMATCH:" + role)
    if m.get("ledger_sha256") != sha256(ledger_path):
        stop("LEDGER_SHA256:" + role)
    if m.get("ledger_bytes") != ledger_path.stat().st_size:
        stop("LEDGER_BYTES:" + role)
    if m.get("identity_before") != m.get("identity_after"):
        stop("RUNTIME_IDENTITY_MISMATCH:" + role)
    identity = m.get("identity_before")
    if not isinstance(identity, dict) or identity.get("clean_status") is not True:
        stop("RUNTIME_IDENTITY_MISSING:" + role)
    ledger = Ledger(ledger_path)  # validates complete run4-style SHA chain
    # G5: Ledger.append can add one lscpu_raw_trace immediately after header
    # or segment_end. It is included in the hash chain, not a mathematical
    # result; forbid it in any other position.
    cleaned = []
    for item in ledger.records:
        if item["record_type"] == "lscpu_raw_trace":
            if (not cleaned or cleaned[-1]["record_type"]
                    not in ("header", "segment_end")):
                stop("UNEXPECTED_LSCPU_TRACE_POSITION:" + role)
            continue
        cleaned.append(item)
    if len(cleaned) < 3:
        stop("LEDGER_TOO_SHORT:" + role)
    header, *body = cleaned
    if header["record_type"] != "header" or body[-1]["record_type"] != "segment_end":
        stop("LEDGER_FORMAT:" + role)
    if header["payload"].get("mode") != target_mode:
        stop("LEDGER_MODE_MISMATCH:" + role)
    if body[-1]["payload"].get("reason") != "COMPLETED":
        stop("SEGMENT_NOT_COMPLETED:" + role)
    if header["payload"].get("identity_before") != identity:
        stop("LEDGER_HEADER_IDENTITY:" + role)
    parents = header["payload"].get("parents")
    if not isinstance(parents, list) or len(parents) != expected_count:
        stop("HEADER_PARENT_COUNT:" + role)
    if (m.get("parents") != parents or m.get("accepted_parent_slabs") != expected_count
            or m.get("expected_parent_slabs") != expected_count):
        stop("MANIFEST_PARENT_COUNT:" + role)
    if header["payload"].get("sealed_input_sha256") != m.get("input_sha256"):
        stop("INPUT_PIN_MISMATCH:" + role)
    if header["payload"].get("judge_ruling_sha256") != m.get("judge_ruling_sha256"):
        stop("JUDGE_PIN_MISMATCH:" + role)
    if any(x["record_type"] != "slab_record" for x in body[:-1]):
        stop("NON_SLAB_RECORD:" + role)
    recs = [x["payload"] for x in body[:-1]]
    if m.get("attempted") != len(recs):
        stop("ATTEMPTED_COUNT_MISMATCH:" + role)
    return m, parents, recs, manifest_sha256


def exact_partition(te):
    """G4: independently construct equal-width t-cells with rational arithmetic."""
    q = 512 * (1 - te)
    n = (q.numerator + q.denominator - 1) // q.denominator
    if not (1 <= n <= 16 and Fraction(31, 32) <= te < 1):
        stop("INVALID_ENDPOINT_SEED_OR_N")
    dt = (1 - te) / n
    return [(te + j * dt, te + (j + 1) * dt) for j in range(n)], dt


def check_gate_arithmetic(ev, te, parent_id):
    """Verify the printed gate using exact fractions, not float or Arb."""
    boxes, dt = exact_partition(te)
    actual = ev.get("endpoint_gt_boxes")
    contributions = ev.get("endpoint_contributions")
    if not isinstance(actual, list) or len(actual) != len(boxes):
        stop("GT_PARTITION_LENGTH:" + parent_id)
    if not isinstance(contributions, list) or len(contributions) != len(boxes):
        stop("GT_CONTRIBUTION_COUNT:" + parent_id)
    seed = exact(ev.get("endpoint_seed_g_upper"))
    if ev.get("endpoint_n_boxes") is not None and ev["endpoint_n_boxes"] != len(boxes):
        stop("ENDPOINT_N_MISMATCH:" + parent_id)
    if ev.get("endpoint_delta_t") is not None and exact(ev["endpoint_delta_t"]) != dt:
        stop("ENDPOINT_DT_MISMATCH:" + parent_id)
    terms = []
    for j, (cell, planned) in enumerate(zip(actual, boxes)):
        got = cell.get("t_cell")
        if (cell.get("j") != j or not isinstance(got, list) or len(got) != 2
                or (exact(got[0]), exact(got[1])) != planned):
            stop("GT_PARTITION_MISMATCH:" + parent_id)
        if cell.get("dispatch") != ("endpoint_corner_ordinary" if j == len(boxes)-1 else "ordinary"):
            stop("GT_CHART_DISPATCH_MISMATCH:" + parent_id)
        u = exact(cell.get("upper"))
        term = max(Fraction(0), u)
        if exact(contributions[j]) != term:
            stop("GT_CONTRIBUTION_MISMATCH:" + parent_id)
        terms.append(term)
    # Arb rounding may increase the recorded cumulative upper bound.
    exact_cumulative = seed + dt * sum(terms, Fraction(0))
    recorded = exact(ev.get("endpoint_cumulative_mvt_upper"))
    if not (exact_cumulative <= recorded < 0 and seed < 0):
        stop("CUMULATIVE_EXACT_ARITHMETIC_MISMATCH:" + parent_id)
    return seed, recorded


def validate_tree(parents, recs, role):
    indexed = defaultdict(list)
    for x in recs:
        parent_id = x.get("parent_slab_id")
        if not isinstance(parent_id, str):
            stop("PARENT_ID_MISSING:" + role)
        indexed[parent_id].append(x)
    lookup = {p["parent_id"]: p for p in parents}
    if len(lookup) != len(parents) or set(indexed) != set(lookup):
        stop("PARENT_SET_MISMATCH:" + role)
    report = []
    for parent_id, p in lookup.items():
        ll, lr, te = exact(p["lambda_lo"]), exact(p["lambda_hi"]), exact(p["t_e"])
        if not ll < lr or not Fraction(31, 32) <= te < 1:
            stop("PARENT_DOMAIN:" + parent_id)
        coarse = int(p["coarse_index"])
        todo = [(0, ll, lr)]  # LIFO; right child first
        leaves = []
        max_seed, max_cum = None, None
        for record in indexed[parent_id]:
            if not todo:
                stop("EXTRA_CHILD:" + parent_id)
            depth, left, right = todo.pop()
            slab = record.get("slab", {})
            if (int(slab.get("coarse_index", -1)) != coarse
                    or int(slab.get("refinement_depth", -1)) != depth
                    or exact(slab.get("lambda_lo")) != left
                    or exact(slab.get("lambda_hi")) != right):
                stop("TREE_OR_SLAB_ORDER:" + parent_id)
            if exact(record.get("t_e")) != te:
                stop("CHILD_SEED_NOT_INHERITED:" + parent_id)
            ev = record.get("evidence", {})
            if exact(ev.get("endpoint_seed_t")) != te or ev.get("endpoint_work") != record.get("work"):
                stop("EVIDENCE_SEED_WORK_MISMATCH:" + parent_id)
            # Inconclusive internal nodes are allowed if they REFINE and
            # all descendant ACCEPT leaves independently certify the sign.
            # Their seed or cumulative bound may legitimately be unavailable.
            seed_raw = ev.get("endpoint_seed_g_upper")
            cum_raw = ev.get("endpoint_cumulative_mvt_upper")
            decision = record.get("decision")
            if decision == "ACCEPT":
                seed, cum = check_gate_arithmetic(ev, te, parent_id)
                max_seed = seed if max_seed is None else max(max_seed, seed)
                max_cum = cum if max_cum is None else max(max_cum, cum)
            if decision == "ACCEPT":
                if ev.get("endpoint_pass") is not True or ev.get("endpoint_reason") != "PASS":
                    stop("ACCEPT_WITHOUT_GATE:" + parent_id)
                leaves.append((left, right))
            elif decision == "REFINE" and depth < 3:
                mid = (left + right) / 2
                todo.extend([(depth + 1, left, mid), (depth + 1, mid, right)])
            else:
                stop("ABORT_OR_INVALID_DECISION:" + parent_id)
        if todo:
            stop("MISSING_LEAF:" + parent_id)
        leaves.sort()
        if not leaves or leaves[0][0] != ll or leaves[-1][1] != lr or any(
                a[1] != b[0] for a, b in zip(leaves, leaves[1:])):
            stop("PARENT_COVERAGE_HOLE:" + parent_id)
        if not max_seed < 0 or not max_cum < 0:
            stop("FINAL_SIGN_NOT_NEGATIVE:" + parent_id)
        report.append({
            "parent_id": parent_id, "lambda_lo": str(ll), "lambda_hi": str(lr),
            "t_e": str(te), "accepted_leaves": len(leaves),
            "worst_seed_upper": str(max_seed), "worst_cumulative_upper": str(max_cum),
            "accepted_intervals": [[str(a), str(b)] for a, b in leaves],
        })
    return report


def compare(producer_dir, checker_dir, *, synthetic=False, judge_ruling_sha256=None):
    if synthetic and judge_ruling_sha256 is not None:
        stop("SYNTHETIC_MUST_NOT_HAVE_JUDGE_PIN")
    pm, pp, pr, p_manifest_sha = read_lineage(
        producer_dir, "producer", synthetic=synthetic,
        judge_ruling_sha256=judge_ruling_sha256)
    cm, cp, cr, c_manifest_sha = read_lineage(
        checker_dir, "checker", synthetic=synthetic,
        judge_ruling_sha256=judge_ruling_sha256)
    for key in ("input_sha256", "judge_ruling_sha256", "parents",
                "expected_parent_slabs", "accepted_parent_slabs"):
        if pm.get(key) != cm.get(key):
            stop("LINEAGE_PIN_OR_PARENT_MISMATCH:" + key)
    # The code/environment/commit must be identical except for the respective
    # runtime import closure (different kernel/gating modules are expected).
    p_identity, c_identity = pm["identity_before"], cm["identity_before"]
    for key in ("head", "direct_parent", "frozen_grandparent",
                "changed_13_plus_new", "current_blobs_and_sha256",
                "run4_frozen_25_blobs", "python", "python_executable",
                "flint_version", "mpmath_version", "platform"):
        if p_identity.get(key) != c_identity.get(key):
            stop("LINEAGE_RUNTIME_MISMATCH:" + key)
    p_report = validate_tree(pp, pr, "producer")
    c_report = validate_tree(cp, cr, "checker")
    if {r["parent_id"] for r in p_report} != {r["parent_id"] for r in c_report}:
        stop("PARENT_SET_DIFFER")
    checkers = {r["parent_id"]: r for r in c_report}
    rows = []
    for prow in p_report:
        crow = checkers[prow["parent_id"]]
        if (prow["lambda_lo"], prow["lambda_hi"], prow["t_e"]) != (
                crow["lambda_lo"], crow["lambda_hi"], crow["t_e"]):
            stop("PARENT_T_E_OR_DOMAIN_DIFFER:" + prow["parent_id"])
        rows.append({
            "parent_id": prow["parent_id"], "lambda_lo": prow["lambda_lo"],
            "lambda_hi": prow["lambda_hi"], "t_e": prow["t_e"],
            "producer_accepted": prow["accepted_leaves"],
            "checker_accepted": crow["accepted_leaves"],
            "producer_worst_seed_upper": prow["worst_seed_upper"],
            "checker_worst_seed_upper": crow["worst_seed_upper"],
            "producer_worst_cumulative_upper": prow["worst_cumulative_upper"],
            "checker_worst_cumulative_upper": crow["worst_cumulative_upper"],
            "producer_covered": True, "checker_covered": True,
            "both_lineages_pass": True,
        })
    return {
        "schema": "C_GAP2_CROSS_LINEAGE_V1",
        "verdict": ("SYNTHETIC_COMPARE_PASS_NOT_EVIDENCE" if synthetic
                    else "COMPARE_PASS_NOT_JUDGE_CLOSED"),
        "parent_count": len(rows),
        "producer_manifest_sha256": p_manifest_sha,
        "checker_manifest_sha256": c_manifest_sha,
        "producer_ledger_sha256": pm["ledger_sha256"],
        "checker_ledger_sha256": cm["ledger_sha256"],
        "global_worst": {
            "producer_seed_upper": str(max(Fraction(r["producer_worst_seed_upper"]) for r in rows)),
            "checker_seed_upper": str(max(Fraction(r["checker_worst_seed_upper"]) for r in rows)),
            "producer_cumulative_upper": str(max(Fraction(r["producer_worst_cumulative_upper"]) for r in rows)),
            "checker_cumulative_upper": str(max(Fraction(r["checker_worst_cumulative_upper"]) for r in rows)),
        },
        "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--producer-run", type=Path, required=True)
    ap.add_argument("--checker-run", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--synthetic-two-parent", action="store_true",
                    help="Only for two NOT_EVIDENCE parents; cannot certify a real run")
    ap.add_argument("--judge-ruling-sha256",
                    help="Required for SEALED; full 64-character SHA256 of the Judge FREEZE ruling")
    a = ap.parse_args()
    if not a.synthetic_two_parent and not a.judge_ruling_sha256:
        ap.error("--judge-ruling-sha256 is mandatory for SEALED comparisons")
    result = compare(a.producer_run, a.checker_run,
                     synthetic=a.synthetic_two_parent,
                     judge_ruling_sha256=a.judge_ruling_sha256)
    if a.output.exists():
        stop("OUTPUT_ALREADY_EXISTS")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    a.output.write_text(data)
    print(result["verdict"], "parents", result["parent_count"])


if __name__ == "__main__":
    main()
