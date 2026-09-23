# D-OB P2 CONTRACT CORRECTION PREDECLARE — RESUMABLE EXECUTION

**Status**: `PREDECLARED / DOC_ONLY / NOT_IMPLEMENTED / NOT_BINDING`

**Parent gate.** This correction is authored from branch `design/d-ob-p2` at parent `c615987cfb08cbc620159f8582c286266da9fa38`. It corrects the execution design of `analysis/D_OB_P2_PRE_RUN_CONTRACT_V2.md`; it changes no mathematical claim in SPEC V2 and authorizes no certification run by itself.

**Reason for correction.** Three smoke attempts established structural incompatibility between the all-or-nothing execution design and the actual environment (daily power interruption and parallel sessions). Pinned observed burn rate: one initial box completed in CPU 4h03m; the remaining three boxes were still incomplete after more than 6h33m. This agrees with the earlier abandoned run at about 4h06m per unit. The remedy is checkpoint/resume, not another restart of the same smoke design.

## 1. Sequential append-only ledger

The producer SHALL write one record to an append-only JSONL ledger inside `RUN_DIR` whenever the decision for a dyadic node is finalized. Every record SHALL contain at least the node coordinates, decision, panel count, and elapsed time. Each record SHALL be flushed on that line before computation proceeds.

The existing terminal artifacts `certificate.jsonl.gz` and producer summary remain terminal outputs and are generated only at the end of a completed producer run. The ledger is the resumability record; it does not replace the certificate.

## 2. Resume contract

The producer SHALL accept `--resume <ledger>`. On resume it SHALL validate the ledger and skip the already-completed dyadic-node subtrees represented by valid completed records, then continue unresolved work.

**Determinism requirement.** For the same pinned inputs and implementation, a completed run obtained through any valid sequence of interruption and resume SHALL have exactly the same final leaf set as an uninterrupted completed run. Resume is an execution optimization only; it SHALL NOT alter the mathematical partition or acceptance decisions.

Malformed, inconsistent, identity-mismatched, or non-prefix-compatible resume state SHALL fail closed rather than being silently repaired or ignored.
## 3. Heartbeat

The producer SHALL emit a one-line heartbeat to stdout at a fixed documented interval while work is active. The heartbeat SHALL include the number of completed nodes. Evidence/smoke launch SHALL use unbuffered stdout so the heartbeat is externally observable during a long unit.

Heartbeat output is operational telemetry only and has no mathematical evidentiary force.

## 4. Single-writer and interruption provenance

Only one writer may operate on a computation run. While a run is active, other sessions SHALL NOT modify or operate on the corresponding repository computation process or `RUN_DIR`.

Each `RUN_DIR` SHALL contain a `LOCK` file. Startup and resume SHALL gate on that lock and fail closed on an incompatible live writer. Lock lifecycle and stale-lock handling SHALL be explicitly implemented and tested before smoke is reauthorized.

If a run is deliberately killed, the actor and time of the kill SHALL be recorded either in the append-only ledger or in a separate interruption record inside `RUN_DIR`. Silent external termination is not an accepted workflow action.

Where the checker has an equivalent long-running or resumable lineage responsibility, the same single-writer, checkpoint/resume, heartbeat, and fail-closed principles SHALL be applied symmetrically rather than weakened.

## 5. Mandatory controls before smoke reauthorization

**C-R1 — kill → resume equivalence.** Run the same controlled workload once uninterrupted and once with an intentional kill followed by resume. Require equality of the final leaf sets. A mismatch is a hard failure of resumability.

**C-R2 — ledger write-through.** Exercise every newly introduced ledger record type through the actual production path, end to end. The control SHALL include both a successful path and a fail-closed path. This is the standing “追加物通し検査” rule: no new persistent record type is accepted merely because an isolated writer/parser unit test passes.

**C-R3 — heartbeat existence.** During a controlled nontrivial run, verify that heartbeat lines are actually observable on stdout under the prescribed unbuffered launch and that completed-node counts advance.

Controls that apply to both producer and checker lineages SHALL be implemented and exercised symmetrically.

---

## Acceptance and authorization boundary

This predeclaration is documentation only. Producer/checker implementation SHALL NOT begin until this correction has passed external acceptance: codeload retrieval, parent=`c615987` verification, doc-only verification, verbatim audit of the five sections above, and freeze/implementation authorization.

Until then, D-OB P2 remains `NOT_CERTIFIED`, the all-or-nothing smoke SHALL NOT be restarted, and no output from the three lost smoke attempts is promoted to evidence.

A future accepted implementation may be published only under an authorized candidate reference in the `candidate/dob-p2-resume` family. Canonical references remain unchanged unless separately authorized.
