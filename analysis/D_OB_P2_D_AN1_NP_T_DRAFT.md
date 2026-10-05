# D-OB P2 — D-AN-1 NP-T North-pole Transverse Positivity — DRAFT

**Status:** PAPER-PROOF DRAFT / AWAITING CHAT AUDIT / NOT A THEOREM
**Frozen parent:** `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_1.md`, commit `6de8a178b3f9c278952ac68590f97f3f100ed9f9`, SHA-256 `1461fc081c99cfd820792248bc2f6fe2401a182a8a4941df46a4288f49f8cc78`, **FROZEN**.
**Normative MRA:** `analysis/D_OB_P2_D_AN1_L2_MRA_DRAFT.md`, commit `4e60b1ed32f862455450d38af6a5e440c64aa3ec`, SHA-256 `7e0337379bff33ef3ba63e71069287cb849aad9de688c466775ef68f31cb3185`, **AUDIT PASS**.
**L2:** `analysis/D_OB_P2_D_AN1_L2_DRAFT.md`, commit `9eb8ddee96cbb1703618aa606eeb9e81f7697549`, SHA-256 `0a83e411e51582674c5490cb8e92defd171481c6271c48c6760681b8f5e839cb`, **AUDIT PASS**.
**P1 source:** commit `6c6282a8`, file `analysis/D_OB_P1_DESIGN_NOTE.md`, SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`.

No diagnostic value, interval computation, or G-numbered computation is used.

## 1. NP-T statement

**Candidate Lemma NP-T (north-pole transverse positivity).** For the oblate family `K_lambda` and the energy `E` defined in the pinned P1 design note, conditional on the audited Lemma V bundle, for every `lambda in [2/5,93/200]`, the continuous boundary value of the transverse second derivative satisfies

`E_rhorho(0,lambda) > 0`.

Equivalently by P1 Lemma 6.1(iii),

`H(0,lambda) > 0`.

The candidate claims no explicit margin and no sign of `g_axis_ob(1,lambda)`, `partial_t g_axis_ob(1-,lambda)`, or the center coefficient `H_axis_ob(lambda)`.

The statement above is the frozen v1.1 / MRA statement verbatim. The proof below establishes only this statement; intermediate quantitative inequalities are not promoted to an additional theorem claim.

## 2. North-pole variables

Fix `lambda in [2/5,93/200]` and put

`p+=(0,0,lambda)`, `q=1-mu`, `y=lambda^2`, `a^2=1-mu^2=q(2-q)`, `b=a cos(phi)`.

Thus `q in [0,2]` and `y in [4/25,8649/40000]`.

At `p+`, the P1 definitions specialize to

`h=lambda q`,

`w^2=(1-q)^2+lambda^2 q(2-q)`,

`D^2=q d`, where `d:=2-(1-y)q`.

In particular `lambda <= w <= 1` and `0<d<=2` for `q<2`, with the endpoint values understood by continuity where needed. Also

`gamma=h/(wD)` lies in `[0,1]`: this is already part of the convexity range used in P1 Lemma V. Directly at the north pole, `gamma -> 0` as `q -> 0`, while at `q=2` we have `w=1`, `D=2lambda`, `h=2lambda`, hence `gamma=1`.

Write

`R=arccos(gamma)/sqrt(1-gamma^2)`.

For `gamma=cos(alpha)`, `alpha in [0,pi/2]`, so

`1 <= R <= pi/2`, `R_gamma <= 0`.

Indeed `R=alpha/sin(alpha)`, and

`R_gamma=(alpha cos(alpha)-sin(alpha))/sin^3(alpha) <= 0`

because `tan(alpha)>=alpha`. For reference, the stronger trap suggested by the north-pole range is also elementary:

`-1 <= R_gamma <= -1/3`.

The lower bound is the P1 Lemma 3.2 bound. For the upper bound, `R_gamma <= -1/3` is equivalent to

`3(sin(alpha)-alpha cos(alpha)) >= sin^3(alpha)`.

The difference has value zero at `alpha=0` and derivative

`3 sin(alpha)[alpha-sin(alpha)cos(alpha)] >= 0`,

since `alpha-sin(alpha)cos(alpha)` has derivative `2 sin^2(alpha)>=0`. The proof below needs only `R_gamma<=0`.

## 3. Exact phi-average of the transverse kernel

Take `v=e_x` in P1 Lemmas 3.3–3.4. At `rho=0`,

`h_rho=-lambda b`, `D_rho=-b/D`, `D_rhorho=(1-b^2/D^2)/D`.

Define

`C := -lambda/(wD)+gamma/D^2 = (lambda/w)(q-D^2)/D^3`.

Then

`gamma_rho=b C`,

`gamma_rhorho=-gamma/D^2+b^2[-2lambda/(wD^3)+3gamma/D^4]`.

P1 Lemma 3.4 gives

`F_rhorho=-4 h_rho R gamma_rho -2 h R_gamma gamma_rho^2 -2 h R gamma_rhorho`.

At `rho=0`, the quantities `h,D,w,gamma,R,R_gamma,C` depend on `mu,lambda` but not on `phi`; only `b` carries the azimuthal dependence. Since

`(1/(2pi)) integral_0^{2pi} b^2 dphi = a^2/2`,

the azimuthal average is exactly

`<F_rhorho>_phi = R A + R_gamma B`,                         (3.1)

where

`A = 2h gamma/D^2 + a^2[2lambda C + 2h lambda/(wD^3) - 3h gamma/D^4]`,

`B = -h a^2 C^2`.                                          (3.2)

Hence immediately

`B <= 0`, and therefore `R_gamma B >= 0`.                  (3.3)

No pointwise sign of `A` is asserted.

## 4. Algebraic reduction of A

Substitute the north-pole formulas of §2 into (3.2). Straight expansion and collection give

`A = lambda^2 sqrt(q) P(q,y) / [w d^(5/2)]`,               (4.1)

where `y=lambda^2` and

`P(q,y) = 2 y^2 q^3 - 4 y^2 q^2 - 4 y q^3 + 12 y q^2 - 6 y q`

`         + 2 q^3 - 8 q^2 + 9 q - 2`.                     (4.2)

For completeness, the other coefficient becomes

`B = -lambda^3 q(2-q)[1-(1-y)q]^2 / [w^2 d^3] <= 0`.      (4.3)

Thus all sign difficulty is confined to the cubic polynomial `P` in (4.1).

## 5. Elementary control of the negative part of P

Differentiate (4.2) in `q`:

`P_q = 6(1-y)^2 q^2 - 8(1-y)(2-y)q + 9 - 6y`.             (5.1)

For `0<=q<=1/2`, discard the nonnegative quadratic term and use `q<=1/2` in the negative linear term:

`P_q >= 9-6y-4(1-y)(2-y) = 1+6y-4y^2 > 0`.               (5.2)

So `P` is increasing in `q` on `[0,1/2]`, uniformly in the frozen `y` range.

At the three left endpoints needed below,

`P(0,y)=-2`,

`P(1/8,y)=-(15y^2+146y+255)/256`,

`P(1/4,y)=-(7y^2+26y+7)/32`.

The magnitudes of the last two expressions increase with `y`. At `y<=8649/40000`, direct rational comparison gives

`-P(1/8,y) < 9/8`,

`-P(1/4,y) < 41/100`.                                     (5.3)

Consequently, wherever `P<0`, its magnitude is bounded by

`|P| <= 2` on `[0,1/8]`,

`|P| < 9/8` on `[1/8,1/4]`,

`|P| < 41/100` on `[1/4,3/8]`.                            (5.4)

Section 6 proves `P>0` from `q=3/8` onward, so (5.4) covers the entire negative part.

## 6. Rational lower bounds for the positive part of P

For fixed `q in [0,2]`, the coefficient of `y^2` in `P` is

`2q^2(q-2) <= 0`.

Thus `P(q,y)` is concave in `y`, and its minimum over `y in [4/25,8649/40000]` occurs at one of the two rational endpoints.

For a cubic on a rational interval `[u,v]`, put `q=u+(v-u)x`, `0<=x<=1`, and expand `P(q,y)-m` in the degree-3 Bernstein basis

`sum_{i=0}^3 c_i binom(3,i) x^i(1-x)^(3-i)`.

Every basis function is nonnegative and their sum is one, so nonnegative Bernstein coefficients imply `P>=m`. The following table gives, for each interval and each endpoint of the `y` range, the **smallest** of the four exact Bernstein coefficients after subtracting the stated lower bound `m`:

| q interval | m | y=4/25: min coefficient | y=8649/40000: min coefficient |
|---|---:|---:|---:|
| `[3/8,1/2]` | `1/6` | `25609/480000` | `243134449/1228800000000` |
| `[1/2,1]` | `3/5` | `127/2500` | `43664397/6400000000` |
| `[1,3/2]` | `9/10` | `31/2500` | `1394033191/6400000000` |
| `[3/2,2]` | `59/100` | `23/2500` | `314544799/1200000000` |

All entries are strictly positive. Concavity in `y` therefore gives the uniform bounds

`P >= 1/6` on `[3/8,1/2]`,

`P >= 3/5` on `[1/2,1]`,

`P >= 9/10` on `[1,3/2]`,

`P >= 59/100` on `[3/2,2]`.                               (6.1)

In particular `P>0` for all `q in [3/8,2]`.

## 7. The positive A contribution

On the region where the bounds (6.1) apply, `w<=1`, `d<=2`, and therefore from (4.1)

`A >= lambda^2 sqrt(q) P / 2^(5/2)`.

Use `sqrt(2)<3/2`, hence `2^(5/2)=4sqrt(2)<6`, and on the four intervals respectively use

`sqrt(q) >= 3/5, 7/10, 1, 6/5`.

Multiplying each constant lower bound by its interval length gives

`integral_{P>0} A dq`

`> (lambda^2/6)[(1/6)(1/8)(3/5) + (3/5)(1/2)(7/10)`

`                  + (9/10)(1/2) + (59/100)(1/2)(6/5)]`

`= lambda^2 (2053/12000)`.                                (7.1)

Since `lambda>=2/5`,

`integral_{P>0} A dq > lambda (2053/30000) > lambda (17/250)`.  (7.2)

## 8. The negative A contribution

Where `P<0`, (4.1) and `w>=lambda` give

`|A| <= lambda sqrt(q)|P| d^(-5/2)`.                      (8.1)

Since `d=2-(1-y)q`, on the three intervals of (5.4) its lower bounds are respectively

`379/200`, `179/100`, `337/200`,

obtained at the right endpoint in `q` and at `y=4/25`. Direct squaring of positive rational quantities gives the convenient upper bounds

`(379/200)^(-5/2) < 21/100`,

`(179/100)^(-5/2) < 6/25`,

`(337/200)^(-5/2) < 11/40`.                               (8.2)

For the three square-root integrals, using

`sqrt(1/8)<71/200`, `sqrt(1/8)>7/20`, `sqrt(3/8)<123/200`,

we have

`integral_0^(1/8) sqrt(q)dq < 71/2400`,

`integral_(1/8)^(1/4) sqrt(q)dq < 13/240`,

`integral_(1/4)^(3/8) sqrt(q)dq < 169/2400`.              (8.3)

Combining (5.4), (8.1), (8.2), and (8.3),

`integral_{P<0} |A| dq`

`< lambda [ 2(71/2400)(21/100)`

`          + (9/8)(13/240)(6/25)`

`          + (41/100)(169/2400)(11/40) ]`

`= lambda (335899/9600000)`.                              (8.4)

Since `R<=pi/2<11/7`,

`integral_{P<0} |R A| dq`

`< lambda (3694889/67200000) < lambda (11/200)`,          (8.5)

where the final rational comparison has difference `1111/67200000 > 0`.

## 9. Strict positivity

On `A>=0`, `R>=1`; on `A<0`, `R<=pi/2`. Therefore (7.2) and (8.5) give

`integral_0^2 R A dq`

`> lambda [17/250 - 11/200] = lambda (13/1000) > 0`.      (9.1)

By (3.3), `R_gamma B>=0`, so from (3.1)

`integral_0^2 <F_rhorho>_phi dq > 0`.                     (9.2)

Lemma V gives the boundary second derivative by the absolutely convergent surface integral. Since `dmu=-dq` and the azimuthal average contributes the factor `2pi`,

`E_rhorho(0,lambda)`

`= (1/(2lambda)) integral_0^2 <F_rhorho>_phi dq > 0`.      (9.3)

Finally P1 Lemma 6.1(iii) gives

`H(0,lambda)=E_rhorho(0,lambda)>0`.

This proves NP-T, conditional exactly on the inherited Lemma V audit dependency declared in frozen D-AN-1 v1.1. No C-axis C1/C2 sign statement, diagnostic value, or numerical certification has entered the proof. QED.

## 10. Scope / governance note

This draft does not enlarge the frozen NP-T theorem statement. In particular it does not promote the intermediate lower estimates to a separately claimed margin theorem. It uses the direct `E_beta` route allowed by v1.1; L2 is cited as an audited dependency record but its optional paired representation is not required for the proof itself.

If chat audit finds any algebraic or rational-bound defect, NP-T remains unproved and the v1.1 fail-closed rule applies; there is no same-version numerical rescue without the separately predeclared G-number procedure required by §5.
