# D-OB P2 — D-AN-1 QM-1 Third-Directional-Derivative Majorant — DRAFT

**Status:** PAPER-PROOF DRAFT / AWAITING CHAT AUDIT / NOT A THEOREM
**Frozen parent:** `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`, commit `e9c8b1caa3ad502a3d01dafe354b61108787eed2`, SHA-256 `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217`, **FROZEN**.
**P1 source:** commit `6c6282a8`, file `analysis/D_OB_P1_DESIGN_NOTE.md`, SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`.
**Evidence:** ANALYTIC PAPER PROOF / NO DIAGNOSTIC EVIDENCE / NO INTERVAL COMPUTATION.

## 1. Purpose and scope

Frozen D-AN-1 v1.2 exposes QM as the obligation to construct an explicit uniform modulus for `E_rhorho`. QM-1 supplies one analytic ingredient for that construction: a uniform third-directional-derivative majorant for the P1 density away from the diagonal `x=p`.

For `lambda in [2/5,93/200]`, `x in bd K_lambda`, `p in closure(K_lambda)`, `x != p`, and arbitrary unit directions `u,v,s` in the base-point variable `p`, QM-1 proves

`|F_{uvs}(x,p)| <= C3 / D(x,p)^2`,

with the explicit constant

`C3 := 8788 + 39 pi`.

This note does not by itself construct `omega_E`, does not assert a third derivative of `E` up to the boundary, and does not change Lemma V. The near/far integration needed to turn this kernel bound into a quantitative modulus belongs to the subsequent QM assembly.

## 2. Pinned notation

Use the P1 definitions

`D=|x-p|`, `h=w(x-p).nu`, `gamma=h/(wD)`, `G(gamma)=arccos^2(gamma)`, `F=h G(gamma)`,

where `w=w(x)` and `nu=nu(x)` do not depend on `p`. P1 Lemma 3.1 gives

`0 <= h <= wD`, `0 <= gamma <= 1`,

and on the oblate family `lambda <= w <= 1`. Hence

`|h| <= D`, `|h_u| <= 1`, `h_{uv}=h_{uvs}=0`.

P1 Lemma 3.2 gives on `gamma in [0,1]`

`1 <= R <= pi/2`, `-1 <= R_gamma <= 0`, `G'=-2R`,

where

`R(gamma)=arccos(gamma)/sqrt(1-gamma^2)`

is understood by its analytic extension at `gamma=1`.

## 3. Scalar lemma for `R_{gamma gamma}`

**Lemma QM-1.1.** On `0 <= gamma <= 1`,

`|R_{gamma gamma}(gamma)| <= 544`.

### 3.1 The interval `0 <= gamma <= 1/2`

Direct differentiation of `R` gives the ODE identity

`(1-gamma^2) R_{gamma gamma} = 3 gamma R_gamma + R`.

Using `|R_gamma|<=1`, `R<=pi/2`, `gamma<=1/2`, and `1-gamma^2>=3/4`,

`|R_{gamma gamma}| <= (3/2 + pi/2)/(3/4) = 2 + 2pi/3 < 5`.

### 3.2 The interval `1/2 <= gamma <= 1`

Put

`q=1-gamma^2`, `R(gamma)=Psi(q)`.

The analytic chart from P1 Lemma 3.2 is

`Psi(q)=sum_{n>=0} c_n q^n`,

with

`c_n=(2n)!/[4^n (n!)^2 (2n+1)]`.

Every `c_n` is nonnegative and `c_n<=1`. Since `gamma>=1/2`, `0<=q<=3/4`. Therefore

`|Psi'(q)| <= sum_{n>=1} n q^(n-1) = 1/(1-q)^2 <= 16`,

`|Psi''(q)| <= sum_{n>=2} n(n-1) q^(n-2) = 2/(1-q)^3 <= 128`.

Because `q_gamma=-2gamma`,

`R_{gamma gamma}=4 gamma^2 Psi''(q)-2 Psi'(q)`.

Thus

`|R_{gamma gamma}| <= 4(128)+2(16)=544`.

Combining §§3.1–3.2 proves Lemma QM-1.1. The constant is deliberately conservative. A sharper scalar constant is possible by a different split, but no sharper value is needed anywhere in this draft.

## 4. Consequences for the angle function `G`

From `G'=-2R`, P1 Lemma 3.2 and Lemma QM-1.1 give

`|G'| <= pi`,

`|G''| = 2|R_gamma| <= 2`,

`|G'''| = 2|R_{gamma gamma}| <= 1088`.                    (4.1)

These bounds are uniform on the full convexity range `gamma in [0,1]`.

## 5. Mixed derivatives of `D`

Let

`n=(x-p)/D`, `P=I-n tensor n`.

For a unit direction `u` in the `p` variable,

`D_u=-n.u`, so `|D_u|<=1`.

For unit `u,v`,

`D_{uv}=((Pu).(Pv))/D`,

hence

`|D_{uv}|<=1/D`.                                         (5.1)

Differentiate `D_{uv}` in a third unit direction `s`. Since

`n_s=-Ps/D`,

the derivative of the numerator `u.Pv` has absolute value at most `2/D`, while the derivative of `D^{-1}` has absolute value at most `D^{-2}`. Therefore

`|D_{uvs}| <= 3/D^2`.                                    (5.2)

This is the mixed-direction estimate; no polarization from repeated directions is used.

## 6. Mixed derivatives of `gamma`

Put

`f:=h/w=(x-p).nu`, `g:=D^{-1}`.

Then `gamma=fg`, and, because `nu` is independent of `p`,

`|f|<=D`, `|f_u|<=1`, `f_{uv}=f_{uvs}=0`.

From §5,

`|g_u|=|D_u|/D^2 <= 1/D^2`,

`g_{uv}=2D_uD_v/D^3-D_{uv}/D^2`,

so

`|g_{uv}| <= 3/D^3`.                                     (6.1)

Differentiating once more,

`g_{uvs}=-D_{uvs}/D^2`

`          +2(D_{uv}D_s+D_{us}D_v+D_{vs}D_u)/D^3`

`          -6D_uD_vD_s/D^4`.

Using (5.1)–(5.2),

`|g_{uvs}| <= (3+6+6)/D^4 = 15/D^4`.                    (6.2)

The product rule now gives the uniform mixed bounds

`|gamma_u| <= |f_u|/D + |f| |g_u| <= 2/D`,              (6.3)

`|gamma_{uv}| <= |f_u g_v|+|f_v g_u|+|f g_{uv}| <= 5/D^2`,  (6.4)

and

`gamma_{uvs}=f_u g_{vs}+f_v g_{us}+f_s g_{uv}+f g_{uvs}`.

Hence

`|gamma_{uvs}| <= (3+3+3+15)/D^3 = 24/D^3`.             (6.5)

Equations (6.3)–(6.5) extend the repeated-direction P1 bounds to the mixed directions required below.

## 7. Third derivative of the density

Since `F=h G(gamma)` and all second and third `p` derivatives of `h` vanish,

`F_{uvs}` equals

`h_u [G'' gamma_v gamma_s + G' gamma_{vs}]`

`+ h_v [G'' gamma_u gamma_s + G' gamma_{us}]`

`+ h_s [G'' gamma_u gamma_v + G' gamma_{uv}]`

`+ h [G''' gamma_u gamma_v gamma_s`

`     + G''(gamma_{uv}gamma_s+gamma_{us}gamma_v+gamma_{vs}gamma_u)`

`     + G' gamma_{uvs}]`.                                (7.1)

For each of the first three bracketed terms, (4.1) and (6.3)–(6.4) give

`|G'' gamma_v gamma_s + G' gamma_{vs}|`

`<= [2*2*2 + pi*5]/D^2 = (8+5pi)/D^2`.

Since `|h_u|,|h_v|,|h_s|<=1`, their total contribution is at most

`(24+15pi)/D^2`.                                         (7.2)

For the final `h` term, use `|h|<=D`. Its bracket in (7.1) is bounded by

`[1088*(2^3) + 2*(3*5*2) + pi*24]/D^3`

`= (8764+24pi)/D^3`.

Therefore its contribution is at most

`(8764+24pi)/D^2`.                                       (7.3)

Adding (7.2) and (7.3) yields

`|F_{uvs}(x,p)| <= (8788+39pi)/D(x,p)^2`.                (7.4)

This proves the announced constant

`C3=8788+39pi`.

## 8. What QM-1 does and does not supply

QM-1 supplies an explicit pointwise Lipschitz majorant for every second directional density derivative away from `x=p`: along any base-point segment that stays a positive distance from `x`, the mean-value theorem and (7.4) control the change of `F_{uv}` by `C3 D^{-2}` times the segment length, with the distance taken along that segment.

It does not integrate this singular majorant over the boundary and does not claim that `D^{-2}` is globally integrable at a boundary base point. The global QM modulus must split near and far boundary regions and combine this third-derivative estimate with the already audited area-growth and second-derivative bounds from P1. That assembly is separate from this draft.

No diagnostic quantity enters any constant above. No interval computation is used or authorized.

## 9. Verdict and governance

The scalar angle-function residue and the mixed-direction residue needed for the third-density bound are closed analytically in this draft:

- `|R_{gamma gamma}| <= 544` on `[0,1]`;
- `|D_{uvs}| <= 3/D^2`;
- `|gamma_u| <= 2/D`, `|gamma_{uv}| <= 5/D^2`, `|gamma_{uvs}| <= 24/D^3`;
- `|F_{uvs}| <= (8788+39pi)/D^2`.

These are paper-proof claims awaiting audit. They do not yet discharge the full frozen QM node, because an explicit nondecreasing modulus `omega_E` has not been assembled here.

**Operational status:** QM-1 DRAFT / AWAITING CHAT AUDIT / QM NOT YET COMPLETE / L1 PAUSED / NO DIAGNOSTIC EVIDENCE / NO INTERVAL COMPUTATION / D-P2 NOT_CERTIFIED.
