# Plan B RUN1 final producer handoff (2026-11-13)

**Numeric result and Dig cover PASS; awaits independent chat re-cover and 200-box audit, then Judge. Not a formal adoption.**

- Repository `cotaxxxx/bg-oblate-spheroid`, branch `evidence/d5-planb-run1-20261112`
- All basic records: 11,648. Basic POS: 11,551. Basic REFINE: 97 (j6=3,j7=14,j8=34,j9=46).
- Each REFINE parent split into two level-1 children: 194/194 strictly positive. No level-2 children; OPEN=0.
- Final leaves: 11,745, min exact H_B^- `35680063385905506296772740487309731144185038559378064487291542173837499/14134777360725407985123873589287569595983329726165714869365739644828778496` (~0.0025242748771583) in `PB_j08_b0_t15_l05`.
- Frozen tool `chat_planb_run.py` SHA256 `bfb2ff6f9509ffc07362402a123ccaaf3f0242ac1c6236442914e9f31fee6df5`. All 14 frozen objects listed in `pbrun_pkg/SHA256SUMS` passed `sha256sum -c`; Muse tool audit was completed on 2026-11-12, so it is *not* repeated.
- Run 2026-11-13 22:56 JST with Python 3.11.16: `python3.11 -I chat_planb_run.py cover --out planb_run_out.jsonl`. Exit=0, `final records 11745, cells 9984, failures 0`, `COVER PASS`.
- The outdated run status label `VERIFIER_ONLY_PENDING_MUSE_COVER_AND_CHAT200` was a misnomer. Correct status after Dig cover: `DIG_COVER_PASS_PENDING_CHAT_COVER_AND_CHAT200_AND_JUDGE`. The frozen tool and original logs were **not edited**.
- Uncompressed JSONL SHA256: `ec1fd1357d9b39a3e7008dfe65c938b1c855ab20276672b7263180de1c844c78`, size 52037317 bytes.
- `planb_run_out.jsonl.gz` uses gzip level 9, mtime 0 and no embedded filename. Compressed size 13456037 bytes. Decompression readback matches source SHA256.
- `SHA256SUMS` lists the transferred compressed JSONL and raw cover output.
- Next: chat independently obtains the ZIP and re-runs cover; 200-box exact sampling is planned as two sets of 100; then Judge acceptance. D5 overall remains OPEN until these conditions are established.
