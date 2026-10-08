# D-OB P2 / D-AN-1 FT_q: Judge contract 20''--23'', v1.1 constant upgrade

Status: v1.1 records CHAT AUDIT PASS of kernel strengthening and the resulting numerical substitution. It does not alter the Judge-approved one-sided structure.
Parent fixed contract: 00138df257cee8e5480b412157dce36ae90743d0.
Kernel strengthening: a3fbbb8eb28dfd9016270c90950ed26828a720f1;
SHA-256 94f9c417bc8df4e7b582dc6ab7f87101898b13899615aa1009b02d947ef4872c.
User-reported chat audit: all 12 Bernstein coefficients and interval constants independently recomputed PASS.
Units: S_K, C_out and U are in double-integral P units, not H units.

## 20'' CLOSED -- strengthened
On K=[-1,-1/4], S_K >= S_K,lb := 207/5000.
The previous 27/2500 bound remains in history and is superseded for residual comparisons.
Proof uses exact Bernstein interval certificates, a global adverse secant bound,
and pi>3. Improvement factor over original lower bound: 23/6.

## 21'' OPEN -- one-sided exterior residual
I(mu,phi)=-lambda^2*(m-mu)*F*W;
G(mu)=integral_0^pi I(mu,phi) dphi;
C_out=integral_{-1/4}^1 G(mu) dmu.
Prove C_out >= -U with a uniform explicit rational U.
Allowed partition: exterior south (-1/4,mu_C), north far,
near band |mu-m|<=rho including cap. Exterior south has
s=m-mu>221/565, D_+ , D_- >442/2825.
Allowed: U_minus=integral_{-1/4}^1 [-G(mu)]_+ dmu, with U>=U_minus.
Do not impose the obsolete two-sided |C_out|<=U contract.
Positive exterior-south contributions may be retained.

## 22'' OPEN -- certification condition
H >= (207/5000-U)/(2*pi*lambda).
Require U < 207/5000.
Only after a proof of that inequality may a uniform rational c_FT>0
be declared, by bounding pi and lambda rationally; then
m0=min(c_FT,13/2000). No value is currently assigned to c_FT or m0.

## 23'' FIXED -- evidence and diagnostic separation
Numerical diagnostics are not proof constants. The reported north signed
contribution -0.005 to -0.0065 is retained only as a target-precision warning.
The new 0.0414 threshold improves margin but does not prove U.
All prior prohibitions on sampling/probe-derived certification remain.

## Corrections and next work unit
The old exterior-south claim s>1/2 was false; the adopted bound is
s>221/565, implying D_+ , D_- >442/2825.
For |mu-m|<=rho, cap m<mu<=1 is all near; far-cap is EMPTY and removed.
Next: prove an explicit exterior-south lower bound for G(mu) integrated over
(-1/4,mu_C), retaining positive mass. Rebuild the square-completion
argument with E of indeterminate sign; the old |Z| bound used E<0 on K
and cannot be imported without reproof. If B<0 then A/S3<=E, but
E itself need not be negative throughout the exterior-south region.
Then bound north far and near contributions to obtain U<207/5000.

## Ledger
20'' CLOSED (upgraded); 21'' OPEN; 22'' OPEN; 23'' FIXED.
U OPEN; c_FT UNSET; Boundary Pair Lemma OPEN; m0 UNAVAILABLE;
L3 BLOCKED; L1 PAUSED; D-P2 NOT_CERTIFIED.
