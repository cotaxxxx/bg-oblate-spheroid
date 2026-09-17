# GLOBAL AXIAL C1B — BUNDLED ROOT-GT / T2 ENDPOINT REFINEMENT PRE-RUN AMENDMENT v2.10

Status: FROZEN / CHAT_AUDIT_PASS / MACHINE_NOT_RUN / NOT_EVIDENCE

This document predeclares the single bundled canonical implementation that combines:

1. the already-predeclared v2.9 bounded root-Gt t refinement, unchanged; and
2. a new bounded T2 endpoint-strip t refinement, specified below.

No canonical implementation may begin until this document has passed chat-side verbatim audit and has been committed as the frozen predeclare ancestor required by §8.

## 1. Scope

The new v2.10 refinement applies only to the T2 tube stage and only to a T2 t-cell satisfying:

- `t_hi == 1`;
- the ordinary T2 evaluation is finite on every one of the existing 16 λ subcells; and
- at least one of those 16 λ subcells does not satisfy the existing required sign `Gt.upper() < 0`.

A nonfinite T2 endpoint-strip evaluation does NOT activate v2.10 refinement.

Any nonfinite T2 endpoint-strip evaluation remains on the existing nonfinite handling and serialized-reason path. v2.10 is not authorized to subdivide, retry, reinterpret, or otherwise repair a nonfinite evaluation.

All other T2 t-strips are unchanged.

The existing T2 parameters remain unchanged:

- `nt = 32`;
- `nl = 16`;
- `panels = 8192`;

T0 and T1 are unchanged.

The existing λ grid is unchanged.

The existing s partition, chart selection, tube acceptance rule, left/right wall tests, nonfinite handling, work accounting outside the added endpoint child evaluations, and all other numerical paths are unchanged except where this document explicitly authorizes the endpoint refinement.

No refinement introduced here may activate on a T2 endpoint strip that already satisfies the existing T2 sign requirement.

## 2. Deterministic endpoint refinement procedure

The refinement unit is the complete T2 endpoint t-strip across all 16 existing λ subcells.

The 16 λ subcells do not refine independently.

For an activated T2 endpoint strip `[t_lo, 1]`, split the complete t-strip at its exact rational midpoint. The same t split is applied simultaneously to all 16 existing λ subcells.

At every refinement level:

1. evaluate the non-endpoint child on all 16 λ subcells using the same T2 evaluator, the same λ subdivision, the same `panels = 8192`, and the same sign rule `Gt.upper() < 0`;

2. the non-endpoint child passes only if all 16 λ-subcell evaluations are finite and all 16 satisfy `Gt.upper() < 0`;

3. if even one non-endpoint λ subcell is nonfinite or fails `Gt.upper() < 0`, the complete endpoint refinement fails closed immediately;

4. evaluate the endpoint child containing `t = 1` on all 16 λ subcells;

5. the endpoint child closes at that level only if all 16 λ-subcell evaluations are finite and all 16 satisfy `Gt.upper() < 0`;

6. if the endpoint child does not close, but all 16 endpoint-child λ-subcell evaluations are finite, only that complete endpoint child is eligible for the next t refinement level;

7. if any endpoint-child λ-subcell evaluation is nonfinite, v2.10 refinement terminates and the existing nonfinite path applies; a nonfinite result must not be repaired by further v2.10 splitting.

Thus the t-refinement decision is strip-wide: one failing sign subcell causes the entire finite endpoint child to continue, and acceptance requires 16/16 PASS.

Only the endpoint child containing `t = 1` may be recursively subdivided.

The maximum additional endpoint-refinement depth is 4.

No open-ended refinement is permitted.

If any required non-endpoint sibling fails the strip-wide rule above, the refinement fails closed.

If the endpoint child still fails the finite sign gate at the level-4 bound, the refinement fails closed.

Failure uses the existing `TUBE` failure path and existing coarse-skip behavior.

No new success category, failure category, or alternate acceptance word is authorized.

## 3. Serialized refinement trace

Every activated endpoint refinement must serialize a deterministic trace.

For every evaluated child at every level, the trace must include at minimum:

- refinement level;
- child role: `non_endpoint` or `endpoint`;
- exact rational `t_lo`;
- exact rational `t_hi`;
- exact rational λ-subcell endpoints;
- finite boolean;
- signed `Gt.upper()` enclosure value;
- boolean result of the existing sign gate `Gt.upper() < 0`.

The trace must preserve deterministic child order.

The implementation may serialize additional diagnostic fields, but those additions must not change the gate.

The implementation must retain enough information to reconstruct whether each parent was closed by its two required children and at what endpoint depth closure occurred.

Every additional child evaluation introduced by v2.10 MUST be charged to the existing work accounting.

The work charge must reflect the actual λ-subcell and panel evaluations performed by the endpoint refinement.

No v2.10 child evaluation may be omitted from `work_total` or treated as uncharged diagnostic work.

The canonical gate remains only the existing finite/sign conditions described above.

## 4. Exact corner contact and analytic fallback status

The offline diagnostic established an exact corner-contact location with

`q_min = 0`

at the geometric corner

`s = 0`, `mu = 1`, `t = 1`.

This exact contact is a known feature of the endpoint geometry and is not itself a new failure condition.

The current v2.10 design does NOT introduce an analytic `t -> 1` upper bound.

An analytic endpoint bound or closed-form endpoint treatment is retained only as a named escalation path if a persistent endpoint floor reappears under the bounded canonical implementation.

No such analytic treatment is authorized by this amendment.

## 5. Diagnostic provenance

The design is based on two local research-machine artifacts.

Both are DIAGNOSTIC_ONLY / NOT_EVIDENCE and are not promoted to binding certification evidence.

1. `offline_dyadic_child_and_corner.json`
   - SHA-256:
     `bb25f97986cba27133750c0b6e30a1d0716524eefa5cb83f5c5c2fe02d143fbd`
   - bytes: `25370`
   - lines: `590`

2. `actual_T2_lambda16_endpoint_refinement.json`
   - SHA-256:
     `94cf4ec2d986611d6de1c27fc47f142a3edf1b45df2225046507aa041b97bba0`
   - bytes: `47663`
   - lines: `1092`

These hashes identify the exact diagnostic artifacts consulted by this predeclare.

They do not upgrade those artifacts beyond DIAGNOSTIC_ONLY.

The offline diagnostic observed, for the coarse-115 failed depth-3 T2 endpoint strip, that:

- the level-1 non-endpoint child passed;
- the level-1 endpoint child failed;
- the level-2 non-endpoint sibling passed on the actual T2 λ subdivision, 16/16 finite and 16/16 `Gt.upper() < 0`;
- the level-2 endpoint child still failed;
- the endpoint lineage closed by level 3;
- level 4 remained passing.

These observations motivate, but do not prove in advance, the bounded canonical rule.

## 6. Predeclared run prediction

The following is a falsifiable pre-run prediction, not a certification claim:

The contiguous scout TUBE fault band consisting of coarse cells 105 through 139, inclusive, will close under the bundled canonical implementation with endpoint refinement depth no greater than 4, and the resulting TUBE skip count over those 35 coarse cells will be zero.

This prediction is evaluated exactly as written.

If any one of coarse cells 105 through 139 reaches endpoint refinement depth 4 without closure, or otherwise remains a TUBE skip under the authorized procedure, the prediction is recorded as FAIL.

The implementation must not rename or reinterpret a remaining TUBE failure as success.

The existing fail-closed behavior remains binding.

## 7. Root / MV freeze and bundled v2.9 scope

The root-side component of the bundled implementation is exactly the already-predeclared v2.9 root-Gt bounded t refinement, as clarified by v2.9.1.

No additional root, MV, predictor, root-grid, root-panel, root-step, or root-localization numerical change is authorized by v2.10.

In particular, v2.10 may not be used as authority to modify the root/MV evaluator, its grids, its panel counts, its accepted guard, or its fail-closed behavior beyond the already frozen v2.9/v2.9.1 specification.

The scout census showed the later TUBE band to be a distinct blocker.

The bundled implementation therefore combines the already-frozen v2.9 root repair with the new T2 endpoint repair, but does not broaden the v2.9 root design.

## 8. Canonical ancestry and single bundled implementation

The canonical ancestry is binding.

The relevant predeclare chain is:

- v2.9 predeclare commit:
  `8bbd159b35db8eb1c203301ad6291e99d10788a6`
- v2.9.1 clarification commit:
  `c0f4d2bc4a0a18acdf39f2f4eec0b0bfff152b6f`
- the future frozen v2.10 predeclare commit created from this document after chat audit.

The bundled canonical implementation commit MUST:

1. be a descendant of `8bbd159b35db8eb1c203301ad6291e99d10788a6`;
2. include `c0f4d2bc4a0a18acdf39f2f4eec0b0bfff152b6f` in its ancestry;
3. have the frozen v2.10 predeclare commit as its immediate parent; and
4. implement v2.9 and v2.10 together in a single bundled canonical implementation commit.

No separate canonical v2.9-only implementation commit is authorized between the frozen v2.10 predeclare and the bundled implementation.

No history rewrite is authorized.

If a clarification to this v2.10 document is required before implementation, that clarification must itself be committed after the v2.10 predeclare and before implementation, and the bundled implementation must have the final clarification commit as its immediate parent.

## 9. Controls required before any official Phase 1 rerun

The bundled implementation must include deterministic controls sufficient to verify at least the following:

1. v2.9 root-Gt refinement still satisfies its previously frozen activation, deterministic split, bounded-depth, nonactivation, and fail-closed controls.

2. v2.10 does not activate outside T2 endpoint strips with `t_hi == 1`.

3. v2.10 does not activate on an already passing T2 endpoint strip.

4. For the frozen coarse-115 diagnostic coordinate, the canonical T2 endpoint refinement reproduces the required lineage shape:
   - level-1 non-endpoint child PASS;
   - endpoint child may continue;
   - level-2 non-endpoint sibling PASS;
   - endpoint lineage closes by depth no greater than 4.

5. An artificial endpoint case that still fails at the depth-4 bound returns the existing fail-closed TUBE outcome.

6. The serialized trace contains every child evaluation required by §3.

7. Existing T0, T1, non-endpoint T2 behavior, grids, panel counts, and unrelated work paths remain unchanged.

The exact control implementation may differ in local structure, but the above behaviors are binding.

## 10. Evidence boundary and execution order

The required order is:

1. draft this v2.10 predeclare in chat;
2. complete chat-side verbatim audit;
3. commit the frozen v2.10 predeclare on the canonical ancestry;
4. perform no canonical numerical implementation before that freeze;
5. create the single bundled v2.9 + v2.10 implementation commit with the ancestry required by §8;
6. perform raw source / byte audit of the implementation;
7. refresh pins and manifest only after the implementation bytes are accepted;
8. run official preflight;
9. only then run the next official Phase 1.

The two offline JSON files in §5 remain DIAGNOSTIC_ONLY throughout.

This document predeclares behavior. It is not machine evidence and does not itself certify closure of the TUBE band.

END OF v2.10 PREDECLARE
