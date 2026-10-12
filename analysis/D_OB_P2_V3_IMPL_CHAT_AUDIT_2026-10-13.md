# CHAT AUDIT — D-OB P2 V3 implementation `cad6296a` — 2026-10-13

**Auditor.** chat, the sole auditor.
**Object.** bg-oblate-spheroid `candidate/dob-p2-v3-impl-20261013`: implementation `cad6296a73541e7346682efb2ee09f4879306f61` (parent `c0f099f946b28e00db95d9ece6c1da703a6dc3b9`), control stdout `b7cf270b0edbc9c022f2222949fe1a237ffb4b37` (parent `cad6296a`). Frozen documents on `design/d-ob-p2` `111c3169`.
**Method.** chat read the full `git diff c0f099f9 cad6296a` and the relevant unchanged code paths (`solve_initial`, `main`, `runtime_identity`, `checker_identity`, ledger loaders) from the GitHub bytes.

## Verdict
**PASS.** The main run is authorized under the run conditions in §3.

## 1. Frozen bytes
- SPEC V3 `511d2f37…9330` and CONTRACT V3 `f8db209a…b4e4` are byte-identical in `111c3169` and in `cad6296a`. The chat audit record in `111c3169` is byte-identical to chat's file (`58781546…f691`).

## 2. Diff (producer +14/−3, checker +25/−2, plus the two frozen documents)
- **Active list.** Producer `all_indices()` and checker `active_indices()` both skip exactly `{(7,7,0),(0,0,3)}` from the lexicographic 8×8×4 order. The checker's `initial_box` λ grid `2/5 + k·13/200` matches SPEC §6.
- **Complete traversal.** An unresolved node is recorded as an unresolved leaf and `solve_initial` returns normally, and kernel exceptions are mapped to unresolved. `pool.imap` therefore continues through all 254 boxes, and the new guard `INITIAL_TRAVERSAL_INCOMPLETE` catches a short result list. Exit 1 if and only if `unresolved > 0`.
- **SPEC identity (K5).** `runtime_identity()` reads SPEC V3 and stops with `SPEC_V3_IDENTITY_MISMATCH` unless the SHA-256 is `511d2f37…`. The ledger header identity therefore differs from every V2-era ledger, so no smoke ledger can be resumed into this run.
- **Coverage (F2).** `validate_initial_ids` requires set equality with the 254 active ids and then the exact order. Controls E (one id missing) and F (excluded id added) are rejected at the set test, which matches this code.
- **No numerical change.** The kernel, enclosures, ρ₀, chart, cut, budgets and subdivision rule are untouched. The checker still imports no producer module.

## 3. Run conditions (binding)
1. Run from a clean checkout of `b7cf270b`. The code bytes are those of `cad6296a`; the extra commit adds only stdout files.
2. Do not use `--initial`. It is a smoke-only restriction, and a main run that used it is NOT_EVIDENCE.
3. `identity_before.txt` and `identity_after.txt` carry every field of CONTRACT V3 §2, including the SHA-256 of SPEC V3, of CONTRACT V3, of the producer and of the checker.
4. If the run FAILs, the unresolved map in the receipt is built from the ledger `node_decision` records with `decision = "unresolved"`, which carry the node coordinates.
5. Before ignition, write the CONTRACT V3 §8 backup unit to USB and verify its SHA-256 there. The unit contains the P1 diagnostic script and log, SPEC V3, CONTRACT V3, the producer and checker at `cad6296a`, and this audit together with the earlier audit records. The 04:26 backup predates these files.
6. Launch with `setsid` and redirect into the run directory, as in the 09-22 lesson. Stop only with SIGTERM.

## 4. Record-only item (not blocking)
The dry-run and checker-control harness (the version fixed after the `dataclass` import error) was not committed. Commit it next to the stdout. The F2 conclusion rests on chat's reading of `validate_initial_ids`, not on the harness.
