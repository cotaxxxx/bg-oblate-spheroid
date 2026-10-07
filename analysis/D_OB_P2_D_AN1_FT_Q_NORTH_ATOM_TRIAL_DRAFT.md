# D-OB P2 — D-AN-1 FT_q North-Atom Trial — DRAFT

**Status:** ANALYTIC TRIAL / AWAITING CHAT AUDIT / CLOSURE NOT ASSUMED / NOT A PROOF
**Parent:** `analysis/D_OB_P2_D_AN1_FT_Q_BOUNDARY_PAIR_EVALUATION_STRATEGY_DRAFT.md`, commit `a60c445c2610e9a2be72958e8938dff13de6032d`, SHA-256 `b79624f8f3f931c77797d24ee527155b03883e9dbfb5738e4647e1eb3742bf74`, 120 lines, CHAT AUDIT PASS.
**Governance:** NORTH ATOM TRIAL CONTRACT 17-19 ONLY / NO SAMPLING / NO ENCLOSURE / c_FT UNSET.

## 1. W-9 citation correction
For the folded first-derivative integral, coincidence integrability is grounded first in the P1 Section 5 definition of `E_beta`, its first-derivative integrand estimate `|F_v| lesssim 1/D`, and Corollary 4.3 for the uniformly integrable `1/(wD)` family.
P1 Lemma V remains relevant to the second-derivative / endpoint H representation, not as the primary citation for the first-derivative folded identity.

## 2. Contract 17 — exact north atom
Define the north main-region atom
`A_N := {(mu,phi): mu_C<mu<m, 0<=phi<pi}`. (2.1)
On A_N, exactly
`m-mu>0`, `C0(mu)>0`, `E=mq+C0>0`, `B1(mu)<0`, where `q=b^2`. (2.2)
Thus the Rbar contribution
`E S3 + 4B1 q L_D = E S3 - 4|B1|qL_D` (2.3)
contains an adverse q-independent part `C0 S3` and a favorable term proportional to q.

At q=0, the favorable B1 term vanishes while `E S3=C0 S3>0`. Therefore pointwise closure of the whole north atom by the P1 Rbar trap is impossible. The trial target is only an integrated inequality.

## 3. X sub-atoms without root-order assumptions
No ordering between `mu_c^+` and `mu_C` is assumed.
Define exact sub-atoms by polynomial sign:
`A_N^+ := A_N intersect {X>=0}`,
`A_N^- := A_N intersect {X<0}`. (3.1)
If `c(mu)>=0`, then the point lies in `A_N^+`. If `c(mu)<0`, the split is equivalently by
`q >= q_X(mu):=-h0 c(mu)/(lambda^2 rho^2)` versus `q<q_X(mu)`. (3.2)
Thus no cross-ordering of c-roots is required for this trial.

## 4. Exact distance ratio requested by contract 18
Using `u^2=2d0+2v`,
`S3=u(2d0-v)`, `L_D=(2d0+v)/u`. (4.1)
Hence exactly
`L_D/S3=(2d0+v)/[(2d0+2v)(2d0-v)]`. (4.2)
This converts every comparison of `qL_D` with an S3 term into an exact inequality in `(lambda,m,mu,q)` through `d0` and `v=sqrt(d0^2-4rho^2q)`.

## 5. Rbar-only necessary comparison
Apply the adverse/favorable endpoints of the P1 trap:
`Rbar E S3 <= (pi/2) E S3`,
`4Rbar B1 qL_D <= -4|B1|qL_D`. (5.1)
Therefore a sufficient Rbar-only condition for negativity is
`(pi/2) E S3 < 4|B1|qL_D`. (5.2)
Equivalently, by (4.2),
`(pi/2) E < 4|B1|q (2d0+v)/[(2d0+2v)(2d0-v)]`. (5.3)

Condition (5.3) cannot hold uniformly down to q=0 because its right side vanishes while its left side tends to `(pi/2)C0>0`. Thus even before correction terms, the north atom does not close by a pointwise trap argument.

## 6. Integrated Rbar obstacle
For fixed mu in `(mu_C,m)`, define the exact positive weight
`W:=1/(w v^3)`. (6.1)
A sufficient integrated Rbar condition is
`4|B1| int_0^pi q L_D W dphi > (pi/2) int_0^pi E S3 W dphi`. (6.2)
Since `E=C0+mq`, this is
`4|B1| I_qL > (pi/2)[C0 I_S + m I_qS]`, (6.3)
where
`I_qL:=int q L_D W dphi`, `I_S:=int S3 W dphi`, `I_qS:=int q S3 W dphi`. (6.4)
All three are exact phi-integrals; no numerical evaluation is made.

Equivalently, closure of the Rbar part requires the exact ratio condition
`4|B1| I_qL / [C0 I_S + m I_qS] > pi/2`. (6.5)
This is an explicit obstacle criterion, not a proved inequality.

## 7. Correction terms by X sign
Write the correction bracket
`F_corr:=b(DeltaR/rho)[4rho^2 E L_D+B1 S3]`. (7.1)
Because `b(DeltaR/rho)` has sign `-sign(X)` (with zero handled exactly), its sign is determined on A_N^+ and A_N^-.
However the second bracket
`K:=4rho^2 E L_D+B1 S3 = 4rho^2 E L_D-|B1|S3` (7.2)
has competing terms. Its sign is not fixed by the north-atom data alone.

Using only `|kappa_R|<=1` and the exact finite difference gives the allowed magnitude estimate away from coincidence:
`|b DeltaR/rho| <= 2q |X|/{w v[h0u-4lambda rho^2q/u]}`. (7.3)
No stronger R estimate is used.

Thus a sufficient fixed-mu integrated north condition would be (6.3) with the additional adverse correction integral
`I_corr:=int_0^pi |b DeltaR/rho| |K| W dphi`, (7.4)
namely
`4|B1| I_qL > (pi/2)[C0 I_S+m I_qS] + I_corr`. (7.5)
Equation (7.5) is the exact trap-level obstacle form. It is not claimed to hold.

## 8. Coincidence separation and what remains OPEN
The coincidence point lies at the north-atom boundary `mu=m`, with the corresponding azimuthal q at its exact coincidence value. It is not inside the open atom (2.1), but estimates may deteriorate as `mu` approaches m.

No arbitrary numerical cutoff is introduced. For any symbolic parameter `eta` with `0<eta<1`, one may define
`A_N^far(eta): mu_C<mu<=m-eta(m-mu_C)`,
`A_N^near(eta): m-eta(m-mu_C)<mu<m`. (8.1)
This is only a candidate exact family of separations; eta is not chosen or tuned here.

On the near piece, the outside factor `m-mu` vanishes linearly at the coincidence latitude. This factor is retained in the original folded integrand and is a candidate mechanism for a future mu-integrated estimate.
The present trial does not prove that this linear vanishing quantitatively controls (7.3). Therefore `A_N^near` remains OPEN.

## 9. Contract 19 — closure report
**Closed sub-atoms:** none.

**Pointwise north closure:** impossible under the coarse Rbar trap because q=0 leaves the adverse `C0 S3` term while the favorable B1 term vanishes.

**Fixed-mu phi-integrated closure:** OPEN. Its exact trap-level requirement is (7.5). Even omitting corrections, the necessary comparison to investigate is the ratio (6.5).

**X-sign sub-atoms:** sign(X) is exact, but sign(K) is not fixed; therefore X splitting alone does not close either sub-atom.

**Near coincidence:** OPEN. The linear `(m-mu)` vanishing is recorded but not converted into a quantitative bound.

## 10. Consequence for route choice
The obstruction is structural: with only `1<=Rbar<=pi/2`, the q-independent adverse term `C0 I_S` must be overcome by q-weighted favorable mass and correction control.
If (7.5) cannot be proved exactly, the next Judge choice should be between:
(a) refining Rbar using exact gamma dependence beyond the coarse trap; or
(b) abandoning fixed-mu closure and using mu-integration with the `(m-mu)` weight and possible cancellation.
This memo does not choose between (a) and (b).

## 11. Prohibitions
No sampling, enclosure, numerical eta, root-order assertion, c_FT, m0, or Boundary Pair Lemma conclusion is introduced.

**Operational status:** NORTH ATOM TRIAL / AWAITING CHAT AUDIT / CONTRACT 17-19 TARGET / NO CLOSED SUB-ATOM / POINTWISE CLOSURE IMPOSSIBLE UNDER COARSE TRAP / PHI-INTEGRATED RATIO OBSTACLE EXPLICIT / NEAR-COINCIDENCE OPEN / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
