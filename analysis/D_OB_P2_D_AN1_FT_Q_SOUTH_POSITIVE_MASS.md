# D-OB P2 / D-AN-1 FT_q — South Positive-Mass Lemma (unified paper proof) — DRAFT

**Status:** PAPER-PROOF DRAFT / AWAITING CHAT FULL-TEXT AUDIT / NOT A THEOREM / NOT CANONICAL
**Evidence class:** exact analytic inequalities + exact rational Bernstein certificates (D-AN-1 v1.1 §5 ruling: no G-numbered predeclare required; no interval computation; no diagnostic value enters any constant or partition).
**Scope:** the boundary face `rho^2 + m^2 = 1` of FT_q, meridional variable `mu in [-1, 1/2]`. It establishes a uniform rational lower bound for the positive mass of the paired kernel on `[-1, 1/2]`. It does **not** bound the north/near residual, does not set `c_FT` or `m0`, and does not change the status of the Boundary Pair Lemma (OPEN) or of D-P2 (NOT_CERTIFIED).
**Author of this draft:** code (Claude Code). Component attribution is recorded in §8.

## 0. Pins (full SHA-256)

| object | identity |
|---|---|
| FT_q reduction (audited) | `analysis/D_OB_P2_D_AN1_FT_Q_DRAFT.md`, commit `20c5c59bd74f940fe0b1e05892bd2169e09d4fde`, SHA-256 `46443f0e981f360e57fb70d99754b0e480042d246e22d36732b00b96102a9cd1` |
| P exact decomposition (audited) | `analysis/D_OB_P2_D_AN1_FT_Q_P_DECOMPOSITION_DRAFT.md`, commit `641e2a2d4b0720e47c73f257cbf8de1b89eac9c5`, SHA-256 `67d821d4612015648758de57887fce699db1143952b658e6733cba1ebd61b518` |
| C0/B1 root structure (audited) | `analysis/D_OB_P2_D_AN1_FT_Q_C0_B1_ROOT_STRUCTURE_DRAFT.md`, commit `32308e842681b72c5fe661cb73ce4daecbd4ea4e`, SHA-256 `d2dc0cf0aee36ae73a97f9d4b461b1aed82678a0d7f716ed5ec2cc65de217bb8` |
| B1 ordering lemma (audited) | `analysis/D_OB_P2_D_AN1_FT_Q_B1_ORDERING_LEMMA_DRAFT.md`, commit `428320ec7fda757e17e9e19d0e0236aba99d9aab`, SHA-256 `4145624ad9b8b8203ada46d02fad9c2c39e2798e8253809b7f101bedffdfc283` |
| Judge contracts 20''–23'' v1.1 (frozen) | `analysis/D_OB_P2_D_AN1_FT_Q_CONTRACT_20_DOUBLE_PRIME_TO_23_DOUBLE_PRIME_V1_1.md`, commit `b1a10ea6f0ef127aaf4a40a93070cf270d03e073`, SHA-256 `db975daba9d712246ed5e27465437f34450b356f453729a5fb78ec8ceab468cb`; parent fixed contract `analysis/D_OB_P2_D_AN1_FT_Q_CONTRACT_20_DOUBLE_PRIME_TO_23_DOUBLE_PRIME.md`, commit `00138df257cee8e5480b412157dce36ae90743d0`, SHA-256 `80c0570329dfba48cd9e60f0d330afe6d4a526887c44b0cca826eca5ed0db39d` |
| Astra 39' independent report (audited) | `D_OB_P2_certificate39prime_independent_report_2026-10-08.md`, SHA-256 `1d084881ffe60fb4fb7f7f37ac48aae06ba6be2693f76fd2b091d222a0c60d9f` |
| Astra 39' exact script | `certificate39prime_exact.py`, SHA-256 `4b51bd9b57bb83c40737f6c10ce61fab736ed08334f29ed430a5825d8b0d8888` |
| Astra 39' coefficients | `certificate39prime_coefficients.json`, SHA-256 `853d022e0fa8720a99f34a81b5ff5664e0c2c6f6fa6fa2e6fdccc78fe4d40a80` |
| code: G > 0 on K (question 1) | `tools/d_ob_p2/ftq_cert/bernstein_G.py`, commit `f74e1221762f1b52e00bf5fbc7ba3b548526f953`, SHA-256 `97057844894f699dea9a994dc7b9d2c5f46673d9f67c5b9c9535f5e7f4cc23e3` |
| code: A < 0 on J (C1–C4, AUX) | `tools/d_ob_p2/ftq_cert/bernstein_south_A.py`, commit `f74e1221762f1b52e00bf5fbc7ba3b548526f953`, SHA-256 `977f629435d84dfda5152271d8774f2f432757f8f7cc5d5615ef8df820e5a0af` |
| code: theta d > 14/5 on J (independent route) | `tools/d_ob_p2/ftq_cert/theta_14_over_5_cert.py`, commit `6621f3d9c234557200f1d6a884ed603306ca1b40`, SHA-256 `f0ab87b17507451197c06f2ab25cca66f1083c1f609b93f83e1c135c97ca8b88` |
| code: kernel extension (ACTIVE PIN) | `tools/d_ob_p2/ftq_cert/kernel_extension_cert.py`, commit `1ac44469f33fb74b1b4cbfcd62621dce3f6fa12e`, SHA-256 `3c4b0d452d87072c2c7a27d432048691c4cce47da871bfad0a50630436146e85` (supersedes `71695085` / `da89b482…`, W-17 wording only) |

The three Astra originals are not yet imported into canonical; they are pinned here by SHA-256 only. The code certificates live on `cotaxxxx/basepoint-geometry`, branch `claude/d-ob-p2-resumable-i8dgpn`.

## 1. Setting and units

Frozen box: `lambda in [2/5, 93/200]`, `tau in [7/8, 1]`; `L := lambda^2 in [4/25, 8649/40000]`, `m = 2 tau/(1+tau^2) in [112/113, 1]`, `rho = (1-tau^2)/(1+tau^2) in [0, 15/113]`, `r := rho^2 = 1 - m^2`.
Surface variables: `mu in [-1,1]`, `phi in [0, pi]`, `a^2 = 1 - mu^2`, `b = a cos phi`, `q = b^2 in [0, a^2]`, `s = m - mu`, `h = 1 - m mu`, `w^2 = mu^2 + L a^2`.
Distances: `d = a^2 + r + L s^2`, `D_±^2 = d ∓ 2 rho b`, `v = D_+ D_-`, `u = D_+ + D_-`, `e := 4 r a^2`; exactly `v^2 = d^2 - 4 r q >= d^2 - e`, `u^2 = 2(d + v)`.
Kernel pieces (P-decomposition, FT_q §§5–7): `S_3 = u(2d - v) = D_+^3 + D_-^3`, `L_D = (2d+v)/u`, `theta = 4 L_D/S_3 = 2(2d+v)/((d+v)(2d-v))`,
`B_1 = m(1-L)mu^2 + ((1+L)m^2 + L - 2)mu - L m`, `C_0 = (L-1)mu^3 - L m mu^2 + (2-L)mu - m(1-L)`, `E = m q + C_0`, `g = m a^2 + C_0`,
`A = E S_3 + 4 B_1 q L_D = S_3 (E + theta B_1 q)`, `K_R = 4 r E L_D + B_1 S_3`, and the paired integrand
`F = Rbar A + b (DeltaR/rho) K_R`, with `Rbar = (R_+ + R_-)/2 in [1, pi/2]`, `DeltaR = (R_+ - R_-)/2`, `-1 <= kappa_R <= 0` the secant coefficient of `R` (P1 trap `-1 <= R_gamma <= 0`).
**P units** (contract 21''): `I(mu,phi) = -lambda^2 s F W`, `W = 1/(w v^3)`, `G(mu) = int_0^pi I dphi`, and `2 pi lambda H(rho, lambda m; lambda) = int_{-1}^{1} G(mu) dmu`.

Roots. For `m < 1` (the domain of the audited root-structure lemma): `B_1` has exactly one root `mu_B^- in (-1/2, -1/8)` in `[-1,1]`, `B_1 > 0` to its left and `< 0` to its right; `C_0` has exactly one root `mu_C in (0, m)` in `[-1,1]`, `C_0 < 0` for `mu < mu_C`. Certified in addition: `1/2 < mu_C < 3/5` (39' C4 / `bernstein_south_A.py` C4a, C4b).
Endpoint `m = 1` (`rho = 0`, included in the frozen box but excluded from the root-structure lemma): both polynomials acquire the additional root `mu = 1`, exactly
`B_1 = (mu - 1)((1-L) mu + L)`, `C_0 = (mu - 1) P(mu)`, `P(mu) := (1-L)(1 - mu^2) - mu`.
Hence on `[-1, 1)` the statements above persist at `m = 1`: the inner root of `B_1` is `mu_B^- = -L/(1-L) in (-1/2, -1/8)` (since `1/9 < L < 1/3`), with `B_1 > 0` left of it and `< 0` on `(mu_B^-, 1)`; `P > 0` on `[-1, 0]`, `P' = -2(1-L) mu - 1 < 0` on `[0, 1]`, `P(1/2) = (1-3L)/4 >= 14053/160000 > 0`, `P(3/5) = (1-16L)/25 <= -39/625 < 0`, so `C_0` has exactly one root `mu_C in (1/2, 3/5)` in `[-1, 1)` with `C_0 < 0` for `mu < mu_C`. Uniqueness of the roots is therefore asserted on the half-open interval `[-1, 1)` for all `m in [112/113, 1]`; the extra root `mu = 1` at `m = 1` plays no role below (`[-1, 1/2]` and `[-1, mu_C)` do not contain it).

## 2. Inputs taken as audited

- (I1) FT_q reduction §§3–7 and P-decomposition §§2–6: the exact forms of `A`, `K_R`, `F`, the finite difference `gamma_+ - gamma_- = 4 rho b X/[w D_+ D_- (h_+ D_- + h_- D_+)]`, `X = h_0 c(mu) + L r q`, the Lipschitz/sign control of `DeltaR`.
- (I2) 39' C3 identities (code-verified symbolically): with `c_* = h - d`, `T = (1-L)m - (2-L)mu`, `Y = h c_* + r q`, `Z = T - m q/h + theta E`, `M = h u - 4 r q/u`: `B_1 = m c_* + r T`, `C_0 + h T = mu (L-1) s^2`, `K_R/S_3 = (m/h) Y + r Z`, `X = L Y`, `h_+ D_- + h_- D_+ = lambda M`, hence
  `F/S_3 = Rbar (E + theta B_1 q) + (2 kappa_R lambda q/(w v M)) Y ((m/h) Y + r Z)`, and after completing the square the adverse part of the secant term is at most `J_sec := lambda q r^2 h Z^2/(2 m w v M)`.
- (I3) `theta <= 3/d` (from `v <= d` and monotonicity of `psi(t) = 2(2+t)/((1+t)(2-t))`, `psi(1) = 3`).
- (I4) `S_3/v^3 = D_+^{-3} + D_-^{-3} >= 2 v^{-3/2} >= 2 d^{-3/2}` (AM–GM, `v <= d`).

## 3. Lemma A — pointwise sign on the exterior south `J = [-1/4, mu_C)` (Astra 39' C1–C4; code audit PASS)

For all parameters in the box and all `mu in [-1/4, mu_C)`, `phi in [0, pi]`:

    -F/S_3 >= (-C_0) sin^2 phi + (3/200) cos^2 phi > 0.                                (A)

Proof structure (constants are those certified in the 39' report and `bernstein_south_A.py`; all on the box `L in [4/25, 8649/40000]`, `m in [112/113, 1]`, `mu in [-1/4, 3/5]`):
1. `d >= 416/625`, `d < 13/10`; `4 r q/d^2 <= 87890625/552438016 < 23/144`, hence `v/d > 11/12` and `theta d > psi(11/12) = 840/299 > 14/5`. Independent route: `(1-c^2) d^2 - e > 0` with `c = 913/1000 > (1+sqrt 29)/7` (`theta_14_over_5_cert.py`, min Bernstein coefficient `2058768436330482951/63690375390625000000`).
2. Secant: `h > 2/5`, `u^2 > 62/25`, `-369/32 < Z < 479/80`, `4 r q/(h u^2) < 28125/395839 < 1/14`, so `M > (13/14) h u` and `J_sec <= 7 q r^2 Z^2/(13 m v u) <= (506250/18757661) q <= (3/100) q` (the last inequality is strict for `q > 0`; at `q = 0` both sides vanish, e.g. `mu = 0, phi = pi/2`).
3. `Pi_t := -(g + (3/100) a^2) d - t B_1 a^2 > 0` for `t = 3` and `t = 14/5` (72 + 72 positive Bernstein coefficients, minima `106592/1953125` and `40192/1953125`); with `d < 13/10`, `Pi_t/d > 3/200`.
4. With `z = cos^2 phi`: `E + theta B_1 q + (3/100) q = (1-z) C_0 + z[-Pi_t/d + (theta - t/d) B_1 a^2]`; choose `t = 3` where `B_1 >= 0` (`theta <= 3/d`) and `t = 14/5` where `B_1 < 0` (`theta > 14/(5d)`), so the bracket is `<= -Pi_t/d < -3/200`. Hence `E + theta B_1 q <= (1-z) C_0 - (3/200) z - (3/100) q < 0`, and with `Rbar >= 1`:
   `-F/S_3 >= -Rbar (E + theta B_1 q) - J_sec >= -(E + theta B_1 q) - (3/100) q >= (-C_0)(1-z) + (3/200) z`.
   `C_0 < 0` on `J` gives strict positivity. Degenerate cases `q = 0`, `B_1 = 0`, `E = 0`, `rho = 0` are included; no coincident point lies in `J` (`D_± > 0`).

## 4. Lemma B — pointwise sign on the kernel `K = [-1, -1/4]` (code; CHAT AUDIT PASS recorded)

For all parameters and all `mu in [-1, -1/4]`, `phi in [0, pi]`, inequality (A) holds with the same constants `3/100`, `3/200`.

Every condition of §3 is re-proved on the box `L in [4/25, 8649/40000]`, `m in [112/113, 1]`, `mu in [-1, -1/4]` by `kernel_extension_cert.py` (no J-box constant is imported):
1. `Pi_3 > 0`, `Pi_{14/5} > 0` on `K` (minimum Bernstein coefficients `1572994971/23086352000`, `23286555999/144289700000`).
2. `(1-c^2) d^2 - e > 0` on `K` with `c = 913/1000` (minimum `665724/9765625`), hence `theta d > 14/5`; `theta d <= 3` by (I3).
3. Secant on `K`: `d >= 16/25`, `d^2 - e >= 256/625` (so `v >= 16/25`, `u >= 8/5`), `h >= 141/113`, `a^2 <= 15/16`, `T in [22107911/18080000, 67/25]`, `C_0 in [-209/100, -70811733/57856000]`, `E <= g <= -30053/102400 < 0`, `theta E in [3(-209/100)/(16/25), 0)`; therefore `|Z| <= 7924370683/849760000`, `4 r q/(h u^2) <= 28125/1359616 < 1/14`, `M > (13/14) h u`, and
   `J_sec <= 7 q r^2 Z^2/(13 m v u) <= (5086447708448780805609/355067704829628215459840) q <= (3/100) q` (strict for `q > 0`; both sides vanish at `q = 0`).
4. `d < 13/10` on `K` from the identity `d = 2 - (1-2L) m^2/(1-L) - (1-L)(mu + L m/(1-L))^2` (so `d <= 2 - (1-2L) m^2/(1-L) <= 515867950/400320919`), hence `Pi_t/d > 3/200` for both `t`.
5. The algebra of §3 step 4 is identical; `C_0 < 0` on `K`.

The seam `mu = -1/4` belongs to both closed certificate boxes, so (A) holds on the whole of `[-1, mu_C)`.

## 5. Lemma C — integrated positive mass on `[-1, 1/2]`

Let `C_0^*(mu) := C_0(L, m, mu)` at `(L, m) = (8649/40000, 112/113)`. Since `dC_0/dm = -(L mu^2 + 1 - L) < 0` and `dC_0/dL = (m - mu)(1 - mu^2) >= 0`, `C_0 <= C_0^*` on the box, so `-C_0 >= -C_0^*` for every parameter.

For `mu in [-1, 1/2]` (`1/2 < mu_C`, so (A) applies):
`G(mu) = int_0^pi lambda^2 s (S_3/v^3)(-F/S_3)/w dphi >= (lambda^2 s/w) (5/4) int_0^pi [(-C_0) sin^2 phi + (3/200) cos^2 phi] dphi = (lambda^2 s/w)(5/4)(pi/2)[-C_0 + 3/200]`,
using `S_3/v^3 >= 2 d^{-3/2} > 5/4` (`d < 13/10 < (8/5)^{2/3}`), `lambda^2 >= 4/25`, `w <= 1`, `s >= 112/113 - mu > 0`, `pi > 3`:

    G(mu) >= (3/10) (112/113 - mu) (-C_0^*(mu) + 3/200),                              (C)

and, by exact integration of the polynomial on the right,

    int_{-1}^{1/2} G(mu) dmu  >=  S''_lb := 635530452759/817216000000  (~ 0.77768).  (S'')

`S''_lb` is a lower bound for the **whole** interval `[-1, 1/2]`. It replaces the earlier `S_K >= 207/5000` (20'') and `C_core >= 1/8` (39'); it is never added to them (W-17).

## 6. Consequence for the Boundary Pair Lemma (what is and is not established)

With contract 21'' partition `[-1,1] = [-1,1/2] ∪ (1/2, mu_C) ∪ [mu_C, m - rho) ∪ [m - rho, 1]`:
- `(1/2, mu_C)`: `G > 0` by Lemma A, so it may be dropped one-sidedly (`U_south,rem = 0`).
- `[mu_C, m - rho)` (north far) and `[m - rho, 1]` (near band incl. cap): OPEN; write `U_north + U_near >= int [-G]_+` over them.
Consequently,

    2 pi lambda H >= S''_lb - (U_north + U_near).

If a uniform certified rational bound `U_north + U_near < S''_lb` is established, the resulting positive gap can be used to derive an explicit uniform lower bound for `H` on the face, and only then may a rational `c_FT` be declared (22''). **None of `U_north`, `U_near`, `c_FT`, `m0` is established here; `c_FT` remains UNSET.** Until 22'' is updated, the active budget remains `U_north + U_near < 104/625`.

## 7. Not claimed

No bound on the north/near residual; no `c_FT`; no `m0`; no statement about `L3`, `L1`, `D-AN-2`, or D-P2 certification. Diagnostic values (region decompositions, grid scans) were used only to find counterexample candidates and to check feasibility of majorants, never to choose a constant or a partition.

## 8. Attribution and audit ledger

| component | producer | audit |
|---|---|---|
| question-1 `G > 0` on `K` (`A < 0` on `K`) | code | chat |
| Lemma A (39' C1–C4) and `C_core > 1/8` (C5) | Astra | code (full re-derivation), chat |
| independent `theta d > 14/5` certificate | code | chat (SHA verified, execution reported) |
| proposal and precheck of the kernel extension | chat | — |
| Lemma B (kernel extension certificate) | code | chat (CHAT AUDIT PASS, W-17 corrected in `1ac44469`) |
| this unified draft | code | PENDING |

## 9. Reproduction

Python 3.11, sympy 1.14.0; exact `fractions.Fraction` / sympy rationals only.
`python3 tools/d_ob_p2/ftq_cert/bernstein_G.py` (≈0.4 s), `bernstein_south_A.py` (≈12 s), `theta_14_over_5_cert.py` (≈1 s), `kernel_extension_cert.py` (≈1.2 s, ends with `ALL CERTIFICATES PASS`); Astra: `python3 certificate39prime_exact.py` (≈2 s, `EXACT ALGEBRA CHECKS: PASS`).

**Operational status:** SOUTH POSITIVE-MASS DRAFT / AWAITING CHAT AUDIT / S''_lb CANDIDATE (22'' OLD BUDGET ACTIVE) / NORTH + NEAR OPEN / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
