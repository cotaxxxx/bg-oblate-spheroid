# CHAT AUDIT — D-OB P2 / FT_q South 39′ and South Positive-Mass Lemma (2026-10-10)

Status: CHAT AUDIT PASS (mathematics + machine evidence). South 39′ becomes CLOSED only after the canonical commit below is read back by chat.
Scope: south side only ([-1, mu_C) pointwise sign, [-1, 1/2] integrated mass). North far / near band, c_FT, BPL and D-P2 are NOT affected.
D-P2: NOT_CERTIFIED (unchanged).

## 1. Audited objects (SHA-256 verified against the pins of the south paper proof §0)
| object | pin |
|---|---|
| South paper proof | basepoint-geometry 05668a47216e243450211f0cf438702dc6d1527c, blob a66ac60e, SHA-256 f320acb964cb278d1dd8ef6240fcc88bc9bdf77ae75edd4c77f86ce78da93d3c |
| Astra 39′ report | D_OB_P2_certificate39prime_independent_report_2026-10-08.md, SHA-256 1d084881ffe60fb4fb7f7f37ac48aae06ba6be2693f76fd2b091d222a0c60d9f |
| Astra 39′ script | certificate39prime_exact.py, SHA-256 4b51bd9b57bb83c40737f6c10ce61fab736ed08334f29ed430a5825d8b0d8888 |
| Astra 39′ coefficients | certificate39prime_coefficients.json, SHA-256 853d022e0fa8720a99f34a81b5ff5664e0c2c6f6fa6fa2e6fdccc78fe4d40a80 |
| bernstein_G.py | f74e1221, blob 15a77344, SHA-256 97057844…23e3 |
| bernstein_south_A.py | f74e1221, blob 48a185c3, SHA-256 977f6294…a0af |
| theta_14_over_5_cert.py | 6621f3d9, blob 95501111, SHA-256 f0ab87b1…8b88 |
| kernel_extension_cert.py | 1ac44469, blob 3600e077, SHA-256 3c4b0d45…6e85 |

## 2. Coverage (paper)
- J = [-1/4, mu_C): Lemma A (Astra 39′ C1–C4); certificate box mu in [-1/4, 3/5] contains J because mu_C < 3/5 (C4b).
- K = [-1, -1/4]: Lemma B (kernel extension); the seam mu = -1/4 lies in both closed boxes.
- [-1, 1/2]: Lemma C, int G >= S''_lb = 635530452759/817216000000.
- (1/2, mu_C): G > 0 by Lemma A; dropped one-sidedly.
- Parameter box L in [4/25, 8649/40000], m in [112/113, 1] is exactly lambda in [2/5, 93/200], tau in [7/8, 1].
- The original beta route is rejected by the exact counterexample beta(1/8192) < 0 (rational interval); the Pi_t route replaces it.

## 3. Machine evidence (chat re-runs, python3 -I, isolated directories, SymPy 1.14.0, exact arithmetic only)
- Astra certificate39prime_exact.py: exit 0, `EXACT ALGEBRA CHECKS: PASS`; regenerated JSON (--write-certificate) is identical to the received JSON.
- chat independent check chk144.py (Pi_t rebuilt from the paper definitions, not from Astra's script):
  Pi_3 and Pi_14/5: degree (2,3,5), 72 coefficients each, full index set, exact Bernstein reconstruction identity, all coefficients > 0,
  minima 106592/1953125 and 40192/1953125 (match the JSON). Result: CHAT 144-COEFFICIENT CHECK: PASS.
- chat auxiliary check chkd.py: on the J box d >= 416/625 (all Bernstein coefficients >= 0) and 13/10 - d > 0 (min 96386071/8172160000);
  C0*(1/2) < 0; C_core = 10778024217619399/81721600000000000 > 1/8; S''_lb recomputed and equal.
- Code certificates (4): all exit 0, stderr empty, no FAIL; bernstein_south_A ALL CERTIFICATES PASS; kernel_extension 19 PASS, ALL CERTIFICATES PASS.
- Independence note: the 144 Pi_t coefficients on J were previously produced only by Astra (Code reproduced the original C1–C4 split);
  chk144.py is the first independent verification of those coefficients.

## 4. Output hashes (SHA-256)
| file | SHA-256 |
|---|---|
| chk144.py | e5973a6f5fd8bc16eb9ca7f1a2fe945f166341fede00b3f3f3fc6579f45f5c6a |
| chkd.py | fe1d5b529477e69ea908ebb8aba10aae09b5dbecbe47494d2cc2375d93f99442 |
| chk144.stdout.txt | e76341100a7514fbdeaa0ce7a5b2d491969b1f7a095dd5c0abb582aca2f3ad1c |
| chkd.stdout.txt | 628fcc5a885783de4a2914346943f3cdecaf6449cb42a14db556f17f81a3a985 |
| astra_39prime_rerun.stdout.txt | 5e584bff7a0126c33cbee1e8b717170e1cccf71e99cb2f14b8fc00695511cfb5 |
| code_bernstein_G_rerun.stdout.txt | 779fe1b1ba649f9459480694c0b33816848fe7e442c5e14a425b6bf24c517a55 |
| code_bernstein_south_A_rerun.stdout.txt | 2e8e74c60247c7c24d43a0b50da0a0ac5116c8dd5665933f310662e014447140 |
| code_theta_14_over_5_cert_rerun.stdout.txt | 74596dc161b80793292e7c2a70239dd953874260c8490bdb3f394a1759439504 |
| code_kernel_extension_cert_rerun.stdout.txt | a478d418774577d6798ea626d14bad763a8dcc789c34bb3dc1e8acd87876cf46 |

## 5. Historical wording kept verbatim
The 39′ files state "Remaining required budget: U_north+U_near < 104/625". This is the bookkeeping budget of 2026-10-08; inside the south
paper proof S''_lb replaces 104/625 (W-17). The pinned files are not edited.

## 6. Deviation logged
CHAT-39P-RECEIPT-001: chat stated on 2026-10-10 that the 39′ originals had not been received; they had been received on 2026-10-08 19:04 JST
with matching SHA-256. Corrected in this record.
