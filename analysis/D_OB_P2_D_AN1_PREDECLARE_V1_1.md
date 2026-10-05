# D-OB P2 — D-AN-1 Near-column H>0 Analytic Predeclare v1.1

**Status:** v1.1 DRAFT / AWAITING CHAT FULL-DIFF AUDIT / NOT FROZEN
**Evidence class:** ANALYTIC DESIGN / NOT A THEOREM
**Execution:** NOT AUTHORIZED

## §0. Identity, parent, and inherited ledger

This v1.1 draft supersedes the frozen v1 predeclare for future D-AN-1 proof work. Frozen v1 remains immutable pinned history: `analysis/D_OB_P2_D_AN1_PREDECLARE.md`, commit `a262496a75467e2506beda3ad5443abe0508a78c`, SHA-256 `f65150f72af95fd4061ee8f15d1a72893bf0bceed142e18c005b8e186c32baac`. Supersession changes no historical status or bytes of v1.

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

### L2 — paired representation, rho-even extension, and C-axis anchor

Deliverable: establish the paired `phi -> phi+pi` representation used by D-AN-1; preserve the inherited rho symmetry/continuous H extension; connect `H(0,z)=E_rhorho(0,z)` to the C-axis premises as enumerated in the normative L2-MRA annex. Dependencies: §2.2–§2.5 and the L2-MRA premise enumeration. No diagnostic value may serve as the axis margin.

### NP-T — north-pole transverse positivity

**Candidate Lemma NP-T (north-pole transverse positivity).** For the oblate family `K_lambda` and the energy `E` defined in the pinned P1 design note, conditional on the audited Lemma V bundle, for every `lambda in [2/5,93/200]`, the continuous boundary value of the transverse second derivative satisfies

`E_rhorho(0,lambda) > 0`.

Equivalently by P1 Lemma 6.1(iii),

`H(0,lambda) > 0`.

The candidate claims no explicit margin and no sign of `g_axis_ob(1,lambda)`, `partial_t g_axis_ob(1-,lambda)`, or the center coefficient `H_axis_ob(lambda)`.

NP-T is an **internal D-AN-1 proof obligation**, not an external condition of T1. Dependencies: §2 premises (Lemma V and Lemma 6.1); the proof may optionally use L2's paired representation, but that route is not frozen. A direct proof from Lemma V's `E_beta` surface-integral representation at `p=(0,lambda)` and a proof through the paired-kernel `rho -> 0` limit are both admissible.

### L3 — boundary layer and closed-corner extension

Deliverable, in the frozen 09-22 derivation order:

1. uniform oblate boundary-layer bounds;
2. `D`/`h` comparison through Lemma V architecture;
3. bounds for `gamma_rho` and `gamma_rhorho`;
4. a uniform `L1` majorant for `P_rhorho` / the paired H kernel;
5. justified limit/interchange;
6. strictly positive extension to the closed corner, including `(0,lambda)`.

Dependencies: L0, L2, NP-T, Lemma V bundle, and the boundary-layer premises explicitly stated in the eventual proof.

### Frozen DAG

`P1/Lemma-V bundle -> L2 -> L3`

`P1/Lemma-V + Lemma-6.1 -> NP-T -> L3`

`L2 -> NP-T` is an **optional proof route**, not a required dependency edge.

`definitions -> L0 -> L1`

`L0 -> L3`

`L0 + L1 + L2 + NP-T + L3 -> T1`

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

D-AN-1 may be declared CLOSED only when T1's complete lemma chain L0–L3 is assembled on paper, every assumption/dependency is explicit, and chat full-proof audit passes. External Lemma V audit dependency must remain visible; if still pending, any closure language must remain conditional rather than silently upgrading T1 to an unconditional theorem.

For v1.1, the frozen DAG defines that complete chain as including the internal NP-T node before L3/T1 assembly; this sentence adds no new closure criterion beyond the DAG.

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
- If NP-T cannot be established, record the failure and STOP. There is no same-version rescue: a new-version Judge must choose among **(A)** revised analytic continuation, **(B)** analytic excision plus a separately predeclared certified numerical band, or **(C)** lambda-range restriction.
- If uniformity at the `(0,lambda)` closed corner fails, there is no same-version rescue. A new-version Judge must choose among: **(A)** revised analytic continuation, **(B)** analytic excision plus a separately predeclared certified numerical band, or **(C)** lambda-range restriction.
- If a proof step needs a diagnostic-derived partition/threshold, STOP and version-up before using it.
- If the `0,0,3` band becomes necessary, STOP: that is D-AN-2 scope.
- Pin mismatch or uncertainty about an inherited lemma's audited status is fail-closed.

## §7. Freeze boundary

This DRAFT authorizes no proof computation and no certification run. Freeze requires chat full-diff/full-text audit and explicit FREEZE countersign. At freeze, the following become fixed: §0 identity/pins and dependency status; §1 Sigma and D-AN-2 exclusion; §2 inherited source statements/assumptions; §3 lemma targets including NP-T and DAG; §4 T1/T2 status; §5 proof/diagnostic boundary; §6 governance/fail paths.

Proof text may evolve after freeze only within those frozen targets. A change to target domain, lemma dependency, theorem statement, decomposition architecture, diagnostic use, or fallback route requires a version-up and renewed audit before continuation.

## §CHANGES — complete v1 -> v1.1 change ledger

1. **Version identity / supersession.** The title/status identify v1.1; frozen v1 is pinned and declared immutable superseded history.
2. **Pending-bundle wording precision.** The historical bundle wording is expanded to `six-lemma audit bundle (including Lemma V and the C-axis C1/C2 lemmas)`. T1's external condition is narrowed to audited Lemma V.
3. **Normative L2-MRA annex.** Commit `4e60b1ed…`, SHA `7e033737…`, AUDIT PASS, is pinned as the canonical enumeration of C-axis premises; the old generic `C-axis C1/C2 lemmas` requirement is replaced by that enumeration.
4. **Audit carry-forward.** L0 AUDIT PASS and L2-MRA AUDIT PASS are explicitly carried forward because Sigma/L0 and the pinned MRA analysis are unchanged.
5. **L2 precision.** Its C-axis clause now points to the normative L2-MRA premise enumeration rather than generically requiring C1/C2 lemmas. Its paired-representation and no-diagnostic-margin obligations are unchanged.
6. **NP-T node added.** The MRA §4 candidate lemma statement and its no-margin/no-`g_axis_ob`/no-`partial_t g_axis_ob`/no-`H_axis_ob` sign limitation are adopted verbatim. NP-T is an internal proof obligation. Its required dependencies are Lemma V and Lemma 6.1; L2 pairing is an optional proof route, so direct `E_beta` and paired-limit proofs remain admissible.
7. **L3 dependency enlarged only by the new internal obligation.** L3 now depends on NP-T because frozen step 6 consumes the north-pole transverse sign. The six frozen L3 deliverable steps themselves are unchanged.
8. **DAG/T1 assembly.** T1 assembly is now `L0 + L1 + L2 + NP-T + L3`. No proof route inside NP-T is frozen.
9. **T1 condition narrowed.** The theorem target is conditional on audited Lemma V only; C-axis premise bookkeeping is governed by L2-MRA and NP-T is to be proved internally rather than assumed externally. The quantified Sigma statement is unchanged.
10. **Closure interpretation.** The original §5 closure sentence is byte-preserved; an added sentence records that the v1.1 DAG places NP-T inside the complete chain. All diagnostic/partition/G-number computation restrictions are unchanged.
11. **NP-T fail path.** Failure of NP-T is fail-closed and requires STOP plus a new-version Judge choosing pillar-3 route (A), (B), or (C); same-version rescue remains forbidden.
12. **Freeze boundary.** §7 explicitly includes NP-T among frozen lemma targets and changes the required audit wording from full-text to full-diff/full-text for this version-up.
13. **Verbatim-preserved frozen material.** §1 Sigma/natural-domain/D-AN-2 exclusion; L0 target; L1 target; the six numbered L3 deliverables; T2 reservation; D-P2 handoff; the original §5 closure/diagnostic/computation text; §6 seven governance rules and all pre-existing fail paths are byte-for-byte inherited from v1. v1.1 additions are separate sentences/items rather than rewrites of those preserved clauses.
