# D-OB P2 / D-AN-1: FT_q exact south-kernel lower bound (paper-proof draft)

Status: CHAT AUDIT PASS for (B1)--(B12) as reported 2026-10-08; repository import only, NOT D-P2 certification.
Provenance: independent verification dated 2026-10-08 (provided under Astra name; document identifies author as Codex; attribution unresolved).
Verifier reported SHA-256: 29c9b8fa930360a1ff530e37f4efa7422e54991925787f7464145fa8e0597ed4. Verifier source is NOT embedded in this artifact.
The chat three-layer audit reports independent SymPy/rational/hand recomputation PASS. This draft records the proof and does not claim a new independent machine run.

## Domain and notation
lambda in [2/5,93/200], L=lambda^2 in [4/25,8649/40000], m in [112/113,1], r=rho^2=1-m^2.
mu in K=[-1,-1/4], a2=1-mu^2, q=b^2 in [0,a2], s=m-mu, h=1-m*mu.
dbar=a2+L*s^2, d=dbar+r, w^2=mu^2+L*a2.
D_+^2=d-2*rho*b, D_-^2=d+2*rho*b, u=D_++D_-, v=D_+*D_-.
u^2=2*(d+v), v^2=d^2-4*r*q, S3=u*(2*d-v), LD=(2*d+v)/u.
B=m*(1-L)*mu^2+((1+L)*m^2+L-2)*mu-L*m.
C=(L-1)*mu^3-L*m*mu^2+(2-L)*mu-m*(1-L).
cstar=(1-L)*mu^2-m*(1-2*L)*mu-(r+L*m^2).
E=m*q+C, g=m*a2+C, X=L*(h*cstar+r*q).
A=E*S3+4*B*q*LD, KR=4*r*E*LD+B*S3.
F=Rbar*A+b*(DeltaR/rho)*KR, W=1/(w*v^3).
S_K=integral_{mu=-1}^{-1/4} integral_{phi=0}^{pi} -L*s*F*W dphi dmu.

## Exact polynomial and distance bounds (B1)--(B3)
On K: -21/10<E<=g<=-delta, delta=30053/102400; 16/25<=d<13/10<4/3;
r<=225/12769<1/56, q<=15/16, h>=1.
g'=3*(L-1)*mu^2-2*m*(1+L)*mu+(2-L)>0 on [-1,0].
g(-1/4)=(60*L*m+15*L-4*m-31)/64 <= -delta.
C_L=s*a2>=0, C_m=-L*mu^2-(1-L)<0. At L=4/25,m=1,
the degree-3 Bernstein coefficients for C(-1+3*t/4) are
[-2,-209/100,-139/80,-83/64], hence C>=-209/100>-21/10.
d_L=s^2>0; d_m=2*(L*m-L*mu-m)<0. At L=4/25,m=1,
d endpoints on K are 16/25 and 19/16; d is concave in mu.
d=2-((1-2*L)/(1-L))*m^2-(1-L)*(mu+L*m/(1-L))^2 <13/10.

Set P=(-g)*dbar-3*B*a2. Its derivatives satisfy
P_L=s*(a2*(3*h-dbar)-s*g)>0;
g_m=L*a2-mu^2, B_m=mu*(2*(1+L)*m+(1-L)*mu)-L<=-L,
P_m>=L*a2*(3-dbar)-2*L*s*g>0.
Thus P(L,m,mu)>=P(4/25,112/113,mu). With mu=-1+3*t/4, t in [0,1],
P=sum_{j=0}^5 beta_j*binom(5,j)*t^j*(1-t)^(5-j), where
beta_0=1822500/1442897
beta_1=805275/2885794
beta_2=13437063/230863520
beta_3=2112429969/23086352000
beta_4=199963336149/1154317600000
beta_5=43139741157/184690816000
All are >= beta_2; beta_2-7/125=12717647/5771588000>0.
Consequently P>=beta_2>7/125>0 uniformly.

## A and secant sign (B4)--(B11)
theta=4*LD/S3=2*(2*d+v)/((d+v)*(2*d-v))<=3/d,
since the numerator of the cleared difference is (d-v)*(2*d+3*v)>=0.
For B>=0, A/S3=E+theta*B*q<=-P/d<-(7/125)*(10/13)
=-14/325<-21/500; for B<0, A/S3<=E<=-delta<-21/500.

Define T=(1-L)*m-(2-L)*mu, Y=X/L=h*cstar+r*q.
Exact identities: cstar=h-d; B=m*cstar+r*T; C+h*T=mu*(L-1)*s^2.
Then B=(m/h)*Y+r*(T-m*q/h). Let Z=T-m*q/h+theta*E.
KR/S3=(m/h)*Y+r*Z.
For R(gamma)=arccos(gamma)/sqrt(1-gamma^2), its secant kappa_R satisfies -1<=kappa_R<=0.
Let M=h*u-4*r*q/u. Exact finite difference:
b*(DeltaR/rho)=2*kappa_R*lambda*q*Y/(w*v*M).
Thus F/S3=Rbar*(E+theta*B*q)+[2*kappa_R*lambda*q/(w*v*M)]*Y*((m/h)*Y+r*Z).
With alpha=m/h>0,
Y*(alpha*Y+r*Z)=alpha*(Y+r*Z/(2*alpha))^2-r^2*Z^2/(4*alpha).
The first term is favorable because kappa_R<=0. The adverse part is at most
lambda*q*r^2*h*Z^2/(2*m*w*v*M).
Exact bounds: h*T-m*q=-E+mu*(L-1)*s^2>0; -10<Z<10;
v^2>256/625-15/224>1/4, v>1/2, u>3/2;
4*r*q/(h*u^2)<5/168<1/32, M>(31/32)*h*u, lambda/w<=1.
Therefore adverse part <14125/680512<21/1000.
As Rbar>=1 and A/S3<-21/500,
F/S3<-21/500+21/1000=-21/1000<-1/50 on K.

## Integral lower bound (B12)
s>=561/452>6/5, w<=1. By convexity,
S3/v^3=D_+^(-3)+D_-^(-3)>=2/d^(3/2)>5/4.
Hence -L*s*F/(w*v^3)>(4/25)*(6/5)*(1/50)*(5/4)=3/625.
The integration domain has measure 3*pi/4, so
S_K>9*pi/2500>27/2500. At rho=0 use continuous extension
of the symmetric secant; on K all denominators remain nonzero.

## Corrections and governance
The former claim s>1/2 on the entire exterior south (-1/4,mu_C) is FALSE.
Exact counterexample: lambda=2/5, tau=15/16, m=480/481, rho=31/481,
mu=9/16, C(mu)=-6453/1970176<0, s-1/2=-497/7696.
C(3/5)>=78/3125>0 implies mu_C<3/5 and s>221/565 there.
This is a PROPOSED correction to contract 21'; frozen contract change requires Judge.
For the existing near band |mu-m|<=rho, cap m<mu<=1 lies entirely in near
since 1-m=rho^2/(1+m)<rho; far-cap is EMPTY (proposed contract 26' correction).
The one-sided C_out bound and contract modification remain Judge decisions.
Candidate NEXT: C_out>=-27/5000 is OPEN, and the diagnostic north contribution
must NOT be treated as a proof. Retain positive exterior-south mass in future bounds.
No U bound, c_FT, m0, L3, L1 or D-P2 certification is claimed.
