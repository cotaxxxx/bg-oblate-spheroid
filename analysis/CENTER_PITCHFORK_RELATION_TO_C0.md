# CENTER PITCHFORK (B) - RELATION TO THE C0 JUDGE RECEIPT

**Status**: `SUBSUMED_BY_C0_JUDGE_RECEIPT / NO_SEPARATE_JUDGE / CONDITIONAL_ON_TWO_LEMMAS`

Request: `analysis/CENTER_PITCHFORK_JUDGE_REQUEST.md` (blob 813829c0):
`c3_ob(lambda) = (1/6) partial_t^3 g_axis_ob(0,lambda) < 0` for `lambda` in `[2/5,83/200]`.
Decision of the human Judge, 2026-09-22: no separate Judge is issued; the claim is recorded
as contained in the C0 Judge receipt.

Containment. C0a of `analysis/GLOBAL_AXIAL_C0_JUDGE_RECEIPT.md` (commit 95fd4b66, blob fc41e71f)
gives `partial_t^3 g_axis_ob < 0` on `[0,1/2] x [2/5,83/200]`, which contains `t = 0`.
The identification `c3_ob(lambda) = partial_tau Phi(0,lambda) = (1/6) partial_t^3 g_axis_ob(0,lambda)`
is Lemma 16 of the lower-half lemma as transferred to the C0 box (commit 963b03be),
which is among the C0 receipt's conditions; the conditions are therefore identical.

Corroboration, not relied upon: the separate B machine evidence (64 exact `lambda` boxes,
machine receipt `analysis/CENTER_PITCHFORK_MACHINE_RECEIPT.md`, blob 4279f059, recorded as
chat raw-audited) was not re-verified on 2026-09-22.

With contract A (Judge receipt 0e4b199b), this supplies the cubic nondegeneracy at `lambda_c^ob`
and the supercritical orientation stated in the B request, under the same conditions.
This closes the B item of the 2026-09-06 decision.
