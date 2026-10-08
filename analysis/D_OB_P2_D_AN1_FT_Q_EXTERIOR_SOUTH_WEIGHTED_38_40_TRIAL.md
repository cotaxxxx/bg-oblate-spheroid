# D-OB P2 FT_q exterior south: weighted certificates 38--40 (partial trial)

Status: EXACT COARSE ONE-SIDED BOUND CANDIDATE; certificate 39 OPEN;
NOT A CLOSURE OF CONTRACT 21''. Independent chat audit PENDING.
Parent: exterior south certificates 35--37, commit 37ffce8b8ba0395b14109663d670505a0b0f041c.
Parameter face: 2/5<=lambda<=93/200, L=lambda^2,
112/113<=m<=1, rho^2=1-m^2, 0<=rho<=15/113.
Domain J=(-1/4,mu_C), 0<mu_C<3/5; a=sqrt(1-mu^2),
s=m-mu>0, h=1-m*mu, q=a^2*cos(phi)^2,
d=a^2+rho^2+L*s^2, v=D_+*D_-, w^2=mu^2+L*a^2.
S3/v^3=D_+^(-3)+D_-^(-3).
Let f=F/S3 and H_w=S3/v^3 (not to be confused with global H).
I=-lambda^2*s*F/(w*v^3)=-(lambda^2*s/w)*H_w*f.
G(mu)=integral_0^pi I dphi (OUTSIDE FACTOR INCLUDED).
C_south=integral_J G(mu) dmu.

## 38. Weight envelope and sign-correct conversion

D_+^2=d-2*rho*b and D_-^2=d+2*rho*b, |b|<=a.
Since a^2>16/25 and 2*rho*a<=30/113,
d-2*rho*a>16/25-30/113=1058/2825>0.
Define the explicit mu-dependent envelopes
w_min(mu)=2*(d+2*rho*a)^(-3/2),
w_max(mu)=2*(d-2*rho*a)^(-3/2).
These depend on mu and the frozen face parameters but NOT phi.
Then 0<w_min<=H_w<=w_max.
Also d-2*rho*a>1058/2825>9/25, so
w_max<2*(25/9)^(3/2)=250/27<10.

Set E=m*q+C0(mu), E_+=max(E,0), E_-=max(-E,0).
Let GE(mu)=integral_0^pi Rbar*E dphi, an INNER angular quantity.
The sign-separated weighted inequality is
integral_0^pi H_w*Rbar*E dphi
 <= (pi/2)*w_max*integral E_+ dphi
    -w_min*integral E_- dphi.
The pointwise completed-square upper estimate from certificate 37 is
f<=Rbar*(E+theta*B*q)+J_sec,
where theta>0 and 0<=J_sec<1/10.
For B<0, theta*B*q<=0, hence
G(mu)>=-(lambda^2*s/w)*[
 (pi/2)*w_max*integral E_+ dphi
 -w_min*integral E_- dphi
 +(pi/10)*w_max
].
This is the required signed conversion: negative sign OUTSIDE the
bracket; the inner bracket may itself be negative.
For B>=0 the additional nonnegative upper term is bounded by
(pi/2)*w_max*integral theta*B*q dphi.
Thus the exact uniform form for arbitrary B is
G(mu)>=-(lambda^2*s/w)*[
 (pi/2)*w_max*integral E_+ dphi
 -w_min*integral E_- dphi
 +(pi/2)*w_max*integral theta*B_+*q dphi
 +(pi/10)*w_max
],
where B_+=max(B,0).
This retains the B sign split without asserting its root location.

## 39. Rational cutoff: OPEN (not falsely claimed)

On mu>=-1/8, B<0 by certificate 35; on
(-1/4,-1/8), B sign depends on parameters and B_+ is retained.
The exact E_+ integral from certificate 36 contains
alpha=arccos(sqrt(-C0/(m*a^2))) when 0<-C0/(m*a^2)<1.
No rational mu_* is certified here as separating a nonnegative G
region from a negative G region. In particular, an upper bound on
the bracket in certificate 38 cannot by itself certify G<0:
it only supplies a LOWER bound for G.
The sharp bound on integral [-G]_+ remains OPEN.
The coarse global bound below does not require any cutoff.

## 40. Explicit rational coarse south lower bound

First, |B|<5/4 throughout J. Indeed write
B=m*(1-L)*mu^2+K*mu-L*m,
K=(1+L)*m^2+L-2.
Since m^2>49/50 and L>=4/25,
K>(1+4/25)*(49/50)+4/25-2>-1;
also K<=-1+2*L<0. Hence |K|<1.
Using |mu|<3/5, mu^2<9/25, L<1/4 gives
|B|<9/25+3/5+1/4=121/100<5/4.
Certificate 35 yields E<1; certificate 37 yields theta<75/16.
Therefore E+theta*B*q<1+(75/16)*(5/4)=437/64.
Since Rbar<=pi/2, pi<22/7, and J_sec<1/10,
f< (11/7)*(437/64)+1/10<11.
This is a pointwise upper bound (negative f is allowed).
Furthermore w>=lambda*a, a>4/5, and s<5/4, so
lambda^2*s/w <=lambda*s/a
 < (93/200)*(5/4)/(4/5)=465/640<3/4.
Consequently
G(mu)=-(lambda^2*s/w)*integral H_w*f dphi
 > -(3/4)*10*11*pi > -(3/4)*10*11*(22/7)
 > -260.
The last implication is valid because H_w>0 and f<11 pointwise:
H_w*f<=11*H_w<110.
Since length(J)=mu_C+1/4<17/20,
C_south=integral_J G dmu> -260*(17/20)=-221.
Thus U_south=221 is an explicit rational valid (very weak)
one-sided south bound. It is NOT the sharp negative-part integral.

## Global budget / honest status

To close 21'' using this crude certificate and separate north/near
one-sided bounds U_north and U_near, a sufficient condition would be
U_south+U_north+U_near<207/5000.
With U_south=221 this cannot follow from NONNEGATIVE U_north,
U_near. A more refined south certificate or signed compensation is
mandatory. No assertion that the total target is met is made.
Do not interpret the bound C_south>-221 as south positivity.
Ledger: certificates 35--37 CHAT AUDIT PASS; 38 candidate;
39 OPEN; 40 coarse rational candidate; 21'' OPEN; U OPEN;
c_FT UNSET; Boundary Pair Lemma OPEN; m0 UNAVAILABLE;
L3 BLOCKED; L1 PAUSED; D-P2 NOT_CERTIFIED.
