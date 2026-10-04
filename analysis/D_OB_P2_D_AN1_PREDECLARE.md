# D-OB P2 — D-AN-1 Near-column H>0 Analytic Predeclare

**Status:** DRAFT / AWAITING CHAT FULL-TEXT AUDIT / NOT FROZEN
**Evidence class:** ANALYTIC DESIGN / NOT A THEOREM
**Execution:** NOT AUTHORIZED

## §0. Identity, parent, and inherited ledger

Parent kick-off: `analysis/D_OB_P2_D_PROBLEM_TRACK_KICKOFF_REV2_DRAFT.md`, SHA-256 `462f7ffa116f36289fd720542dc2019c301c1f3c9d6e96a7e35e87a418190a5d`, countersigned by chat. D-AN-1 is a new analytic predeclare; it does not resume historical P-numbers.

P1 design source: commit `6c6282a8`, file SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`. P1 is CLOSED with diagnostic adjudication Q1 YES(+) / Q2 NO, selecting `H>0` through `K_H` as the analytic target; result commit `eff18894`.

Inherited diagnostic pins: true Phase 0 instrument `phase0_b44_sign.py` SHA `7268ee90…` and `run_phase0_g7.sh` SHA `eb302334…` at basepoint-geometry `bb2bdbd5…`; mathematical source SHA `2dcd16673c214369ba0555e653dae51fca7d3f3cf13c83aeac4fd000d5bfccd7`. N7 input `ea166df49d8d0486fe836088fdbc13acbd0154811c882ae98b2a3f92275a8b9c` has diagnostic Route-B H in `[1.163983,1.24974]`; B44 result `361db4a7c5fbe3bc6c8afc335282af8b26a1bf653dd5edf1dde56d08e634b4e0` has 44/44 POSITIVE and H in `[1.0772846,1.1923643]`. These are separate diagnostic sets and are not merged into a proof margin.

Candidate-comparison etiology inherited as design input only: the B band is unchanged by the tested resource/depth/RHO0 mechanisms; budget helps the N/enclosure-width band but does not close D-P2. Candidate-comparison chapter is CLOSED with zero adoption. D-P2 remains NOT_CERTIFIED.

Governance note: the historical six-lemma audit bundle **including Lemma V** remains externally pending. Any theorem statement in D-AN-1 is therefore **conditional on the audited Lemma V bundle** until that dependency is discharged.

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

Deliverable: establish the paired `phi -> phi+pi` representation used by D-AN-1; preserve the inherited rho symmetry/continuous H extension; connect `H(0,z)=E_rhorho(0,z)` to the audited C-axis lemma at the `(0,lambda)` anchor with the required C1/C2 regularity hypotheses stated explicitly. Dependencies: §2.2–§2.5. No diagnostic value may serve as the axis margin.

### L3 — boundary layer and closed-corner extension

Deliverable, in the frozen 09-22 derivation order:

1. uniform oblate boundary-layer bounds;
2. `D`/`h` comparison through Lemma V architecture;
3. bounds for `gamma_rho` and `gamma_rhorho`;
4. a uniform `L1` majorant for `P_rhorho` / the paired H kernel;
5. justified limit/interchange;
6. strictly positive extension to the closed corner, including `(0,lambda)`.

Dependencies: L0, L2, Lemma V bundle, and the boundary-layer premises explicitly stated in the eventual proof.

### Frozen DAG

`P1/Lemma-V bundle -> L2 -> L3`

`definitions -> L0 -> L1`

`L0 -> L3`

`L1 + L2 + L3 -> T1`

A failed dependency may not be bypassed silently by repartitioning the domain.

## §4. Committed theorem target and reserved target

### T1 — the only committed theorem target

**Conditional T1 (D-AN-1 target).** Conditional on the audited Lemma V bundle and the explicitly cited inherited C-axis premises, for every `lambda in [2/5,93/200]` and every `(rho,z;lambda) in Sigma`,

`H(rho,z;lambda) > 0`.

No weaker non-negativity statement counts as T1 closure. Any proof on `S_AN` must discharge L0 and then imply the stated Sigma result.

### T2 — reserved, not committed

A future theorem on the full quarter-domain `Q_lambda` for `lambda in [2/5,33/50]` is reserved as **T2 / NOT COMMITTED IN D-AN-1**. Failure or success of D-AN-1 does not silently change T1 into T2 or vice versa.

### D-P2 handoff boundary

D-AN-1 does **not** claim the corollary that the 7,662 numerical unresolved boxes may be removed from D-P2. The theorem-to-D-P2 handoff is a separate audited stage, as fixed in the countersigned kick-off §0.4. No certification consequence is established inside D-AN-1.

## §5. Paper-proof boundary and closure condition

D-AN-1 is a **paper-proof predeclare**. It contains no certification computation.

D-AN-1 may be declared CLOSED only when T1's complete lemma chain L0–L3 is assembled on paper, every assumption/dependency is explicit, and chat full-proof audit passes. External Lemma V audit dependency must remain visible; if still pending, any closure language must remain conditional rather than silently upgrading T1 to an unconditional theorem.

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
- If uniformity at the `(0,lambda)` closed corner fails, there is no same-version rescue. A new-version Judge must choose among: **(A)** revised analytic continuation, **(B)** analytic excision plus a separately predeclared certified numerical band, or **(C)** lambda-range restriction.
- If a proof step needs a diagnostic-derived partition/threshold, STOP and version-up before using it.
- If the `0,0,3` band becomes necessary, STOP: that is D-AN-2 scope.
- Pin mismatch or uncertainty about an inherited lemma's audited status is fail-closed.

## §7. Freeze boundary

This DRAFT authorizes no proof computation and no certification run. Freeze requires chat full-text audit and explicit FREEZE countersign. At freeze, the following become fixed: §0 identity/pins and dependency status; §1 Sigma and D-AN-2 exclusion; §2 inherited source statements/assumptions; §3 lemma targets and DAG; §4 T1/T2 status; §5 proof/diagnostic boundary; §6 governance/fail paths.

Proof text may evolve after freeze only within those frozen targets. A change to target domain, lemma dependency, theorem statement, decomposition architecture, diagnostic use, or fallback route requires a version-up and renewed audit before continuation.
