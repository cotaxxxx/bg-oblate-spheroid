# D5 (D-OB P2 V3) run — Judge abort ruling and stop record (2026-10-18)

Recorded by chat. The ruling is the Judge's. Status of the run: **D5 V3: ABORTED / NOT_EVIDENCE.**

This is not the completed-traversal FAIL of CONTRACT V3 §6. The ledger is preserved as diagnostic material.

## 1. Run
| Item | Value |
|---|---|
| run dir | `~/basepoint-geometry-artifacts/D_OB_P2/run_20261012T205303Z` |
| started | 2026-10-12T20:53:03Z (10/13 05:53 JST) |
| producer | parent pid 1102346, `producer/d_ob_p2_producer.py`, 12 workers |
| interpreter | `/home/daybreak/.pyenv/versions/3.11.16/bin/python` |
| ledger header | identity pin check 4/4 MATCH, as reported by the read-only monitor |

## 2. State at the ruling
The figures below come from the read-only monitor, which parses the ledger. They are NOT_EVIDENCE.
- **Initial boxes:** 9/254 complete, 12 in progress, 233 not started.
- **Node decisions at stop:** accepted 1200, split 44925, unresolved 43654.
- **Where the unresolved leaves are:**
  - Every unresolved leaf shown lies in the i_r = 0 column (r ∈ [0, 1/8]).
  - At small τ, about 3,500–3,600 unresolved leaves per initial box (box depth limit 12).
  - The count falls quickly as τ grows. Examples: (0,3,1) has 253, (0,5,0) has 50.
- **Box-completion count:** an initial box is complete when 1 + split − accepted − unresolved = 0. This is exact, because every split creates exactly two children (`PBox.split`) and each node is decided once.

## 3. Judge ruling (2026-10-18)
**"停止して方式を作り直す"** — stop the run and rebuild the method.

**Reason.** CONTRACT V3 makes the run FAIL as soon as one unresolved leaf exists, and 43,654 already exist. The pace also projects to months of exclusive use of the research PC. The original estimate was 150–170 h; about 120 h had already been used.

The ruling replaces the V3 §6 obligation to traverse all 254 boxes for this run only. V3 itself is not edited.

## 4. Stop procedure and result (2026-10-17T22:30:38Z = 10/18 07:30 JST)
1. Process checked: `ps -o pid,etime,cmd -p 1102346` showed elapsed 5-01:36:49 and `.../python -u producer/d_ob_p2_prod…`.
2. Stopped: `kill -TERM 1102346`. After 20 s, `pgrep -f d_ob_p2_producer.py` found nothing (`ALL_STOPPED`).
3. Ledger integrity:
   - the last byte is `\n`;
   - there are 13 `interruption` records (parent and 12 workers; actor `signal:15`);
   - LOCK was removed by the producer's own `finally`.
4. Nothing was written into the run dir by the stop procedure. The run dir now contains `identity_before.sha256`, `identity_before.txt`, `producer.log`, `producer.pid`, `producer_ledger.jsonl`.
   - `identity_after.txt` was not recorded. This is not needed for an ABORTED run.
   - No certificate and no summary were produced.
5. SHA-256 after the stop, also saved to `~/D5_STOP_SHA256_20261018.txt`:
   - `producer_ledger.jsonl` (89,793 lines): `5c74c09dc1e8dd2dda3ad6ab7d020b609c814b31d1984e56d547565177d34012`
   - `producer.log`: `a171d53008e8b8e238e93aa77b942fe6a8d6699fb6dca4e22e82f9426b1c7971`

The ledger is resumable under the V3 resume rules, but no resume is authorized.

## 5. Next steps (redesign, each requiring audit and Judge ruling)
1. **Cause analysis.**
   - The working hypothesis is the near-column hull loss identified in the D4 source audit (§6): s ∈ [−ρ, ρ] is kept after ρ > 0 is fixed, so the averaged structure is lost.
   - It is now seen across the whole i_r = 0 column, not only (0,0,3).
   - Confirm it from the ledger. The node records contain no L or B_cut values, so the stdout or new diagnostics must be used.
2. **Hand the i_r = 0 column (r ≤ 1/8) to the D4-type analytic method** (center lower bound plus Taylor remainder).
   - The D4 center bound m* is proved only for λ ∈ [119/200, 33/50]. It must be re-derived on the full λ range [2/5, 33/50].
3. **NOT_EVIDENCE diagnostic on selected i_r ≥ 1 boxes** to test whether the V3 method closes there. The selection rule must be fixed before the diagnostic runs.
4. **CONTRACT V4:** narrow the D5 domain accordingly, then audit, FREEZE, and run.

The research PC is free.
