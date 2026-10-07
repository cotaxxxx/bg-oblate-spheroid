# D-OB P2 — D-AN-1 FT_q North+Cap U Assembly — DRAFT

**Status:** PAPER-PROOF U-ASSEMBLY DRAFT / CONTRACT 24–27 / PARTIAL CLOSURE ONLY
**Parent:** Pair-scale majorant v1.2 commit `96b92860a75861a70d352943df63a6590789236a`, SHA-256 `7132b4f4ab8384da524f9f2467a6ca163a1414968adb0edd44a5014ca819700a`, CHAT AUDIT PASS.
**Evidence:** EXACT ANALYTIC INEQUALITIES ONLY / NO PROBE VALUES / NO SAMPLING / NO ENCLOSURE.

## 1. Variables and exact baseline band

Put `s=m-mu`. Since
`D_+^2=a^2+rho^2-2rho b+lambda^2s^2`
and similarly for minus,
`D_+>=lambda|s|`, `D_->=lambda|s|`. (1.1)

Choose the baseline near band
`B_near := {(mu,phi): |mu-m|<=rho}`. (1.2)
This is Contract 24 with the exact rational choice `kappa=1`.

On its complement,
`|s|>rho`, hence
`D_+,D_->lambda rho>=2rho/5`. (1.3)
Thus
`v=D_+D_->4rho^2/25`, `u=D_++D_->4rho/5`. (1.4)

A narrower `|s|<=rho^2` band would improve the near-band measure from `O(rho)` to `O(rho^2)`, but its far complement gives only `D_±>lambda rho^2`; this weakens the W-11 denominator powers. No such narrower band is adopted in this draft.

## 2. Near-band measure and U_near

The `dmu dphi` measure of (1.2), after intersection with `[-1,1]x[0,2pi]`, is at most
`M0=4pi rho`. (2.1)
The corresponding surface area is at most `M0`, because `dA=w dmu dphi` and `w<=1`.

Pair-scale v1.2 gives `C_*=(9pi+8)/2` and
`U_near <= C_* sup_p int_{B_near} dA/(wD)`. (2.2)
Since `w>=lambda`, Corollary 4.2 gives
`U_near <= C_*(1/lambda) 2sqrt(4pi M0) <= C_* 20pi sqrt(rho)`. (2.3)

Using `rho<=15/113`, `pi<22/7`, `sqrt(15/113)<3/8`, and
`C_*<(9(22/7)+8)/2=127/7`, one obtains
`U_near < (127/7)*20*(22/7)*(3/8)=20955/49`. (2.4)

This is a valid uniform rational bound, but quantitatively coarse. It is not by itself a plausible closure against a small south lower bound.

## 3. Exact rational lower placement of mu_C

Recall
`C0(mu)=(lambda^2-1)mu^3-lambda^2 m mu^2 +(2-lambda^2)mu-m(1-lambda^2)`.
At `mu=1/2`,
`C0(1/2)=7/8-m+(3lambda^2/8)(2m-1)`. (3.1)

This decreases with `m` because `-1+3lambda^2/4<0`, and increases with `lambda^2` because `2m-1>0`.
Therefore
`C0(1/2)<=C0(1/2)|_{m=112/113, lambda^2=(93/200)^2}`
`=-1319883/36160000<0`. (3.2)
Since `C0<0` exactly below its unique physical root,
`mu_C>1/2`. (3.3)
Consequently on `mu_C<mu<m`,
`0<s=m-mu<m-mu_C<1/2`. (3.4)
No numerical root enclosure is used.

## 4. Far-north exact denominator ledger

Define
`F_far := {mu_C<mu<m, |mu-m|>rho}`. (4.1)
On this set (1.3)–(1.4) hold. Also `D_±<=2`, hence
`u<=4`, `v<=4`. (4.2)

For
`S3=D_-^3+D_+^3`, `L_D=(D_-^2+D_-D_++D_+^2)/u`,
the elementary bounds are
`0<S3<=16`, `0<L_D<=3`. (4.3)
W-11 gives
`h_+D_-+h_-D_+ >= (lambda/2)uv`, (4.4)
hence
`|b DeltaR/rho|<=4q|X|/(lambda w v^2u)`. (4.5)

The four exact P/rho terms are
`T_EE/rho=-lambda^2 s Rbar E S3`,
`T_OO/rho=-4lambda^2 s Rbar B1 q L_D`,
`T_RE/rho=-4lambda^2 s rho^2 b(DeltaR/rho)E L_D`,
`T_RO/rho=-lambda^2 s b(DeltaR/rho)B1 S3`. (4.6)

Using only (1.3)–(1.4) in (4.5) gives
`v^2u > (4rho^2/25)^2(4rho/5)=64rho^5/3125`. (4.7)
Thus naive termwise absolute values can generate negative powers of rho in the last two terms; the explicit `rho^2` in `T_RE` is insufficient by itself, and `T_RO` has no such explicit suppression.

Accordingly the far-north termwise estimate is **OPEN**. Contract 25 is not discharged. Further algebraic use of `X`, `B1`, `E`, or paired cancellation is required before a rho-uniform useful `U_far` can be claimed.

## 5. Cap ledger

Let `C_cap := {m<mu<=1}`. Then
`0<mu-m<=1-m<=1/113`. (5.1)
Its portion with `|mu-m|<=rho` is already included in `B_near`.

On the remaining cap, `mu-m>rho`, so
`D_±>lambda rho`, `v>4rho^2/25`, `u>4rho/5`,
and W-11 apply. The outer factor obeys
`|m-mu|<=1/113`. (5.2)

However, applying (4.5) termwise with only these denominator bounds again leaves adverse negative powers of rho in the DeltaR terms. The cap width factor `1/113` alone does not remove that loss.

Hence a useful uniform `U_cap` is **OPEN**. Contract 26 is only partially discharged: exact cap width and near-band absorption are proved; the far-cap trap estimate is not closed.

## 6. Assembly status and trade-off

The intended assembly is
`U=U_near+U_far+U_cap`. (6.1)
At present only `U_near` has an explicit uniform rational bound:
`U_near<20955/49`. (6.2)
Both `U_far` and `U_cap` remain OPEN, so no finite useful assembled `U` is claimed.

The baseline band `|s|<=rho` gives near scaling `O(sqrt(rho))` but far distance scale `D_±>lambda rho`.
The alternative `|s|<=rho^2` gives near scaling `O(rho)` but only far distance scale `D_±>lambda rho^2`.
Thus narrowing the band improves the near estimate while worsening the raw W-11 far denominator. This trade-off is exact and unresolved here.

Contract 24: baseline band and explicit near bound CLOSED, quantitatively coarse.
Contract 25: OPEN.
Contract 26: PARTIAL / far-cap OPEN.
Contract 27: assembly formula fixed, assembled U OPEN.
Contract 20: not attempted.
Contract 22: not attempted; `c_FT` UNSET.
Contract 23: obeyed.

**Operational status:** U-ASSEMBLY DRAFT / CONTRACT 24 BASELINE CLOSED / CONTRACT 25 OPEN / CONTRACT 26 PARTIAL / U_near<20955/49 / U_far OPEN / U_cap OPEN / U OPEN / SOUTH S_lb OPEN / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
