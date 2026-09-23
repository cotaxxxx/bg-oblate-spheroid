# Jev triage policy

Status: `ADVISORY_ONLY / NON_BINDING`

## Purpose

Jev is used only as a cheap semantic triage layer over already-produced audit material.
It may flag a receipt as apparently consistent or requiring human/LLM review.

Jev is not a proof engine, interval checker, judge, or certification authority.
Its output must never create, upgrade, or replace `PASS`, `JUDGE_PASS`, or `CERTIFIED`.

## Allowed output states

- `JEV_TRIAGE_OK`: Jev answered yes and met the configured probability threshold.
- `JEV_TRIAGE_REVIEW`: Jev did not meet the threshold or answered no.
- `JEV_TRIAGE_ERROR`: the Jev invocation or response failed.

All three states are non-binding.

## Default threshold

The repository wrapper uses `0.90` by default.
A threshold change is a triage-policy change, not a mathematical change.

## Required provenance

Each wrapper record includes the input SHA-256, question, threshold,
provider, returned model identifier, answer, probability, and token usage.

API keys are never read, printed, copied, or stored by the wrapper.
Authentication remains exclusively in the Jev CLI configuration.

## Research workflow position

```text
producer/checker numerical evidence
        -> exact receipt / pinned provenance
        -> Jev semantic triage (optional, non-binding)
        -> ChatGPT / Claude / local-LLM review
        -> Judge decision
```

A Jev result can request more review; it cannot waive any review or gate.

## Lineage isolation (adopted)

1. **Advisory provenance only.** Jev is advisory tooling originating from a separate ChatGPT workstream; its judgments are not part of either numerical lineage.
2. **Pinned-runtime separation.** Any Jev-side Python cache/runtime artifact outside the pinned Python 3.11.16 lineage (including observed Python 3.14 `__pycache__` artifacts) is excluded from evidence and commits. Repository ignore rules must exclude `__pycache__/`.
3. **No evidence-path execution.** `tools/jev_triage.py` must not be imported by producer or checker and must not execute inside an identity-gate `RUN_DIR`.
4. **Separate outputs.** Jev triage logs stay outside producer/checker evidence artifacts and must not be cited by the machine receipt or Judge request.

These restrictions are governance gates. A violation is a workflow error and cannot be repaired by a favorable Jev result.
