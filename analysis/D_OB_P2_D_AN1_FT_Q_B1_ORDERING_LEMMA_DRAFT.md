# D-OB P2 — FT_q B1 Ordering Lemma — DRAFT

**Status:** EXACT ORDERING PROOF / AWAITING CHAT AUDIT / SOUTH S_lb OPEN.
**Parent:** U-assembly draft `b7c8817c7f53da55956e8d73fcbbd80b20536468`, CHAT AUDIT PASS.
**Predeclaration:** Contract 12, `-1/2 < mu_B^- < -1/8`; order versus `-1/4` left parameter-dependent.
**Method:** Rational polynomial arithmetic only; no probes, sampling, or enclosure.

## 1. Definitions

Set `L=lambda^2 in [4/25,8649/40000]`, `m in [112/113,1]`. From the audited B1 structure,
`B1(mu)=L*m^2*mu-L*m*mu^2-L*m+L*mu+m^2*mu+m*mu^2-2*mu`.
The existing exact-root lemma supplies a unique physical negative root `mu_B^- in (-1,0)`, with `B1>0` to its left and `B1<0` to its right.

## 2. Positive endpoint at -1/2

`B1(-1/2)=1+m/4-m^2/2-L*(m^2/2+5m/4+1/2)`.
`partial_m B1=1/4-m-L*(m+5/4)<0` throughout the frozen box, because `m>=112/113>1/4` and `L>0`.
`partial_L B1=-(m^2/2+5m/4+1/2)<0`.
Therefore its exact minimum occurs at `m=1,L=8649/40000`, and
`B1(-1/2)>=3/4-(9/4)*(8649/40000)=42159/160000>0`.

## 3. Negative endpoint at -1/8

`B1(-1/8)=1/4+m/64-m^2/8-L*(m^2/8+65m/64+1/8)`.
`partial_m B1=1/64-m/4-L*(m/4+65/64)<0` since `m>=112/113>1/16`.
`partial_L B1=-(m^2/8+65m/64+1/8)<0`.
Therefore its exact maximum occurs at `m=112/113,L=4/25`, and
`B1(-1/8)<=-37043/638450<0`.

## 4. Root location and parameter-dependent order

The unique negative physical root and the preceding strict signs imply
`-1/2<mu_B^-<-1/8` uniformly.

For `mu=-1/4`,
`B1(-1/4)=1/2+m/16-m^2/4-L*(m^2/4+17m/16+1/4)`.
`partial_m B1=1/16-m/2-L*(m/2+17/16)<0`, and `partial_L B1<0`.
At `L=4/25`, the minimum at `m=1` is
`B1(-1/4)>=5/16-(25/16)*(4/25)=1/16>0`.
At `L=8649/40000`, the maximum at `m=112/113` is
`B1(-1/4)<=-37824549/2043040000<0`.
Thus the sign at `-1/4` changes across the frozen lambda range, and no uniform order versus `-1/4` is asserted.

## 5. Adverse set and limits

For the favorable E-kernel `K=[-1,-1/4]`, the B1-positive (T_OO adverse) set is exactly
`K intersect [-1,mu_B^-)`, up to the zero boundary. It cannot be discarded when lower-bounding the south integral.

This lemma does not bound the integrated adverse terms, does not provide a positive rational `S_lb`, and does not certify the Boundary Pair Lemma.

**Operational status:** B1 ORDERING LEMMA DRAFT / AWAITING CHAT AUDIT / ORDER -1/2<mu_B^-<-1/8 PROVED / ORDER VS -1/4 PARAMETER-DEPENDENT / SOUTH S_lb OPEN / U OPEN / c_FT UNSET / BOUNDARY PAIR LEMMA OPEN / m0 UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED.
