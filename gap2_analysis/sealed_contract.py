"""C gap 2 v4-r2 sealed input contract. IMPORT DOES NOT OPEN SEALED INPUTS.

L0(c)/(d) may be run ONLY after Judge FREEZE. Every unproven C1b
right-exterior coverage is fail-closed, never silently accepted.
This module contains parsing/coverage only, no numerical sign evaluations.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from gap1_analysis import c1b_resumable_driver as persistence

ROOT_REL = Path("C1b")
PINNED = {
    "phase1_v212s_seal_20260918T222551Z/ledger.jsonl":
        "1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f",
    "phase2_v212s_seal_20260920T140743Z/ledger.jsonl":
        "09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38",
    "phase1_v212s_seal_20260918T222551Z/checker_replay_exact.jsonl":
        "c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69",
    "c1b_receipt_extract.json":
        "8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b",
}
T_MID = Fraction(31, 32)
LAM_LO, LAM_HI = Fraction(9, 20), Fraction(5, 8)
UNCLAMPED_HI = Fraction(931, 1600)
EXPECTED_ACCEPTED, EXPECTED_CLAMPED, EXPECTED_UNCLAMPED = 159, 35, 124


def fail(reason: str):
    raise RuntimeError(reason)


def sha_file(path: Path) -> str:
    with path.open("rb") as fp:
        return hashlib.file_digest(fp, "sha256").hexdigest()


def require_judge_authorization(path: str | None, sha256: str | None):
    """An explicit external Judge authorization is mandatory for L0(c) or a run."""
    if os.environ.get("C_GAP2_JUDGE_FREEZE_APPROVED") != "YES":
        fail("EXECUTION_PROHIBITED_NOT_FROZEN")
    if not path or not sha256 or len(sha256) != 64:
        fail("JUDGE_FREEZE_RULING_MISSING")
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != sha256:
        fail("JUDGE_FREEZE_RULING_SHA_MISMATCH")
    text = data.decode("utf-8")
    if "空白②" not in text or "FREEZE" not in text or "実行許可" not in text:
        fail("JUDGE_FREEZE_RULING_NOT_AUTHORIZING")
    # The reviewer must check the actual document and scope independently.
    return sha256


def read_jsonl(path: Path):
    lines = path.read_bytes().splitlines()
    if not lines:
        fail("LEDGER_EMPTY")
    return [json.loads(ln) for ln in lines]


def rational(x):
    if not isinstance(x, str):
        fail("DOMAIN_MISMATCH_NONCANONICAL_RATIONAL")
    try:
        return Fraction(x)
    except (TypeError, ValueError, ZeroDivisionError):
        fail("DOMAIN_MISMATCH_RATIONAL")


def key(payload):
    return (int(payload["coarse_index"]), int(payload["refinement_depth"]),
            rational(payload["lambda_lo"]), rational(payload["lambda_hi"]))


@dataclass(frozen=True)
class Parent:
    key: tuple
    ll: Fraction
    lr: Fraction
    t_plus: Fraction
    right_exterior: tuple

    @property
    def id(self):
        c, d, ll, lr = self.key
        return f"{c}:{d}:{ll}:{lr}"

    @property
    def t_e(self):
        return max(T_MID, self.t_plus)


def accepted_from_ledger(path: Path):
    """Verify hash-chain via frozen persistence before accepting any slab."""
    source = persistence.Ledger(path)
    state = persistence.resume_state(source.records)
    if state["unmatched"] or any(p["decision"] == "ABORT" for p in state["terminal"]):
        fail("LEDGER_TERMINAL_OR_INTERRUPTED")
    accepted = state["accepted"]
    if len(accepted) != EXPECTED_ACCEPTED:
        fail("LEDGER_ACCEPTED_COUNT_MISMATCH")
    output = {}
    clamped = 0
    for payload in accepted:
        ident = key(payload)
        if ident in output:
            fail("LEDGER_DUPLICATE_ACCEPTED_SLAB")
        _, _, ll, lr = ident
        if not (LAM_LO <= ll < lr <= LAM_HI):
            fail("DOMAIN_MISMATCH")
        result = payload["result"]
        tp = rational(result["t_plus"])
        right_clamp = result["right_clamp"]
        if not isinstance(right_clamp, bool):
            fail("LEDGER_CLAMP_SCHEMA_MISMATCH")
        if right_clamp:
            clamped += 1
            if tp != 1:
                fail("LEDGER_CLAMP_TPLUS_MISMATCH")
        else:
            if not (tp < 1 and lr <= UNCLAMPED_HI):
                fail("DOMAIN_MISMATCH_UNCLAMPED")
        output[ident] = (payload, right_clamp, tp)
    if clamped != EXPECTED_CLAMPED:
        fail("LEDGER_CLAMPED_COUNT_MISMATCH")
    if len(output) - clamped != EXPECTED_UNCLAMPED:
        fail("LEDGER_UNCLAMPED_COUNT_MISMATCH")
    widths = sorted((key_[2], key_[3]) for key_ in output)
    if widths[0][0] != LAM_LO or widths[-1][1] != LAM_HI:
        fail("COVERAGE_FAILED_RANGE")
    if any(a[1] != b[0] for a, b in zip(widths, widths[1:])):
        fail("COVERAGE_FAILED_LAMBDA_GAPS")
    return output


def _right_exterior_guards(payload, tp: Fraction):
    """C1b v2.4 signed right exterior boxes: direct R or monotone R_MONO."""
    if tp >= T_MID:
        return tuple()
    result = payload["result"]
    raw = result.get("exterior_guards")
    if not isinstance(raw, list):
        fail("RIGHT_EXTERIOR_EVIDENCE_OPEN")
    positive = []
    for box in raw:
        if box.get("kind") not in ("R", "R_MONO") or box.get("truth") is not True:
            continue
        tl, tr = rational(box["t_lo"]), rational(box["t_hi"])
        ll, lr = rational(box["lambda_lo"]), rational(box["lambda_hi"])
        if tl < tp or tr > T_MID or not (tl < tr and ll < lr):
            fail("RIGHT_EXTERIOR_EVIDENCE_OPEN")
        positive.append((tl, tr, ll, lr, box["kind"]))
    return tuple(positive)


def _verify_right_cover(ll, lr, tp, guards):
    """Finite union of CLOSED negative boxes must cover the full rectangle.

    Testing all open grid cells suffices: the closed rectangles containing
    each cell also contain its closure, including every shared boundary.
    """
    if tp >= T_MID:
        return
    if not guards:
        fail("RIGHT_EXTERIOR_EVIDENCE_OPEN")
    xs = sorted({ll, lr} | {x for a, b, x, y, kind in guards} |
                {y for a, b, x, y, kind in guards})
    ys = sorted({tp, T_MID} | {a for a, b, x, y, kind in guards} |
                {b for a, b, x, y, kind in guards})
    if xs[0] < ll or xs[-1] > lr or ys[0] < tp or ys[-1] > T_MID:
        fail("RIGHT_EXTERIOR_COVERAGE_FAILED")
    for a, b in zip(xs, xs[1:]):
        for u, v in zip(ys, ys[1:]):
            if not any(x <= a and b <= y and t <= u and v <= w
                       for t, w, x, y, kind in guards):
                fail("RIGHT_EXTERIOR_COVERAGE_FAILED")


def load_verified_parents(sealed_root: Path):
    """L0(c)/(d) executable validation — must not be called before Judge FREEZE."""
    sealed_root = sealed_root.resolve()
    manifest = {}
    for rel, digest in PINNED.items():
        file = sealed_root / rel
        actual = sha_file(file)
        if actual != digest:
            fail("LEDGER_MISMATCH_SHA")
        manifest[rel] = actual

    p = accepted_from_ledger(sealed_root / "phase1_v212s_seal_20260918T222551Z/ledger.jsonl")
    c = accepted_from_ledger(sealed_root / "phase2_v212s_seal_20260920T140743Z/ledger.jsonl")
    if set(p) != set(c):
        fail("LEDGER_LINEAGE_DOMAIN_MISMATCH")

    replay = read_jsonl(sealed_root / "phase1_v212s_seal_20260918T222551Z/checker_replay_exact.jsonl")
    replay_accepted = {key(x): x for x in replay if x.get("decision") == "ACCEPT"}
    if set(replay_accepted) != set(p):
        fail("LEDGER_REPLAY_MISMATCH")
    receipt = json.loads((sealed_root / "c1b_receipt_extract.json").read_text())
    if not isinstance(receipt, dict) or not receipt:
        fail("RECEIPT_EXTRACT_SCHEMA_OPEN")

    parents = []
    for ident, (pp, clamped, tp) in sorted(p.items(), key=lambda x: (x[0][2], x[0][3])):
        cp, cclamped, ctp = c[ident]
        if clamped != cclamped or tp != ctp:
            fail("LEDGER_LINEAGE_TPLUS_MISMATCH")
        rp = replay_accepted[ident]
        if rp.get("t_plus") != pp["result"]["t_plus"]:
            fail("LEDGER_REPLAY_TPLUS_MISMATCH")
        if clamped:
            continue
        ll, lr = ident[2], ident[3]
        pg = _right_exterior_guards(pp, tp)
        cg = _right_exterior_guards(cp, tp)
        _verify_right_cover(ll, lr, tp, pg)
        _verify_right_cover(ll, lr, tp, cg)
        parents.append(Parent(ident, ll, lr, tp, pg))
    if len(parents) != EXPECTED_UNCLAMPED:
        fail("LEDGER_UNCLAMPED_COUNT_MISMATCH")
    return parents, manifest, {"receipt_sha256": manifest["c1b_receipt_extract.json"],
                               "right_exterior": "producer_checker_both_closed_boxes"}
