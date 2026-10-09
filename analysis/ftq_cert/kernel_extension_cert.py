"""Exact rational certificates: extension of the certificate-39' south sign lemma to the kernel K = [-1, -1/4].

Lemma (to be audited):  -F/S3 >= (-C0) sin^2 phi + (3/200) cos^2 phi  on mu in K, all parameters.
Combined with the audited exterior-south lemma (39' C4) this holds on [-1, mu_C), and then
    int_{-1}^{1/2} G(mu) dmu  >  (3/10) int_{-1}^{1/2} (112/113 - mu)(-C0*(mu) + 3/200) dmu  =  635530452759/817216000000,
which is a lower bound for the WHOLE interval [-1, 1/2] and replaces (is not added to) the earlier S_K >= 207/5000 and
C_core >= 1/8 (sum 104/625).
C0* = C0 at (L, m) = (8649/40000, 112/113) (C0 is decreasing in m and increasing in L, dC0/dm = -(L mu^2 + 1 - L),
dC0/dL = (m - mu)(1 - mu^2)), pi >= 3, S3/v^3 >= 2 d^{-3/2} > 5/4 (d < 13/10), lambda^2 s / w >= (4/25)(112/113 - mu).

Box K: L in [4/25, 8649/40000], m in [112/113, 1], mu in [-1, -1/4].  Notation as in bernstein_south_A.py and 39' C1-C4:
r = 1 - m^2, a^2 = 1 - mu^2, s = m - mu, h = 1 - m mu, d = a^2 + r + L s^2, e = 4 r a^2, v^2 = d^2 - 4 r q >= d^2 - e,
u^2 = 2(d + v), theta = 2(2d + v)/((d + v)(2d - v)), T = (1 - L) m - (2 - L) mu, eps = 3/100, eta = 3/200.

Conditions re-proved on K (none imported from the J box):
 (1) Pi_3 > 0 and Pi_{14/5} > 0 on K, Pi_t = -(g + eps a^2) d - t B1 a^2, g = m a^2 + C0   [Bernstein]
 (2) theta d > 14/5 on K: (1 - c^2) d^2 - e > 0 with c = 913/1000 > (1 + sqrt 29)/7      [Bernstein]
     theta d <= 3 always (v <= d).
 (3) secant: J_sec <= 7 q r^2 Z^2 / (13 m v u) <= eps q, using on K:
     d >= 16/25, d^2 - e >= 256/625 (v >= 16/25, u >= 8/5), h >= 141/113, a^2 <= 15/16,
     T in [T_lo, 67/25], C0 >= C0_lo, E <= g < 0, theta E in [3 C0_lo / (16/25), 0),  and 4 r q/(h u^2) < 1/14.
 (4) Pi_t / d > eta on K:  Pi_min > eta * 13/10, with d < 13/10 from d = 2 - (1-2L) m^2/(1-L) - (1-L)(mu + L m/(1-L))^2.
All arithmetic is exact (Fractions / sympy rationals).  No floating point enters any assertion.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
import sympy as sp

L, m, mu = sp.symbols('L m mu')
r = 1 - m**2; a2 = 1 - mu**2; s = m - mu; h = 1 - m*mu
d = a2 + r + L*s**2; e = 4*r*a2
B1 = m*(1-L)*mu**2 + ((1+L)*m**2 + L - 2)*mu - L*m
C0 = (L-1)*mu**3 - L*m*mu**2 + (2-L)*mu - m*(1-L)
g = m*a2 + C0
T = (1-L)*m - (2-L)*mu
K = [(L, Q(4, 25), Q(8649, 40000)), (m, Q(112, 113), Q(1)), (mu, Q(-1), Q(-1, 4))]
EPS, ETA = Q(3, 100), Q(3, 200)


def bern(expr, box):
    ts = sp.symbols('t0:%d' % len(box))
    sub = {v: sp.Rational(lo.numerator, lo.denominator) + sp.Rational((hi-lo).numerator, (hi-lo).denominator)*t
           for (v, lo, hi), t in zip(box, ts)}
    P = sp.Poly(sp.expand(expr.subs(sub)), *ts)
    degs = P.degree_list()
    a = {k: Q(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for k, c in zip(P.monoms(), P.coeffs())}
    mn = mx = None
    for idx in product(*[range(dd+1) for dd in degs]):
        sm = Q(0)
        for k, c in a.items():
            if all(ki <= ii for ki, ii in zip(k, idx)):
                w = Q(1)
                for ki, ii, dd in zip(k, idx, degs):
                    w *= Q(comb(ii, ki), comb(dd, ki))
                sm += w*c
        mn = sm if mn is None else min(mn, sm); mx = sm if mx is None else max(mx, sm)
    return mn, mx


ok = True
def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(f"{name}: {'PASS' if cond else 'FAIL'} {detail}")


# (1) Pi_t positivity
pi_min = {}
for t in (sp.Integer(3), sp.Rational(14, 5)):
    mn, _ = bern(sp.expand(-(g + EPS*a2)*d - t*B1*a2), K); pi_min[t] = mn
    check(f"(1) Pi_{t} > 0 on K", mn > 0, f"min Bernstein coeff = {mn}")
# (2) theta bounds
c = Q(913, 1000)
check("(2a) c=913/1000 > (1+sqrt29)/7", 7*c > 1 and (7*c-1)**2 > 29)
mn, _ = bern(sp.expand((1-c*c)*d**2 - e), K)
check("(2b) (1-c^2)d^2 - e > 0 on K  (=> theta d > 14/5)", mn > 0, f"min coeff = {mn}")
# auxiliary ranges on K
mn_d, _ = bern(sp.expand(d), K); check("(3a) d >= 16/25 on K", mn_d >= Q(16, 25), f"Bernstein lower bound = {mn_d}")
mn_v2, _ = bern(sp.expand(d**2 - e), K); check("(3b) d^2 - e >= 256/625 on K (v >= 16/25, u^2 = 2(d+v) >= 64/25)", mn_v2 >= Q(256, 625), f"lower bound = {mn_v2}")
mn_h, _ = bern(sp.expand(h), K); check("(3c) h >= 141/113 on K", mn_h >= Q(141, 113), f"lower bound = {mn_h}")
_, mx_a2 = bern(sp.expand(a2), K); check("(3d) a^2 <= 15/16 on K", mx_a2 <= Q(15, 16), f"upper bound = {mx_a2}")
mn_T, mx_T = bern(sp.expand(T), K); check("(3e) T range on K", True, f"[{mn_T}, {mx_T}]")
mn_C0, mx_C0 = bern(sp.expand(C0), K); check("(3f) C0 range on K (C0 < 0)", mx_C0 < 0, f"[{mn_C0}, {mx_C0}]")
_, mx_g = bern(sp.expand(g), K); check("(3g) E <= g < 0 on K", mx_g < 0, f"g upper bound = {mx_g}")
# secant coefficient on K
v_lo, u_lo, d_lo, h_lo = Q(16, 25), Q(8, 5), Q(16, 25), Q(141, 113)
r_hi, m_lo = Q(225, 12769), Q(112, 113)
mq_h_hi = mx_a2/h_lo                       # 0 <= m q/h <= a^2/h
thE_lo = 3*mn_C0/d_lo                      # theta E in [3 C0_lo/d_lo, 0): theta <= 3/d, E >= C0 >= C0_lo, E < 0
Z_lo = mn_T - mq_h_hi + thE_lo; Z_hi = mx_T
Zabs = max(abs(Z_lo), abs(Z_hi))
check("(3h) 4 r q/(h u^2) < 1/14 on K (=> M > 13/14 h u)", 4*r_hi*mx_a2/(h_lo*u_lo**2) < Q(1, 14), f"bound = {4*r_hi*mx_a2/(h_lo*u_lo**2)}")
coef = 7*Zabs**2*r_hi**2/(13*m_lo*v_lo*u_lo)
check("(3i) secant coefficient 7 Z^2 r^2/(13 m v u) <= eps = 3/100 on K", coef <= EPS, f"|Z| <= {Zabs} (~{float(Zabs):.3f}), coefficient = {coef} (~{float(coef):.5f})")
# (4) Pi_t/d > eta with d < 13/10 (mu-independent bound from completing the square; identity checked)
ident = sp.simplify(d - (2 - (1-2*L)/(1-L)*m**2 - (1-L)*(mu + L*m/(1-L))**2)) == 0
Lh, ml = Q(8649, 40000), Q(112, 113)
d_hi = 2 - (1-2*Lh)/(1-Lh)*ml**2          # (1-2L)/(1-L) decreasing in L; m^2 >= (112/113)^2
check("(4a) completing-the-square identity for d", ident)
check("(4b) d < 13/10 on K", d_hi < Q(13, 10), f"d <= {d_hi} (~{float(d_hi):.5f})")
check("(4c) Pi_t/d > eta on K for both t", min(pi_min.values()) > ETA*Q(13, 10), f"Pi_min = {min(pi_min.values())} > eta*13/10 = {ETA*Q(13,10)}")
# (5) integral lower bound on [-1, 1/2] with pi >= 3
check("(5a) dC0/dm < 0, dC0/dL >= 0 (C0 max at L=8649/40000, m=112/113)",
      sp.simplify(sp.diff(C0, m) + (L*mu**2 + 1 - L)) == 0 and sp.simplify(sp.diff(C0, L) - (m-mu)*(1-mu**2)) == 0)
C0s = C0.subs({L: sp.Rational(8649, 40000), m: sp.Rational(112, 113)})
I = sp.integrate((sp.Rational(112, 113) - mu)*(-C0s + sp.Rational(3, 200)), (mu, -1, sp.Rational(1, 2)))
I = Q(int(sp.fraction(I)[0]), int(sp.fraction(I)[1]))
print(f"(5b) int_{{-1}}^{{1/2}} (112/113-mu)(-C0*+3/200) dmu = {I} (~{float(I):.5f}); with pi>=3: (3/10)*I = {Q(3,10)*I} (~{float(Q(3,10)*I):.5f})")
check("(5c) (3/10)*I > 104/625 (previous total positive-mass lower bound 207/5000 + 1/8; the new bound REPLACES it, no addition)", Q(3, 10)*I > Q(104, 625))
print("ALL CERTIFICATES PASS" if ok else "SOME CERTIFICATE FAILED")
