# D-OB P2 / D-AN-1 FT_q: Judge-adopted contract 20''--23''

Decision: Judge ADOPTED 3/3 (2026-10-08). This file records the replacement contract; it does not claim residual completion or D-P2 certification.
Basis: kernel paper-proof draft at commit 0bc53da572b6ae55d01005772c631235bc1c5cf1, file SHA-256 2218ef772642d68af756e53bd560949b77cdbb2049ccf384935969b5fddc7519.
Units: all S_K, C_out, U use the double-integral P convention, not H-normalized units.

## Contract 20'' (CLOSED)
On K=[-1,-1/4], S_K >= S_K,lb := 27/2500.
The cited kernel proof in fact gives S_K > 27/2500. Strengthening this constant is optional and does not reopen the proved baseline.

## Contract 21'' (OPEN)
Let I(mu,phi)=-lambda^2*(m-mu)*F*W and G(mu)=integral_0^pi I(mu,phi) dphi.
C_out := integral_{-1/4}^1 G(mu) dmu.
Prove the ONE-SIDED lower bound C_out >= -U with explicit uniform rational U.
Permitted decomposition: exterior south (-1/4,mu_C), north far, and near band |mu-m|<=rho including the cap.
On exterior south, s=m-mu>221/565 and D_+ , D_- >442/2825.
One may use the azimuthally averaged negative part:
U_minus := integral_{-1/4}^1 [-G(mu)]_+ dmu, with U>=U_minus.
Positive exterior-south contributions may be retained; no requirement to bound |C_out|.

## Contract 22'' (OPEN)
H >= (27/2500-U)/(2*pi*lambda).
Require U < 27/2500; then produce a uniform explicit rational c_FT>0
from this inequality (including rational bounds on pi and lambda as needed).
Set m0=min(c_FT,13/2000) only after c_FT is rigorously certified.
Do not call (27/2500-U)/(2*pi*lambda) a rational constant while lambda varies
without deriving an explicit uniform rational lower bound.

## Contract 23'' (FIXED)
Existing bans on diagnostic/probe evidence remain in force.
North signed diagnostic range -0.005 to -0.0065 is a warning for target
precision ONLY; it cannot be used as a proof constant.
U must be <27/2500=0.0108 at baseline; positive exterior-south mass
may be necessary to obtain a useful one-sided residual bound.

## Judge-adopted corrections
The former exterior-south claim s>1/2 is false. The correct uniform bound
is s>221/565, giving D_+ , D_- >442/2825.
For the existing band |mu-m|<=rho, the cap m<mu<=1 is entirely near
since 1-m=rho^2/(1+m)<rho; the old far-cap component is EMPTY and removed.

## Next proof order
(1) Improve kernel constant using mu-dependent -A/S3>=P/d and
mu-dependent S3/v^3>=2/d^(3/2), while retaining adverse secant control.
(2) Establish a positive exterior-south lower bound, then bound north far
and near residual with azimuthal sign correlations.
The exact inequality S_K>=27/2500 remains the certified baseline until
a stronger uniform rational constant is independently audited.

## Ledger
Judge ADOPTED 3/3; 20'' CLOSED; 21'' OPEN; 22'' OPEN; 23'' FIXED.
U OPEN; c_FT UNSET; FT_q Boundary Pair Lemma OPEN; m0 UNAVAILABLE;
L3 BLOCKED; L1 PAUSED; D-P2 NOT_CERTIFIED.
