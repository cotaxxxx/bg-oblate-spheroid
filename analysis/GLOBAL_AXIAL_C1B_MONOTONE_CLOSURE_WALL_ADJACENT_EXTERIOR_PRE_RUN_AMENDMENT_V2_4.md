# C1b Pre-Run Amendment v2.4 — Monotone Closure of Wall-Adjacent Exterior Boxes

Status: PREDECLARED / NOT_EVIDENCE / MACHINE_NOT_RUN.
Scope: exterior stage of the C1b middle-t partition, both lineages (producer 160-bit, checker 192-bit).
Parent contract and amendments v2 … v2.3.1 remain in force except where this document
explicitly changes the exterior closure rule and the work ceilings.
The resumable driver (analysis/c1b_resumable_driver.py, blob 5fd308bb…) is NOT touched.

## 0. Canonical control (motivating ABORT)

RUN_DIR c1b_producer_20260906T101458Z, HEAD ad318967, attempt 14,
slab (coarse 1, depth 3, λ ∈ [723/1600, 2893/6400]), decision ABORT reason EXTERIOR.

- t_c = 20236857975/2^35, walls t₋ = 18089374327/2^35, t₊ = 22384341623/2^35 (t_c ∓ 1/16, no clamp)
- tube T0 PASS: gt_worst_upper ≈ −0.10147, left_worst_lower ≈ +0.0085677, right_worst_upper ≈ −0.012166
- root PASS (TARGET_WIDTH), predictor accept PASS
- exterior E0/E1/E2 unresolved 56/48/32; worst_left_lower −0.03928 / −0.01310 / −0.0003646
- the 32 E2 failures are all kind L, all in the single t-cell [71447992165/2^37, t₋] (width (t₋−1/2)/4),
  spanning the full slab λ-range in 32 contiguous λ-subcells.

Diagnosis: the wall value G(t₋,λ) is structurally small (≈ |G_t|·W0 ≈ 0.0063), while the
interval enclosure of G over a t-box of width Δt loses ≈ 1.35–1.8·Δt (≫ |G_t|·Δt); the sign test on the
wall-adjacent cell can therefore fail at every finite E stage. Neither λ-refinement (all 32 λ-subcells fail
alike) nor an extra E3 stage (extrapolated margin ≈ +0.004) removes the structural cause. The
quantity that makes the wall value small — G_t < 0 — is exactly what closes the cell by monotonicity.

## 1. Rule (mathematics)

Let B = [a, b] × Λ_B be an exterior box of the current E stage with panels p.

Left side (B ⊂ [T_LO, t₋] × Λ, i.e. b ≤ t₋). Define the strip S = [a, t₋] × Λ_B. If

  (L1) gt_box(a, t₋, Λ_B, p).upper < 0            (G_t < 0 on the whole strip S), and
  (L2) g_box(t₋, t₋, Λ_B, p).lower > 0            (wall value positive on Λ_B),

then for every (t, λ) ∈ B:  G(t, λ) = G(t₋, λ) − ∫_t^{t₋} G_t(s, λ) ds ≥ G(t₋, λ) > 0.

Right side (B ⊂ [t₊, T_MID_HI] × Λ, i.e. a ≥ t₊). Strip S = [t₊, b] × Λ_B. If

  (R1) gt_box(t₊, b, Λ_B, p).upper < 0, and
  (R2) g_box(t₊, t₊, Λ_B, p).upper < 0,

then G(t, λ) = G(t₊, λ) + ∫_{t₊}^{t} G_t(s, λ) ds ≤ G(t₊, λ) < 0 on B.

Both evaluators (g_box, gt_box) are the already-certified lineage evaluators used by the tube stage;
the corner chart cannot arise (b ≤ T_MID_HI = 31/32 < 1). The rule is a sufficient condition; a box that
fails it stays unresolved and is refined exactly as before (fail-closed, no new refinement path).

## 2. Placement in the exterior cascade (eval_exterior / exterior_cover)

At each E stage, for each box: (i) sign test as today; (ii) if unresolved, attempt monotone closure
(L1∧L2 or R1∧R2) subject to the MONO work cap; (iii) boxes still unresolved are refined as today.

Ordering (needed for A.1 guard-sequence equality across lineages): the monotone attempts of a stage
are made in ascending order of the exact key (dist, ll, tl), dist = t₋ − b for L boxes and a − t₊ for R
boxes (Fractions). The cap check precedes each attempt: if mono_work + 2·p > MONO_WORK_CAP the box is
skipped (stays unresolved). All arithmetic on box coordinates is exact (Fraction).

Terminal accounting: a box closed by (ii) is `resolved` for live_terminal and E_BOX_CAP purposes,
identically to a box closed by (i).

## 3. Work accounting and ceilings

- MONO_WORK_CAP = 1,048,576 (= 2^20) panel-evaluations per attempt; each monotone attempt costs 2·p
  (one gt_box + one g_box) and is charged to work["exterior"].
- ATTEMPT_WORK_CEILING: 23,560,192 → 24,608,768 (= 23,560,192 + 2^20; the old value decomposes exactly
  as tube 5,210,112 + root 1,376,256 + E0 196,608 + E2 cap 16,777,216).
- GLOBAL_ATTEMPT_WORK_CEILING: 49,476,403,200 → 51,678,412,800 (= 2100 × 24,608,768).
- ACCEPTED_WORK_CEILING: 26,387,415,040 → 27,561,820,160 (= 1120 × 24,608,768).
- Interrupted-attempt full charge = ATTEMPT_WORK_CEILING + predictor 262,656 (unchanged rule).
- Reference cost on the canonical control (56/48/32 unresolved): 573,440 < cap. Wall-adjacent-only bound
  for both sides, all stages: 688,128 < cap.
- MAX_DEPTH, MAX_ACCEPTED, MAX_ATTEMPTED, T/E stages, E_BOX_CAP, ROOT_* constants: unchanged.

## 4. Record / schema

- exterior_guards gains two guard kinds: "L_MONO" and "R_MONO". A monotone attempt appends exactly one
  guard tuple (stage, kind, a, b, ll, lr, truth) with the box coordinates (not the strip); truth = L1∧L2
  (resp. R1∧R2). Sign-test guards ("L"/"R") are unchanged and always precede the MONO guards of the same
  stage. Guard serialization (_serialize_guard) needs no change.
- Log line per stage: `C1B_EXTERIOR_MONO <coarse> <depth> <label> attempted <n> closed <m> skipped_cap <k> work <w>
  worst_gt_upper <str50|None> worst_wall <str50|None>`.
- New result field in slab_record.result: `"exterior_mono": {"attempted","closed","skipped_cap","work"}` (ints).
  It is REPORTED-layer only; it is NOT added to the replay plan (REPLAY_KEYS unchanged, so
  REPLAY_PLAN_KEY_ORDER_FAIL / REPLAY_SCHEMA_FAIL semantics are untouched). A.1 carries the rule through
  exterior_guards, which the checker replay and the comparison stage already compare for exact equality.
- Preflight prints `MONO_RULE left: Gt<0 on [a,t-]xL and G(t-)>0 => G>0 ; right: Gt<0 on [t+,b]xL and G(t+)<0 => G<0`
  and `MONO_WORK_CAP 1048576`.

## 5. Predeclared controls

Preflight logic controls (pure decision table, injected interval values; PASS required, FAIL → SystemExit
"EXTERIOR_MONO_CONTROL_FAIL"; string `C1B_EXTERIOR_MONO_CONTROL <i> PASS|FAIL`):
  1. L: gt.upper < 0, wall.lower > 0 → closed
  2. L: gt.upper < 0, wall.lower ≤ 0 → open
  3. L: gt.upper ≥ 0, wall.lower > 0 → open
  4. R: gt.upper < 0, wall.upper < 0 → closed
  5. R: gt.upper < 0, wall.upper ≥ 0 → open
  6. structural: L box with b > t₋ (or R box with a < t₊) → TypeError/RuntimeError "MONO_BOX_SIDE_INVALID"
  7. cap: mono_work at cap → box skipped, counted in skipped_cap, guard NOT appended

Machine control MC1 (canonical cell, both lineages, run once before the production run and recorded):
  box [71447992165/2^37, 18089374327/2^35] × [723/1600, 2893/6400], p = 4096, walls as in §0.
  Expected: sign test lower < 0 (producer recorded −0.0003645986525…); L1 upper < 0; L2 lower > 0;
  closure TRUE. The three enclosure values are recorded to 50 digits in the receipt.

Machine control MC2 (negative, both lineages): the same box with the wall value evaluated at the
wrong wall t₊ (R2-style test applied to an L box must be rejected structurally by control 6), plus a
box strictly inside the tube region [t₋, t₊] passed as an exterior box → "MONO_BOX_SIDE_INVALID".

## 6. Transcription obligations (two lineages)

- producer/global_axial_c1b_kernel.py and checker/global_axial_c1b_kernel.py: identical text of the new
  function(s) (mono_closure_box, mono_closure_controls) and of the modified eval_exterior/exterior_cover,
  modulo the existing lineage differences (BITS, evaluator imports). The three constants above change in
  both kernels; the byte-diff between the two kernels must remain "BITS line + lineage imports/evaluator
  bindings only" for all touched regions.
- Gating files: no functional change required (guard kinds are opaque strings; ceilings are read from the
  kernel). If estimates() is extended with "mono_cap_per_attempt", it must be done identically in both
  gating files.
- After implementation: chat raw audit (blob binding of the touched files + parent diff), new pin manifest
  (7-path schema, driver unchanged), preflight both lineages (controls 1–7 PASS), MC1/MC2 receipts,
  then a NEW RUN_DIR two-phase run (Phase 2 only after Phase 1 completes).

## 7. Non-goals / explicitly unchanged

- No E3 stage. No change to the sign-test rule, E_BOX_CAP, T/E stage tables, root localization, predictor
  selection, resume semantics, replay schema (REPLAY_KEYS), or the comparison stage.
- The ABORT ledger of §0 remains non-resumable; it is retained as the historical control.
- Observed refinement pattern (depth 2 required at the left end, ≈7 attempts and ≈12.6M evals per coarse
  slab, ≈1.76G evals if uniform) is recorded as an observation only; no change to ROOT_MV_STEPS here.
