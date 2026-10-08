# D-OB P2 / FT_q: exterior-south one-sided residual, exact preliminary trial

Status: PROOF DRAFT / NOT AUDITED / NO POSITIVE SOUTH-MASS CLAIM.
Governance: contracts 20''--23'' v1.1, commit b1a10ea6f0ef127aaf4a40a93070cf270d03e073.
Kernel lower bound S_K>=207/5000 is CLOSED; 21'' remains OPEN.
Scope: exterior south J=(-1/4,mu_C), with mu_C<3/5 and C(mu_C)=0.
All bounds below are exact and uniform on J, including parameter endpoints
by continuous extension where appropriate.

## Definitions
L=lambda^2 in [4/25,8649/40000], m in [112/113,1],
r=rho^2=1-m^2 in [0,225/12769], a2=1-mu^2, s=m-mu,
h=1-m*mu, q=a2*cos(phi)^2, w^2=mu^2+L*a2.
d=a2+r+L*s^2, D_+^2=d-2*rho*b, D_-^2=d+2*rho*b,
v=D_+*D_-, u=D_++D_-, theta=4*LD/S3<=3/d.
B=B1, C=C0, E=m*q+C, T=(1-L)*m-(2-L)*mu,
Z=T-m*q/h+theta*E, M=h*u-4*r*q/u.
The exact secant completion in the audited kernel paper proof gives
F/S3=Rbar*(E+theta*B*q)
 +[2*kappa_R*lambda*q/(w*v*M)]*Y*((m/h)*Y+r*Z),
where -1<=kappa_R<=0 and Y=h*cstar+r*q.
Its adverse contribution is at most
J_sec=lambda*q*r^2*h*Z^2/(2*m*w*v*M).
This algebraic bound requires NO sign condition on E.

## Certificate 35: exterior-south sign bookkeeping
C'=3*(L-1)*mu^2-2*L*m*mu+2-L.
For -1/4<mu<3/5, |mu|<3/5 and mu^2<9/25, hence
C'>2-L-27/25-6*L/5=23/25-11*L/5
 >=88861/200000>2/5>0.
Thus C strictly increases throughout J, and
-3/2<C(-1/4)<C(mu)<C(mu_C)=0.
Indeed C(-1/4)=-1/2-m+(1-L)/64+L/4+(15/16)*L*m>-3/2.
Therefore -3/2<E=m*q+C<1.
The exact sign boundary is q_E=-C/m>0:
E>0 iff q>q_E, and E<0 iff q<q_E.
B<0 for mu>=-1/8; on (-1/4,-1/8), retain B-sign split.
The assertion B<0 on all of J is NOT used.

## Certificate 36: azimuthal positive/negative parts
For fixed mu, put k=-C/(m*a2)>0.
If k>=1 then E<=0 for every phi, and integral E_+ dphi=0.
If 0<k<1, put alpha=arccos(sqrt(k)). Exactly,
integral_0^pi E_+ dphi
 =m*a2*((1-2*k)*alpha+sin(2*alpha)/2).
Also integral E dphi=pi*(m*a2/2+C)=pi*g_tilde(mu),
and integral E_- dphi=integral E_+ dphi-pi*g_tilde(mu).
Here E_+=max(E,0), E_-=max(-E,0).
Because 1<=Rbar<=pi/2 pointwise,
integral Rbar*E dphi <= (pi/2)*integral E_+ dphi
 - integral E_- dphi.
On the B<0 subregion, theta*B*q<=0, so
integral Rbar*(A/S3) dphi
 <= (pi/2)*integral E_+ dphi-integral E_- dphi.
No phi-independent replacement of Rbar has been made.
The exact expression involving alpha is NOT a rational bound and
is not yet a contract-21'' residual certificate.

## Certificate 37: exact global exterior-south secant control
On J, a2>16/25, h>2/5, h<5/4, q<=a2<=1.
From v^2=(a2+r+L*s^2)^2-4*r*q,
v^2 >= (a2+r)^2-4*r*a2=(a2-r)^2.
As a2-r>16/25-225/12769>3/5, conclude v>3/5.
Also d>a2>16/25, u^2=2*(d+v)>62/25,
so u>3/2. This improves the crude D_+*D_- bound
from the exterior-south distance floor.
Since theta<=3/d<75/16, and E in (-3/2,1),
-225/32<theta*E<75/16.
Moreover T=(1-L)*m-(2-L)*mu obeys -2<T<13/10,
and 0<=m*q/h<5/2. Consequently
-369/32<Z<479/80, so |Z|<12.
The exact ratio bound is
4*r*q/(h*u^2)<28125/395839<1/14,
whence M>(13/14)*h*u>39/70.
Using lambda/w<=1, m>=112/113, v>3/5, h<5/4,
q<=1, r<=225/12769 and |Z|<12 yields
J_sec < (225/12769)^2*(5/4)*144
 / (2*(112/113)*(3/5)*(39/70))
 =6328125/75030644<1/10.
Thus, everywhere on J, the adverse secant part of F/S3 is <1/10.
This is a valid but likely too coarse bound for a sharp signed integral.

## Open bridge to contract 21''
The factor L*s*S3/(w*v^3) depends on both mu and phi,
and its sign is positive on J. Thus the preceding azimuthal
Rbar*E inequality CANNOT simply be multiplied by an averaged factor:
sign correlations with the weight must be retained.
In particular, the positivity of the unweighted g_tilde average
does not by itself determine the sign of the weighted G(mu).
No rigorous positive lower bound for the full south integral
integral_J integral_0^pi -L*s*F/(w*v^3) dphi dmu
is established in this trial. U remains OPEN.

## Next exact steps
1. Split mu at -1/8 and at exact algebraic root(s) of g_tilde;
   keep B and E sign boundaries explicit, without assuming root order.
2. Obtain rational upper/lower bounds for the weighted azimuthal
   integrals, using interval Bernstein certificates for mu and
   rational angular partitions where needed.
3. Improve J_sec from the global 1/10 bound on subintervals,
   then combine signed south contributions with north-far and near.
4. Submit every interval certificate and resulting rational
   C_south lower bound for independent chat audit before any
   21'' CLOSED claim.

Ledger: 20'' CLOSED (207/5000); 21'' OPEN; U OPEN; c_FT UNSET;
Boundary Pair Lemma OPEN; m0 UNAVAILABLE; L3 BLOCKED;
L1 PAUSED; D-P2 NOT_CERTIFIED.
