# C1b Pre-Run Amendment v2.12 — Root Bracket Tau-Prime Clamp with Two-Part Strip Certificate

Status: PREDECLARE ONLY. No numerical implementation or Phase-1 launch is authorized by this commit.

Required parent: `892a846d543df488212eba67a11d02cb233fce57`.
This amendment wholesale supersedes the unimplemented v2.11.1 predeclare at `34f1ad0f`, including
corrections `572a84a1` and `892a846d`. The implemented v2.11 machinery remains the numerical base.

Evidence basis is limited to the pinned fifth-run ledger/stdout evidence already referenced by the
frozen v2.11/v2.11.1 documents: the terminal attempt is coarse 105 / depth 3, with
`ROOT:GT_DIVISION_GUARD_UNRESOLVED`, after the v2.11 corner certificate passed three times. The
sealed ledger is `b0481804...e54a`. That evidence also shows the axial Gt enclosure changes sign
before the corner, so the division guard cannot be repaired by endpoint subdivision while retaining
the bracket through tau = 65535/65536. A smaller certified root bracket is therefore required.

PROBE1--PROBE4 are `DIAGNOSTIC_ONLY / NOT_EVIDENCE`. They motivate the design and fixed constants
below but are not cited as certification evidence. In particular, they do not substitute for the
runtime certificate or the acceptance controls required by this predeclare.

## 1. Scope — exactly the v2.12 changes

Define `ROOT_GT_CLAMP_TAU = 255/256` (tau-prime). When `hi == T_HI` and
`lo < ROOT_GT_CLAMP_TAU`, root_localize may clamp its ROOT bracket high endpoint to tau-prime only
after the two-part strip certificate in section 2 PASSES. Under activation, every MV step, including
step 1, partitions both Gt and Gl cells only over `[lo, ROOT_GT_CLAMP_TAU]`. The
`first_step_gt_hi` mechanism is removed. This is the v2.12 successor to v2.11.1 scope item (i).

Add one lineage-local band-wall evaluator for P1. It evaluates the existing corner-regular wall
density over `[tau-prime,tau]`, where `tau = ROOT_GL_CORNER_TAU = 65535/65536`, using exactly 16
uniform fat t-cells. Each t-cell uses `ROOT_GL_CORNER_WALL_PANELS = 8192` wall panels. There is no
adaptive or geometric refinement in the authorized P1 construction. Every cell must return a finite
enclosure with strict `upper < 0`; otherwise P1 FAILS closed.

The existing v2.11 P2 machinery, constants, evaluator, B_ob receipt, tube receipt, and conjunction
remain unchanged. No TUBE, EXTERIOR, MONO, predictor, g_box, gt_box, endpoint-refinement, or other
numerical policy changes are authorized. The existing ROOT reason `GL_CORNER_CERT_UNRESOLVED` is
reused; no new reason is introduced.

A.2 slab-record serialization inherits v2.11.1 item (ii): when the certificate is evaluated, the
step-1 `result.root_mv_steps` entry records `"Gl_corner_certificate"`. Its payload contains separate
P1 and P2 results. P1 records tau-prime, tau, the exact 16 t-cell endpoints and enclosures, evaluator
label, wall-panel count, work and PASS/FAIL. P2 preserves the v2.11 section-3 certificate fields and
values, including its exact tau, receipts, G_tau enclosure, wall statistics, work and PASS/FAIL.

## 2. Two-part strip certificate and mathematical authorization

The removed strip `[tau-prime,1]` is certified as the union of two pieces.

**P1 — band wall `[tau-prime,tau]`.** The new band evaluator computes the corner-regular wall
quantity on each of the 16 uniform fat t-cells spanning `[255/256,65535/65536]` over the complete
current lambda slab. P1 PASS requires all 16 enclosures finite and all 16 upper bounds strictly
negative. This establishes `g(t,lambda)<0` throughout the band.

**P2 — existing v2.11 strip `[tau,1]`.** P2 is exactly the v2.11 conjunction: exact
tau `65535/65536`, successful right-clamped final TUBE Gt monotonicity obligation, covering pinned
B_ob endpoint receipt with `g(1,lambda)<0`, and the existing `root_gl_corner_wall_box` finite-t wall
with `G_tau.upper()<0`. Its mechanism, constants, receipt requirements and payload are unchanged.

The v2.12 strip certificate PASSES iff `P1 AND P2`. If either part is non-finite, throws, fails a
receipt condition, or lacks strict negativity, the certificate FAILS closed with the existing reason
`GL_CORNER_CERT_UNRESOLVED`, and root_localize does not use the tau-prime clamp. P1 and P2 results
are both retained in the A.2 certificate payload whenever evaluated.

Only a PASS authorizes replacing the ROOT bracket `[lo,1]` by `[lo,tau-prime]`. Consequently all MV
Gt/Gl domains are subsets of that certified bracket and the excluded strip contains no root.

## 3. v2.11.1 supersession and V211-C1 delegation

v2.11.1 (`34f1ad0f`, corrections `572a84a1` and `892a846d`) is superseded wholesale without being
implemented. Its intended first-step/full-step Gt clamp and A.2 recording are replaced/inherited as
specified here. No implementation commit may be made from the v2.11.1 specification itself.

The existing `V211-C1` terminal-reason assertion is delegated to `V212-C1`. The single corresponding
assertion inside `v211_preflight_controls` may be edited only to remove the superseded terminal-reason
expectation. All other V211-C1 invariants remain mandatory: activation, exact P2 tau, certificate
PASS, no Q_BOX guard activation originating in the removed strip, and issuance of a normal MV-step
record. No other existing V211 control assertion may change.

## 4. Work accounting

P1 charges exactly `16 * ROOT_GL_CORNER_WALL_PANELS = 16 * 8192 = 131072` units to attempt work,
in addition to unchanged P2 and ROOT-MV work. This charge is included on PASS and on evaluated
fail-closed paths according to the cells actually evaluated; acceptance controls must demonstrate
the full 131072 charge for canonical P1 PASS.

The three ceilings remain unchanged:
`ATTEMPT_WORK_CEILING = 25_600_000`,
`GLOBAL_ATTEMPT_WORK_CEILING = 53_760_000_000`, and
`ACCEPTED_WORK_CEILING = 28_672_000_000`.
No gating ceiling or estimates formula change is authorized.

## 5. Controls V212-C1..C4 — both lineages, hard-fail, inside preflight

**V212-C1 — canonical 105/3 replay.** Replay coarse 105 / depth 3 with historical bracket
`lo = 481429049247/549755813888` and the pinned fifth-run tube context. Require P1 PASS and record
all 16 P1 cell enclosures verbatim in the acceptance receipt. Require P2 PASS; its G_tau enclosure
must be bit-identical to the pinned fifth-run v2.11 value. Require every step-1 Gt cell to be a subset
of `[lo,255/256]` and to pass the division guard; record the worst step-1 Gt upper bound and require
it strictly negative. The only lawful outcomes are: (a) complete ROOT resolution with finite N_k and
a computed T_next; or (b) fail-closed termination, with the exact ROOT reason and terminating
measurements pinned verbatim. Any other outcome FAILS. The acceptance receipt pins the achieved
outcome and measured values verbatim.

Outcome (a) is the only outcome that authorizes the sixth Phase-1 launch; outcome (b) routes to the
next amendment with no launch.

**V212-C2 — non-activation identity and confinement.** On the existing v2.11 C2 non-activation
cases, output digests must be bit-identical and neither the P1 band evaluator nor the v2.11 P2 wall
evaluator may be called. Diff confinement is mandatory: kernel hunks may occur only inside
`root_localize`, inside the new band-evaluator function, inside the new `v212_preflight_controls`,
inside `v211_preflight_controls` solely for the delegated V211-C1 terminal-reason assertion, or as
exactly one invocation line added to the existing preflight control sequence. Gating hunks may occur
only inside the slab-record builder. No other function or existing line may be touched.

**V212-C3 — schema purity.** Machine checks require A.1 = 15 keys, replay = 16 keys, and cross-lineage
comparison `A1_KEYS` = 14 keys, unchanged. `"Gl_corner_certificate"` and all P1/P2 subfields are
A.2-only and absent from replay and A.1 comparison schemas.

**V212-C4 — thin-t anchor identity.** In each lineage, the new band evaluator evaluated on the thin
t-cell `t=tau` must be bit-identical to `root_gl_corner_wall_box(tau)` for the same lambda slab,
including the enclosure. Any mismatch FAILS preflight.

## 6. Required implementation and acceptance sequence

1. Freeze this doc-only predeclare before any implementation.
2. Implement as one clean commit, direct child of the frozen v2.12 predeclare; no rebase/amend and no
   unrelated edit. Changes are confined exactly as in V212-C2.
3. Deliver the acceptance payload through the candidate ref. Chat independently recomputes the
   candidate ancestry, changed-file pins (blob SHA-1, bytes, lines, SHA-256), canonical diff line
   count/SHA-256, both-lineage control stdout, V212-C1 outcome/measurements, and launch-gate quote.
4. Only after chat acceptance, push the canonical implementation commit. Then refresh the pinned
   expected blobs as a direct child, with the established eight-line expected_blobs replacement only,
   and push that pins commit.
5. Run official machine preflight at the pins commit, both lineages, with stdout captured verbatim via
   tee. The legacy suite, V211-C1..C5 and V212-C1..C4 must all hard-PASS; identity gates must
   PASS. The superseded, unimplemented V2111-C1..C3 controls are not introduced.
6. Only if V212-C1 achieved outcome (a), start the sixth Phase-1 run in a fresh RUN_DIR with producer
   stdout piped through tee to `RUN_DIR/stdout.log`, and quote the exact launch command in the receipt.
   Historical Phase-1 RUN_DIRs must not be resumed. Phase 2 remains separately gated.

No implementation, canonical implementation push, pins refresh, sixth-run launch, or Phase-2 work is
authorized by this predeclare commit alone. Any ambiguity or conflict with a frozen repo
requirement is fail-closed: stop before implementation and amend the predeclare explicitly.
