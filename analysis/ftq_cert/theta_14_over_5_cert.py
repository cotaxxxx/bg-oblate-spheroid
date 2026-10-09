"""Exact rational Bernstein certificate: theta * d > 14/5 on the FT_q south box (auxiliary to C1 of
Astra's certificate-39' report; independent route, not the report's own proof).

Notation: L = lambda^2, r = 1 - m^2, a^2 = 1 - mu^2, s = m - mu, d = a^2 + r + L s^2, e = 4 r a^2,
v^2 = d^2 - 4 r q >= d^2 - e  (0 <= q <= a^2),  theta = 4 L_D / S3 = 2 (2d + v) / ((d + v)(2d - v)).
Box: L in [4/25, 8649/40000], m in [112/113, 1], mu in [-1/4, 3/5].

Claim: theta d > 14/5 on the box.
Proof: theta d > 14/5  <=>  7 v^2 - 2 d v - 4 d^2 > 0  <=  v > (1 + sqrt 29)/7 * d  <=  v >= c d with the
rational c = 913/1000 > (1 + sqrt 29)/7 (checked exactly: 7c > 1 and (7c - 1)^2 > 29)  <=  v^2 >= c^2 d^2
<=  (1 - c^2) d^2 - e > 0.  The last polynomial in (L, m, mu) has all tensor-Bernstein coefficients
positive on the box (degree (2, 4, 4); exact Fractions only, no floating point), which proves it.

Expected output (sympy 1.14.0, Python 3.11):
  c=913/1000 exceeds (1+sqrt29)/7: True
  (1-c^2) d^2 - e: degree (2, 4, 4), 75 coefficients, min = 2058768436330482951/63690375390625000000
  CERTIFIED: theta*d > 14/5 on the box
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
import sympy as sp

L, m, mu = sp.symbols('L m mu')
r = 1 - m**2
a2 = 1 - mu**2
d = a2 + r + L*(m - mu)**2
e = 4*r*a2


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
    return degs, res


c = Q(913, 1000)
ok_c = 7*c > 1 and (7*c - 1)**2 > 29
print(f"c=913/1000 exceeds (1+sqrt29)/7: {ok_c}")
box = [(L, Q(4, 25), Q(8649, 40000)), (m, Q(112, 113), Q(1)), (mu, Q(-1, 4), Q(3, 5))]
degs, res = bern(sp.expand((1 - c*c)*d**2 - e), box)
mn = min(res.values())
print(f"(1-c^2) d^2 - e: degree {tuple(degs)}, {len(res)} coefficients, min = {mn}")
print("CERTIFIED: theta*d > 14/5 on the box" if ok_c and mn > 0 else "FAILED")
