#!/usr/bin/env python3
"""chat independent verifier for D5 M22:  E_{rho rho z z}(0,0,z;lam) >= -400.

Independent of the Astra/Dig evaluator: own outward-rounded rational interval arithmetic,
own bivariate jets in (dz, du) truncated at z-degree 2 and u-degree 2, and a DIFFERENT
organisation of the auxiliary v-integral (expansion in powers of delta-q, separate moments
I_{m,r} for r = 2..6, monotone in q) instead of the common-denominator operator.

Audited ingredients (chat audit 2026-11-05): axial kernel (6.2), Psi form (5.2), Gram form of q
(4.1), moment tail (6.1), 1-D midpoint Peano rule, geometric caps d,h >= lam_lo - Z, w in [lam,1].

usage:  python3 -I chat_m22iv.py BOXES.json [--cells 32] [--workers N] [--out out.jsonl]
BOXES.json: {"boxes": [{"lam": ["2/5","81/200"], "z": ["7/200","81/1600"]}, ...]}  (z >= 0)
"""
import sys, json, argparse, time
from fractions import Fraction as Fr
from math import comb, isqrt
from multiprocessing import Pool

PREC = 200
SC = 1 << PREC

def rd(x):  # round down to 2^-PREC grid
    return Fr((x.numerator * SC) // x.denominator, SC)
def ru(x):
    return Fr(-((-x.numerator * SC) // x.denominator), SC)

class I:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=None):
        if b is None: b = a
        s.a = Fr(a); s.b = Fr(b)
        assert s.a <= s.b, (s.a, s.b)
    def __add__(s, o):
        o = o if isinstance(o, I) else I(o); return I(rd(s.a + o.a), ru(s.b + o.b))
    __radd__ = __add__
    def __neg__(s): return I(-s.b, -s.a)
    def __sub__(s, o):
        o = o if isinstance(o, I) else I(o); return I(rd(s.a - o.b), ru(s.b - o.a))
    def __rsub__(s, o): return I(o) - s
    def __mul__(s, o):
        o = o if isinstance(o, I) else I(o)
        p = (s.a * o.a, s.a * o.b, s.b * o.a, s.b * o.b)
        return I(rd(min(p)), ru(max(p)))
    __rmul__ = __mul__
    def recip(s):
        assert s.a > 0 or s.b < 0, 'division by interval containing 0'
        return I(rd(1 / s.b), ru(1 / s.a))
    def __truediv__(s, o):
        o = o if isinstance(o, I) else I(o); return s * o.recip()
    def sqrt(s):
        assert s.a >= 0
        def sq_lo(x):
            n = (x.numerator * SC * SC) // x.denominator; return Fr(isqrt(n), SC)
        def sq_hi(x):
            n = -((-x.numerator * SC * SC) // x.denominator); r = isqrt(n); r += (r * r < n); return Fr(r, SC)
        return I(sq_lo(s.a), sq_hi(s.b))
    def meet(s, lo=None, hi=None):
        a = s.a if lo is None else max(s.a, Fr(lo)); b = s.b if hi is None else min(s.b, Fr(hi))
        assert a <= b, 'empty meet: geometric cap contradicts enclosure'
        return I(a, b)

# ---- bivariate jets: coefficients c[(i,k)] of dz^i du^k, 0<=i<=2, 0<=k<=KU
class J:
    __slots__ = ('c', 'ku')
    def __init__(s, c, ku): s.c = c; s.ku = ku
    @staticmethod
    def const(x, ku):
        c = {(i, k): I(0) for i in range(3) for k in range(ku + 1)}; c[(0, 0)] = x if isinstance(x, I) else I(x); return J(c, ku)
    def __add__(s, o):
        if not isinstance(o, J): o = J.const(o, s.ku)
        return J({key: s.c[key] + o.c[key] for key in s.c}, s.ku)
    __radd__ = __add__
    def __neg__(s): return J({key: -v for key, v in s.c.items()}, s.ku)
    def __sub__(s, o):
        if not isinstance(o, J): o = J.const(o, s.ku)
        return s + (-o)
    def __rsub__(s, o): return J.const(o, s.ku) - s
    def __mul__(s, o):
        if not isinstance(o, J):
            o = o if isinstance(o, I) else I(o); return J({key: v * o for key, v in s.c.items()}, s.ku)
        r = {}
        for (i, k) in s.c:
            acc = I(0)
            for i1 in range(i + 1):
                for k1 in range(k + 1):
                    acc = acc + s.c[(i1, k1)] * o.c[(i - i1, k - k1)]
            r[(i, k)] = acc
        return J(r, s.ku)
    __rmul__ = __mul__
    def nil(s):  # jet minus constant term
        c = dict(s.c); c[(0, 0)] = I(0); return J(c, s.ku)
    def order(s): return 2 + s.ku
    def recip(s):
        c0 = s.c[(0, 0)]; inv = c0.recip(); y = s.nil() * inv  # 1/(c0(1+y)) = inv * sum (-y)^k
        acc = J.const(1, s.ku); p = J.const(1, s.ku)
        for _ in range(s.order()):
            p = p * (-y); acc = acc + p
        return acc * inv
    def __truediv__(s, o):
        if not isinstance(o, J): o = J.const(o, s.ku)
        return s * o.recip()
    def sqrt(s):
        c0 = s.c[(0, 0)]; r0 = c0.sqrt(); y = s.nil() * c0.recip()   # sqrt(c0) * sum binom(1/2,k) y^k
        acc = J.const(1, s.ku); p = J.const(1, s.ku); coef = Fr(1)
        for k in range(1, s.order() + 1):
            coef = coef * (Fr(1, 2) - (k - 1)) / k; p = p * y; acc = acc + p * I(coef)
        return acc * r0
    def cap0(s, lo=None, hi=None):
        c = dict(s.c); c[(0, 0)] = c[(0, 0)].meet(lo, hi); return J(c, s.ku)

def moment(m, r, q, N=24):
    """rational interval for I_{m,r}(q') for all q' in q=[qa,qb], 0<=qa<=qb<1: monotone decreasing in q'."""
    def T(qq): return sum((Fr((-1) ** n * comb(r + n - 1, n)) * qq ** n / (2 * (m + n) + 1) for n in range(N + 1)), Fr(0))
    def e(qq): return Fr(comb(r + N, N + 1)) * qq ** (N + 1) / (2 * (m + N + 1) + 1)
    lo = T(q.b) - e(q.b); hi = T(q.a)
    return I(rd(lo), ru(hi))

def qcap(lam, Z):
    """sup q on {lam in [la,lb], |z|<=Z}: wd <= (1+lam^2)/2 + Z, h >= lam - Z, F decreasing in lam (chat audited)."""
    la = lam.a; Zh = Z.b
    assert la - Zh > 0
    Fm = ((1 + la * la) / 2 + Zh) / (la - Zh)
    g = 1 / Fm
    return (1 - g) / (1 + g)

def psi_integrals(lam, Z, U, eps, ku, qmax):
    """returns intervals for  int_0^1 [dz^2 du^k] Psi dv  (k = 0..ku), Psi = (A0 + A1 x)/(1+q x)^2, x=v^2."""
    z = J.const(Z, ku); z.c[(1, 0)] = I(1)
    u = J.const(U, ku)
    if ku >= 1: u.c[(0, 1)] = I(1)
    one = J.const(1, ku)
    u2 = u * u
    mu = (one - u2) / (one + u2) * I(eps)
    jj = (u * 4) / ((one + u2) * (one + u2))
    lam2 = lam * lam
    a2 = one - mu * mu
    vz = mu * lam - z
    d2 = a2 + vz * vz
    h = J.const(lam, ku) - z * mu
    w2 = J.const(lam2, ku) + mu * mu * (1 - lam2)
    Zh = Z.b
    d = d2.sqrt().cap0(lam.a - Zh, 1 + Zh)
    h = h.cap0(lam.a - Zh, lam.b + Zh)
    w = w2.sqrt().cap0(lam.a, 1)
    L = w * d + h
    V = h - d2 * lam
    d4 = d2 * d2
    P = (h * h * (d2 * 2 - a2) - a2 * V * V * 2) / d4
    Q0 = a2 * h * V * V / d4
    g = mu * (1 - lam2) + z * lam
    q = (a2 * g * g / (L * L)).cap0(0, qmax)
    A = jj * P / (L * lam)
    B = jj * Q0 / (L * L * lam)
    A0 = A + B
    A1 = A * q - B
    dq = q.nil(); q0 = q.c[(0, 0)]
    # (1+qx)^-2 = (1+q0x)^-2 * sum_k (-1)^k (k+1) x^k dq^k (1+q0x)^-k ; dq^k = 0 for k > 2+ku
    res = [I(0) for _ in range(ku + 1)]
    p = J.const(1, ku)
    for k in range(0, 3 + ku):
        t0 = p * A0; t1 = p * A1
        cf = I(Fr((-1) ** k * (k + 1)))
        mk = moment(k, 2 + k, q0); mk1 = moment(k + 1, 2 + k, q0)
        for kk in range(ku + 1):
            res[kk] = res[kk] + cf * (t0.c[(2, kk)] * mk + t1.c[(2, kk)] * mk1)
        p = p * dq
    return res

def box_lower(box, cells=32):
    lam = I(Fr(box['lam'][0]), Fr(box['lam'][1])); Z = I(Fr(box['z'][0]), Fr(box['z'][1]))
    assert Z.a >= 0
    qmax = qcap(lam, Z)
    total = I(0); recs = []
    for eps in (1, -1):
        for c in range(cells):
            ua, ub = Fr(c, cells), Fr(c + 1, cells); hc = ub - ua; um = (ua + ub) / 2
            mid = psi_integrals(lam, Z, I(um), eps, 0, qmax)[0] * 2          # f(m) = int Psi_zz dv
            cur = psi_integrals(lam, Z, I(ua, ub), eps, 2, qmax)[2] * 4      # f''(u) on cell
            contrib = mid * hc + cur * (hc ** 3 / 24)
            total = total + contrib
            recs.append({'eps': eps, 'cell': c, 'mid': [str(mid.a), str(mid.b)], 'curv': [str(cur.a), str(cur.b)]})
    return total.a, recs

def work(arg):
    box, cells = arg
    t0 = time.time(); lo, recs = box_lower(box, cells)
    return {'box': box, 'lower': str(lo), 'lower_float': float(lo), 'pass': lo >= -400, 'sec': round(time.time() - t0, 2)}

def check_cover(boxes, lam_lo=Fr(2, 5), lam_hi=Fr(119, 200)):
    """boxes must form lambda-strips tiling [lam_lo, lam_hi]; in each strip the z-intervals must tile
    [0, Z] contiguously with Z >= lam_b/8 (so the strip covers 0 <= z <= lam/8 for every lam in it)."""
    strips = {}
    for b in boxes:
        key = (Fr(b['lam'][0]), Fr(b['lam'][1])); strips.setdefault(key, []).append((Fr(b['z'][0]), Fr(b['z'][1])))
    ks = sorted(strips)
    if ks[0][0] != lam_lo or ks[-1][1] != lam_hi: return False, 'lambda range not covered'
    for (a1, b1), (a2, b2) in zip(ks, ks[1:]):
        if b1 != a2: return False, 'lambda gap/overlap at %s' % b1
    for (la, lb), zz in strips.items():
        if la >= lb: return False, 'degenerate lambda strip'
        zz.sort()
        if zz[0][0] != 0: return False, 'z does not start at 0 in strip %s' % la
        for (z1, z2), (z3, z4) in zip(zz, zz[1:]):
            if z2 != z3: return False, 'z gap/overlap in strip %s' % la
        if zz[-1][1] < lb / 8: return False, 'z top < lam_b/8 in strip %s' % la
    return True, '%d strips, %d boxes' % (len(ks), len(boxes))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('boxes'); ap.add_argument('--cells', type=int, default=32)
    ap.add_argument('--workers', type=int, default=1); ap.add_argument('--out', default='chat_m22iv_out.jsonl')
    a = ap.parse_args()
    boxes = json.load(open(a.boxes))['boxes']
    ok, info = check_cover(boxes); print('COVER', 'PASS' if ok else 'FAIL', info, flush=True)
    with Pool(a.workers) as pool, open(a.out, 'w') as f:
        res = []
        for r in pool.imap(work, [(b, a.cells) for b in boxes]):
            res.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(r['box'], '%.6f' % r['lower_float'], 'PASS' if r['pass'] else 'FAIL', r['sec'], 's', flush=True)
    worst = min(res, key=lambda r: Fr(r['lower']))
    print('boxes', len(res), '| all >= -400:', all(r['pass'] for r in res), '| worst', worst['box'], '%.6f' % worst['lower_float'])
    print('M22 VERDICT:', 'PASS' if (ok and all(r['pass'] for r in res)) else 'NOT PASS')
