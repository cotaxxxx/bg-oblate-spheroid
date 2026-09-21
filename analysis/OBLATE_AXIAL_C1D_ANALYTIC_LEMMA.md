# C1D ANALYTIC LEMMA FOR THE OBLATE AXIAL FUNCTIONAL

**Status**: `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`

**Purpose.** To supply, as a self-contained and independently auditable statement, the analytic facts needed for the C1d assembly: the integral representation of the axial gradient, its `C^3` regularity on the compact C1d interval, its parity in `t`, the extension of the reduced quotient `Phi` through the origin, and the identity for `partial_tau Phi`. No non-binding document is used as a premise; prior records stating the same facts are cited as provenance only.

**Scope.** `B' := { (t,lambda) : |t| <= 31/32, 5/8 <= lambda <= 33/50 }`, with `mu` in `[-1,1]`, `s` in `[0, sqrt 2]`.

**Dependency order.** §1 (definitions, congruence) → §2 (uniform bounds) → §3 (kernel: `E -> F -> F_t -> majorants`) → §4 (`g = integral F_t ds`, `C^3`, parity) → §5 (`Phi`, `partial_tau Phi`) → §6 (containment, sign propagation). Each section uses only earlier ones.

**Provenance (non-normative).** This artifact was constructed from the corrected lower-half analytic lemma, `analysis/OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA.md`, blob `6fba6e4f981d08201a779be2a435b49954c8b659`, as a transcription template only; that artifact is not a logical premise. Parity: `CENTER_PITCHFORK_SYMBOLIC_NOTE.md`. Quotient `Phi` and the `partial_tau Phi` identity: C0 contract `19fdb750`. Notation `F_x = Phi(1/4,lambda) = 2 g(1/2,lambda)`: C1 contract `80f2c2bd`. Low-order densities: `CENTER_PITCHFORK_SYMBOLIC_NOTE.md`, `GT_BOUNDARY_SYMBOLIC_AUDIT.md`.

## §1 Definitions and congruence invariance

For a convex body `K` with outward unit normal `nu_K` and interior basepoint `p`:

```
alpha_{K,p}(x) = arccos( (x-p).nu_K(x) / |x-p| )
d mu_{K,p}(x)  = (x-p).nu_K(x) / (3 Vol K) dA(x)
E_K(p)         = integral_{bd K} alpha_{K,p}(x)^2 d mu_{K,p}(x)
```

For `K_lambda = { x^2+y^2+z^2/lambda^2 <= 1 }`, `0 < lambda < 1`, the axial basepoint is `p(t) = (0,0,lambda t)`, interior for `|t| < 1`, and

```
E_lambda(t) := E_{K_lambda}(p(t)),     g_axis_ob(t,lambda) := partial_t E_lambda(t).
```

**Lemma 1 (congruence invariance).** `E_{QK}(Qp) = E_K(p)` for every `Q` in `O(3)`.

*Proof.* `Q` is a linear isometry: `|Qx-Qp| = |x-p|`; the outward normal transforms as `nu_{QK}(Qx) = Q nu_K(x)`, and `(Qx-Qp).Q nu_K(x) = (x-p).nu_K(x)`. Hence `alpha` is unchanged pointwise under `x -> Qx`. Surface measure and volume are preserved, so `d mu` is unchanged. The map `x -> Qx` is a bijection `bd K -> bd QK`. ∎

**Lemma 2 (evenness of `E_lambda`).** `E_lambda(-t) = E_lambda(t)` for every `|t| < 1`, in particular on `B'`.

*Proof.* Take `Q = -I`. Then `-K_lambda = K_lambda`, since `K_lambda` is defined by an even quadratic form, and `-p(t) = p(-t)`. Apply Lemma 1. ∎

*Remark.* Lemma 2 is an identity between values and uses no differentiability. Parity of `g_axis_ob` is deduced only in §4, after `C^3` regularity.

## §2 Uniform bounds

Write

```
mu = 1 - s^2,   e = 1 - mu^2,   A = 1 - t mu,   d = t - mu,
q = e + lambda^2 d^2 = 1 - mu^2 + lambda^2 (mu-t)^2,
w^2 = mu^2 + lambda^2 e = lambda^2 + (1-lambda^2) mu^2,
gamma = lambda A / (w sqrt q),   u = 1 - gamma^2,
L = lambda^2,   a = 1 - L  (so 0 < a < 1 on B').
```

**Lemma 3.** On `B'`, `q >= lambda^2/1024 >= 25/65536`.

*Proof.* For fixed `t, lambda`, `q''(mu) = 2(lambda^2-1) < 0`, so `q` is strictly concave in `mu` and its minimum over `[-1,1]` is at an endpoint. At `mu = ±1`, `1-mu^2 = 0`, so `q = lambda^2(±1-t)^2`; and `|t| <= 31/32` gives `|±1-t| >= 1/32`. ∎

**Lemma 4.** On `B'`, `w >= lambda >= 5/8`.

*Proof.* `w^2 = lambda^2 + (1-lambda^2) mu^2 >= lambda^2`. ∎
**Lemma 5.** On `B'`, `0 <= u <= (1 - lambda^2/32)^2 <= (2023/2048)^2 = 4092529/4194304 < 1`.

*Proof.* Lower bound. The factorization

```
w^2 q - lambda^2 A^2 = (1 - mu^2) [ mu(1 - lambda^2) + lambda^2 t ]^2
```

exhibits the left side as a product of nonnegative factors, since `|mu| <= 1`. As `w^2 q > 0` by Lemmas 3–4, dividing gives

```
gamma^2 = lambda^2 A^2 / (w^2 q) <= 1,     hence u = 1 - gamma^2 >= 0.
```

Upper bound. The same factorization written as

```
u = 1 - gamma^2 = (1 - mu^2) [ a mu + L t ]^2 / (w^2 q)
```

is the form used below. Since `q = (1-mu^2) + lambda^2(mu-t)^2 >= 1-mu^2 >= 0`, the factor `(1-mu^2)/q <= 1`, so

```
u <= f(mu) := (a mu + L t)^2 / (a mu^2 + L),      where w^2 = a mu^2 + L.
```

Differentiating, `f'(mu) = 2 a L (a mu + L t)(1 - t mu) / (a mu^2 + L)^2`. On `B'`, `|t mu| <= 31/32` so `1 - t mu >= 1/32 > 0`; the only critical point is `mu_0 = -L t / a`, where `f = 0`. It lies in `(-1,1)` throughout `B`, since `L/a = lambda^2/(1-lambda^2)` is increasing in `lambda` and

```
|L t / a| <= (31/32)(33/50)^2 / (1 - (33/50)^2) = (31/32)(1089/1411) = 33759/45152 < 1.
```

So `mu_0` is a minimum and the maximum is at `mu = ±1`. With `a·1 + L = 1`, the endpoint values are `f(1) = (a + L t)^2` and `f(-1) = (a - L t)^2`; maximizing over `|t| <= 31/32` gives `(a + 31L/32)^2 = (1 - lambda^2/32)^2` in both cases (at `t = 31/32` for `mu = 1`, at `t = -31/32` for `mu = -1`). This is decreasing in `lambda`, so its maximum over `[5/8,33/50]` is at `lambda = 5/8`, giving `(2023/2048)^2 = 4092529/4194304`. ∎

*Remark (sharpness not claimed).* The step `(1-mu^2)/q <= 1` is lossy: at `mu = ±1` the true value is `u = 0` while the majorant `f` is maximal. Lemma 5 gives an explicit uniform bound strictly below 1, not the supremum of `u`.

*Remark (two distinct roles).* The value `u = 0` occurs on `B'` — at `mu = ±1` and on the interior locus `mu_0` — and is the removable singularity of `Psi`, handled in §3.3 by analytic continuation. The endpoint `u = 1` is the singular endpoint of the `u`-derivative representation of `Psi`; Lemma 5 keeps `B` uniformly inside `[0,1)`. The two facts serve different purposes.

*Remark.* The interval implementation switches charts at `u = 3/5`. That is a numerical policy of the producer and plays no role here; only `u_max < 1` is used.

## §3 The kernel

### 3.1 From the `mu`-representation to the `s`-representation

By the definitions of §1 specialized to `K_lambda` with the cone-volume normalisation `3 Vol(K_lambda) = 4 pi lambda`,

```
E_lambda(t) = (1/2) integral_{-1}^{1} A alpha^2 d mu.
```

Substituting `mu = 1 - s^2`, so `d mu = -2 s ds`, with `mu = 1 <-> s = 0` and `mu = -1 <-> s = sqrt 2`,

```
E_lambda(t) = integral_0^{sqrt 2} s A alpha^2 ds,       F(s,t,lambda) := s A alpha^2.
```

### 3.2 Branch determination

On `B'`, `A = 1 - t mu >= 1/32 > 0`, and `q, w > 0` by Lemmas 3–4, so `gamma = lambda A/(w sqrt q) > 0`. Lemma 5 gives `u = 1-gamma^2 >= 0`, hence `gamma <= 1`; therefore `gamma` lies in `(0,1]`. With `alpha = arccos(gamma)` and `u = 1 - gamma^2`,

```
alpha = arcsin(sqrt u),    sin(alpha) = sqrt u,
```

and hence, for `R := alpha / sin(alpha)`,

```
R = arcsin(sqrt u) / sqrt u = Psi(u),        alpha^2 = u R^2.
```

### 3.3 The angular factor

`Psi(u) = arcsin(sqrt u)/sqrt u` has the power series `sum_{n>=0} c_n u^n` with `c_n = (2n)!/(4^n (n!)^2 (2n+1))`, radius of convergence 1, defining the analytic continuation to `u = 0` with `Psi(0) = 1`. Thus `Psi` is real-analytic on `[0,1)`.

**Lemma 6.** With `u_max = 4092529/4194304`, there is `K_Psi < infinity` with `|Psi^{(k)}(u)| <= K_Psi` for `u` in `[0,u_max]` and `k = 0,1,2,3`.

*Proof.* `[0,u_max]` is compact in `[0,1)`, on which `Psi` is real-analytic; each `Psi^{(k)}` is continuous there and attains a finite maximum. ∎

*Remark.* No quantitative value of `K_Psi` is needed or claimed. The series truncation bounds used by the interval producer are a separate, numerical matter.

From `R = Psi(u)`, `u = 1 - gamma^2`:

```
R_gamma           = -2 gamma Psi'(u)
R_gammagamma      = 4 gamma^2 Psi''(u) - 2 Psi'(u)
R_gammagammagamma = -8 gamma^3 Psi'''(u) + 12 gamma Psi''(u)
```

**Lemma 7.** On `B'`, `|R|, |R_gamma|, |R_gammagamma|, |R_gammagammagamma| <= 20 K_Psi`.

*Proof.* By Lemma 5, `u` in `[0,u_max]`, so Lemma 6 applies; and `gamma^2 = 1-u <= 1` gives `|gamma| <= 1`. The coefficient sums are `1, 2, 6, 20`. ∎
### 3.4 `t`-derivatives of `gamma`

**Lemma 8.** There is `K_gamma < infinity` such that `|partial_t^k gamma| <= K_gamma`, `k = 1,2,3,4`, on `B'`, uniformly in `mu` in `[-1,1]`.

*Proof.* Write

```
gamma = (lambda/w) A q^{-1/2}.
```

Here `w` is independent of `t`,

```
A_t = -mu,    A_tt = 0,
q_t = 2 lambda^2 (t-mu),    q_tt = 2 lambda^2,    q_ttt = 0.
```

Repeated application of the product and chain rules therefore expresses each `partial_t^k gamma`, `1 <= k <= 4`, as a finite sum of products of bounded polynomial factors in `(mu,t,lambda)`, the bounded factor `lambda/w`, and negative half-integer powers of `q`. On the compact parameter box, Lemmas 3–4 give

```
q >= 25/65536,    w >= 5/8,    lambda <= 33/50,
```

so every such term is uniformly bounded. Taking the maximum of the four resulting bounds gives `K_gamma`. ∎

*Remark.* Negative powers of `q` could fail to be bounded only where `q -> 0`, which on the full axial domain happens only as `(mu,t) -> (1,1)`. That corner is excluded by `|t| <= 31/32`; in particular `1-t >= 1/32`, and Lemma 3 quantifies the separation. Thus this compact box needs no boundary-layer majorant of the kind required at `t = 1`.

### 3.5 Pointwise smoothness

**Lemma 9.** For each fixed `s` in `[0,sqrt 2]` and `lambda` in `[5/8,33/50]`, `F(s,·,lambda)` is `C^4` on `[-31/32,31/32]`.

*Proof.* `A` and `q` are polynomials in `t`; `q >= 25/65536 > 0` and `w >= 5/8 > 0` (Lemmas 3–4), so `gamma = lambda A/(w sqrt q)` is a composition of a rational function with `x -> x^{-1/2}` on a domain bounded away from zero, hence `C^infinity` in `t`. Then `u = 1 - gamma^2` is `C^infinity` with values in `[0,u_max]` (Lemma 5), and `Psi` is real-analytic there (§3.3), so `R = Psi(u)` and `alpha^2 = u R^2` are `C^infinity` in `t`. Finally `F = s A alpha^2` is a product of such functions. ∎

### 3.6 Successive derivatives of the density

From `A = 1 - t mu`, `A_t = -mu`. For `u > 0`, differentiating `alpha = arccos(gamma)` gives

```
alpha_t = -gamma_t / sqrt(1 - gamma^2) = -gamma_t / sqrt u,
```

so, with `C := R gamma_t` and `R = alpha/sqrt u`,

```
(alpha^2)_t = 2 alpha alpha_t = -2 (alpha/sqrt u) gamma_t = -2 R gamma_t = -2 C.
```

Extension to the locus `u = 0`. By Lemma 9, `alpha^2 = u R^2` is `C^infinity` in `t` on the whole box, so `(alpha^2)_t` is continuous there; and `R = Psi(u)`, `gamma_t` are continuous on the box by Lemma 6 and §3.4, so `-2C` is continuous there as well. The zero locus is exactly `mu = ±1` or `a mu + L t = 0`, by the factorization in Lemma 5; hence `{ u > 0 }` is dense in the box. Since `(alpha^2)_t` and `-2C` are continuous on the whole box and agree on `{ u > 0 }`, they agree everywhere by continuity. Thus

```
(alpha^2)_t = -2 C
```

holds throughout `B'`.

Differentiating `F = s A alpha^2` repeatedly, using `A_t = -mu` and `(alpha^2)_t = -2C`:

```
F_t             = s [ A_t alpha^2 + A (alpha^2)_t ]         = s [ -mu alpha^2 - 2 A C ]
partial_t F_t   = s [ -mu (alpha^2)_t - 2 A_t C - 2 A C_t ] = s [ 4 mu C   - 2 A C_t   ]
partial_t^2 F_t = s [ 6 mu C_t  - 2 A C_tt  ]
partial_t^3 F_t = s [ 8 mu C_tt - 2 A C_ttt ]
```

where, by the chain rule of §3.3 with the `gamma`-derivatives of §3.4,

```
C_t   = R_gamma gamma_t^2 + R gamma_tt
C_tt  = R_gammagamma gamma_t^3 + 3 R_gamma gamma_t gamma_tt + R gamma_ttt
C_ttt = R_gammagammagamma gamma_t^4 + 6 R_gammagamma gamma_t^2 gamma_tt
        + 3 R_gamma gamma_tt^2 + 4 R_gamma gamma_t gamma_ttt + R gamma_tttt
```

All four displays are derived here from `F = s A alpha^2`; the same identities recorded in the provenance documents serve as cross-checks, not premises.

### 3.7 Integrable majorants

**Lemma 10.** For `j = 0,1,2,3` there is `C_j < infinity`, independent of `(t,lambda)` in `B'`, with

```
|partial_t^j F_t(s,t,lambda)| <= C_j s     for all s in [0,sqrt 2], (t,lambda) in B',
```

and `M_j(s) := C_j s` is integrable on `[0,sqrt 2]`.

*Proof.* By Lemma 7 each `R`-factor is bounded by `20 K_Psi`; by Lemma 8 each `gamma`-derivative by `K_gamma`. Each of `C, C_t, C_tt, C_ttt` is a fixed finite sum of products of one `R`-factor and at most four `gamma`-derivative factors, with coefficient sums at most `15`; hence

```
|C|, |C_t|, |C_tt|, |C_ttt| <= 15 (20 K_Psi) max(1,K_gamma)^4 =: K_C.
```

By Lemma 5 and Lemma 7, `|alpha^2| = u R^2 <= u_max (20 K_Psi)^2`. On `B'`, `|mu| <= 1` and `|A| <= 63/32`. Substituting into the four displays of §3.6 gives the claim; integrability of `C_j s` on a finite interval is immediate. ∎

## §4 Integral representation, regularity, parity

**Lemma 11.** On `B'`, `g_axis_ob(t,lambda) = partial_t E_lambda(t) = integral_0^{sqrt 2} F_t(s,t,lambda) ds`.

*Proof.* By §3.1, `E_lambda(t) = integral_0^{sqrt 2} F(s,t,lambda) ds`. For each fixed `s`, `F(s,·,lambda)` is `C^4`, in particular `C^1`, by Lemma 9. By Lemma 10 with `j = 0`, `|partial_t F| = |F_t| <= C_0 s`, integrable on `[0,sqrt 2]` and independent of `t`. Dominated differentiation applies. ∎

**Proposition 12 (`C^3` regularity).** For each `lambda` in `[5/8,33/50]`, `t -> g_axis_ob(t,lambda)` is `C^3` on `[-31/32,31/32]`, and for `j = 1,2,3`

```
partial_t^j g_axis_ob(t,lambda) = integral_0^{sqrt 2} partial_t^j F_t(s,t,lambda) ds.
```

*Proof.* By Lemma 9, `F_t(s,·,lambda)` is `C^3` for each fixed `s`, with derivatives given in §3.6. By Lemma 10 these are dominated by `M_j(s) = C_j s`, integrable and independent of `t`, for `j = 1,2,3`. Starting from Lemma 11, apply dominated differentiation three times: at step `k` the pair `(partial_t^{k-1} F_t, partial_t^k F_t)` satisfies the hypotheses. Continuity of the third derivative follows from continuity of `partial_t^3 F_t` in `t` with the same domination. ∎

**Corollary 13 (parity).** On `|t| <= 31/32`, `g_axis_ob(-t,lambda) = -g_axis_ob(t,lambda)`; in particular `g_axis_ob(0,lambda) = 0`.

*Proof.* Lemma 2 gives `E_lambda(-t) = E_lambda(t)` for `|t| < 1`. Proposition 12 shows `g_axis_ob = partial_t E_lambda` is `C^3`, so `E_lambda` is differentiable on `[-31/32,31/32]`. Differentiating the even identity gives `-g_axis_ob(-t,lambda) = g_axis_ob(t,lambda)`. Setting `t = 0` gives `g_axis_ob(0,lambda) = -g_axis_ob(0,lambda)`. ∎

*Remark.* Lemma 2 was an identity between values, proved without differentiability; the differentiability needed to differentiate it is supplied only here. There is no circularity.

*Remark.* Parity implies `partial_t^j g_axis_ob` is even in `t` for odd `j`, odd for even `j`; in particular `partial_t^2 g_axis_ob(0,lambda) = 0`.
## §5 The reduced quotient

**Definition.** For `|t| <= 31/32`, `Phi~(t,lambda) := integral_0^1 partial_t g_axis_ob(u t, lambda) du`. The integrand is continuous by Proposition 12, so `Phi~` is defined at every `t` in `[-31/32,31/32]`, including `t = 0`, where `Phi~(0,lambda) = partial_t g_axis_ob(0,lambda) = H_axis_ob(lambda)`.

**Lemma 14 (quotient form away from the origin).** For `0 < |t| <= 31/32`, `Phi~(t,lambda) = g_axis_ob(t,lambda)/t`.

*Proof.* By Proposition 12 and the fundamental theorem of calculus, for `t != 0`,

```
integral_0^1 partial_t g_axis_ob(ut,lambda) du = ( g_axis_ob(t,lambda) - g_axis_ob(0,lambda) ) / t,
```

and `g_axis_ob(0,lambda) = 0` by Corollary 13. ∎

*Remark.* The definition of `Phi~` is valid at `t = 0`; the quotient representation is not. `Phi~` is the extension of `g/t` through the origin, and it is `Phi~`, not the quotient, that is used below.

**Lemma 15 (descent to `tau`).** `Phi~` is even in `t`; hence there is `Phi` with `Phi(tau,lambda) = Phi~(t,lambda)`, `tau = t^2`, defined for `tau` in `[0,961/1024]`, and `Phi(0,lambda) = H_axis_ob(lambda)`.

*Proof.* By Corollary 13, `partial_t g_axis_ob` is even in `t`, so the integrand is unchanged under `t -> -t` for every `u`; hence `Phi~(-t,lambda) = Phi~(t,lambda)`. An even function on `[-31/32,31/32]` factors through `t -> t^2`. Differentiability in `tau` is established in Lemma 16. ∎

**Lemma 16 (identity for `partial_tau Phi`).** For `tau` in `[0,961/1024]`, `lambda` in `[5/8,33/50]`, `t = sqrt(tau)`,

```
partial_tau Phi = (1/2) integral_0^1 integral_0^1 u^2 partial_t^3 g_axis_ob(v u t, lambda) dv du    (i)
                = (1/4) integral_0^1 (1-x^2) partial_t^3 g_axis_ob(x t, lambda) dx                  (ii)
```

with the derivative at `tau = 0` understood as the right derivative; in particular `partial_tau Phi(0,lambda) = (1/6) partial_t^3 g_axis_ob(0,lambda)`.

*Proof.* Write `G(t) := partial_t g_axis_ob(t,lambda)`, which is `C^2` by Proposition 12 and even by Corollary 13, so `G'(0) = 0`.

For `t > 0`, `Phi(tau,lambda) = integral_0^1 G(ut) du` with `tau = t^2`, so `partial_tau Phi = (1/(2t)) integral_0^1 u G'(ut) du`. Since `G'(0) = 0`, the fundamental theorem of calculus gives `G'(ut) = ut integral_0^1 G''(vut) dv`. Substituting and cancelling `t` yields (i) for `tau > 0`.

*Extension to `tau = 0`.* `G'' = partial_t^3 g_axis_ob` is continuous on the compact box, so the right side of (i) is continuous in `t`, hence in `tau`, with limit `L := (1/2) integral_0^1 integral_0^1 u^2 dv du · G''(0) = (1/6) G''(0)` as `tau -> 0+`. Since `partial_tau Phi` is continuous on `(0,961/1024]` with finite limit `L`, the fundamental theorem of calculus gives `Phi(tau,lambda) - Phi(0,lambda) = integral_0^tau partial_sigma Phi(sigma,lambda) d sigma`, so the right derivative at `tau = 0` exists and equals `L`.

*Derivation of (ii).* In (i), fix `u > 0` and substitute `x = vu`, so `dv = dx/u` and `0 <= x <= u`:

```
(1/2) integral_0^1 u^2 [ (1/u) integral_0^u G''(xt) dx ] du = (1/2) integral_0^1 u integral_0^u G''(xt) dx du.
```

Interchanging the order over `{ 0 <= x <= u <= 1 }`,

```
= (1/2) integral_0^1 ( integral_x^1 u du ) G''(xt) dx = (1/4) integral_0^1 (1-x^2) G''(xt) dx.
```

Setting `t = 0` in (ii) gives `(1/4) integral_0^1 (1-x^2) dx · G''(0) = (1/6) G''(0)`, consistent with `L`. ∎

## §6 Containment and sign propagation

**Lemma 17.** For `x` in `[0,1]` and `t` in `[0,31/32]`, `x t` lies in `[0,31/32]`. Hence the right side of Lemma 16(ii) involves `partial_t^3 g_axis_ob` only at points of `[0,31/32] x [5/8,33/50]`.

*Proof.* Immediate. ∎

**Corollary 18 (sign propagation).** If `partial_t^3 g_axis_ob < 0` on `[0,31/32] x [5/8,33/50]`, then `partial_tau Phi(tau,lambda) < 0` for all `tau` in `[0,961/1024]` and `lambda` in `[5/8,33/50]`; that is, `Phi` is strictly decreasing in `tau` on `[0,961/1024]`.

*Proof.* The weight `1-x^2` in Lemma 16(ii) is nonnegative and positive on `[0,1)`; by Lemma 17 the integrand is evaluated only where the hypothesis applies. ∎
