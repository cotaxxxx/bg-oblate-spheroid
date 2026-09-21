# OBLATE LOCAL BOUNDARY ENTRY — BAND [31/32, 1] JUDGE REQUEST

**Status**: `EXTERNAL_JUDGE_REQUESTED / NOT_BINDING`

**Scope.** `t` in `[31/32, 1]`, with `t = 1` understood one-sidedly, and `lambda` in `I = [5/8, 33/50]`. This request supersedes, as the request to be judged, the template `analysis/LOCAL_ENTRY_JUDGE_RECEIPT_TEMPLATE.md` (blob `5389bfba`), which is not modified.

## §1 Claims to judge

~~~
Claim 1   partial_t g_axis_ob(t,lambda) < 0   on [63/64, 1]    x I   (t = 1 one-sided)
Claim 2   partial_t g_axis_ob(t,lambda) < 0   on [31/32, 63/64] x I
Claim 3   g_axis_ob(31/32, lambda) > 0        for lambda in I
~~~

## §2 Machine evidence

All runs belong to the workflow `.github/workflows/oblate-gt-boundary-prototype.yml` (workflow id `346289126`). On 2026-09-21 each run's head commit was read from the GitHub API and its tree was checked locally for the blobs listed.

**Claim 1.** Contract `5808e845`; producer `producer/monotone_tube_refinement_producer.py` `c2fee400`; checker `checker/monotone_tube_refinement_checker.py` `fd778d6d`; test `tests/test_monotone_tube_refinement.py` `99c2a196`. The step "Run separately declared monotone tube refinement" succeeded in three runs whose head trees contain all four blobs:

~~~
run #87    id 33362970980   head 2f1186386a329a61a51d125245b5bc8971b6610e
run #101   id 33368313307   head dbe215cfa7e4cbb549dc909382bc83a3e7019fad
run #147   id 33371387643   head efb6b5bacf13e9d0bf98e40d04904e1d5a66953a
~~~

Raw audit: `analysis/MONOTONE_TUBE_REFINEMENT_RAW_AUDIT.md` (blob `c3b3666d`).

**Claims 2 and 3.** Run #147 (head `efb6b5ba`), step "Run lower slab and 31/32 edge gates", succeeded; test `tests/test_lower_slab_and_edge_31_32.py` `9f03d6f5`. Machine receipt `analysis/LOWER_SLAB_31_32_MACHINE_RECEIPT.md` (commit `3e2dfb04`).

~~~
Claim 2   contract 61068734   producer e927cda5   checker 3d38a16e
          worst independent-checker upper  -1.13084988282485256603...
          raw audit analysis/LOWER_SLAB_31_32_CHAT_RAW_AUDIT.md   commit ab97724a  blob 138b3cee
Claim 3   producer 8b3cb9ab   checker b11617f3
          weakest lambda box [5/8, 1007/1600], independent-checker lower  +0.00481079813050572...
          raw audit analysis/LOWER_EDGE_31_32_CHAT_RAW_AUDIT.md    commit cca99bef  blob c9e3ef8b
~~~

**Meaning of a step success.** Each of the two tests calls the producer, passes its record to the checker's `verify`, which raises on any gate failure or record mismatch, and asserts the producer's `gating_pass`. A successful step therefore means that both lineages passed the gate.

**Workflow-level conclusions.** Runs #87, #101 and #147 each conclude `failure`. In each case the failing step is a later, separately declared historical control — the fixed initial 64-box tube contract (#87, #101) or the superseded `t = 63/64` lower-edge refinement (#147) — and is not part of this request.

## §3 Analytic pins

~~~
C1 lemma   analysis/OBLATE_ENDPOINT_C1_LEMMA.md
           commit aefa8ed24f257694d5b1e349ef7478b9c1e5b807   blob 5afa815ff24760ab5ebbb63bcbae912c9c7a84c6
C2 lemma   analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA_31_32.md
           commit f66ffe5a0567053c5b2fdeaaeb5d2380b961e08e   blob 5c3dfeb3d0283aae50df7cd26af2621c2fa39aec
~~~

Both are `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`. They supply: `g_axis_ob = integral F_t ds` on `[1/2,1)`, which identifies the Claim 3 quantity with `g_axis_ob(31/32,lambda)` (C1 Lemma 3); `partial_t g_axis_ob = integral G_t ds` on `[31/32,1)` with the one-sided derivative at `t = 1`, which identifies the Claim 1 and Claim 2 quantities with `partial_t g_axis_ob` (C2 §6); and `g_axis_ob(1,lambda) = B_ob(lambda)` with `g_axis_ob(·,lambda)` continuous on `[1/2,1]` (C1 Lemma 5).

## §4 External input: endpoint sign structure

`analysis/BOB_ENDPOINT_RECERTIFICATION_MACHINE_RECEIPT.md`, commit `705623b07fc900afd6df6908555db8028dee98ce`, blob `399776b9c5008313ab071651457b18b9f8310137`, machine gating PASS on the reachable commit `5ba56eb1`: `B_ob(5/8) < 0`, `B_ob(33/50) > 0`, `B'_ob > 0` on `I`. Its condition (i) — that the two-chart kernel represents `B_ob` and that differentiation under the integral is valid — is supplied by Lemmas 5 and 6 of the C1 lemma. Hence `B_ob` has exactly one zero `lambda_partial` in `(5/8, 33/50)`, with `B_ob < 0` before it and `B_ob > 0` after it.

This request uses only that sign structure. The receipt's condition (ii) — the identification of this zero with the boundary passage of the axial branch — is not an input here; it is a consequence of §6.

## §5 Uniform margin

Claims 1 and 2 are established on 128 parameter boxes, each with an independent-checker enclosure of `integral G_t ds` whose upper endpoint is negative. Let `M > 0` be the minimum over these boxes of the negated upper endpoint. Then

~~~
partial_t g_axis_ob(t,lambda) <= -M < 0     on [31/32, 1] x I.
~~~

Only `M > 0` is used below. For reference, the template records `M_EXACT = 0.77557919579513414984...` from a diagnostic reconstruction (run #159), with the upper tube as the limiting side; that run was not re-verified on 2026-09-21 and the argument does not depend on its value.

## §6 Consequences, only after PASS of Claims 1–3

For each fixed `lambda` in `I`, §5 makes `t -> g_axis_ob(t,lambda)` strictly decreasing on `[31/32,1]`. With Claim 3 and `g_axis_ob(1,lambda) = B_ob(lambda)` (§3), the sign structure of §4 gives:

~~~
lambda < lambda_partial :  exactly one root t*(lambda) in (31/32, 1)
lambda = lambda_partial :  the unique root in [31/32, 1] is t = 1
lambda > lambda_partial :  no root in [31/32, 1]
~~~

**Boundary convergence.** For `lambda < lambda_partial`, the mean-value theorem on `[t*(lambda), 1]` gives `B_ob(lambda) = partial_t g_axis_ob(xi,lambda) (1 - t*(lambda))` for some `xi`, so `0 <= 1 - t*(lambda) <= |B_ob(lambda)| / M`. Since `B_ob` is continuous (C1 Lemma 6) and `B_ob(lambda) -> 0` as `lambda -> lambda_partial` from below, `t*(lambda) -> 1`.

**Entry parameter.** Hence the parameter at which the unique axial root in `[31/32,1]` reaches the boundary is `lambda_entry,ob = lambda_partial`, within the band. This discharges condition (ii) of the `B_ob` receipt for the band.

## §7 Exclusions

This request does not claim: roots with `t < 31/32`; off-axis stationary points; any statement for `lambda` outside `I`; continuity or `C^1` regularity of the root branch `t*(lambda)` beyond the boundary convergence above (joint regularity of `g_axis_ob` in `(t,lambda)` for `t < 1` is not pinned); the sign of `dt*/dlambda`; a global no-fold statement; any promotion of the historical controls named in §2.

## §8 Requested Judge output

~~~
PASS
FAIL: <specific mathematical or provenance defect>
UNRESOLVED: <specific missing obligation>
~~~

A PASS must list the blobs, commits and runs actually relied upon and confirm the exclusions of §7.
