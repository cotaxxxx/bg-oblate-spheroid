# D-OB P2 — D Problem (Cross-sectional Monotonicity) Track Kick-off — DRAFT

Status: DRAFT / AWAITING CHAT AUDIT / DIAGNOSTIC / NOT_EVIDENCE

## §0. Restart boundary and inherited assets

### 0.1 Post-comparison Judge

The SPEC V3 candidate-comparison chapter is CLOSED with zero adoption. The next main line is the **D problem / cross-sectional monotonicity track**. Plan C `(a)+(c)` remains reserved under the frozen v2 sole-revival clause; `(b)` geometric redesign is placed last in the current priority order. This priority decision does not itself prove or certify any mathematical claim.

The comparison closure is recorded on the comparison branch by finalization commit `ab683fc33543dcb2cd3f5e0a0eeee7ef2c7031e0`; its closure report remains `DIAGNOSTIC / NOT_EVIDENCE`, and D-P2 remains `NOT_CERTIFIED`.

### 0.2 Inherited Phase 0 diagnostic infrastructure

The Phase 0 H-sign infrastructure is inherited as a **numerical diagnostic instrument**, not as formal evidence and not as a formal producer/checker component.

Pinned identities currently available in the D-OB tree:

- `tools/d_ob_p2/candidate_comparison_harness.py` SHA-256 `4014210732502fa6c3f4f4aa9348b1df8c7384a921b3ba8f426891c66725226e`.
- independent `geom/F/Frho` source pin recorded by the frozen Phase 0 predeclare: `tools/d_ob_p2/independent_H_sign.py` SHA-256 `2dcd16673c214369ba0555e653dae51fca7d3f3cf13c83aeac4fd000d5bfccd7` from commit `dabc2a3b`.
- Phase 0 decision: B44 = `POSITIVE=44, NEGATIVE=0, INCONCLUSIVE=0` (P0-A), diagnostic only.
- frozen v2 file SHA-256 `06fe184c565982cf295d03f7dd421662ec7672a48686229d5a44d69b5badbb7d`.

The harness has strong operational reproducibility and may be reused for D-track point diagnostics. Any previously recorded multi-environment bit-reproduction belongs to the diagnostic reproducibility ledger only. It **must not** be described as formal evidence, imported into a formal RUN_DIR, or substituted for an independent formal producer/checker if a future proof/certification stage requires one.

### 0.3 Etiology inherited from candidate comparison

The comparison establishes the following **diagnostic design facts**:

1. The B44 band is not removed by the tested resource, cell-depth, box-depth, regular-selection, or RHO0 changes.
2. Cell budget is useful for the N/enclosure-width band but does not close D-P2.
3. RHO0 changes are structurally inactive in the deep-near region measured by the comparison.
4. Therefore the unresolved B mechanism should not be treated as a resource/scale/RHO0 tuning problem. The D track targets the underlying analytic sign/monotonicity structure instead.

These are design inferences from diagnostics, not theorem statements.

### 0.4 Analytic target

The D-track target is sharpened to:

> Establish a sound analytic route to **H > 0 on the near-column domain**, beginning with the unresolved band represented by the `7,7,0` near-column region and ultimately extending to the full required parameter domain P.

If a valid theorem establishes the required H positivity on the full domain needed by D-P2, the intended consequence is analytic elimination of the corresponding two-dimensional stationary-point obstruction, including the B band, so that the present 7,662 near-column unresolved boxes need not be discharged one-by-one by the existing numerical enclosure. **This is a target implication, not an established result.** Its exact theorem-to-D-P2 handoff must be proved and audited before any certification claim.

### 0.5 Current diagnostic support

Current support for the H>0 conjectural direction is diagnostic:

- B44 Phase 0: 44/44 conclusive POSITIVE by the frozen two-route sign diagnostic.
- N-band independent H computations are positive. The current `D_OB_P2_REVISION_DIRECTION_PREDECLARE.md` records approximately `+1.16` to `+1.25`; the restart instruction ledger reports `+1.08` to `+1.25`. **This numerical-range discrepancy must be resolved against pinned source artifacts before the next predeclare is frozen.** It does not affect the common observed sign.
- sigma-split / regularity work supplies raw C1-regularity premises relevant to analytic decomposition, but remains diagnostic until its exact hypotheses and domain are re-pinned for the D track.

No pointwise floating computation is promoted to an interval proof or global theorem.

### 0.6 Existing P0–P4 program

The existing D-track **P0–P4 program is incorporated by reference and is not redefined by this kick-off note**. This note only supplies the new §0 restart boundary: inherited diagnostic infrastructure, post-comparison B-band etiology, and the sharpened near-column H>0 target.

Before any P0–P4 execution resumes, the current authoritative P0–P4 text and its pins must be identified and countersigned. If the authoritative text cannot be located or its identity is ambiguous, execution is BLOCKED; this kick-off note must not be used to reconstruct P0–P4 from memory.

### 0.7 Governance inherited from candidate comparison

The D track adopts the established discipline:

1. predeclare before computation;
2. pin source, inputs, configuration and target domain;
3. chat audit and **pre-ignition countersign** as the default rule;
4. fail closed on pin/domain/identity ambiguity;
5. version-up → re-audit → re-freeze for post-result changes;
6. preserve diagnostic/formal evidence separation;
7. audit artifacts by a line independent from the producing line where formal evidence is eventually sought.

No D-track computation is authorized by this draft. The next executable state begins only after the authoritative P0–P4 program is recovered, §0 is reconciled with it, a versioned predeclare is frozen, and the relevant stage receives its required countersign.

## §1. Reserved post-D alternatives

This kick-off does not erase the closure-report alternatives:

- Plan C `(a)+(c)` remains legally re-proposable only as a **new-version item**, under the v2 clause: after candidate (c), `(a)+(c)` may be proposed as a new version item; implicit revival is forbidden.
- `(b)` geometric/coupled redesign remains available as a later route, not the present main line.
- `(e)` analytic handoff remains conceptually available but requires its own sound bound/domain/handoff specification.

The present Judge selects only the **D problem track as the next main line**.

## §2. Evidence boundary

Everything in this kick-off note is `DIAGNOSTIC / NOT_EVIDENCE`. D-P2 remains `NOT_CERTIFIED`. Candidate-comparison diagnostics, Phase 0 diagnostics, and any future D-track exploratory computation do not become formal evidence merely by being reproducible or cited here.
