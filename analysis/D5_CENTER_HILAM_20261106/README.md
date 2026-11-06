# D5 high-lambda center column: computation evidence, adoption pending

Registered 2026-11-06 JST by Dig/Codex at the user's request.
Target: lambda in [119/200,33/50]; M40' on 0 <= rho <= 1/8, 0 <= z <= lambda/8; M22' on rho=0, 0 <= z <= lambda/8.

**All three computations exist and satisfy their numerical thresholds. This registration is not formal adoption.**
The old M40 1,248-box and M22 156-box runs cover [2/5,119/200], not this high-lambda band.

| Component | Completed computation | Existing second implementation | Formal adoption |
|---|---|---|---|
| C0' | Dig exact Bernstein calculation, H lower = 1.4641310094381321... >= 7/5 | Original chat reference coefficient comparison pending | Pending |
| M40' | Producer 416/416 >= -400; worst -47.40499577249319... | chat verifier 416/416 >= -400; worst -68.6322956611115... | Pending |
| M22' | Producer 52/52 >= -200; worst -46.75005927034623... | chat verifier 52/52 >= -200; worst -42.69154354653672... | Pending |

All decimals are references only; exact rational values are retained in the bundles and compact indices.

## Evidence

- [C0' original exact result](raw/c0_prime_dig_exact.json) and [original script](raw/c0_prime_independent.py).
- [M40' paired full bundle](m40_hilam_bundle.json), [compact exact bounds](m40_hilam_bounds_compact.jsonl).
- [M22' paired full bundle](m22_hilam_bundle.json), [compact exact bounds](m22_hilam_bounds_compact.jsonl).
- [Read-only registration check](REGISTRATION_CHECK.json).
- [Byte-preserving source manifest](SOURCE_MANIFEST.json).
- Original computation files, statuses, per-box records, and M40 DONE files are copied unchanged under raw/.
- Unchanged evaluator/driver snapshots are under sources/. The scripts retain their original absolute paths; this is an evidence snapshot, not a newly portable execution environment.
- M22 had no standalone DONE.json in the source directory. The new bundle explicitly stores original_done_records=null and a separately labeled registration completeness check; no original completion marker was invented.

## Checks performed during registration

Exact rational construction check: 13 adjacent lambda intervals from 119/200 to 33/50, eight rho intervals for M40, four z intervals up to each lambda band's upper endpoint divided by 8. All producer/verifier rows match their cover one-to-one; indices are complete and unique. All exact lower bounds meet -400 (M40) or -200 (M22). Existing M40 DONE minima match the raw rows.

The C0 stored polynomial was independently converted to all 19 Bernstein coefficients and matched exactly, with H >= 7/5. This is an internal arithmetic consistency check, not a comparison with the absent original chat c0_hilam.py, nor a new proof of the inherited analytic assumptions.

No expensive interval integrations were rerun. The independent verifier outputs already present on the external PC were inspected. M40 verifier source SHA matches d39be478485cb1faaf804ddbf970ce1c790b0d7a5d0bf7f2fb400561c2cdad1b; M22 verifier source matches b4ea57e134150e57be8ced020eafa4cfd6c740af75d27939b108e23de38d6a89. M22 verifier rows do not embed source hashes; the driver and current source snapshot supply provenance, subject to chat review.

## Remaining adoption conditions

1. C0': compare the exact coefficients/minimum with chat's original high-lambda reference (c0_hilam.py, reported SHA prefix e3b65e0f).
2. Fixed-cover identity: actual high-lambda files were explicitly marked diagnostic candidates. Their byte hashes differ from the instruction's pins:
   - M40 actual cfd50476b22b1d01997939688d51893a3d3ceac2c06391b809bfd0a43c719329; expected 2082e711a4d0e9a68947ed40ed358aff6eb9bab2f6fe34213b068ea3b8a03d87.
   - M22 actual f5d0ce5a3169b4bf823c1b81f43eb6bfee5f0f948c62f0ee2fdc9dcd5ce011f5; expected d7fc47723f35600a0753984e60ca0c1c0494fab3515494f744412a5fc4925580.
   Their geometry matches the instruction formula, but the pinned source files were not located. Chat must check full cover/mesh equivalence and Judge must dispose of the differing pins. Do not silently rewrite the recorded hashes or promote diagnostic statuses.
3. Chat's independent audit of these registered results and Judge's formal disposition remain pending.
4. The center-column conclusion retains the upstream P1 hypotheses. With the three bounds formally accepted, the stated arithmetic margin is 7/5 - (1/64)*max(400/6,(33/50)^2*200/2) = 43/120 > 0.

Existing calculation processes, source files, certificates, and the working repository were not changed. Only copies and registration documents were created in a separate checkout.
