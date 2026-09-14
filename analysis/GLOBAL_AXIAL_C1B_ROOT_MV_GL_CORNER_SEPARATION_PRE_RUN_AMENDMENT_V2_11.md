# C1b Pre-Run Amendment v2.11 — ROOT-MV Gl Corner Separation

Status: PREDECLARE ONLY. No numerical implementation is authorized by this commit.

Parent required for this predeclare: `cac327227ab4b8eb56693a96d3e0eeb9685ca7a9`.

This amendment responds only to the certified ROOT-MV `Gl` endpoint-domain contact observed in the
historical Phase-1 run `phase1_v2101_cac32722_20260913T052607Z`. That run is historical evidence only;
it MUST NOT be resumed.

Diagnostic basis, independently transferred through Gist and pinned before this predeclare:

- endpoint failure diagnostic: 75 lines, SHA-256
  `584d7ce25909602038b81ee29067f6b181fb3e2e9ca716f2a1f69c46f26144e2`;
- algebra diagnostic: 85 lines, SHA-256
  `2723e9ec8a876ff59c18d038a54436d63f7a9dca0b7c989280878d547d825a7e`.

The first diagnostic establishes that the failing ROOT-MV path is `Gl = glam_box` at coarse 105,
depth 3, step 1; the endpoint child retaining `t=1` remains non-positive in the positive-q guard
through dyadic depths 1--8. The second establishes the exact corner algebra

    x = s^2,  delta = 1-t,
    q = x(2-x) + lambda^2 (x-delta)^2,

so the zero is a joint north-pole corner contact. On `s=0`, exactly

    q(0,t,lambda) = lambda^2 (1-t)^2,

but `(1-t)^2` is NOT a factor of the full q for general s. Therefore v2.11 does not authorize a
global q-factorization.

## 1. Scope

The only changed numerical path is the ROOT parametric mean-value evaluation when its `Gl` domain
would include the north-pole corner `t=1` through

    root_localize -> glam_box -> _glam_density -> _positive_q_box.

The v2.11 change is a ROOT-MV `Gl` corner separation. Its certificate helpers and any control-only
plumbing exist solely to justify removing a fixed endpoint strip from that ROOT-MV domain.

The following are explicitly unchanged:

- all TUBE numerical evaluators, T0/T1/T2 stages, T2 endpoint refinement and tube decisions;
- all EXTERIOR evaluators, E0/E1/E2 policy and decisions;
- all MONO evaluators, predicates, partitions and work rules;
- predictor construction, predictor selection, predictor acceptance and predictor work;
- the ROOT point/reference `g` evaluation `G0 = g_box(t_ref,t_ref,lambda_c,lambda_c,...)`;
- the ROOT `Gt` evaluator, its 16-cell subdivision, v2.9 refinement and guard predicate;
- the Newton formula, target width, number of MV steps and empty-intersection semantics;
- lambda partition, slab refinement tree, maximum depth, acceptance predicates and Phase-2 rules;
- endpoint `B_ob` mathematics and its existing machine receipt.

A ROOT-only endpoint-safe finite-t wall evaluator may be introduced for the strip certificate below.
It is not a replacement for root `g_box`, tube walls, exterior walls, or any existing evaluator.

No change outside the ROOT-MV corner-contact case is authorized by this amendment.

## 2. Method — fixed ROOT-MV Gl corner separation

Define the fixed separation exponent and cut

    ROOT_GL_CORNER_K = 16,
    tau = 1 - 2^(-16) = 65535/65536.

`k=16` is binding; it is not adaptive and may not be increased or decreased by the implementation.
The diagnostic safe band was `k in [8,16]`: full `glam_box` evaluation passed at k=8,9,10,12,16,
whereas secondary endpoint guards appeared by k=20 and k=24. Among the measured safe values, k=16
removes the narrowest strip and therefore retains the largest ROOT-MV domain while staying strictly
outside the observed secondary-guard band.

Activation is exact and limited to a ROOT-MV interval `T_k=[lo,hi]` with `hi=1` and `lo<tau`.
For such a ROOT call, before the first `Gl` evaluation that would touch `t=1`, the endpoint strip

    S_corner = [tau,1]

is treated as a separate no-root obligation. If and only if the certificate in §3 passes, ROOT-MV
continues on

    T_k^safe = [lo,tau].

All subsequent `Gl` subdivisions in that ROOT call are formed from the safe interval and use the
existing `ROOT_GL_T_CELLS=16`, existing `ROOT_GL_PANELS=8192`, existing `glam_box`, existing
`_glam_density` and existing `_positive_q_box` without weakening any guard.

This is a t-side separation only. There is NO new s-panel split for the ordinary `Gl` computation.
The existing s partition is unchanged. The reason a t-only separation is permitted is that the joint
contact requires `t=1`; after the exact cap `t<=tau<1`, the ordinary `Gl` path no longer contains the
joint corner. Any special s-chart used internally by the §3 certificate is certificate-only and does
not alter ordinary ROOT `Gl` s panels.

If `hi<1`, or if the ROOT-MV box does not cross `tau`, v2.11 is inactive and execution MUST be the
pre-v2.11 path bit-for-bit.

The implementation may perform the certificate once per `root_localize` call before replacing the
initial right endpoint 1 by tau. It may not repeatedly shrink tau, search over k, or create an
adaptive endpoint-refinement tree.

## 3. Strip no-root certificate

Discarding `[tau,1]` from the ROOT-MV domain is authorized only by an explicit, lineage-local proof
that `g(t,lambda)` has no zero there for the current lambda slab.

The certificate has three mandatory inputs, all in the same producer or checker lineage:

1. **Existing TUBE monotonicity receipt.** The immediately preceding successful tube stage for the
   same slab and attempt must be right-clamped (`tp=1`) and must have certified its final `Gt<0`
   obligation through the existing T0/T1/T2 logic, including any already-authorized T2 endpoint
   refinement. No tube value is recomputed or modified by v2.11.
2. **Existing endpoint receipt.** The pinned `B_ob` bridge receipt must cover the slab lambda interval
   and certify `g(1,lambda)=B_ob(lambda)<0` there.
3. **New ROOT-only finite-t wall certificate at tau.** Evaluate the same mathematical quantity
   `g(tau,lambda)` on the full current lambda slab with an endpoint-regular two-chart wall evaluator,
   predeclared name `root_gl_corner_wall_box`. This evaluator must avoid raw division by a q interval
   touching zero and must use the already-audited north-pole bounded variables/identities
   (`rho`, `phi`, `Ahat`, endpoint-safe R data, or an algebraically equivalent exact regrouping).
   It is evaluated only at the exact finite rational `tau=65535/65536`. The pass predicate is finite
   enclosure and strict sign

       G_tau.upper() < 0.

The certificate PASS condition is the conjunction

    right_clamp == True
    AND final tube Gt monotonicity obligation == PASS
    AND B_ob receipt covers [lambda_lo,lambda_hi] with upper < 0
    AND root_gl_corner_wall_box(tau,[lambda_lo,lambda_hi]).upper() < 0.

The mathematical implication is binding: the successful tube proof gives strict decrease of g in t
on the relevant right-hand interval; the finite-t wall gives `g(tau,lambda)<0`; hence
`g(t,lambda)<0` for every `t in [tau,1]`, with the endpoint independently covered by `B_ob<0`.
Therefore the removed strip contains no root.

The certificate record is A.2 lineage-independent evidence. At minimum it records the exact tau,
exact lambda interval, tube stage label, right-clamp state, tube monotonicity PASS state, B_ob receipt
identifier/pin, `G_tau` enclosure, evaluator label, work charged, and PASS/FAIL.

A finite-t surrogate may NOT replace the `B_ob` endpoint receipt. Conversely the B_ob receipt alone
may NOT replace the finite-t `G_tau<0` wall. Both are required.

The implementation must contain an exact-algebra or rational-point audit showing that the new
endpoint-regular wall expression equals the legacy mathematical g wherever both are finite, plus
an enclosure-intersection control on representative non-corner boxes.

## 4. Fail-closed semantics and schema

Introduce exactly one new ROOT reason:

    GL_CORNER_CERT_UNRESOLVED

At slab-attempt serialization this appears through the existing prefix as

    ROOT:GL_CORNER_CERT_UNRESOLVED.

If any certificate input is missing, non-finite, not strictly signed, not covering the full current
lambda slab, or internally inconsistent, the strip is NOT removed. The implementation MUST NOT fall
back to the old corner-touching `Gl` evaluation. Instead `root_localize` returns UNRESOLVED with
reason `GL_CORNER_CERT_UNRESOLVED` and the attempt follows the existing refinement/fail-closed path.
If unresolved at the terminal permitted slab refinement, the existing driver reaches ABORT. No
certificate failure can produce ACCEPT or Phase-2 evidence.

The certificate record and failure diagnostics are A.2 only. Schema invariants are binding:

- A.1 producer data fields remain exactly 15;
- replay object remains exactly 16 keys (`schema` + 15 A.1 fields);
- comparison `A1_KEYS` remains exactly 14;
- no A.1 key is added, removed, renamed or reinterpreted;
- no A.2 enclosure or certificate payload may enter checker replay input.

Producer and checker independently evaluate their own certificate. A lineage may not consume the
other lineage's interval values.

## 5. Invariants and work accounting

All work is charged; no certificate evaluation is free.

- Existing successful TUBE work and existing `B_ob` bridge work retain their current accounting and
  are not double-charged merely because the ROOT certificate references their receipts.
- Every new `root_gl_corner_wall_box` panel evaluation is charged to ROOT work.
- If certificate construction uses more than one internal chart or sub-evaluation, every such panel
  evaluation is charged exactly once to ROOT work.
- The implementation commit must update `ATTEMPT_WORK_CEILING`, global/accepted ceilings and printed
  estimates by the declared worst-case certificate cost before an official run. No observed-cost
  shortcut is permitted.
- A certificate failure charges all work actually performed before failure and then fails closed.
- `ROOT_GL_T_CELLS`, `ROOT_GL_PANELS`, `ROOT_G_PANELS`, `ROOT_GT_PANELS`, `ROOT_MV_STEPS` and all
  non-v2.11 stage panel counts remain unchanged unless a later separately frozen amendment says so.

For every ROOT-MV box that does not activate §2, the producer and checker executable behaviour must
be bit-identical to the v2.10.1-C1 implementation at parent `cac32722...`, including returned balls,
records, reasons and work totals. In particular, corner-noncontact boxes are bit-identical.

For an activated call after certificate PASS, only the ROOT-MV right endpoint used for subsequent Gl
mean-value enclosure is replaced by exact tau. G0, Gt formulae, Newton formulae and all downstream
non-ROOT stages remain unchanged.

## 6. Mandatory controls — both lineages

Every control below is mandatory in BOTH producer and checker preflight. Any control failure is a
preflight failure and no gating run may start.

### V211-C1 — canonical 105/3 resolution

Reproduce the historical coarse 105 / depth 3 corner-contact case with the exact lambda slab
`[931/1600,149/256]` and the historical ROOT context. Require:

- v2.11 activation;
- tau exactly `65535/65536`;
- strip certificate PASS;
- no `R_ENDPOINT_DOMAIN_GUARD/Q_BOX_MIN_NONPOSITIVE` from the removed strip;
- ordinary Gl cells on the safe ROOT domain all finite;
- the ROOT step proceeds beyond the former pre-`C1B_ROOT_MV_STEP` failure point and emits a normal
  MV-step record; and
- the case resolves according to the unchanged ROOT logic rather than by suppressing an unresolved
  result.

The exact resulting ROOT outcome is to be pinned in the implementation acceptance receipt.

### V211-C2 — non-corner bit identity

Select representative ROOT-MV boxes with `hi<tau`, including at least one ordinary box and one box
near but not crossing tau. Run the parent-v2.10.1-C1 path and v2.11 path on identical exact inputs and
require byte/serialized equality of numerical outputs, reason, work and A.2 records. Also perform a
static/diff confinement audit proving that nonactivation dispatch reaches the unchanged evaluator.

### V211-C3 — certificate negative control / fail-closed

Inject a synthetic certificate wall result with `G_tau.upper() >= 0` (and separately a non-finite wall
result if the helper distinguishes it) while all other prerequisites are synthetically PASS. Require
end-to-end `root_localize` failure with exact reason

    GL_CORNER_CERT_UNRESOLVED,

then require slab-attempt serialization

    ROOT:GL_CORNER_CERT_UNRESOLVED,

with no ordinary corner-touching `glam_box` fallback and no ACCEPT. The control must exercise the real
final reason path, not only a helper Boolean.

### V211-C4 — secondary-guard-band exclusion

Assert `ROOT_GL_CORNER_K == 16` and `tau == 65535/65536`. The activation path must contain no adaptive
k loop and no candidate k >= 20. A machine control must show the safe ordinary Gl domain ends exactly
at tau. The diagnostic k=20 `INV_WQ32_NONFINITE` and k=24 `Q_BOX_OUTWARD_NONPOSITIVE` band is therefore
not entered by construction.

### V211-C5 — producer/checker symmetry and schema purity

In each lineage require all V211-C1 through C4 PASS. Verify A.1=15 keys, replay=16 keys and
comparison `A1_KEYS`=14. Verify the v2.11 certificate payload is A.2 only and absent from replay.
Verify producer and checker independently construct interval evidence and do not import one another's
numerical implementation.

## 7. Frozen sequence after this predeclare

The only authorized sequence is:

1. Commit THIS predeclare alone with immediate parent
   `cac327227ab4b8eb56693a96d3e0eeb9685ca7a9`. The commit is document-only. All executable blobs,
   pins and manifests remain unchanged.
2. Transfer the full predeclare text to chat, with commit SHA, Git blob, byte count, line count and
   SHA-256. Chat performs verbatim audit. Until explicit audit PASS, v2.11 is not frozen for
   implementation.
3. After explicit implementation authorization, create exactly one clean implementation commit whose
   immediate parent is this predeclare commit. No rebase, squash-through, amend of the predeclare, or
   mixed unrelated edit is allowed.
4. Build an acceptance payload and physically transfer it to chat using the established Gist tar.gz
   route or base64 route, with per-item pins and archive/payload pin. Chat independently verifies it.
5. Push only after explicit push approval and then verify the remote tree against the accepted bytes.
6. Refresh pins/manifest only after the accepted implementation lineage is fixed, using a separate
   declared pins/manifest step as required by the resumable contract.
7. Run official preflight only after pins/manifest verification. Both producer and checker must pass
   all legacy controls plus V211-C1--C5.
8. Start Phase 1 from a NEW RUN_DIR and execute the full Phase-1 producer from the beginning. The
   historical RUN_DIR
   `/home/daybreak/basepoint-geometry-artifacts/C1b/phase1_v2101_cac32722_20260913T052607Z`
   is permanently historical and MUST NOT be resumed or reused.
9. Phase 2 remains separately approval-gated. Phase-1 completion does not authorize Phase 2.

This predeclare does not authorize implementation, push, pin refresh, official preflight, Phase-1
execution or Phase 2. Those gates remain closed until their listed approvals occur.
