# C1c LOWER-HALF EXCLUSION — ANALYTIC ASSEMBLY

**Status**: `ANALYTIC_ASSEMBLY / DEPENDS_ON_NOT_BINDING_LEMMA / EXTERNAL_AUDIT_PENDING`

This document combines the C1c machine gate, the C1b machine anchor and exact cover, and the pinned lower-half analytic lemma, to conclude the absence of a nonzero axial root on the lower-half domain. It does not modify, reopen, or strengthen any artifact it references.

## §1 Dependencies

```
Lower-half analytic lemma
  commit  e2e12be02ad10bd29109886af96cdc679b37c7db
  path    analysis/OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA.md
  blob    6fba6e4f981d08201a779be2a435b49954c8b659
  status  CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING

C1c Judge receipt
  commit  49cdcbb6
  blob    105126b6c190951f1737e04d8a5199928abf72ad
  scope   partial_t^3 g_axis_ob < 0 on [0,1/2] x [9/20,5/8]
  status  JUDGE_FINAL_C1C_MACHINE PASS

C1b machine receipt
  added by commit 0e6040d; computational HEAD 85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b
  status  MACHINE_PASS / C1B_MACHINE_CLOSED / JUDGE_NOT_YET_ISSUED
  sealed  phase1_v212s_seal_20260918T222551Z, phase2_v212s_seal_20260920T140743Z
```

## §2 Facts supplied

**(F1) Third-derivative sign (C1c).** `partial_t^3 g_axis_ob(t,lambda) < 0` for all `(t,lambda)` in `[0,1/2] x [9/20,5/8]`. Judge-approved; this is the entire approved scope of the C1c receipt.

**(F2) Positive anchor at `t = 1/2` (C1b receipt §6).** For every accepted slab, a positive anchor `Phi(1/4,lambda) = 2 g_axis_ob(1/2,lambda) > 0` is supplied. Of the 159 accepted slabs, 0 obtain it from a left tube wall at `t_minus = 1/2` and 159 from a certified left exterior cover on `[1/2, t_minus]`; none is missing. Exterior closure stages: E0 120, E1 37, E2 2; unresolved 0.

**(F3) Exact cover (C1b).** The union of the accepted slab parameter intervals is exactly `[9/20, 5/8]`.

**(L) Analytic bridge (pinned lemma).** On `B = { |t| <= 1/2 } x [9/20,5/8]`: `g_axis_ob(·,lambda)` is `C^3` and odd in `t` with `g_axis_ob(0,lambda) = 0`; the reduced quotient `Phi` extends through the origin; and (Corollary 18 of (L)) if `partial_t^3 g_axis_ob < 0` on `[0,1/2] x [9/20,5/8]`, then `partial_tau Phi < 0` on `[0,1/4] x [9/20,5/8]`. The identity underlying this evaluates `partial_t^3 g_axis_ob` only at arguments `x t` with `x` in `[0,1]`, `t` in `[0,1/2]`, hence only inside the C1c-certified box (Lemma 17 of (L)).

## §3 Assembly

By (F1) and (L), `Phi(·,lambda)` is strictly decreasing on `[0,1/4]` for every `lambda` in `[9/20,5/8]`. By (F2), `Phi(1/4,lambda) > 0` for every such `lambda`, the range being exactly `[9/20,5/8]` by (F3). Since `Phi` is decreasing and its value at the right endpoint of `[0,1/4]` is positive,

```
Phi(tau,lambda) >= Phi(1/4,lambda) > 0        for all tau in [0,1/4], lambda in [9/20,5/8].
```

By Lemmas 14 and 15 of (L), `Phi~(t,lambda) = g_axis_ob(t,lambda)/t` for `t != 0` and `Phi(t^2,lambda) = Phi~(t,lambda)`. Therefore

```
g_axis_ob(t,lambda) = t Phi(t^2,lambda)        for 0 < t <= 1/2,
```

and since `Phi(t^2,lambda) > 0` by the preceding display,

```
g_axis_ob(t,lambda) > 0                        for all t in (0,1/2], lambda in [9/20,5/8].
```

Hence there is no nonzero axial root in the lower half of the C1c domain. By parity (L), the same holds on `[-1/2,0)` with the opposite sign, and `g_axis_ob(0,lambda) = 0` is the central point, not a nonzero root.

The C1c Judge receipt explicitly excluded this deduction from its approved scope, recording that `Phi(1/4,lambda) > 0`, the deduction `Phi > 0` on `[0,1/4]`, and nonzero-root exclusion on `(0,1/2]` remained pending a C1b anchor and exact cover. The present document supplies those inputs and the analytic bridge.

```
LOGICAL_FINAL_C1C_ASSEMBLY = PASS
conditional_on:
  OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA
  commit e2e12be02ad10bd29109886af96cdc679b37c7db
  blob   6fba6e4f981d08201a779be2a435b49954c8b659
  status CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING
```

`LOGICAL_FINAL_C1C_ASSEMBLY = PASS` is a conditional analytic-assembly result and does not promote the lower-half analytic lemma, the assembly document, or the C1b machine receipt to an external-Judge-certified or binding status.

## §4 Provenance note on the referenced lower-half lemma

The C1c pre-run amendment states that "the same lower-half lemma used by C1a" converts the C1c third-derivative gate into `partial_tau Phi < 0` on `[0,1/4]`. Two separate facts are recorded here.

First, a search of the repository conducted before drafting the pinned lemma did not locate an independent binding artifact corresponding to that reference. The C1a documents define `Phi` and `F_x = Phi(1/4,lambda) = 2 g_axis_ob(1/2,lambda)` as contract notation (C1 contract `80f2c2bd`) and record the outer factor 2 as independently audited (C1a symbolic note `684c90a3`, status `USER_SYMBOLIC_AUDIT_PASS / NOT_BINDING`), but the C1a machine gate itself does not require the `partial_t^3 g < 0 => partial_tau Phi < 0` bridge. The amendment's reference therefore appears to point to the symbolic and C0-contract material rather than to a separately certified lemma.

Second, the pinned lower-half analytic lemma supplies that bridge after the fact, in self-contained form: it derives the integral representation, the density identities, parity, `C^3` regularity, the origin extension of `Phi`, and the `partial_tau Phi` identity from the definition of `E_K(p)`, without taking any non-binding document as a premise.

These two statements are recorded separately and neither is presented as the other.
