#!/usr/bin/env python3
"""chat independent verifier for D5 M40:  E_{rho^4}(rho,0,z;lam) >= -400.

Independent organisation (differs from the Astra common-denominator form):
  * jets in (d rho <= 4, d theta <= 2) with outward-rounded rational interval coefficients,
  * G(gamma0 + Delta) - G(gamma0) = -4 sum_n (-1)^{n+1}/n Delta^n int_0^1 c^{n-1}/A0^n dv   (log series),
    with K_n(q) = int (1-v^2)^{n-1}/(1+q v^2)^n dv enclosed by monotonicity in q (series + exact remainder),
  * sequential midpoint rule (Astra Lemma 2 (4.1), chat audited): f(m) + h_u^2/24 inf_C f_uu + h_t^2/24 inf_{m_u line} f_tt,
  * prefactor 1/(2 pi lam) applied sign-aware, pi in [333/106, 355/113].
usage: python3 -I chat_m40iv.py COVER.json [--cells 16] [--workers N] [--out out.jsonl]
COVER.json: {"boxes": [{"lam": [a,b], "rho": [a,b], "z": [a,b]}, ...], "cells": 16}
"""
import sys, os, json, argparse, time
from fractions import Fraction as Fr
from math import comb
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chat_m22iv as base
base.PREC = 110; base.SC = 1 << base.PREC
I = base.I

class J:
    """jet in (a = d rho, b = d theta), degrees a<=DA, b<=DB."""
    __slots__ = ('c', 'DA', 'DB')
    def __init__(s, c, DA, DB): s.c = c; s.DA = DA; s.DB = DB
    @staticmethod
    def const(x, DA, DB):
        c = {(i, k): None for i in range(DA + 1) for k in range(DB + 1)}
        c = {key: I(0) for key in c}; c[(0, 0)] = x if isinstance(x, I) else I(x); return J(c, DA, DB)
    def _lift(s, o): return o if isinstance(o, J) else J.const(o, s.DA, s.DB)
    def __add__(s, o): o = s._lift(o); return J({k: s.c[k] + o.c[k] for k in s.c}, s.DA, s.DB)
    __radd__ = __add__
    def __neg__(s): return J({k: -v for k, v in s.c.items()}, s.DA, s.DB)
    def __sub__(s, o): return s + (-s._lift(o))
    def __rsub__(s, o): return s._lift(o) - s
    def __mul__(s, o):
        if not isinstance(o, J):
            o = o if isinstance(o, I) else I(o); return J({k: v * o for k, v in s.c.items()}, s.DA, s.DB)
        r = {}
        nz_s = [(k, v) for k, v in s.c.items() if not (v.a == 0 and v.b == 0)]
        nz_o = [(k, v) for k, v in o.c.items() if not (v.a == 0 and v.b == 0)]
        for key in s.c: r[key] = I(0)
        for (i1, k1), v1 in nz_s:
            for (i2, k2), v2 in nz_o:
                i, k = i1 + i2, k1 + k2
                if i <= s.DA and k <= s.DB: r[(i, k)] = r[(i, k)] + v1 * v2
        return J(r, s.DA, s.DB)
    __rmul__ = __mul__
    def nil(s): c = dict(s.c); c[(0, 0)] = I(0); return J(c, s.DA, s.DB)
    def order(s): return s.DA + s.DB
    def recip(s):
        c0 = s.c[(0, 0)]; inv = c0.recip(); y = s.nil() * inv
        acc = J.const(1, s.DA, s.DB); p = J.const(1, s.DA, s.DB)
        for _ in range(s.order()): p = p * (-y); acc = acc + p
        return acc * inv
    def __truediv__(s, o): return s * s._lift(o).recip()
    def sqrt(s):
        c0 = s.c[(0, 0)]; r0 = c0.sqrt(); y = s.nil() * c0.recip()
        acc = J.const(1, s.DA, s.DB); p = J.const(1, s.DA, s.DB); coef = Fr(1)
        for k in range(1, s.order() + 1):
            coef = coef * (Fr(1, 2) - (k - 1)) / k; p = p * y; acc = acc + p * I(coef)
        return acc * r0
    def cap0(s, lo=None, hi=None):
        c = dict(s.c); c[(0, 0)] = c[(0, 0)].meet(lo, hi); return J(c, s.DA, s.DB)

NSER = 30
_B = {}
def Bmn(m, n):  # int_0^1 v^{2m} (1-v^2)^{n-1} dv, exact
    if (m, n) not in _B: _B[(m, n)] = sum((Fr((-1) ** l * comb(n - 1, l), 2 * (m + l) + 1) for l in range(n)), Fr(0))
    return _B[(m, n)]
_K = {}
def Kn(n, q):
    """interval for K_n(q') = int (1-v^2)^{n-1}/(1+q' v^2)^n dv, all q' in q (0<=q<1); decreasing in q'."""
    def T(qq): return sum((Fr((-1) ** m * comb(n + m - 1, m)) * qq ** m * Bmn(m, n) for m in range(NSER + 1)), Fr(0))
    def e(qq): return Fr(comb(n + NSER, NSER + 1)) * qq ** (NSER + 1) * Bmn(NSER + 1, n)
    key = (n, q.a, q.b)
    if key not in _K:
        qb = base.ru(q.b); qa = base.rd(q.a)
        _K[key] = I(base.rd(T(qb) - e(qb)), base.ru(T(qa)))
    return _K[key]

def box_consts(box):
    lam = I(Fr(box['lam'][0]), Fr(box['lam'][1])); RHO = I(Fr(box['rho'][0]), Fr(box['rho'][1])); Z = I(Fr(box['z'][0]), Fr(box['z'][1]))
    assert RHO.a >= 0 and Z.a >= 0
    rbox = I(RHO.b ** 2 + (Z.b / lam.a) ** 2).sqrt().b
    P = I(RHO.b ** 2 + Z.b ** 2).sqrt().b
    assert rbox < 1
    F = ((1 + lam.b ** 2) / 2 + P) / (lam.a * (1 - rbox))
    gmin = 1 / F
    return lam, RHO, Z, rbox, gmin

def raw_coeff(lam, RHO, Z, rbox, gmin, eps_mu, eps_c, U, T, var):
    """returns interval for d^4/drho^4 [ (d/dvar)^k ] of  j(u) k(t) F_E  where var in {None,'u','t'}:
       var None -> k=0 value; var 'u'/'t' -> second derivative in that angle (k=2)."""
    DB = 0 if var is None else 2
    DA = 4
    one = J.const(1, DA, DB)
    rho = J.const(RHO, DA, DB); rho.c[(1, 0)] = I(1)
    u = J.const(U, DA, DB); t = J.const(T, DA, DB)
    if var == 'u': u.c[(0, 1)] = I(1)
    if var == 't': t.c[(0, 1)] = I(1)
    u2 = u * u; t2 = t * t
    mu = (one - u2) / (one + u2) * I(eps_mu)
    a = (u * 2) / (one + u2)
    cc = (one - t2) / (one + t2); ss = (t * 2) / (one + t2)
    xi_x = a * cc * I(eps_c)
    jj = (u * 4) / ((one + u2) * (one + u2)); kk = one * 2 / (one + t2)
    lam2 = lam * lam
    D2 = one - mu * mu * (1 - lam2) - rho * xi_x * 2 - mu * (lam * Z * 2) + rho * rho + J.const(Z * Z, DA, DB)
    D = D2.sqrt().cap0(lam.a * (1 - rbox), 1 + rbox)
    h = (J.const(lam, DA, DB) - rho * xi_x * lam - mu * Z).cap0(lam.a * (1 - rbox), None)
    w = (J.const(lam2, DA, DB) + mu * mu * (1 - lam2)).sqrt().cap0(lam.a, 1)
    Gam = (h / (w * D)).cap0(gmin, 1)
    g0 = Gam.c[(0, 0)]; Dl = Gam.nil()
    a0 = I(1) + g0
    q0 = I((1 - g0.b) / (1 + g0.b), (1 - g0.a) / (1 + g0.a))
    Gp = J.const(0, DA, DB); p = J.const(1, DA, DB); ainv = a0.recip(); apow = I(1)
    for n in range(1, DA + DB + 1):
        p = p * Dl; apow = apow * ainv
        Mn = Kn(n, q0) * apow
        Gp = Gp + p * (Mn * I(Fr(-4 * (-1) ** (n + 1), n)))
    FE = h * Gp * jj * kk
    k = 0 if var is None else 2
    return FE.c[(4, k)] * (24 * (1 if k == 0 else 2))

def grid(spec):
    """spec: int n (uniform n cells on [0,1]) or explicit list of edge strings from 0 to 1."""
    if isinstance(spec, int): e = [Fr(k, spec) for k in range(spec + 1)]
    else: e = [Fr(x) for x in spec]
    assert e[0] == 0 and e[-1] == 1 and all(x < y for x, y in zip(e, e[1:])), 'bad grid'
    return list(zip(e, e[1:]))

def box_lower(box, cells):
    lam, RHO, Z, rbox, gmin = box_consts(box)
    ug = grid(cells['u'] if isinstance(cells, dict) else cells); tg = grid(cells['t'] if isinstance(cells, dict) else cells)
    raw = I(0)
    for em in (1, -1):
        for ec in (1, -1):
            for ua, ub in ug:
                hu = ub - ua; um = (ua + ub) / 2
                for ta, tb in tg:
                    ht = tb - ta; tm = (ta + tb) / 2
                    mid = raw_coeff(lam, RHO, Z, rbox, gmin, em, ec, I(um), I(tm), None)
                    cu = raw_coeff(lam, RHO, Z, rbox, gmin, em, ec, I(ua, ub), I(ta, tb), 'u')
                    ct = raw_coeff(lam, RHO, Z, rbox, gmin, em, ec, I(um), I(ta, tb), 't')
                    raw = raw + (mid + cu * (hu * hu / 24) + ct * (ht * ht / 24)) * (hu * ht)
    PI = I(Fr(333, 106), Fr(355, 113))
    pref = (PI * lam * 2).recip()
    lo = raw.a * (pref.a if raw.a >= 0 else pref.b)
    return lo, raw

def check_cover(boxes, lam_lo=Fr(2, 5), lam_hi=Fr(119, 200), rho_hi=Fr(1, 8)):
    strips = {}
    for b in boxes: strips.setdefault((Fr(b['lam'][0]), Fr(b['lam'][1])), []).append(((Fr(b['rho'][0]), Fr(b['rho'][1])), (Fr(b['z'][0]), Fr(b['z'][1]))))
    ks = sorted(strips)
    if ks[0][0] != lam_lo or ks[-1][1] != lam_hi: return False, 'lambda range'
    for (a1, b1), (a2, b2) in zip(ks, ks[1:]):
        if b1 != a2: return False, 'lambda gap at %s' % b1
    for (la, lb), cells in strips.items():
        rhos = sorted({r for r, _ in cells}); zs = sorted({z for _, z in cells})
        if len(cells) != len(rhos) * len(zs) or len(set(cells)) != len(cells): return False, 'strip %s not a product grid' % la
        if rhos[0][0] != 0 or rhos[-1][1] < rho_hi or any(x[1] != y[0] for x, y in zip(rhos, rhos[1:])): return False, 'rho tiling in strip %s' % la
        if zs[0][0] != 0 or zs[-1][1] < lb / 8 or any(x[1] != y[0] for x, y in zip(zs, zs[1:])): return False, 'z tiling in strip %s' % la
    return True, '%d strips, %d boxes' % (len(ks), len(boxes))

def work(arg):
    box, cells = arg; t0 = time.time(); lo, raw = box_lower(box, cells)
    return {'box': box, 'cells': cells, 'lower': str(lo), 'lower_float': float(lo), 'pass': lo >= -400, 'sec': round(time.time() - t0, 1)}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cover'); ap.add_argument('--cells', type=int, default=None)
    ap.add_argument('--workers', type=int, default=1); ap.add_argument('--out', default='chat_m40iv_out.jsonl'); ap.add_argument('--nocover', action='store_true')
    a = ap.parse_args(); d = json.load(open(a.cover)); boxes = d['boxes']; cells = a.cells or d.get('cells', 16)
    ok = True
    if not a.nocover:
        ok, info = check_cover(boxes); print('COVER', 'PASS' if ok else 'FAIL', info, flush=True)
    res = []
    with Pool(a.workers) as pool, open(a.out, 'w') as f:
        for r in pool.imap_unordered(work, [(b, cells) for b in boxes]):
            res.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(r['box'], '%.4f' % r['lower_float'], 'PASS' if r['pass'] else 'FAIL', r['sec'], 's', flush=True)
    worst = min(res, key=lambda r: Fr(r['lower']))
    print('boxes', len(res), '| all >= -400:', all(r['pass'] for r in res), '| worst', worst['box'], '%.4f' % worst['lower_float'])
    if not a.nocover: print('M40 VERDICT:', 'PASS' if (ok and all(r['pass'] for r in res)) else 'NOT PASS')
