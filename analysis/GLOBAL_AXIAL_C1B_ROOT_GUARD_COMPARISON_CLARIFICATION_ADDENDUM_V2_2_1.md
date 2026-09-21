# C1b root guard comparison clarification addendum v2.2.1

Status: `PREDECLARED_ADDENDUM / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_BINDING`

This addendum is committed after addendum v2.2 and before the correction implementation. It clarifies only the cross-lineage classification of root-localization guard results and iteration counts. Addendum v2.1, addendum v2.2, and all fail-closed obligations remain otherwise unchanged.

## 1. Root-localization guard classification

The strict per-cell derivative guards and empty-intersection checks executed inside parametric mean-value root localization are lineage-internal gating conditions because they are evaluated on that lineage's current certified `T_k`, whose endpoints may differ between producer and checker.

Accordingly, for each lineage independently:

```text
all required per-cell upper(Gt_j) < 0 predicates must hold before division;
empty intersection is a hard fail-closed contradiction/error;
a failed derivative guard makes that lineage root localization UNRESOLVED;
ROOT_MV_STEPS remains at most 8.
```

These predicates are not weakened, skipped, or converted into non-gating diagnostics.
## 2. Cross-lineage comparison scope

Cross-lineage `A1_EXACT_EQUALITY` does not require equality of the per-iteration root-localization guard truth-value sequence or of the root-localization iteration count. Those quantities are evaluated on lineage-specific `T_k` and therefore belong to the lineage-internal root proof record.

The `A1_EXACT_EQUALITY` comparison is instead applied, at slab level, to the root-localization outcome and to the existing logical slab decision:

```text
root-localization outcome: RESOLVED_WITH_CERTIFIED_T_STAR or UNRESOLVED;
logical slab decision: ACCEPT / REFINE / ABORT.
```

For a producer-accepted slab, checker `UNRESOLVED` remains exactly the v2.1 §B hard failure

```text
CHECKER_REPLAY_UNRESOLVED / FAIL_CLOSED / NOT_EVIDENCE.
```

Thus a lineage-internal guard failure cannot be hidden by omitting per-step cross-lineage equality: it propagates to a slab-level root-localization mismatch or checker replay failure and remains fail-closed.
## 3. Tube/exterior guards remain A.1

The v2.1 requirement that guard truth values may not be classified as A.2 is retained for guards evaluated by producer and checker on the same exact rational boxes. In particular, tube-stage and exterior-stage guard truth values on their common exact boxes remain `A1_EXACT_EQUALITY` and any mismatch is fail-closed.

For avoidance of ambiguity, the v2.1 §C phrase that a “guard truth value may never be classified as A.2” is henceforth read as applying to guard predicates evaluated on the same exact rational box in both lineages. It does not impose cross-lineage equality on root-localization per-step guards evaluated on lineage-specific `T_k` or on their lineage-derived 16-cell subdivisions.

The root-localization per-step guard records, their 16-cell partitions, `Gt_j`, `Gt_hull`, empty-intersection status within a lineage, and the number of iterations used by that lineage are recorded as lineage-specific proof data. Their failure semantics remain binding within that lineage.

## 4. Comparison-record labels

The comparison record must label fields consistently with this clarification:

```text
A1_EXACT_EQUALITY:
  exact slab identity and lambda endpoints,
  refinement tree/depth,
  exact predictor t_c,
  exact clamp kind and t_minus/t_plus,
  exact T_0 and ROOT_GT_T_CELLS=16,
  common-box tube/exterior guard truth values,
  slab-level root outcome RESOLVED_WITH_CERTIFIED_T_STAR / UNRESOLVED,
  logical slab decision ACCEPT / REFINE / ABORT.

A2_LINEAGE_INDEPENDENT:
  lineage-specific T_k and 16-cell root subdivisions,
  per-step root derivative guards,
  per-step empty-intersection status,
  root iteration count,
  G0/Gt_j/Gt_hull/Gl/Gpar/N_k/T_{k+1}, widths, and work.

A3_CROSS_LINEAGE_CONSISTENCY:
  nonempty intersection of final certified T_star intervals,
  independent 1/64 midpoint-acceptance predicates in both lineages.
```

A2 classification does not make any root guard non-gating; it only means its numerical truth value is not required to equal the other lineage's value at the same iteration index.
## 5. No weakening and implementation-audit carry-forward

This clarification cannot turn a failed lineage into accepted evidence. A root derivative-guard failure still returns `UNRESOLVED`; an empty intersection still stops fail-closed; a producer/checker slab-level root-outcome mismatch still fails A.1; checker failure on a producer-accepted slab still triggers `CHECKER_REPLAY_UNRESOLVED`; and final acceptance still requires the v2.1 A.3 overlap and dual midpoint-acceptance predicates.

All v2.2 constants, work ceilings, precisions, panels, root target, iteration cap, and lambda-refinement depth remain unchanged.

The correction implementation raw audit must additionally verify:

```text
Gt_hull lower endpoint = outward enclosure of min_j lower(Gt_j),
Gt_hull upper endpoint = outward enclosure of max_j upper(Gt_j),
all uniform T_k cell endpoints are constructed with Fraction only and no float path,
if b_k=1, the final root Gt cell touching t=1 executes corner_hull,
all Gt_j evaluations actually performed are charged in full, including before any fail-closed exit.
```

This addendum changes classification and cross-lineage comparison scope only; it authorizes no numerical threshold, panel, precision, work-ceiling, or refinement change.