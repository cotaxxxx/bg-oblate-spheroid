# D-OB P2 / D-AN-1 — QM proof and swept-segment scope audit record

2026-10-18 JST

**Record type:** Judge-relayed independent chat paper-audit report / provenance record.
**Recorded by:** ChatGPT / Dig.
**Independent auditor:** external chat, as identified in the report supplied by Judge. This file records that report; Dig has not conducted an additional independent QM proof audit.
**Evidence class:** source readback + reported independent paper derivation / no interval or numerical sampling.
**Reported audit verdict:** **PASS (conditional on P1 inherited-premise bundle and QM-1)**.
**Swept-segment applicability:** **DISCHARGED** as reported in the Judge-provided audit.
**No unconditional QM discharge or L3/T1 closure is declared by this record.**

## 1. Pinned sources and source-readback

- QM source: analysis/D_OB_P2_D_AN1_QM_DRAFT.md; SHA-256 e8588c1b677e10aceac22e79784e41111cffe2c2cffce1636804485dafb09edc.
- Frozen parent: analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md, commit e9c8b1caa3ad502a3d01dafe354b61108787eed2; SHA-256 f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217.
- P1: analysis/D_OB_P1_DESIGN_NOTE.md, commit 6c6282a8acbf467bcbe6a7e32236e1d32a91f400; SHA-256 2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9.
- QM-1: analysis/D_OB_P2_D_AN1_QM1_DRAFT.md, commit 930b44bb6ce2ab9d7298556e8f5ff1768386857c; SHA-256 dd001338000ed8cf98ec13ce8b15fe4badd833f08826becfd8fc777d39848186.

These source pins were provided by Judge and matched the source readback. Source-byte agreement does not itself re-prove the inherited lemmas. Historical operational status lines inside earlier drafts are not Judge's current project status.

## 2. Stronger domain statement and swept-point inclusion

QM §1 states that its modulus applies to the full convex body closure(K_lambda), for each frozen lambda. QM §10 states that the modulus inequality holds for every pair p,p' in closure(K_lambda), and §12 records uniformity for lambda in [2/5,93/200].

For the meridional swept point p_v=(v rho,0,z), |v|<=1,

\[
|L_\lambda^{-1}p_v|^2
=v^2\rho^2+z^2/\lambda^2
\le \rho^2+z^2/\lambda^2=r^2\le1.
\]

Thus p_v belongs to closure(K_lambda). For the segment between p and a boundary point q used by L3, convexity of closure(K_lambda) places every point on that segment inside the same closure; QM §4 invokes the identical convexity premise. The domain/swept-segment applicability obligation is thereby closed as a geometry and source-scope issue, conditional on validity of the QM analytic proof.

## 3. Exact paper audit findings as reported by external chat

Fix C2=9 pi+8 and C3=8788+39 pi. The stated modulus is

\[
\omega_E(0)=0,\quad
\omega_E(d)=50C_2d+25C_3d[1+2\log(1/d)]
\quad (0<d\le1/2),
\]
and omega_E(d)=omega_E(1/2) for d>=1/2.

The independent chat report supplied by Judge states PASS on the following derivations:

| QM source | Reported exact check |
|---|---|
| §2 | dA/w=dmu dphi, consistent with E=(4 pi lambda)^(-1) integral F dphi dmu; 1/lambda<=5/2, 1/w<=5/2 |
| (2.3)–(2.4) | Surface area within B(p,s) <=4 pi s^2; layer-cake integral_A D^(-1) dA <=2 sqrt(4 pi M) |
| §3 | Global absolute E_rhorho bound (25/2) C2, hence difference <=25 C2 |
| §5 | Near-area <=4 pi eta^2 gives each D^(-1) integral <=8 pi eta; sum <=25 C2 eta=50 C2 d |
| §6 | Far D^(-2) layer-cake identity gives pi+8 pi log(2/eta), then the stated coarser 4 pi+8 pi log(2/eta) |
| §7 | Along p_t=(1-t)p+tp', D(x,p_t)>=D_p-d>=D_p/2, so directional MVT gives <=4 C3 d/D_p^2; far term <=25 C3 d[1+2 log(1/d)] |
| §9 | omega'_E(d)=50 C2+25 C3[2 log(1/d)-1]>0 for 0<d<=1/2; continuity at 0 |
| §10 | omega_E(1/2)>25 C2 controls d>=1/2 |
| §11 | FTC representation for H and nondecreasing omega_E transfer the same modulus to H |
| §12 | Constants C2, C3, 4 pi and diameter bound 2 do not depend on lambda |

These are recorded as the external chat's independently checked findings communicated by Judge; no standalone audit code or original external-chat transcript was provided for separate byte verification with this record.

## 4. Two audit notes

**N1 — fixed rho direction.** On the relevant meridional plane y=0, interpret E_rhorho as a fixed Cartesian x-direction second derivative for the mean-value argument along p_t. The rho direction must not rotate along this segment without an additional derivation. A one-line clarification in the QM explanatory text is recommended, but the pinned QM source is not edited here.

**N2 — QM-1 audit provenance.** The QM header labels QM-1 CHAT AUDIT PASS. However the QM-1 source header reads PAPER-PROOF DRAFT / AWAITING CHAT AUDIT / NOT A THEOREM, and a standalone QM-1 audit record was not located on the compared design branch. Locate the earlier audit with exact path/commit/SHA; if unavailable, commission an independent QM-1 paper audit of the claimed C3 third-directional-derivative bound. Do not silently upgrade the QM-1 header or claim the missing artifact exists.

## 5. Inherited-premise dependency and discharge gate

The QM proof conditionally inherits:
- P1 Lemma 3.4: |F_rhorho|<=C2/D, including the boundary-base-point scope and extension.
- P1 Lemmas 4.1 and 4.2: surface-area and potential-area estimates.
- P1 Lemma 6.1 / Lemma V: axis/boundary extension and H=integral_0^1 E_rhorho(t rho,z) dt.
- QM-1: |F_uvs|<=C3/D^2 away from x=p, with arbitrary unit base-point directions, and its independent-audit provenance.
- P1 normalization and paired-density interpretation where inherited downstream.

The intended order is common P1/Lemma V bundle audit -> QM-1 provenance/audit -> final QM condition discharge -> L3/T1 unconditional assembly review. This record does not make any of those downstream Judge rulings.

NP-T remains a nonblocking cross-check pin; FT_q and L3 retain their previously ruled conditional statuses.

## 6. Governance and current state

**Report classification:** EXTERNAL CHAT AUDIT PASS, CONDITIONAL; Dig provenance-recording only.
**QM scope/swept applicability:** DISCHARGED (reported).
**QM proof:** PASS subject to inherited P1/Lemma V bundle and QM-1.
**P1 bundle:** OPEN.
**L1:** DUAL-TRACK PAPER COMPARISON, report due 2026-10-24; L1-R0 PARTIAL.
**T1:** NOT CLOSED.
**D-P2:** NOT_CERTIFIED.
**No interval/certification computation, new numeric diagnostics, Git changes to source notes, or D5 access is authorized by the mathematical content of this record.**
