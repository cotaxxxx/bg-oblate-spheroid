# GLOBAL AXIAL C1B — CONTROLS-FIX PRE-RUN AMENDMENT v2.10.1

Status: PREDECLARED / FROZEN / CHAT_AUDIT_PASS / MACHINE_NOT_RUN / NOT_EVIDENCE

This document predeclares a controls-only corrective revision to the frozen bundled v2.9 + v2.10 implementation design.

The previously created local implementation candidate
`1daa406d50177dc894efbfc59cf164c5e03721af`
is classified as `REJECTED_IMPLEMENTATION_CANDIDATE`.
It was never pushed and is not canonical implementation evidence.

Its SHA, four-file pins, and canonical parent-to-candidate diff SHA-256
`af31d132ed0b70f3e0628333e31a0d3c8d79adf6fc4ac7d81345af12f62622af`
are retained only as audit provenance.

The replacement canonical implementation must be recreated as one clean commit whose ancestry is governed by §7 below.
No executable implementation is authorized until this v2.10.1 document is frozen.

## 1. F1 — restore all monkeypatched root functions

In both producer and checker `v29_preflight_controls()`, the control saves `g_box`, `gt_box`, and `glam_box` as `saved_g`, `saved_gt`, and `saved_glam`.

The `finally` block MUST restore all three functions explicitly:

`g_box, gt_box, glam_box = saved_g, saved_gt, saved_glam`

The prior rejected candidate's restoration form is not accepted.
This correction is control hygiene only and authorizes no root numerical change.
## 2. F2 — V29-C3 propagation control

V29-C3 must be strengthened from helper-local failure detection to propagation verification.
The control must establish all of the following:

1. an ordinary root-Gt cell fails;
2. the fixed v2.9 level-1 / level-2 bounded refinement is exercised;
3. at least one terminal level-2 leaf remains failed;
4. the refinement result is `recovered == False`;
5. no level-3 root-Gt evaluation occurs;
6. the failure propagates through the root-localization decision path to the existing reason `GT_DIVISION_GUARD_UNRESOLVED`.

The control must verify the existing reason text exactly.
No new root failure word is authorized.
The production propagation behavior itself is unchanged from frozen v2.9.

## 3. F3 — V210-C5 end-to-end TUBE propagation control

V210-C5 must verify the full failure path rather than only the endpoint-refinement helper result.
The injected control case must force finite T2 endpoint-strip sign failure, bounded endpoint refinement through depth 4, continued sign failure at the depth-4 bound, no deeper refinement, fail-closed return, propagation through the ordinary tube decision path, and final existing ledger reason exactly `TUBE`.

No new failure category, success category, retry category, or substitute decision word is authorized.
This is a control-coverage change only; the frozen v2.10 production rule remains unchanged.

## 4. F4 — activation and unchanged-path controls

The v2.10 control set must directly verify all activation exclusions required by the frozen specification.
At minimum it must test:

1. T2 endpoint strip, `t_hi == T_HI`, finite 16/16, at least one sign failure: refinement activates.
2. T2 endpoint strip, `t_hi == T_HI`, finite 16/16, sign PASS 16/16: refinement does not activate.
3. T2 strip with `t_hi != T_HI`: refinement does not activate, regardless of otherwise eligible finite sign status.
4. T0: v2.10 endpoint refinement does not activate.
5. T1: v2.10 endpoint refinement does not activate.
6. nonfinite T2 endpoint strip: v2.10 refinement does not activate and the existing nonfinite handling path remains responsible.

The controls must also verify that ordinary T0, ordinary T1, and non-endpoint T2 evaluation retain their pre-v2.10 stage structure and decision semantics.
No change to their numerical evaluators is authorized.

## 5. Internal fail-kind to serialized reason mapping

This section records the current mapping and is descriptive and binding for audit interpretation only. It does NOT authorize a production behavior change.

| Internal condition | Nonfinite record present? | Serialized / terminal reason |
| --- | --- | --- |
| finite sign failure at depth-4 bound | no | `TUBE` |
| ordinary finite sibling sign failure | no | `TUBE` |
| Arb/nonfinite condition recorded by existing nonfinite mechanism | yes | existing `TUBE_NONFINITE` path |
| existing endpoint-domain nonfinite record | yes | existing `TUBE_NONFINITE` path |
| `ValueError` / `ZeroDivisionError` handled by the existing evaluator wrapper without adding a nonfinite record | no | `TUBE` |

Internal `fail_kind` is not declared to be in one-to-one correspondence with the serialized reason.
For existing `ValueError` / `ZeroDivisionError` handling, the evaluator returns failure, no new nonfinite record is introduced by that handling, and the terminal tube path therefore remains `TUBE`.
Any proposed change to this mapping requires a later predeclare amendment.
## 6. Authorized change surface and frozen numerical behavior

The replacement implementation is authorized to change only what is necessary to close F1 through F4 above and their associated control serialization or test plumbing.
The following remain frozen and unchanged:

- v2.10 §2 T2 endpoint-strip driving rule;
- strip-wide 16-λ-subcell behavior;
- exact rational midpoint subdivision;
- non-endpoint sibling 16/16 PASS requirement;
- endpoint-child 16/16 closure requirement;
- nonfinite non-repair rule;
- maximum T2 endpoint refinement depth 4;
- existing `TUBE` fail-closed decision;
- v2.10 §3 trace content and work charging;
- v2.9 root-Gt refinement depth 2;
- root/MV numerical formulas, grids, and panel counts;
- existing root sign guard;
- v2.10 §7 prohibition on additional root/MV numerical changes.

No new numerical algorithm is authorized.

### Kernel blob expectation

The rejected implementation candidate had producer kernel blob `284d591b9f47d360c78de2ef52e08112a329c037` and checker kernel blob `83d14ba37acaf921920c8f33429ff42b8d03fb62`.

If the v2.10.1 controls correction can be completed without modifying executable kernel bytes, these exact kernel blobs are the predeclared expected values for the replacement implementation.

If either kernel blob must change in order to implement F1-F4 correctly, implementation MUST STOP before such a change is committed. The need, exact reason, affected functions, and intended byte-level scope must first be declared in chat and adjudicated. A kernel change may not be silently absorbed under the label "controls fix."
## 7. Ancestry and replacement-commit rule

The rejected candidate `1daa406d50177dc894efbfc59cf164c5e03721af` is not part of the canonical ancestry. Because it was never pushed, it may be discarded locally.
The canonical line remains based on `944f1d886c47ee6d9ddcde8d88646dafd1a8ed60`.

This §7 explicitly supersedes only the v2.10 requirement that the bundled implementation commit have `944f1d886c47ee6d9ddcde8d88646dafd1a8ed60` as its immediate parent. All other frozen v2.10 requirements remain in force.

The v2.10.1 predeclare commit MUST be document-only. It may add only this amendment document and MUST NOT modify any executable file.
Any v2.10.1 clarification commit, if required before implementation, MUST also be document-only and may add or modify only the amendment / clarification documentation needed to resolve the declared wording issue.

Across every v2.10.1 predeclare or clarification commit, these four executable files MUST remain bit-identical to their blobs at `944f1d886c47ee6d9ddcde8d88646dafd1a8ed60`:

- `producer/global_axial_c1b_kernel.py`
- `checker/global_axial_c1b_kernel.py`
- `producer/global_axial_c1b_gating.py`
- `checker/global_axial_c1b_gating.py`

At freeze time these four paths MUST be confirmed to exist under exactly these repository paths, and their blobs MUST be declared from `git ls-tree`.
Acceptance MUST verify this document-only constraint by `git ls-tree` blob comparison before the replacement implementation is accepted.

Required sequence:

    frozen v2.10 commit 944f1d886c47ee6d9ddcde8d88646dafd1a8ed60
      -> frozen v2.10.1 controls-fix predeclare commit
      -> one clean replacement bundled implementation commit

The replacement implementation commit MUST have the frozen v2.10.1 predeclare commit as its immediate parent. If a clarification is required, the final clarification commit becomes the required immediate parent. No commit derived from `1daa406d...` may be pushed as canonical implementation. No history rewrite of already-pushed canonical commits is authorized.
## 8. Acceptance audit for the replacement implementation

The replacement implementation is not accepted merely by local tests. It must be delivered to chat using the same archive-transfer procedure that produced VERIFIED_DELIVERY for the rejected candidate.

The frozen v2.10.1 amendment document itself is also a pinned audit object. At freeze time, the following metadata MUST be declared for the exact frozen document bytes:

- path;
- commit SHA;
- parent commit SHA;
- Git blob SHA-1;
- byte count;
- line count;
- SHA-256.

That SHA-256 is the canonical document-byte pin for v2.10.1. If a clarification document is introduced, it MUST receive the same metadata and byte-level pinning before implementation authorization.

The delivery package must contain at minimum every changed current file in full and the canonical full-index parent-to-replacement-implementation diff.

### V2101-A1 — byte and diff closure

Independently recompute SHA-256, bytes, lines, and Git blob SHA-1 for each current executable file, plus canonical diff SHA-256.
Also recompute the frozen v2.10.1 amendment document Git blob SHA-1 and SHA-256 against its declared freeze-time byte pin; if present, do the same for the final clarification document.
The canonical diff must apply from the declared parent chain and close exactly onto the delivered current bytes.

### V2101-A2 — delta against rejected candidate

Compare the new canonical implementation diff against rejected-candidate diff SHA-256 `af31d132ed0b70f3e0628333e31a0d3c8d79adf6fc4ac7d81345af12f62622af`.
The semantic difference must be confined to F1-F4 control corrections and explicitly permitted control serialization/test plumbing. The already-audited v2.9/v2.10 implementation body need not undergo a full B-E audit again if this delta confinement is established. Any unrelated numerical or runtime change fails acceptance.
### V2101-A3 — kernel expectation

If §6's kernel-unchanged expectation remains applicable, verify exact equality with producer kernel blob `284d591b9f47d360c78de2ef52e08112a329c037` and checker kernel blob `83d14ba37acaf921920c8f33429ff42b8d03fb62`.
A mismatch without prior chat adjudication is acceptance FAIL.

## 9. Required controls before push authorization

Before implementation acceptance can lead to push authorization, corrected controls must establish at least:

- F1 three-function restoration on both lineages;
- V29-C3 end-to-end propagation to `GT_DIVISION_GUARD_UNRESOLVED`;
- V210-C5 end-to-end propagation to final `TUBE`;
- direct nonactivation for `T2 AND t_hi != T_HI`;
- T0 nonactivation;
- T1 nonactivation;
- passing endpoint-T2 nonactivation;
- nonfinite endpoint-T2 nonactivation;
- previously frozen v2.9 and v2.10 positive controls;
- no unauthorized root/MV numerical change.

The corrected control suite is still preflight machinery, not certification evidence by itself. Official machine preflight remains separately gated.

## 10. Push, pin, preflight, and rerun order

After chat-side implementation acceptance, the next sequence remains:

1. explicit push approval;
2. before or with push adjudication, close the parent-tree check at `944f1d886c47ee6d9ddcde8d88646dafd1a8ed60`, including the four relevant executable parent blobs; verify by `git ls-tree` that every v2.10.1 predeclare / clarification commit is document-only and those blobs remain bit-identical; verify the frozen v2.10.1 document blob and SHA-256, and if present the final clarification document, against their freeze-time pins;
3. push only the accepted canonical ancestry;
4. verify remote tree;
5. recompute the canonical diff SHA-256 from the pushed remote tree and confirm equality with the accepted diff; reverify the pushed v2.10.1 document blob / SHA-256 byte pin from the remote tree; if present, reverify the final clarification document identically from the remote tree;
6. refresh pins and manifest;
7. run official machine preflight including all carried-forward controls and corrected v2.10.1 controls;
8. only if official preflight passes, create a new Phase-1 RUN_DIR;
9. never resume a failed historical Phase-1 run;
10. Phase 2 remains separately gated and requires explicit authorization.

## 11. Binding Phase-1 prediction remains unchanged

This controls amendment does not alter the previously frozen falsifiable prediction:

All 35 coarse cells in the prior contiguous TUBE fault band, coarse 105 through 139 inclusive, will close under the canonical bundled implementation at T2 endpoint refinement depth no greater than 4, with TUBE skip count equal to zero for those 35 cells.

If even one of those cells remains a TUBE skip, or requires depth greater than 4, the prediction is FAIL.

No controls fix in v2.10.1 may weaken, rename, reinterpret, or replace that prediction.

END OF v2.10.1 PREDECLARE