# Dig receipt: Plan B chat V6 acceptance and Judge V7 adoption (2026-11-14)

- Archive V6 SHA256: `76bf7e49cae140ef9c3d57b49e038f2bb2be557312ad55e9cbf6275505eb65cf`. ZIP CRC PASS, 6/6 internal SHA256SUMS PASS. Extracted exact original files and archived the ZIP bytes.
- Archive V7 SHA256: `f490ec9c72c102da883768ff4039e0c47aac05d33a3a358f384ee450028fd17c`. ZIP CRC PASS, ruling SHA256 `27ab75658d8a2c04e795561f36da5f7de43ef16eec02fb2b8b5b0791f4977bbc`. Extracted exact original file and archived the ZIP bytes.
- Standalone CHAT_ACCEPTANCE SHA256: `3b770caf30def563d7f5e2c7f37c1561548113c1673426d51085531ca235c594`, byte-identical to V6 member.
- Chat cover log: `COVER PASS`, 11745 final leaves, 9984 cells, failures 0.
- Chat resample: 200 random + minimum = 201 unique names. 201/201 match flags and H exact strings. Level0=199 and level1=2. All compared to original local `planb_run_out.jsonl` records, 201/201 matching H strings. This is a receipt-level check, not a fresh arithmetic recomputation.
- Judge V7 2026-11-14 ruling **「採用＋producer は事後補強」**. D5 thick collar PB-RUN-1 accepted for r∈[15/16,1−2^-16], τ∈[0,1], λ∈[2/5,33/50]. OPEN=0, min H_B^-=+0.0025242748771583325, strict rational positive. 97 REFINE parents -> 194 positive level1 children.
- Producer independent comparison remains pending as **post-adoption reinforcement**. If any producer-vs-verifier relative difference >1e-6, report to chat and reconsider adoption.
- Main binding STATE v1.52 can be updated to v1.53 to reflect this ruling. **Do not state D5 whole-domain unconditional CLOSED**: P1 and FT_q linkage remain global conditions. Do not touch V5.3 FROZEN, frozen Plan B code, or historic authorships.
