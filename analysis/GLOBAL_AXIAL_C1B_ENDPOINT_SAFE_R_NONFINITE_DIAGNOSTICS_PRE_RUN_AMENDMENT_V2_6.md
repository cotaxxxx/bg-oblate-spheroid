# C1b Pre-Run Amendment v2.6 — Endpoint-Safe R and Explicit Non-Finite Diagnostics

Status: PREDECLARED / NOT_EVIDENCE / MACHINE_NOT_RUN.
Scope: the R evaluation used by the C1b densities in both lineages, and the non-finite
diagnostics of the tube and exterior stages. Amendments v2 … v2.5.1 remain in force.
No existing shared evaluator function is modified: C0/C1a/C1c/BOB keep their exact source paths
and call sites, so their receipts remain byte-reproducible.

## 0. Canonical control (ABORT of Phase 1, run c1b_producer_20260907T073426Z)

attempt 154, coarse 102, depth 3, λ ∈ [231/400, 3697/6400] (width 1/6400),
t_c = 512497935639/2^39, t₋ = 478138197271/2^39, t₊ = 546857674007/2^39, right_clamp False.
T0/T1/T2 all failed on the right wall with right_worst_upper = NaN; unresolved 4 → 8 → 16;
root was never reached; decision ABORT, reason TUBE; segment_end failure, post_pin_check PASS.
Ledger SHA-256 d85bbc4c…, replay plan SHA-256 88b2fe0e…; both retained unchanged as control.

Isolation. In g_box(t₊, t₊, λ) at 4096 panels (5793 sub-panels), the first non-finite panels are
40–42, s ≈ [0.00977, 0.01050]; these are NOT the moving singularity at s = √2. There
e, d, d², γ, q, √q are all finite with q ≈ 2·10⁻⁴ > 0, so this is NOT the q → 0 mechanism of v2.5.
On panel 40, u = [0.907321643957402557, 1.000000000058207660] and _R_bundle returns
R = Rg = Rgg = Rggg = NaN. The upper bound exceeds 1 by 5.8207660·10⁻¹¹ = 2⁻³⁴ (to 1.6·10⁻⁸
relative). _unit_nonnegative clamps mathematically via min(1, upper) but then rebuilds a ball with
_box(lo, hi); the ball radius is an arb mag with a 30-bit mantissa, and its outward rounding pushes
the reconstructed upper end above 1 (radius 0.04634 × 2⁻³⁰ ≈ 4.3·10⁻¹¹, the observed order).
u > USTAR then selects the direct chart, asin(sqrt(u)) receives an argument set leaving [-1, 1],
and the result is NaN.

Two consequences fix the shape of this amendment:
- The excess comes from the radius representation, not from the working precision. Raising BITS does
  not remove it: the checker at 192 bits has the identical leak. The defect is lineage-independent.
- Subdividing s does not remove it either. Whatever the panel width, some panel attains u = 1, and
  clamping there always produces a reconstructed upper end above 1. Sub-division is therefore
  explicitly NOT a remedy for this class and is not part of this amendment.

The v2.5.1 defence layer behaved correctly: nothing crashed. The NaN was recorded as a failed sign
test and the attempt refined to depth 3 and aborted. That is why the fix must be in the evaluation.

## 1. Cause layer — endpoint-safe R (binding)

R(u) = arcsin(√u)/√u on [0,1] has the power series R(u) = Σ_{n≥0} c_n uⁿ with
c_n = C(2n,n) / (4ⁿ (2n+1)) > 0, hence R is continuous and strictly increasing on [0,1], with
R(0) = 1 and R(1) = π/2. Monotonicity is analytic, not a numerical observation.

A new primitive is added to the shared layer WITHOUT modifying any existing function
(producer side and, transcribed independently, checker side):

    def _R_endpoint_safe(u, stats):            # R only — this is what the g density needs
        # precondition: mathematically u ⊂ [0,1] (as established by the existing
        # _unit_nonnegative clamp). Violations are fail-closed, see below.
        ulo = max(exact 0, u.lower())          # arf endpoints, no ball repacking
        uhi = min(exact 1, u.upper())
        if uhi < ulo: raise REndpointDomainGuard("R_ENDPOINT_EMPTY")
        Rlo = R_point(ulo)
        Rhi = R_point(uhi)
        return _box(Rlo.lower(), Rhi.upper())  # monotone ⇒ this encloses R(u)

    def _R_Rg_endpoint_safe(u, gamma, stats):  # R and Rg — this is what _glam_density needs
        if <legacy chart criterion selects the series branch for u>:
            R, Rg, _, _ = legacy_R_bundle(u, gamma, stats)   # unchanged, incl. moving u = 0
            return R, Rg
        if not u.lower() > 0:
            raise REndpointDomainGuard("R_ENDPOINT_DIRECT_BRANCH_ZERO_DENOMINATOR")
        R  = _R_endpoint_safe(u, stats)
        Rg = (gamma * R - 1) / u               # the existing legacy algebraic relation
        return R, Rg

    def R_point(x):        # x an exact arf in [0,1]
        if x == 0: return arb(1)
        if x == 1: return pi/2                 # evaluated at working precision
        y = sqrt(x)
        if not y.upper() <= 1: raise REndpointDomainGuard("R_ENDPOINT_DOMAIN_GUARD")
        return asin(y) / y

The essential property is that the clamped endpoints are never repacked into a ball before asin:
the endpoints are evaluated as points and only the two results are hulled. The path by which mag
rounding can violate the domain therefore does not exist. The explicit x == 1 case removes the only
value where sqrt(x) could legitimately touch the boundary; the domain guard covers the residual
case 1 − x < 2⁻(BITS−ε) fail-closed rather than silently.

REndpointDomainGuard is a dedicated exception class defined next to the primitive, in each lineage.
It is NEVER caught by a generic `except RuntimeError`: generic capture would hide unrelated program
defects behind an UNRESOLVED verdict. It is caught only at the C1b evaluator boundaries — the tube
stage, the exterior stage (sign test and MONO closure), the root step's g/Gl calls, and the
predictor scan, i.e. every call site that reaches the new primitive — and is converted there into
the non-finite outcome of §2, with kind = "R_ENDPOINT_DOMAIN_GUARD" in the nonfinite record so that
it is distinguishable from a plain Arb NaN. In predictor_scan, any guard or non-finite sample causes
immediate scan termination with no bracket, and the attempt reason is PREDICTOR_NONFINITE; later
samples are not examined and no sign change may be inferred across the failed sample. The resulting semantics is:

    endpoint evaluation not domain-safe
      → not a sign failure, not a crash
      → non-finite / domain-guard enclosure failure, recorded with its kind
      → fail-closed: the box or step stays unresolved
      → REFINE while depth < MAX_DEPTH, ABORT at MAX_DEPTH

Domain-safe evaluability of the endpoint path is therefore a binding condition of this amendment,
and the complementary identity stays a control (§5 C2); it is not promoted into the implementation.

The Rg path is deliberately hybrid. The algebraic relation Rg = (γR − 1)/u divides by u, so it is
usable only away from u = 0; the legacy series branch exists precisely to handle small u and the
moving u = 0 chart, and it is a part of the already certified lineage. This amendment therefore
does NOT touch it: the branch criterion is exactly the legacy one, bit for bit, and only the direct
branch's computation of R is replaced. On the direct branch u is bounded away from 0 by that same
criterion; the explicit u.lower() > 0 test is a fail-closed backstop, not a new chart boundary.
Because R is an enclosure of R(u) and the algebraic relation is the one the legacy bundle already
uses, Rg computed from the new R is a valid enclosure by the same argument as before. No new
monotonicity lemma about Rg, Rgg or Rggg is required, and Rgg/Rggg are not provided by the new
primitives: the legacy bundle keeps them. The g density takes R from _R_endpoint_safe and never
constructs Rg at all.

Adoption is limited to the C1b densities of both lineages:
- the g density used by g_box takes R from the new primitive;
- _glam_density takes R and Rg from the new primitive;
- Rgg/Rggg call sites, and every C0/C1a/C1c/BOB call site, keep the legacy bundle unchanged.

## 2. Diagnostic layer — non-finite is not a sign failure

In tube_stage and eval_exterior, finiteness is tested BEFORE the sign test. A non-finite value is
recorded as such and never conflated with a proven-negative or unproven-sign outcome:
- new reasons TUBE_NONFINITE and EXTERIOR_NONFINITE, distinct from TUBE and EXTERIOR;
- a nonfinite record carrying side, stage label, refinement depth, the exact t interval, the exact
  λ interval, and the evaluator name;
- the worst-value trackers (gt_worst_upper, left_worst_lower, right_worst_upper) ignore non-finite
  values, so the printed worst values are always real bounds;
- a box whose evaluation is non-finite stays unresolved, exactly as today; the decision path
  (REFINE while depth < MAX_DEPTH, else ABORT) is unchanged. This layer changes what is recorded and
  reported, not what is accepted.

The MONO closure of v2.4 inherits the same rule: a non-finite gt or wall makes the closure false and
is recorded as non-finite rather than as a failed monotonicity test. A.1 remains the exact 15-key
producer schema, replay remains the exact 16-key schema, and comparison A1_KEYS remains the exact
14-key set of v2.4.2; nonfinite records and TUBE_NONFINITE / EXTERIOR_NONFINITE /
PREDICTOR_NONFINITE belong only to A.2 diagnostics and do not add, remove or reinterpret any A.1 key.

## 3. Work accounting

Unchanged. The new primitives replace one evaluation by two point evaluations of the same function
inside an existing panel loop; panel counts, step_work, ATTEMPT/GLOBAL/ACCEPTED ceilings,
MONO_WORK_CAP, ROOT_*_T_CELLS and the E/T tables are all as in v2.5.1.

This is exact, not approximate, because work is the predeclared logical panel/cell accounting metric
and not a count of internal Arb elementary operations: g_box, gt_box and glam_box each return their
panel count as the charged amount, and every accumulation site adds either that returned count or a
declared ROOT_*_PANELS / 2·panels constant. Changing the internal implementation of R therefore
cannot alter a panel's declared work charge.

Reporting detail (diagnostics, not accounting): since the worst-value trackers of §2 skip non-finite
values, a stage in which every evaluation of a given kind was non-finite has an empty set of real
bounds. Such a tracker prints None; it must never print ±inf, NaN, or a value carried over from an
earlier stage or box.

## 4. Pinning — second-level verification of the numeric import closure

The driver's fixed 7-path blob schema is NOT changed. Instead the trust chain is extended one level:

    7-path manifest  →  pins  →  C1b kernel / gating
                     →  contain expected blobs  →  numeric import closure

Each C1b kernel carries a constant map C1B_NUMERIC_IMPORT_CLOSURE from path to expected blob,
covering every module its numerical evaluation actually reads — for the producer lineage
producer/global_axial_c0_producer.py, producer/global_axial_c0_producer_v2.py,
producer/c0a_four_group_v2.py, producer/monotone_tube_refinement_producer.py and the module holding
the new primitive; for the checker lineage checker/global_axial_c0_checker.py,
checker/c0a_four_group_v2.py, checker/monotone_tube_refinement_checker.py and its own primitive
module. The two lineages declare their closures separately and never share an entry, even where the
file names look alike. The kernels and gating files themselves are excluded: they are pinned one
level up, and embedding a file's own blob in itself is circular.

preflight verifies the map before any numerical work, in the manner already used by bob_preflight:
the blob is recomputed from the bytes on disk (sha1 over "blob <len>\0" + content), because those
are the bytes Python actually imports; a git-tree lookup would attest the commit rather than the
loaded file. A mismatch, a missing file or an unreadable file is a hard failure
(SystemExit "NUMERIC_IMPORT_CLOSURE_FAIL").

Completeness is checked, not assumed — but over the numerical dependency graph, not over everything
the process happens to have loaded. The kernel declares a small set of numeric ROOT modules (the
ones it imports for evaluation); preflight computes the transitive closure of those roots restricted
to the lineage's own package, and requires that closure to equal the declared key set exactly. An
undeclared module that has entered the numerical path, or a declared module no longer reachable,
both fail. Modules outside that graph — logging, argument parsing, any future helper the kernel
imports for non-numerical purposes — are outside the population by construction and cannot cause a
spurious NUMERIC_IMPORT_CLOSURE_FAIL.

The receipt records NUMERIC_IMPORT_CLOSURE_CHECK = PASS together with every path, expected blob and
observed blob, listed separately per lineage.

## 5. Predeclared controls

C1 (analytic, preflight): c_n > 0 for the first terms, R(0) = 1, R(1) = π/2, and R evaluated on an
increasing sample is increasing; string C1B_R_ENDPOINT_CONTROL 1 PASS|FAIL.
C2 (complementary identity, independent control evaluator, NOT the implementation): for u in the
danger window, the endpoint-safe R is consistent with (π/2 − arcsin√(1−u))/√u, which is exact since
arcsin√u + arcsin√(1−u) = π/2. Recorded as an enclosure-consistency check in both lineages.
C3 (legacy agreement): on a representative grid where the legacy bundle is finite, legacy R and
endpoint-safe R intersect and the new enclosure is contained in or equal to the legacy one; zero
inconsistencies required.
C4 (regression witness): the canonical box of §0 — t = 546857674007/2^39, λ = [231/400, 3697/6400],
s panels 40–42 of the 4096 partition — is non-finite under the legacy path and finite under the new
one, in both lineages. The old and new values are recorded to 50 digits.
C5 (Gl regression): in the same window, R, Rg and the whole _glam_density are finite in both
lineages; and the aborted slab of §0 completes its tube stage.
C5b (moving u = 0 regression): on boxes selecting the series branch — including a box containing the
moving u = 0 chart — v2.6 and the legacy bundle take the same branch and return identical values for
R and Rg, and both are finite. This is the control that the small-u path was not disturbed.
C6 (diagnostics): a synthetic non-finite evaluation produces TUBE_NONFINITE / EXTERIOR_NONFINITE
with the full nonfinite record, and is not counted as a sign failure. A synthetic
REndpointDomainGuard raised inside each of the five call-site classes (tube, exterior sign, exterior
MONO, root g/Gl, predictor) is converted to the same non-finite outcome with
kind = "R_ENDPOINT_DOMAIN_GUARD" and never escapes as an exception; an unrelated RuntimeError raised
in the same position is NOT swallowed and propagates.
C7 (closure pin): every declared closure entry matches the on-disk blob; the declared key set equals
the transitive numeric dependency closure reachable from the predeclared numeric ROOT modules,
restricted to the lineage's own package; a deliberately perturbed entry, and a deliberately
undeclared module made reachable from a numeric ROOT, each produce NUMERIC_IMPORT_CLOSURE_FAIL. A
non-numerical import added outside that graph changes no control outcome.

## 6. Transcription and follow-up

- The new primitive is implemented independently in the producer and checker layers with no shared
  helper; the mathematical text is identical, the lineage differences remain the existing ones.
- The aborted run of §0 is not resumable and is retained as the historical control.
- Deferred, not in v2.6: the γ ∈ [0,1] a priori clamp (from v2.5 §6); endpoint-safe forms for
  Rgg/Rggg; folding the numeric import closure into the driver's own blob-path schema (the
  second-level check of §4 binds it already, one level below the driver).
- Open, recorded: whether other clamped quantities in the geometry are rebuilt through _box and can
  leak past their a priori bounds by the same mag-rounding mechanism. The new non-finite records of
  §2 make any such case visible instead of silent.

## 7. Required sequence

The binding order is implementation commit → chat raw audit → explicit push approval and push → new
manifest → preflight including C1–C7 → a fresh Phase 1 RUN_DIR and full producer rerun → Phase 2
checker → comparison → receipt; c1b_producer_20260907T073426Z remains historical control only, and
all push and tag operations remain approval-gated.
