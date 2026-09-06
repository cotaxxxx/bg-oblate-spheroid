# C1b Pre-Run Amendment v2.4.2 — Reclassification of Enclosure-Derived Fields from A.1 to A.2

Status: PREDECLARED / NOT_EVIDENCE / MACHINE_NOT_RUN.
Scope: two-phase replay contract (replay plan, checker replay verification, comparison stage).
Supersedes the A.1 field list of v2.3.1 and the A.1 sentences of v2.4/v2.4.1 (§2 ordering, §4 guards).
Kernels (producer 2f21147b…, checker 0c5c1e18…, HEAD 6a62ada9), the resumable driver (5fd308bb…),
the resume/segment machinery, the E-stage tables, MONO rule and all work ceilings are NOT touched.

## 0. Motivating control (canonical attempt 14, both lineages, v2.4.1 kernels)

Same exact tree, t_c, walls and E-stage tables; both lineages close the exterior cover at E1:
producer E0 sign-unresolved 56 → MONO closed 40, E1 closed 32, work 573,440;
checker  E0 sign-unresolved 56 → MONO closed 0,  E1 closed 64, work 1,032,192.
MC1 enclosures (p = 4096, full slab λ): sign lower producer −0.000987 / checker −0.001688;
wall lower producer +0.008094 / checker +0.007399; G_t upper both −0.121031…
The checker (192 bit) yields wider enclosures than the producer (160 bit): the difference is the
lineage-specific evaluator implementation, not precision. Guard truth values are therefore
lineage-dependent by construction and cannot be objects of an A.1 exact-equality requirement.
The same holds, latently since v2.3.1, for sign-test guards and for the first-passing tube/E stage.

## 1. Field classification (binding)

A.1 EXACT EQUALITY (producer plan → checker replay → comparison; exact rationals/ints/enums only).
  A.1 data fields = 15:
  attempt_sequence, tree_node, coarse_index, refinement_depth, lambda_lo, lambda_hi, decision,
  t_c, left_clamp, right_clamp, t_minus, t_plus, T_0, root_gt_t_cells, producer_accept_root_outcome.
  The replay plan object = these 15 + "schema" = 16 keys; the schema key is checked for identity
  separately from the data fields.
  (left/right_clamp, t_minus, t_plus, T_0 are exact functions of t_c and W0; their equality is a
  structural consistency check, kept.)
  producer_accept_root_outcome is an A.1 plan field but is NOT subject to generic producer/checker
  field equality: it is checked against the producer's ACCEPT certificate by the existing explicit
  ACCEPT branch. The checker's corresponding obligation is its own independent
  checker_root_outcome == RESOLVED_WITH_CERTIFIED_T_STAR check (never equated with the producer's).

A.2 LINEAGE INDEPENDENT (each lineage records its own; never compared for equality):
  tube_stage, corner_boxes, tube_guards, exterior_guards (incl. kinds L_MONO/R_MONO), root_mv_steps,
  root_reason, work, and every Arb enclosure.

A.3 CROSS-LINEAGE CONSISTENCY (unchanged): for ACCEPT, T_star intersection non-empty and
  |t_c − mid(T_star)| ≤ 1/64 in BOTH lineages.

Acceptance obligation (unchanged, made explicit): for every plan item with decision ACCEPT the checker's
own full certificate must succeed (checker_full_ok TRUE; otherwise CHECKER_REPLAY_ACCEPT_FAILURE) and
its root outcome must be RESOLVED_WITH_CERTIFIED_T_STAR. For REFINE/ABORT items the checker replays the
fixed t_c and records its own outcome; no equality of outcome is required.

## 2. Schema changes

- REPLAY_SCHEMA: "C1B_A1_REPLAY_V2_3_1" → "C1B_A1_REPLAY_V2_4_2" (producer gating, checker gating, compare).
- REPLAY_KEYS (producer tuple / checker set): remove tube_stage, corner_boxes, tube_guards,
  exterior_guards. The remaining 16 keys (schema + 15 A.1 data fields) keep their current relative
  order. replay_plan_item emits exactly these keys; FORBIDDEN_REPLAY_KEYS unchanged (A.2 leak guard
  still applies).
- checker verify_a1_fields: the `checks` tuple becomes ("left_clamp","right_clamp","t_minus","t_plus",
  "T_0","root_gt_t_cells"); the exterior_guards branch is deleted. Everything else unchanged.
- comparison stage: A1_KEYS (currently 18, without producer_accept_root_outcome) drops the four
  enclosure-derived fields → 14 keys under generic producer/checker equality. producer_accept_root_outcome
  remains a replay-plan A.1 field checked only by the existing explicit ACCEPT branch (plan value ==
  RESOLVED_WITH_CERTIFIED_T_STAR); the checker's checker_root_outcome is checked independently in the same
  branch, as today. A2 record gains, for each lineage, tube_stage, corner_boxes, tube_guards,
  exterior_guards (verbatim from the ledgers). Output schema string "C1B_CROSS_LINEAGE_COMPARISON_V2_4_2".
  A3 unchanged.
- slab_record payloads (both gatings) are unchanged: all fields keep being recorded.

## 3. Controls (predeclared)

- CC1 (positive, machine): the two canonical attempt-14 ledgers of §0 (one slab_record each) with the
  v2.4.2 replay plan → comparison PASS (15 A.1 data fields equal, replay schema key identical, A2 records
  differing guard sequences, A3 PASS). Under the v2.3.1 A1_KEYS the same input must FAIL with A1_CHECKER_MISMATCH key=exterior_guards
  (negative control on the old rule; both outputs recorded in the receipt).
- CC2 (negative, synthetic): checker payload with t_c differing → A1_CHECKER_MISMATCH key=t_c;
  disjoint T_star → A3_DISJOINT_T_STAR; plan line carrying "exterior_guards" → REPLAY_SCHEMA_FAIL
  (checker set(obj) != REPLAY_KEYS).
- Existing chat synthetic smoke (v2.3.1, 20 cases) is re-run against the v2.4.2 bytes with the
  four keys removed from the fixtures.

## 4. Files

Touched: producer/global_axial_c1b_gating.py, checker/global_axial_c1b_gating.py,
analysis/c1b_cross_lineage_compare.py. Byte-diff 0: both kernels, driver, entrypoints, requirements.
After implementation: chat raw audit (3 files + parent diff), 7-path manifest (kernel blobs from
6a62ada9), preflight both lineages, CC1/CC2 receipts, new RUN_DIR two-phase run.

## 5. Receipt correction carried forward

v2.4 §5 wrote "producer recorded −0.0003645986525…" as the MC1 sign lower; that value is the worst of the
32 E2 λ-subcells of the ABORT run (reproduced exactly on subcell [723/1600, 18509/40960]), not the
full-λ box value (−0.000987…). MC1's requirement (sign lower < 0) is unaffected; the receipt states both.

## 6. Observation (not a contract change)

Checker exterior margins are thinner than the producer's (wider enclosures at equal panels). Phase 2 may
need deeper E stages than Phase 1 on the same slabs; the Phase 2 receipt records per-slab exterior
first-pass stage and work for both lineages so that this asymmetry is visible.
