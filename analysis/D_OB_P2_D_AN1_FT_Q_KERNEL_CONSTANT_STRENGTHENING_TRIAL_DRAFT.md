# D-OB P2 / D-AN-1 FT_q: kernel constant strengthening, exact trial

Status: NEW PROOF CANDIDATE; CHAT AUDIT PENDING. Contracts 20''--23'' FIXED.
Baseline S_K,lb=27/2500 remains CLOSED. No U or D-P2 certification is claimed.
Dependencies: pinned kernel paper proof 0bc53da572b6ae55d01005772c631235bc1c5cf1,
Judge contract 00138df257cee8e5480b412157dce36ae90743d0.

## Goal and symbols
Use exactly the definitions of P=(-g)*dbar-3*B*a2, d, S3, A, F, K,
in the kernel paper proof. On K, d<13/10, -g>=delta=30053/102400,
and the adverse secant contribution to F/S3 is <21/1000.
The established inequality S3/v^3>5/4 and L*s/w>(4/25)*(6/5)
are retained. The proof below uses exact rational interval endpoints.

## Polynomial monotonicity and split
The existing verified inequalities P_L>0 and P_m>0 on K imply
P(L,m,mu)>=P0(mu):=P(4/25,112/113,mu).
By the pinned B1 ordering lemma, B>0 on [-1,-1/2].
On [-1/2,-1/4], B may have either sign. If B>=0, -A/S3>=P/d;
if B<0, -A/S3>=-E>=-g. Thus on the right interval
-A/S3>=min(P/d,-g), and on the left -A/S3>=P/d.

## Exact Bernstein certificates
For each interval [a,b], substitute mu=a+(b-a)*t (0<=t<=1) and
write P0(mu)=sum_{j=0}^5 beta_j*binom(5,j)*t^j*(1-t)^(5-j).
These are the exact degree-five Bernstein coefficients:

Left interval [-1,-1/2]:
j=0: 1822500/1442897
j=1: 875925/1442897
j=2: 148239/510760
j=3: 466838497/2885794000
j=4: 9434127229/72144850000
j=5: 4160622181/28857940000
Minimum is beta_4=9434127229/72144850000 >13/100;
the difference is 55296729/72144850000 >0.

Right interval [-1/2,-1/4]:
j=0: 4160622181/28857940000
j=1: 43541078257/288579400000
j=2: 97360396247/577158800000
j=3: 220440930219/1154317600000
j=4: 492806733741/2308635200000
j=5: 43139741157/184690816000
Minimum is beta_0=4160622181/28857940000 >143/1000;
the difference is 33936761/28857940000 >0.

All comparisons are exact rational. Since the Bernstein basis is
nonnegative and sums to one, on the left P/d>(13/100)/(13/10)=1/10.
On the right P/d>(143/1000)/(13/10)=11/100.
Also -g>=30053/102400>11/100. Therefore:
left: -A/S3>1/10; right: -A/S3>11/100.
The adverse secant contribution is <21/1000 on both intervals, so
left: -F/S3>79/1000>3/40;
right: -F/S3>89/1000>2/25.
These strict bounds apply pointwise, including rho=0 by continuity.

## Exact integration and rational pi bound
For both intervals,
-L*s*F/(w*v^3)=(L*s/w)*(S3/v^3)*(-F/S3)
> (4/25)*(6/5)*(5/4)*(-F/S3)=(6/25)*(-F/S3).
The phi range has length pi. The mu interval lengths are 1/2 and 1/4.
Consequently
S_K>pi*(6/25)*[(1/2)*(3/40)+(1/4)*(2/25)]
=pi*(6/25)*(23/400)=69*pi/5000
>207/5000, using the explicit rational inequality pi>3.
Hence S_K >= S_K,lb' := 207/5000 >27/2500.
Improvement factor (207/5000)/(27/2500)=23/6 (~3.8333).
No diagnostic integrals or floating-point samples enter this proof.

## Audit gates
(32) Two interval polynomial Bernstein certificates and exact rational
integration supplied; pi>3 explicitly used.
(33) The previously audited global secant adverse bound 21/1000 is
retained unchanged, including its globally proved |Z|, v and u bounds.
No local replacements are asserted.
(34) Candidate uniform rational 207/5000 strictly exceeds baseline
27/2500, factor 23/6. Independently audit all 12 Bernstein coefficients,
their minimum ordering, the B>0 left-interval premise, and integrations
before elevating this candidate to a CLOSED strengthened contract.
U OPEN; c_FT UNSET; Boundary Pair Lemma OPEN; m0 UNAVAILABLE;
L3 BLOCKED; L1 PAUSED; D-P2 NOT_CERTIFIED.
