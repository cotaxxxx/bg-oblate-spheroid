# MONOTONE-TUBE C2 INTERCHANGE LEMMA — BAND [31/32, 1]

**Status**: `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`

**Purpose.** To justify, for `t` in `[31/32, 1)` and `lambda` in `[5/8, 33/50]`,

~~~
partial_t g_axis_ob(t,lambda) = integral_0^{sqrt 2} G_t(s,t,lambda) ds,
~~~

and the one-sided endpoint derivative `partial_t g_axis_ob(1-,lambda) = integral_0^{sqrt 2} G_boundary(s,lambda) ds`. This supplies the analytic identification of the machine-enclosed second-`t` density with `partial_t g_axis_ob` on the whole band, both the lower slab `[31/32, 63/64]` and the upper tube `[63/64, 1]`. It asserts no sign.

**Premises.** The oblate endpoint C1 lemma, `analysis/OBLATE_ENDPOINT_C1_LEMMA.md`, commit `aefa8ed24f257694d5b1e349ef7478b9c1e5b807`, blob `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6`, with `I = [5/8, 33/50]`: its Lemma 1 (`N = -s^2 H`, `q > 0`, `0 < gamma <= 1`), Lemma 2 (bound on `H`), Lemma 3 (`g_axis_ob = integral F_t ds` on `[1/2,1)`), and Lemma 5 (continuity of `g_axis_ob` on `[1/2,1]` with `g_axis_ob(1,lambda) = B_ob(lambda)`).

Throughout, `lambda_- = 5/8`, `lambda_+ = 33/50`, `delta = 1 - t` in `(0, 1/32]`.

## §1 Pre-limit kernel

With the definitions of §1 of the C1 lemma,

~~~
F_t = s [ -mu alpha^2 - 2 A R gamma_t ],   gamma_t = lambda N / (w q^{3/2}),   N = -s^2 H,
H = (1 - s^2)(2 - s^2) + lambda^2 (2 s^2 - 2 delta - s^4 + delta s^2),
~~~

and `g_axis_ob(t,lambda) = integral_0^{sqrt 2} F_t ds` for `t` in `[31/32,1)` by Lemma 3 of the C1 lemma.

## §2 Formal second-t derivative

For `t < 1`,

~~~
R_gamma  = (gamma R - 1)/(1 - gamma^2),       N_t = -lambda^2 s^2 (2 - s^2),
gamma_tt = lambda^3 s^2 [ 3 d H - (2 - s^2) q ] / (w q^{5/2}),
G_t := partial_t F_t = s [ 4 mu R gamma_t - 2 A ( R_gamma gamma_t^2 + R gamma_tt ) ].
~~~

The coefficient `4 mu` is the sum of the two contributions `2 mu R gamma_t` from `-mu alpha^2` (using `(alpha^2)_t = -2 R gamma_t`) and from `-2 A R gamma_t` (using `A_t = -mu`). Across the locus `gamma = 1`, `R = Psi(u)` and `R_gamma = -2 gamma Psi'(u)` with `u = 1 - gamma^2` are the continuous extensions.

## §3 Corner-scaled identity

For `q > 0` put `rho = s/sqrt q`, `phi = d/sqrt q`, `Ahat = A/sqrt q`. Then exactly

~~~
rho^2 (2 - s^2) + lambda^2 phi^2 = 1,       Ahat = (2 - s^2) s rho - (1 - s^2) phi,
~~~

and `G_t = T1 + T2 + T3` with

~~~
T1 = -4 (1 - s^2) R lambda rho^3 H / w,
T2 = -2 R_gamma lambda^2 H^2 Ahat rho^5 / w^2,
T3 = -2 R lambda^3 Ahat rho^3 [ 3 phi H - (2 - s^2) sqrt q ] / w,
~~~

in which no negative power of `q` appears.

## §4 North half s in [0,1]

**Lemma A (angle factors).** For `gamma` in `[0,1]`: `1 <= R <= pi/2` and `-1 <= R_gamma <= 0`.

*Proof.* With `gamma = cos(alpha)`, `alpha` in `[0, pi/2]`, `R = alpha/sin(alpha)` increases from `1` to `pi/2`. Also `R_gamma = (alpha cos(alpha) - sin(alpha))/sin^3(alpha)`, with limit `-1/3` at `alpha = 0`. The numerator is `<= 0` because `tan(alpha) >= alpha`. The bound `R_gamma >= -1` is equivalent to `f(alpha) = sin^3(alpha) - sin(alpha) + alpha cos(alpha) >= 0`. Here `f(0) = f(pi/2) = 0` and `f'(alpha) = sin(alpha) [ (3/2) sin(2 alpha) - alpha ]`; the bracket is concave on `[0, pi/2]`, positive near `0` and negative at `pi/2`, so it has exactly one zero there, and `f` increases then decreases. Hence `f >= 0`. ∎

**Lemma B (north majorant).** On `s` in `[0,1]`, `t` in `[31/32,1)`, `lambda` in `[5/8,33/50]`, `|G_t| <= M_N` for the constant

~~~
M_N = 4 (pi/2) lambda_+ 4 / lambda_-
    + 2 lambda_+^2 16 (2 + 1/lambda_-) / lambda_-^2
    + 2 (pi/2) lambda_+^3 (2 + 1/lambda_-) [ 12/lambda_- + 2 sqrt 2 ] / lambda_-.
~~~

*Proof.* On `[0,1]`, `2 - s^2 >= 1`, so the first identity of §3 gives `0 <= rho <= 1` and `|phi| <= 1/lambda_-`, and the second gives `|Ahat| <= 2 + 1/lambda_-`. Also `w >= lambda_-`, `|H| < 4` (Lemma 2 of the C1 lemma, valid for `delta <= 1/2`), Lemma A for `R` and `R_gamma`, and `q <= 2`, so `sqrt q <= sqrt 2`. Substituting into `T1`, `T2`, `T3` gives the three terms of `M_N`. None of these bounds depends on `t`. ∎

## §5 South half s in [1, sqrt 2]

**Lemma C (south majorant).** On `s` in `[1, sqrt 2]`, `t` in `[31/32,1]`, `lambda` in `[5/8,33/50]`, `|G_t|` is bounded by a constant `M_S`.

*Proof.* Here `d = s^2 - delta >= 1 - 1/32 = 31/32`, so `q >= lambda_-^2 (31/32)^2 > 0`. Also `A = delta + (1-delta) s^2 >= 31/32`, `w <= 1` and `q <= 1 + 4 lambda_+^2`, so `gamma^2 = lambda^2 A^2 / (w^2 q) >= lambda_-^2 (31/32)^2 / (1 + 4 lambda_+^2) > 0`, and `u = 1 - gamma^2` is bounded away from `1`. Hence `R = Psi(u)` and `R_gamma = -2 gamma Psi'(u)` are continuous on this compact set, including the internal locus `gamma = 1`, and so are all other factors of `G_t` in §2. A continuous function on a compact set is bounded. ∎

## §6 Differentiation under the integral and endpoint extension

**Proposition.** For `lambda` in `[5/8,33/50]`:

~~~
partial_t g_axis_ob(t,lambda) = integral_0^{sqrt 2} G_t(s,t,lambda) ds          for t in [31/32, 1),
partial_t g_axis_ob(1-,lambda) = integral_0^{sqrt 2} G_boundary(s,lambda) ds,
~~~

where `G_boundary(s,lambda) = lim_{t->1-} G_t(s,t,lambda)` for `s > 0`.

*Proof.* By §1, `g_axis_ob = integral F_t ds` on `[31/32,1)`. For fixed `s > 0`, `F_t` is `C^1` in `t` on `[31/32,1)` with derivative `G_t`, by the same smoothness argument as Lemma 3 of the C1 lemma. Lemmas B and C give the integrable, `t`-independent majorant `max(M_N, M_S)`; dominated differentiation gives the first identity.

For fixed `s > 0`, as `t -> 1-`, `q -> s^2 qhat > 0`, so `rho`, `phi`, `Ahat`, `H`, `w` converge, and `R`, `R_gamma` converge by continuity in `gamma`; hence `G_t -> G_boundary` pointwise. The same majorant and dominated convergence give `lim_{t->1-} partial_t g_axis_ob(t,lambda) = integral G_boundary ds`. By Lemma 5 of the C1 lemma, `g_axis_ob(·,lambda)` is continuous at `t = 1` with value `B_ob(lambda)`; the fundamental theorem of calculus on `[t,1)` then gives the one-sided derivative at `t = 1` equal to this limit. ∎

## §7 Scope and audit items

Analytic bridge only; the sign of no integral is asserted. The five audit items listed in §7 of blob `7cb9b809` now stand as follows: (1) the formal second derivative and (2) the scaled identities `T1`–`T3` were re-derived by the chat audit on 2026-09-21; (3) the bounds on `R` and `R_gamma` are proved in Lemma A; (4) the C1 premises are pinned to Lemmas 1, 2, 3 and 5 of the C1 lemma above; (5) for the upper tube, the refinement producer `c2fee400` and checker `fd778d6d` are recorded as chat raw-audited (`analysis/MONOTONE_TUBE_REFINEMENT_RAW_AUDIT.md`, blob `c3b3666d`); for the lower slab, the producer `e927cda5` and checker `3d38a16e` remain to be raw-audited against the `G_t` of §2–§3. On the slab `t <= 63/64`, `q >= lambda_-^2 (1/64)^2 > 0` at `s = 0`, so no corner representation is required there.

## Provenance (non-normative)

Derived from `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md`, blob `7cb9b8091596510203d74e09387bc1e8188b8b47`, scope `[63/64, 1]`, which is not modified. Changes: (1) scope extended to `[31/32, 1]`, the south-half constant becoming `d >= 31/32`; (2) premises pinned to the oblate endpoint C1 lemma instead of an unnamed earlier argument; (3) proof of `-1 <= R_gamma <= 0` added; (4) explicit lower bound on `gamma` in the south half, justifying the `Psi`/`Psi'` extensions there; (5) statement that the north-half bounds are independent of `t`.
