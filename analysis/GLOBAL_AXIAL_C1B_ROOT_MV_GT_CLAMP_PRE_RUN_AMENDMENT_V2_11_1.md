# GLOBAL_AXIAL_C1B — Pre-run Amendment v2.11.1
# Root-MV Gt clamp alignment and corner-certificate A.2 recording

Status: PREDECLARE (doc-only). Parent commit: 0886a7bb4c2928fb303e5edd66da14d882e1062d.
Applies to: producer/global_axial_c1b_kernel.py, checker/global_axial_c1b_kernel.py,
producer/global_axial_c1b_gating.py, checker/global_axial_c1b_gating.py (A.2 record schema only).
Reference: v2.11 predeclare (blob 8d3e32e9), fifth-run terminal record
(coarse 105 / depth 3, reason ROOT:GT_DIVISION_GUARD_UNRESOLVED, sealed ledger b0481804...e54a).

## 1. Scope — exactly three changes

(i) root_localize: remove the first_step_gt_hi mechanism. When v2.11 corner
separation is ACTIVE (hi == T_HI and lo < ROOT_GL_CORNER_TAU and certificate
PASS), every MV step, including step 1, partitions its Gt cells over the
clamped bracket [lo, ROOT_GL_CORNER_TAU]. No Gt cell may extend beyond tau
while the separation is active. The v2.9 scale-compatible corner refinement
ladder applies unchanged to the clamped cells.

(ii) A.2 recording: the slab_record serialization adds the key
"Gl_corner_certificate" to the step-1 entry of result.root_mv_steps whenever
the certificate was evaluated (PASS or FAIL). The payload is the certificate
record defined in v2.11 section 3 (tau, lambda, tube_stage, right_clamp,
tube_monotonicity_pass, bob_receipt_blob, bob_covers, evaluator, G_tau,
wall_stats, work, pass, detail-on-exception). This key is A.2-only:
A.1 remains 15 keys, the replay schema remains 16 keys, and the cross-lineage
comparison A1_KEYS remains 14. No replay-plan or comparison change.

(iii) Nothing else changes. The wall evaluator root_gl_corner_wall_box, the
certificate assembly and its three-certificate conjunction, the activation
condition, ROOT_GL_CORNER_K = 16 and ROOT_GL_CORNER_TAU = 65535/65536,
ROOT_GL_CORNER_WALL_PANELS = 8192, tube stages and v2.10 endpoint refinement,
exterior, MONO, predictor, g_box/gt_box evaluators, and the fail-closed reason
GL_CORNER_CERT_UNRESOLVED are all byte-for-byte outside the scope of this
amendment except where (i) and (ii) textually require edits inside
root_localize and the record builder.

Non-activated boxes remain bit-identical to v2.11 (the edits of (i) are
reachable only under the activation condition; (ii) adds a key only when a
certificate exists, which also requires activation).

## 2. Mathematical basis

Under activation, the strip [tau, 1] is root-free for g(., lambda) on the
slab: the v2.11 conjunction (tube right-clamp Gt<0 receipt over the clamped
interval up to t=1; B_ob endpoint receipt g(1,.)<0; wall certificate
G(tau,.) upper < 0) establishes g < 0 on [tau, 1]. The mean-value root
localization therefore operates on the bracket [lo, tau]: its enclosure
N_k and the division guard require bounds of Gt on T_k, a subset of
[lo, tau], and nothing outside it. Evaluating step-1 Gt up to the original
hi = 1 (the v2.11 first_step_gt_hi choice) was sound but strictly wider than
required, and it re-imported the corner-driven enclosure blow-up of Gt near
t = 1 (fifth-run evidence: tube-stage gt_worst_upper about 1.1e4 at T0;
endpoint-adjacent cells positive through ladder levels 1-2) into the division
guard, which is exactly the failure recorded as GT_DIVISION_GUARD_UNRESOLVED.
On [lo, tau] the corner is excluded: q >= lambda^2 (1-tau)^2 > 0 at s = 0,
all evaluators are finite there, and the v2.9 ladder addresses residual
looseness at the tau-adjacent cell.

## 3. Work accounting

Step-1 Gt partitions into ROOT_GT_T_CELLS = 16 cells of ROOT_GT_PANELS = 8192
panels each, exactly as in v2.11; only the cell endpoints change. Certificate
work is unchanged. Therefore ATTEMPT_WORK_CEILING = 25_600_000,
GLOBAL_ATTEMPT_WORK_CEILING = 53_760_000_000 and
ACCEPTED_WORK_CEILING = 28_672_000_000 are unchanged, as are the gating
estimates() formulas.

## 4. Controls V2111-C1..C3 (both lineages, hard-fail, run inside preflight)

C1 (historical replay): replay coarse 105 / depth 3 with the historical
bracket lo = 481429049247/549755813888 and the fifth-run tube context.
Required: certificate PASS with tau exact; every step-1 Gt cell satisfies
t_cell[1] <= tau; and the outcome is one of the two predeclared lawful
outcomes: (a) the division guard resolves (finite N_k and a computed T_next),
or (b) GT_DIVISION_GUARD_UNRESOLVED with the worst step-1 Gt upper bound
strictly smaller than the fifth-run value. Any other outcome FAILS. The
achieved outcome (a or b, with the measured values) is pinned verbatim in
the acceptance receipt.

C2 (bit-identity and confinement): (a) non-activated boxes reproduce v2.11
outputs bit-for-bit (digest comparison on the v2.11 C2 cases; the wall
evaluator must not be called); (b) diff confinement: all kernel hunks lie
inside root_localize, and all gating hunks lie inside the slab-record
builder; no other function is touched.

C3 (A.2 recording and schema purity): after C1, the in-memory slab record
contains root_mv_steps[0]["Gl_corner_certificate"] with pass == True and
G_tau present; machine checks confirm A1 == 15 keys, replay == 16 keys,
comparison A1_KEYS == 14, and "Gl_corner_certificate" absent from the
replay schema.

## 5. Required sequence

1. This predeclare as a doc-only commit, parent 0886a7bb (this document).
2. Chat verbatim audit and freeze.
3. Implementation as a single clean commit, direct child of the frozen
   predeclare commit; no rebase or amend; changes confined to section 1.
4. Acceptance delivery via candidate ref; chat recomputes all pins from
   the remote objects (per-file blob SHA-1, bytes, lines, SHA-256,
   canonical diff).
5. Push of the canonical branch only after chat acceptance; then pins
   refresh (8-line expected_blobs replacement) as a direct child; both
   pushed.
6. Official machine preflight at the pins commit: legacy suite +
   V211-C1..C5 + V2111-C1..C3, both lineages, verbatim stdout with pins.
7. Launch procedure MUST capture stdout: the producer is started with its
   stdout piped through tee into RUN_DIR/stdout.log, and the launch report
   quotes the exact launch command.
8. Phase 1 sixth full rerun in a fresh RUN_DIR after the identity gate.
   RUN_DIR phase1_v211_0886a7b_20260915T192742Z is historical; resume is
   forbidden. Phase 2 remains separately gated.
