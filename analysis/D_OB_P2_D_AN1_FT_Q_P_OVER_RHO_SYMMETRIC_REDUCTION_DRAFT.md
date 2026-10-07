# D-OB P2 — D-AN-1 FT_q P/rho Exact Symmetric Reduction — DRAFT

**Status:** PAPER-PROOF EXACT REDUCTION DRAFT / AWAITING CHAT AUDIT / BOUNDARY PAIR LEMMA OPEN / NOT A THEOREM
**Parent:** `analysis/D_OB_P2_D_AN1_FT_Q_P_DECOMPOSITION_DRAFT.md`, commit `641e2a2d4b0720e47c73f257cbf8de1b89eac9c5`, SHA-256 `67d821d4612015648758de57887fce699db1143952b658e6733cba1ebd61b518`, 330 lines, CHAT AUDIT PASS.
**Evidence:** EXACT ANALYTIC ALGEBRA ONLY / NO DIAGNOSTIC / NO INTERVAL COMPUTATION.

## 1. Contract-7 correction
`DeltaR/rho != (gamma_+-gamma_-)/rho` in general. Define the exact secant factor
`kappa_R=(R_+-R_-)/(gamma_+-gamma_-)` if the denominator is nonzero, with continuous extension `kappa_R=R_gamma(gamma_+)` at equality.
Then `-1<=kappa_R<=0` and exactly
`DeltaR/rho=(kappa_R/2)(gamma_+-gamma_-)/rho`. (1.1)

## 2. Symmetric distance identities
`d0=(D_+^2+D_-^2)/2=a^2+rho^2+lambda^2(mu-m)^2`, `u=D_++D_-`, `v=D_+D_-`.
`u^2=2d0+2v`. (2.1)
`v^2=d0^2-4rho^2b^2`. (2.2)
`S3=D_-^3+D_+^3=u^3-3uv=u(u^2-3v)`. (2.3)
`L_D=(D_-^2+D_-D_++D_+^2)/(D_-+D_+)=(u^2-v)/u`. (2.4)
`Delta3=D_-^3-D_+^3=4rho b(u^2-v)/u`. (2.5)

## 3. Symmetric h denominator
`h_+=h0-lambda rho b`, `h_-=h0+lambda rho b`, and `D_--D_+=4rho b/u` give
`h_+D_-+h_-D_+=h0u-4lambda rho^2b^2/u`. (3.1)
Hence the finite-difference denominator is `w v[h0u-4lambda rho^2b^2/u]`, with rho entering only through rho-even quantities.

## 4. Exact gamma/R finite difference
`X=h0 c(mu)+lambda^2rho^2b^2`. (4.1)
`(gamma_+-gamma_-)/rho=4bX/{w v[h0u-4lambda rho^2b^2/u]}`. (4.2)
Thus exactly
`DeltaR/rho=2kappa_R bX/{w v[h0u-4lambda rho^2b^2/u]}`. (4.3)
Under `rho->-rho`, plus/minus members interchange, so the secant quotient `kappa_R` is rho-even. Thus (4.3) contains no naked odd rho.

## 5. Exact P/rho reduction
Let `E=mb^2+C0`. The parent gives
`N_e=-lambda^2(m-mu)rho E`, `N_o=-lambda^2(m-mu)B1b`.
Therefore
`T_EE/rho=-lambda^2(m-mu)Rbar E S3`. (5.1)
`T_OO/rho=-4lambda^2(m-mu)Rbar B1b^2 L_D`. (5.2)
`T_RE/rho=-4lambda^2(m-mu)rho^2 b(DeltaR/rho)E L_D`. (5.3)
`T_RO/rho=-lambda^2(m-mu)b(DeltaR/rho)B1 S3`. (5.4)
and
`P/rho=-lambda^2(m-mu){Rbar[E S3+4B1b^2L_D]+b(DeltaR/rho)[4rho^2E L_D+B1S3]}`. (5.5)

## 6. rho-even ledger — W-4
`d0,v,u,S3,L_D,h0,w,X,kappa_R,DeltaR/rho` are rho-even in the symmetric representation above.
Hence every term (5.1)-(5.4), and `P/rho`, is rho-even. No naked odd power of rho remains.
The only extra explicit rho weight among the four reduced terms is `rho^2` in (5.3). On the frozen face,
`0<=rho^2<=(15/113)^2=225/12769<1/56`, since `225*56=12600<12769`. (6.1)
This is only a factor suppression specific to `T_RE/rho`, not a comparison of full term magnitudes.

## 7. Four-term sign table — W-5
For `rho>0`, `Rbar,S3,L_D>0`, and the exact signs are
`sign(T_EE)=sign(N_e)`. (7.1)
`sign(T_OO)=sign(A1)`. (7.2)
`sign(T_RE)=-sign(X)sign(N_e)`. (7.3)
`sign(T_RO)=-sign(X)sign(A1)`. (7.4)
For `X>0`, each DeltaR term opposes its corresponding Rbar term; for `X<0`, it has the same sign. This does not assert positivity of either pair.

## 8. Exact c(mu) single-negative-interval lemma
On `z=lambda m`,
`c(mu)=lambda(1-lambda^2)mu^2-z(1-2lambda^2)mu-lambda(rho^2+z^2)`. (8.1)
The leading coefficient is `lambda(1-lambda^2)>0`, while `c(0)=-lambda(rho^2+z^2)<0`.
Thus the product of the two roots is negative: the roots are real, nonzero, and of opposite signs.
Writing `mu_c^-<0<mu_c^+`, exactly `c(mu)<0 iff mu_c^-<mu<mu_c^+`. (8.2)
No frozen-box numerical value or sampling is used.

## 9. Exact X=0 derived boundary — W-6
For `rho>0`, `h0=lambda(1-m mu)>0`. Since `X=h0c(mu)+lambda^2rho^2b^2`, an interior zero of X can occur only where `c(mu)<0`, and there
`b^2=-h0c(mu)/(lambda^2rho^2)`. (9.1)
This is a derived b^2-boundary inside the exact c-negative interval, not a new mu-partition root.
At `X=0`, (4.2) gives `gamma_+=gamma_-`, hence `DeltaR=0`.
No root or enclosure of `C0` or `B1` is introduced.

## 10. Open status
No C0/B1 proof partition, rational root enclosure, paired-integral lower bound, `c_FT`, or `m0` is introduced.
**Operational status:** P/rho EXACT SYMMETRIC REDUCTION DRAFT / AWAITING CHAT AUDIT / CONTRACT 6-9 ADDRESSED WITH CONTRACT-7 CORRECTION / C0-B1 PARTITION NOT INTRODUCED / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
