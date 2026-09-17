# C1b parametric mean-value cross-lineage comparison addendum v2.1

Status: `PREDECLARED_ADDENDUM / IMPLEMENTATION_AUDIT_PENDING / MACHINE_NOT_RUN / NOT_BINDING`

This addendum is committed after the PREDECLARED parametric mean-value root-localization amendment and before any implementation commit. It supersedes only the cross-lineage comparison rule for the new interval-valued `T_*` enclosures. It does not weaken either lineage's obligation to certify the root independently.

The purpose of this addendum is to distinguish exact logical-state equality from lineage-specific interval evidence. Producer and checker use different Arb precisions and independent transcriptions; therefore their outward-rounded `T_*` endpoints need not be exactly equal even when both independently certify the same root branch.

## A. Three-layer comparison rule

Every accepted slab is audited under all three layers below. No gating decision may be moved from the exact-equality layer into the lineage-independent evidence layer.

### A.1 Exact-equality layer — mismatch is fail-closed

The following producer/checker objects must agree exactly:

```text
accepted slab order,
exact rational lambda endpoints for every replayed slab,
refinement-tree topology and refinement depth,
predictor t_c as an exact rational,
left/right clamp kind and exact t_minus/t_plus values,
identity of every box on which corner_hull is applied,
all logical guard truth values, including upper(Gt)<0 and empty-intersection status,
logical decision for each attempted slab: ACCEPT / REFINE / ABORT.
```

Any mismatch in this layer is `FAIL_CLOSED / NOT_EVIDENCE`.
### A.2 Lineage-independent proof layer — exact equality is not required

Each lineage must independently provide and retain its own certified values for:

```text
T_* and width(T_*) <= 1/128,
parametric mean-value iteration count <= 8,
G0, Gt, Gl, Gpar, and N_k as canonical mid/rad/lower/upper records,
actual charged work for each root-localization step and for the slab,
its own ledger record and hash chain.
```

Producer and checker endpoint equality is not required for these interval-valued quantities. The absence of an equality requirement does not permit either lineage to use values, intervals, work records, or runtime state from the other lineage.

### A.3 Cross-lineage consistency layer — failure is fail-closed

For every slab accepted by both lineages, require

```text
T_*^producer intersect T_*^checker is nonempty.
```

Predictor acceptance is evaluated independently in each lineage using that lineage's exact rational midpoint of its own certified `T_*`:

```text
|t_c - mid(T_*^producer)| <= 1/64,
|t_c - mid(T_*^checker)|  <= 1/64.
```

Final acceptance requires both predicates to be true. If exactly one lineage accepts the predictor, or if the two certified `T_*` enclosures are disjoint, the comparison is `FAIL_CLOSED / NOT_EVIDENCE`.
## B. Checker replay rule

The producer alone generates the exact rational slab/refinement tree under the existing left-child-first and `MAX_DEPTH=3` policy. The checker does not generate an alternative tree.

For cross-lineage verification, the checker must replay the producer's exact rational slab sequence and refinement tree as fixed input. The checker may not introduce an additional lambda bisection, change child order, change depth, skip a producer slab, or rescue a producer branch with a checker-only refinement.

If checker root localization returns `UNRESOLVED` on any producer-replayed slab that the producer accepted, the result is

```text
CHECKER_REPLAY_UNRESOLVED / FAIL_CLOSED / NOT_EVIDENCE.
```

It is not converted into checker-side refinement. Likewise, any mismatch in the replayed tree or exact slab endpoints is an A.1 exact-equality failure.

The producer tree-generation rules themselves remain unchanged and continue to be audited independently: exact lambda bisection only, left child before right child, and depth not exceeding 3.

## C. Comparison record and supersession

This addendum supersedes the sentence in the PREDECLARED amendment §8 that could be read as requiring producer/checker exact equality of interval endpoints for `T_k`, `N_k`, `T_{k+1}`, or final `T_*`.

The comparison record must instead place the producer and checker step sequences side by side. For every step it must record:

```text
T_k, t_ref, lambda_c,
G0, Gt, Gl, Gpar, N_k,
T_{k+1}, width,
guard results,
iteration count,
actual charged work,
final T_* where applicable.
```

Each recorded row or field must be labelled as `A1_EXACT_EQUALITY`, `A2_LINEAGE_INDEPENDENT`, or `A3_CROSS_LINEAGE_CONSISTENCY`. A gating decision, exact slab identity, exact clamp state, predictor `t_c`, refinement decision, or guard truth value may never be classified as A.2.
## D. Reported non-gating smoke control

The pre-commit development smoke on the historical depth-3 regression box reported:

```text
Lambda = [9/20, 2881/6400]
T_0    = [9/16, 19/32]
producer: 2 iterations, width approximately 6.292e-3, work 98304
checker:  2 iterations, width approximately 7.599e-3, work 98304
producer/checker T_* overlap: nonempty
producer/checker midpoint difference: approximately 1e-4
```

These values are `REPORTED / NON_GATING`. The checker width is only about 2.7% below the `1/128` target, so a later evidence run may legitimately require additional checker mean-value iterations on some slabs. This observation does not authorize any change to the target, panel counts, precision, iteration cap, refinement depth, or ceilings.

Failure of a future pinned implementation to satisfy the exact predicates is not excused by agreement with these reported decimals.

## E. Invariants preserved by this addendum

The following remain exactly as declared in the existing C1b contract stack and parametric mean-value amendment:

```text
domain,
predictor construction,
tube width,
monotonicity gate and wall signs,
clamp rules and corner treatment,
T0/T1/T2 and E0/E1/E2 policies,
MAX_DEPTH = 3,
predictor acceptance threshold = 1/64,
ROOT_TARGET = 1/128,
ROOT_MV_STEPS = 8,
root panels: G0/Gt/Gl = 32768/8192/8192,
Arb precision: producer 160 bits / checker 192 bits,
all accepted/attempted/work ceilings.
```

This addendum changes only the cross-lineage comparison semantics for interval-valued root enclosures and the checker replay obligation needed to audit them.