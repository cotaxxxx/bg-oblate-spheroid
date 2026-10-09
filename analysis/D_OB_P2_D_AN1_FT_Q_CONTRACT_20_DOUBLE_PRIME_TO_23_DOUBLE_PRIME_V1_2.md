# D-OB P2 / D-AN-1 FT_q: Judge contract 20''--23'', v1.2 (22'' amended)

Status: CONTRACT v1.2 / 22'' AMENDED / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / D-P2 NOT_CERTIFIED
Supersedes: v1.1 commit b1a10ea6f0ef127aaf4a40a93070cf270d03e073, blob 49e658b0487123249eb81d70bde1ef188ff640d7,
SHA-256 db975daba9d712246ed5e27465437f34450b356f453729a5fb78ec8ceab468cb (file analysis/D_OB_P2_D_AN1_FT_Q_CONTRACT_20_DOUBLE_PRIME_TO_23_DOUBLE_PRIME_V1_1.md).
Parent fixed contract: 00138df257cee8e5480b412157dce36ae90743d0.
Scope of this version: ONLY the 22'' certification condition is amended (section 22'' below and the amendment record).  Sections 20'', 21'', 23''
and "Corrections and next work unit" are reproduced VERBATIM from v1.1 and are not changed in mathematical content.
Units: S_K, C_out, U, S''_lb, U_north, U_near are in double-integral P units, not H units; 2 pi lambda H = integral_{-1}^{1} G(mu) dmu with G as in 21''.
Adoption: CHAT recommendation and Judge adoption on 2026-10-09 (design value S''_lb adopted as the 22'' budget).  Drafted by Code for CHAT AUDIT;
not a canonical commit until Judge approval.

## 20'' CLOSED -- strengthened
On K=[-1,-1/4], S_K >= S_K,lb := 207/5000.
The previous 27/2500 bound remains in history and is superseded for residual comparisons.
Proof uses exact Bernstein interval certificates, a global adverse secant bound,
and pi>3. Improvement factor over original lower bound: 23/6.

## 21'' OPEN -- one-sided exterior residual
I(mu,phi)=-lambda^2*(m-mu)*F*W;
G(mu)=integral_0^pi I(mu,phi) dphi;
C_out=integral_{-1/4}^1 G(mu) dmu.
Prove C_out >= -U with a uniform explicit rational U.
Allowed partition: exterior south (-1/4,mu_C), north far,
near band |mu-m|<=rho including cap. Exterior south has
s=m-mu>221/565, D_+ , D_- >442/2825.
Allowed: U_minus=integral_{-1/4}^1 [-G(mu)]_+ dmu, with U>=U_minus.
Do not impose the obsolete two-sided |C_out|<=U contract.
Positive exterior-south contributions may be retained.

## 22'' AMENDED (v1.2) -- certification condition
Regions (s = m - mu as in 21'', m in [112/113, 1], rho^2 = 1 - m^2):
  South:       mu in [-1, 1/2].
  North far:   s in [rho, 1/2], i.e. mu in [m - 1/2, m - rho]   (Contract 45, three pieces).
  North near:  |mu - m| <= rho and mu <= 1, i.e. mu in [m - rho, 1]   (Contract 24 baseline band kappa = 1; Contract 43).
Coverage and overlap: m - 1/2 in [111/226, 1/2], hence [-1, 1/2] U [m - 1/2, m - rho] U [m - rho, 1] = [-1, 1] and no part of [-1, 1] is uncovered.
South and north far overlap on [m - 1/2, 1/2], of width 1 - m <= 1/113.  The overlap is harmless (safe-side slack): with
U_north >= integral_{m-1/2}^{m-rho} [-G]_+ dmu and U_near >= integral_{m-rho}^{1} [-G]_+ dmu, and since [1/2, 1] is contained in [m - 1/2, 1],
  integral_{-1}^{1} G(mu) dmu  >=  integral_{-1}^{1/2} G(mu) dmu  -  integral_{1/2}^{1} [-G(mu)]_+ dmu  >=  S''_lb - U_north - U_near.
Counting the negative part of G on the overlap inside U_north only lowers the right-hand side; the direction of the inequality is preserved.
Positive exterior-south mass in (-1/4, 1/2] is retained inside S''_lb, as allowed by 21''.
South lower bound: integral_{-1}^{1/2} G(mu) dmu >= S''_lb := 635530452759/817216000000.
  Derivation source (paper proof, CHAT AUDIT PASS, canonical import NOT DONE):
    tools/d_ob_p2/ftq_paper_proof/D_OB_P2_D_AN1_FT_Q_SOUTH_POSITIVE_MASS_DRAFT.md in cotaxxxx/basepoint-geometry,
    commit 05668a47216e243450211f0cf438702dc6d1527c, blob a66ac60edfc75e70ae198bdea7807e6d5c14b360,
    SHA-256 f320acb964cb278d1dd8ef6240fcc88bc9bdf77ae75edd4c77f86ce78da93d3c.
  Input certificate (one input to that derivation, CHAT AUDIT PASS; a distinct piece of evidence, not the derivation itself):
    tools/d_ob_p2/ftq_cert/kernel_extension_cert.py, commit 1ac44469f33fb74b1b4cbfcd62621dce3f6fa12e,
    blob 3600e0771c73456698035484eb267415111acc4d, SHA-256 3c4b0d452d87072c2c7a27d432048691c4cce47da871bfad0a50630436146e85.
Certification condition (replaces the v1.1 condition "U < 207/5000"):
  Require  U_north + U_near < S''_lb,  with uniform explicit rational U_north, U_near certified by exact rational / Bernstein certificates.
  Then  H >= (S''_lb - U_north - U_near)/(2 pi lambda) > 0.
Only after a proof of that inequality may a uniform rational c_FT > 0 be declared, by bounding pi and lambda rationally; then
m0 = min(c_FT, 13/2000).  No value is currently assigned to c_FT or m0.
Superseded budget: the v1.1 22'' condition U < 207/5000 (U bounding the exterior residual of 21'' on (-1/4, 1]).  The figure
104/625 = 207/5000 + 1/8, used in later working documents as a combined informal budget (S_K,lb plus a core contribution C_core >= 1/8),
does not appear in v1.1 and is likewise superseded; it is recorded here only so that no document continues to cite it as the budget.
Recorded fact: the certified north-far bound alone (U_north < 5481/10000, Contract 45 pieces 1-3) exceeds both 207/5000 and 104/625;
the v1.1 budget was therefore unattainable by the certified north route, which is the reason for this amendment.

## Reference values (not part of the certification clause)
Certified (CHAT AUDIT PASS) north-far bound: U_north < 5481/10000 (exact sum of pieces 1-3: 99c9b62a..., 7ba339a8..., 9cb723c0...).
Astra L43 near-band bound (independent report; exact script CHAT AUDIT PASS; H-43-1(ii) CLOSED; Code certificate NOT EXECUTED; Contract 43
NOT FROZEN): U_near <= 3887073979116207/17284813033600000 < 9/40.
Residual after the far band: S''_lb - 5481/10000 = 187614363159/817216000000; margin over 9/40: 3740763159/817216000000 > 0.
These values do not certify 22''; certification requires the frozen Contract 43 certificate run and CHAT AUDIT.

## 23'' FIXED -- evidence and diagnostic separation
Numerical diagnostics are not proof constants. The reported north signed
contribution -0.005 to -0.0065 is retained only as a target-precision warning.
The new 0.0414 threshold improves margin but does not prove U.
All prior prohibitions on sampling/probe-derived certification remain.

## Corrections and next work unit
The old exterior-south claim s>1/2 was false; the adopted bound is
s>221/565, implying D_+ , D_- >442/2825.
For |mu-m|<=rho, cap m<mu<=1 is all near; far-cap is EMPTY and removed.
Next: prove an explicit exterior-south lower bound for G(mu) integrated over
(-1/4,mu_C), retaining positive mass. Rebuild the square-completion
argument with E of indeterminate sign; the old |Z| bound used E<0 on K
and cannot be imported without reproof. If B<0 then A/S3<=E, but
E itself need not be negative throughout the exterior-south region.
Then bound north far and near contributions to obtain U<207/5000.

## v1.2 amendment record
Changed: section 22'' (condition, regions, coverage/overlap statement, south evidence rows, superseded-budget note); header Status/Units/Adoption;
Reference values section (new); Ledger (status words only).  Unchanged (verbatim): 20'', 21'', 23'', "Corrections and next work unit".
Adopted: CHAT recommendation and Judge adoption, 2026-10-09 ("案A").  Drafted by Code; CHAT AUDIT and Judge approval precede any canonical commit.
Lapsed text (R-V1): the sections reproduced verbatim above (in particular 21'' "Prove C_out >= -U with a uniform explicit rational U" and the
"Corrections and next work unit" line "Then bound north far and near contributions to obtain U<207/5000") still carry the v1.1 instruction
U < 207/5000.  That instruction is LAPSED in v1.2: the operative certification condition is the amended 22'' (U_north + U_near < S''_lb).
The verbatim text is preserved for the record and for the unchanged mathematical content of 20'', 21'', 23''; it is not to be read as a budget.
Ledger correction recorded by CHAT (deviation CHAT-22-V11-BUDGET-001): the v1.1 written budget was U < 207/5000, not 104/625.
Evidence state at drafting (R-V2): Astra exact script `l43_graph_majorant_exact.py` (SHA-256 6187c2b0...) CHAT AUDIT PASS for script/report
consistency; H-43-1(ii) CLOSED by CHAT ruling on Astra's independent lemma (H43_ENDPOINT_LEMMA.md, SHA-256 b1a906ed...); Code certificate
`tools/d_ob_p2/ftq_cert/north_near_l43_cert.py` (commit 213ec4bb...) NOT EXECUTED; Contract 43 NOT FROZEN (FREEZE 3/4: condition 4 = pin of this document).

## Ledger
20'' CLOSED (upgraded); 21'' OPEN; 22'' AMENDED (v1.2: U_north + U_near < S''_lb; OPEN until certified); 23'' FIXED.
U_north CERTIFIED < 5481/10000; U_near OPEN (Contract 43 FREEZE pending); c_FT UNSET; Boundary Pair Lemma OPEN; m0 UNAVAILABLE;
L3 BLOCKED; L1 PAUSED; D-P2 NOT_CERTIFIED.
