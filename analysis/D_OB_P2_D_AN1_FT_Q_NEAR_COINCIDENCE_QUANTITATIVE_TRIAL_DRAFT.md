# D-OB P2 — D-AN-1 FT_q Near-Coincidence Quantitative Trial — DRAFT

**Status:** ANALYTIC TRIAL / AWAITING CHAT AUDIT / LOCAL CANCELLATION PROVED / CONTRACT-21 PAIR-SCALE BOUND STILL OPEN
**Parent:** north-atom trial commit `83a928096904b17eb2d7085c73aa285d3c534fa7`, SHA-256 `195e9128cbda9ac0cf7e4be025f81d68338f1f6759bc994598804e7a3d89ba20`.
**Governance:** Judge B-prime / GLOBAL SPLIT CONTRACT 20-23. Probe outputs are NOT_EVIDENCE and no probe number is used here.

## 1. Exact local geometry
On the boundary face set `s:=m-mu`. For the plus member of the b-pair,
`D_+^2=a^2+rho^2-2rho b+lambda^2 s^2`. (1.1)
The coincidence point is `s=0`, `b=rho`; the minus coincidence is `s=0`, `b=-rho`.
Because the vertical coordinate difference is `lambda s` and the horizontal first-coordinate difference is `b-rho`,
`|s| <= D_+/lambda`, `|b-rho|<=D_+`. (1.2)
Similarly `|s|<=D_-/lambda`, `|b+rho|<=D_-`. (1.3)
On the frozen lambda interval, `1/lambda<=5/2`.

## 2. Exact numerator cancellation at each coincidence
Write `q=b^2`, `E=mq+C0`. The audited numerator factors are
`N_+=-lambda^2 s Q_+`, `Q_+:=rho E+B1 b`,
`N_-=-lambda^2 s Q_-`, `Q_-:=rho E-B1 b`. (2.1)
At `mu=m`, exact endpoint algebra gives
`B1(m)=-2m rho^2`, `C0(m)=m rho^2`. (2.2)
Hence at the plus coincidence `b=rho`,
`E=2m rho^2`, `Q_+=rho(2m rho^2)+(-2m rho^2)rho=0`. (2.3)
At the minus coincidence `b=-rho`,
`E=2m rho^2`, `Q_-=rho(2m rho^2)-(-2m rho^2)(-rho)=0`. (2.4)
Thus each unpaired numerator has the product of the exact latitude factor s and an additional factor vanishing at its own coincidence.

## 3. A uniform first-order bound for Q_+ and Q_-
Differentiate the exact polynomial `Q_+=rho(mb^2+C0)+B1 b` with respect to `(mu,b)`.
Using only `|mu|<=1`, `|b|<=1`, `0<m<=1`, `0<rho<=1`, `lambda^2<1`, direct coefficientwise bounds give
`|partial_mu Q_+|<=20`, `|partial_b Q_+|<=10`. (3.1)
The same bounds hold for Q_- after `b -> -b` symmetry. (3.2)

By the mean-value estimate from the corresponding coincidence and (1.2)-(1.3),
`|Q_+| <= 20|mu-m|+10|b-rho| <= 60 D_+`, (3.3)
`|Q_-| <= 20|mu-m|+10|b+rho| <= 60 D_-`. (3.4)
No numerical enclosure or sampled estimate enters these constants.

## 4. Consequent quantitative removability bound
From (2.1), (1.2), and (3.3),
`|N_+| <= lambda^2 |s| 60D_+ <= 60 lambda D_+^2`. (4.1)
Likewise
`|N_-| <= 60 lambda D_-^2`. (4.2)
Since `1<=R<=pi/2`, each original paired summand satisfies
`|R_+ N_+/(wD_+^3)| <= 30 pi lambda/(wD_+)`,
`|R_- N_-/(wD_-^3)| <= 30 pi lambda/(wD_-)`. (4.3)
This is an explicit `1/D` singularity and is integrable by the P1 Section 5 / Corollary 4.3 mechanism. It gives a quantitative local removability statement without using the degenerate denominator in the DeltaR secant formula.

## 5. Exact double cancellation in the symmetric brackets
At `mu=m`, `b^2=rho^2`, one has
`E=2m rho^2`, `B1=-2m rho^2`. (5.1)
At coincidence `D_+=0`, `D_-=2rho`, so
`S3=8rho^3`, `L_D=2rho`. (5.2)
Therefore the Rbar bracket cancels exactly:
`E S3+4B1 b^2 L_D=16m rho^5-16m rho^5=0`. (5.3)
The correction bracket also cancels exactly:
`4rho^2 E L_D+B1 S3=16m rho^5-16m rho^5=0`. (5.4)
Thus the symmetric P/rho representation has more cancellation at coincidence than is visible from the factor `(m-mu)` alone.

## 6. Why this does not yet close Contract 21
Bounds (4.3) control the original pair before division by the outer rho in H. If they are simply summed and then divided by rho, they produce a `1/rho` loss. Therefore (4.3) proves integrability/removability but is insufficient for the required uniform north/cap upper bound.

Contract 21 requires retaining the b-pair cancellation before absolute values, i.e. proving an estimate directly for
`P/(rho w v^3)`, (6.1)
or an integrated equivalent, in which the exact cancellations (5.3)-(5.4) supply the missing rho-scale gain.

Termwise absolute values of `T_EE,T_OO,T_RE,T_RO` before combining the cancelling brackets are therefore forbidden for the near-coincidence estimate: they destroy (5.3)-(5.4).

## 7. Remaining exact target
A sufficient next local statement would be an explicit integrable majorant of the form
`|P/(rho w v^3)| <= C_* [1/(wD_+)+1/(wD_-)]` (7.1)
with `C_*` independent of `rho`, `lambda`, and the boundary parameter, proved from the combined brackets rather than from separate terms.
An integrated variant with the same uniformity is equally admissible.

This draft does NOT prove (7.1). The obstacle is now sharply localized: one must quantify the first-order variation of the combined cancellations (5.3)-(5.4) without dividing by the degenerating secant denominator.

## 8. Probe provenance ledger — route selection only
`ftq_north_probe_DIAGNOSTIC.py`: SHA-256 `fa8d3917b48c2459a46e3b0cdb8c7a84771cdea24f5835568089f71f74aaad6e`.
`ftq_face_H_xcheck_DIAGNOSTIC.py`: SHA-256 `8b89a0a4431bb3a4952f3e381b2052f74943ee53526c9d73bb7451a977cf706b`.
These hashes record provenance only. No output value, split point, or constant from either diagnostic is used in Sections 1-7.

## 9. Contract status
Contract 20: not attempted here.
Contract 21: local integrability and exact coincidence cancellations proved; required pair-scale uniform majorant remains OPEN.
Contract 22: not attempted; c_FT remains UNSET.
Contract 23: obeyed; no probe-derived numerical datum, sampling, enclosure, or diagnostic split is used.

**Operational status:** NEAR-COINCIDENCE QUANTITATIVE TRIAL / LOCAL DOUBLE CANCELLATION PROVED / 1/D REMOVABILITY PROVED / PAIR-SCALE P-over-rho MAJORANT OPEN / GLOBAL SPLIT NOT YET ASSEMBLED / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
