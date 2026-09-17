# C1b Pre-Run Amendment v2.8.2 — Derived-q Reconstruction and Zero-Cross Implementation Control

Status: PREDECLARED_CLARIFICATION / IMPLEMENTATION_ALREADY_COMMITTED_LOCALLY / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent implementation: a3b6f6bc5cb20cf3f6189838a2ff459fe965ae65.
This clarification records two implementation details that were mathematically required by v2.8/v2.8.1 but were not stated with sufficient implementation-level uniqueness before the local implementation commit. It does not authorize any new source change to that implementation commit.

## 1. Local reconstruction of q-dependent derived quantities

Within each C1b `_glam_density`, the certified positive q enclosure is the unique q enclosure for the v2.8 positive-structure path. Because the shared geometry return values `sq`, `gamma`, and `u` were computed from the pre-v2.8 generic q enclosure, they must not be reused in this path.

After obtaining the certified positive q enclosure, the C1b kernel locally reconstructs

    sq = sqrt(q_positive),
    gamma = lambda*A/(w*sq),
    h = mu + lambda^2*d,
    u = unit_nonnegative(e*h^2/(w2*q_positive)).

Producer and checker use their independent lineage notation for the same formulas. This reconstruction is explicitly authorized only inside `_glam_density`. It is not a change to the mathematical definitions of q, gamma, h, or u; it changes only the interval-enclosure path so that every q-dependent quantity used by the v2.8 Gl evaluation is derived from the same certified positive q enclosure.

The shared C0/C0a geometry functions remain byte-untouched. No authorization is given to change `_g_density_stable`, `g_box`, `gt_box`, monotone evaluators, C1a, C1c, BOB, gating, persistence, driver, comparison, or any other density. The intentional g-path separation fixed by v2.7.1/v2.8.1 remains binding.

The already-committed local implementation at `a3b6f6bc...` is the implementation being clarified. v2.8.2 does not permit a follow-up source edit merely because this documentation commit is later in Git ancestry. Any source change after this clarification requires a new predeclaration and audit.

## 2. Strengthened zero-cross implementation control

V28-C3 remains governed by the exact q-box-minimum theorem of v2.8 §1. The theorem, not sampling, proves the lower bound. This clarification strengthens only the implementation control that prevents a future endpoint-square shortcut from replacing that theorem-based construction.

The control must include a box for which `d=t-mu` crosses zero. On that box it must:

1. compute the exact theorem-based `q_box_min` using the same clamp branches specified by v2.8;
2. evaluate the actual lineage implementation (`_positive_q_box` in producer, `_certified_positive_q` in checker) on the corresponding interval box;
3. require the implementation lower endpoint to be outward-safe with respect to the exact theorem-based minimum and strictly positive when that exact minimum is positive;
4. separately compute the invalid endpoint-square shortcut candidate obtained by taking `min(d_lo^2,d_hi^2)` despite `0 in d`;
5. demonstrate that this shortcut assigns a positive lower bound to `d^2` although the true squared lower bound is zero, and reject any implementation result whose construction depends on that shortcut.

A source/control inspection must also establish that the actual positive-q helper computes q from the mu endpoints with `t_star=clamp(mu,t_lo,t_hi)` and does not construct its lower bound from an interval or endpoint lower bound for `d^2`.

The existing exact-rational child-box monotonicity and sampled interior-point inequalities remain required. Those sampled checks are soundness controls only and do not replace the theorem.

## 3. Additional preflight controls

V282-C1 — derived-q reconstruction. Source/control inspection must establish, independently in producer and checker, that `_glam_density` discards the shared geometry q-dependent `gamma/u/sqrt(q)` values for the v2.8 path and reconstructs `sqrt(q_positive)`, gamma, h, and u locally from the certified positive q enclosure. The unique `inv_wq32` path and `L = lambda*inv_wq32` requirement of v2.8.1 remain unchanged.

V282-C2 — zero-cross implementation binding. Execute the strengthened control of §2 in both lineages. Record the exact theorem-based q minimum, the implementation positive-q lower endpoint, the d interval crossing zero, the true d-squared lower bound zero, and the invalid endpoint-square candidate. Any nonpositive certified q lower endpoint when the exact minimum is positive, any inward lower bound, or any endpoint-square-based construction is FAIL.

These controls are added to, not substituted for, V28-C1..C7 and V281-C1..C3.

## 4. Implementation boundary, work accounting, and supersession

The four-source-file boundary remains exact: producer/checker C1b kernels and producer/checker C1b endpoint-R modules only. v2.8.2 itself changes documentation only. The local implementation commit `a3b6f6bc...` is not amended or replaced.

Logical work accounting remains the frozen panel/cell charging metric of v2.8.1. Reconstructing q-dependent `sq`, gamma, h, and u, and executing positive-q endpoint operations, adds no logical work unit and changes no ceiling.

v2.8 and v2.8.1 remain binding except that v2.8.2 makes the local reconstruction of q-dependent derived quantities explicitly authorized and strengthens the V28-C3 zero-cross control from a mathematical negative example to a direct implementation-binding control. No other v2.7.1/v2.8/v2.8.1 obligation is superseded.

## 5. Byte-chain recovery and required sequence

Chat-side byte-level verification is unavailable beyond v2.5.1 at the time of this clarification. The v2.6 implementation layer itself did not complete chat-side byte audit because its split raw transfer was interrupted before closure; the current v2.8 implementation is layered on top of that previously unaudited byte layer.

Before push or machine preflight, the current four source files at implementation commit `a3b6f6bc...` must therefore be transmitted in full and audited. Each file is split independently. Each chunk is cut directly from the file by complete lines, includes the terminating newline of its final line, and is hashed before transmission as that exact raw byte slice. Concatenating the raw chunks in order must reproduce the complete file byte-for-byte.

For each file, chat audit must reconstruct total line count, byte count, SHA-256, and Git blob SHA-1. Only after all four current source blobs match may the current byte chain be recorded as restored at `a3b6f6bc...`. Historical v2.6 remains historically unaudited at the time it was introduced, but the executable current bytes will then have been audited by full-file reconstruction.

Required order:

    v2.8.2 clarification commit
      -> chat raw/content audit PASS
      -> full current four-file byte-chain recovery at a3b6f6bc...
      -> four current Git blobs reconstructed and matched
      -> chat-side byte chain RESTORED at a3b6f6bc...
      -> explicit push approval and push
      -> manifest refresh
      -> preflight including v2.7.1 carry-forward, V28-C1..C7, V281-C1..C3, V282-C1..C2
      -> only if preflight PASS: NEW third Phase-1 RUN_DIR
      -> Phase 2 checker -> comparison -> chat adjudication -> receipt.

Until byte-chain recovery, explicit push approval, manifest refresh, and machine preflight complete, the implementation remains LOCAL / NOT_MACHINE_CERTIFIED / NOT_EVIDENCE.
