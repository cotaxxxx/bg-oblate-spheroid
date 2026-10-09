"""Exact rational Bernstein certificates: A < 0 on the exterior south J = (-1/4, mu_C).

Notation (FT_q P-decomposition, certificate-39' request): L = lambda^2, rho^2 = 1 - m^2, a^2 = 1 - mu^2,
d = a^2 + rho^2 + L (m-mu)^2, e = 4 rho^2 a^2,  A = S3 (E + theta B1 q),  theta = 4 L_D / S3 = 2 f(v),
f(v) = (2d+v)/((d+v)(2d-v)) increasing in v,  v^2 = d^2 - 4 rho^2 q >= d^2 - e,
v >= v_lo := (d^2 - e)/d  (sqrt(x) >= x/d for 0 <= x <= d^2),  theta >= theta_lo = 2 d (3d^2-e)/((2d^2-e)(d^2+e)).
Box: L in [4/25, 8649/40000], m in [112/113, 1].

Certificates (each: all Bernstein coefficients of the stated polynomial positive on the stated box):
 C1  mu in [-1/4,-1/8]:  -g > 0  and  G1 := (-g)(a^2 + L s^2) - 3 B1 a^2 > 0       (B1 > 0 branch, as for K)
 C2  mu in [-1/4, 1/2]:  -T* > 0,  T* := (a^2 m + C0)(2d^2-e)(d^2+e) + 2 a^2 B1 d (3d^2-e)   (= T (2d^2-e)(d^2+e))
 C3  mu in [1/2, 3/5]:   -M* > 0,  M* := m (2d^2-e)(d^2+e) + 2 B1 d (3d^2-e)                (= (m+theta_lo B1)(...))
 C4  -C0(mu=1/2) > 0 and C0(mu=3/5) > 0 on the (L,m) box  => 1/2 < mu_C < 3/5.
 Auxiliary positivity of the denominators: d^2 - e > 0 on mu in [-1/4, 3/5] (then 2d^2-e>0, d^2+e>0).
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
import sympy as sp

L, m, mu = sp.symbols('L m mu')
r2 = 1 - m**2
a2 = 1 - mu**2
d = a2 + r2 + L*(m - mu)**2
e = 4*r2*a2
B1 = m*(1-L)*mu**2 + ((1+L)*m**2 + L - 2)*mu - L*m
C0 = (L-1)*mu**3 - L*m*mu**2 + (2-L)*mu - m*(1-L)
g = m*a2 + C0


def bern(expr, box):
    ts = sp.symbols('t0:%d' % len(box))
    sub = {v: sp.Rational(lo.numerator, lo.denominator) + sp.Rational((hi-lo).numerator, (hi-lo).denominator)*t
           for (v, lo, hi), t in zip(box, ts)}
    P = sp.Poly(sp.expand(expr.subs(sub)), *ts)
    degs = P.degree_list()
    a = {k: Q(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for k, c in zip(P.monoms(), P.coeffs())}
    res = {}
    for idx in product(*[range(dd+1) for dd in degs]):
        s = Q(0)
        for k, c in a.items():
            if all(ki <= ii for ki, ii in zip(k, idx)):
                w = Q(1)
                for ki, ii, dd in zip(k, idx, degs):
                    w *= Q(comb(ii, ki), comb(dd, ki))
                s += w*c
        res[idx] = s
    return min(res.values()), len(res)


def certify(name, expr, mlo, mhi, max_split=64):
    LB = (L, Q(4, 25), Q(8649, 40000))
    pieces = [(mlo, mhi, Q(112, 113), Q(1))]
    ok = []; n = 0
    while pieces:
        a_, b_, m0, m1 = pieces.pop()
        mn, nc = bern(expr, [LB, (m, m0, m1), (mu, a_, b_)])
        n += 1
        if mn > 0:
            ok.append((a_, b_, m0, m1, mn))
        elif n > max_split:
            print(f"{name}: FAILED to certify (piece mu[{a_},{b_}] m[{m0},{m1}] min coeff {float(mn):.4g})"); return False
        else:
            c = (a_+b_)/2
            pieces += [(a_, c, m0, m1), (c, b_, m0, m1)]
    mn = min(x[4] for x in ok)
    print(f"{name}: CERTIFIED on mu in [{mlo},{mhi}] with {len(ok)} mu-pieces; min Bernstein coefficient {mn} (~{float(mn):.4g})")
    return True


allok = True
allok &= certify("C1a  -g", -g, Q(-1, 4), Q(-1, 8))
allok &= certify("C1b  G1", sp.expand(-g*(a2 + L*(m-mu)**2) - 3*B1*a2), Q(-1, 4), Q(-1, 8))
allok &= certify("AUX  d^2-e", sp.expand(d**2 - e), Q(-1, 4), Q(3, 5))
allok &= certify("C2  -T*", sp.expand(-((a2*m + C0)*(2*d**2 - e)*(d**2 + e) + 2*a2*B1*d*(3*d**2 - e))), Q(-1, 4), Q(1, 2))
allok &= certify("C3  -M*", sp.expand(-(m*(2*d**2 - e)*(d**2 + e) + 2*B1*d*(3*d**2 - e))), Q(1, 2), Q(3, 5))
for nm, ex in (("C4a -C0(1/2)", -C0.subs(mu, sp.Rational(1, 2))), ("C4b  C0(3/5)", C0.subs(mu, sp.Rational(3, 5)))):
    mn, _ = bern(sp.expand(ex + 0*mu), [(L, Q(4, 25), Q(8649, 40000)), (m, Q(112, 113), Q(1)), (mu, Q(0), Q(1))])
    print(f"{nm}: min Bernstein coefficient {mn} (~{float(mn):.4g}) -> {'CERTIFIED' if mn > 0 else 'FAILED'}")
    allok &= mn > 0
print("ALL CERTIFICATES PASS" if allok else "SOME CERTIFICATE FAILED")
