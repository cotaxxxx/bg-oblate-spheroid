#!/usr/bin/env python3
"""D-OB P2 / certificate 39': exact independent algebra certificate.

Default execution uses only symbolic polynomials, integers, and rational
arithmetic. No quadrature or floating point enters a proof assertion.
The optional --diagnostic mode is separate NOT_EVIDENCE counterexample search.
Requires SymPy. This is not the canonical D-P2 certification checker.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import product
from math import comb, isqrt
from pathlib import Path
import sympy as S

Q = S.Rational
L, m, mu = S.symbols('L m mu', real=True)
a2 = 1-mu**2
r = 1-m**2
s = m-mu
h = 1-m*mu
d = a2+r+L*s**2
B = m*(1-L)*mu**2+((1+L)*m**2+L-2)*mu-L*m
C = (L-1)*mu**3-L*m*mu**2+(2-L)*mu-m*(1-L)
g = m*a2+C
cstar = (1-L)*mu**2-m*(1-2*L)*mu-(r+L*m**2)
T = (1-L)*m-(2-L)*mu
Llo, Lhi, mlo = Q(4,25), Q(8649,40000), Q(112,113)
RMAX = Q(225,12769)
BOX = [(Llo,Lhi),(mlo,Q(1)),(Q(-1,4),Q(3,5))]

def check(condition, message):
    if not bool(condition):
        raise AssertionError(message)

def zero(expr, message):
    check(S.cancel(S.expand(expr)) == 0, message)

def bernstein_certificate(expr):
    z = S.symbols('z0:3')
    subs = {v:lo+(hi-lo)*t for v,t,(lo,hi) in zip((L,m,mu),z,BOX)}
    p = S.Poly(S.expand(expr.subs(subs, simultaneous=True)),*z)
    deg = p.degree_list()
    coefficients = {}
    for k in product(*(range(n+1) for n in deg)):
        coefficients[k] = sum(
            c*S.prod(Q(comb(ki,ji),comb(ni,ji)) for ki,ji,ni in zip(k,j,deg))
            for j,c in p.terms() if all(ji<=ki for ji,ki in zip(j,k)))
    rebuilt = sum(c*S.prod(S.binomial(n,ki)*t**ki*(1-t)**(n-ki)
                             for n,ki,t in zip(deg,k,z))
                  for k,c in coefficients.items())
    zero(p.as_expr()-rebuilt, 'Bernstein reconstruction')
    check(all(c>0 for c in coefficients.values()), 'positive Bernstein coefficients')
    return {
        'degree': list(deg),
        'minimum': str(min(coefficients.values())),
        'coefficients': [{'index':list(k),'value':str(c)} for k,c in coefficients.items()]
    }

# Closed rational intervals. Every operation encloses its exact operand.
class RI:
    def __init__(self,lo,hi=None):
        self.lo=F(lo); self.hi=F(lo if hi is None else hi)
        check(self.lo<=self.hi,'ordered interval')
    def __add__(self,other):
        o=as_ri(other); return RI(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self): return RI(-self.hi,-self.lo)
    def __sub__(self,other): return self+-as_ri(other)
    def __rsub__(self,other): return as_ri(other)+-self
    def __mul__(self,other):
        o=as_ri(other); v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return RI(min(v),max(v))
    __rmul__=__mul__
    def reciprocal(self):
        check(self.lo>0 or self.hi<0,'reciprocal excludes zero')
        return RI(1/self.hi,1/self.lo)
    def __truediv__(self,other): return self*as_ri(other).reciprocal()
    def __rtruediv__(self,other): return as_ri(other)*self.reciprocal()

def as_ri(x): return x if isinstance(x,RI) else RI(x)

def sqrt_fraction_bounds(x, digits=32):
    x=F(x); check(x>=0,'nonnegative square root')
    scale=10**digits
    n=isqrt((x.numerator*scale**2)//x.denominator)
    lo=F(n,scale)
    hi=lo if n*n*x.denominator==x.numerator*scale**2 else F(n+1,scale)
    check(lo*lo<=x<=hi*hi,'rational sqrt bracket')
    return RI(lo,hi)

def sqrt_ri(x):
    x=as_ri(x)
    return RI(sqrt_fraction_bounds(x.lo).lo,sqrt_fraction_bounds(x.hi).hi)

def atan_series_bracket(x, pairs=48):
    x=F(x); check(0<=x<=1,'atan series range')
    total=F(0); power=x; xx=x*x
    for j in range(2*pairs):
        total += (power if j%2==0 else -power)/(2*j+1)
        power *= xx
    # Alternating series: even partial sum is lower; next odd sum is upper.
    return RI(total,total+power/(4*pairs+1))

PI = 16*atan_series_bracket(F(1,5))-4*atan_series_bracket(F(1,239))
check(F(3)<PI.lo<PI.hi<F(22,7),'Machin pi bracket')

def normalized_positive_part(k):
    """Enclose integral_0^pi (cos(phi)^2-k)_+ dphi, for rational k>=0."""
    k=F(k); check(k>=0,'nonnegative k')
    if k>=1: return RI(0)
    if k==0: return PI/2
    if k>=F(1,2):
        z=sqrt_fraction_bounds((1-k)/k)
        alpha=RI(atan_series_bracket(z.lo).lo,atan_series_bracket(min(z.hi,F(1))).hi)
    else:
        z=sqrt_fraction_bounds(k/(1-k))
        small=RI(atan_series_bracket(z.lo).lo,atan_series_bracket(min(z.hi,F(1))).hi)
        alpha=PI/2-small
    result=(1-2*k)*alpha+sqrt_fraction_bounds(k*(1-k))
    return RI(max(F(0),result.lo),max(F(0),result.hi))

def positive_part_parameter_box(Mlo,Mhi,Clo,Chi):
    """Clo<=C<=Chi<0, 0<Mlo<=M<=Mhi; uses monotonicity in k."""
    Mlo,Mhi,Clo,Chi=map(F,(Mlo,Mhi,Clo,Chi))
    check(0<Mlo<=Mhi and Clo<=Chi<0,'positive-part input box')
    klo=-Chi/Mhi; khi=-Clo/Mlo
    return RI(Mlo*normalized_positive_part(khi).lo,
              Mhi*normalized_positive_part(klo).hi)

def rational_beta_at(lam,tau,x):
    """Certified beta interval at a rational point with B<=0."""
    lam,tau,x=map(F,(lam,tau,x))
    mm=2*tau/(1+tau*tau); rho=(1-tau*tau)/(1+tau*tau); LL=lam*lam
    aa=1-x*x; MM=mm*aa
    CC=(LL-1)*x**3-LL*mm*x*x+(2-LL)*x-mm*(1-LL)
    BB=mm*(1-LL)*x*x+((1+LL)*mm*mm+LL-2)*x-LL*mm
    check(BB<=0 and CC<0,'point lies in B<=0,C<0 cell')
    dd=aa+rho*rho+LL*(mm-x)**2
    a=sqrt_fraction_bounds(aa)
    dp=dd+2*rho*a; dm=dd-2*rho*a
    check(dm.lo>0,'positive distance denominator')
    wmin=2/(dp*sqrt_ri(dp)); wmax=2/(dm*sqrt_ri(dm))
    eplus=MM*normalized_positive_part(-CC/MM)
    eminus=eplus-PI*(MM/2+CC)
    good=wmin*eminus
    loss_R=(PI/2)*wmax*eplus
    loss_sec=(PI/10)*wmax
    beta=good-loss_R-loss_sec
    return beta,{'favorable':good,'E_positive_loss':loss_R,'secant_loss':loss_sec}

def decimal_rational_enclosure(x, digits=8):
    n=10**digits
    lo=F((x.lo.numerator*n)//x.lo.denominator,n)
    hi=F(-((-x.hi.numerator*n)//x.hi.denominator),n)
    return [str(lo),str(hi)]

def run_exact():
    # Algebra used by the completed secant estimate.
    zero(cstar-(h-d),'cstar=h-d')
    zero(B-m*cstar-r*T,'B=mcstar+rT')
    zero(C+h*T-mu*(L-1)*s**2,'C+hT identity')
    q,theta=S.symbols('q theta',real=True)
    E=m*q+C; Y=h*cstar+r*q; Z=T-m*q/h+theta*E
    zero(B+theta*r*E-m*Y/h-r*Z,'K_R/S3 correlated identity')
    y,z,alpha,rv=S.symbols('y z alpha rv')
    zero(y*(alpha*y+rv*z)-alpha*(y+rv*z/(2*alpha))**2+rv**2*z**2/(4*alpha),'secant square completion')
    zero(S.diff(C,L)-s*a2,'C L derivative')
    zero(S.diff(C,m)+L*mu**2+1-L,'C m derivative')
    zero(d-(2-(1-2*L)*m**2/(1-L)-(1-L)*(mu+L*m/(1-L))**2),'distance square completion')
    check(Lhi<Q(2,9) and mlo**2>Q(49,50),'distance upper-bound premises')
    check(Q(2)-Q(5,7)*Q(49,50)==Q(13,10),'distance upper bound')
    check(d.subs({L:Llo,m:1,mu:Q(3,5)})==Q(416,625),'distance lower endpoint')
    check(d.subs({L:Llo,m:1,mu:Q(-1,4)})==Q(19,16),'distance other endpoint')
    distance_ratio=4*RMAX/Q(416,625)**2
    check(distance_ratio==Q(87890625,552438016)<Q(23,144),'v/d>11/12')
    check(Q(840,299)>Q(14,5),'theta lower bound')
    t=S.symbols('t')
    psi=2*(2+t)/((1+t)*(2-t))
    zero(S.diff(psi,t)-2*t*(t+4)/((1+t)**2*(2-t)**2),'theta monotonicity')
    zero(3*(1+t)*(2-t)-2*(2+t)-(1-t)*(2+3*t),'theta upper bound')
    check(Q(23,25)-Q(11,5)*Lhi==Q(88861,200000)>Q(2,5),'C monotonicity premise')
    check(Q(-369,32)>-12 and Q(479,80)<12,'Z bound arithmetic')
    check(Q(28125,395839)<Q(1,14),'M>(13/14)hu')
    secant=Q(7*144,13)*RMAX**2/mlo/Q(3,5)/Q(3,2)
    check(secant==Q(506250,18757661)<Q(27,1000)<Q(3,100),'secant upper coefficient')

    # Uniform beta counterexample at mu=1/4, without evaluating inverse trig.
    avg=m*a2/2+C
    zero(S.diff(avg,m)+Q(1,2)-L+(L+Q(1,2))*mu**2,'mean m derivative')
    check(avg.subs({L:Llo,m:1,mu:Q(1,4)})==Q(21,320),'uniform mean minimum at mu=1/4')
    check(Q(21,320)+Q(1,10)==Q(53,320),'uniform beta negative margin')

    # A short interval where the original beta itself is positive.
    check(g.subs({L:Lhi,m:1,mu:Q(-1,8)})==Q(-496017,20480000)<0,'short interval E<=0')
    check((-C-m*a2/2).subs({L:Lhi,m:mlo,mu:Q(-1,8)})==Q(1189049017,2314240000)>Q(1,2),'short negative mean')
    check(B.subs({L:Llo,m:mlo,mu:Q(-1,4)})==Q(43773,638450)<Q(7,100),'short B positive bound')
    check(d.subs({L:Llo,m:1,mu:Q(-1,8)})==Q(1899,1600)>Q(59,50)>Q(7,6),'short distance bound')
    check(Q(8167,5167)**3<4,'short weight ratio <2')
    check(Q(400,81)>Q(8,5)**3,'wmin>9/10')
    check(Q(1,2)-2*(Q(9,100)*Q(11,7)+Q(1,10))==Q(3,175),'short beta bracket')
    check(3*Q(9,10)*Q(3,175)==Q(81,1750),'short beta rational lower')
    check(Q(4,25)*(mlo+Q(1,8))==Q(1009,5650)>Q(7,40),'short exterior coefficient')
    check(Q(81,1750)*Q(7,40)*Q(1,8)==Q(81,80000)>Q(1,1000),'short beta mass')

    # Complete polynomial certificates for the alternative proof on ALL of J.
    certificates={}
    for t0 in [Q(3),Q(14,5)]:
        poly=-(g+Q(3,100)*a2)*d-t0*B*a2
        certificates[str(t0)]=bernstein_certificate(poly)
    check(certificates['3']['minimum']==str(Q(106592,1953125)),'Pi_3 minimum')
    check(certificates['14/5']['minimum']==str(Q(40192,1953125)),'Pi_14/5 minimum')
    check(Q(40192,1953125)>Q(39,2000),'endpoint gap > (3/200)*(13/10)')

    # Exact integration of the proven pointwise lower bound.
    Cmax=C.subs({L:Lhi,m:mlo})
    check(Cmax.subs(mu,Q(2,5))==Q(-41747957,282500000)<0,'2/5<mu_C uniformly')
    integral=S.integrate((mlo-mu)*(-Cmax+Q(3,200)),(mu,Q(-1,4),Q(2,5)))
    core_lower=Q(3,10)*integral
    check(core_lower==Q(10778024217619399,81721600000000000)>Q(1,8),'direct core mass >1/8')
    check(Q(4,25)*(mlo-Q(2,5))==Q(1336,14125)>Q(884,14125),'correct stronger exterior coefficient')
    check(Q(207,5000)+Q(1,8)==Q(104,625),'remaining global budget')
    check(1+Q(75,16)*Q(5,4)==Q(439,64),'W-16 correction')
    check(Q(11,7)*Q(439,64)+Q(1,10)<11,'corrected coarse f<11')

    # Additional exact counterexample close to mu=0.
    beta0,terms0=rational_beta_at(F(93,200),F(7,8),F(0))
    beta_small,_=rational_beta_at(F(93,200),F(7,8),F(1,8192))
    check(beta0.lo>0,'beta at zero is positive at the selected parameter point')
    check(beta_small.hi<0,'beta at mu=1/8192 is negative at the selected parameter point')
    check(normalized_positive_part(F(1)).lo==0,'k=1 case')
    check(normalized_positive_part(F(2)).hi==0,'k>1 case')
    check(normalized_positive_part(F(1,2)).lo==F(1,2)==normalized_positive_part(F(1,2)).hi,'k=1/2 exact angular integral')
    angular_examples=[]
    cuts=[F(-1,4),F(-1,8),F(0),F(1,8),F(1,4),F(2,5)]
    def sf(x):
        x=S.Rational(x); return F(int(x.p),int(x.q))
    for left,right in zip(cuts,cuts[1:]):
        max_square=max(left*left,right*right)
        min_square=F(0) if left<=0<=right else min(left*left,right*right)
        Mlo=F(112,113)*(1-max_square); Mhi=1-min_square
        Clo=sf(C.subs({L:Llo,m:1,mu:Q(left.numerator,left.denominator)}))
        Chi=sf(C.subs({L:Lhi,m:mlo,mu:Q(right.numerator,right.denominator)}))
        box_value=positive_part_parameter_box(Mlo,Mhi,Clo,Chi)
        angular_examples.append({'mu':[str(left),str(right)],'M':[str(Mlo),str(Mhi)],
            'C':[str(Clo),str(Chi)],'k':[str(-Chi/Mhi),str(-Clo/Mlo)],
            'E_positive_integral':decimal_rational_enclosure(box_value,6)})
    record={
        'status':'EXACT ALGEBRA CHECKS PASS / ANALYTIC PROOF IN REPORT / NOT CANONICAL CERTIFICATION',
        'box':[[str(a),str(b)] for a,b in BOX],
        'variables':['L','m','mu'],
        'polynomial_definition':'Pi_t = -(g+(3/100)*a2)*d - t*B*a2',
        'Bernstein':certificates,
        'secant_coefficient_upper':str(secant),
        'original_beta_short_interval':['-1/4','-1/8'],
        'original_beta_mass_lower':'1/1000',
        'direct_core_interval':['-1/4','2/5'],
        'direct_core_rational_lower_before_simplification':str(core_lower),
        'direct_core_mass_lower':'1/8',
        'south_remainder_one_sided_loss':'0 (new proof; audit required)',
        'north_plus_near_required_upper':'104/625 (strict)',
        'point_intervals':{
            'lambda=93/200,tau=7/8,mu=0':decimal_rational_enclosure(beta0),
            'lambda=93/200,tau=7/8,mu=1/8192':decimal_rational_enclosure(beta_small),
            'terms_at_mu=0':{k:decimal_rational_enclosure(v) for k,v in terms0.items()}
        },
        'angular_box_examples':angular_examples,
        'canonical_status':'D-P2 NOT_CERTIFIED (unchanged)',
        'unproved':['useful uniform U_north','useful uniform U_near','positive final global gap']
    }
    print('EXACT ALGEBRA CHECKS: PASS')
    print('SymPy:',S.__version__)
    for t0,c in certificates.items():
        print('Pi_'+t0+': degree',c['degree'],'coefficients',len(c['coefficients']),'minimum',c['minimum'])
    print('beta(0) interval:',record['point_intervals']['lambda=93/200,tau=7/8,mu=0'])
    print('beta(1/8192) interval:',record['point_intervals']['lambda=93/200,tau=7/8,mu=1/8192'])
    print('Original beta positive on [-1/4,-1/8]; mass >1/1000.')
    print('Alternative analytic proof: G>0 on J; core mass >1/8.')
    print('Remaining required budget: U_north+U_near <104/625; UNPROVED.')
    return record

def diagnostic():
    import math
    for lam in [0.4,0.465]:
        for tau in [0.875,1.0]:
            for x in [-0.25,-0.125,-0.0625,0.0,1/8192,0.125,0.25,0.375,0.4]:
                mm=2*tau/(1+tau*tau); rr=(1-tau*tau)/(1+tau*tau); ll=lam*lam
                aa=1-x*x; mmass=mm*aa
                cc=(ll-1)*x**3-ll*mm*x*x+(2-ll)*x-mm*(1-ll)
                k=-cc/mmass
                alpha=math.acos(math.sqrt(k)) if 0<k<1 else 0.0
                plus=mmass*((1-2*k)*alpha+math.sqrt(k*(1-k))) if 0<k<1 else 0.0
                minus=plus-math.pi*(mmass/2+cc)
                dd=aa+rr*rr+ll*(mm-x)**2
                low=2/(dd+2*rr*math.sqrt(aa))**1.5
                high=2/(dd-2*rr*math.sqrt(aa))**1.5
                bb=mm*(1-ll)*x*x+((1+ll)*mm*mm+ll-2)*x-ll*mm
                bcost=0.0
                if bb>0:
                    total=0.0; n=400
                    for i in range(n+1):
                        q=aa*math.cos(math.pi*i/n)**2
                        v=math.sqrt(dd*dd-4*rr*rr*q)
                        th=2*(2*dd+v)/((dd+v)*(2*dd-v))
                        total+=(1 if i in (0,n) else 4 if i%2 else 2)*th*bb*q
                    bcost=total*math.pi/(3*n)
                beta=low*minus-math.pi/2*high*(plus+bcost)-math.pi/10*high
                print('DIAGNOSTIC / NOT_EVIDENCE',lam,tau,x,beta)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--diagnostic',action='store_true')
    parser.add_argument('--write-certificate')
    args=parser.parse_args()
    if args.diagnostic:
        diagnostic()
    else:
        record=run_exact()
        if args.write_certificate:
            Path(args.write_certificate).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
