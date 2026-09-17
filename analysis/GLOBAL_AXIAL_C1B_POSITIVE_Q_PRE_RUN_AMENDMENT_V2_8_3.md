# C1b Pre-Run Amendment v2.8.3 — Control-Only Follow-up and Audit-Status Clarification

Status: PREDECLARED_CONTROL_FOLLOWUP / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent clarification: v2.8.2 at commit 0519b6332bd17b626f8c95a3ddf06c9c59bbdf86.
This clarification resolves the sequencing conflict between the documentation-only v2.8.2 commit and the fact that V282-C1/V282-C2 must exist as executable preflight controls inside the C1b kernels before byte-chain recovery and machine preflight.

## 1. Audit-status distinction

The v2.8.2 §1 description of the already-committed `a3b6f6bc...` evaluation path is retroactive documentation, not a predeclaration of that already-existing source behavior. The reconstructed `sq`, gamma, h, and u formulas were already present in `a3b6f6bc...` before v2.8.2 was committed.

By contrast, the V282-C1/V282-C2 control additions specified by v2.8.2 §3 are predeclared controls. They have not yet been added to source at the time of this v2.8.3 commit. The historical distinction must be preserved in later receipt language: evaluation-path documentation is retroactive; the control-only follow-up is predeclared-before-implementation.

## 2. Authorized control-only follow-up

A single follow-up implementation commit is authorized after this clarification and before byte-chain recovery. It may modify only:

1. `producer/global_axial_c1b_kernel.py`
2. `checker/global_axial_c1b_kernel.py`

The follow-up may add only the executable V282-C1 and V282-C2 controls and the minimal invocation needed to run them from preflight. No mathematical evaluation path may change. In particular, `_glam_density`, `_positive_q_box` / `_certified_positive_q`, `_positive_inv_wq32` / `_positive_reciprocal_wq32`, `g_box`, `gt_box`, `glam_box`, root localization, tube/exterior logic, work accounting, schemas, reason serialization, and every ceiling are byte-preserved relative to `a3b6f6bc...` except for source/control inspection references that live only inside the new control code.

The endpoint-R modules are not changed by this follow-up. No fifth source path is authorized.

## 3. V282-C1 executable control

V282-C1 must inspect the actual lineage `_glam_density` source and require all of the following:

- the shared geometry q-dependent return values for gamma/u/sqrt(q) are not used as the v2.8 Gl path values;
- the function constructs the certified positive q enclosure first;
- `sqrt(q_positive)` is reconstructed locally;
- gamma is reconstructed from that positive square root;
- h is reconstructed as `mu + lambda^2*d` in lineage notation;
- u is reconstructed from `e*h^2/(w2*q_positive)` and passed through the existing unit-nonnegative guard;
- the existing v2.8.1 unique reciprocal-path conditions remain true.

Any failure is V282-C1 FAIL. This control is structural and does not authorize an alternate evaluation formula.

## 4. V282-C2 executable zero-cross binding

V282-C2 must exercise an exact-rational control box in which `d=t-mu` crosses zero and the theorem-based `q_box_min` is strictly positive. For that same box it must:

1. compute the exact theorem-based q minimum with `_q_box_min_fraction` or its independent checker transcription;
2. construct the actual Arb mu/t/lambda/q inputs and call the lineage positive-q implementation helper;
3. record the exact theorem q minimum and the implementation positive-q lower endpoint;
4. require the implementation lower endpoint to be outward-safe, i.e. not greater than the exact theorem minimum, while remaining strictly positive;
5. compute exact `d_lo` and `d_hi` with `d_lo < 0 < d_hi`;
6. record the true lower bound of d-squared as exactly zero;
7. compute the invalid shortcut candidate `min(d_lo^2,d_hi^2)` and require that candidate to be strictly positive;
8. inspect the positive-q helper source and require the clamp-at-mu-endpoints construction while rejecting a lower-bound construction based on endpoint or interval `d^2`.

The purpose is to bind the actual implementation to the theorem-based clamp construction, not merely to show abstractly that the endpoint-square shortcut is unsound.

## 5. Byte-chain recovery target

Byte-chain recovery must target the source bytes after the authorized control-only follow-up commit, not `a3b6f6bc...`. The two endpoint-R files remain the same blobs as at `a3b6f6bc...`; the two kernel blobs will change only because V282-C1/V282-C2 controls and their preflight invocation are added.

The full-file transmission format remains that of v2.8.2 §5: each file independently split on complete lines, every chunk includes its final terminating newline, and every chunk SHA-256 is computed from the exact raw byte slice before transmission. Concatenation must reproduce each final file byte-for-byte.

## 6. Required sequence

    v2.8.3 clarification commit
      -> chat raw/content audit PASS
      -> control-only follow-up implementation commit adding V282-C1/V282-C2
      -> local static/control check; no push
      -> full current four-file byte-chain recovery at that follow-up commit
      -> four current Git blobs reconstructed and matched
      -> chat-side byte chain RESTORED at the follow-up commit
      -> explicit push approval and push
      -> manifest refresh
      -> machine preflight including v2.7.1 carry-forward, V28-C1..C7, V281-C1..C3, V282-C1..C2
      -> only if preflight PASS: NEW third Phase-1 RUN_DIR
      -> Phase 2 checker -> comparison -> chat adjudication -> receipt.

Until this sequence completes, no push, manifest refresh, machine preflight, or third Phase-1 run is authorized.
