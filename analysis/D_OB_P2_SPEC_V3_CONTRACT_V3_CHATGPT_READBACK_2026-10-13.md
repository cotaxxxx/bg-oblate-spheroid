# CHAT RAW AUDIT — D-OB P2 SPEC V3 / PRE-RUN CONTRACT V3 — 2026-10-13

**Readback by ChatGPT.**
**Object:** draft commit `db69919c0164ed8b78ce610f91676f4b6eba46b7` on `design/d-ob-p2`.
**Judge ruling audited:** 2026-10-13 D5 scope re-ruling: exclude initial boxes `(7,7,0)` and `(0,0,3)` as delegated analytic regions; run the retained initial boxes to completion even if unresolved boxes occur; map all unresolved output.
**Verdict:** **PASS WITH BINDING READINGS K1–K5 / FREEZE CANDIDATE ONLY.** This audit is not a Judge FREEZE and authorizes no main run.

## 1. Pins

- SPEC V2 SHA-256: `19af6f7f4aa68771707bc3ffe1abf06fabbbc3098b4bfe0710db00631b8bb069`.
- CONTRACT V2 SHA-256: `8461069aad635efe517008c52ce571a09b8d552f43726a9fccac508a2c093e27`.
- SPEC V3 draft SHA-256: `0e07fb4ec8c45ea366ba4abf4cddacdc1a10ce4bd1ed2eca5e32a69b3a90e26f`.
- CONTRACT V3 draft SHA-256: `372a6bfd88aac51d1b04268b87952b93e80bb68bf1a93e7ffe5dbd06ef738294`.
- Resume implementation pin: `c0f099f946b28e00db95d9ece6c1da703a6dc3b9` (`Make D-OB P2 execution resumable`).

Both V3 documents are marked `DRAFT / NOT_FROZEN / NOT_RUN / NOT_BINDING`.

## 2. SPEC V3 diff audit

PASS.

1. Title/status and `Supersedes` are changed to V3/draft state and record the Judge's smoke-#4 motivation.
2. §0 defines
   `P' = P \\ (relint_P(B_770) union relint_P(B_003))`, where relative interior is taken in `P`.
3. The entire numerical body §1–§6 is byte-identical to SPEC V2. Therefore the kernel, `rho_0`, chart rules, cut rules, resource budgets, initial grid, cell refinement and box-subdivision rules are unchanged.
4. §7 changes only the coverage target `P -> P'`; §8 changes only the not-claimed target `P -> P'`. These are required propagation of the §0 scope change and do not change a numerical rule.

The excluded initial boxes computed from the unchanged V2 grid are exactly:

- `(7,7,0)`: `r,tau in [7/8,1]`, `lambda in [2/5,93/200]`;
- `(0,0,3)`: `r,tau in [0,1/8]`, `lambda in [119/200,33/50]`.

The full grid has 256 ids; deleting exactly those two leaves 254 ids.

## 3. Smoke #4 source audit

PASS.

Independent readback of `basepoint-geometry-artifacts/D_OB_P2/smoke_20260923T121918Z_resumable/producer_ledger.jsonl` found unresolved terminal nodes in exactly two initial ids and no others:

- `(7,7,0)`: 4,078 unresolved nodes;
- `(0,0,3)`: 3,584 unresolved nodes;
- total: 7,662.

This matches the Judge's delegation split. `full_terminal_map.tsv` remains `DIAGNOSTIC / NOT_EVIDENCE`.

## 4. CONTRACT V3 diff audit

PASS.

- Active initial ids are the canonical V2 256-id order with exactly `(7,7,0)` and `(0,0,3)` skipped: 254 units.
- Producer policy requires traversal of all 254 active ids before terminal verdict. An unresolved result does not stop dispatch of later active ids. Any unresolved residue after the complete traversal gives producer exit 1 and run verdict `FAIL`.
- Checker is required on a producer-PASS candidate. A completed producer FAIL caused by unresolved residue is already `FAIL`; checker is not allowed to convert it into PASS.
- Receipt must retain a complete unresolved map: initial id, unresolved-leaf count and exact coordinate range(s).
- Historical smoke #4 is not rerun. C-R1, C-R2 and C-R3 must be rerun on the implementation candidate, plus an enumeration-only dry run requiring 254 active ids and the exact two-id exclusion set.
- CONTRACT V2 sections 1 (files/independence) and 5 (parallelism/determinism) are byte-identical. Environment/output wording changes only as needed to define the producer-FAIL terminal path.

## 5. Geometric coverage reading

For this grid, the union of the 254 retained closed initial boxes is exactly `P'` under the definition using **relative interior in `P`**. Shared grid faces of the two delegated boxes remain in `P'` and are covered by retained neighboring boxes; the delegated D-AN-1 Sigma / D4 regions are the full closed excluded boxes, so those shared faces also provide overlap for the later global assembly.

## 6. Binding readings

**K1 — `relint_P` is binding.** Do not replace it by ordinary Euclidean interior. The relative-interior definition is what makes the 254-box closed union equal the D5 claim region and removes the non-shared outer faces of the two delegated corner boxes from D5.

**K2 — SPEC §6 remains the generic 256-box grid.** CONTRACT V3 is authoritative for the active 254-id execution list. This is not a change to the §6 subdivision rule or numerical kernel.

**K3 — full-map FAIL is terminal evidence about the attempted D5 run, not a partial PASS.** If unresolved residue exists outside the delegated two boxes, all 254 active ids must nevertheless finish and the receipt must map the residue. Verdict remains `FAIL`.

**K4 — no smoke rerun.** The only pre-main-run execution gates are C-R1–C-R3 plus the enumeration-only 254/2 dry run, followed by identity checks fixed by CONTRACT V3.

**K5 — implementation identity plumbing.** The implementation candidate is to be a single direct child of `c0f099f9`, with numerical code changes limited to the active-box list / complete-traversal policy. Because `c0f099f9` currently records the SPEC identity from `analysis/D_OB_P2_CERTIFICATION_SPEC_V2.md`, the candidate must also carry the exact frozen V3 document bytes and mechanically bind the runtime SPEC identity to the frozen SPEC V3 SHA. This is provenance plumbing, not a numerical-kernel change; leaving the runtime identity pinned to V2 would make a V3 evidence run inadmissible.

## Conclusion

**SPEC V3 + CONTRACT V3 draft: PASS WITH K1–K5.** They are suitable for Judge FREEZE consideration. No implementation commit has been created and D5 main run remains **NOT STARTED**.
