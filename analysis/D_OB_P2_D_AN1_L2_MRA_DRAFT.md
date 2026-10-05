# D-OB P2 — D-AN-1 L2 Minimum Requirement Analysis (L2-MRA) — DRAFT

**Status:** PAPER-PROOF DRAFT / NOT A THEOREM / AWAITING CHAT AUDIT
**Parent freeze:** `analysis/D_OB_P2_D_AN1_PREDECLARE.md`, commit `a262496a75467e2506beda3ad5443abe0508a78c`, SHA-256 `f65150f72af95fd4061ee8f15d1a72893bf0bceed142e18c005b8e186c32baac`
**L0:** AUDIT PASS, commit `3cabe008b95ed7f81597a45f74303a5b7c53907f`, SHA-256 `41b6be56e6e81f6b0f90e155865f9fc9fcd75129215cfd5df8be6845755c639e`
**Scope:** minimum assumptions actually consumed by L2/L3 at the north-pole anchor `(rho,z)=(0,lambda)`, `lambda in [2/5,93/200]`. No diagnostic value is used.

## §1 Pinned analytic sources

### P1 design note

Commit `6c6282a8`; file `analysis/D_OB_P1_DESIGN_NOTE.md`; SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`.

The following source statements are reproduced verbatim.

> **Lemma V.** For a multi-index `|beta| <= 2` and `p` in `closure(K)`, put
>
> `E_beta(p) := (1/(4 pi lambda)) integral_{bd K \ {p}} partial_p^beta F(x, p) dA(x)/w(x).`
>
> Then: (a) the integral converges absolutely for every `p` in `closure(K)`; (b) `E` is `C^2` on `int K` with `partial^beta E = E_beta` there; (c) each `E_beta` is continuous on `closure(K)`.

> **Lemma 6.1.** (i) `E(-rho, z) = E(rho, z)`, and `E_rho(0, z) = 0` for `|z| <= lambda`. (ii) For `(rho, z)` in `M_lambda` with `rho > 0`, `E_rho(rho, z) = integral_0^rho E_rhorho(s, z) ds`. (iii) `H(rho, z) := integral_0^1 E_rhorho(tau rho, z) dtau` is continuous on `M_lambda`, satisfies `H = E_rho/rho` for `rho > 0`, and `H(0, z) = E_rhorho(0, z)`.

### Endpoint C1 lemma

Commit `aefa8ed24f257694d5b1e349ef7478b9c1e5b807`; file `analysis/OBLATE_ENDPOINT_C1_LEMMA.md`; SHA-256 `74e7dfe253e9f196e7f0ab583527962a4bb808cb77d5b54f449a9acef780e4f6`.

Its general scope statement is, verbatim:

> **Scope.** `t` in `[1/2, 1)` and `lambda` in `I = [lambda_-, lambda_+]` with `0 < lambda_- <= lambda_+ < 1/sqrt 2`. For the band, `I = [5/8, 33/50]`.

Thus `I=[2/5,93/200]` is an admissible instance because `0 < 2/5 <= 93/200 < 1/sqrt 2`.

The endpoint statement potentially relevant to an anchor is, verbatim:

> **Lemma 5.** For `lambda` in `I`, `lim_{t->1-} g_axis_ob(t,lambda)` exists and equals `integral_0^{sqrt 2} F_ob(s,lambda) ds`. Defining `B_ob(lambda)` as this limit and `g_axis_ob(1,lambda) := B_ob(lambda)`, the function `g_axis_ob(·,lambda)` is continuous on `[1/2,1]`.

The source also explicitly states, verbatim:

> Not claimed: the sign of any integral; the identification of the zero of `B_ob` with the boundary passage of the interior axial branch (condition (ii) of the receipt); any statement for `t < 1/2` or `lambda` outside `I`.

### Band C2 interchange lemma — domain-gap record only

Commit `f66ffe5a`; file `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA_31_32.md`; SHA-256 `74cac5be71bcc6f003c15693c8bc6ae737dc0dcd5ed98791c341af71a13b17c7`.

Its proposition begins, verbatim:

> **Proposition.** For `lambda` in `[5/8,33/50]`:

and concerns `partial_t g_axis_ob` on `t in [31/32,1)` plus its one-sided endpoint derivative. Its lambda domain is disjoint from `[2/5,93/200]`; it is therefore not an admissible premise for D-AN-1. The question below is whether D-AN-1 needs any theorem of this type at all.

## §2 MRA-1 — minimum requirements, separated by role

Only facts consumed by frozen L2/L3 are listed.

### Regularity requirements

**R1. Closure second-derivative regularity.** `E_rhorho` must be defined on the closed meridional domain through the north-pole point `(0,lambda)` and continuous there, uniformly enough in the spatial variables for the fixed-`lambda` L2/L3 limit to use its boundary value.

**R2. Axis value of H without an extra interchange.** `H` must extend continuously to `rho=0` and satisfy

`H(0,z)=E_rhorho(0,z)`, in particular `H(0,lambda)=E_rhorho(0,lambda)`.

This is the exact equality consumed when the paired/off-axis expression is closed at the axis. No `t`-derivative of `g_axis_ob` is requested by this requirement.

**R3. Paired full-azimuth representation compatibility.** The L2 derivation must rewrite the pinned full-azimuth `K_H` integral as an integral on a half azimuth with the `phi` and `phi+pi` terms paired, preserve absolute integrability, and have the same continuous `rho->0` value supplied by R2.

### Sign requirement

**S1. North-pole transverse sign.** For every `lambda in [2/5,93/200]`,

`H(0,lambda)=E_rhorho(0,lambda) > 0`.

This is the minimum anchor sign required by frozen L3 step 6 to extend strict positivity to the closed corner. A numerical margin, an explicit uniform constant, or a sign for `partial_t g_axis_ob(1-,lambda)` is not required by MRA unless the later paper proof of L3 proves that compactness/continuity alone is insufficient. No such stronger requirement is pre-imposed here.

## §3 MRA-2 — disposition of every requirement

### R1 -> disposition (a): Lemma V (b)(c), directly

Lemma V(b) identifies the second derivatives in the interior and Lemma V(c) continuously extends every `E_beta`, `|beta|<=2`, to `closure(K)`. Taking `beta=(2,0,0)` gives the required `E_rhorho` closure value. No C2 axial interchange lemma is used.

### R2 -> disposition (b): Lemma 6.1(iii), directly

The exact statement `H(0,z)=E_rhorho(0,z)` is already part of Lemma 6.1(iii), together with continuity of `H` on `M_lambda`. Therefore **no additional exchange of a `t` derivative with an integral is required to obtain R2**. The exchange work in `f66ffe5a` concerns `partial_t g_axis_ob` and is not the exchange used in the definition/axis extension of D-side `H`.

### R3 -> disposition (d): internal to L2 paired derivation

R3 is not inherited as a theorem. It must be derived in L2 from the pinned `K_H` surface integral by splitting `[0,2pi)` into `[0,pi)` and `[pi,2pi)`, substituting `phi'=phi-pi` in the second half, and explicitly combining the two kernel values. Absolute integrability must be inherited from the pinned `K_H` integrability rather than postulated anew.

### S1 -> disposition (e): RESIDUE

Neither Lemma V nor Lemma 6.1 asserts a sign for `E_rhorho(0,lambda)`. The endpoint C1 lemma does not discharge S1: it supplies existence/continuity of the **axial first-derivative endpoint quantity** `g_axis_ob(1,lambda)=B_ob(lambda)` and explicitly claims no sign of any integral. The band C2 interchange lemma concerns the **axial second-t derivative** `partial_t g_axis_ob(1-,lambda)` and, independently, has the wrong lambda domain.

The center-axis coefficient `H_axis_ob(lambda)=partial_t g_axis_ob(0,lambda)` found elsewhere in the C lineage is also not S1: it is an axial coefficient at the center `t=0`, whereas S1 is the transverse Hessian component `E_rhorho` at the north-pole boundary point `(rho,z)=(0,lambda)`. No identification between these quantities is assumed.

Thus S1 is a genuine analytic residue.

## §4 MRA-3 — residue and exact candidate lemma

The RESIDUE set is nonempty and contains exactly S1 at this stage. Accordingly, D-AN-1 cannot conclude that all C-axis premises are already discharged.

However, the analysis **does conclude that the C2 interchange lemma `f66ffe5a` is not required by L2 regularity or by the identity `H(0,z)=E_rhorho(0,z)`**. Its domain gap therefore does not itself create a new D-AN-1 lemma obligation. It is retained above only as the audited record of why it is excluded from the L2 premise list.

The minimal new analytic candidate is:

**Candidate Lemma NP-T (north-pole transverse positivity).** For the oblate family `K_lambda` and the energy `E` defined in the pinned P1 design note, conditional on the audited Lemma V bundle, for every `lambda in [2/5,93/200]`, the continuous boundary value of the transverse second derivative satisfies

`E_rhorho(0,lambda) > 0`.

Equivalently by P1 Lemma 6.1(iii),

`H(0,lambda) > 0`.

The candidate claims no explicit margin and no sign of `g_axis_ob(1,lambda)`, `partial_t g_axis_ob(1-,lambda)`, or the center coefficient `H_axis_ob(lambda)`.

This candidate must be sent to the A/B Judge before being inserted as a proved premise. MRA does not prove NP-T.

## §5 Consequence for the L2 premise list

Subject to chat audit of this MRA, the minimal L2 premise list is:

1. Lemma V(b)(c), pinned above, for closure `C2` regularity of `E` and `E_rhorho`;
2. Lemma 6.1(i)-(iii), pinned above, for rho symmetry, continuous `H`, and the exact axis identity;
3. the pinned P1 `K_H` definition/properties already frozen in D-AN-1 §2.4, from which L2 must derive the `phi -> phi+pi` pairing;
4. NP-T, **RESIDUE / NOT YET PROVED**, solely for the north-pole transverse sign consumed by L3 step 6.

The endpoint C1 lemma `aefa8ed2` is not needed to establish R1-R3 or S1 as presently formulated; its domain admissibility has nevertheless been checked because the frozen predeclare named C-axis premises. The C2 interchange lemma `f66ffe5a` is excluded as unnecessary and domain-inapplicable.

If the MRA is accepted, the next-version wording should replace the imprecise frozen phrase `C-axis C1/C2 lemmas` by `C-axis premises as enumerated in L2-MRA`. This is a precision/shrinking correction, not an expansion of the frozen theorem target.

## §6 MRA-4 — status and evidence boundary

This MRA is a PAPER-PROOF construction and NOT A THEOREM. It uses no Phase 0, N7, B44 or other diagnostic value to infer S1. No observed positive sign is evidence for NP-T. No interval computation is authorized. If NP-T requires interval constants, D-AN-1 §5 requires a separately predeclared G-numbered computation with pre-ignition countersign.
