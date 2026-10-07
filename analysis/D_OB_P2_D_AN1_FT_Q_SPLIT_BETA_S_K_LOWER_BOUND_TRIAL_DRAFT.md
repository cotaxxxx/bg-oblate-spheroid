# D-OB P2 — Split-beta South Kernel Lower-Bound Trial — DRAFT

**Status:** EXACT PARTIAL BOUNDS / POSITIVE S_K,lb NOT PROVED / CHAT AUDIT PENDING.
**Parent:** B1 ordering lemma commit `428320ec7fda757e17e9e19d0e0236aba99d9aab`, CHAT AUDIT PASS.
**Predeclared replacement:** contracts 20'-23' (split beta). All inequalities below are analytic; no diagnostic data or numerical sampling is evidence.

## 1. Split and units (W-13)

Write `K=[-1,-1/4]`, `S_K=int_K int_0^pi -lambda^2 (m-mu) F W dphi dmu`, with `W=1/(w v^3)` and `F=Rbar(E S3+4 B1 q L_D)+b(DeltaR/rho)(4 rho^2 E L_D+B1 S3)`.
Define `U_signed` as the **negative of the signed integral contribution** of the complementary mu-domain `(-1/4,1]`, partitioned into exterior south `(-1/4,mu_C)`, north `(mu_C,m)`, and cap `(m,1]`.
Then **exactly** `H=(S_K-U_signed)/(2 pi lambda)`, and `|U_signed|<=U` implies `H>=(S_K,lb-U)/(2 pi lambda)` if `S_K>=S_K,lb`.
This supersedes old `S=int_(-1)^mu_C ...` and old `U` (north+cap only). The enlarged `U` is OPEN. No c_FT is set.

## 2. Uniform E gap on K

Let `L=lambda^2 in [4/25,8649/40000]`, `m in [112/113,1]`, `rho<=15/113`. Since `q<=1-mu^2`, `E<=g(mu)`.
`g'=3(L-1)mu^2-2m(1+L)mu+(2-L)` is concave in mu; on `[-1,0]` its minimum is at an endpoint. Both `g'(-1)=(2L-1)+2m(1+L)>0` and `g'(0)=2-L>0`. Thus g increases on `[-1,0]`.
`g(-1/4)=(60Lm+15L-4m-31)/64`. It is affine separately in m and L, so extrema on the rectangle occur at its four corners. The four exact values are:
`(m,L)=(112/113,4/25): -13023/36160`, `(112/113,8649/40000): -17051733/57856000`, `(1,4/25): -23/64`, `(1,8649/40000): -30053/102400`.
The maximum is `-30053/102400`; hence on K, `-E>=delta:=30053/102400>0` uniformly.

## 3. Explicit favorable EE mass, independent of adverse terms

On K, `s=m-mu>1`, `D_±>=lambda*s>2/5`, `D_±<=2`, `w<=1`, `v<=4`, `S3=D_-^3+D_+^3>16/125`, `W>=1/64`, `Rbar>=1`.
The favorable EE integrand `-lambda^2 s Rbar E S3 W` therefore exceeds `lambda^2*delta/500` pointwise.
Integrating over K (mu-length 3/4, phi-length pi), with `lambda^2>=4/25` and `pi>3`, gives the exact rational bound
`EE_K > (4/25)*(30053/102400)*(1/500)*(3/4)*3 = 270477/1280000000 >0`.
This is **only the EE component**, not a lower bound for the full S_K.

## 4. Adverse ledger and finite non-singular denominator

The four pieces of S_K have signs: EE favorable; OO adverse where `B1>0`, i.e. `K intersect [-1,mu_B^-)` (ordering lemma audited); RE and RO are of undetermined sign because X is not fixed.
On K, `D_±>2/5`, `v>4/25`, `u>4/5`, `w>=lambda>=2/5`, `q<=15/16`, `s<=2`. In particular `lambda*w*v^2*u > (2/5)^2*(4/25)^2*(4/5)=256/78125`.
From the exact secant bound `|b DeltaR/rho|<=4q|X|/(lambda*w*v^2*u)`, there are no negative powers of rho in this region.
For `c(mu)=lambda[(1-L)mu^2-m(1-2L)mu-(rho^2+Lm^2)]`, triangle inequalities give `|c(mu)|<=lambda(1+1+1+1)=4lambda`, `h0=lambda(1-m mu)<=2lambda`, and `|X|<=h0|c|+lambda^2 rho^2 q<=9lambda^2<=9`.
Consequently `|b DeltaR/rho| < 4*(15/16)*9*(78125/256)=10546875/1024` (deliberately coarse). All these bounds are exact and uniform, but far too large for a positive net lower bound using direct termwise subtraction.

## 5. Unresolved comparison

The EE bound in section 3 cannot be promoted to S_K,lb: the OO adverse term is present on a nonempty subinterval, and RE/RO require bounds integrated with their correlated weights. The coarse secant bound above does not establish dominance of EE over adverse terms. A refined exact cancellation, sign lemma, or weighted integration estimate is required.
**S_K,lb remains OPEN.** The expanded U, c_FT, Boundary Pair Lemma, and m0 remain OPEN/UNSET. No interval computation is authorized. D-P2 NOT_CERTIFIED; L3 BLOCKED; L1 PAUSED.
