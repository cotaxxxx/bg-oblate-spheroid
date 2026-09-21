# B_ob ENDPOINT SIGN STRUCTURE — RE-CERTIFICATION MACHINE RECEIPT

**Status**: `MACHINE_GATING_PASS / JUDGE_NOT_ISSUED / NOT_BINDING`

## 1. Claim and conditions

~~~
B_ob(5/8) < 0,     B_ob(33/50) > 0,     B'_ob(lambda) > 0 on [5/8, 33/50],
~~~

hence exactly one transverse zero of `B_ob` in `[5/8, 33/50]`, conditional on (i) the endpoint-regular two-chart kernel being the analytic representation of `B_ob` with valid differentiation under the integral, and (ii) the `t -> 1` identification of this zero with the boundary passage of the interior axial branch. Neither condition is discharged by this receipt.

## 2. Pre-run note and source

Pre-run note: `analysis/BOB_ENDPOINT_RECERTIFICATION_PRE_RUN.md`, commit `5ba56eb1dd657b48f828041f196e9a418a429a9a`, blob `33b97cbbec6865755518c7bf23d0b98307830d84`. The run was made at that commit; the code blobs are those listed in §3 of the note.

This receipt replaces, as evidence, the prior pin naming the unreachable source commit `7bdcbdcba3dab51c8ddbe72dac02c6307e1b5064`. That pin's history is retained and not relied upon.

## 3. Run

Output directory `recert_20260921T133307Z`, outside the repository.

Identity, identical before the tests and after the checker: HEAD `5ba56eb1dd657b48f828041f196e9a418a429a9a`, clean worktree, Python 3.11.16 (`/home/daybreak/.pyenv/versions/3.11.16/bin/python`), python-flint 0.9.0, CPU AMD Ryzen 9 9900X 12-Core Processor.

Pre-run tests `tests.test_endpoint_interval_certificate` and `controls.test_endpoint_algebra`: 20 tests, OK.

Producer: 160 bits, 1024 panels per unit, series degree 50; three evaluations of 1,449 cells each.

~~~
record.json   SHA-256 e060f9006fb47d938fe87bbadd512d8bfe8fdc35855bfc937a6b6eaef53980c9
receipt.json  SHA-256 51fdaf676dcce520dbf19995a142aab5c61938453678d3cb9c312aa2a54a0475
~~~

Checker receipt: status PASS; `source_commit` equals the HEAD above; `record_sha256` equals the SHA-256 of `record.json`; `conditional_on` has two entries.

## 4. Checker enclosures

Truncated; the full values are in `receipt.json`.

~~~
B_ob(5/8)              in [-0.0254893476,  -0.0158072135 ]
B_ob(33/50)            in [ 0.01336182771,  0.02259273537]
B'_ob([5/8,33/50])     in [ 0.41840131816,  1.88100160707]
~~~

All three separate from zero with the signs of §1.

Comparison with the values reported in §5 of the pre-run note (not gating): the two endpoint enclosures agree to all displayed digits; the derivative enclosure lies inside the earlier `[0.41835218, 1.88100252]`, which came from the first candidate run before the differential audit fixes.

## 5. Status

Machine gating PASS on a reachable commit. The source differences from the audited base `701a2e8a` were read in full by the chat audit (pre-run note §3). Human Judge not issued. Condition (i) is to be discharged by the C1 endpoint lemma, condition (ii) by the band theorem.
