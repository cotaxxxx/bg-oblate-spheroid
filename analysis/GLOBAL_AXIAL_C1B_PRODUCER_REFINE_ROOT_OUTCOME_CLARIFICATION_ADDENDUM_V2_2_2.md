# C1b producer-refine root-outcome comparison clarification addendum v2.2.2

Status: `PREDECLARED_ADDENDUM / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_BINDING`

This addendum is committed after v2.2.1 and before the correction implementation. It clarifies only the slab-level scope of the v2.2.1 A.1 root-localization outcome comparison when checker replays the producer-fixed refinement tree. All v2.1 replay, A.1/A.2/A.3 comparison, and fail-closed obligations remain otherwise unchanged.

## 1. Scope of slab-level root-outcome equality

The v2.2.1 A.1 requirement that producer and checker agree on the slab-level root-localization outcome applies to every producer `ACCEPT` slab.

For such a producer-accepted slab, both lineages must have

```text
RESOLVED_WITH_CERTIFIED_T_STAR
```

and checker `UNRESOLVED` remains the existing hard failure

```text
CHECKER_REPLAY_UNRESOLVED / FAIL_CLOSED / NOT_EVIDENCE.
```

For a producer `REFINE` or producer `ABORT` slab, checker must still replay the producer-fixed slab and refinement decision exactly, but checker is not required to reproduce the producer's root-localization outcome on that slab. The checker lineage's own root result on such a nonaccepted producer slab is recorded as `A2_LINEAGE_INDEPENDENT` proof data and does not alter the producer-fixed tree.

In particular, a checker `RESOLVED_WITH_CERTIFIED_T_STAR` result on a producer `REFINE` slab does not authorize checker-side acceptance, pruning, child suppression, alternative refinement, or any tree change. The producer decision remains the A.1 replay decision.

## 2. No weakening of accepted-leaf evidence

This clarification does not weaken the evidence requirement on accepted leaves. Every producer `ACCEPT` slab still requires:

```text
checker RESOLVED_WITH_CERTIFIED_T_STAR,
nonempty producer/checker T_star intersection,
producer midpoint acceptance <= 1/64,
checker midpoint acceptance <= 1/64,
all remaining v2.1 A.1 exact-equality predicates,
and the same logical ACCEPT decision.
```

Only accepted leaves contribute to the final certified covering evidence. Therefore allowing a checker to resolve a producer-refined ancestor without forcing root-outcome equality cannot create evidence that the producer did not establish and cannot weaken fail-closed behavior.

## 3. Comparison-record labels
The comparison record must label the producer decision and checker replay behavior as follows:

```text
A1_EXACT_EQUALITY:
  producer-fixed slab identity and exact rational lambda endpoints,
  producer-fixed refinement-tree position and depth,
  producer-fixed logical decision ACCEPT / REFINE / ABORT,
  producer-ACCEPT slab root outcome RESOLVED_WITH_CERTIFIED_T_STAR,
  tube-stage corner_hull application-box identity,
  all other common-exact-box A.1 guards and states already required by v2.1/v2.2.1.

A2_LINEAGE_INDEPENDENT:
  checker root-localization result on a producer-REFINE or producer-ABORT slab,
  and the existing lineage-specific root proof data from v2.2.1.
```

For producer `REFINE` and `ABORT` slabs, the checker result must be recorded but cannot modify the replay decision or tree. For producer `ACCEPT` slabs, root-outcome equality is mandatory and checker `UNRESOLVED` is fail-closed.

## 4. Replay and resume invariants

The checker replay input remains restricted to the exact A.1 producer data authorized by v2.1; no producer interval evidence such as `T_*`, `G0`, `Gt`, `Gl`, `Gpar`, or `N_k` may be supplied as checker numerical input.

Producer-to-checker two-phase replay, resume pin equality, independent checker work charging, and all existing ceilings remain unchanged. This addendum authorizes no checker-side refinement, no tree optimization, and no numerical threshold change.
