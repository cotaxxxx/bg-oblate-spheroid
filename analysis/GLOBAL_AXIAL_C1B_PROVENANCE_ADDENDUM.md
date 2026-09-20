# GLOBAL AXIAL C1b — PROVENANCE ADDENDUM

**Status:** `PROVENANCE_ADDENDUM / NOT_BINDING / DOES_NOT_MODIFY_MACHINE_RECEIPT`

This addendum records provenance concerning the BoxLocalGuard correction lineage used by the closed C1b machine computation. It does **not** amend, reopen, supersede, or strengthen the existing machine receipt, external Judge request, Phase 1 seal, Phase 2 seal, or cross-lineage comparison. All such artifacts are referenced only.

The canonical computational HEAD remains:

`85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`

The machine status remains:

`MACHINE_PASS / C1B_MACHINE_CLOSED / JUDGE_NOT_YET_ISSUED`

## 1. Correction lineage

The relevant checker correction lineage is:

`ce974f35ece2145c73ade687577c6414841f9feb`  
→ `59305d85a60cbcba709d8a6c721c6aaf1ffd75b9`  
→ `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`  
→ sealed Phase 1 / Phase 2 execution.

Commit `ce974f35ece2145c73ade687577c6414841f9feb` introduced `BoxLocalGuard` and aligned the checker tube exception boundary with the producer. At that commit, textual `BoxLocalGuard` occurrences were 2 / 7 / 8 in `checker/global_axial_c1b_kernel.py`, `checker/monotone_tube_interval_checker.py`, and `checker/monotone_tube_refinement_checker.py`, respectively.

Commit `59305d85a60cbcba709d8a6c721c6aaf1ffd75b9` subsequently extended the catch boundary to the producer-symmetric `ValueError` sites in the checker kernel. That commit changed `checker/global_axial_c1b_kernel.py` by 7 insertions and 7 deletions. The resulting occurrence counts at the final computational lineage were 9 / 7 / 8.

Across the three checker files, the change from the parent of `ce974f3` through `85eca22` was 25 insertions and 23 deletions.

Commit `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b` then refreshed the resumable pins after the case C-2a exception-boundary extension, including the checker-kernel pin transition from `b2936a036a0b571351e313b0c2e5456af4852844` to `4eaca55ddf79b437fc756d666294372e5d1a6ba4`.

For byte-level reproducibility at the present repository state, the three checker files have SHA-256 values: `checker/global_axial_c1b_kernel.py` = `b45caaa3e124c39e5af9d00ce70d670439f0d79f405feb6696ab5313cf28d0bb`; `checker/monotone_tube_interval_checker.py` = `d13fad743095b40c134645aa0c94bb2221820208645ae1084f84fae378e4499f`; `checker/monotone_tube_refinement_checker.py` = `0e9db85c85705877a5e397ee923d5ecf7f5d922089d5b10f33369923c4b3f90c`.

## 2. Recording-medium exception for case C-2a

Case C, committed as `ce974f35ece2145c73ade687577c6414841f9feb`, was the original BoxLocalGuard correction. Production subsequently exposed an analogous box-local guard escape in `root_localize`, leading to the scope extension designated **case C-2a**.

The case C-2a predeclaration is not contained in a separate `analysis/*.md` correction document. It is recorded directly in the commit message of `59305d85a60cbcba709d8a6c721c6aaf1ffd75b9`. That message records the rationale: the producer catches the corresponding condition as `ValueError`, and enumeration of the two kernels identified eight `ValueError`-catching sites in one-to-one correspondence. It also records `Controls 1-5 all PASS` and describes the control 4/5 reproduction at coarse 105, depth 0.

This recording medium differs from the procedure used for other C1b corrections, including the v2.12-C1 through C5 sequence, where an `analysis` predeclaration document was committed and frozen before implementation after separate textual review. Because the C-2a predeclaration is part of the implementation commit itself, it cannot be retrospectively inserted into that commit; this gives the Git record resistance to later alteration. It is nevertheless **not procedurally equivalent** to a separately committed and independently text-reviewed predeclaration.

Accordingly, this addendum records the exception rather than normalizing it into the usual C1b correction procedure.

## 3. Acceptance controls and evidence layers

Three distinct evidence layers must not be conflated.

**Historical commit record.**  
The `59305d85a60cbcba709d8a6c721c6aaf1ffd75b9` commit message records `Controls 1-5 all PASS`. For controls 4/5 it further records that a coarse-105, depth-0 run from predictor through tube to `root_localize` yielded `MV_EVAL_UNRESOLVED` in both lineages, reproducing the Phase 1 record. This is a contemporaneous Git record, but the control result stated in the commit message was not independently text-audited in the same manner as the separately frozen C1b correction documents.

**Sealed production evidence.**  
The stronger direct evidence for the stage-transition fact targeted by control 5 is the sealed Phase 2 execution:

`phase2_v212s_seal_20260920T140743Z`

For coarse 105, depth 0, attempt sequence 142, the sealed ledger and stdout directly record:

`T0: gt_unresolved/gt_bad = 1`  
→ `T1: gt_unresolved/gt_bad = 1`  
→ `T2: gt_unresolved/gt_bad = 0`  
→ `C1B_TUBE_FIRST_PASS 105 0 T2`.

This is a statement about the tube-stage transition only. The enclosing slab decision was subsequently `REFINE`, with `checker_reason = ROOT:MV_EVAL_UNRESOLVED`. A tube first-pass at T2 therefore must not be represented as acceptance of the complete slab at that attempt.

**Later diagnostic control execution (2026-09-21).**  
A later execution of `~/bin/c1b_controls_boxlocal.py` against the already closed lineage produced PASS for controls 1–4 but produced no control-5 line and no final SUMMARY. Static inspection established that the control-5 block is syntactically reachable, that no early `return` or `sys.exit` intervenes after control 4, and that the referenced `CK.T_STAGES` and `CK.tube_stage()` API exists with the expected interface. A normal Python `Exception` inside that block would be caught and reported.

No preserved exit status was found for that later execution, and the available kernel logs contained no OOM indication. The reason for termination or output loss is therefore **historically unresolved**. No API incompatibility, OOM event, native abort, or output-capture failure is asserted without evidence.

This later execution is not treated as a substitute for the historical acceptance record and does not modify the sealed machine evidence.

## 4. Separately retained issue

A separate, unresolved implementation-audit issue concerns the receiving-order difference around `gt_box`: the checker uses the form `val, chart = ...`, whereas the producer uses `chart, terms = ...`.

The available Phase 1 ledger serialization does not preserve sufficient keys to determine from the previously examined records whether `tr == T_HI` occurred. Absence of a literal serialized match must therefore not be interpreted as evidence that the branch was never traversed.

The canonical numerical record for the right-clamped and `corner_hull` quantities remains the existing machine receipt, specifically **§3 “Clamp events and lambda_B”** and **§5.1 “corner_hull counts”**. This addendum does not duplicate those numerical quantities. The receipt also states in its conclusions that it does not assert general harmlessness of the corner-branch return-value interface difference; it records only the observed cross-lineage agreement on the slabs where that branch was taken.

This issue remains separate from the BoxLocalGuard provenance recorded above and is not resolved by this addendum.

---

**Effect of this addendum:** provenance documentation only.

It does not change the canonical computational identity, rerun any computation, alter either seal, modify the cross-lineage comparison, strengthen the machine claims, or change the status of the pending external Judge request.
