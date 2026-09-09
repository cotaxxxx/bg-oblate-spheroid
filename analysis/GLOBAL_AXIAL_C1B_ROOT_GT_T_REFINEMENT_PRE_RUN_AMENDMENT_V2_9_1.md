# C1b Pre-Run Amendment v2.9.1 — Implementation-Parent Chain Clarification

Status: PREDECLARED_CLARIFICATION / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent predeclare: v2.9 at commit `8bbd159b35db8eb1c203301ad6291e99d10788a6`.

## 1. Binding defect corrected

This clarification corrects one binding omission in §5 of `analysis/GLOBAL_AXIAL_C1B_ROOT_GT_T_REFINEMENT_PRE_RUN_AMENDMENT_V2_9.md`: v2.9 fixed the required sequence but did not explicitly bind the ancestry and immediate parent of the later implementation commit.

No mathematical, algorithmic, control, accounting, trace-schema, failure-mode, or scope requirement of v2.9 is changed by this clarification.

## 2. Required implementation ancestry and parent

The v2.9 implementation commit must be a descendant of commit `8bbd159b35db8eb1c203301ad6291e99d10788a6`, and its parent must be the commit that introduces this v2.9.1 clarification document.

Therefore the implementation commit may not be based on a sibling commit, an alternate parent, a rebased replacement of the v2.9 predeclare, or any history that omits this clarification from its ancestry.

The exact Git hash of the v2.9.1 clarification commit is to be pinned after this document is committed and must then be used as the required immediate parent of the implementation commit.

## 3. Supersession of v2.9 §5 sequencing language

This document supplements and, only with respect to implementation-parent chain-of-custody, supersedes the sequencing language in v2.9 §5.

All other v2.9 §5 requirements remain binding, including predecessor pins, chat-side verbatim/content audit before implementation, raw byte audit after implementation, explicit approval before push, manifest refresh as required, official machine preflight, a new Phase-1 RUN_DIR only after preflight PASS, and separate Phase-2 authorization.

The binding sequence is therefore:

    v2.9 predeclare commit 8bbd159b35db8eb1c203301ad6291e99d10788a6
      -> v2.9.1 clarification commit as its child
      -> chat-side verbatim/content audit PASS for both v2.9 and v2.9.1
      -> implementation commit whose immediate parent is the v2.9.1 clarification commit
      -> local static/control checks; no machine evidence claim
      -> raw byte audit of every changed executable file against that implementation parent
      -> chat-side byte-chain verification and explicit implementation adjudication
      -> only after explicit approval: push / manifest refresh as required by changed pinned blobs
      -> official machine preflight including V29-C1..C4 and all carried-forward controls
      -> only if preflight PASS: NEW Phase-1 RUN_DIR; never resume the failed historical run
      -> Phase 2 remains separately gated and requires explicit authorization.

## 4. Audit requirement

This clarification must be included with v2.9 in the same chat-side verbatim audit package before any executable implementation begins.

The audit package must use the established pin format for each document: Path, parent commit, commit, Git blob, Bytes, Lines, SHA-256, complete raw file content, and complete parent-to-commit diff. Every pasted raw chunk must carry its exact line count and SHA-256 computed from the transmitted bytes, with final newlines preserved.

Until both v2.9 and v2.9.1 pass chat-side verbatim/content audit, v2.9 implementation, push, manifest refresh, official machine preflight, and new Phase-1 execution remain unauthorized.
