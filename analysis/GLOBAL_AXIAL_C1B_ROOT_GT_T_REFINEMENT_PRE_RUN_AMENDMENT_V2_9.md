# C1b Pre-Run Amendment v2.9 — Corner Scale-Compatible Root-Gt t Refinement (k=2)

Status: PREDECLARED / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent executable state: commit 02e83105c398e8eb43579d7deda4ad532de42c9b.
Scope: root-side Gt division-guard recovery only. No implementation is authorized by this document until chat-side verbatim audit passes.

## 1. Target and activation condition

This amendment applies only to the root-localization Gt guard evaluation whose current per-cell condition is:

`"guard": bool(value.upper() < 0)`

and whose Newton division is permitted only when every root Gt t-cell has established a strictly negative upper bound.

The refinement may be invoked only when the ordinary root Gt evaluation over the existing 16 deterministic t-cells produces at least one cell with `guard == False`. A cell that already satisfies `value.upper() < 0` is final and must not be refined. No refinement is permitted on an ACCEPT-path cell that already passed its ordinary guard.

The authorized scope is confined to this root-side Gt guard recovery. Tube evaluation, root G0, root Gl/MV evaluation, predictor, exterior evaluation, c0a source, monotone source, endpoint-R source, manifest/replay key sets, reason sets except for recording the refinement trace, and every unrelated work-accounting path are outside scope and must remain unchanged.

## 2. Deterministic dyadic refinement rule

For each failed ordinary root Gt t-cell `[a,b]`, define the exact midpoint `m=(a+b)/2` using the existing exact `Fraction` representation. Producer and checker must use the same exact rational endpoints and the same left-to-right child ordering.

Level 1 replaces only that failed parent cell by the two children `[a,m]` and `[m,b]`. Each child is evaluated by the same lineage Gt evaluator, with the same lambda interval and the same Gt s-panel count as the parent root-Gt call.

If both level-1 children satisfy `value.upper() < 0`, the parent guard is recovered and no deeper evaluation is permitted for that parent.

If one or both level-1 children fail the guard, only the failed child or children are bisected once more at their exact dyadic midpoint. This is level 2. Passed level-1 children are final and must not be reevaluated.

The maximum refinement depth is exactly `k=2` relative to the failed ordinary cell. Therefore a single ordinary failed cell can produce at most four level-2 leaves. There is no open-ended refinement, no adaptive depth beyond level 2, and no "refine until pass" behavior.

After level 2, if any leaf still fails `value.upper() < 0`, the parent ordinary cell remains unresolved and root localization must terminate fail-closed with the existing reason `GT_DIVISION_GUARD_UNRESOLVED`. The amendment does not authorize a new success condition, epsilon sign test, midpoint sign substitution, or heuristic acceptance.

## 3. Work accounting and ledger trace

Every child Gt evaluation is charged explicitly using the existing root-Gt panel work unit. No child evaluation is free, hidden, amortized, or charged to another stage. The ordinary 16-cell evaluation retains its existing charge; refinement adds only the work of the actually evaluated children.

The root step record must preserve the ordinary `Gt_cells` information and add a deterministic refinement trace for each ordinary failed cell that triggered this amendment. The trace schema is fixed as follows:

`Gt_refinement = [{"cell_index": i, "parent_t_cell": (a,b), "levels": [...]}, ...]`

Each `levels` entry must record `level` equal to 1 or 2 and a left-to-right `children` array. Each child record must contain at minimum:

`{"t_cell": (lo,hi), "Gt": <existing Arb snapshot form>, "guard": bool, "work": ROOT_GT_PANELS}`

Only children actually evaluated are recorded. Level 2 records only descendants of failed level-1 children. The order is deterministic: increasing ordinary `cell_index`, then increasing level, then left child before right child.

The final ordinary-cell guard used by root localization is true if and only if either the ordinary cell already passed, or every terminal leaf generated for that failed cell by this fixed k=2 schedule passes. If refinement reaches level 2 with a failed terminal leaf, the final guard is false.

The existing nonfinite handling remains binding. Any nonfinite or evaluator exception encountered in a child must follow the existing fail-closed root nonfinite/unresolved policy; this amendment does not convert a nonfinite child into a sign result.

## 4. Predeclared controls

### V29-C1 — coarse-105 depth-1 cell-15 replay

The executable preflight must replay the previously observed coarse-105, depth-1 ordinary failed root-Gt cell 15 using the current canonical interval data:

- lambda interval: `[93/160, 931/1600]`;
- parent t-cell: `[545276670493/549755813888, 549571637789/549755813888]`;
- exact level-1 midpoint: `547424154141/549755813888`;
- left child: `[545276670493/549755813888, 547424154141/549755813888]`;
- right child: `[547424154141/549755813888, 549571637789/549755813888]`.

For both level-1 children the control must require a strictly positive certified q lower endpoint for every underlying ordinary s-panel for which q positivity is required, and must require the integrated child `Gt.upper() < 0`.

The producer-side observed diagnostic targets to be matched by enclosure overlap/containment, not decimal equality, are:

- left child: `Gt.upper() ≈ -1.21884066913933`, minimum certified `q.lower ≈ 6.07294463818e-6`;
- right child: `Gt.upper() ≈ -0.826293135430`, minimum certified `q.lower ≈ 3.62915150658e-8`.

The checker must independently obtain compatible enclosing results under its lineage implementation. The binding pass condition is the exact sign condition (`q.lower > 0`, `Gt.upper() < 0`) on both children; the decimal values are diagnostic cross-check targets only.

### V29-C2 — no-activation control

A root Gt ordinary cell whose existing evaluation already satisfies `value.upper() < 0` must produce no refinement child evaluations and no nonempty refinement trace for that cell. The control must verify both zero added refinement work and absence of child records for the passed cell.

### V29-C3 — bounded fail-closed control

A control-only injected evaluator result or isolated helper test must force an ordinary failed cell to remain failed through level 1 and through at least one level-2 leaf. The refinement engine must stop after level 2, must perform no level-3 evaluation, and must return/propagate `GT_DIVISION_GUARD_UNRESOLVED`.

The control must also verify the deterministic maximum-depth/leaf bound: no terminal path deeper than level 2 and no more than four terminal leaves per ordinary failed parent cell.

### V29-C4 — accounting and trace identity

For a fixed synthetic pattern of pass/fail children, the control must verify that added work equals exactly the number of child evaluations times `ROOT_GT_PANELS`, and that the serialized refinement trace contains exactly the evaluated children in deterministic order with their exact rational endpoints, level numbers, guard booleans, Arb snapshots, and per-child work.

No control in this section authorizes a change to Gt mathematics, q mathematics, chart selection, s-panel partitioning, or root Newton algebra.

## 5. Supersession, frozen predecessors, and required sequence

This v2.9 amendment is additive to, and does not reopen or weaken, the positive-q and regrouping requirements frozen by the following predecessor documents:

1. `analysis/GLOBAL_AXIAL_C1B_POSITIVE_Q_PRE_RUN_AMENDMENT_V2_8.md`
   - commit `cd1f06ad7b270bd11ddecb7f95deed27bb50f97e`
   - Git blob `fa544b633f1f052a379b5918b442f2394b395494`
2. `analysis/GLOBAL_AXIAL_C1B_POSITIVE_Q_PRE_RUN_AMENDMENT_V2_8_1.md`
   - commit `925fb382f787279547702d02d5bc1fefa607deb6`
   - Git blob `cd42fe1f2369667cdb43c898e84a55960a7e77fb`
3. `analysis/GLOBAL_AXIAL_C1B_POSITIVE_Q_PRE_RUN_AMENDMENT_V2_8_2.md`
   - commit `0519b6332bd17b626f8c95a3ddf06c9c59bbdf86`
   - Git blob `177c2195026248364c0503a42ad609215097a901`
4. `analysis/GLOBAL_AXIAL_C1B_POSITIVE_Q_PRE_RUN_AMENDMENT_V2_8_3.md`
   - commit `dae7b051e5a2ab7c1fb217c077a1b4591e61f015`
   - Git blob `15f7e92a02b1fac08854943c6275f93323a527dd`

The current executable parent state for this predeclaration is commit `02e83105c398e8eb43579d7deda4ad532de42c9b`. No executable source change is part of this predeclare commit.

The required sequence is binding:

    v2.9 predeclare document committed alone
      -> chat-side verbatim/content audit PASS
      -> implementation commit limited to the predeclared root-Gt refinement and controls
      -> local static/control checks; no machine evidence claim
      -> raw byte audit of every changed executable file against its parent
      -> chat-side byte-chain verification and explicit implementation adjudication
      -> only after explicit approval: push / manifest refresh as required by changed pinned blobs
      -> official machine preflight including V29-C1..C4 and all carried-forward controls
      -> only if preflight PASS: NEW Phase-1 RUN_DIR; never resume the failed historical run
      -> Phase 2 remains separately gated and requires explicit authorization.

The audit package for this predeclare commit and for the later implementation must use the established pin format: Path, parent commit, commit, Git blob, Bytes, Lines, SHA-256, complete raw file content, and complete parent-to-commit diff. Every pasted raw chunk must carry its exact line count and SHA-256 computed from the transmitted bytes, with final newlines preserved.

Until chat-side verbatim audit of this v2.9 predeclare passes, no v2.9 executable implementation, push, manifest refresh, official machine preflight, or new Phase-1 run is authorized.
