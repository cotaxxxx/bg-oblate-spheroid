# OBLATE AXIAL LOWER-HALF ANALYTIC LEMMA — C1a TRANSFER

**Status:** DRAFT / CHAT_AUDIT_PENDING / NOT_BINDING / NO_NEW_NUMERICAL_RUN

2026-11-16 / Dig / proposed A1 completion per chat V22 audit (`680eda0`).
This document **does not claim chat audit PASS or Judge certification**.

## 0. Pinned premises and transferred assertion

**Premise:** `analysis/OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA.md`,
Git blob `6fba6e4f981d08201a779be2a435b49954c8b659`.
Its proved statements (Lemmas 1–11 and 14–17, Proposition 12,
Corollaries 13 and 18) were written for
`B = { (t,lambda): |t| <= 1/2, 9/20 <= lambda <= 5/8 }`.

**Method template:** `analysis/OBLATE_AXIAL_LOWER_HALF_LEMMA_C0_TRANSFER.md`,
Git blob `0ab178967075459faf7bdc43dcf09e449492b130`,
adopted for `B0 = [-1/2,1/2] × [2/5,83/200]`.

**Claim for independent audit:** Every statement and formula of the premise
specified above remains valid with `B` replaced throughout by

```text
B_1a := { (t,lambda): |t| <= 1/2, 83/200 <= lambda <= 9/20 }.
```

All hypotheses `mu ∈ [-1,1]`, `s ∈ [0,sqrt(2)]`,
`0<lambda<1`, and the definitions of `E_lambda`, `g_axis_ob`,
`q`, `w`, `gamma`, `u`, `A`, `F`, and `Phi` are *unchanged*.
No newly assumed numerical approximation is used.

## 1. Seven lambda-dependent lemmas; exact constants

Use `L=lambda^2`, `a=1-L`, `A=1-t mu`,
`q=1-mu^2+lambda^2(mu-t)^2`,
`w^2=mu^2+lambda^2(1-mu^2)`, `u=1-gamma^2`.
All inequalities are uniform on `B_1a×[-1,1]_mu`.

| Pinned lemma | Changed constant or proof obligation | Exact result on B_1a |
|---|---|---|
| **Lemma 3** | Concavity of `q` in `mu`; endpoints `mu=±1` | `q >= lambda^2/4 >= (83/200)^2/4 = 6889/160000 > 0` |
| **Lemma 4** | `w^2 = lambda^2+(1-lambda^2)mu^2` | `w >= lambda >= 83/200 > 0` |
| **Lemma 5** | Lower bound `u>=0`, the endpoint majorant `u <= (1-lambda^2/2)^2`; interior critical point `|Lt/a|` | `0 <= u <= u_max=(1-(83/200)^2/2)^2=5345218321/6400000000 < 1`; `|Lt/a| <= (1/2)(9/20)^2/(1-(9/20)^2)=81/638<1` |
| **Lemma 6** | Compact analyticity interval for `Psi` and its first three derivatives | Replace `u_max` by `5345218321/6400000000`; `K_Psi<infinity` remains valid |
| **Lemma 8** | Uniform `gamma` derivatives through order four use lower bounds on `q,w` | `q>=6889/160000`, `w>=83/200`; hence `K_gamma<infinity` |
| **Lemma 9** | Pointwise `C^4` of `F(s,·,lambda)`; excludes branch and denominator singularities | `q,w>0` and `u<=u_max<1` on `B_1a`; same proof |
| **Lemma 10** | Uniform integral majorant `|partial_t^j F_t|<=sM` for `j=0,1,2,3` | Use `u_max=5345218321/6400000000`, `q_min=6889/160000`, `w_min=83/200`, and `|A|<=3/2`; existence of finite `M` by the same finite derivative bounds |

**Proof of Lemma 5's changed maximum.**
The exact factorization of the premise gives
`u=(1-mu^2)(a mu+L t)^2/(w^2 q)`, with `0<=u`, and
`(1-mu^2)/q<=1`. Thus `u<=f(mu)=(a mu+L t)^2/(a mu^2+L)`.
For `|t|<=1/2`, `A>=1/2`.
The only interior critical zero of `f` is `mu_0=-Lt/a`
and lies in `(-1,1)`, since `81/638<1`; it is a minimum.
The maximum occurs at `mu=±1`, giving
`f<= (a+L/2)^2=(1-lambda^2/2)^2`.
This last function decreases as `lambda` increases in `(0,1)`,
so it is bounded by its value at `83/200`. This supplies a
uniform `u_max<1`, without claiming it is the true supremum of `u`.

**Other common constants:** `|A|=|1-t mu|<=3/2`;
`A>=1/2`; `|gamma|<=1`; `0<L,a<1`. The bounds from the
C0-transfer template used by Lemmas 8–10 are replaced only by
the exact rational constants displayed above.

## 2. Range-independent argument and analytic identity pins

- **Lemmas 1–2:** Congruence invariance and evenness
  `E_lambda(-t)=E_lambda(t)` use only reflection of the rotational
  ellipsoid and `0<lambda<1`.
- **Lemma 7:** The coefficient bounds for the first three derivatives
  of `R=Psi(u)` use `|gamma|<=1` and the Lemma 6 constant.
- **§3.1–§3.6 and Lemma 10:** Parameter substitution, angular branch
  `0<gamma<=1`, differentiation of `F=s A alpha^2`, and
  compact uniform `sM` majorants depend on the range only through
  the positivity and compact bounds of §1.
- **Lemma 11, Proposition 12, Corollary 13:** Differentiation under the
  integral gives
  `g_axis_ob(t,lambda)=∫_0^{sqrt(2)} F_t(s,t,lambda) ds`,
  `C^3` in `t` on `[-1/2,1/2]`, and oddness of `g`
  from evenness of `E`.
- **Lemmas 14–16:** The quotient `g(t,lambda)/t` extends through
  `t=0` via `Phi~(t,lambda)=∫_0^1 partial_t g(vt,lambda)dv`.
  It descends to `Phi(tau,lambda)`, `tau=t^2`, with
  `Phi(0,lambda)=H_axis_ob(lambda)`. The exact identity, including
  the right derivative at `tau=0`, is
  ```text
  partial_tau Phi(tau,lambda)
     = (1/2) ∫_[0,1] ∫_[0,1] v^2 partial_t^3 g(u v sqrt(tau),lambda) du dv
     = (1/4) ∫_[0,1] (1-x^2) partial_t^3 g(x sqrt(tau),lambda) dx.
  ```
  The two integration dummy variables in the first display are
  interchangeable; the original source uses `u^2` and `v u t`.
- **Lemma 17:** `0<=x<=1`, `0<=t<=1/2` implies `0<=xt<=1/2`;
  the third-derivative sign is never sampled outside the transferred box.
- **Corollary 18:** If `partial_t^3 g<0` on `[0,1/2]×[83/200,9/20]`,
  then the nonnegative kernel `1-x^2`, strictly positive for `0<=x<1`,
  gives `partial_tau Phi<0` for `0<=tau<=1/4`.

In particular, **the transfer does not prove a new third-derivative sign**.
That input is supplied by the already audited C1a machine Gate A, pinned by
`analysis/GLOBAL_AXIAL_C1A_MACHINE_RECEIPT.md` (blob
`e494e789cbceb1c8b7cfc8acfae92a1d44c08c90`), scope
`[0,1/2]×[83/200,9/20]`.
The source for `F_x(lambda)=Phi(1/4,lambda)=2g(1/2,lambda)`
is Lemma 14 and C1a's existing normalization.

## 3. Limited consequence for global C-axis assembly

Combining the *transferred lemma* with C1a Gate A, conditional on chat
acceptance of this transfer, yields
```text
partial_tau Phi(tau,lambda) < 0
for 0 <= tau <= 1/4, 83/200 <= lambda <= 9/20.
```
The endpoint values `Phi(0,lambda)=H_axis_ob(lambda)` and
`Phi(1/4,lambda)=F_x(lambda)` then permit the lower-half root count:
`H>0, F_x<0` implies one root in `(0,1/2)`;
`H>0, F_x=0` implies one root at `t=1/2`;
and `F_x>0` implies no positive root at `t<=1/2`.
These are **logical consequences contingent on the signed C1a/C0 inputs**
and a future independent audit; not new standalone machine evidence.

This transfer makes no claim on `1/2<t<=1`, on off-axis stationary points,
or on global CLOSED. The predecessor C0 transfer, source lemma, and prior
machine certificates are not modified or re-executed.

## 4. Independent-audit request

Check the seven range-dependent lemma replacements (3,4,5,6,8,9,10)
in exact rational arithmetic, verify the unchanged steps (§2), then check
the link C1a Gate A → Corollary 18 with `Phi(0)=H` and
`Phi(1/4)=F_x`. The output of this file is **DRAFT until chat PASS**.
