# D-OB P2 — D-AN-1 L3 Minimum Requirement Analysis (L3-MRA) — DRAFT

**Status:** PAPER-PROOF DRAFT / NOT A THEOREM / AWAITING CHAT AUDIT
**Parent freeze:** v1.1, commit `6de8a178b3f9c278952ac68590f97f3f100ed9f9`
**Evidence:** ANALYTIC PREMISE ANALYSIS / NO DIAGNOSTIC EVIDENCE

## 1. Frozen target and purpose

Frozen L3 has six stages: boundary-layer bounds; D/h comparison; gamma derivative bounds; uniform L1 majorant; justified limit/interchange; strict positivity on the closed corner. This MRA changes none of them. It enumerates the minimum sign and quantitative continuity facts needed by stage 6.

## 2. Required boundary face

For lambda in [2/5,93/200] and tau in [7/8,1], define

rho_b=(1-tau^2)/(1+tau^2),  z_b=lambda*2tau/(1+tau^2).

This is exactly the r=1 face of Sigma. Its endpoints are (0,lambda) at tau=1 and (15/113,112lambda/113) at tau=7/8.

## 3. Existing supply

R1: Lemma V(c) and Lemma 6.1 give qualitative continuity of E_rhorho and H on closure(K).
R2: audited L2 gives the paired representation and H(0,z)=E_rhorho(0,z).
S1: audited NP-T gives H(0,lambda)>0, i.e. the tau=1 endpoint.
No existing node gives a quantitative uniform lower bound on the whole required face, and no existing node gives an explicit uniform continuity modulus sufficient to construct a boundary-layer width.

## 4. Residue FT_q — quantitative boundary-face positivity

A new internal node must prove an explicit rational constant m0>0, uniform in lambda and tau, such that

H(rho_b,z_b;lambda) >= m0

for all lambda in [2/5,93/200], tau in [7/8,1].

FT_q claims no sign outside this face. It contains the NP-T endpoint tau=1 and is stronger there, but it does not modify the NP-T statement.

## 5. Residue QM — quantitative modulus

A second internal node must provide an explicit modulus omega_E:[0,infinity)->[0,infinity) for E_rhorho on a closed region containing every segment point required below. The modulus must satisfy omega_E(0)=0, omega_E(d)->0 as d->0+, and be nondecreasing.

For all relevant p,p' in that region,

|E_rhorho(p)-E_rhorho(p')| <= omega_E(|p-p'|).

No exponent or asymptotic form for omega_E is frozen by this MRA.

By Lemma 6.1(iii),

H(rho,z)=integral_0^1 E_rhorho(t rho,z) dt.

Hence for p=(rho,z), p'=(rho',z'),

|(t rho,z)-(t rho',z')| <= |p-p'|

for 0<=t<=1, so the same modulus gives

|H(p)-H(p')| <= omega_E(|p-p'|).

Thus QM may be proved as a quantitative version of Lemma V(c) for beta=(2,0,0); no K_H-specific modulus is required. Its domain must include the full swept segments {(t rho,z):0<=t<=1}, not merely the boundary layer.

## 6. Exact inward correspondence and delta0

For a Sigma point with delta=1-r^2, use the same (tau,lambda) and define

p_boundary=p_b(tau,lambda),  p_in=r*p_boundary,  r=sqrt(1-delta).

This correspondence exactly covers Sigma. Since |p_boundary|<=1,

|p_in-p_boundary|=(1-r)|p_boundary| <= 1-r = delta/(1+r) <= delta.

Therefore

H(p_in) >= m0-omega_E(delta).

L3 must produce an explicit rational delta0>0 satisfying

omega_E(delta0) < m0.

Because omega_E is nondecreasing, every 0<=delta<=delta0 then satisfies H(p_in)>0. Equivalently, a proof using sup_{d<=delta0} omega_E(d)<m0 is admissible.

The constant delta0 must be derived solely from proved FT_q and QM constants. Diagnostic values may not select it.

## 7. Consequence for L1

After such a delta0 is proved, L3 owns 0<=delta<=delta0 and paused L1 restarts on the single compact layer

Sigma intersect {delta in [delta0,15/64]}.

No numerical size for delta0 is anticipated in this MRA. Its effect on L1 can be judged only after FT_q and QM are proved.

## 8. NP-T dependency-edge Judge item for v1.2

The v1.1 edge NP-T -> L3 remains mandatory until a version-up is audited and frozen.

Because FT_q contains tau=1 with the stronger H(0,lambda)>=m0, v1.2 must explicitly choose one of:

A. make NP-T -> L3 optional and retain NP-T as an independent analytic cross-check; or
B. retain NP-T -> L3 as mandatory and state why the redundant dependency is required.

NP-T's theorem statement is unchanged in either choice. This MRA makes no silent DAG change.

## 9. Verdict and governance

Minimum newly exposed residues are FT_q and QM. Qualitative FT alone is insufficient for the constructive delta0 architecture.

Accordingly L3 body work must not assume either residue. After this MRA passes chat audit, v1.2 must add FT_q and QM as internal proof obligations, resolve the NP-T dependency-edge Judge item, and undergo renewed audit/FREEZE before proof work on the new nodes.

No interval computation is authorized here. If FT_q or QM later requires interval certification, the frozen section 5 rule requires a separate G-numbered predeclare and pre-ignition countersign.

**Operational status:** L1 PAUSED / L3-MRA DRAFT / FT_q+QM RESIDUES IDENTIFIED / L3 BODY NOT STARTED / NO DIAGNOSTIC EVIDENCE / D-P2 NOT_CERTIFIED.
