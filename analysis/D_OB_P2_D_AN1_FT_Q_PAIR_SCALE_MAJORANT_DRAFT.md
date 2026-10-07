# D-OB P2 — D-AN-1 FT_q Pair-Scale Majorant — DRAFT

**Status:** PAPER-PROOF MAJORANT DRAFT / AWAITING CHAT AUDIT
**Parent:** near-coincidence trial commit `deb0c7d42df12788929017ca933f05de9341a3b3`, CHAT AUDIT PASS.
**Governance:** Contract 21 core only. Probe outputs are NOT_EVIDENCE.

## 1. W-10 strengthened bound

For `Q_+=rho E+B1 b`, at `(mu,b)=(m,rho)`,
`Q_+=partial_mu Q_+=partial_b Q_+=0`.

Exact second derivatives obey on the frozen box
`|Q_bb|<=2`, `|Q_mumu|<=10`, `|Q_mub|<=7`.
Taylor's integral remainder and `|b-rho|<=D_+`, `|mu-m|<=D_+/lambda<=5D_+/2` give
`|Q_+| <= (1/2)[2D_+^2+2*7*(5D_+/2)D_+ +10*(5D_+/2)^2]`
`=41D_+^2<50D_+^2`.
The segment from `(m,rho)` to `(mu,b)` stays in the frozen box, so the displayed Hessian sup bounds apply along the full Taylor segment.
By symmetry `|Q_-|<50D_-^2`.

Since `N_+ =-lambda^2(m-mu)Q_+` and similarly for minus,
`|N_+|<=50lambda D_+^3`, `|N_-|<=50lambda D_-^3`.
Thus
`|R_+N_+/(wD_+^3)|<=25pi lambda/w`,
and likewise for minus.

## 2. W-11

Exact geometry gives
`1-c=(D^2+(1-lambda^2)(m-mu)^2)/2>=D^2/2`,
hence `h>=lambda D^2/2`.
Therefore
`h_+D_-+h_-D_+ >= (lambda/2)uv`.
The secant estimate becomes
`|b DeltaR/rho|<=4q|X|/(lambda w v^2u)`.

## 3. Near pointwise control

On `D_+<=rho`,
`|R_+N_+/(rho wD_+^3)|<=25pi lambda/(wD_+)`.
The symmetric statement holds for minus.

## 4. Global integrated equivalent

Let `F=hG`. The audited azimuthal identity is
`int F_rho dphi =2 int RJ dphi`.
After b-pair folding,
`int_0^pi P/(rho wv^3)dphi=(1/(2rho))int_0^(2pi)F_rho(rho)dphi`.

At `rho=0`, `h_rho=-lambda b` and, from FT_q (5.1), `gamma_rho=-lambda b/(wD)+hb/(wD^3)`, while `D` and `h` are independent of `b`. Hence both `h_rho` and `gamma_rho` are odd in `b`, so `F_rho=h_rho G-2hR gamma_rho` is odd in `b`; under `phi -> phi+pi`, `b -> -b`, and therefore `int_0^(2pi)F_rho(0)dphi=0`.

For `p_t=(t rho,0,lambda m)`, `t<1` gives `t^2rho^2+m^2<1`, so `p_t` is an interior point. P1 Section 2 gives smooth interior differentiation, and `|F_rhorho|<=C2/D` is integrable; differentiation/integration is therefore justified for `t<1`. The endpoint `t=1` is measure zero in the t-integral.
Thus, with `rho_t=t rho`,
`int_0^pi P/(rho wv^3)dphi
 =(1/2)int_0^1 int_0^(2pi)F_rhorho(rho_t)dphi dt`.

This retains the rho=0 cancellation before absolute values; it does not estimate `F_rho` and then divide by rho.

## 5. Explicit majorant

P1 Lemma 3.4 gives
`|F_rhorho|<=C2/D_t`, `C2=9pi+8`.
Therefore
`|int_0^pi P/(rho wv^3)dphi|
 <=(C2/2)int_0^1 int_0^(2pi)1/D_t dphi dt`.

Hence the integrated-equivalent pair-scale constant is
`C_*=(9pi+8)/2`.
With `dA/w=dmu dphi`, P1 Corollary 4.3 supplies uniform integrability over the swept family.

This majorant discards sign information. Under Contract 21 it is therefore restricted to an exact near-coincidence band to be specified in the later U construction; it must not be used as the north-side-wide or cap-wide U estimate. The far north region is to be treated with the symmetric `P/rho` form and W-11, retaining its algebraic structure.

This removes the artificial `1/rho` loss and passes through coincidence. It does not yet prove a small north/cap constant `U`; the near-band width and the separate far-region/cap estimates remain OPEN.

## 6. Ledger

Contract 20: not attempted.
Contract 21 technical coincidence majorant: PROVED in integrated-equivalent form, subject to chat audit. Quantitative north+cap `U`: OPEN.
Contract 22: not attempted; `c_FT` UNSET.
Contract 23: obeyed; no probe output, sampling, enclosure, or diagnostic split is used.

**Operational status:** PAIR-SCALE MAJORANT DRAFT / AWAITING CHAT AUDIT / integrated-equivalent `C_*=(9pi+8)/2` / NORTH+CAP U OPEN / SOUTH S_lb OPEN / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
