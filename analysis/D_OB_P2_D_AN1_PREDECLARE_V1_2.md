# D-OB P2 — D-AN-1 Near-column H>0 Analytic Predeclare v1.2

**Status:** v1.2 DRAFT / AWAITING CHAT FULL-DIFF AUDIT / NOT FROZEN
**Evidence class:** ANALYTIC DESIGN / NOT A THEOREM
**Execution:** NOT AUTHORIZED

## §0. Identity, parent, and inherited ledger

This v1.2 draft supersedes frozen v1.1 for future D-AN-1 proof work. Frozen v1.1 remains immutable pinned history: `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_1.md`, commit `6de8a178b3f9c278952ac68590f97f3f100ed9f9`, SHA-256 `1461fc081c99cfd820792248bc2f6fe2401a182a8a4941df46a4288f49f8cc78`. Supersession changes no historical status or bytes of v1.1.

Earlier frozen v1 likewise remains immutable pinned history: `analysis/D_OB_P2_D_AN1_PREDECLARE.md`, commit `a262496a75467e2506beda3ad5443abe0508a78c`, SHA-256 `f65150f72af95fd4061ee8f15d1a72893bf0bceed142e18c005b8e186c32baac`.

Normative L3 minimum-requirement annex: `analysis/D_OB_P2_D_AN1_L3_MRA_DRAFT.md`, commit `5fc0341216f4e0f6722a96f3d8edb2e1c9fbc47c`, SHA-256 `b13e07d63b3f3035b7b983cc39acbae893d4a184dfa030eaf73bb9f243a0d842`, **AUDIT PASS**. It exposes the quantitative residues FT_q and QM required for a constructive boundary-layer width.

Parent kick-off: `analysis/D_OB_P2_D_PROBLEM_TRACK_KICKOFF_REV2_DRAFT.md`, SHA-256 `462f7ffa116f36289fd720542dc2019c301c1f3c9d6e96a7e35e87a418190a5d`, countersigned by chat. D-AN-1 is a new analytic predeclare; it does not resume historical P-numbers.

P1 design source: commit `6c6282a8`, file SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`. P1 is CLOSED with diagnostic adjudication Q1 YES(+) / Q2 NO, selecting `H>0` through `K_H` as the analytic target; result commit `eff18894`.

Inherited diagnostic pins: true Phase 0 instrument `phase0_b44_sign.py` SHA `7268ee90…` and `run_phase0_g7.sh` SHA `eb302334…` at basepoint-geometry `bb2bdbd5…`; mathematical source SHA `2dcd16673c214369ba0555e653dae51fca7d3f3cf13c83aeac4fd000d5bfccd7`. N7 input `ea166df49d8d0486fe836088fdbc13acbd0154811c882ae98b2a3f92275a8b9c` has diagnostic Route-B H in `[1.163983,1.24974]`; B44 result `361db4a7c5fbe3bc6c8afc335282af8b26a1bf653dd5edf1dde56d08e634b4e0` has 44/44 POSITIVE and H in `[1.0772846,1.1923643]`. These are separate diagnostic sets and are not merged into a proof margin.

Candidate-comparison etiology inherited as design input only: the B band is unchanged by the tested resource/depth/RHO0 mechanisms; budget helps the N/enclosure-width band but does not close D-P2. Candidate-comparison chapter is CLOSED with zero adoption. D-P2 remains NOT_CERTIFIED.

Governance note: the historical **six-lemma audit bundle (including Lemma V and the C-axis C1/C2 lemmas)** remains externally pending. Following the audited L2-MRA below, T1's external condition is narrowed to the **audited Lemma V** dependency; C-axis requirements are governed instead by the minimal premise enumeration in L2-MRA, and NP-T is an internal D-AN-1 proof obligation rather than an external theorem condition.

Normative premise annex: `analysis/D_OB_P2_D_AN1_L2_MRA_DRAFT.md`, commit `4e60b1ed32f862455450d38af6a5e440c64aa3ec`, SHA-256 `7e0337379bff33ef3ba63e71069287cb849aad9de688c466775ef68f31cb3185`, **AUDIT PASS**. It is the canonical enumeration of the C-axis premises actually required by L2/L3. The earlier C-axis C1/C2 wording is superseded by **C-axis premises as enumerated in L2-MRA**.

L0 remains **AUDIT PASS** at commit `3cabe008b95ed7f81597a45f74303a5b7c53907f`, SHA-256 `41b6be56e6e81f6b0f90e155865f9fc9fcd75129215cfd5df8be6845755c639e`. Because v1.1 changes neither Sigma nor the L0 target, that audit carries forward. The L2-MRA audit likewise carries forward because its pinned premise analysis is made normative here without alteration.

## §1. Target domain: double definition

### §1.1 Certification-demand domain Σ

For

`lambda in [2/5,93/200]`, `r in [7/8,1]`, `tau in [7/8,1]`,

define

`rho = r (1-tau^2)/(1+tau^2)`,

`z = lambda r 2 tau/(1+tau^2)`.

The certification-demand image is

`Sigma := { (rho,z;lambda) obtained from the above closed rational box }`.

The `rho=0` boundary is included by the even-extension limit supplied by the inherited H regularity. Put `delta=1-r^2`; then `delta in [0,15/64]`. This includes the pole/corner boundary layer relevant to the `7,7,0` near-column unresolved region.

### §1.2 Analytic natural domain

The proof may work on a natural analytic superset `S_AN` (for example a boundary-layer sector) provided that it is fixed analytically and contains Sigma. A required D-AN-1 deliverable is a **coverage lemma `Sigma subset S_AN` proved by rational inequalities** from the pinned parameter ranges. Numerical sampling, floating containment, or post-hoc enlargement does not satisfy this requirement.

The `0,0,3` band, with `lambda in [0.595,0.66]` near the upper central endpoint and a distinct thin-margin mechanism, is **out of scope for D-AN-1** and explicitly deferred to **D-AN-2**. D-AN-1 may not silently enlarge its scope to absorb that band.

## §2. Inherited analytic assumptions and exact source statements

The following source statements are reproduced verbatim from P1 design note commit `6c6282a8`, SHA `2c304ee6…`. Their use in T1 remains conditional on completion of the external six-lemma audit bundle including Lemma V.

### §2.1 Directional sign/size premise — verbatim

> **Lemma 3.1 (sign and size of `h`).** For `p` in `closure(K)` and `x` in `bd K`, `0 <= h(x,p) <= w(x) D`. If `p` in `int K`, then `h > 0`.

### §2.2 Lemma V — verbatim

> **Lemma V.** For a multi-index `|beta| <= 2` and `p` in `closure(K)`, put
>
> `E_beta(p) := (1/(4 pi lambda)) integral_{bd K \ {p}} partial_p^beta F(x, p) dA(x)/w(x).`
>
> Then: (a) the integral converges absolutely for every `p` in `closure(K)`; (b) `E` is `C^2` on `int K` with `partial^beta E = E_beta` there; (c) each `E_beta` is continuous on `closure(K)`.

The inherited proof architecture uses `h <= wD`, the second-derivative `1/D` domination, and convex area growth; curvature bounds are not required. This explanatory sentence is not a replacement for the verbatim assumptions above.

### §2.3 H extension and axis anchor — verbatim

> **Lemma 6.1.** (i) `E(-rho, z) = E(rho, z)`, and `E_rho(0, z) = 0` for `|z| <= lambda`. (ii) For `(rho, z)` in `M_lambda` with `rho > 0`, `E_rho(rho, z) = integral_0^rho E_rhorho(s, z) ds`. (iii) `H(rho, z) := integral_0^1 E_rhorho(tau rho, z) dtau` is continuous on `M_lambda`, satisfies `H = E_rho/rho` for `rho > 0`, and `H(0, z) = E_rhorho(0, z)`.

### §2.4 Paired K_H — verbatim source definition/properties

> `H(rho, z)        = (1/(4 pi lambda)) integral integral K_H dphi dmu,`
>
> `K_H(rho, z; mu, phi) := [ F_rho(rho, b) - F_rho(-rho, b) ] / (2 rho)   (rho > 0),`
>
> `K_H(0, z; mu, phi)   := F_rhorho(0, b),`

and, verbatim from the source properties:

> `(i) since E_rho is odd in rho, (1/(4 pi lambda)) integral integral K_H = [E_rho(rho, z) - E_rho(-rho, z)]/(2 rho) = H(rho, z); (ii) K_H(rho) = (1/(2 rho)) integral_{-rho}^{rho} F_rhorho(s, b) ds;`

The D-AN-1 proof design may additionally pair azimuthal terms under `phi -> phi + pi`; that pairing must be derived explicitly from the pinned kernel rather than treated as an extra inherited theorem.

### §2.5 Interior analytic layer

On compact subsets of `int K`, `D` is bounded below and the P1 note establishes smooth differentiation under the integral. The apparent `u=1-gamma^2=0` locus is not a density singularity because the angle functions extend real-analytically across `gamma=1`. D-AN-1 may use this internal non-singular compact layer; **real-analyticity of E itself is not assumed or claimed**.

## §3. Frozen lemma targets and dependency DAG

Only lemma **targets and dependencies** are frozen here. Proofs, constants, algebraic rearrangements and admissible analytic techniques are not frozen, except where another section explicitly imposes a governance restriction.

### L0 — rational coverage

Deliverable: define the analytic natural domain `S_AN` and prove `Sigma subset S_AN` by rational inequalities using §1.1. Dependencies: none beyond definitions.

### L1 — interior compact positivity

Deliverable: prove the required positive lower sign for the paired-H representation on the interior compact layer `S_int subset S_AN`, with all hypotheses explicit and without importing diagnostic margins. Dependencies: L0 and §2 interior regularity/kernel premises.


### v1.2 L1 positioning note

After L3 proves `delta0`, the concrete compact `Sigma intersect {delta in [delta0,15/64]}` is the L1 target instance. This is a concrete instance of the byte-preserved frozen L1 target, not a rewrite of that target. Existing G2 material is preserved. Whether L1 closes analytically or proceeds through a separately predeclared G-numbered interval proof is decided only after `delta0` is proved; no diagnostic value may choose the split.

### L2 — paired representation, rho-even extension, and C-axis anchor

Deliverable: establish the paired `phi -> phi+pi` representation used by D-AN-1; preserve the inherited rho symmetry/continuous H extension; connect `H(0,z)=E_rhorho(0,z)` to the C-axis premises as enumerated in the normative L2-MRA annex. Dependencies: §2.2–§2.5 and the L2-MRA premise enumeration. No diagnostic value may serve as the axis margin.

### NP-T — north-pole transverse positivity

**Candidate Lemma NP-T (north-pole transverse positivity).** For the oblate family `K_lambda` and the energy `E` defined in the pinned P1 design note, conditional on the audited Lemma V bundle, for every `lambda in [2/5,93/200]`, the continuous boundary value of the transverse second derivative satisfies

`E_rhorho(0,lambda) > 0`.

Equivalently by P1 Lemma 6.1(iii),

`H(0,lambda) > 0`.

The candidate claims no explicit margin and no sign of `g_axis_ob(1,lambda)`, `partial_t g_axis_ob(1-,lambda)`, or the center coefficient `H_axis_ob(lambda)`.

NP-T is an **internal D-AN-1 proof obligation**, not an external condition of T1. Dependencies: §2 premises (Lemma V and Lemma 6.1); the proof may optionally use L2's paired representation, but that route is not frozen. A direct proof from Lemma V's `E_beta` surface-integral representation at `p=(0,lambda)` and a proof through the paired-kernel `rho -> 0` limit are both admissible.

### FT_q — quantitative boundary-face positivity

A new internal node must prove an explicit rational constant m0>0, uniform in lambda and tau, such that

`H(rho_b,z_b;lambda) >= m0`

for all `lambda in [2/5,93/200]`, `tau in [7/8,1]`, where

`rho_b=(1-tau^2)/(1+tau^2)`,  `z_b=lambda*2tau/(1+tau^2)`.

FT_q claims no sign outside this face. It contains the NP-T endpoint `tau=1` and is stronger there, but it does not modify the NP-T statement.

Dependencies: Lemma V and Lemma 6.1. L2 and the NP-T method are optional proof routes only. The proof route is not frozen.

### QM — quantitative modulus

A second internal node must provide an explicit modulus `omega_E:[0,infinity)->[0,infinity)` for `E_rhorho`, **uniform in `lambda in [2/5,93/200]`**, on a closed region containing every swept segment point `{(t rho,z):0<=t<=1}` arising from every point of Sigma, including its boundary face. The modulus must satisfy `omega_E(0)=0`, be continuous at 0, be nondecreasing, and satisfy

`|E_rhorho(p)-E_rhorho(p')| <= omega_E(|p-p'|)`

for all relevant `p,p'` in that region. No exponent or asymptotic form for `omega_E` is frozen.

Node note: by Lemma 6.1(i), `E_rho` is odd in rho and `E_rho(0,z)=0`; by the fundamental theorem of calculus, justified by Lemma V(c),

`E_rho(rho,z)=integral_0^rho E_rhorho(s,z) ds`,

hence

`H(rho,z)=integral_0^1 E_rhorho(t rho,z) dt`.

Therefore `|(t rho,z)-(t rho',z')| <= |(rho,z)-(rho',z')|` implies that the same `omega_E` controls the corresponding H difference. A K_H-specific modulus is not required.

Dependencies: Lemma V(c) and Lemma 6.1.

### L3 — boundary layer and closed-corner extension

Deliverable, in the frozen 09-22 derivation order:

1. uniform oblate boundary-layer bounds;
2. `D`/`h` comparison through Lemma V architecture;
3. bounds for `gamma_rho` and `gamma_rhorho`;
4. a uniform `L1` majorant for `P_rhorho` / the paired H kernel;
5. justified limit/interchange;
6. strictly positive extension to the closed corner, including `(0,lambda)`.

Dependencies: L0, L2, FT_q, QM, Lemma V bundle, and the boundary-layer premises explicitly stated in the eventual proof. The edge NP-T -> L3 is optional; NP-T is retained as an independent analytic cross-check.

In addition to the six byte-preserved stages above, L3 must produce an explicit rational `delta0>0` satisfying `omega_E(delta0) < m0`, using proved constants only and never diagnostic values. With `p_in=r p_boundary`, `r=sqrt(1-delta)`, one has `|p_in-p_boundary| <= delta`; monotonicity of `omega_E` then gives strict positivity throughout `delta in [0,delta0]`.

### Frozen DAG

`P1/Lemma-V bundle -> L2 -> L3`

`P1/Lemma-V + Lemma-6.1 -> NP-T`

`L2 -> NP-T` is an **optional proof route**, not a required dependency edge.

`P1/Lemma-V + Lemma-6.1 -> FT_q -> L3`

`L2 -> FT_q` and the NP-T method -> FT_q are **optional proof routes**, not required dependency edges.

`P1/Lemma-V(c) + Lemma-6.1 -> QM -> L3`

`NP-T -> L3` is **optional**. NP-T is retained as an independent analytic cross-check.

`definitions -> L0 -> L1`

`L0 -> L3`

`L0 + L1 + L2 + FT_q + QM + L3 -> T1`

A failed dependency may not be bypassed silently by repartitioning the domain.

## §4. Committed theorem target and reserved target

### T1 — the only committed theorem target

**Conditional T1 (D-AN-1 target).** Conditional on the audited Lemma V, for every `lambda in [2/5,93/200]` and every `(rho,z;lambda) in Sigma`,

`H(rho,z;lambda) > 0`.

No weaker non-negativity statement counts as T1 closure. Any proof on `S_AN` must discharge L0 and then imply the stated Sigma result.

### T2 — reserved, not committed

A future theorem on the full quarter-domain `Q_lambda` for `lambda in [2/5,33/50]` is reserved as **T2 / NOT COMMITTED IN D-AN-1**. Failure or success of D-AN-1 does not silently change T1 into T2 or vice versa.

### D-P2 handoff boundary

D-AN-1 does **not** claim the corollary that the 7,662 numerical unresolved boxes may be removed from D-P2. The theorem-to-D-P2 handoff is a separate audited stage, as fixed in the countersigned kick-off §0.4. No certification consequence is established inside D-AN-1.

## §5. Paper-proof boundary and closure condition

D-AN-1 is a **paper-proof predeclare**. It contains no certification computation.

D-AN-1 may be declared CLOSED only when T1's complete lemma chain L0–L3, including FT_q and QM as required internal nodes, is assembled on paper, every assumption/dependency is explicit, and chat full-proof audit passes. External Lemma V audit dependency must remain visible; if still pending, any closure language must remain conditional rather than silently upgrading T1 to an unconditional theorem.

For v1.2, the frozen DAG defines T1 assembly as `L0 + L1 + L2 + FT_q + QM + L3`; NP-T remains an independent analytic cross-check and its edge into L3 is optional.

During drafting/proof exploration, numerical work is repo-external and `DIAGNOSTIC_ONLY`. Partition tuning from diagnostic outputs is forbidden. A diagnostic may contribute only a predeclared binary feasibility signal; values, margins, worst points, observed transition locations, subdivision counts, precision or thresholds may not choose the proof partition or constants.

If interval computation becomes necessary to establish a lemma constant, that computation is **not authorized by D-AN-1**. It requires a separate G-numbered predeclare with inputs, algorithm, bounds, pins, failure conditions and pre-ignition chat countersign.

## §6. Governance and fail-closed paths

The countersigned kick-off §0.7 discipline is adopted:

1. predeclare before computation;
2. pin source, inputs, configuration and target domain;
3. chat audit and pre-ignition countersign as the default rule;
4. fail closed on pin/domain/identity ambiguity;
5. version-up -> re-audit -> re-freeze for post-result changes;
6. preserve diagnostic/formal-evidence separation;
7. use an audit line independent from the producing line where formal evidence is eventually sought.

Additional D-AN-1 fail paths:

- If L0, L1, L2 or L3 is false or cannot be established under its frozen target, record the failure and STOP. Any decomposition change requires a version-up; silent re-scope/repartition is forbidden.
- If NP-T cannot be established, record the cross-check failure. Because NP-T is not a required T1/L3 dependency in v1.2, this does not by itself invalidate an otherwise complete FT_q + QM + L3 chain; no claim may use the failed cross-check.
- If FT_q cannot be established, record the failure and STOP. There is no same-version rescue: a new-version Judge must choose among **(A)** revised analytic continuation, **(B)** analytic excision plus a separately predeclared certified numerical band, or **(C)** lambda-range restriction.
- If QM cannot be established explicitly under its frozen target, record the failure and STOP. There is no same-version rescue: a new-version Judge must choose among **(A)** revised analytic continuation, **(B)** analytic excision plus a separately predeclared certified numerical band, or **(C)** lambda-range restriction.
- If uniformity at the `(0,lambda)` closed corner fails, there is no same-version rescue. A new-version Judge must choose among: **(A)** revised analytic continuation, **(B)** analytic excision plus a separately predeclared certified numerical band, or **(C)** lambda-range restriction.
- If a proof step needs a diagnostic-derived partition/threshold, STOP and version-up before using it.
- If the `0,0,3` band becomes necessary, STOP: that is D-AN-2 scope.
- Pin mismatch or uncertainty about an inherited lemma's audited status is fail-closed.

## §7. Freeze boundary

This DRAFT authorizes no proof computation and no certification run. Freeze requires chat full-diff/full-text audit and explicit FREEZE countersign. At freeze, the following become fixed: §0 identity/pins and dependency status; §1 Sigma and D-AN-2 exclusion; §2 inherited source statements/assumptions; §3 lemma targets including NP-T, FT_q and QM, the explicit-delta0 requirement, and DAG; §4 T1/T2 status; §5 proof/diagnostic boundary; §6 governance/fail paths.

Proof text may evolve after freeze only within those frozen targets. A change to target domain, lemma dependency, theorem statement, decomposition architecture, diagnostic use, or fallback route requires a version-up and renewed audit before continuation.

## §CHANGES — complete v1.1 -> v1.2 change ledger

1. **Version identity / supersession.** The title/status identify v1.2. Frozen v1.1 is pinned by file, commit `6de8a178...`, and SHA-256 `1461fc08...`, and is declared immutable superseded history; frozen v1 remains immutable earlier history.
2. **L3-MRA annex.** Commit `5fc03412...`, SHA-256 `b13e07d6...`, AUDIT PASS, is pinned as the normative minimum-requirement analysis for the L3 version-up.
3. **Audit carry-forward.** Existing AUDIT PASS status for L0, L2-MRA, L2, and NP-T carries forward; their theorem statements are not rewritten by this version-up.
4. **FT_q added.** L3-MRA §4 quantitative boundary-face positivity is adopted: an explicit rational `m0>0`, uniform in lambda and tau, on exactly the required boundary face, with no sign claim outside it. Lemma V and Lemma 6.1 are required dependencies; L2 and the NP-T method are optional routes. No proof route is frozen.
5. **QM added.** L3-MRA §5 quantitative modulus is adopted, with the additional audited requirement that it be uniform in `lambda in [2/5,93/200]`. Its closed domain contains all swept segments from every Sigma point to the axis; `omega_E` is explicit, nondecreasing, zero and continuous at 0. No exponent/asymptotic form is frozen. The Lemma-6.1/FTC swept representation is recorded as a node note.
6. **L3 dependency and constructive width.** FT_q and QM are required L3 dependencies. NP-T -> L3 is changed from mandatory to optional (Judge choice A); NP-T remains an independent analytic cross-check. L3 must produce an explicit rational `delta0>0` with `omega_E(delta0)<m0` from proved constants only, never diagnostic values, and owns `delta in [0,delta0]`. The six numbered L3 stages are byte-for-byte preserved from v1.1.
7. **L1 positioning.** The frozen L1 target is byte-for-byte preserved. After delta0 is proved, the concrete compact `Sigma intersect {delta in [delta0,15/64]}` is the L1 target instance. Preserved G2 material may be used; the choice between analytic closure and a separately predeclared G-numbered interval proof is deferred until delta0 is known.
8. **T1 assembly.** Required assembly changes from `L0 + L1 + L2 + NP-T + L3` to `L0 + L1 + L2 + FT_q + QM + L3`. NP-T is cross-check only. T1's quantified theorem statement is unchanged.
9. **Fail paths.** FT_q failure and explicit-QM failure each require record -> STOP -> new-version Judge choosing pillar-3 route (A), (B), or (C). NP-T failure is now a cross-check failure and cannot be used as evidence, but is no longer by itself a required-chain STOP.
10. **Procedure.** FT_q and QM proof work is forbidden until this v1.2 draft is committed, full-diff/full-text audited against v1.1, and explicitly FREEZE countersigned. Any interval computation still requires a separate G-numbered predeclare and countersign.
11. **Verbatim-preserved material.** §1 target domain and D-AN-2 exclusion; §2 inherited source statements; L0 target; L1 target; L2 target; NP-T theorem statement; the six numbered L3 stages; T1 theorem statement; T2 reservation; D-P2 handoff; diagnostic/G-number restrictions; and the seven governance rules are inherited from v1.1 except for separately identified version-up sentences above.
