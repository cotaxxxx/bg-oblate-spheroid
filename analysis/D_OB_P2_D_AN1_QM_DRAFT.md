# D-OB P2 — D-AN-1 QM Quantitative Modulus — DRAFT

**Status:** PAPER-PROOF DRAFT / AWAITING CHAT AUDIT / NOT A THEOREM
**Frozen parent:** `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`, commit `e9c8b1caa3ad502a3d01dafe354b61108787eed2`, SHA-256 `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217`, **FROZEN**.
**QM-1 input:** `analysis/D_OB_P2_D_AN1_QM1_DRAFT.md`, commit `930b44bb6ce2ab9d7298556e8f5ff1768386857c`, SHA-256 `dd001338000ed8cf98ec13ce8b15fe4badd833f08826becfd8fc777d39848186`, **CHAT AUDIT PASS**.
**P1 source:** commit `6c6282a8`, file `analysis/D_OB_P1_DESIGN_NOTE.md`, SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`.
**Evidence:** ANALYTIC PAPER PROOF / NO DIAGNOSTIC EVIDENCE / NO INTERVAL COMPUTATION.

## 1. Target

Frozen D-AN-1 v1.2 requires an explicit nondecreasing modulus `omega_E:[0,infinity)->[0,infinity)`, uniform in `lambda in [2/5,93/200]`, such that

`|E_rhorho(p)-E_rhorho(p')| <= omega_E(|p-p'|)`

on a closed region containing all swept points needed by Sigma, with `omega_E(0)=0` and `omega_E(d)->0` as `d->0+`.

This draft proves the stronger statement on the full convex body `closure(K_lambda)` for every frozen lambda.

Put

`C2 := 9 pi + 8`,

`C3 := 8788 + 39 pi`.

The proposed modulus uses the natural logarithm and is

`omega_E(0):=0`,

for `0<d<=1/2`,

`omega_E(d):=50 C2 d + 25 C3 d [1+2 log(1/d)]`,          (1.1)

and for `d>=1/2`,

`omega_E(d):=omega_E(1/2)`.

The remainder of the draft proves that this function has all frozen QM properties.

## 2. Uniform input bounds

For `x in bd K_lambda`, `p in closure(K_lambda)`, write `D_p=|x-p|`. P1 Lemma 3.4 gives, for the rho-direction second derivative,

`|F_rhorho(x,p)| <= C2/D_p`.                              (2.1)

P1 has

`E_rhorho(p)=(1/(4 pi lambda)) integral_{bd K_lambda} F_rhorho(x,p) dA(x)/w(x)`.

Uniformly on the frozen lambda interval,

`1/lambda <= 5/2`, `1/w <= 5/2`.                         (2.2)

P1 Lemma 4.1 gives

`area(bd K_lambda intersect B(p,s)) <= 4 pi s^2`,         (2.3)

and P1 Lemma 4.2 gives, for any measurable surface set `A` of area `M`,

`integral_A dA/D_p <= 2 sqrt(4 pi M)`.                    (2.4)

Finally, audited QM-1 gives for arbitrary unit base-point directions `u,v,s`, away from `x=p`,

`|F_{uvs}(x,p)| <= C3/D_p^2`.                             (2.5)

No constant in (2.1)–(2.5) depends on lambda.

## 3. A uniform absolute bound for `E_rhorho`

Take `A=bd K_lambda` in (2.4). Since `area(bd K_lambda)<=4 pi`,

`integral dA/D_p <= 8 pi`.

Using (2.1)–(2.2),

`|E_rhorho(p)|`

`<= (1/(4 pi lambda)) (5/2) C2 (8 pi)`

`<= (25/2) C2`.                                          (3.1)

Therefore for all `p,p' in closure(K_lambda)`,

`|E_rhorho(p)-E_rhorho(p')| <= 25 C2`.                   (3.2)

This bound will close the large-distance part of the modulus.

## 4. Near/far split for `0<d<=1/2`

Fix `p,p' in closure(K_lambda)` and put

`d:=|p-p'|`, `0<d<=1/2`, `eta:=2d`.

Let

`A_near := {x in bd K_lambda : D_p <= eta}`,

`A_far := bd K_lambda \ A_near`.

Because `K_lambda` is convex, the segment

`p_t=(1-t)p+t p'`, `0<=t<=1`,

lies in `closure(K_lambda)`.

We estimate the two surface regions separately.

## 5. Near contribution

By (2.3),

`area(A_near) <= 4 pi eta^2`.

Applying (2.4) to the same set `A_near`, first with base point `p` and then with base point `p'`, gives

`integral_{A_near} dA/D_p <= 8 pi eta`,

`integral_{A_near} dA/D_{p'} <= 8 pi eta`.                (5.1)

Hence, using the triangle inequality, (2.1), and (2.2),

`Near`

`:= (1/(4 pi lambda)) integral_{A_near} |F_rhorho(x,p)-F_rhorho(x,p')| dA/w`

`<= (1/(4 pi lambda))(5/2) C2 [8 pi eta+8 pi eta]`

`<= 25 C2 eta`

`= 50 C2 d`.                                              (5.2)

This estimate does not require `p'` to lie near the same nearest boundary point; Lemma 4.2 is applied to the fixed measurable set `A_near` with each base point separately.

## 6. Far `D^{-2}` integral

For `x in A_far`, `D_p>=eta`. Since both `x` and `p` lie in the unit ball, `D_p<=2`.

For `eta<=D_p<=2`,

`1/D_p^2 = 1/4 + integral_{D_p}^{2} 2 s^{-3} ds`.

Integrating and using (2.3),

`integral_{A_far} dA/D_p^2`

`<= area(bd K_lambda)/4 + integral_eta^2 2 s^{-3} area(bd K_lambda intersect B(p,s)) ds`

`<= pi + 8 pi log(2/eta)`

`<= 4 pi + 8 pi log(2/eta)`.                              (6.1)

The last, slightly coarser, form is retained because it yields a simple monotonic modulus below.

## 7. Far contribution by the mean-value theorem

For `x in A_far` and every `t in [0,1]`,

`D(x,p_t) >= D_p-|p_t-p| >= D_p-d`.

Since `D_p>=eta=2d`,

`D(x,p_t) >= D_p/2`.                                     (7.1)

Let `s=(p'-p)/d`. Applying the one-variable mean-value theorem to the scalar function

`t -> F_rhorho(x,p_t)`

and using QM-1 with directions `(e_rho,e_rho,s)`, (7.1) gives

`|F_rhorho(x,p)-F_rhorho(x,p')|`

`<= d sup_t C3/D(x,p_t)^2`

`<= 4 C3 d/D_p^2`.                                       (7.2)

Therefore, by (2.2) and (6.1),

`Far`

`:= (1/(4 pi lambda)) integral_{A_far} |F_rhorho(x,p)-F_rhorho(x,p')| dA/w`

`<= (1/(4 pi lambda))(5/2)(4 C3 d) integral_{A_far} dA/D_p^2`

`<= (25 C3 d/(4 pi)) [4 pi+8 pi log(2/eta)]`

`=25 C3 d [1+2 log(2/eta)]`.                              (7.3)

With `eta=2d`,

`Far <= 25 C3 d [1+2 log(1/d)]`.                         (7.4)

## 8. Modulus for `0<d<=1/2`

Combining (5.2) and (7.4),

`|E_rhorho(p)-E_rhorho(p')|`

`<= 50 C2 d +25 C3 d [1+2 log(1/d)]`

`=omega_E(d)`                                             (8.1)

for all `0<d<=1/2`.

The formula is explicit and uniform in lambda.

## 9. Monotonicity and continuity at zero

For `0<d<=1/2`, differentiating (1.1) gives

`omega_E'(d)=50 C2 +25 C3 [2 log(1/d)-1]`.                (9.1)

Since

`log 2 = integral_1^2 dt/t > 1/2`,

we have `2 log(1/d)-1 >= 2 log 2-1 >0` on `(0,1/2]`. Hence

`omega_E'(d)>0` on `(0,1/2]`.                            (9.2)

For `d>=1/2` the definition is constant, so `omega_E` is nondecreasing on `[0,infinity)`.

Also

`d log(1/d) -> 0` as `d->0+`.

Therefore (1.1) gives

`omega_E(d)->0=omega_E(0)` as `d->0+`.                   (9.3)

Thus `omega_E` is continuous at zero, as required by the frozen node.

## 10. Large distances

At the joining point,

`omega_E(1/2)=25 C2 +(25/2) C3 [1+2 log 2] >25 C2`.      (10.1)

For `d>=1/2`, (3.2) therefore gives

`|E_rhorho(p)-E_rhorho(p')| <=25 C2 < omega_E(1/2)=omega_E(d)`.  (10.2)

Hence the modulus inequality holds for every pair `p,p' in closure(K_lambda)`, not merely for small distances.

## 11. Consequence for `H`

For meridional points `p=(rho,z)`, `p'=(rho',z')`, P1 Lemma 6.1 gives

`H(rho,z)=integral_0^1 E_rhorho(t rho,z) dt`.

For each `t in [0,1]`,

`|(t rho,z)-(t rho',z')| <= |(rho,z)-(rho',z')|`.         (11.1)

Because `omega_E` is nondecreasing,

`|H(p)-H(p')|`

`<= integral_0^1 omega_E(|(t rho,z)-(t rho',z')|) dt`

`<= omega_E(|p-p'|)`.                                    (11.2)

Thus the same explicit modulus controls the H difference required by L3-MRA and frozen v1.2.

## 12. Frozen-domain and lambda uniformity check

The proof was carried out on all of `closure(K_lambda)`, which is stronger than the frozen requirement of a closed region containing every swept Sigma segment point. Every such point lies in `closure(K_lambda)`.

Uniformity in `lambda in [2/5,93/200]` is explicit: the only lambda-dependent prefactors were replaced by

`1/lambda <=5/2`, `1/w<=5/2`,

and the constants `C2`, `C3`, `4 pi`, and the unit-ball diameter bound are lambda-independent.

No diagnostic value, observed numerical margin, or interval computation enters `omega_E`.

## 13. Verdict and governance

This draft supplies the full frozen QM deliverable:

- an explicit `omega_E:[0,infinity)->[0,infinity)`;
- `omega_E(0)=0`;
- continuity at zero;
- nondecreasing behavior;
- uniformity in `lambda in [2/5,93/200]`;
- the inequality `|E_rhorho(p)-E_rhorho(p')|<=omega_E(|p-p'|)` on the stronger domain `closure(K_lambda)`;
- the same modulus for `H` on the swept meridional region.

The only new analytic input beyond audited P1 is audited QM-1. No third derivative of the integrated energy is asserted; QM-1 is used only under the far-region mean-value theorem where the segment stays a positive distance from the fixed surface point `x`.

If this draft passes chat audit, the frozen QM node is discharged. L3 may then use this modulus together with a proved FT_q margin `m0` to choose an explicit rational `delta0` satisfying `omega_E(delta0)<m0`. L1 remains PAUSED until that delta0 exists.

**Operational status:** QM DRAFT / AWAITING CHAT AUDIT / QM-1 AUDIT PASS / FT_q STILL REQUIRED FOR delta0 / L1 PAUSED / NO DIAGNOSTIC EVIDENCE / NO INTERVAL COMPUTATION / D-P2 NOT_CERTIFIED.
