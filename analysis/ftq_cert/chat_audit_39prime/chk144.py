"""chat independent check of the 144 Astra 39' Bernstein coefficients.
Pi_t built from the definitions in the south paper proof 05668a47 / kernel_extension_cert (not from Astra's script).
Check: polynomial sum_k b_k * prod Bernstein basis (with the box affine map inverted) == Pi_t exactly; all b_k > 0; count 72 each."""
import json, sys
from math import comb
import sympy as sp
from fractions import Fraction
L, m, mu = sp.symbols('L m mu')
a2 = 1 - mu**2; r = 1 - m**2; s = m - mu
d = a2 + r + L*s**2
B1 = m*(1-L)*mu**2 + ((1+L)*m**2 + L - 2)*mu - L*m
C0 = (L-1)*mu**3 - L*m*mu**2 + (2-L)*mu - m*(1-L)
g = m*a2 + C0
box = [(sp.Rational(4,25), sp.Rational(8649,40000)), (sp.Rational(112,113), sp.Integer(1)), (sp.Rational(-1,4), sp.Rational(3,5))]
J = json.load(open(sys.argv[1]))
ok = True
for tkey, t in (('3', sp.Integer(3)), ('14/5', sp.Rational(14,5))):
    Pi = sp.expand(-(g + sp.Rational(3,100)*a2)*d - t*B1*a2)
    rec = J['Bernstein'][tkey]; deg = rec['degree']
    xs = [(v - lo)/(hi - lo) for v,(lo,hi) in zip((L,m,mu), box)]
    rebuilt = 0; vals = []
    for c in rec['coefficients']:
        k = c['index']; b = sp.Rational(c['value']); vals.append(b)
        term = b
        for n,ki,x in zip(deg,k,xs): term *= comb(n,ki)*x**ki*(1-x)**(n-ki)
        rebuilt += term
    idx = {tuple(c['index']) for c in rec['coefficients']}
    full = len(idx) == (deg[0]+1)*(deg[1]+1)*(deg[2]+1) == len(rec['coefficients'])
    exact = sp.expand(rebuilt - Pi) == 0
    pdeg = sp.Poly(Pi, L, m, mu).degree_list()
    pos = all(v > 0 for v in vals); mn = min(vals)
    print(f"Pi_{tkey}: n={len(vals)} full_index_set={full} poly_degree={list(pdeg)} json_degree={deg} exact_identity={exact} all_positive={pos} min={mn} min_matches_json={str(mn)==rec['minimum']}")
    ok &= full and exact and pos and str(mn)==rec['minimum'] and list(pdeg)==deg
print('CHAT 144-COEFFICIENT CHECK:', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
