# CHAT AUDIT — D-OB P2 SPEC V3 / PRE-RUN CONTRACT V3 — 2026-10-13

**Auditor.** chat, the sole auditor (roles record 2026-10-11).
**Object.** Draft commit `db69919c0164ed8b78ce610f91676f4b6eba46b7` on bg-oblate-spheroid `design/d-ob-p2` (parent `bbcfe662`): SPEC V3 draft SHA-256 `0e07fb4e…e26f`, CONTRACT V3 draft SHA-256 `372a6bfd…8294`.
**Method.** chat diffed SPEC V2 → V3 and CONTRACT V2 → V3 itself from the GitHub bytes. The readback committed at `d487e3f6` was written by ChatGPT, not by chat; it is kept as `…_CHATGPT_READBACK_2026-10-13.md` and is not this audit.

## Verdict
**PASS after two corrections, both applied in the frozen bytes below.** K1–K5 of the ChatGPT readback are adopted as binding readings.

## 1. Findings
- **F1 (mathematical claim; corrected).** SPEC V3 §0 kept the V2 sentence "the claim excludes interior stationary points of `E` with `rho > 0`, for every `lambda` in `[2/5, 33/50]`". After the excision this sentence overclaims, because nothing in V3 covers the relative interiors of `B_770` and `B_003`. The sentence now reads: exclusion at base points with parameters in `P'`; the two boxes are delegated to D-AN-1 Σ and D4; the exclusion for every λ follows only after those are closed.
- **F2 (soundness of the coverage check; corrected).** The checker's coverage target changes from `P` to `P'`, which is a change in the checker code, but no pre-run control exercised it. CONTRACT V3 §7 now adds three kernel-free checker controls: (d) 254 active ids → pass; (e) one active id removed → fail; (f) one excluded id added → fail. It also requires the set of initial ids to equal the 254 active ids exactly.

## 2. Checked and found correct
- SPEC V3 vs V2: besides F1, the only changes are the title, status, Supersedes (motivation per CONTRACT V2 §7), §0 domain `P'`, and `P → P'` in §7 and §8. §1–§6 are byte-identical.
- `P'` equals the union of the 254 retained closed initial boxes: `B_770` and `B_003` do not meet, every shared face stays in `P'`, and the outer faces of the two boxes on `∂P` lie in `relint_P` and are removed. `(7,7,0)` = `[7/8,1]²×[2/5,93/200]` equals D-AN-1 Σ exactly (λ step 13/200); `(0,0,3)` = `[0,1/8]²×[119/200,33/50]`.
- CONTRACT V3 vs V2: the changes are the SPEC pin, the 254-id active list in canonical order, complete traversal with exit 1 / FAIL on unresolved leaves, the identity-after definition on the FAIL path, the full unresolved map in the receipt, and C-R1–C-R3 plus the 254/2 dry run replacing smoke. §1 (independence) and §5 (parallelism) are unchanged.

## 3. Frozen bytes
- `analysis/D_OB_P2_CERTIFICATION_SPEC_V3.md`: 11,473 B, SHA-256 `511d2f371784a07359c2b691abfb224ef772cddf298f2890b5596a5dc2309330`.
- `analysis/D_OB_P2_PRE_RUN_CONTRACT_V3.md`: 9,352 B, SHA-256 `f8db209ad896f8ddc49015ae54a20cc837f38abe94d5f44065e7c4ac9c22b4e4` (it pins the SPEC SHA above).
- K5 therefore binds the implementation's runtime SPEC identity to `511d2f37…9330`, not to `0e07fb4e…`.
