# D-OB P2 — D-AN-1 FT_q Boundary-Face Positivity — REDUCTION DRAFT

**Status:** PAPER-PROOF REDUCTION DRAFT / CORE LOWER-BOUND LEMMA OPEN / NOT A THEOREM
**Frozen parent:** `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`, commit `e9c8b1caa3ad502a3d01dafe354b61108787eed2`, SHA-256 `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217`, **FROZEN**.
**L2 input:** `analysis/D_OB_P2_D_AN1_L2_DRAFT.md`, commit `9eb8ddee96cbb1703618aa606eeb9e81f7697549`, SHA-256 `0a83e411e51582674c5490cb8e92defd171481c6271c48c6760681b8f5e839cb`, **AUDIT PASS**.
**NP-T input:** `analysis/D_OB_P2_D_AN1_NP_T_DRAFT.md`, commit `99467ed5`, SHA-256 `e929d95631a5e6a5dac86dad86f5285b69429e5ff9bcb33c1695f24eff8b196b`, **AUDIT PASS / CROSS-CHECK**.
**QM input:** `analysis/D_OB_P2_D_AN1_QM_DRAFT.md`, commit `7f9119f7cbe7d5dab95e42300bb9563c974e23f5`, SHA-256 `e8588c1b677e10aceac22e79784e41111cffe2c2cffce1636804485dafb09edc`, **AUDIT PASS**.
**Evidence:** ANALYTIC PAPER PROOF ONLY / NO DIAGNOSTIC EVIDENCE / NO INTERVAL COMPUTATION.

## 1. Frozen target

For

`lambda in [2/5,93/200]`, `tau in [7/8,1]`,

define

`rho=(1-tau^2)/(1+tau^2)`,

`m=2 tau/(1+tau^2)`,

`z=lambda m`.

Then

`rho^2+m^2=1`, `0<=rho<=15/113`, `112/113<=m<=1`.

Frozen FT_q requires an explicit rational `m0>0`, independent of `lambda,tau`, such that

`H(rho,z;lambda)>=m0`.

This draft fixes the exact boundary-face reduction that any completion of FT_q may use. It does **not** yet claim an `m0`; the remaining lower-bound lemma is isolated in §8.

## 2. Boundary geometry

Write the surface point as

`x=(a cos(phi),a sin(phi),lambda mu)`, `a=sqrt(1-mu^2)`, `b=a cos(phi)`.

For the boundary base point `p=(rho,0,lambda m)`, the P1 quantities become

`h=lambda(1-rho b-m mu)`,

`D^2=a^2+rho^2+lambda^2(mu-m)^2-2 rho b`,

`w^2=mu^2+lambda^2 a^2`.

Equivalently, if `c=rho b+m mu` is the Euclidean dot product of the corresponding unit-sphere directions, then

`h=lambda(1-c)`,

`D^2=2(1-c)-(1-lambda^2)(mu-m)^2`.                       (2.1)

In particular `h>=0`, with equality only at the coincident surface point, and the diagonal singularity is the already audited Lemma-V one.

## 3. First-derivative representation of H

For `rho>0`, P1 Lemma 6.1 gives

`H(rho,z)=E_rho(rho,z)/rho`.

Since

`F=h G(gamma)`, `G'= -2R`,

we have

`F_rho=h_rho G-2hR gamma_rho`,                            (3.1)

where `h_rho=-lambda b`.

Because `dA/w=dmu dphi`,

`E_rho=(1/(4 pi lambda)) integral integral F_rho dphi dmu`.  (3.2)

The point `tau=1` has `rho=0` and is supplied by the continuous extension `H(0,lambda)=E_rhorho(0,lambda)` and audited NP-T. Sections 4–8 treat `rho>0`; a completed uniform lower bound must be compatible with the endpoint by continuity.

## 4. Exact integration-by-parts removal of G

For fixed `mu`, dependence on `phi` is through `b=a cos(phi)`. Since

`gamma_b=-lambda rho/(wD)+h rho/(wD^3)`,                 (4.1)

and `b_phi=-a sin(phi)`, integration by parts over one full azimuth gives

`integral_0^(2pi) b G dphi`

`=a^2 integral_0^(2pi) sin^2(phi) G'(gamma) gamma_b dphi`.

Using `G'=-2R`, (3.1) becomes the exact averaged identity

`integral_0^(2pi) F_rho dphi = 2 integral_0^(2pi) R J dphi`,  (4.2)

where

`J:=lambda(a^2-b^2) gamma_b-h gamma_rho`.                 (4.3)

Consequently

`H(rho,z;lambda)`

`=(1/(2 pi lambda rho)) integral_{-1}^1 integral_0^(2pi) R J dphi dmu`.  (4.4)

Thus FT_q is reduced to a lower bound for a single paired `R J` surface integral. No `G` term remains.

## 5. Quadratic numerator N_J

The remaining derivatives are

`gamma_b=-lambda rho/(wD)+h rho/(wD^3)`,

`gamma_rho=-lambda b/(wD)-h(rho-b)/(wD^3)`.              (5.1)

Define

`N_J:=w D^3 J`.

Direct substitution into (4.3) shows that `N_J` is exactly quadratic in `b`:

`N_J=A2 b^2+A1 b+A0`,                                    (5.2)

with

`A2=lambda^2 rho^3-lambda^2 rho+lambda mu rho z`,

`A1=lambda^4 mu^2-lambda^3 mu^3 z-2lambda^3 mu z`

`   -lambda^2 mu^2 rho^2+2lambda^2 mu^2 z^2-lambda^2 mu^2+lambda^2 z^2`

`   +lambda mu^3 z+lambda mu rho^2 z-lambda mu z^3+lambda mu z-mu^2 z^2`,

`A0=lambda^4 mu^4 rho-lambda^4 mu^2 rho-2lambda^3 mu^3 rho z+2lambda^3 mu rho z`

`   -lambda^2 mu^4 rho+lambda^2 mu^2 rho^3+lambda^2 mu^2 rho z^2+lambda^2 mu^2 rho`

`   -lambda^2 rho^3-lambda^2 rho z^2+lambda^2 rho+lambda mu^3 rho z`

`   -3lambda mu rho z+mu^2 rho z^2`.

The exact degree-two structure is the principal algebraic simplification supplied by the L1 route; the earlier direct `F_rhorho` numerator is quartic in `b`.

## 6. Boundary specialization and diagonal factor

Put `z=lambda m` and use `rho^2+m^2=1`. Polynomial reduction of (5.2) gives the exact factorization

`N_J=-lambda^2 (m-mu) Q`,                                (6.1)

where

`Q=b^2 m rho`

` +b[lambda^2 m^2 mu-lambda^2 m mu^2-lambda^2 m+lambda^2 mu`

`    +m^2 mu+m mu^2-2mu]`

` +rho[-lambda^2 m mu^2+lambda^2 m+lambda^2 mu^3-lambda^2 mu`

`      -m-mu^3+2mu]`.                                    (6.2)

Hence the numerator vanishes on the latitude `mu=m` through the boundary base point. This factor is exact and is not a numerical observation.

Formula (6.1) by itself is not a sign proof: the remaining factor `Q`, the denominator `wD^3`, and `R(gamma)` all vary with `b`.

## 7. Exact b-pair controls

For fixed `mu`, set

`h0=lambda-z mu`,

`h_+=h(b)=h0-lambda rho b`, `h_-=h(-b)=h0+lambda rho b`,

`D_+=D(b)`, `D_-=D(-b)`,

`gamma_+=gamma(b)`, `gamma_-=gamma(-b)`.

The exact finite-difference identity previously derived in the L1 analysis is

`gamma_+-gamma_-`

`=4 rho b [h0 c(mu)+lambda^2 rho^2 b^2]`

` / [w D_+ D_- (h_+ D_-+h_- D_+)]`,                     (7.1)

where

`c(mu)=lambda mu^2-z mu-lambda rho^2-lambda(lambda mu-z)^2`

`     =lambda(1-lambda^2)mu^2-z(1-2lambda^2)mu-lambda(rho^2+z^2)`.  (7.2)

In the interior of the parameter surface the denominator in (7.1) is positive. The quadratic `c(mu)` has opposite-sign roots, so its negative set is a single interval.

The P1 trap `-1<=R_gamma<=0` yields the exact Lipschitz control

`|R(gamma_+)-R(gamma_-)|<=|gamma_+-gamma_-|`.             (7.3)

Together, (5.2), (6.1), and (7.1)–(7.3) reduce the nonalgebraic part of the paired integrand to an explicit finite difference with a positive denominator.

## 8. Remaining core lower-bound lemma

To complete FT_q without adding any new dependency, it is sufficient to prove the following purely analytic lemma from the formulas above.

**Boundary Pair Lemma (open in this draft).** There exists an explicit rational `c_FT>0` such that, for every

`lambda in [2/5,93/200]`, `112/113<=m<1`, `rho=sqrt(1-m^2)`,

one has

`integral_{-1}^1 integral_0^(2pi) R J dphi dmu >= 2 pi lambda rho c_FT`.  (8.1)

Then (4.4) immediately gives

`H(rho,lambda m;lambda)>=c_FT`                            (8.2)

for `rho>0`, while the `rho=0` endpoint is supplied by NP-T. If the same `c_FT` is also below an explicit NP-T endpoint margin, then

`m0:=c_FT`

is the frozen FT_q constant.

The intended proof of (8.1) must use only exact inequalities derived before any result is seen. A permissible route is:

1. pair `b` and `-b` on `phi in [0,pi)` using L2;
2. split the pair into the even quadratic part of `N_J` and its odd part;
3. use `1<=R<=pi/2` on same-sign pieces;
4. control the `R_+-R_-` correction by (7.1) and (7.3);
5. reduce the remaining bounds to rational inequalities on the frozen box in `(lambda,m,mu,b^2)`.

No diagnostic margin, sampled worst point, or interval-computed threshold may be inserted into this lemma.

## 9. Endpoint information from NP-T

Although NP-T's theorem statement asserts only strict positivity, its audited proof contains the explicit intermediate estimate

`integral_0^2 <F_rhorho>_phi dq > lambda (13/1000)`.

Therefore its final normalization gives the paper-proof endpoint margin

`H(0,lambda)=E_rhorho(0,lambda)>13/2000`.                 (9.1)

This number was derived analytically inside NP-T and is not diagnostic evidence. A completed FT_q proof may therefore choose

`m0 <= min(c_FT,13/2000)`

with an explicit rational choice after (8.1) is proved. This draft does not yet make that choice because `c_FT` is still open.

## 10. Why QM alone does not close FT_q

QM now supplies an explicit global modulus, but its constants are deliberately conservative. Using it only to transport the endpoint margin (9.1) across the whole face would not yield a useful positive bound at `rho=15/113`. FT_q therefore genuinely needs the boundary-face cancellation encoded in (4.2)–(7.3); it is not merely a corollary of NP-T plus continuity.

This observation changes no frozen dependency or theorem statement.

## 11. Governance verdict

The following parts are closed in this reduction draft:

- exact boundary parametrization;
- removal of `G` by azimuthal integration by parts;
- exact representation `H=(2 pi lambda rho)^(-1) integral R J`;
- exact quadratic numerator `N_J`;
- exact boundary factor `(m-mu)`;
- exact paired finite-difference formula for `gamma_+-gamma_-`;
- `R` Lipschitz reduction;
- explicit NP-T endpoint margin `13/2000` as an analytic intermediate consequence.

The frozen FT_q node is **not yet discharged** because Boundary Pair Lemma (8.1), and hence an explicit face-wide `m0`, has not yet been proved.

No interval computation is authorized or used. No diagnostic result enters this draft.

**Operational status:** FT_q REDUCTION DRAFT / CORE BOUNDARY PAIR LEMMA OPEN / QM AUDIT PASS / L3 BODY BLOCKED ON FT_q / delta0 NOT YET AVAILABLE / L1 PAUSED / D-P2 NOT_CERTIFIED.
