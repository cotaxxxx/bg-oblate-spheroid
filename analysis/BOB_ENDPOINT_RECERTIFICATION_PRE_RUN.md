# B_ob ENDPOINT SIGN STRUCTURE — RE-CERTIFICATION PRE-RUN NOTE

**Status**: `PREDECLARED / MACHINE_NOT_RUN / NOT_BINDING`

## §1 Reason

The prior `CERTIFIED_ENCLOSURE` pin for the endpoint sign structure (`AUDIT_PIN.md` on branch `receipt-binding-e5ab171`, blob `e763bda81f71aa566786bda8144f4341c94b2fae`) names the source commit `7bdcbdcba3dab51c8ddbe72dac02c6307e1b5064`. On 2026-09-21 that commit was found unreachable from `origin` (upload-pack: not our ref; GitHub commit and object APIs: not found) and absent from every local clone examined. The prior certification is therefore not reproducible from the current repository and is not inherited. This note re-certifies the same claim on a reachable commit.

## §2 Claim

~~~
B_ob(5/8) < 0,     B_ob(33/50) > 0,     B'_ob(lambda) > 0 on [5/8, 33/50],
~~~

hence exactly one transverse zero of `B_ob` in `[5/8, 33/50]`, conditional on the two statements the checker records in `conditional_on`:

- (i) the endpoint-regular two-chart kernel is the analytic representation of `B_ob`, and differentiation under the integral is valid;
- (ii) the `t -> 1` one-sided limit identifies this zero with the boundary passage of the interior axial branch.

This run discharges neither condition. Condition (i) is to be discharged by the C1 endpoint lemma (`analysis/endpoint_kernel_lemma.md`, blob `aa6a1a17`); condition (ii) by the band theorem on `[31/32,1] x [5/8,33/50]`.

## §3 Code

All files are taken at the commit that adds this note, which fixes every blob below.

~~~
producer/endpoint_interval_producer.py          51060fea
checker/endpoint_interval_checker.py            4cb16f8a
checker/endpoint_local_controls.py              c913c47d
checker/oblate_axis_prototype.py                df402583
spec/endpoint_local_interval_contract_v1.json   1b667e21
requirements-interval.txt                       399cb569
tests/test_endpoint_interval_certificate.py     2511ea5e
controls/test_endpoint_algebra.py               ee529377
~~~

Relation to earlier audits. The five files other than the producer, the checker, and the certificate test are byte-identical to their versions at `701a2e8a54e57c3259973c20f44bb5abe355a628`, the audited base superseded by the lost pin. The producer, checker, and certificate test differ from that base only by (a) the series domain guard `u.lower() < 0` replacing the fail-open `u.upper() < 0`, (b) removal of the unused `Phi` series from derivative cells, and (c) receipt binding of the canonical record SHA-256 and source commit. Items (a) and (b) are the content the lost pin records as differentially audited; item (c) touches no enclosure computation. The full diff from `701a2e8a` was read by the chat audit on 2026-09-21.

## §4 Execution

At the commit that adds this note, with a clean worktree and an output directory outside the repository:

~~~
python -m unittest tests.test_endpoint_interval_certificate controls.test_endpoint_algebra
python producer/endpoint_interval_producer.py --output OUT/record.json --bits 160 --panels 1024 --degree 50
python checker/endpoint_interval_checker.py OUT/record.json --receipt OUT/receipt.json
~~~

Recorded before the tests and after the checker: HEAD, empty `git status --porcelain`, interpreter path and version, python-flint version, CPU. Recorded after: SHA-256 of `record.json` and `receipt.json`. The receipt must carry `record_sha256` equal to the SHA-256 of `record.json` and `source_commit` equal to HEAD. Any identity mismatch makes the run `NOT_EVIDENCE`.

The wheel filename and SHA-256 written into the record by the producer are constants of the source and do not verify the local environment; the recorded interpreter and python-flint version are the environment evidence.

## §5 Expected values (REPORTED, not gating)

From the prior certification:

~~~
B_ob(5/8)                 subset [-0.02549, -0.01581]
B_ob(33/50)               subset [ 0.01336,  0.02259]
B'_ob([5/8,33/50])        subset [ 0.4184,   1.8810 ]
~~~

The gate is the checker's three strict signs only.

## §6 Outcome

On checker PASS, a machine receipt records the identity, the two SHA-256 values, and the checker totals; the result then awaits human Judge. On any failure the run is recorded fail-closed and no code is modified to obtain a PASS.
