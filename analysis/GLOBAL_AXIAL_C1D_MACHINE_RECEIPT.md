# C1d AXIAL UPPER EXCLUSION — MACHINE RECEIPT

**Status**: `C1D_MACHINE_PASS / JUDGE_NOT_ISSUED / NOT_BINDING`

## 1. Claim certified by the machine gate

    partial_t^3 g_axis_ob(t,lambda) < 0     on  D = [0, 31/32] x [5/8, 33/50].

This receipt certifies only this sign. It does not certify the right-endpoint anchor,
the analytic bridge, the absence of nonzero axial roots, the band [31/32,1], or any
off-axis statement; those belong to the separate C1d assembly.

## 2. Contract and implementation

Pre-run contract (frozen): analysis/GLOBAL_AXIAL_C1D_PRE_RUN_CONTRACT.md,
commit 957848e9e76725e9167c1babd0b7438f613cfa79, blob 23433fac2b3d55d47384086ad88592ae23d23e67.

Implementation commit: 3fdc0e891d1a56d9fb522211aff4ad16edc4fb93 (immediate parent 957848e9).
  producer/global_axial_c1d_driver.py     dc717d97eaed239a92d73d1944dd1a1faa7ba157
  checker/global_axial_c1d_checker.py     80b712e31b234976a1ea501784e5e0f1a37721ac
  tests/test_global_axial_c1d_drivers.py  5ded0cc2d9bb6de363f1ccb06972236e44e4f929
Evaluators reused byte-identically: producer fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62,
checker 3ecbda1b3e9acd8134fdd94505721b1780e14edc.

Pre-production acceptance at clean HEAD 3fdc0e89: chat raw audit of all three files PASS;
§8.2 C1-C4, the 62-root schema sweep, and the run-directory refusal test PASS; producer and
checker import closures unchanged across evaluation.

Rejected candidates (not evidence; preserved as local branches):
  7a583d75 (rejected/c1d-driver-7a583d75): evaluation records carried arb values in stats;
    C4 did not exercise the production record.
  d49c439d (rejected/c1d-driver-d49c439d): production run c1d_producer_20260921T055540Z
    ended ABORT at its first evaluation on a None stats entry. That run is not evidence.
  57643a6 (rejected/c1d-driver-57643a6): differs from 3fdc0e89 by one line in each driver
    (import_closure did not skip module __file__ values beginning with "<"); committed at
    15:35:48 +0900 and superseded by 3fdc0e89 at 15:37:08 +0900. No run was made with it.
    It was not reported to the chat audit when superseded and is recorded here after
    discovery in the branch listing.

## 3. Producer run

Run directory: c1d_producer_20260921T064822Z (started 2026-09-21T06:48:22Z), outside the repository.
Identity, identical before and after:
  HEAD 3fdc0e891d1a56d9fb522211aff4ad16edc4fb93, clean true,
  driver dc717d97, producer evaluator fbffaccc, checker evaluator 3ecbda1b,
  Python 3.11.16, python-flint 0.9.0, CPU AMD Ryzen 9 9900X 12-Core Processor.
Import closure (repository-relative path : blob):
  checker/__init__.py                    ef022967a7731d96a016ec20d0cf124af49ff9a8
  checker/endpoint_local_controls.py     c913c47d228e51a15f56957f5df9196efa1b22c3
  checker/oblate_axis_prototype.py       df402583c320c459ff4f72dc5294558f14f44d31
  producer/__init__.py                   204df430371533fd8f2e799ea715f6cedd78b9f4
  producer/c0a_four_group_v2.py          2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4
  producer/endpoint_interval_producer.py 51060fea01cb9ff661518b7c52146f71187846ff
  producer/global_axial_c0_producer.py   c4c8d6b59d3829e1843d149b7857eda5800287aa
  producer/global_axial_c1c_producer.py  fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62
  producer/global_axial_c1d_driver.py    dc717d97eaed239a92d73d1944dd1a1faa7ba157

Sealed ledger producer.jsonl: mode 444, 4,633 lines,
SHA-256 d7fa98f9dfabde2ad4c5860fab7b90a018c545abf9b113e8cc25da431fbe2442 (matches seal file).

Final record: status PASS, attempted nodes 2,034, panel evaluations 15,069,184, accepted leaves 1,265.
Record types: identity 2, evaluation 3,365, leaf 1,265, final 1; unresolved 0; abort 0.
Evaluation outcomes: accepted 1,265, not_accepted 2,084, nonfinite 16, exception 0.
Nonfinite enclosures failed the §3 acceptance criterion and the ladder proceeded as specified.
Tree bookkeeping: 496 roots, 769 splits; nodes 496 + 2·769 = 2,034; leaves 496 + 769 = 1,265.
Accepted leaves by N_s: 2048 → 703, 8192 → 562, 16384 → 0.
Accepted leaves by depth: 0 → 349, 1 → 126, 2 → 160, 3 → 192, 4 → 202, 5 → 236; depths 6 and 7 unused.

## 4. Checker run

Input: the sealed producer ledger only. Output: c1d_checker_20260921T083516Z.json,
SHA-256 d7f3e7d3bbe4b8ec6a852d6b628d4fc9310e3de87eef7e2e48786f623e21258f.
Result: status PASS; exact tiling of D by the 1,265 leaves verified (dyadic t endpoints,
exact lambda boxes, no gaps or overlaps, all 496 roots covered); every leaf re-evaluated
at 192 bits at its recorded N_s and accepted.
Checker identity, identical before and after: HEAD 3fdc0e89, clean true.
Checker import closure:
  checker/__init__.py                         ef022967a7731d96a016ec20d0cf124af49ff9a8
  checker/c0a_four_group_v2.py                18e66b6450cd2a379bbb869a99e4e5ce6999f6e5
  checker/endpoint_interval_checker.py        4cb16f8a975e5a3be601a7926af695ad5be57790
  checker/endpoint_local_checker.py           2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc
  checker/endpoint_local_controls.py          c913c47d228e51a15f56957f5df9196efa1b22c3
  checker/global_axial_c0_checker.py          85978625e029b01c8ae40fa8234566f10eea251c
  checker/global_axial_c1c_checker.py         3ecbda1b3e9acd8134fdd94505721b1780e14edc
  checker/global_axial_c1d_checker.py         80b712e31b234976a1ea501784e5e0f1a37721ac

## 5. Downstream

The C1d assembly will combine this gate with the right-endpoint anchor of receipt 3e2dfb04
(chat raw audit PASS, recorded separately) and the analytic lemma
analysis/OBLATE_AXIAL_C1D_ANALYTIC_LEMMA.md (commit 8577878d, blob 35656381,
EXTERNAL_AUDIT_PENDING / NOT_BINDING).

Trust boundary: Arb primitive enclosures (python-flint 0.9.0).
