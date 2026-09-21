# C1d AXIAL UPPER EXCLUSION — ANALYTIC ASSEMBLY

**Status**: `ANALYTIC_ASSEMBLY / DEPENDS_ON_NOT_BINDING_LEMMA / EXTERNAL_AUDIT_PENDING`

This document combines the C1d machine gate, the lower-edge anchor at t = 31/32, and the pinned C1d analytic lemma, to conclude the absence of a nonzero axial root on (0, 31/32] for lambda in [5/8, 33/50]. It does not modify, reopen, or strengthen any artifact it references.

## §1 Dependencies

~~~
C1d analytic lemma (L)
  analysis/OBLATE_AXIAL_C1D_ANALYTIC_LEMMA.md
  commit  8577878d5a6d2ef12c15c3683fd049fb2d14b8ab
  blob    35656381de9f13f684fa389fcbecdf2c0901a23f
  status  CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING

C1d machine receipt
  analysis/GLOBAL_AXIAL_C1D_MACHINE_RECEIPT.md
  commit  d5953355cc19e3da0893671d7c20b1f821e82d08
  blob    4e1b014b7b05a3d3c1b5fb357f98d07d06a3efc9
  status  C1D_MACHINE_PASS / JUDGE_NOT_ISSUED / NOT_BINDING
  pre-run contract 957848e9e76725e9167c1babd0b7438f613cfa79

Lower-edge anchor
  machine receipt 3e2dfb04293d7a5c92fcd3ed164b164fe33115a6
    status MACHINE_GATING_PASS / NOT_AUDITED / NOT_BINDING
  chat raw audit record analysis/LOWER_EDGE_31_32_CHAT_RAW_AUDIT.md
    commit cca99befd90aecc3b6dec1ed37c09a01e61a7f96
    blob   c9e3ef8bec1f6249cfa8f5184b590a30a21d6568
    status CHAT_RAW_AUDIT_PASS / JUDGE_NOT_ISSUED / NOT_BINDING
~~~

## §2 Facts supplied

**(F1) Third-derivative sign (C1d machine receipt).** `partial_t^3 g_axis_ob(t,lambda) < 0` for all `(t,lambda)` in `[0,31/32] x [5/8,33/50]`. The 1,265 accepted leaves tile this box exactly; every leaf was re-evaluated independently at 192 bits and accepted. The checker import closure recorded in the receipt contains no producer module.

**(F2) Positive anchor at t = 31/32 (receipt 3e2dfb04, chat raw audited).** `g_axis_ob(31/32,lambda) > 0` for lambda in each of the eight exact boxes `[(1000+7k)/1600, (1007+7k)/1600]`, `k = 0,...,7`, hence for all lambda in `[5/8,33/50]`; the recorded weakest checker lower bound is `+0.00481...` on `[5/8,1007/1600]`. The identification of the evaluated integral with `g_axis_ob(31/32,lambda)` is Lemma 11 of (L), since `(31/32,lambda)` lies in `B'`.

**(F3) Exact lambda agreement.** The eight lambda boxes of (F2) are exactly the boxes `Lambda_k` of the C1d gate (contract verification V1), and their union is exactly `[5/8,33/50]`.

**(L) Analytic bridge.** On `B' = { |t| <= 31/32 } x [5/8,33/50]`: `g_axis_ob(·,lambda)` is `C^3` and odd in `t` (Proposition 12, Corollary 13); the reduced quotient `Phi` extends through the origin (Lemmas 14, 15); and if `partial_t^3 g_axis_ob < 0` on `[0,31/32] x [5/8,33/50]`, then `partial_tau Phi < 0` on `[0,961/1024] x [5/8,33/50]` (Corollary 18 of (L)). The underlying identity evaluates `partial_t^3 g_axis_ob` only inside that box (Lemma 17 of (L)).

## §3 Assembly

By (F1) and Corollary 18 of (L), `Phi(·,lambda)` is strictly decreasing on `[0,961/1024]` for every lambda in `[5/8,33/50]`.

By Lemmas 14 and 15 of (L) at `t = 31/32`, `Phi(961/1024,lambda) = g_axis_ob(31/32,lambda)/(31/32)`, which is positive for every lambda in `[5/8,33/50]` by (F2) and (F3). Since `Phi` is decreasing and positive at the right endpoint,

~~~
Phi(tau,lambda) >= Phi(961/1024,lambda) > 0      for all tau in [0,961/1024], lambda in [5/8,33/50].
~~~

By Lemmas 14 and 15 of (L), `g_axis_ob(t,lambda) = t Phi(t^2,lambda)` for `0 < t <= 31/32`, so

~~~
g_axis_ob(t,lambda) > 0                           for all t in (0,31/32], lambda in [5/8,33/50].
~~~

Hence there is no nonzero axial root in `(0,31/32]` for lambda in `[5/8,33/50]`. By parity (Corollary 13 of (L)), `g_axis_ob < 0` on `[-31/32,0)`, and `g_axis_ob(0,lambda) = 0` is the centre, not a nonzero root.

The C1d pre-run contract did not predeclare a logical-final judgment word. This document defines `LOGICAL_FINAL_C1D_ASSEMBLY` in the same form as the C1c assembly:

~~~
LOGICAL_FINAL_C1D_ASSEMBLY = PASS
conditional_on:
  OBLATE_AXIAL_C1D_ANALYTIC_LEMMA
  commit 8577878d5a6d2ef12c15c3683fd049fb2d14b8ab
  blob   35656381de9f13f684fa389fcbecdf2c0901a23f
  status CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING
~~~

The anchor is not listed in `conditional_on`: its audit condition under §9(1) of the C1d pre-run contract is discharged by the audit record cca99bef, matching the treatment of the C1b anchor in the C1c assembly.

`LOGICAL_FINAL_C1D_ASSEMBLY = PASS` is a conditional analytic-assembly result and does not promote the C1d analytic lemma, the C1d machine receipt, the anchor receipt, or this document to an external-Judge-certified or binding status.

## §4 Scope

This assembly does not certify the band `[31/32,1]`, the endpoint behaviour at `t = 1`, the existence or uniqueness of a nonzero axial root in `(31/32,1)`, or any off-axis statement.
