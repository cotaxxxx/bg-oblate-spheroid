# D-OB P2 — D-AN-1 FT_q Exact Pair-Numerator Decomposition — DRAFT

**Status:** PAPER-PROOF ALGEBRA DRAFT / AWAITING CHAT AUDIT / BOUNDARY PAIR LEMMA OPEN / NOT A THEOREM

**Parent FT_q reduction:** `analysis/D_OB_P2_D_AN1_FT_Q_DRAFT.md`, commit `20c5c59bd74f940fe0b1e05892bd2169e09d4fde`, SHA-256 `46443f0e981f360e57fb70d99754b0e480042d246e22d36732b00b96102a9cd1`, **REDUCTION AUDIT PASS**.

**Evidence:** EXACT ANALYTIC ALGEBRA ONLY / NO DIAGNOSTIC EVIDENCE / NO INTERVAL COMPUTATION.

## 1. Scope

This artifact fixes only the exact `b <-> -b` decomposition of the common-denominator pair numerator required by FT_q §8.

It does not choose a proof partition, prove a lower bound, or define `c_FT` or `m0`.

Use the notation of the audited FT_q reduction:

`N_e := A2 b^2 + A0`,
`N_o := A1 b`,

so that

`N_+ := N_J(b) = N_e + N_o`,
`N_- := N_J(-b) = N_e - N_o`.

Also write

`D_+ := D(b)`,
`D_- := D(-b)`,
`R_+ := R(gamma_+)`,
`R_- := R(gamma_-)`,

and

`Rbar := (R_+ + R_-)/2`,
`DeltaR := (R_+ - R_-)/2`.

Hence exactly

`R_+ = Rbar + DeltaR`,
`R_- = Rbar - DeltaR`.                                      (1.1)

## 2. Exact four-term identity

The paired integrand before the common positive factors is

`R_+ N_+/D_+^3 + R_- N_-/D_-^3`.

After multiplication by the positive common denominator
`D_+^3 D_-^3`, define

`P := R_+ N_+ D_-^3 + R_- N_- D_+^3`.                       (2.1)

Substituting (1.1) and
`N_+ = N_e + N_o`,
`N_- = N_e - N_o`,
gives the exact identity

`P = Rbar N_e (D_-^3 + D_+^3)`
`  + Rbar N_o (D_-^3 - D_+^3)`
`  + DeltaR N_e (D_-^3 - D_+^3)`
`  + DeltaR N_o (D_-^3 + D_+^3)`.                           (2.2)

No inequality has been used in (2.2).

For bookkeeping, put

`S3 := D_-^3 + D_+^3 > 0`,
`Delta3 := D_-^3 - D_+^3`,                                  (2.3)

and

`T_EE := Rbar N_e S3`,
`T_OO := Rbar N_o Delta3`,
`T_RE := DeltaR N_e Delta3`,
`T_RO := DeltaR N_o S3`.                                    (2.4)

Thus

`P = T_EE + T_OO + T_RE + T_RO`.                            (2.5)

## 3. Exact distance asymmetry

Since

`D_-^2 - D_+^2 = 4 rho b`,

we have away from the coincident point

`D_- - D_+ = 4 rho b/(D_- + D_+)`.                          (3.1)

Therefore

`Delta3`
`= (D_- - D_+)(D_-^2 + D_- D_+ + D_+^2)`
`= 4 rho b L_D`,                                            (3.2)

where

`L_D := (D_-^2 + D_- D_+ + D_+^2)/(D_- + D_+) > 0`.        (3.3)

Consequently, for `rho > 0`,

`sign(Delta3) = sign(b)`.                                   (3.4)

The distance-asymmetric odd term becomes exactly

`T_OO = 4 rho Rbar A1 b^2 L_D`.                             (3.5)

Thus `T_OO` is even in `b`.

## 4. Exact R asymmetry and sign ledger

The audited FT_q reduction gives

`gamma_+ - gamma_-`
`= 4 rho b X`
`  / [w D_+ D_- (h_+ D_- + h_- D_+)]`,                     (4.1)

where

`X := h0 c(mu) + lambda^2 rho^2 b^2`.                       (4.2)

On the boundary face `h_+, h_- >= 0`.

Away from the coincident surface/base-point point, the denominator
in (4.1) is positive. Hence

`sign(gamma_+ - gamma_-) = sign(b) sign(X)`                 (4.3)

whenever the difference is nonzero.

Because `R_gamma <= 0`,

`sign(DeltaR) = -sign(b) sign(X)`                           (4.4)

whenever `DeltaR` is nonzero.

The P1 trap gives

`1 <= Rbar <= pi/2`,                                        (4.5)

and the Lipschitz estimate gives

`|DeltaR| <= |gamma_+ - gamma_-|/2`.                        (4.6)

No stronger estimate on `R` is assumed.

For the two terms containing `N_o = A1 b`, the exact sign ledger is

`sign(T_OO) = sign(A1)`,                                    (4.7)

and

`sign(T_RO) = -sign(A1) sign(X)`.                           (4.8)

Thus for `X > 0`, these two odd-origin terms have opposite signs.

For `X < 0`, they have the same sign.

## 5. Parity under b -> -b

Under `b -> -b`:

- `N_e` is even;
- `N_o` is odd;
- `D_+ <-> D_-`;
- `S3` is even;
- `Delta3` is odd;
- `gamma_+ <-> gamma_-`;
- `Rbar` is even;
- `DeltaR` is odd.

Therefore every term in (2.4) is even:

`T_EE : even * even * even`,
`T_OO : even * odd * odd`,
`T_RE : odd * even * odd`,
`T_RO : odd * odd * even`.                                 (5.1)

Hence

`P(-b) = P(b)`.                                             (5.2)

This is the parity required for the L2 half-azimuth folding.

Equation (3.5) displays the `b^2` factor in `T_OO` explicitly.

For `T_RE`, both `DeltaR` and `Delta3` are odd in `b`.

For `T_RO`, the product `DeltaR * N_o` is even.

## 6. Boundary coefficient and rho-power ledger

On the boundary face, the audited factorization gives

`A2 = -lambda^2 (m - mu) m rho`,                            (6.1)

`A1 = -lambda^2 (m - mu) B1`,                              (6.2)

`A0 = -lambda^2 (m - mu) rho C0`,                          (6.3)

where

`B1`
`:= lambda^2 m^2 mu`
` - lambda^2 m mu^2`
` - lambda^2 m`
` + lambda^2 mu`
` + m^2 mu`
` + m mu^2`
` - 2 mu`,                                                  (6.4)

and

`C0`
`:= -lambda^2 m mu^2`
` + lambda^2 m`
` + lambda^2 mu^3`
` - lambda^2 mu`
` - m`
` - mu^3`
` + 2 mu`.                                                  (6.5)

Therefore

`N_e`
`= -lambda^2 (m - mu) rho [m b^2 + C0]`,                   (6.6)

and

`N_o`
`= -lambda^2 (m - mu) B1 b`.                               (6.7)

Thus:

- `N_e` carries one explicit odd power of `rho`;
- `N_o` carries no explicit power of `rho`;
- `Delta3` carries one explicit `rho` by (3.2).

In particular,

`T_OO`
`= -4 lambda^2 (m - mu) rho Rbar B1 b^2 L_D`.              (6.8)

For `T_RE`, the product `N_e Delta3` contains

`rho^2 = 1 - m^2`.                                         (6.9)

For `T_RO`, `N_o` contains no explicit `rho`, while
`DeltaR` is controlled by (4.1), whose numerator contains
the explicit factor `rho b X`.

Any later rational reduction must state explicitly which odd powers
of `rho` remain after using

`rho^2 = 1 - m^2`.                                         (6.10)

No odd power of `rho` may be silently replaced by a rational
polynomial in `m`.

## 7. Proof-partition acceptance conditions

No proof partition is selected in this artifact.

Any later partition of the `mu` interval is restricted to exact roots
of

`C0(lambda,m,mu) = 0`,
`c(lambda,m,mu) = 0`,
`B1(lambda,m,mu) = 0`.                                     (7.1)

The roots depend on `(lambda,m)`.

The `m = 1` factorizations are orientation aids only and must not be
used as substitutes for the exact `m < 1` formulas.

If a rational enclosure of a root is introduced, it must be certified
by polynomial sign evaluation at rational endpoints.

Such an enclosure must either be uniform on the frozen box

`lambda in [2/5,93/200]`,
`m in [112/113,1]`,                                        (7.2)

or the exact root must remain as a `(lambda,m)`-dependent partition
boundary.

Every inequality used on a partition piece must depend only on:

1. that piece's defining exact sign conditions; and
2. the frozen global box (7.2).

No information from an adjacent partition piece may be borrowed.

No sampled, diagnostic, or post-selected partition is admissible.

## 8. What remains open

The exact identity (2.2), parity (5.1), and sign ledger
(3.4), (4.3)-(4.8) do not prove `P >= 0`.

Pointwise positivity of `P` is not asserted and is not required by the
frozen FT_q statement.

The next analytic task is to integrate the even pair over the
half-azimuth and `mu`, extract favorable contributions, and dominate
unfavorable contributions using only:

- the exact proof partitions allowed by §7;
- `1 <= Rbar <= pi/2`;
- `|DeltaR| <= |gamma_+ - gamma_-|/2`;
- exact finite-difference identities.

No `c_FT` is set here.

## 9. Governance

This artifact is algebra/sign bookkeeping only.

It introduces:

- no diagnostic evidence;
- no numerical threshold;
- no proof partition;
- no interval computation;
- no `c_FT`;
- no `m0`;
- no theorem claim.

**Operational status:** P EXACT DECOMPOSITION DRAFT / AWAITING CHAT AUDIT / PROOF-PARTITION CONDITIONS PREDECLARED / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
