# D-OB P1 DESIGN NOTE — TRANSVERSE KERNEL, REGULARITY, CERTIFICATION QUANTITIES

**Status**: `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`

**Base.** Branch `design/d-ob-p1`, cut from `30fbc5cff8948f9ccaed699a3f7035c5f0399c3b` (`implementation/gt-boundary-two-chart`). **Scope.** `lambda` in `[2/5, 33/50]`. This note is analytic only: no implementation, predeclare, diagnostic or certification run is part of it. Derived jointly on 2026-09-22 and checked step by step by the chat audit.

## §1 Definitions

`K = K_lambda = { x^2 + y^2 + z^2/lambda^2 <= 1 }`. Boundary points are `x(mu,phi) = (a cos phi, a sin phi, lambda mu)` with `a = sqrt(1 - mu^2)`. With `w^2 = lambda^2 (1 - mu^2) + mu^2`, so `w` in `[lambda, 1]`, the outward unit normal is `nu = (lambda a cos phi, lambda a sin phi, mu)/w` and `dA = w dmu dphi`.

For `p` in `closure(K)` and `x` in `bd K` with `x != p`:

~~~
D = |x - p|,     h = w (x - p).nu,     gamma = h/(w D),     alpha = arccos(gamma),     R = alpha/sin(alpha),
E(p) = (1/(4 pi lambda)) integral_{bd K} F dA/w,     F := h alpha^2.
~~~

Here `3 Vol(K) = 4 pi lambda` and `(x - p).nu dA = h dmu dphi`. For a meridional base point `p = (rho, 0, z)`, `h = lambda (1 - rho b) - z mu` with `b = a cos phi`. On the axis, `E(0, lambda t) = (1/2) integral_{-1}^{1} A alpha^2 dmu` with `A = 1 - t mu`, which is `E_lambda(t)` of the C system.

## §2 Interior regularity

For `p` in `int K`, `h > 0` and `gamma` in `(0, 1]` (Lemma 3.1). By Lemma 3.2, `alpha^2` and `R` are real-analytic functions of `gamma` across `gamma = 1`. The locus `gamma = 1` (`u = 1 - gamma^2 = 0`), a curve in the `(mu, phi)` parameters off the axis, is therefore not a singular set of the density, and no dedicated chart is needed there. On a compact subset of `int K`, `D` is bounded below, so derivatives of every order may be taken under the integral: `E` is `C^infinity` on `int K`. Real-analyticity of `E` is not claimed and not needed.

## §3 Directional bounds

**Lemma 3.1 (sign and size of `h`).** For `p` in `closure(K)` and `x` in `bd K`, `0 <= h(x,p) <= w(x) D`. If `p` in `int K`, then `h > 0`.

*Proof.* Upper bound: Cauchy–Schwarz, `(x-p).nu <= |x-p| |nu| = D`. Lower bound: by convexity `K` lies in the half-space `{ y : (y - x).nu(x) <= 0 }`, so `(p - x).nu <= 0`; if `p` in `int K`, a ball around `p` lies in `K`, which forces strict inequality. ∎

Consequently, for `x != p`, `gamma = h/(wD)` lies in `[0, 1]`, and in `(0, 1]` when `p` in `int K`.

**Lemma 3.2 (angle functions).** `G(gamma) := arccos^2(gamma)` and `R(gamma) := arccos(gamma)/sqrt(1 - gamma^2)`, initially defined on `(-1, 1)`, admit real-analytic extensions across `gamma = 1` to `(-1, sqrt 2)`, with `G' = -2R`. On `[0, 1]`: `0 <= G <= pi^2/4`, `1 <= R <= pi/2`, `-1 <= R_gamma <= 0`.

*Proof.* On `(-1, 1)`, `arccos` is analytic and `sqrt(1 - gamma^2) > 0`. On `(0, sqrt 2)`, `G = Phi(1 - gamma^2)` and `R = Psi(1 - gamma^2)`, where `Phi(u) = (arcsin sqrt u)^2` and `Psi(u) = arcsin(sqrt u)/sqrt u` are power series of radius 1 in `u`; the representations agree on `(0, 1)`. The bounds on `R` and `R_gamma` are Lemma A of `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA_31_32.md` (commit `f66ffe5a`, blob `5c3dfeb3`). ∎

**Lemma 3.3 (first and second `p`-derivatives).** Fix `x` in `bd K` and `p` in `closure(K)` with `x != p`. For unit vectors `v`, `v'`, with derivatives in `p`:

~~~
h_v = -w nu.v,          |h_v| <= w,          h_{vv'} = 0,
D_v = -(x - p).v / D,   |D_v| <= 1,          D_vv = (1 - D_v^2)/D in [0, 1/D],
gamma_v  = h_v/(wD) - gamma D_v/D,                                          |gamma_v|  <= 2/D,
gamma_vv = -h_v D_v/(wD^2) - gamma_v D_v/D - gamma D_vv/D + gamma D_v^2/D^2,  |gamma_vv| <= 5/D^2.
~~~

*Proof.* `h` is affine in `p` with gradient `-w nu`; `w` does not depend on `p`. Differentiating `gamma = h/(wD)` gives `gamma_v`. Differentiating again, `(h_v/(wD))_v = -h_v D_v/(wD^2)` since `h_vv = 0`, and `(gamma D_v/D)_v = gamma_v D_v/D + gamma D_vv/D - gamma D_v^2/D^2`. With `0 <= gamma <= 1`, the four terms of `gamma_vv` are bounded by `1/D^2`, `2/D^2`, `1/D^2`, `1/D^2`. ∎

**Lemma 3.4 (the density).** With `C2 := 9 pi + 8`,

~~~
|F| <= pi^2/2,      |F_v| <= pi^2/4 + 2 pi,      |F_{vv'}| <= C2/D.
~~~

*Proof.* `h <= wD <= 2` and `G <= pi^2/4` give the first bound. `F_v = h_v G - 2 h R gamma_v`, so `|F_v| <= pi^2/4 + 2 wD (pi/2)(2/D)`. For `v = v'`,

~~~
F_vv = -4 h_v R gamma_v - 2 h R_gamma gamma_v^2 - 2 h R gamma_vv,
~~~

bounded term by term, using `h <= D`, by `4 pi/D`, `8/D`, `5 pi/D`. `Q(v) = F_vv` is a quadratic form with `|Q(u)| <= C2 |u|^2/D`; for unit `v`, `v'`, `F_{vv'} = (1/4)[Q(v+v') - Q(v-v')]` and `|v+v'|^2 + |v-v'|^2 = 4`, so `|F_{vv'}| <= C2/D`. No cancellation is used. ∎

Only the second derivatives need more than a uniform bound.

## §4 Area growth and uniform integrability

The measure space is `(bd K, dA)`; the weight satisfies `1/w <= 1/lambda <= 5/2`.

**Lemma 4.1.** For every `p` in `R^3` and `s > 0`, `area(bd K ∩ B(p, s)) <= 4 pi s^2`. Also `area(bd K) <= 4 pi`.

*Proof.* If `bd K ∩ B(p, s)` is nonempty, it contains a boundary point of `K`, near which `K` has interior points inside `B(p, s)`; so `K ∩ closure(B(p, s))` is a convex body. Surface area is monotone under inclusion of convex bodies, so `area(bd(K ∩ closure(B(p,s)))) <= 4 pi s^2`, and `bd K ∩ B(p, s)` is contained in `bd(K ∩ closure(B(p, s)))`. The second claim follows from `K` contained in `closure(B(0, 1))`. ∎

**Lemma 4.2.** For every `p` in `R^3` and measurable `A` in `bd K` with `M = area(A)`,

~~~
integral_A dA(x)/|x - p|  <=  2 sqrt(4 pi M)  <=  8 pi.
~~~

*Proof.* `1/|x - p| = integral_0^infinity 1{s > |x - p|} s^{-2} ds` for `x != p`, and `{x = p}` is null. By Tonelli and Lemma 4.1 the left side is at most `integral_0^infinity min(M, 4 pi s^2) s^{-2} ds`; splitting at `s0 = sqrt(M/(4 pi))` gives `4 pi s0 + M/s0 = 2 sqrt(4 pi M)`. ∎

**Corollary 4.3.** The family `{ C2/(w D(., p)) : p in closure(K) }` is uniformly integrable on `(bd K, dA)`: for every measurable `A`, `sup_p integral_A C2/(wD) dA <= (5/2) C2 · 2 sqrt(4 pi area(A))`.

## §5 Continuous extension of the second derivatives

**Lemma V.** For a multi-index `|beta| <= 2` and `p` in `closure(K)`, put

~~~
E_beta(p) := (1/(4 pi lambda)) integral_{bd K \ {p}} partial_p^beta F(x, p) dA(x)/w(x).
~~~

Then: (a) the integral converges absolutely for every `p` in `closure(K)`; (b) `E` is `C^2` on `int K` with `partial^beta E = E_beta` there; (c) each `E_beta` is continuous on `closure(K)`.

*Proof.* (a) By Lemma 3.4 the integrand is bounded for `|beta| <= 1` and bounded by `(5/2) C2/D` for `|beta| = 2`, integrable by Lemma 4.2.

(b) Let `p` in `int K`, `r = dist(p, bd K)/2 > 0`. For `p'` in `B(p, r)`, `D(x, p') >= r` on `bd K`, so all integrands with `|beta| <= 2` are bounded on `bd K x B(p, r)`. Differentiation under the integral on a finite measure space, applied twice, gives `E` in `C^2(B(p, r))` with `partial^beta E = E_beta`.

(c) Let `p_n -> p0` in `closure(K)` and fix `x != p0`. For large `n`, `D(x, p_n) >= D(x, p0)/2 > 0`; `h`, `D` and their `p`-derivatives are continuous at `p0`; `gamma(x, p_n)` in `[0, 1]` converges to `gamma(x, p0)` in `[0, 1]`; and `G`, `R`, `R_gamma` are continuous on `[0, 1]`. Hence `partial_p^beta F(x, p_n) -> partial_p^beta F(x, p0)` for almost every `x`. The integrands are uniformly bounded for `|beta| <= 1` and uniformly integrable for `|beta| = 2` (Corollary 4.3). Vitali's theorem on `(bd K, dA)` gives `E_beta(p_n) -> E_beta(p0)`. ∎

**Remark (strict convexity is not needed).** At a boundary base point `p0`, `h(x, p0) = 0` would mean `gamma(x, p0) = 0`, inside the interval on which `G` and `R` are analytic. Part (c) uses only `gamma` in `[0, 1]`, i.e. convexity. For the ellipsoid, strict convexity also gives `h(x, p0) > 0` for `x != p0`, but the proof does not use it.

**Remark (formulation).** Lemma V states that the second derivatives of `E` on `int K` extend continuously to `closure(K)`; a Whitney-type `C^2` extension beyond `closure(K)` is not claimed.

**Remark (joint continuity in `lambda`).** Lemma V is stated for fixed `lambda`. Joint continuity in `(p, lambda)` follows by the same argument on the fixed parameter domain `(mu, phi)` with measure `dmu dphi`: the `lambda`-surface area of a parameter set `A` is `integral_A w dmu dphi <= integral_A dmu dphi`, so the bound of Lemma 4.2 is uniform, and `1/w <= 5/2` and `C2` do not depend on `lambda`.

## §6 Extension of `H` and symmetry reduction

Write `E(rho, z) := E((rho, 0, z))` and `M_lambda := { (rho, z) : rho >= 0, rho^2 + z^2/lambda^2 <= 1 }`. `E_rho`, `E_rhorho` are the directional derivatives in `p` along `e_x` at `(rho, 0, z)`, extended to `closure(K)` by Lemma V.

**Lemma 6.1.** (i) `E(-rho, z) = E(rho, z)`, and `E_rho(0, z) = 0` for `|z| <= lambda`. (ii) For `(rho, z)` in `M_lambda` with `rho > 0`, `E_rho(rho, z) = integral_0^rho E_rhorho(s, z) ds`. (iii) `H(rho, z) := integral_0^1 E_rhorho(tau rho, z) dtau` is continuous on `M_lambda`, satisfies `H = E_rho/rho` for `rho > 0`, and `H(0, z) = E_rhorho(0, z)`.

*Proof.* (i) The half-turn about the `z`-axis maps `K` to itself and `(rho, 0, z)` to `(-rho, 0, z)`; congruence invariance gives evenness, hence `E_rho(0, z) = 0` for `|z| < lambda`, and at `z = ±lambda` by continuity. (ii) If `(rho, z)` is interior, the segment `{(s, z) : 0 <= s <= rho}` is interior. If it lies on the boundary with `rho > 0`, then `|z| < lambda` and the points with `s < rho` are interior; apply the fundamental theorem on `[0, rho - eta]` and let `eta -> 0` using continuity of `E_rho`, `E_rhorho`. At the poles the segment degenerates, and `H(0, ±lambda)` is given directly by (iii). (iii) `E_rhorho` is uniformly continuous on the compact `M_lambda`. ∎

**Lemma 6.2 (equatorial reflection).** `E(rho, -z) = E(rho, z)`, and likewise for `E_rho`, `E_rhorho`, `H`. It suffices to treat `Q_lambda := { (rho, z) : rho >= 0, z >= 0, rho^2 + z^2/lambda^2 <= 1 }`.

*Proof.* `S(x, y, z) = (x, y, -z)` maps `K` to itself and `(rho, 0, z)` to `(rho, 0, -z)`, and fixes `e_x`. ∎

**Consequence.** An interior stationary point with `rho > 0` has `E_rho = 0`, hence `H = 0`. Thus `H != 0` on `{ (rho, z) in int Q_lambda : rho > 0 }` excludes off-axis stationary points, up to the reflections.

## §7 Specialization at the pole and control against the C system

On the axis, `h = lambda A` with `z = lambda t`, and

~~~
g_axis(t, lambda) = lambda E_z(0, lambda t),        partial_t g_axis(t, lambda) = lambda^2 E_zz(0, lambda t).
~~~

With `mu = 1 - s^2`, the Lemma V integrands at `(0, 0, lambda t)` become `s partial_t (A alpha^2)` and `s partial_t^2 (A alpha^2)`, i.e. `F_t` and `G_t` of the C1 and C2 lemmas. At the pole `p+ = (0, 0, lambda)`: `h = lambda s^2`, `D = s sqrt(qhat)`, `gamma = lambda s/(w sqrt(qhat))`, so the integrands are the pointwise values of `F_t`, `G_t` at `t = 1` for `s > 0`, namely `F_ob` and `G_boundary`. Lemma V (c) along the axis gives

~~~
lim_{t->1-} g_axis(t, lambda)          = integral_0^{sqrt 2} F_ob(s, lambda) ds,
lim_{t->1-} partial_t g_axis(t, lambda) = integral_0^{sqrt 2} G_boundary(s, lambda) ds,
~~~

and the mean-value theorem gives the one-sided derivative at `t = 1`. These are Lemma 5 of `analysis/OBLATE_ENDPOINT_C1_LEMMA.md` (commit `aefa8ed2`) and the Proposition of §6 of the band C2 lemma (commit `f66ffe5a`).

**What the control checks.** The endpoint kernels coincide by construction: both are pointwise values at the pole. The independent content is the justification of the limit: the C lemmas use axis-specific substitutions and explicit majorants; Lemma V uses `h <= wD`, `|partial_p^2 F| <= C2/D` and convex area growth.

## §8 Certification design

**8.1 Integration dimension.** Off the symmetry axis, `h = H0 - H1 cos phi` and `D^2 = D0 - D1 cos phi` with `H0 = lambda - z mu`, `H1 = lambda rho a`, `D0 = a^2 + rho^2 + (lambda mu - z)^2`, `D1 = 2 rho a`, so the azimuthal dependence enters through an inverse-trigonometric function composed with an algebraic function of `cos phi`. No reduction eliminating the azimuthal integration is used; the certification kernels are two-dimensional `(mu, phi)`-integrals. On the axis, rotational symmetry removes the `phi`-dependence and recovers the one-dimensional C kernel. Nonexistence of a closed form is not claimed.

**8.2 Certification quantities.** Two candidates, both two-dimensional:

~~~
E_rhorho(rho, z) = (1/(4 pi lambda)) integral integral F_rhorho dphi dmu,
H(rho, z)        = (1/(4 pi lambda)) integral integral K_H dphi dmu,
K_H(rho, z; mu, phi) := [ F_rho(rho, b) - F_rho(-rho, b) ] / (2 rho)   (rho > 0),
K_H(0, z; mu, phi)   := F_rhorho(0, b),
~~~

where `F_rho(-rho, b)` is taken at the mirror base point `(-rho, 0, z)` in `closure(K)`. Properties: (i) since `E_rho` is odd in `rho`, `(1/(4 pi lambda)) integral integral K_H = [E_rho(rho, z) - E_rho(-rho, z)]/(2 rho) = H(rho, z)`; (ii) `K_H(rho) = (1/(2 rho)) integral_{-rho}^{rho} F_rhorho(s, b) ds`; (iii) with `p_s = (s, 0, z)`, Tonelli and Lemma 4.2 give `integral_A |K_H| dA <= C2 · 2 sqrt(4 pi area(A))` uniformly in `rho`, including `rho -> 0`; (iv) for a cell with `0 <= rho <= rho_hi`, `K_H` lies in the hull of `F_rhorho` over `s` in `[-rho_hi, rho_hi]`, so evaluating `F_rhorho` with the `rho`-argument `[-rho_hi, rho_hi]` is a valid enclosure, and the `1/rho` cancellation of the difference quotient produces no singularity in the enclosure. Whether the resulting widths are practical is an implementation question, not claimed here.

**8.3 Boundary cells.** For a base point near `bd K`, the contribution of a neighbourhood `A` of the point of `bd K` nearest to it is bounded by Lemma 4.2, `(5/2) C2 · 2 sqrt(4 pi area(A))`, without curvature bounds or normal coordinates.

**8.4 Diagnostic rule.** A `DIAGNOSTIC_ONLY` run, kept outside the repository, may answer only two binary questions declared in advance: (1) does `H` have a uniform sign on `Q_lambda`; (2) does `E_rhorho` have a uniform sign on `Q_lambda`. The sampling rule is fixed before any result is seen, and only the two binaries are recorded. No value, margin, worst point, observed sign-change location, subdivision count, precision, chart threshold or other parameter from the diagnostic may be used in any predeclare or certification choice. A diagnostic answers plausibility on finitely many points and is not a proof. Outcome use: if (2) holds, a single `E_rhorho` design; if only (1) holds, `H` via `K_H`; if neither holds, any partition is derived analytically (the axis relation `H(0, z) = E_rhorho(0, z)` with the C results, boundary asymptotics, and the structure of the kernels), never from diagnostic values.

**8.5 Not claimed.** Regularity of order three up to the boundary (cancellation not examined); a Whitney extension; real-analyticity of `E`; practical interval widths; any sign of `H` or `E_rhorho`.

## §9 Status of the P1 design conditions

- Quarter-domain reduction by `rho -> -rho` and `z -> -z`: closed (Lemmas 6.1 (i), 6.2).
- Joint `C^2` regularity near the axis, proved with the kernel: closed, in the stronger form of Lemma V on all of `closure(K)`.
- Removability at `u = 0`: closed; not a singular set (Lemma 3.2, §2).
- Extension of `H` to `rho = 0` and connection to the C system: closed (Lemma 6.1 (iii), §7).
- Integration dimension: decided, two-dimensional `(mu, phi)` (§8.1), with kernels fixed (§8.2).
- Diagnostic before predeclare: rule fixed (§8.4); not yet run.
