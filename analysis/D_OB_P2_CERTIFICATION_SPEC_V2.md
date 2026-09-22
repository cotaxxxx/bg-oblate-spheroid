# D-OB P2 CERTIFICATION SPECIFICATION V2 — H > 0 ON THE QUARTER MERIDIONAL DOMAIN

**Status**: `SEALED / NOT_RUN / NOT_BINDING`

**Base.** Branch `design/d-ob-p2`, cut from `eff18894e414c1edcf783fbb2346027506d95d0e`. Analytic basis: `analysis/D_OB_P1_DESIGN_NOTE.md` (commit `6c6282a8`, blob `f81e120e`), cited below as P1. Strategy selection: `analysis/D_OB_P1_DIAGNOSTIC_RESULT.md` (commit `eff18894`, blob `56fa9b4e`). No value from the P1 diagnostic is used anywhere in this specification.

**Supersedes.** SPEC V1 (`analysis/D_OB_P2_CERTIFICATION_SPEC_V1.md`, commit `4513b420`, SHA-256 `93dd6d12b8ab29191bd4b878ab99b84de3ff015179941689fc851f81cca9c8c3`), before any run. The chat audit of the first producer draft found that, under V1, a far-column cell that passes both ball tests but whose evaluation fails was covered by neither `L` nor `B_cut`. V2 adds such cells to `A_p` (§3, §5) and fixes the comparison used to rank regular cells (§6). No run under V1 took place and no acceptance outcome informed this change.

## §0 Claim

For every `(r, tau, lambda)` in `P := [0, 1] x [0, 1] x [2/5, 33/50]`,

~~~
H(rho, z; lambda) > 0,     rho = r (1 - tau^2)/(1 + tau^2),     z = lambda r · 2 tau/(1 + tau^2).
~~~

Since `rho^2 + z^2/lambda^2 = r^2`, the map `(r, tau) -> (rho, z)` sends `[0,1]^2` onto `Q_lambda` for each `lambda`; `tau = 0` is the equator, `tau = 1` the axis, `r = 1` the boundary. With P1 Lemmas 6.1–6.2 the claim excludes interior stationary points of `E` with `rho > 0`, for every `lambda` in `[2/5, 33/50]`.

## §1 Quantity certified

`H = I/(4 pi lambda)` with `I(rho, z; lambda) := integral_{-1}^{1} integral_{0}^{2 pi} K_H dphi dmu` and `K_H` as in P1 §8.2. Since `lambda > 0`, `H > 0` is equivalent to `I > 0`. The integrand is even in `phi` (the base point lies in the plane `y = 0`), so `I = 2 J` with `J := integral_{-1}^{1} integral_{0}^{pi} K_H dphi dmu`. **The certified inequality is `J > 0`.**

## §2 Parameter boxes and columns

A parameter box is `B = [r_lo, r_hi] x [tau_lo, tau_hi] x [lambda_lo, lambda_hi]` with rational endpoints and positive width in each coordinate. Put

~~~
rho_lo = r_lo (1 - tau_hi^2)/(1 + tau_hi^2),         rho_hi = r_hi (1 - tau_lo^2)/(1 + tau_lo^2),
z_lo   = lambda_lo r_lo · 2 tau_lo/(1 + tau_lo^2),    z_hi   = lambda_hi r_hi · 2 tau_hi/(1 + tau_hi^2),
rho_0 := 1/8.
~~~

These are exact rationals, and every base point of `B` satisfies `rho_lo <= rho <= rho_hi`, `z_lo <= z <= z_hi` (monotonicity of `(1 - tau^2)/(1 + tau^2)` and `2 tau/(1 + tau^2)` on `[0, 1]`).

- **Far column**: `rho_lo >= rho_0`. `K_H` is evaluated as the difference quotient `[F_rho(rho, b) - F_rho(-rho, b)]/(2 rho)`.
- **Near column**: otherwise, if `rho_hi <= 2 rho_0`. `K_H` is enclosed by `F_rhorho` evaluated with the `rho`-argument `S(B) := [-rho_hi, rho_hi]` (P1 §8.2 (iv)).
- **Straddle**: neither holds. The box is subdivided (§6) and never evaluated.

A straddle box has `rho_hi - rho_lo > rho_0`, so every box whose `rho`-range is narrower than `rho_0` is far or near. `rho_0` is a design constant: it keeps `1/rho_lo <= 8` in the far column and `S(B)` within `[-1/4, 1/4]` in the near column. It is not derived from the diagnostic.

## §3 Base-point balls and cell classification

**Rounding rule.** For a positive rational `R2`, `round_up(R2) := k/2^32`, where `k` is the least integer with `k^2 >= R2 · 2^64`, computed in exact integer arithmetic. A box with `R2 = 0` is invalid and fails closed.

- **Far column.** `c = (rho_c, 0, z_c)` with `rho_c = (rho_lo + rho_hi)/2`, `z_c = (z_lo + z_hi)/2`; `R2 = ((rho_hi - rho_lo)/2)^2 + ((z_hi - z_lo)/2)^2`; `R = round_up(R2)`; mirror centre `cbar = (-rho_c, 0, z_c)`.
- **Near column.** `c = (0, 0, z_c)` with `z_c = (z_lo + z_hi)/2`; `R2 = rho_hi^2 + ((z_hi - z_lo)/2)^2`; `R = round_up(R2)`.

Then `|p - c| <= R` for every base point `p` of `B` (far), and for every `p_s = (s, 0, z)` with `s` in `S(B)` and `z` in `[z_lo, z_hi]` (near).

`J` is computed on the parameter rectangle `[-1, 1] x [0, pi]`, partitioned into cells `C = [mu_lo, mu_hi] x [phi_lo, phi_hi]` with rational `mu`-endpoints and `phi`-endpoints equal to `pi` times a rational. `|C| := (mu_hi - mu_lo)(phi_hi - phi_lo)`. The cell order is lexicographic in `(mu_lo, phi_lo)`. `x(mu, phi; lambda) = (a cos phi, a sin phi, lambda mu)` with `a = sqrt(1 - mu^2)`.

A cell is **regular** if an interval evaluation over `C x [lambda_lo, lambda_hi]` proves `|x - c| >= 2R` (far column: and also `|x - cbar| >= 2R`). Every other cell is **cut**. In the far column, `A_p` is the set of cut cells failing the test for `c`, together with every cell treated as cut because its evaluation failed (§5); `A_pbar` is the set of cut cells failing the test for `cbar`; a cut cell may lie in both. On every regular cell and for every base point of `B` (far: and its mirror; near: every `p_s`), `D >= 2R - R = R > 0`.

## §4 Regular lower bound, cut bound, acceptance

**Regular part.** For each regular cell, an interval enclosure `K(C, B)` of `K_H` over `C x B`, in the form of §2 for the column, gives `integral_C K_H dmu dphi >= |C| · lower(K(C, B))` at every parameter point of `B`. `L(B) := sum over regular cells of |C| · lower(K(C, B))`. The regular cells are exactly the complement of the union of the cut cells.

**Cut part.** With `C1 := pi^2/4 + 2 pi` and `C2 := 9 pi + 8` (P1 Lemma 3.4):

~~~
far:   B_cut(B) := (C1 / rho_lo) · ( sum_{C in A_p} |C|  +  sum_{C in A_pbar} |C| )
near:  B_cut(B) := (2 C2 / lambda_lo) · sqrt( 4 pi · sum_{C cut} |C| )
~~~

*Far.* `|F_rho| <= C1` everywhere (P1 Lemma 3.4), so `|K_H| <= C1/rho_lo` on every cut cell; the two sums are always added, so a cell in both sets is counted twice, which keeps an upper bound. *Near.* `integral_A |K_H| dmu dphi = integral_A |K_H| dA/w <= (1/lambda_lo) integral_A |K_H| dA <= (1/lambda_lo) · C2 · 2 sqrt(4 pi · area(A))` by P1 §8.2 (iii), and `area(A) = sum_{C cut} integral_C w dmu dphi <= sum_{C cut} |C|` since `w <= 1`.

**Acceptance.** `B` is accepted iff `L(B) - B_cut(B) > 0`, evaluated as an interval whose lower endpoint is positive. Then `J > 0` at every parameter point of `B`.

## §5 Enclosure requirements

- `gamma` is intersected with `[0, 1]`; valid because every true base point lies in `closure(K)` (P1 Lemma 3.1). Then `u := 1 - gamma^2`, intersected with `[0, 1]`, and `G := u R^2`.
- **Chart rule** for a `gamma`-enclosure `Gamma = [g_lo, g_hi]` and a rational threshold `gamma_*`: if `g_lo >= gamma_*`, use the series chart; if `g_hi <= gamma_*`, use the direct chart; otherwise evaluate the series chart on `Gamma ∩ [gamma_*, 1]` and the direct chart on `Gamma ∩ [0, gamma_*]` and take the hull. Producer `gamma_* = 7/10`, checker `gamma_* = 5/8`.
- **Series chart.** `R = Psi(u) = sum_{n=0}^{79} c_n u^n + T0`, `R_gamma = -2 gamma (sum_{n=1}^{79} n c_n u^{n-1} + T1)`, with `c_0 = 1`, `c_{n+1} = c_n (2n+1)^2/((2n+2)(2n+3))`, and tails enclosed by `T0` in `[0, c_80 u^80/(1 - u)]`, `T1` in `[0, 80 c_80 u^79/(1 - u)]`, evaluated at the upper endpoint of `u`. These hold because all terms are nonnegative, `c_n` is nonincreasing, and `n c_n` is nonincreasing for `n >= 1`, as `(n+1) c_{n+1} / (n c_n) = (4n^2 + 4n + 1)/(4n^2 + 6n) <= 1`. On the series chart `u <= 1 - gamma_*^2 < 1`.
- **Direct chart.** `R = arccos(gamma)/sqrt(u)` and `R_gamma = (gamma R - 1)/u`; on the direct chart `u >= 1 - gamma_*^2 > 0`.
- Every interval operation must be defined on its arguments. An undefined operation on a cell (for instance a `D^2` enclosure not strictly positive) makes that cell's evaluation fail; such a cell is treated as cut for the box, never as regular, and in the far column it belongs to `A_p` (§3).
- Precision: producer 160 bits, checker 192 bits.

## §6 Producer search, partition and termination

**Resource-budget constants.** `MAX_CELL_COUNT = 2^16`, `MAX_CELL_DEPTH = 10`, `MAX_BOX_DEPTH = 12`. These are the resource budget itself; they are neither mathematical constants nor derived from any diagnostic value.

- **Initial boxes**: `r` and `tau` each split into 8 equal parts, `lambda` into 4 equal parts; 256 boxes, each of box depth 0.
- **Initial cells**: `mu` split into 64 equal parts, `phi` into 32 equal parts of `[0, pi]`; 2048 cells, each of cell depth 0. A cell of depth `MAX_CELL_DEPTH` may be evaluated but not bisected.
- **Cell round** for a non-straddle box: classify cells (§3), compute `L` and `B_cut` (§4); if accepted, stop. Otherwise let the bisectable cells be those of depth less than `MAX_CELL_DEPTH`. Select every bisectable cut cell, and the `ceil(N_reg/4)` bisectable regular cells with the largest score, where the score of a cell is the upper endpoint of the computed enclosure of `|C| · width(K(C, B))`, compared exactly, and `N_reg` is the number of bisectable regular cells; ties are broken by cell order. If the selection is empty, or `(current cell count) + 3 · (number selected)` exceeds `MAX_CELL_COUNT`, give up on the box. Otherwise bisect each selected cell in both variables (four children of depth one more) and repeat.
- **Box subdivision**: a straddle box, or a box given up on, of box depth less than `MAX_BOX_DEPTH`, is bisected along the coordinate of largest normalized width (`r` and `tau` normalized by 1, `lambda` by `13/50`; ties in the order `r`, `tau`, `lambda`). The two children have box depth one more and restart from the initial cells. A straddle box, or a box given up on, of box depth `MAX_BOX_DEPTH` is `UNRESOLVED` and is not subdivided.
- **Fail-closed**: one `UNRESOLVED` box makes the P2 run fail; no numerical near-positivity is accepted.
- **Versioning**: any change to this specification requires a new version and a fresh run; a run under a superseded version is closed as failed.

## §7 Certificate and checker

The producer emits, for every accepted leaf box: the box, its column, `c` (and `cbar`), `R`, and its cell partition. Producer values of `L`, `B_cut` and cell labels are informational and not trusted.

The checker imports no producer module and verifies, with exact rational arithmetic, that the leaf boxes cover `P` and that each cell partition covers `[-1, 1] x [0, pi]`; recomputes `rho_lo`, `rho_hi`, `z_lo`, `z_hi` and the column, and requires every leaf to be far or near; requires `c`, `cbar` and `R` to equal the values given by the rules of §3; reclassifies every cell by its own test; recomputes every enclosure at 192 bits with its own chart threshold; recomputes `L` and `B_cut` from its own classification; and requires `L - B_cut > 0` for every leaf.

## §8 Not claimed

Anything outside `P`; stationary points on the axis (the C system); any statement at `lambda` outside `[2/5, 33/50]`; the practical run time.
