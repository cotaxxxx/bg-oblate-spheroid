# D-OB P2 / D-AN-1 — L1 RESTART STATUS BRIEF

2026-10-17 — Dig preparation for independent chat audit and Judge restart ruling

**Status: DIG PREPARATION / FOR CHAT AUDIT / NO JUDGE L1 RESTART RULING / NO COMPUTATION AUTHORIZED**

## 0. Purpose and role boundary

This note does not audit L1 and does not restart L1. It records the current L1 restart state from the pinned D-AN-1 sources after the Judge's conditional L3 FREEZE.

Preparation role: ChatGPT / Dig.
Independent audit role: chat.
Final restart ruling: Judge.

The six questions fixed for this handoff are:

1. Why L1 was paused.
2. What remained OPEN when it was paused.
3. What FT_q V3 and the L3 FREEZE have now resolved.
4. What inherited conditions remain.
5. What the first exact task should be if L1 is restarted.
6. Dig's non-binding recommendation for the independent auditor and Judge.

Nothing in this note changes a theorem statement, frozen target, dependency edge, proof method, partition, or certification status.

---

## 1. Frozen L1 target

The v1.2 D-AN-1 predeclare preserves the L1 target:

> prove the required positive lower sign for the paired-H representation on the interior compact layer `S_int subset S_AN`, with all hypotheses explicit and without importing diagnostic margins.

Its direct dependencies are L0, and the §2 interior regularity / kernel premises.

The v1.2 positioning note further fixes how the abstract compact layer is instantiated after L3 supplies a boundary-layer width:

\[
S_{\mathrm{L1}}
:=
\Sigma\cap\left\{\delta\in[\delta_0,15/64]\right\},
\qquad
\delta=1-r^2.
\]

This is a concrete instance of the byte-preserved L1 target, not a rewrite of that target.

The whole T1 assembly in v1.2 is

\[
L0+L1+L2+FT_q+QM+L3\longrightarrow T1.
\]

NP-T is retained as an independent cross-check; its edge into L3/T1 is optional in v1.2.

---

## 2. Why L1 was paused

L1 was not paused because an L1 positivity claim had been refuted.

The explicit staging reason was that L1's concrete compact remainder could not be fixed until L3 produced an explicit rational \(\delta_0>0\). The L3-MRA states that, after such a \(\delta_0\) is proved, L3 owns

\[
0\le\delta\le\delta_0
\]

and the paused L1 restarts on the single compact layer

\[
\Sigma\cap\{\delta\in[\delta_0,15/64]\}.
\]

At the pause point, the needed \(\delta_0\) was unavailable because the two quantitative L3 residues were not yet jointly available:

- FT_q: a uniform positive rational whole-face lower bound \(m_0>0\);
- QM: an explicit uniform modulus \(\omega_E\) strong enough to choose \(\delta_0\) with
  \[
  \omega_E(\delta_0)<m_0.
  \]

Thus the L1 pause was a dependency/staging hold: the exact compact target instance did not yet exist.

---

## 3. What was OPEN at the pause point

### 3.1 Direct L1 item

L1 itself remained unproved. No paper proof or accepted interval certificate for the compact positivity target had been completed.

### 3.2 Missing compact cutoff

The exact lower endpoint \(\delta_0\) of the compact L1 layer was unavailable. Therefore the domain on which L1 was to prove positivity was not yet instantiated.

### 3.3 Upstream L3 quantitative residues

FT_q and QM were the two quantitative residues exposed by the L3-MRA. In the historical FT_q route, the whole-face \(m_0\) was unavailable and the boundary-pair route remained open. Those historical sub-obligations are provenance for the pause, not current L1 sublemmas.

### 3.4 Route choice intentionally undecided

The frozen v1.2 text deliberately postpones the choice between:

- analytic paper closure of L1; and
- a separately predeclared G-numbered interval proof,

until after \(\delta_0\) is proved. Diagnostic values are forbidden from choosing this split.

The v1.2 text also says that existing G2 material is preserved. Current branch readback for this brief did not identify a canonical standalone **L1 G2** artifact, so this note does not infer or invent its content. Any later use of "G2 material" must identify its exact file / commit / SHA and scope before it is treated as an input.

### 3.5 Inherited analytic conditions

The P1 / Lemma V regularity and kernel premises remained inherited conditions rather than newly proved facts inside L1.

---

## 4. What FT_q V3 and the L3 FREEZE have resolved

### 4.1 Whole-face positive margin now exists

The accepted V3 μ16 / P-only certificate supplies the display lower bound

\[
M=\frac{295346256371}{10^{12}}>0
\]

for the required whole-face quantity, subject to the inherited normalization / extension pins recorded in the FT_q and L3 handoff.

Thus the old state "whole-face \(m_0\) unavailable" is no longer the reason to hold L1.

### 4.2 QM modulus is available in the frozen chain

The QM source gives the explicit modulus

\[
\omega_E(d)
=
50C_2d+25C_3d\{1+2\log(1/d)\},
\qquad 0<d\le1/2,
\]

with

\[
C_2=9\pi+8,\qquad C_3=8788+39\pi,
\]

and states the stronger scope on all of \(\overline K_\lambda\) for fixed \(\lambda\). This is the scope needed to include the swept interior segments used in the H-transfer.

This brief records the source statement; it does not independently re-audit QM.

### 4.3 L3 now supplies an explicit exact cutoff

The conditionally frozen L3 V0.2 fixes

\[
\boxed{\delta_0=\frac3{100000000}}.
\]

It also gives, under its inherited conditions,

\[
H(p)>
\frac{273790294597}{7000000000000}>0
\]

throughout the closed boundary layer

\[
0\le\delta\le\delta_0.
\]

Therefore the compact L1 target is now exact:

\[
\boxed{
S_{\mathrm{L1}}
=
\Sigma\cap
\left\{
\frac3{10^8}\le\delta\le\frac{15}{64}
\right\}.
}
\]

Using \(\delta=1-r^2\), the same domain can be recorded without introducing an irrational endpoint as

\[
\lambda\in[2/5,93/200],\qquad
\tau\in[7/8,1],
\]

\[
\frac{49}{64}\le r^2\le 1-\frac3{10^8}.
\]

The shared endpoint \(\delta=\delta_0\) may be covered by both L3 and L1; there is no gap.

### 4.4 The direct reason for the L1 pause is resolved

The particular prerequisite stated by the L3-MRA for restarting L1 — existence of a proved explicit \(\delta_0\) — is now satisfied under the Judge's conditional L3 FREEZE.

This does **not** prove L1.

---

## 5. Remaining inherited conditions and non-closures

These must remain visible if L1 is restarted.

### 5.1 Direct L1 dependencies

- L0 rational coverage / the fixed analytic sector \(S_{\rm AN}\).
- P1 interior compact regularity and the pinned kernel identities.
- Lemma V / Lemma 6.1 assumptions used to identify and control H.
- The rule that no diagnostic margin may be imported into the L1 proof.

L0 provides the exact coverage identity

\[
\rho^2+\frac{z^2}{\lambda^2}=r^2
\]

and the fixed sector containment, but L0 itself proves no sign of H.

### 5.2 Conditions inherited through the current FT_q/L3 freeze

The L3 FREEZE record keeps visible:

- P1 normalization;
- paired density / \(H=E_{yy}\) integral identification;
- boundary extension through Lemma V / Lemma 6.1;
- the fixed QM modulus scope, including interior swept segments;
- endpoint NP-T connection as an inherited cross-check/pin.

NP-T is not a direct L1 dependency and is not a required v1.2 DAG edge into L3, but its current inherited cross-check status should not be silently erased.

### 5.3 Provenance/reproducibility items still outstanding

Two record-completion items remain outside the mathematical L1 target:

1. the L3 V0.2 auxiliary check files (`l3_v02_checks.py`, `l3_v02_checks_result.json`, `source_ledger.json`) have not yet been pushed with the body;
2. the final JSON/script/SHA artifacts from the external chat 4096-branch FT_q V3 recomputation have not yet been pushed.

Per the Judge's current handling, these are provenance/reproducibility completions and are not, by themselves, a mathematical refutation of the L3 conclusion. This note does not mark them completed.

### 5.4 No downstream certification consequence yet

Even if L1 is restarted:

- T1 is not yet CLOSED;
- D-P2 remains NOT_CERTIFIED;
- no numerical unresolved boxes are removed by this note;
- D5 is unchanged.

---

## 6. First exact task if Judge restarts L1

The first task should be a **paper-only compact-instance preparation**, not an interval run.

### L1-R0 — exact compact instance and denominator-safe interior ledger

1. **Freeze the concrete L1 domain exactly**
   \[
   S_{\mathrm{L1}}
   =
   \Sigma\cap
   \left\{
   \frac3{10^8}\le1-r^2\le\frac{15}{64}
   \right\}.
   \]

2. **Rewrite the paired-H representation on this exact domain**, preserving the existing L1 target and all inherited kernel identities.

3. **Derive exact compact separation / denominator-safe bounds** required by the intended analytic inequalities. In particular, any positive lower bound on a geometric denominator such as \(D\), or any equivalent safe quantity, must be derived from the frozen compact domain and source identities; no observed numerical value may be inserted.

4. **Produce a finite sign-inequality ledger** identifying which terms are controlled analytically and what exact residue, if any, remains before \(H>0\) follows on all of \(S_{\mathrm{L1}}\).

5. **Stop before interval computation.** If the paper inequalities close, continue as a paper proof. If an interval certificate is actually required, prepare a separate G-numbered predeclare containing the domain, exact inputs, algorithm, bounds, source pins, failure conditions, and checker contract, and submit that predeclare for independent chat audit / Judge authorization before any run.

No result-driven subdivision, diagnostic threshold, or worst-box tuning is authorized by this restart brief.

---

## 7. Dig recommendation — non-binding

\[
\boxed{\text{RESTART\_CANDIDATE}}
\]

Dig recommends that the Judge permit **L1 paper-proof preparation to restart**, beginning with L1-R0 in §6, while withholding authorization for any interval/certification computation.

Reason:

- the recorded pause was caused by the absence of the exact L3 cutoff;
- the conditional L3 FREEZE now supplies
  \[
  \delta_0=3/10^8;
  \]
- the exact compact target is therefore fixed;
- no source read in preparing this brief records an L1 mathematical failure.

This is a preparation recommendation, not an audit verdict. The independent chat audit may recommend RESTART, HOLD, or REDESIGN after checking the pins, dependency interpretation, and current branch state.

A pin mismatch, a contradiction in the frozen DAG, or failure of an inherited premise must remain fail-closed.

---

## 8. Current state pending independent audit and Judge ruling

\[
\mathrm{FT}_q:
\mathrm{DISCHARGED}
\quad\text{(specified inherited conditions)}
\]

\[
L3:
\mathrm{FREEZE}
\quad\text{(inherited conditions)}
\]

\[
\boxed{L1:\mathrm{PAUSED}}
\]

\[
D\!-\!P2:\mathrm{NOT\_CERTIFIED}.
\]

This document does not change `L1: PAUSED`.

---

## 9. Source / provenance ledger used for this Dig preparation

Repository: `cotaxxxx/bg-oblate-spheroid`
Branch readback base before this note: `design/d-ob-p2` at `1b65c7cf45a4c32f47cf718b582ca1b7527533c4`.

- D-AN-1 predeclare v1.2:
  - path: `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`
  - frozen parent pin used downstream: commit `e9c8b1caa3ad502a3d01dafe354b61108787eed2`
  - SHA-256 `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217`
- L3-MRA:
  - path: `analysis/D_OB_P2_D_AN1_L3_MRA_DRAFT.md`
  - commit `5fc0341216f4e0f6722a96f3d8edb2e1c9fbc47c`
  - SHA-256 `b13e07d63b3f3035b7b983cc39acbae893d4a184dfa030eaf73bb9f243a0d842`
- L0:
  - path: `analysis/D_OB_P2_D_AN1_L0_DRAFT.md`
  - commit `3cabe008b95ed7f81597a45f74303a5b7c53907f`
  - SHA-256 `41b6be56e6e81f6b0f90e155865f9fc9fcd75129215cfd5df8be6845755c639e`
- QM:
  - path: `analysis/D_OB_P2_D_AN1_QM_DRAFT.md`
  - commit `7f9119f7cbe7d5dab95e42300bb9563c974e23f5`
  - SHA-256 `e8588c1b677e10aceac22e79784e41111cffe2c2cffce1636804485dafb09edc`
- L3 V0.2 body:
  - path: `analysis/D_OB_P2_D_AN1_L3_BODY_DRAFT_V0_2.md`
  - SHA-256 `d4d2591e0a800202e50224eb9caa697a35054db6971885bc727d87aad5766997`
- L3 V0.2 independent audit + Judge conditional FREEZE record:
  - path: `analysis/CHAT_AUDIT_D_AN1_L3_BODY_V0_2_AND_JUDGE_FREEZE_2026-10-17.md`
  - SHA-256 `37419196a0c6f5ccb2d0e02a7b30da7e6e0b03608e58f7440ad7d3030db68d42`
- V3 exact production report:
  - SHA-256 `6b9e51e5a13d7dcef09fa04c96b0510bd22e552fa477903e32bd5058cb282d6d`
- canonical exact m0 file:
  - SHA-256 `207b9617d61645e2c89f125debac2e40576f11f790feb09f81471564a1fd7d17`

Evidence boundary: this Dig note is a source readback and restart-status preparation. It is intentionally not an independent audit.
