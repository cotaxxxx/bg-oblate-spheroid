# D-OB P1 DIAGNOSTIC — PREDECLARED SAMPLING RULE

**Status**: `PREDECLARED / DIAGNOSTIC_NOT_RUN / NOT_EVIDENCE`

**Base.** Branch `design/d-ob-p1`, P1 design note `analysis/D_OB_P1_DESIGN_NOTE.md` (commit `6c6282a8acbf467bcbe6a7e32236e1d32a91f400`, blob `f81e120e44a866d206117d4fab5fac627f26ccd1`), §8.4. This document fixes the diagnostic before any result is seen. The diagnostic is `DIAGNOSTIC_ONLY`: it is not a proof, and no value it produces may enter any predeclare or certification choice.

## 1. Questions and admissible answers

- Q1: does `H` have a uniform sign on `Q_lambda` for every sampled `lambda`?
- Q2: does `E_rhorho` have a uniform sign on `Q_lambda` for every sampled `lambda`?

Each answer is exactly one of `YES(+)`, `YES(-)`, `NO`. The direction of the sign is recorded because it determines which inequality a later certification would target. No numerical value is recorded.

## 2. Sample

- `lambda`: 9 equally spaced values in `[2/5, 33/50]`, endpoints included. Parameters known from the C system (`lambda_c`, `lambda_partial`) are deliberately not added.
- Meridional points: `rho = r cos(theta)`, `z = lambda r sin(theta)`, with
  - `theta`: 9 equally spaced values in `[0, pi/2]`, including the equator `theta = 0` and the axis `theta = pi/2`;
  - `r`: `k/8` for `k = 0, ..., 7`, and `1 - 2^(-k)` for `k = 4, 6, 8, 10`.
- The boundary `r = 1` is not sampled, because the `1/D` singularity of the integrand makes quadrature there unreliable; by Lemma V the quantities are continuous up to the boundary.

## 3. Quantities and evaluation

- `E_rhorho` is evaluated as `(1/(4 pi lambda)) integral integral F_rhorho dphi dmu`, with `F_rhorho` from Lemmas 3.3–3.4 of the design note at `v = e_x`.
- `H` is evaluated as `E_rho/rho` for `rho > 0`, with `E_rho = (1/(4 pi lambda)) integral integral F_rho dphi dmu`, and as `E_rhorho` on the axis `rho = 0`.
- `R` and `R_gamma` are evaluated with a representation that is stable near `gamma = 1` (Lemma 3.2).
- The `phi`-integral uses the symmetry `phi -> -phi` (integrate over `[0, pi]` and double).
- Every integral is computed in double precision by adaptive two-dimensional quadrature at two tolerance levels, `(epsabs, epsrel) = (1e-7, 1e-7)` and `(1e-9, 1e-9)`.

## 4. Decision rule

For each question: the answer is `YES(+)` if, at every sampled `(lambda, r, theta)`, both tolerance levels give a strictly positive value; `YES(-)` if both give a strictly negative value everywhere; otherwise `NO`. In particular, any sampled point at which the two tolerance levels disagree in sign, or either value is zero, makes the answer `NO`. Quadrature uncertainty is never resolved in favour of a uniform sign.

## 5. Records

The script and its outputs are kept outside the repository, as for PROBE6. The repository receives only this document and, afterwards, a short record of the two answers. If neither answer is `YES`, any partition is derived analytically as stated in §8.4 of the design note, never from diagnostic values.
