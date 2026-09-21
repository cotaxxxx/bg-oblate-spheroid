# C0 V2 KERNEL — CHAT RAW AUDIT

**Status**: `CHAT_RAW_AUDIT_PASS / JUDGE_NOT_ISSUED / NOT_BINDING`

Evidence head `b8a25658a67cec2d750eef7c5b5ce037dfc6cadf`; run #38 (id `33576831323`), all steps success. Read in full on 2026-09-22:

~~~
producer/global_axial_c0_producer_v2.py   cdbdf51f
checker/global_axial_c0_checker_v2.py     fbec8905
producer/c0a_four_group_v2.py             2bb556ab
checker/c0a_four_group_v2.py              18e66b64
~~~

The base modules `c4c8d6b5` / `85978625` were chat raw-audited earlier (machine receipt `605c11c6`) and not re-read. A repository-side re-audit of request checks 1–8 reported PASS on 2026-09-22 and is recorded as `OWNER_RE_AUDIT_PASS`.

Findings:

1. The wrappers replace only `_g_density` (stabilized `alpha^2 = u R^2`) and `_g3_density` (four-group). The four-group width statistics, produced only by the v2 kernel, witness that the replacement took effect.
2. `K3 = -2 A lambda^4 N^4 / (w^4 q^6)`, `K2 = lambda^3 (8 mu N^3 q - 12 A N^2 M) / (w^3 q^{11/2})`, `K1` from the three `R_gamma` terms, and `K0 = 6 lambda^3 e G / (w q^{9/2})` with constant coefficient `4 e^2 mu^2` agree with the `C_ttt` assembly.
3. Nonnegativity intersections apply only to quantities known to be nonnegative. Positive-`q` powers require `q.lower() > 0`, else `ValueError` and the box is unresolved.
4. `_box(left, right)` encloses `[left.lower(), right.upper()]`: checked with python-flint 0.9.0 at 160 and 192 bits, six cases, both lineages.
5. The checker kernel is a separate transcription with identical formulas; independence scope as declared in the request.
