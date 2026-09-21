# GT-BOUNDARY - RELATION TO THE BAND JUDGE RECEIPT

**Status**: `SUBSUMED_BY_BAND_JUDGE_RECEIPT / NO_SEPARATE_JUDGE / CONDITIONAL_ON_TWO_LEMMAS`

Request: `analysis/GT_BOUNDARY_JUDGE_REQUEST.md` (blob 594824eb): `partial_t g_axis_ob(1,lambda) < 0`
for `lambda` in `[5/8,33/50]`. Decision of the human Judge, 2026-09-22: no separate Judge is issued;
the claim is recorded as contained in the band Judge receipt.

Containment. The claim is Claim 1 of `analysis/LOCAL_ENTRY_BAND_JUDGE_RECEIPT.md`
(commit b1a6710e, blob d6b0a787) restricted to `t = 1`: same quantity (the one-sided derivative
at `t = 1`), same `lambda` domain, same sign. The identification of the machine endpoint-kernel
integral with `partial_t g_axis_ob(1-,lambda)` is §6 of the band C2 lemma (commit f66ffe5a),
which is among the band receipt's conditions; the conditions are therefore identical.

Corroboration, not relied upon: run #11 (id 33354706446, source 23cd0874) with the separate
implementation producer 00e3986b / checker ae2b0665 passed on the whole `lambda` interval as a
single box, checker enclosure `[-1 +/- 0.740]`. This run was not re-verified on 2026-09-22.

The template `analysis/GT_BOUNDARY_JUDGE_RECEIPT_TEMPLATE.md` (blob 3a343b6e) is left unfilled
and is superseded by this record. This closes the gt-boundary item of the 2026-09-06 decision.
