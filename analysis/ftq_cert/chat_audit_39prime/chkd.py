import sympy as sp
from math import comb
from itertools import product
L,m,mu=sp.symbols('L m mu'); R=sp.Rational
a2=1-mu**2; r=1-m**2; s=m-mu; d=a2+r+L*s**2
C0=(L-1)*mu**3-L*m*mu**2+(2-L)*mu-m*(1-L)
def bern_min(expr,box):
    z=sp.symbols('z0:3'); sub={v:lo+(hi-lo)*t for v,t,(lo,hi) in zip((L,m,mu),z,box)}
    p=sp.Poly(sp.expand(expr.subs(sub,simultaneous=True)),*z); n=p.degree_list()
    cs=[sum(c*sp.prod([R(comb(k[i],j[i]),comb(n[i],j[i])) for i in range(3)]) for j,c in p.terms() if all(j[i]<=k[i] for i in range(3))) for k in product(*(range(x+1) for x in n))]
    return min(cs)
J=[(R(4,25),R(8649,40000)),(R(112,113),1),(R(-1,4),R(3,5))]
print('J: min Bernstein of d-416/625 =',bern_min(d-R(416,625),J), ' (>=0 needed; =0 allowed at the attained corner)')
print('J: min Bernstein of 13/10-d =',bern_min(R(13,10)-d,J))
print('d at (4/25,1,3/5) =',d.subs({L:R(4,25),m:1,mu:R(3,5)}))
# core integral and S''_lb recomputation
Cs=C0.subs({L:R(8649,40000),m:R(112,113)})
core=R(3,10)*sp.integrate((R(112,113)-mu)*(-Cs+R(3,200)),(mu,R(-1,4),R(2,5)))
Slb=R(3,10)*sp.integrate((R(112,113)-mu)*(-Cs+R(3,200)),(mu,-1,R(1,2)))
print('core =',core,'>1/8:',core>R(1,8)); print("S''_lb recomputed =",Slb,'matches:',Slb==R(635530452759,817216000000))
print('C0* at 1/2 =',Cs.subs(mu,R(1,2)),' C0* at 2/5 =',Cs.subs(mu,R(2,5)))
