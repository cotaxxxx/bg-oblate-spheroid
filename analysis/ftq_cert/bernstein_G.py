"""Exact rational Bernstein certificate for question 1 (FT_q, south kernel K).

Claim checked: for all L=lambda^2 in [4/25, 8649/40000], m in [112/113, 1], mu in [-1, -1/4],
    G := (-g)(1 - mu^2 + L (m - mu)^2) - 3 B1 (1 - mu^2) > 0,
with g = m(1-mu^2) + C0 and B1, C0 exactly as in FT_q P-decomposition (6.4), (6.5).

Method: the polynomial is rewritten in Bernstein form on each sub-box (exact Fractions only);
if every Bernstein coefficient on a sub-box is > 0 then G > 0 on that closed sub-box
(range-enclosing property: G is a convex combination of its Bernstein coefficients).
Sub-boxes are produced by bisecting mu only, until all coefficients are positive.
No floating point is used anywhere.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
import sympy as sp

L, m, mu = sp.symbols('L m mu')
B1 = L*m**2*mu - L*m*mu**2 - L*m + L*mu + m**2*mu + m*mu**2 - 2*mu
C0 = -L*m*mu**2 + L*m + L*mu**3 - L*mu - m - mu**3 + 2*mu
g = m*(1 - mu**2) + C0
G = sp.expand(-g*(1 - mu**2 + L*(m - mu)**2) - 3*B1*(1 - mu**2))


def bernstein_coeffs(expr, box):
    """box: [(var, lo, hi), ...] with Fraction ends. Returns dict of Bernstein coefficients."""
    ts = sp.symbols('t0:%d' % len(box))
    sub = {v: sp.Rational(lo.numerator, lo.denominator) + sp.Rational((hi-lo).numerator, (hi-lo).denominator)*t
           for (v, lo, hi), t in zip(box, ts)}
    P = sp.Poly(sp.expand(expr.subs(sub)), *ts)
    degs = P.degree_list()
    a = {k: Q(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for k, c in zip(P.monoms(), P.coeffs())}
    out = {}
    for idx in product(*[range(d+1) for d in degs]):
        s = Q(0)
        for k, c in a.items():
            if all(ki <= ii for ki, ii in zip(k, idx)):
                w = Q(1)
                for ki, ii, d in zip(k, idx, degs):
                    w *= Q(comb(ii, ki), comb(d, ki))
                s += w*c
        out[idx] = s
    return out


Lbox = (L, Q(4, 25), Q(8649, 40000))
mbox = (m, Q(112, 113), Q(1))
pieces = [(Q(-1), Q(-1, 4))]
done = []
while pieces:
    a, b = pieces.pop()
    bc = bernstein_coeffs(G, [Lbox, mbox, (mu, a, b)])
    mn = min(bc.values())
    if mn > 0:
        done.append((a, b, mn))
    else:
        c = (a+b)/2
        pieces += [(a, c), (c, b)]
done.sort()
for a, b, mn in done:
    print(f"mu in [{a}, {b}]: min Bernstein coefficient = {mn} (~{float(mn):.6f}) > 0")
print(f"CERTIFIED: G > 0 on the full box ({len(done)} mu-pieces), min coefficient {min(x[2] for x in done)}")
