# D-OB P2 — D-AN-1 FT_q C0/B1 Exact Root Structure Lemma — DRAFT

**Status:** PAPER-PROOF ROOT-STRUCTURE DRAFT / AWAITING CHAT AUDIT / NO ENCLOSURE / NO PROOF PARTITION / NOT A THEOREM
**Parent:** `analysis/D_OB_P2_D_AN1_FT_Q_P_OVER_RHO_SYMMETRIC_REDUCTION_DRAFT.md`, commit `356f194a8507b50edd4997cb665a75029c6f2f6e`, SHA-256 `94429400a83da386fda1b18c8aa5d05f5162e90e2f1767ba55aec01ce190b1e7`, 76 lines, CHAT AUDIT PASS.
**Domain of this lemma:** `2/5<=lambda<=93/200`, `112/113<=m<1`, hence `rho=sqrt(1-m^2)>0`. The endpoint `m=1` is excluded and remains for endpoint continuation / NP-T handling.

## 1. Scope
This artifact proves only the exact root counts and interval locations of `B1(mu)` and `C0(mu)` needed before any proof-partition choice.
No rational enclosure, sampling, diagnostic partition, `c_FT`, or Boundary Pair Lemma estimate is introduced.
Additional ordering relative to the already-defined roots `mu_c^-<0<mu_c^+` is not claimed unless proved below. In this draft it remains UNDETERMINED.

## 2. B1 coefficient form
Starting from the audited boundary coefficient, collect powers of `mu`:
`B1(mu)=m(1-lambda^2)mu^2 +(lambda^2 m^2+lambda^2+m^2-2)mu-lambda^2 m`. (2.1)
The leading coefficient and constant term satisfy
`m(1-lambda^2)>0`, `B1(0)=-lambda^2 m<0`. (2.2)
Hence the product of the two roots is negative: `B1` has exactly two distinct real roots of opposite signs.

## 3. B1 exact endpoint signs
Direct substitution in (2.1) gives
`B1(m)=-2m rho^2<0`. (3.1)
`B1(1)=-(1-m)[m+2-lambda^2(1-m)]<0`. (3.2)
The bracket in (3.2) is positive because `m>0`, `lambda^2<1`, and `0<1-m<1`.
Also
`B1(-1)=-(1+m)[lambda^2(1+m)+m-2]`. (3.3)
Since `lambda^2<1/2`,
`lambda^2(1+m)+m-2 < (1+m)/2 +m-2 = 3(m-1)/2 <0`,
so `B1(-1)>0`. (3.4)

Let the two roots be `mu_B^-<0<mu_B^+`. From `B1(-1)>0>B1(0)`,
`-1<mu_B^-<0`. (3.5)
Because the quadratic opens upward and `B1(1)<0`, while the positive root is the right-hand zero,
`mu_B^+>1`. (3.6)
Therefore on `[-1,1]` there is exactly one B1-root, `mu_B^-`, and
`B1(mu)>0` for `-1<=mu<mu_B^-`,
`B1(mu)<0` for `mu_B^-<mu<=1`. (3.7)

## 4. C0 coefficient form
Collecting powers of `mu` gives
`C0(mu)=(lambda^2-1)mu^3-lambda^2 m mu^2 +(2-lambda^2)mu-m(1-lambda^2)`. (4.1)
The leading coefficient is negative.

Direct substitution gives
`C0(-1)=-(1+m)<0`. (4.2)
`C0(0)=-m(1-lambda^2)<0`. (4.3)
`C0(m)=m rho^2>0`. (4.4)
`C0(1)=1-m>0`. (4.5)

## 5. C0 exact root count and placement
Because the leading coefficient in (4.1) is negative,
`C0(mu)->+infinity` as `mu->-infinity`, and `C0(mu)->-infinity` as `mu->+infinity`.
Together with (4.2)--(4.5), the intermediate value theorem gives at least one root in each of the three disjoint intervals
`(-infinity,-1)`, `(0,m)`, `(1,+infinity)`. (5.1)
`C0` has degree three, so these three roots exhaust all roots, each interval contains exactly one root, and all three are simple.

Let the middle root be `mu_C`. Then
`0<mu_C<m<1`. (5.2)
Consequently `mu_C` is the unique root of `C0` in `[-1,1]`, and continuity plus the absence of any other in-interval root gives
`C0(mu)<0` for `-1<=mu<mu_C`,
`C0(mu)>0` for `mu_C<mu<=1`. (5.3)

## 6. Inputs actually used
For B1 root placement, the proof uses positivity of `m`, `m<1`, and `lambda^2<1/2` (the latter only for the convenient sign proof at `mu=-1`; `lambda^2<1` is otherwise sufficient where stated).
For C0 root placement, it uses `0<m<1` and `0<lambda^2<1`.
No decimal value, rational enclosure, sampled sign, or numerically chosen split point is used.

## 7. Relation to c(mu) roots
The previously proved c-lemma supplies only
`mu_c^-<0<mu_c^+`. (7.1)
This artifact also proves
`mu_B^-<0<mu_C<m`. (7.2)
No ordering between `mu_B^-` and `mu_c^-`, between `mu_c^+` and `mu_C`, or any other additional c/B1/C0 root ordering is asserted here.
Such an ordering may be added only after an exact sign evaluation at a defining root or an equivalent exact algebraic proof.

## 8. Structural consequence for E — not a partition
Recall `E=m b^2+C0(mu)` with `m>0`.
If `mu>mu_C`, then `C0(mu)>0`, hence `E>0` for every allowed `b` except that no endpoint equality arises here because `C0>0` strictly. (8.1)
If `mu<mu_C`, then `C0(mu)<0`, and the sign of E depends on the exact derived threshold
`b^2=-C0(mu)/m` whenever that threshold lies in the allowed b-range. (8.2)
This observation is not a selected proof partition and no enclosure is attached to it.

## 9. Endpoint m=1
The present lemma assumes `rho>0`, equivalently `m<1`.
At `m=1`, endpoint signs used above can become equalities and `C0` has a factor `(mu-1)`; that endpoint is deliberately not absorbed into this root-placement proof.
It remains under the separate endpoint-continuation / NP-T side of the frozen design.

## 10. Audit contract 10–12 ledger
10. Coefficient forms and endpoint values are explicit in Sections 2--4.
11. Root counts and placements use only IVT, degree, and the exact inequalities recorded in Section 6; no enclosure or sampling occurs.
12. No additional ordering versus `mu_c^+/-` is claimed; therefore no unproved root-order relation is used.

**Operational status:** C0/B1 EXACT ROOT STRUCTURE DRAFT / AWAITING CHAT AUDIT / ENCLOSURE FORBIDDEN AND ABSENT / PROOF PARTITION NOT CHOSEN / ORDERING VS mu_c^+/- UNDETERMINED / m=1 ENDPOINT SEPARATE / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
