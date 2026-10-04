# D-OB P2 — D-AN-1 L0 Rational Coverage Lemma — DRAFT

**Status:** PAPER-PROOF DRAFT / AWAITING CHAT AUDIT / NOT A THEOREM
**Parent:** `analysis/D_OB_P2_D_AN1_PREDECLARE.md`, commit `a262496a75467e2506beda3ad5443abe0508a78c`, SHA-256 `f65150f72af95fd4061ee8f15d1a72893bf0bceed142e18c005b8e186c32baac`
**Frozen target:** D-AN-1 §3, L0 only. No computation or diagnostic input is used.

## L0. Rational coverage of the certification-demand image

For `lambda in [2/5,93/200]`, define the closed analytic sector

`S_AN(lambda) := { (rho,z) : rho >= 0, z >= 0, 49/64 <= rho^2 + z^2/lambda^2 <= 1, 112 lambda rho <= 15 z }`,

and

`S_AN := { (rho,z;lambda) : lambda in [2/5,93/200], (rho,z) in S_AN(lambda) }`.

Then the frozen certification-demand image `Sigma` of D-AN-1 §1.1 satisfies

`Sigma subset S_AN`.

### Proof

Take an arbitrary point of `Sigma`. Thus, for rational-box parameters

`lambda in [2/5,93/200]`, `r in [7/8,1]`, `tau in [7/8,1]`,

we have

`rho = r (1-tau^2)/(1+tau^2)`,

`z/lambda = r 2 tau/(1+tau^2)`.

All denominators below are positive because `tau >= 7/8 > 0`.

First, `tau <= 1` gives `1-tau^2 >= 0`; hence `rho >= 0`. Also `z >= 0` because `lambda,r,tau` are nonnegative.

Second, the exact identity

`(1-tau^2)^2 + 4 tau^2 = (1+tau^2)^2`

gives

`rho^2 + z^2/lambda^2 = r^2`.

Since `7/8 <= r <= 1`, squaring the nonnegative endpoints gives

`49/64 <= rho^2 + z^2/lambda^2 <= 1`.

Third, the sector inequality is equivalent, after substituting the defining map and cancelling the positive factors `lambda r/(1+tau^2)`, to

`112 (1-tau^2) <= 30 tau`.

Move all terms to the right:

`0 <= 112 tau^2 + 30 tau - 112`.

The quadratic factors exactly as

`112 tau^2 + 30 tau - 112 = (8 tau - 7)(14 tau + 16)`.

For `tau in [7/8,1]`, both factors are nonnegative (`8 tau - 7 >= 0` and `14 tau + 16 > 0`). Therefore

`112 lambda rho <= 15 z`.

Every defining inequality of `S_AN` has now been verified using exact rational identities and inequalities. Hence `(rho,z;lambda) in S_AN`. Since the chosen point of `Sigma` was arbitrary,

`Sigma subset S_AN`.

This also includes the `rho=0` edge: at `tau=1`, `rho=0` and the sector inequality is immediate. No floating containment or numerical sampling is used. QED.

## Dependency / scope note

L0 uses only the frozen coordinate map and rational parameter bounds of D-AN-1 §1.1. It does not invoke Lemma V, the C-axis lemmas, the paired `K_H` representation, Phase 0 diagnostics, or any partition tuning. It therefore establishes only the stage on which L1–L3 may be attempted; it establishes no sign of `H`.
