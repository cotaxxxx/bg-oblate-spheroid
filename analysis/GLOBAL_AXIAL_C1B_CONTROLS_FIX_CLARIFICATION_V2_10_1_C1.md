# GLOBAL AXIAL C1B — CONTROLS-FIX CLARIFICATION v2.10.1-C1

Status: PREDECLARED CLARIFICATION / DOCUMENT-ONLY / MACHINE_NOT_RUN / NOT_EVIDENCE

**Naming note.** The suffix `C1` in `v2.10.1-C1` is a clarification sequence number only. It is unrelated to the project contract labels C1a / C1b / C1c and does not rename, amend, or redefine those contracts.

This clarification is subordinate to and read together with the frozen controls-fix pre-run amendment:
`analysis/GLOBAL_AXIAL_C1B_CONTROLS_FIX_PRE_RUN_AMENDMENT_V2_10_1.md`.

It resolves one implementation-location discovery made after the v2.10.1 freeze and before replacement implementation. Except where explicitly replaced below, every frozen v2.10 and v2.10.1 requirement remains in force.

## 1. Reason for clarification and authorized kernel scope

Post-freeze inspection established that the F1-F4 preflight controls are implemented inside the two kernel files rather than wholly in gating code:

- producer `v29_preflight_controls()`;
- producer `v210_preflight_controls()`;
- checker `v29_preflight_controls()`;
- checker `v210_preflight_controls()`.

Therefore a correct F1-F4 replacement necessarily changes executable kernel bytes. The prior v2.10.1 expectation that replacement producer/checker kernel blobs remain equal to the rejected candidate kernel blobs is withdrawn only to this extent.

Kernel changes are authorized only inside those four control functions and strictly necessary control-only plumbing serving F1-F4.

The following remain non-authorized and frozen:

- numerical production body;
- root/MV formulas;
- v2.9 root-Gt refinement numerical body;
- v2.10 T2 endpoint-refinement numerical body;
- grids and panels;
- refinement depths;
- guards and their production semantics;
- work charging;
- production ledger semantics;
- decision vocabulary;
- nonfinite semantics.

## 2. Fail-closed hunk enumeration rule

After replacement implementation and before acceptance, every changed kernel hunk outside the four named control-function bodies MUST be enumerated individually with:

- file;
- function / exact region;
- reason for the change;
- why the change is control-only plumbing;
- why numerical production behavior is unchanged.

Any outside-function hunk not present in that enumeration is immediate acceptance FAIL.

If such outside-function hunks exist, the enumeration report becomes an additional conditional delivery object and MUST be included inside the §9 acceptance archive. In that case the archive contains eight objects rather than seven. If no such hunk exists, no eighth object is required.

## 3. Frozen semantics retained

This clarification does not alter F1-F4, the v2.10.1 fail-kind-to-ledger-reason mapping, or any production decision rule.

In particular:

- finite depth-4 T2 sign failure remains final reason `TUBE`;
- finite sibling sign failure remains `TUBE`;
- existing Arb/nonfinite records remain on the existing `TUBE_NONFINITE` path;
- endpoint-domain nonfinite records remain on the existing `TUBE_NONFINITE` path;
- handled `ValueError` / `ZeroDivisionError` without a nonfinite record remains `TUBE`;
- V29-C3 must propagate end-to-end to exact `GT_DIVISION_GUARD_UNRESOLVED`;
- V210-C5 must propagate end-to-end to final exact `TUBE`;
- endpoint and non-endpoint activation exclusions required by v2.10.1 remain binding.

The previously frozen Phase-1 prediction is unchanged: all prior TUBE-fault coarse cells 105 through 139 inclusive must close with T2 endpoint refinement depth no greater than 4 and TUBE skip count zero for those 35 cells. Any surviving TUBE skip or required depth greater than 4 is prediction FAIL.

## 4. Replacement for V2101-A3 only

This section replaces only v2.10.1 §8 `V2101-A3 — kernel expectation` and the related conditional kernel-blob equality language in v2.10.1 §6.

The rejected implementation candidate remains audit provenance only:

- rejected producer kernel blob: `284d591b9f47d360c78de2ef52e08112a329c037`;
- rejected checker kernel blob: `83d14ba37acaf921920c8f33429ff42b8d03fb62`.

These blobs are the byte baselines for confinement, not required equality targets for the corrected replacement.

Replacement acceptance MUST directly compare the delivered replacement producer kernel bytes against the rejected producer kernel bytes and the delivered replacement checker kernel bytes against the rejected checker kernel bytes.

The resulting deltas must be confined to:

1. the four authorized control functions listed in §1; and
2. any individually declared and accepted control-only plumbing under §2.

If confinement is established, the already completed rejected-candidate audits of v2.10 numerical implementation sections B-E need not be rerun solely because kernel blob IDs changed. Any delta touching the frozen numerical production body or any undeclared region is acceptance FAIL.

## 5. Gating comparison remains required

The v2.10.1 `V2101-A2` delta-confinement requirement for gating files remains in force.

Replacement producer/checker gating bytes MUST be compared against the rejected candidate gating baselines, and any delta must be confined to F1-F4 control serialization / test plumbing already authorized by v2.10.1.

This clarification does not weaken exact producer/checker lineage comparison requirements and does not convert guard-truth or decision mismatches into tolerances.

## 6. Dual comparison required at acceptance

Acceptance requires both independent comparisons:

1. canonical full-index diff from the final clarification parent to the replacement implementation, closing exactly onto the delivered replacement bytes; and
2. direct executable-byte comparison from rejected-candidate executables to replacement executables, used to establish F1-F4 delta confinement.

The canonical ancestry diff and the rejected-to-replacement confinement diff serve different purposes and neither substitutes for the other.

The rejected candidate `1daa406d50177dc894efbfc59cf164c5e03721af` remains noncanonical and MUST NOT be rebased, amended, or pushed into canonical ancestry.

## 7. Clarification freeze pin and ancestry rule

This clarification commit MUST be document-only and MUST have immediate parent:
`c07187354281486a466c00c95fc060eeb64c2fb6`.

At freeze time this exact clarification document MUST receive the seven audit pins:

- path;
- commit SHA;
- parent commit SHA;
- Git blob SHA-1;
- byte count;
- line count;
- SHA-256.

The four executable paths MUST remain bit-identical between parent `c07187354281486a466c00c95fc060eeb64c2fb6` and this clarification commit.

After this clarification is frozen, the one clean replacement implementation commit MUST have the clarification commit as its immediate parent.

## 8. Replacement implementation ancestry and single-commit rule

The required canonical sequence is:

    944f1d886c47ee6d9ddcde8d88646dafd1a8ed60
      -> c07187354281486a466c00c95fc060eeb64c2fb6
      -> frozen v2.10.1-C1 clarification commit
      -> one clean replacement implementation commit

No executable change is permitted in either document-only commit. No implementation work is authorized before this clarification is frozen.

The replacement implementation must be a single clean commit. The rejected candidate is comparison provenance only and is not an ancestry parent.

## 9. Acceptance delivery archive

The replacement acceptance archive MUST contain these seven unconditional objects in full:

1. producer kernel;
2. checker kernel;
3. producer gating;
4. checker gating;
5. canonical full-index clarification-parent-to-replacement diff;
6. frozen v2.10.1 amendment document;
7. frozen v2.10.1-C1 clarification document.

If §2 identifies any changed kernel hunk outside the four named control-function bodies, the archive MUST additionally contain:

8. the complete outside-function hunk enumeration report.

Thus the normal package is seven objects; it is eight objects exactly when the conditional enumeration report is required.

Chat-side acceptance must independently recompute relevant SHA-256, bytes, lines, Git blobs, ancestry, document pins, canonical diff closure, kernel confinement, gating confinement, and required F1-F4 controls from the delivered bytes.

## 10. Required controls remain binding

Before implementation acceptance can lead to push authorization, both lineages must establish at least:

- F1 three-function restoration;
- V29-C3 end-to-end exact `GT_DIVISION_GUARD_UNRESOLVED`;
- V210-C5 end-to-end final exact `TUBE`;
- endpoint T2 activation on eligible finite sign failure;
- passing endpoint T2 nonactivation;
- non-endpoint T2 nonactivation;
- T0 nonactivation;
- T1 nonactivation;
- nonfinite endpoint T2 nonactivation;
- all carried-forward positive controls.

These are preflight controls, not certification evidence by themselves.

## 11. Push and remote re-verification order

Acceptance before push remains mandatory.

After chat-side replacement acceptance and only after explicit push approval:

1. formally verify clarification parent and both frozen document pins;
2. verify both document-only commits left all four executable blobs unchanged from their respective parents;
3. push only accepted canonical ancestry;
4. verify the remote tree;
5. recompute canonical diff SHA-256 from the pushed remote tree and match the accepted value;
6. reverify the pushed v2.10.1 amendment document blob and SHA-256;
7. reverify the pushed v2.10.1-C1 clarification document blob and SHA-256;
8. refresh pins / manifest;
9. run official machine preflight;
10. only after preflight PASS create a new Phase-1 RUN_DIR;
11. do not resume a failed historical Phase-1 run;
12. Phase 2 remains separately gated and requires explicit authorization.

## 12. No other amendment

Except for the explicit replacement of the kernel-equality expectation in §4 and the archive-closure / naming clarifications above, v2.10 and v2.10.1 remain unchanged and fully binding.

END OF v2.10.1-C1 CLARIFICATION
