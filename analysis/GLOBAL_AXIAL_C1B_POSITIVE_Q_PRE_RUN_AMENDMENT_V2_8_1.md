# C1b Pre-Run Amendment v2.8.1 — Unique Positive-Reciprocal Path and Work Accounting Clarification

Status: PREDECLARED_CLARIFICATION / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent amendment: v2.8 at commit cd1f06ad7b270bd11ddecb7f95deed27bb50f97e.
This clarification resolves three remaining implementation ambiguities before any combined v2.7/v2.8 source change begins.

## 1. Unique use of inv_wq32 inside _glam_density

Within each C1b `_glam_density`, `inv_wq32` is the sole authorized enclosure of the mathematical
factor `1/(w*q*sqrt(q))`. No second evaluation path for that factor may remain inside `_glam_density`.
In particular, after constructing the certified positive q enclosure and `inv_wq32`, define

    L = lam * inv_wq32

in producer notation, with the checker using its transcribed symbol names. The legacy form

    L = lam / (w*q*sq)

is not authorized inside `_glam_density` after v2.8 implementation.

The existing algebra that depends on L remains structurally unchanged:

    gt = L*N
    L_lam = L * (1/lam - wl_over_w - 3*lam*d2/q)
    gt_lam = L_lam*N + L*N_lam

subject only to using the v2.8 certified positive q enclosure wherever q appears in the authorized
C1b-local v2.8 evaluation. The regrouped term must use the same `inv_wq32` object:

    regular_rg_term = -(gamma*R - 1) * gamma*e*k * inv_wq32

Thus `gt`, `gt_lam`, and `regular_rg_term` cannot disagree because one uses a positive reciprocal
path while another reconstructs a zero-crossing generic denominator. No occurrence of
`1/(w*q*sqrt(q))` or `lam/(w*q*sqrt(q))` may be independently reconstructed inside `_glam_density`.

This clarification is limited to `_glam_density`. It does not authorize changes to shared C0/C0a
geometry, `gt_box`, monotone evaluators, or any other density.

## 2. Positive q upper endpoint

Let `q_min` be the outward-safe lower endpoint derived from the exact `q_box_min` theorem of v2.8.
Let `q_upper_safe` be any outward-safe upper bound obtained from the existing q enclosure or an equal
or tighter certified construction. The C1b-local positive q enclosure used by v2.8 must satisfy

    q_lo > 0,
    q_hi >= q_lo,
    q_hi >= q_upper_safe,

with the implementation-equivalent construction

    q_hi = max(q_lo, q_upper_safe)

permitted and preferred when using scalar endpoints. This clause prevents an inconsistent enclosure
whose lower endpoint is certified positive while its selected upper endpoint is accidentally below
that lower endpoint. If a finite safe upper endpoint cannot be constructed, evaluation fails closed.
No arbitrary positive epsilon or inward rounding is permitted.

The fact that a loose q upper endpoint only weakens the lower endpoint of `inv_wq32` is accepted; it
is a tightness issue, not a soundness failure, provided the enclosure conditions above hold.

## 3. Logical work accounting remains unchanged

C1b work accounting is a logical panel/cell charging metric, not a count of internal Arb arithmetic
operations. Existing `g_box`, `gt_box`, and `glam_box` calls charge by their declared/logical panel
counts, and the surrounding root/tube/exterior accounting adds returned panel work or the already
frozen declared constants.

Therefore the internal replacement of algebra and interval-enclosure method inside `_glam_density`
— including `q_box_min`, positive q construction, `inv_wq32`, and `L = lam*inv_wq32` — must not alter
logical work charged for a panel or cell. No new work unit is introduced for endpoint evaluations,
exact-rational q-min calculations, square roots, reciprocal endpoints, or additional Arb operations.
All existing per-attempt, cumulative, accepted-work, monotone-work, and global ceilings remain
numerically unchanged.

Preflight must verify that for an identical logical call pattern and panel schedule, work totals are
unchanged from the pre-v2.8 accounting contract. This is a bookkeeping identity control, independent
of wall-clock runtime or the number of primitive Arb operations.

## 4. Implementation boundary and supersession

The four-file boundary from v2.7.1/v2.8 remains exact:

1. `producer/global_axial_c1b_kernel.py`
2. `checker/global_axial_c1b_kernel.py`
3. `producer/global_axial_c1b_endpoint_r.py`
4. `checker/global_axial_c1b_endpoint_r.py`

No fifth source path is authorized. The endpoint files receive only the already-authorized deletion
of `_R_Rg_endpoint_safe` and optional obsolete-Rg docstring cleanup. All q/inv_wq32 logic resides in
the two C1b kernel files. All previously frozen byte-preservation requirements for shared C0/C0a,
gating, persistence, driver, comparison, monotone, C1a, C1c, BOB, and `exterior_cover` remain in
force.

v2.8 remains binding except where this clarification narrows implementation choice. v2.8.1 does not
replace the q-box theorem, the two-stage positive-structure requirement, V28-C1..C7, or the v2.7.1
carry-forward controls. It only makes the reciprocal use unique, makes positive q upper-endpoint
consistency explicit, and makes logical work accounting explicit.

## 5. Additional preflight controls

V281-C1 — unique reciprocal path. Source/control inspection must establish that `_glam_density`
contains a single constructed `inv_wq32`; `L` is formed as `lam*inv_wq32` (checker transcription
analogous); and `regular_rg_term` uses that same reciprocal enclosure. Any surviving generic
`lam/(w*q*sqrt(q))` or independently reconstructed `1/(w*q*sqrt(q))` path inside `_glam_density` is
FAIL.

V281-C2 — positive q endpoint consistency. Exercise cases where the naive q upper bound is much
larger than q_box_min and require `q_hi >= q_lo > 0`; verify exact/high-precision point q values remain
inside the constructed q enclosure. Exercise a synthetic invalid/nonfinite upper-bound case and
require fail-closed behavior rather than epsilon repair.

V281-C3 — work identity. Run paired logical evaluations with identical panel/cell schedules before
and after the v2.8 algebraic path in the control harness and require identical charged work totals.
The control compares logical accounting only; wall-clock timing and primitive-operation counts are
not pass criteria.

## 6. Required sequence

The required sequence becomes:

    v2.8 predeclare cd1f06ad...
      -> v2.8.1 clarification commit
      -> chat verbatim/raw audit PASS
      -> combined v2.7/v2.8 implementation commit
      -> chat raw implementation audit
      -> explicit push approval and push
      -> manifest refresh
      -> preflight including v2.7.1 carry-forward, V28-C1..C7, V281-C1..C3
      -> only if preflight PASS: NEW third Phase-1 RUN_DIR
      -> Phase 2 checker -> comparison -> chat adjudication -> receipt.

Until that later sequence completes, this clarification is PREDECLARED / MACHINE_NOT_RUN /
NOT_EVIDENCE.
