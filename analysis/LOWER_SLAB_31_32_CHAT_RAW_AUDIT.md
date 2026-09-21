# LOWER SLAB [31/32, 63/64] — CHAT RAW AUDIT

**Status**: `CHAT_RAW_AUDIT_PASS / JUDGE_NOT_ISSUED / NOT_BINDING`

Receipt: `3e2dfb04` (claim A: `partial_t g_axis_ob < 0` on `[31/32,63/64] x [5/8,33/50]`; Actions run #147, id `33371387643`).
Source commit: `efb6b5bacf13e9d0bf98e40d04904e1d5a66953a`.

Files read in full (blob / SHA-256):

~~~
analysis/MONOTONE_TUBE_LOWER_SLAB_CONTRACT.md    61068734 / 69d69e67
producer/monotone_tube_lower_slab_producer.py    e927cda5 / 90a26bbc
checker/monotone_tube_lower_slab_checker.py      3d38a16e / 3dbb527d
~~~

Kernel. The producer evaluates cells with `_ordinary` from `producer/monotone_tube_refinement_producer.py`, blob `c2fee400` at the source commit; the checker uses `_ordinary_refinement` from `checker/monotone_tube_refinement_checker.py`, blob `fd778d6d` at the source commit. These are the blobs recorded as chat raw-audited for the upper tube in `analysis/MONOTONE_TUBE_REFINEMENT_RAW_AUDIT.md` (blob `c3b3666d`); they were not re-read here. The remaining imports (`endpoint_interval_producer` `51060fea`, `monotone_tube_interval_producer` `b6d96df2`, `monotone_tube_interval_checker` `78ae54ef`) were read in full on 2026-09-21 in the lower-edge anchor audit.

Findings:

1. The `t` domain `[31/32,63/64]` and the `lambda` domain `[5/8,33/50]` are each split into 8 exact equal boxes (64 boxes). The `s` partition covers `[0, sqrt 2]` exactly at 1024 panels per unit, and is constructed independently in each lineage.
2. Every `s` cell is evaluated by the ordinary-cell kernel; no corner branch exists. Since `delta >= 1/64` on the slab, `q > 0` at `s = 0`.
3. Box totals are sums of cell enclosures of `T1 + T2 + T3` times cell width. Both lineages gate on `total.upper() < 0`; the checker also requires exact agreement of box labels and chart counts, and the producer's `gating_pass`.
4. The checker imports no producer module.
5. By the Proposition of §6 of the band C2 lemma (`analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA_31_32.md`, commit `f66ffe5a`, blob `5c3dfeb3`), the enclosed quantity is `partial_t g_axis_ob` on each box.

Trust boundary: Arb primitive enclosures; the run outputs are those recorded in `3e2dfb04`.

Effect: closes audit item (5) of the band C2 lemma for the lower slab.
