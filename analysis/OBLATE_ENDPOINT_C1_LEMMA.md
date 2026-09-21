# OBLATE ENDPOINT C1 LEMMA — PRE-LIMIT REPRESENTATION AND ONE-SIDED LIMIT

**Status**: `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`

**Scope.** `t` in `[1/2, 1)` and `lambda` in `I = [lambda_-, lambda_+]` with `0 < lambda_- <= lambda_+ < 1/sqrt 2`. For the band, `I = [5/8, 33/50]`.

**Claims.** (a) `g_axis_ob(t,lambda) = partial_t E_lambda(t) = integral_0^{sqrt 2} F_t ds` on the scope (Lemma 3). (b) The one-sided limit `B_ob(lambda) = lim_{t->1-} g_axis_ob(t,lambda)` exists and equals `integral_0^{sqrt 2} F_ob ds` (Lemma 5). (c) `F_ob` is real-analytic on two charts, and `B'_ob = integral_0^{sqrt 2} partial_lambda F_ob ds` (Lemmas 4, 6).

**Dependency order.** §1 → §2 → §3 → §4 → §5 → §6. Each lemma uses only earlier ones; §4 does not use §2–§3.

## §1 Definitions

For `K_lambda = { x^2 + y^2 + z^2/lambda^2 <= 1 }` and `p(t) = (0,0,lambda t)`, with `mu` in `[-1,1]`:

~~~
A = 1 - t mu,   q = 1 - mu^2 + lambda^2 (mu - t)^2,   w^2 = lambda^2 (1 - mu^2) + mu^2,
gamma = lambda A / (w sqrt q),   alpha = arccos(gamma),   R = alpha / sin(alpha),
E_lambda(t) = (1/2) integral_{-1}^{1} A alpha^2 d mu.
~~~

The normalisation `3 Vol(K_lambda) = 4 pi lambda` gives the factor `1/2`; the derivation is §3.1 of the C1d analytic lemma. With `mu = 1 - s^2`, `delta = 1 - t`, `d = t - mu = s^2 - delta`, `x = s^2`:

~~~
A = delta + (1 - delta) s^2,   q = s^2 (2 - s^2) + lambda^2 d^2,
E_lambda(t) = integral_0^{sqrt 2} F ds,   F = s A alpha^2,
F_t = s [ -mu alpha^2 - 2 A R gamma_t ],   gamma_t = lambda N / (w q^{3/2}),   N = -mu q - lambda^2 A d.
~~~

## §2 Pre-limit bounds

**Lemma 1.** For `t < 1`: (i) `N = -s^2 H` with `H = (1-x)(2-x) + lambda^2 (2-x)(x-delta)`; (ii) `q > 0` on `[0, sqrt 2]`; (iii) `0 < gamma <= 1`.

*Proof.* (i) `mu d + A = x(2-x)`, so `mu d^2 + A d = d x (2-x)` and `N = -x(2-x)(mu + lambda^2 d)`; expanding `(2-x)(mu + lambda^2 d)` gives `H`. (ii) For `0 < s < sqrt 2` the first term of `q` is positive; `q = lambda^2 delta^2 > 0` at `s = 0` and `q = lambda^2 (2-delta)^2 > 0` at `s = sqrt 2`. (iii) `A = delta + (1-delta) s^2 > 0` gives `gamma > 0`; the identity `1 - gamma^2 = (1-mu^2)((1-lambda^2) mu + lambda^2 t)^2 / (w^2 q) >= 0` gives `gamma <= 1`. ∎

**Lemma 2 (uniform majorant).** For `t` in `[1/2,1)`, `lambda` in `I`, `s` in `[0, sqrt 2]`: `|F| <= (pi^2/2) s`, and `|F_t| <= M(s)` with

~~~
M(s) = (pi^2/4) s + pi s (lambda_+/lambda_-) * 4 * ( 2/(3 sqrt 3 lambda_-) + 2 s )   on [0,1],
M(s) = (pi^2/4) s + pi s * 32 lambda_+ / lambda_-^4                                 on [1, sqrt 2].
~~~

*Proof.* By Lemma 1(iii), `alpha` in `[0, pi/2]`, so `alpha^2 <= pi^2/4` and `1 <= R <= pi/2`; with `A <= 2` this gives the bound on `F`, and `|F_t| <= s (pi^2/4 + pi |A gamma_t|)` with `|A gamma_t| = lambda A s^2 |H| / (w q^{3/2})` and `w >= lambda_-`.

On `[0,1]`: `|(1-x)(2-x)| <= 2` and `|(2-x)(x-delta)| <= 2`, so `|H| <= 2 + 2 lambda_+^2 < 4`. Also `q >= s^2 + lambda_-^2 d^2` (as `2 - s^2 >= 1`) and `A <= delta + s^2 <= |d| + 2 s^2`. For `s > 0` put `z = lambda_- |d| / s`; then `s^2 |d| / (s^2 + lambda_-^2 d^2)^{3/2} = z / (lambda_- (1+z^2)^{3/2}) <= 2/(3 sqrt 3 lambda_-)`, the maximum of `z/(1+z^2)^{3/2}` being at `z = 1/sqrt 2`; and `2 s^4 / (s^2 + lambda_-^2 d^2)^{3/2} <= 2 s`.

On `[1, sqrt 2]`: `d >= 1 - delta >= 1/2`, so `q >= lambda_-^2 / 4`; `|(1-x)(2-x)| <= 1/4` and `0 <= (2-x)(x-delta) <= (2-x) x <= 1`, so `|H| <= 1/4 + lambda_+^2 < 1`; with `A <= 2`, `s^2 <= 2`, `q^{3/2} >= lambda_-^3/8`, `|A gamma_t| <= 32 lambda_+ / lambda_-^4`. ∎

## §3 Pre-limit representation

**Lemma 3.** For `t` in `[1/2,1)` and `lambda` in `I`, `g_axis_ob(t,lambda) = partial_t E_lambda(t) = integral_0^{sqrt 2} F_t ds`.

*Proof.* Fix `s` in `(0, sqrt 2]`; the single point `s = 0` is null. `A` and `q` are polynomials in `t`, `q > 0` and `w > 0` (Lemma 1), so `gamma` is `C^infinity` in `t`. Write `alpha^2 = Phi(1 - gamma^2)` with `Phi(u) = (arcsin sqrt u)^2`, real-analytic on `[0,1)` by its power series; since `gamma > 0`, `1 - gamma^2 < 1`, so `alpha^2` is `C^infinity` in `t`, including across the locus `gamma = 1`. Its derivative is `-2 R gamma_t`: directly where `gamma < 1`. For fixed `s` in `(0, sqrt 2)`, the set of `t` with `gamma = 1` is at most the single zero of the linear function `(1-lambda^2) mu + lambda^2 t`, where the identity extends by continuity of both sides; at `s = sqrt 2`, `1 - mu^2 = 0` gives `gamma = 1` for every `t`, and both sides vanish identically. Hence `partial_t F = F_t`. By Lemma 2, `|F|` and `|F_t|` are bounded by integrable functions independent of `t`; dominated differentiation gives the claim. ∎

*Remark.* The source asserted this differentiation for all `t < 1` without proof. It is proved here on `[1/2,1)` only, which contains the band `[31/32,1)`.

## §4 Endpoint kernel and two charts

At `t = 1` (`delta = 0`) and `s > 0`, with `a = 1 - lambda^2`:

~~~
A = s^2,   d = s^2,   q = s^2 qhat,   qhat = 2 - a s^2,   w^2 = 1 - 2 a s^2 + a s^4,
(1 - s^2) qhat + lambda^2 s^2 = (2 - s^2)(1 - a s^2),
A gamma_t = - lambda s (2 - s^2)(1 - a s^2) / (w qhat^{3/2}),   gamma = lambda s / (w sqrt qhat),
w^2 qhat - lambda^2 s^2 = (2 - s^2)(1 - a s^2)^2,   u := 1 - gamma^2 = (2 - s^2)(1 - a s^2)^2 / (w^2 qhat).
~~~

Also `w^2 >= lambda^2` and `qhat >= 2 lambda^2`. Define, with `Phi(u) = (arcsin sqrt u)^2` and `Psi(u) = arcsin(sqrt u)/sqrt u`,

~~~
F_ob(s,lambda) = -s (1 - s^2) Phi(u) + 2 lambda s^2 (2 - s^2)(1 - a s^2) Psi(u) / (w qhat^{3/2}).
~~~

This is `s[-mu alpha^2 - 2 R A gamma_t]` at `t = 1`, since on the branch `gamma >= 0`, `alpha = arcsin sqrt u` and `R = Psi(u)`.

**Lemma 4 (two charts).** Let `J` be open with `I ⋐ J ⋐ (0, 1/sqrt 2)` and `lambda_J = inf J > 0`.

(i) On `[0,1] x closure(J)`: `gamma^2 <= 1/(1+lambda^2) <= 1/(1+lambda_J^2) < 1`.

(ii) On `[1, sqrt 2] x closure(J)`: `u <= 1 - lambda^2/2 <= 1 - lambda_J^2/2 < 1`.

(iii) `F_ob` and `partial_lambda F_ob` are continuous and bounded on `[0, sqrt 2] x closure(J)`.

*Proof.* (i) With `e = s^2` in `(0,1]`, `u/gamma^2 = h(e)/lambda^2` where `h(e) = (2-e)(1-a e)^2/e`. Differentiating, the numerator of `h'(e)` is `-(1 - a e)[2 + 2 a e (1-e)]`, negative since `1 - a e > 0` and `a` in `(0,1)`. So `h(e) >= h(1) = lambda^4`, hence `u >= lambda^2 gamma^2`, and `gamma^2 + u = 1` gives `gamma^2 <= 1/(1+lambda^2)`. At `s = 0`, `gamma = 0`.

(ii) `w^2 = 1 - a s^2 (2 - s^2) <= 1`, `qhat <= 2`, `s^2 >= 1`, so `gamma^2 >= lambda^2/2`.

(iii) On `[0,1]`, write `alpha = arccos(gamma)` with `gamma` in `[0, (1+lambda_J^2)^{-1/2}]`, where `arccos` and `alpha/sin(alpha)` are analytic. On `[1, sqrt 2]`, `Phi` and `Psi` are analytic on `[0, 1 - lambda_J^2/2]`; the internal double zero of `u` at `s_0^2 = 1/(1-lambda^2)` in `(1,2)` lies in this chart. Both chart expressions are real-analytic in `(s,lambda)` on their closed rectangles, with positive denominators by the lower bounds on `w^2` and `qhat`, and they coincide on `s = 1`, where `gamma^2 = 1/(1+lambda^2)` and `u = lambda^2/(1+lambda^2)`. Continuous functions on compact sets are bounded. ∎

## §5 One-sided limit

**Lemma 5.** For `lambda` in `I`, `lim_{t->1-} g_axis_ob(t,lambda)` exists and equals `integral_0^{sqrt 2} F_ob(s,lambda) ds`. Defining `B_ob(lambda)` as this limit and `g_axis_ob(1,lambda) := B_ob(lambda)`, the function `g_axis_ob(·,lambda)` is continuous on `[1/2,1]`.

*Proof.* By Lemma 3, `g_axis_ob(t,lambda) = integral F_t ds` for `t < 1`. Fix `s` in `(0, sqrt 2]`. As `t -> 1-`, `A -> s^2` and `q -> s^2 qhat > 0` with `w` independent of `t`, so `gamma`, `gamma_t`, and `A gamma_t` converge to their §4 values; `gamma > 0` throughout, so `u < 1`, and `alpha^2 = Phi(u)`, `R = Psi(u)` converge by continuity of `Phi` and `Psi` on `[0,1)`. Thus `F_t -> F_ob` pointwise on `(0, sqrt 2]`. Lemma 2 gives the integrable majorant `M`, independent of `t`; dominated convergence gives the limit. ∎

## §6 Derivative in lambda

**Lemma 6.** `B_ob` is `C^1` on `I`, and `B'_ob(lambda) = integral_0^{sqrt 2} partial_lambda F_ob(s,lambda) ds`.

*Proof.* By Lemma 4(iii), `partial_lambda F_ob` is continuous and bounded on `[0, sqrt 2] x closure(J)`, and `I` lies in the interior of `J`. Dominated differentiation applies at every point of `I`, endpoints included. ∎

## §7 Consequences and scope

Lemmas 5 and 6 are condition (i) recorded in the `B_ob` endpoint receipt: the endpoint-regular two-chart kernel is the analytic representation of `B_ob`, and differentiation under the integral is valid. Lemma 3 and the continuity in Lemma 5 are the premises invoked in §1 and §6 of the monotone-tube C2 interchange lemma (blob `7cb9b809`).

Not claimed: the sign of any integral; the identification of the zero of `B_ob` with the boundary passage of the interior axial branch (condition (ii) of the receipt); any statement for `t < 1/2` or `lambda` outside `I`.

## Provenance (non-normative)

Transcribed and completed from `analysis/endpoint_kernel_lemma.md`, blob `aa6a1a1710d1a4af560e5ddf0c504870f50c535c`, branch `analytic-endpoint-limit-78c178f` (evidence `DIAGNOSTIC_ONLY / NOT_BINDING`, derivation `PROTOTYPE / NOT_AUDITED`). Changes: (1) Lemma 3 added with proof, restricted to `[1/2,1)`; (2) proof of the gamma-chart bound added; (3) explicit constant for the south half of Lemma 2, where the source stated only a compact-set bound; (4) plain-text notation replacing corrupted markup; (5) omitted as outside the proof chain: the exact algebra controls (`controls/test_endpoint_algebra.py`), the later certification target, and the static normalisation `P = B^3`. The earlier version on the working branch (blob `d0d3c45c`) is superseded as analytic reference by this artifact. Neither earlier file is modified.
