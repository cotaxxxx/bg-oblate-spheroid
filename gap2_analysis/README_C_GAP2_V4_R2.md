# C gap 2 v4-r2 — implementation submission (NOT FROZEN)

**Status:** STATIC IMPLEMENTATION SUBMISSION / NOT FROZEN / EXECUTION PROHIBITED / NOT_EVIDENCE.

**Base:** `cotaxxxx/bg-oblate-spheroid` `run/c-gap1-v0-5` at `26d81e1049340d44ef7f08ae8e17d0692983395b`. Submit as ONE new commit whose direct parent is that frozen commit. Nothing on the original run4 branch may be rewritten.

## Scope and allowed diff

- Modified both `gap1_{producer,checker}/global_axial_c1b_kernel.py`: add a seed parameter to `endpoint_gate`, allow exact rational `t_e` with `31/32 ≤ t_e < 1`, and construct `N=ceil(512(1-t_e))` equal rational t cells. The old default `31/32` branch preserves **exactly** run4's 16 cells and the old partition ID and output fields.
- Modified both `gap1_{producer,checker}/global_axial_c1b_gating.py`: add `gap2_endpoint_record` adaptor; existing gap1 paths remain unmodified.
- Added `gap2_analysis/sealed_contract.py`: SHA-chain/L0(c) loader and fail-closed C1b v2.4 right-exterior CLOSED-box coverage on both lineages. No sealed ledger is read on import.
- Added `gap2_analysis/endpoint_driver.py` and separate `gap2_producer/driver.py`, `gap2_checker/driver.py`: independent lineage numerical calculations; parent `t_e` passed unchanged to all descendants, same right-first lambda bisection depth≤3. No use of prior producer sign results by checker.
- Added `gap2_analysis/run4_regression.py`: **NOT YET RUN**. Deterministic run4 first/middle/last accepted endpoint samples; verify full endpoint record, rational strings, work counters and box order against the corresponding run4 producer/checker ledger.

**Numerical unchanged:** original `g_box`/`gt_box` sources, 160/192 bit, degree50, 8192 seed/Gt s-panels, corner/ordinary dispatch and sole `U_cum<0` sign gate.

**Reused frozen 25-blobs table:** `cotaxxxx/bg-spheroid-family` `runs/2026-10-12/C_GAP1_V0_5_RUN4/RUN_COMMIT_25_BLOBS.tsv` SHA256 `ec5b70b6cc8ebd0ab29fc31021ead613526cc3187efe09f1d6a6d795b810dd00`. Four true gate/kernel blobs in that table are `5503bb7d`, `b4bb44bd`, `baffaf49`, `36bb7983`. Run4 old blobs retain their identity in the PARENT, modified copies deliberately have new blob IDs.

**External frozen input** (L0(a)(b) confirmed SHA 4/4, L0(c)(d) UNREAD until Judge authorizes): `cotaxxxx/bg-spheroid-family`, `evidence/c-gap2-sealed-inputs-20261115`, `ff09197`. This implementation does NOT pin a guessed receipt schema: unknown receipt, right-exterior rows, or incomplete proof coverage stop rather than being treated as evidence.

## Static checks (only; no sealed data read)

```
cd <implementation-checkout>
python -m gap2_producer.driver --static-preflight
python -m gap2_checker.driver --static-preflight
python -m compileall -q gap1_producer gap1_checker gap2_analysis gap2_producer gap2_checker
```

**Run4 regression (after chat static audit, with frozen run4 ledgers only):**

```
python -m gap2_analysis.run4_regression --role producer --run4-ledger <RUN4_PRODUCER_LEDGER>
python -m gap2_analysis.run4_regression --role checker --run4-ledger <RUN4_CHECKER_LEDGER>
```

Each command recomputes numerical integrals; no regression command was launched while preparing this commit.

**Full execution is prohibited without a real Judge FREEZE ruling.** The new driver rejects unapproved execution, requiring a SHA-matched Judge ruling file containing the explicit FREEZE and execution authorization, plus an explicit opt-in environment variable. Do not treat this interface as an authorization to run; chat audits the implementation, regression and L0 contract before Judge decides.

The signed right-exterior interval is validated independently against both sealed C1b ledgers at authorized L0(c). A missing piece is a **FAIL**, not an inferred certification or an automatic fallback. Any later adjustment to schema/implementation must be reviewed in a NEW version/commit; no silent modification of this submitted commit.

**D6 V19:** chat paper/symbolic audit of C1/C2/G0E1 endpoint lemmas 4/4 PASS, ZIP SHA256 `ba2872915ee55ee7dbbe1871dec0ca4751240767fef82b441951b6263b53d424`. C1c/C0/C1d lemmas remain outside this step.

**Mathematical status:** C gap 2 still OPEN; D-OB global OPEN.
