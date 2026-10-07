# D-OB P2 — D-AN-1 FT_q Boundary-Pair Evaluation Strategy Memo — DRAFT

**Status:** ANALYTIC STRATEGY MEMO / AWAITING CHAT AUDIT / NO LOWER-BOUND CLAIM / NOT A PROOF PARTITION
**Parent:** `analysis/D_OB_P2_D_AN1_FT_Q_C0_B1_ROOT_STRUCTURE_DRAFT.md`, commit `32308e842681b72c5fe661cb73ce4daecbd4ea4e`, SHA-256 `d2dc0cf0aee36ae73a97f9d4b461b1aed82678a0d7f716ed5ec2cc65de217bb8`, 92 lines, CHAT AUDIT PASS.
**Inputs:** audited P/rho reduction `356f194a...`; audited C0/B1 root structure `32308e84...`; P1 R-trap and integrability lemmas.

## 1. Purpose and prohibitions
This memo declares candidate analytic pieces and candidate inequalities for the Boundary Pair Lemma. It does not select a proof partition and does not claim that the estimates close.
No root enclosure, sampling, diagnostic split, tuned constant, `c_FT`, or `m0` is introduced.
W-8 is absorbed as: for `mu>mu_C`, `C0>0`, hence `E=mb^2+C0>0` for every allowed b, with no equality.

## 2. Contract 13 — exact target after half-azimuth folding
For `rho>0`, pair `b` with `-b` on the half azimuth `phi in [0,pi)`. With
`P=R_+N_+D_-^3+R_-N_-D_+^3`, `v=D_+D_-`,
the folded identity is
`(1/rho) int_{-1}^1 int_{0}^{2pi} R J dphi dmu`
`= int_{-1}^1 int_{0}^{pi} P/(rho w v^3) dphi dmu`. (2.1)
Using the audited symmetric reduction, write
`P/rho=-lambda^2(m-mu) F`, (2.2)
where
`F:=Rbar[E S3+4B1 b^2 L_D]+b(DeltaR/rho)[4rho^2 E L_D+B1 S3]`. (2.3)
Thus the folded target integrand is exactly
`-lambda^2(m-mu) F/(w v^3)`. (2.4)
The main region is `mu<m`, where `m-mu>0`. The cap is `m<mu<=1`, where `m-mu<0`. The interface `mu=m` is retained exactly and is not shifted.

## 3. Contract 14 — available exact boundaries, not a chosen partition
The available mu-root boundaries are:
`mu_c^-<0<mu_c^+` from c;
`mu_B^- in (-1,0)` from B1;
`mu_C in (0,m)` from C0.
The only already-fixed cross-order is `mu_B^-<0<mu_C<m`. All ordering of `mu_c^-` or `mu_c^+` relative to `mu_B^-` or `mu_C` remains UNDETERMINED.

Two derived b^2 boundaries are available when their right sides are admissible:
`q_X(mu):=-h0 c(mu)/(lambda^2 rho^2)` on `c(mu)<0`, from `X=0`; (3.1)
`q_E(mu):=-C0(mu)/m` on `C0(mu)<0`, from `E=0`. (3.2)
Here `q:=b^2`. These are derived exact boundaries, not new mu roots.

Candidate atomic pieces are generated only by:
(a) the sign cells of c, B1, C0 determined by their exact roots;
(b) inside `c<0`, the comparison `q<q_X`, `q=q_X`, `q>q_X`;
(c) inside `C0<0`, the comparison `q<q_E`, `q=q_E`, `q>q_E`;
(d) the exact interface `mu=m` separating main region and cap.
No ordering of the mu roots is selected to enumerate these cells linearly.

## 4. Sign table available on every candidate atom
`X=h0 c+lambda^2 rho^2 q`.
If `c>0`, then `X>0`; if `c=0`, then `X>=0` with equality only at `q=0`; if `c<0`, the sign of X is fixed by comparison with `q_X`.

`E=mq+C0`.
If `C0>0`, then `E>0`; if `C0=0`, then `E>=0` with equality only at `q=0`; if `C0<0`, the sign of E is fixed by comparison with `q_E`.

`B1>0` exactly below `mu_B^-` in the physical mu interval, and `B1<0` exactly above it.

Since `N_e=-lambda^2(m-mu)rho E` and `A1=-lambda^2(m-mu)B1`, every candidate atom fixes the signs of `N_e`, `A1`, and X once the side of `mu=m` is also specified.

## 5. Root ordering actually needed
For sign determination itself, no additional ordering between `mu_c^+/-`, `mu_B^-`, and `mu_C` is logically necessary: cells can be defined by simultaneous polynomial sign conditions rather than by a globally ordered list of roots.

Additional root ordering becomes useful only if the final proof requires a one-dimensional consecutive mu-interval presentation or wants to eliminate empty intersections before estimating them.
Therefore this strategy memo marks all extra c/B1/C0 root ordering as **NOT YET REQUIRED**.
If a later estimate needs, for example, the relative order of `mu_B^-` and `mu_c^-`, or of `mu_c^+` and `mu_C`, that dependency must be declared before it is proved and used.

## 6. Contract 15 — termwise evaluation rules
On every atom, use the exact four-term form before discarding signs:
`T_EE/rho=-lambda^2(m-mu)Rbar E S3`,
`T_OO/rho=-4lambda^2(m-mu)Rbar B1 q L_D`,
`T_RE/rho=-4lambda^2(m-mu)rho^2 b(DeltaR/rho)E L_D`,
`T_RO/rho=-lambda^2(m-mu)b(DeltaR/rho)B1 S3`.

For Rbar, only the P1 trap is pre-authorized: `1<=Rbar<=pi/2`. Which endpoint is used must follow the known sign of the coefficient multiplying Rbar; no uniform favorable endpoint may be chosen across opposite signs.

For the correction terms use only
`|kappa_R|<=1`,
`DeltaR/rho=2 kappa_R b X/{w v[h0u-4lambda rho^2q/u]}`, (6.1)
or the equivalent P1 Lipschitz trap. No stronger R estimate is assumed.

`T_RE/rho` carries the additional exact factor `rho^2`; this may be exploited only as that explicit factor. `T_RO/rho` has no such extra factor and must be controlled independently.

## 7. Main-region structural cases
For `mu<m`, the outside factor in (2.4) is negative.

North of `mu_C`, `E>0` and, because `mu_C>0>mu_B^-`, `B1<0`. Therefore `E S3` and `4B1qL_D` have opposite signs: the Rbar main terms compete. This region is **NOT CLOSED** by sign alone.

South of `mu_B^-`, `B1>0` and `C0<0`; E is determined by q versus `q_E`. Thus the Rbar terms can be sign-aligned or competing depending on E. This region is **NOT CLOSED** by sign alone.

In the intermediate sign cells, X further determines whether each DeltaR correction is sign-aligned with or opposed to its corresponding Rbar term. These cells are declared candidates only; no claim of closure is made.

## 8. Cap `m<mu<=1`
In the cap, the sign of `m-mu` reverses. No estimate from the main region may be transferred without reversing this outside sign.
The cap contribution must be bounded together with the main-region gain in the eventual Boundary Pair Lemma. This memo supplies no quantitative domination of the cap and therefore marks the cap estimate **OPEN**.

## 9. Coincidence and near-coincidence handling
The finite-difference denominator in (6.1) contains
`h0u-4lambda rho^2q/u = h_+D_-+h_-D_+`,
which can degenerate at coincidence. Therefore (6.1) is not to be used as a standalone uniform pointwise majorant through the coincidence point.

At and near coincidence, integrability is inherited from the original, unfactored P1 second-derivative integrand: P1 Lemma V and Corollary 4.3 provide the analytic dominated-integrability mechanism through the boundary singularity. The paired algebra is an exact rewriting away from coincidence and is extended through the singular set by that original integrable representation.

This settles **integrability/removability only**. It does not yet provide the quantitative signed lower bound required for FT_q. In particular, the explicit `rho^2` in T_RE and the factors `L_D,S3` have not yet been shown to dominate the weakening of (6.1) near coincidence. That quantitative near-coincidence estimate is **OPEN** and must not be described as closed.

## 10. Candidate inequality workflow per atom
For each nonempty exact sign atom, a later proof may attempt the following sequence:
(i) fix the signs of E, B1, X and the side of `mu=m`;
(ii) choose the correct endpoint of the Rbar trap according to the coefficient sign;
(iii) retain favorable T_EE/T_OO terms and bound only genuinely adverse terms;
(iv) control T_RE/T_RO with `|kappa_R|<=1` and the exact finite difference, without crossing coincidence by a false uniform denominator bound;
(v) prove any comparison using only that atom's defining inequalities and the frozen global domain.

If this workflow does not close on an atom, that atom remains explicitly OPEN; no adjacent-cell information may be borrowed.

## 11. Contract 16 — explicit nonclaims
`c_FT` is UNSET.
No rational enclosure is present.
No sampling or diagnostic evidence is present.
No numerical split point is present.
No proof partition has been selected.
No atom is claimed to yield the required lower bound.
The north main-term competition, south E-threshold competition, cap domination, and quantitative near-coincidence control are all explicitly OPEN.

**Operational status:** BOUNDARY-PAIR EVALUATION STRATEGY MEMO / AWAITING CHAT AUDIT / CONTRACT 13-16 TARGET / CANDIDATE PIECES ONLY / NO PARTITION SELECTED / QUANTITATIVE NEAR-COINCIDENCE OPEN / CAP OPEN / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
