# GLOBAL AXIAL C0 - JUDGE RECEIPT

**Status**: `JUDGE_PASS / CONDITIONAL_ON_TWO_LEMMAS / EXTERNAL_AUDIT_PENDING`

~~~
JUDGE_DECISION = PASS
scope   = C0a and C0b of analysis/GLOBAL_AXIAL_C0_JUDGE_REQUEST.md (blob e95aafc4)
judge   = human Judge (repository owner), 2026-09-22
~~~

~~~
C0a  partial_t^3 g_axis_ob(t,lambda) < 0   on [0,1/2] x [2/5,83/200]
C0b  g_axis_ob(1/2,lambda)/(1/2) < 0       for lambda in [2/5,83/200]
~~~

~~~
conditional_on:
  OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA     blob 6fba6e4f981d08201a779be2a435b49954c8b659
  OBLATE_AXIAL_LOWER_HALF_LEMMA_C0_TRANSFER  commit 963b03be2fdeb734d3d600cc82a846e6be13a818  blob 0ab178967075459faf7bdc43dcf09e449492b130
  both EXTERNAL_AUDIT_PENDING / NOT_BINDING
~~~

Evidence relied upon: run #38 (id 33576831323, head b8a25658), all steps success;
contract 95ee0472; raw audit script 26002379; machine receipt 605c11c6;
producer cdbdf51f, c4c8d6b5, 2bb556ab; checker fbec8905, 85978625, 18e66b64;
chat raw audit analysis/GLOBAL_AXIAL_C0_V2_CHAT_RAW_AUDIT.md (commit 89e8e21d, blob 4c1bd541),
which also records the repository-side re-audit of checks 1-8 as OWNER_RE_AUDIT_PASS.

Checker independence is judged in the narrower scope stated in the request
(PRECISION/PARTITION/GATING), not the wider scope in the v2 checker docstring.

Consequence, conditional as above, with contract A (Judge receipt 0e4b199b):
Phi is strictly decreasing in tau on [0,1/4], with Phi(0,lambda) = H_axis_ob(lambda) and
Phi(1/4,lambda) < 0. By the sign structure of A this gives, inside |t| <= 1/2: no nonzero
axial root for lambda < lambda_c^ob; only t = 0 at lambda_c^ob; and for lambda > lambda_c^ob
exactly one positive root in (0,1/2) with its negative mirror.

The claim of contract B, c3_ob(lambda) < 0 on [2/5,83/200], follows from C0a at t = 0
by Lemma 16 of the premise lemma (transfer lemma §3). This receipt records that
consequence but does not issue B's own Judge decision.

Exclusions as in the request: lambda outside [2/5,83/200]; 1/2 < t < 31/32;
connection to the boundary-entry branch; off-axis statements; the global census.
