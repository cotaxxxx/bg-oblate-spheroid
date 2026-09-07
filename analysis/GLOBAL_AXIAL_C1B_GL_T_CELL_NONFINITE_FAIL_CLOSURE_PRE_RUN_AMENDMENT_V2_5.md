# C1b Pre-Run Amendment v2.5 — Gl t-Cell Splitting and Non-Finite Enclosure Fail-Closure

Status: PREDECLARED / NOT_EVIDENCE / MACHINE_NOT_RUN.
Scope: root localization (parametric mean-value step) in both kernels, the work ceilings, and the
ROOT_MV header metadata in both gating files. Touched files = 4 (producer/checker kernel,
producer/checker gating). Amendments v2 … v2.4.2 remain in force except for the constants and the
root-step behaviour changed here. The resumable driver (5fd308bb…), entrypoints, the replay schema
(v2.4.2), the MONO rule, the T/E stage tables and E_BOX_CAP are NOT touched.

## 0. Canonical control (crash of Phase 1, run c1b_producer_20260906T201744Z)

attempt 92, coarse 31, depth 0, λ ∈ [391/800, 49/100], previous_root
[203406215961/2^38, 205473707967/2^38] → t_c = 51109990491/2^36 (continuation),
t₋ = 46815023195/2^36, t₊ = 55404957787/2^36. T0 tube PASS
(gt_worst_upper −0.256802…, left_worst_lower +0.019092…, right_worst_upper −0.021753…).
Root step 1: all 16 Gt t-cells finite with upper < 0, hull Gt ⊂ [−0.586718…, −0.281706…],
division guard satisfied. Gl = NaN → Gpar = NaN → candidate = NaN →
_arb_exact_fraction(candidate.lower()) raised ValueError("man_exp requires an exact, finite value"),
an uncaught exception: the producer terminated without segment_end.

Cause, isolated on the first s-panel [0, 1/8192] of glam_box:
Gt is evaluated on 16 t-cells since amendment v2, but Gl was still evaluated on the full tube
[t₋, t₊] (width 1/8). Over that width d = t − μ (sign as in _geometry) straddles 0, so d² has
lower bound 0, so
q = e + λ²d² ⊂ [±0.0244] contains 0, and L = λ/(w q √q) evaluates to NaN; the failure propagates
through gt_lam to the density. Diagnostic evidence: on the same s-panel, with the tube split into
16 t-cells, cells 0–3 give d ≈ −0.31…−0.29 (radius ≤ 8.8e-3), q ≈ 0.02 (radius ≤ 3.3e-3, bounded
away from 0) and a finite density; the full-tube evaluation also returns γ ⊂ [0.14, 1.86], violating
the a priori bound |γ| ≤ 1, which confirms enclosure blow-up rather than a true singularity.
chart_unresolved was 0 throughout: the existing chart bookkeeping does not detect this failure.

## 1. Cause layer — Gl on t-cells (binding)

New constant ROOT_GL_T_CELLS = 16 (equal to ROOT_GT_T_CELLS, same exact partition of [lo, hi]).
In root_localize, Gl is computed as the outward hull of the per-cell enclosures:

  for (cell_lo, cell_hi) in split(lo, hi, ROOT_GL_T_CELLS):
      value, stats, _ = glam_box(cell_lo, cell_hi, slab.ll, slab.lr, ROOT_GL_PANELS)
  Gl = _outward_hull(gl_values)

using the existing _outward_hull (min lower / max upper, raises ROOT_EMPTY_GT_CELL_SET on an empty
set; that error name is historical and is shared by the Gl hull — it does not imply a Gt failure). This is the exact analogue of the Gt treatment and is valid for the same reason: the mean-value
form needs an enclosure of Gl over the tube, and a hull of enclosures over an exact partition is one.
Per-cell records are appended to the step record as "Gl_cells": [{"t_cell", "Gl", "gl_stats", "work"}],
mirroring "Gt_cells". The aggregated gl_stats of the step is the per-key sum over cells.
glam_box, _glam_density and the chart policy are unchanged.

## 2. Defence layer — non-finite enclosures are contract-internal, never crashes

- _arb_exact_fraction: before man_exp, require x.is_finite(); otherwise
  raise RuntimeError("ROOT_NONFINITE_ARB_BOUND"). (The existing is_exact check is kept; an arf bound
  is always "exact" but may be ±inf or NaN, which is what the old guard missed.)
- root_localize, before the division guard: if any of G0, Gt, Gl, Gpar has a non-finite lower or upper
  bound, close the step with reason "MV_NONFINITE_ENCLOSURE" (record written, no Newton step, break),
  exactly as GT_DIVISION_GUARD_UNRESOLVED does today. The step record gets
  "nonfinite": a dict with keys "G0","Gt","Gl","Gpar" whose value is True exactly when that quantity
  has a non-finite bound (True = non-finite), so the receipt is unambiguous.
- _newton_candidate: return the candidate only if ALL of the following hold — gt.upper() < 0, the
  quotient gpar/gt has finite lower and upper bounds, and the resulting candidate
  t_ref − gpar/gt itself has finite lower and upper bounds; otherwise return None. (The candidate's
  finiteness is required explicitly, not inferred from the quotient's.) A non-finite candidate
  therefore yields guard = False rather than an exception.
- ROOT_EMPTY_INTERSECTION handling is unchanged (still a raise; it is a genuine contradiction, not an
  enclosure defect).
An attempt whose root step ends in MV_NONFINITE_ENCLOSURE is UNRESOLVED and follows the existing
REFINE/ABORT path with full work charged. No new refinement path is created.

## 3. Work accounting and ceilings

- step_work: 32768 + 16·8192 + 8192 = 172,032 → 32768 + 16·8192 + 16·8192 = 294,912.
- root per attempt (8 steps): 1,376,256 → 2,359,296.
- ATTEMPT_WORK_CEILING: 24,608,768 → 25,591,808
  (= tube 5,210,112 + root 2,359,296 + E0 196,608 + E2 cap 16,777,216 + MONO cap 1,048,576).
- GLOBAL_ATTEMPT_WORK_CEILING: 51,678,412,800 → 53,742,796,800 (= 2100 × 25,591,808).
- ACCEPTED_WORK_CEILING: 27,561,820,160 → 28,662,824,960 (= 1120 × 25,591,808).
- Interrupted-attempt full charge = ATTEMPT_WORK_CEILING + predictor 262,656 = 25,854,464 (rule unchanged).
- estimates(): early one-lineage 279,910,400 → 417,536,000; no-refinement 3,481,999,360 → 3,619,624,960.
- Observed cost in the aborted run was ≈1.33M per attempt against the then-ceiling of 24.6M; the added
  983,040 per attempt with a root call is ≈0.9M, i.e. roughly a doubling of measured per-attempt work.
- MONO_WORK_CAP, MAX_DEPTH, MAX_ACCEPTED, MAX_ATTEMPTED, E_BOX_CAP, ROOT_MV_STEPS, ROOT_*_PANELS,
  ROOT_GT_T_CELLS: unchanged.

## 4. Record / schema

- Step record gains "Gl_cells" and "nonfinite" (REPORTED layer, inside root_mv_steps, which is A.2
  under v2.4.2). REPLAY_KEYS, A1_KEYS, verify_a1_fields, the comparison stage and the ledger record
  types are unchanged; no replay/A1 verification logic needs editing in either gating file
  (the header edit below is the only gating change).
- Header ROOT_MV block gains "gl_panels_per_cell" and "gl_t_cells" (mirroring the gt entries),
  replacing "gl_panels". This is the only gating-side edit; it is required, not optional, and must be
  made identically in both gating files. No other gating behaviour changes. Note that this changes the
  header payload, so a ledger written under the old header cannot be resumed against the new one
  (RESUME_HEADER_CONTRACT_MISMATCH) — consistent with §6, which retains the aborted ledger as a
  historical control rather than resuming it.
- Preflight prints ROOT_GL_T_CELLS alongside ROOT_GT_T_CELLS.

## 5. Predeclared controls

Logic controls (preflight, both lineages; string C1B_ROOT_NONFINITE_CONTROL <i> PASS|FAIL, failure →
SystemExit "ROOT_NONFINITE_CONTROL_FAIL"):
  1. _arb_exact_fraction on a finite exact bound → correct Fraction (2 values, one dyadic negative).
  2. _arb_exact_fraction on +inf → RuntimeError ROOT_NONFINITE_ARB_BOUND.
  3. _arb_exact_fraction on NaN → RuntimeError ROOT_NONFINITE_ARB_BOUND.
  4. _newton_candidate with gt.upper() < 0 but non-finite gpar → None (no exception).
  5. _outward_hull of two finite balls → exact min-lower/max-upper containment check.

Machine control MC3 (both lineages, recorded in the receipt): the canonical slab of §0 with its exact
t_c and walls, root step 1 recomputed. Expected: 16 Gl cells all finite; hull Gl finite; Gpar finite;
Newton candidate finite; the step completes with a T_next strictly inside [t₋, t₊]. The Gl hull and
Gpar are recorded to 50 digits. Under the v2.4.2 kernels the same input yields Gl = NaN
(negative control, recorded).

MC4 (negative, both lineages): glam_box called on the full tube [t₋, t₊] for the first s-panel returns
a non-finite density, and root_localize with ROOT_GL_T_CELLS forced to 1 ends the step with
MV_NONFINITE_ENCLOSURE — not an exception. This exercises the defence layer on the real failure.
The forcing to 1 is done only in the control invocation; the canonical source constant stays
ROOT_GL_T_CELLS = 16, and the receipt states this explicitly.

## 6. Transcription obligations and follow-up

- Both kernels change identically (constants, ROOT_GL_T_CELLS loop, guards, controls); the byte-diff
  between the two kernels must remain "docstring + imports + BITS + producer-only tree functions +
  attempt_replay + preflight wording", as verified for 6a62ada9. The two gating files receive the same
  header edit; their mutual byte-diff must not grow beyond the existing lineage differences.
- The aborted ledger (61 accepted, last slab_record hash f9596aac…, last ledger hash ecb8b24f…) is NOT
  resumable under the new pins; it is retained as the historical control for this crash.
- Deferred, not part of v2.5: an a priori clamp γ ∈ [0,1] (or [−1,1]) intersected into the geometry,
  which would have caught the blown-up enclosure one stage earlier. To be handled as a separate
  amendment or control so that its audit stays independent of this fix.
- Open question recorded, not blocking: whether Gt's 16 cells are sufficient at the widest slabs, given
  that the same width caused Gl to blow up. Phase 1 evidence so far (all Gt cells finite, guards true)
  says yes for the slabs reached; the new Gl_cells records make the margin visible per step.
