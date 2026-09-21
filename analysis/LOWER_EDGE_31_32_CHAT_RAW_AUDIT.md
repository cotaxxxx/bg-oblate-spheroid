LOWER-EDGE 31/32 ANCHOR — CHAT RAW AUDIT
Status: CHAT_RAW_AUDIT_PASS / JUDGE_NOT_ISSUED / NOT_BINDING
Receipt: 3e2dfb04 (claim g_axis_ob(31/32,lambda) > 0 on [5/8,33/50], 8 exact boxes)
Source commit: efb6b5bacf13e9d0bf98e40d04904e1d5a66953a

Files read in full (blob / SHA-256):
  producer/census_lower_edge_31_32_producer.py  8b3cb9ab / 06238e85
  producer/census_lower_edge_producer.py         ec0afd45 / 7782c4cd
  producer/endpoint_interval_producer.py         51060fea / 19e37471
  producer/monotone_tube_interval_producer.py    b6d96df2 / 0c23fddb
  checker/census_lower_edge_31_32_checker.py     b11617f3 / e7ff8e4b
  checker/census_lower_edge_checker.py           1b8f4542 / 2ab85641
  checker/monotone_tube_interval_checker.py      78ae54ef / c9be5ab1

Findings:
  1. Density = -s mu alpha^2 + 2 lam R A rho^3 H / w equals F_t = s[-mu alpha^2 - 2 A R gamma_t]
     via gamma_t = lam N/(w q^{3/2}), N = -s^2 H. The historical A/sqrt(q) coefficient
     error is absent.
  2. s-partition covers [0, sqrt 2] exactly; lambda split exact.
  3. Checker imports no producer module. Its density is the same formula re-written,
     not an independent derivation; independence consists of separate code, 192 bits,
     independent partition construction, and chart-count agreement.
  4. The identification of the integral with g_axis_ob(31/32,lambda) is supplied by
     Lemma 11 of the C1d analytic lemma (blob 35656381), since (31/32,lambda) lies in B'.

Trust boundary: Arb primitive enclosures; the run outputs are those recorded in 3e2dfb04.

Effect: discharges the audit condition of §9(1) of the C1d pre-run contract (commit 957848e9) for this anchor.
