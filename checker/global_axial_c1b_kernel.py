#!/usr/bin/env python3
"""Full-source 192-bit C1b checker.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Status: IMPLEMENTED_PROTOTYPE / MACHINE_NOT_RUN / NOT_BINDING.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from checker import global_axial_c0_checker as base
from checker import c0a_four_group_v2 as grouped
from checker.monotone_tube_refinement_checker import _ordinary_refinement as _gt_ordinary
from checker.monotone_tube_interval_checker import _corner as _gt_corner
from checker.global_axial_c1b_endpoint_r import (
    REndpointDomainGuard, _R_endpoint_safe,
)
from checker.global_axial_c0_checker_v2 import _g_density_stable as _legacy_g_density_stable

BITS, DEG = 192, 50
USTAR = Fraction(3, 5)
L_LO, L_HI = Fraction(9, 20), Fraction(5, 8)
DLAM, N_COARSE = Fraction(1, 800), 140
MAX_DEPTH, MAX_ACCEPTED, MAX_ATTEMPTED = 3, 1120, 2100
T_LO, T_MID_HI, T_HI = Fraction(1, 2), Fraction(31, 32), Fraction(1)
W0, PRED_ACCEPT, ROOT_TARGET = Fraction(1, 16), Fraction(1, 64), Fraction(1, 128)
T_STAGES = (("T0", 8, 4, 4096), ("T1", 16, 8, 4096), ("T2", 32, 16, 8192))
ROOT_MV_STEPS = 8
ROOT_G_PANELS, ROOT_GT_PANELS, ROOT_GL_PANELS = 32768, 8192, 8192
ROOT_GT_T_CELLS = 16
ROOT_GL_T_CELLS = 16
E0_TBOXES, E0_LBOXES = 24, 8
E_STAGES = (("E0", 1024), ("E1", 2048), ("E2", 4096))
E_BOX_CAP = 4096
MONO_WORK_CAP = 1_048_576
PRED_GRID_DEN, PRED_SCAN_PANELS = 1024, 256
ATTEMPT_WORK_CEILING = 25_591_808
GLOBAL_ATTEMPT_WORK_CEILING = 53_742_796_800
ACCEPTED_WORK_CEILING = 28_662_824_960
BOB_RECEIPT = Path("analysis/GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md")
BOB_EVIDENCE_HEAD = "25efb59b851eb9d7a3d5ce30309eb8903d976930"
BOB_CONTRACT_BLOB = "215193e2fc2a1abcf2aee2527c4c2e6f3176ea6c"
BOB_AMENDMENT_BLOB = "8e04e2efaf816bab9d9d1f3fd0a9d753538b31ad"
BOB_RECEIPT_BLOB = "0f19e3877b9675506ac8f35a5702147a84723c43"

C1B_NUMERIC_ROOTS = ('checker/global_axial_c0_checker.py', 'checker/global_axial_c0_checker_v2.py', 'checker/c0a_four_group_v2.py', 'checker/monotone_tube_refinement_checker.py', 'checker/monotone_tube_interval_checker.py', 'checker/global_axial_c1b_endpoint_r.py')
C1B_NUMERIC_IMPORT_CLOSURE = {'checker/global_axial_c0_checker.py': '85978625e029b01c8ae40fa8234566f10eea251c', 'checker/global_axial_c0_checker_v2.py': 'fbec890588d2d390ea67bc90116b80bb37ebf9cc', 'checker/c0a_four_group_v2.py': '18e66b6450cd2a379bbb869a99e4e5ce6999f6e5', 'checker/endpoint_interval_checker.py': '4cb16f8a975e5a3be601a7926af695ad5be57790', 'checker/endpoint_local_checker.py': '2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc', 'checker/endpoint_local_controls.py': 'c913c47d228e51a15f56957f5df9196efa1b22c3', 'checker/monotone_tube_interval_checker.py': '78ae54ef3a769d6194c89ab5f4f38ea9f151476c', 'checker/monotone_tube_refinement_checker.py': 'fd778d6d3a2dc52ae38be87bf4eb800bfbdea6d3', 'checker/global_axial_c1b_endpoint_r.py': '1a953b22c12a89afc06790b28d6b0dea9680dc43'}

@dataclass(frozen=True)
class Slab:
    coarse: int
    depth: int
    ll: Fraction
    lr: Fraction

@dataclass(frozen=True)
class EBox:
    side: str
    tl: Fraction
    tr: Fraction
    ll: Fraction
    lr: Fraction

def split(a, b, n):
    h = (b - a) / n
    return [(a + i*h, a + (i+1)*h) for i in range(n)]

def interval(a, b):
    return base._box(base._point(a), base._point(b))

def _stats():
    return {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}

def _g_density_stable(s, t, L, stats):
    s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = grouped._primitives(s, t, L)
    R = _R_endpoint_safe(u, stats)
    gt = L * n / (W * q * rootq)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)

def g_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    stats, z = _stats(), arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        z += _g_density_stable(base._box(aa, bb), t, lam, stats) * (bb-aa)
    return z, panels

def gt_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    z, charts = arb(0), defaultdict(int)
    for si, (a, b) in enumerate(zip(grid, grid[1:])):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        if tr == T_HI and si == 0:
            val, chart = _gt_corner(s, t, lam)
            terms = (val,)
        else:
            chart, terms = _gt_ordinary(s, t, lam)
        charts[chart] += 1
        z += sum(terms, arb(0)) * (bb-aa)
    return z, dict(charts), panels

def _certified_positive_q(mu, t, lam, q):
    lower_mu, upper_mu = mu.lower(), mu.upper()
    lower_t, upper_t, lower_lam = t.lower(), t.upper(), lam.lower()
    if not all(v.is_finite() for v in (lower_mu, upper_mu, lower_t, upper_t, lower_lam, q.upper())):
        raise REndpointDomainGuard("Q_BOX_NONFINITE_ENDPOINT")

    def endpoint_value(mu0):
        nearest_t = lower_t if mu0 < lower_t else upper_t if mu0 > upper_t else mu0
        return (arb(1) - mu0 * mu0 + lower_lam * lower_lam * (nearest_t - mu0) * (nearest_t - mu0)).lower()

    lower_q = min(endpoint_value(lower_mu), endpoint_value(upper_mu))
    if not lower_q.is_finite() or not lower_q > 0:
        raise REndpointDomainGuard("Q_BOX_MIN_NONPOSITIVE")
    safe_upper = q.upper()
    if not safe_upper.is_finite():
        raise REndpointDomainGuard("Q_BOX_UPPER_NONFINITE")
    upper_q = max(lower_q, safe_upper)
    positive_q = base._box(lower_q, upper_q)
    if not positive_q.lower() > 0:
        raise REndpointDomainGuard("Q_BOX_OUTWARD_NONPOSITIVE")
    return positive_q


def _positive_reciprocal_wq32(W, q):
    lower_w, upper_w, lower_q, upper_q = W.lower(), W.upper(), q.lower(), q.upper()
    if not all(v.is_finite() for v in (lower_w, upper_w, lower_q, upper_q)) or not (lower_w > 0 and lower_q > 0):
        raise REndpointDomainGuard("INV_WQ32_NONPOSITIVE_ENDPOINT")
    lower_inv = (arb(1) / upper_w / upper_q / upper_q.sqrt()).lower()
    upper_inv = (arb(1) / lower_w / lower_q / lower_q.sqrt()).upper()
    result = base._box(lower_inv, upper_inv)
    if not result.lower() > 0 or not _arb_bounds_finite(result):
        raise REndpointDomainGuard("INV_WQ32_NONFINITE")
    return result


def _glam_density(s, t, lam, stats):
    s, x, mu, eps, A, delta, delta_sq, _gam, _u, L2, q_raw, _rootq, W, W2, n, m, p, big_q = grouped._primitives(s, t, lam)
    q = _certified_positive_q(mu, t, lam, q_raw)
    rootq = q.sqrt()
    gam = lam * A / (W * rootq)
    h = mu + L2 * delta
    u = base._unit_nonnegative(eps * h * h / (W2 * q))
    R = _R_endpoint_safe(u, stats)
    inv_wq32 = _positive_reciprocal_wq32(W, q)
    wlog = lam * eps / W2
    glam = gam * (1 / lam - wlog - lam * delta_sq / q)
    pref = lam * inv_wq32
    nlam = -2 * lam * (mu * delta_sq + A * delta)
    preflam = pref * (1 / lam - wlog - 3 * lam * delta_sq / q)
    gt = pref * n
    gtlam = preflam * n + pref * nlam
    k = mu - L2 * delta
    regular_rg_term = -(gam * R - 1) * gam * eps * k * inv_wq32
    return s * (2 * mu * R * glam - 2 * A * (regular_rg_term + R * gtlam))

def glam_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    stats = {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}
    z = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        z += _glam_density(base._box(aa, bb), t, lam, stats) * (bb-aa)
    return z, stats, panels

def _arb_exact_fraction(x):
    if not x.is_finite():
        raise RuntimeError("ROOT_NONFINITE_ARB_BOUND")
    if not x.is_exact():
        raise RuntimeError("ROOT_NONEXACT_ARB_BOUND")
    mantissa, exponent = x.man_exp()
    if exponent >= 0:
        return Fraction(int(mantissa) * (1 << int(exponent)), 1)
    return Fraction(int(mantissa), 1 << int(-exponent))

def _arb_snapshot(x):
    return {
        "mid": x.mid().str(50),
        "rad": x.rad().str(50),
        "lower": x.lower().str(50),
        "upper": x.upper().str(50),
    }

def _arb_bounds_finite(x):
    return bool(x.lower().is_finite() and x.upper().is_finite())

def _newton_candidate(t_ref, gpar, gt):
    if not gt.upper() < 0:
        return None
    quotient = gpar / gt
    if not _arb_bounds_finite(quotient):
        return None
    candidate = base._point(t_ref) - quotient
    if not _arb_bounds_finite(candidate):
        return None
    return candidate

def _intersect_newton(lo, hi, candidate):
    nlo = _arb_exact_fraction(candidate.lower())
    nhi = _arb_exact_fraction(candidate.upper())
    new_lo, new_hi = max(lo, nlo), min(hi, nhi)
    if new_hi < new_lo:
        raise RuntimeError("ROOT_EMPTY_INTERSECTION")
    return new_lo, new_hi

def _git_blob_bytes(path):
    data=Path(path).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

def _numeric_dependency_closure():
    seen=set(); stack=list(C1B_NUMERIC_ROOTS); package="checker"
    while stack:
        rel=stack.pop()
        if rel in seen: continue
        q=Path(rel)
        if not q.is_file(): raise SystemExit("NUMERIC_IMPORT_CLOSURE_FAIL")
        seen.add(rel); tree=ast.parse(q.read_text())
        for node in ast.walk(tree):
            names=[]
            if isinstance(node,ast.Import): names=[a.name for a in node.names]
            elif isinstance(node,ast.ImportFrom) and node.module:
                names=[node.module]
                if node.module==package: names += [package+"."+a.name for a in node.names]
            for name in names:
                if name==package or name.startswith(package+"."):
                    cand=name.replace(".","/")+".py"
                    if Path(cand).is_file() and cand not in seen: stack.append(cand)
    return seen

def numeric_import_closure_preflight():
    found=_numeric_dependency_closure(); declared=set(C1B_NUMERIC_IMPORT_CLOSURE); ok=(found==declared)
    for rel in sorted(declared):
        try: obs=_git_blob_bytes(rel)
        except OSError: obs=None
        exp=C1B_NUMERIC_IMPORT_CLOSURE[rel]; hit=(obs==exp); ok = ok and hit
        print("C1B_NUMERIC_IMPORT_BLOB",rel,"PASS" if hit else "FAIL",exp,obs)
    print("NUMERIC_IMPORT_CLOSURE_CHECK","PASS" if ok else "FAIL","declared",len(declared),"discovered",len(found),"missing",sorted(found-declared),"stale",sorted(declared-found))
    if not ok: raise SystemExit("NUMERIC_IMPORT_CLOSURE_FAIL")

def numeric_import_closure_controls():
    global C1B_NUMERIC_ROOTS
    key=sorted(C1B_NUMERIC_IMPORT_CLOSURE)[0]; old=C1B_NUMERIC_IMPORT_CLOSURE[key]
    blob_fail=False
    try:
        C1B_NUMERIC_IMPORT_CLOSURE[key]="0"*40
        try: numeric_import_closure_preflight()
        except SystemExit as exc: blob_fail=(str(exc)=="NUMERIC_IMPORT_CLOSURE_FAIL")
    finally:
        C1B_NUMERIC_IMPORT_CLOSURE[key]=old
    roots_old=C1B_NUMERIC_ROOTS; import_fail=False
    try:
        C1B_NUMERIC_ROOTS=roots_old+("checker/global_axial_c1a_checker.py",)
        try: numeric_import_closure_preflight()
        except SystemExit as exc: import_fail=(str(exc)=="NUMERIC_IMPORT_CLOSURE_FAIL")
    finally:
        C1B_NUMERIC_ROOTS=roots_old
    ok=blob_fail and import_fail
    print("C1B_NUMERIC_IMPORT_CLOSURE_CONTROL",7,"PASS" if ok else "FAIL",
          "perturbed_blob_fail",blob_fail,"undeclared_numeric_root_fail",import_fail)
    if not ok: raise SystemExit("C1B_NUMERIC_IMPORT_CLOSURE_CONTROL_FAIL")

def endpoint_light_controls():
    from math import comb
    coeff_ok=all(Fraction(comb(2*n,n),4**n*(2*n+1))>0 for n in range(8))
    vals=[_R_endpoint_safe(base._point(x),{}) for x in (Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1))]
    mono=all(a.upper()<b.lower() for a,b in zip(vals,vals[1:]))
    endpoint_ok=(vals[0].lower() <= 1 <= vals[0].upper() and vals[-1].lower() <= arb.pi()/2 <= vals[-1].upper())
    c1=coeff_ok and mono and endpoint_ok
    print("C1B_R_ENDPOINT_CONTROL",1,"PASS" if c1 else "FAIL")
    if not c1: raise SystemExit("C1B_R_ENDPOINT_CONTROL_FAIL")
    c2=True
    for x in (Fraction(9,10),Fraction(99,100),Fraction(999,1000)):
        xb=base._point(x); rn=_R_endpoint_safe(xb,{}); comp=(arb.pi()/2-(1-xb).sqrt().asin())/xb.sqrt()
        c2 = c2 and not (rn.upper()<comp.lower() or comp.upper()<rn.lower())
    print("C1B_R_COMPLEMENT_CONTROL",2,"PASS" if c2 else "FAIL")
    if not c2: raise SystemExit("C1B_R_COMPLEMENT_CONTROL_FAIL")
    c3=True; c3_cases=0
    for ulo,uhi in ((Fraction(1,10),Fraction(1,5)),(Fraction(2,5),Fraction(1,2)),
                     (Fraction(7,10),Fraction(4,5)),(Fraction(9,10),Fraction(19,20))):
        for glo,ghi in ((Fraction(1,5),Fraction(3,10)),(Fraction(3,5),Fraction(7,10))):
            u=base._box(base._point(ulo),base._point(uhi)); g=base._box(base._point(glo),base._point(ghi))
            old=base._R(u,g,{"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0})[0]
            new=_R_endpoint_safe(u,{}); c3_cases += 1
            c3 = c3 and old.is_finite() and new.is_finite() and not (new.upper()<old.lower() or old.upper()<new.lower())
            c3 = c3 and new.lower()>=old.lower() and new.upper()<=old.upper()
    print("C1B_R_LEGACY_AGREEMENT_CONTROL",3,"PASS" if c3 else "FAIL","cases",c3_cases)
    if not c3: raise SystemExit("C1B_R_LEGACY_AGREEMENT_FAIL")
    sb=base._box(base._point(Fraction(0)),base._point(Fraction(1,64)))
    tb=interval(Fraction(3,4),Fraction(3,4)); lb=interval(Fraction(1,2),Fraction(1,2))
    moving=_glam_density(sb,tb,lb,{"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0})
    c5b=moving.is_finite()
    print("C1B_MOVING_U0_CONTROL","5b","PASS" if c5b else "FAIL","value",moving.str(50))
    if not c5b: raise SystemExit("C1B_MOVING_U0_CONTROL_FAIL")

def _q_box_min_fraction(mu_lo, mu_hi, t_lo, t_hi, lam_lo):
    def clamp_t(mu0):
        return t_lo if mu0 < t_lo else t_hi if mu0 > t_hi else mu0
    def q_at(mu0):
        t0 = clamp_t(mu0)
        return 1 - mu0 * mu0 + lam_lo * lam_lo * (t0 - mu0) * (t0 - mu0)
    return min(q_at(mu_lo), q_at(mu_hi))


def v28_preflight_controls():
    # V28-C1: exact rational sign identities on the frozen C1b lambda domain.
    lambdas=(Fraction(9,20),Fraction(1,2),Fraction(5,8))
    c1=all(2*(L*L-1)<0 and 2*L*L>0 for L in lambdas)
    c1=c1 and all(2*L*Fraction(1,7)**2>=0 for L in lambdas)
    print("C1B_V28_C1_EXACT_CALCULUS","PASS" if c1 else "FAIL")
    if not c1: raise SystemExit("C1B_V28_C1_FAIL")

    # V28-C2/C3: both clamp branches, subdivision monotonicity, and exact point soundness.
    inside=_q_box_min_fraction(Fraction(1,2),Fraction(3,4),Fraction(2,5),Fraction(3,5),Fraction(1,2))
    outside=_q_box_min_fraction(Fraction(9,10),Fraction(1),Fraction(3,4),Fraction(4,5),Fraction(1,2))
    parent=(Fraction(9,10),Fraction(1),Fraction(3,4),Fraction(4,5),Fraction(1,2))
    pmin=_q_box_min_fraction(*parent)
    child1=_q_box_min_fraction(Fraction(9,10),Fraction(19,20),parent[2],parent[3],parent[4])
    child2=_q_box_min_fraction(Fraction(19,20),Fraction(1),parent[2],parent[3],parent[4])
    samples=(Fraction(9,10),Fraction(37,40),Fraction(19,20),Fraction(39,40),Fraction(1))
    exact_points=True
    for mu0 in samples:
        t0=Fraction(31,40)
        q0=1-mu0*mu0+Fraction(1,4)*(t0-mu0)*(t0-mu0)
        exact_points = exact_points and q0>=pmin
    dlo,dhi=Fraction(-1,100),Fraction(1,200)
    zero_cross = dlo < 0 < dhi and min(dlo*dlo,dhi*dhi) > 0
    c23=inside>=0 and outside>0 and child1>=pmin and child2>=pmin and exact_points and zero_cross
    print("C1B_V28_C2_CLAMP_BRANCHES","PASS" if c23 else "FAIL","inside",inside,"outside",outside)
    print("C1B_V28_C3_SOUNDNESS","PASS" if c23 else "FAIL","parent",pmin,"children",child1,child2)
    if not c23: raise SystemExit("C1B_V28_C23_FAIL")

    # V28-C4/C5/C6: canonical exact q minima and the two-stage positive structure.
    root_lo=Fraction(478138193925,2**39); root_hi=Fraction(546857670661,2**39)
    cell15=split(root_lo,root_hi,16)[15]
    qmins=[]
    for i in (0,1):
        slo=Fraction(i,8192); shi=Fraction(i+1,8192)
        mu_lo=1-shi*shi; mu_hi=1-slo*slo
        qmins.append(_q_box_min_fraction(mu_lo,mu_hi,cell15[0],cell15[1],Fraction(231,400)))
    expected=(Fraction(448191534236194953480969,48357032784585166988247040000),
              Fraction(17985206094396086091889,1934281311383406679529881600))
    c4=tuple(qmins)==expected and all(q>0 for q in qmins)
    print("C1B_V28_C4_QMIN","PASS" if c4 else "FAIL","panel0",qmins[0],"panel1",qmins[1])
    if not c4: raise SystemExit("C1B_V28_C4_FAIL")

    sb=base._box(base._point(Fraction(0)),base._point(Fraction(1,8192)))
    tb=interval(*cell15); lb=interval(Fraction(231,400),Fraction(3697,6400))
    _,_,mu,e,A,d,d2,_,_,l2,qraw,_,w,w2,N,M,P,Q=grouped._primitives(sb,tb,lb)
    qpos=_certified_positive_q(mu,tb,lb,qraw); inv=_positive_reciprocal_wq32(w,qpos)
    s0=Fraction(1,16384); x0=s0*s0; mu0=1-x0; e0=x0*(2-x0)
    t0=(cell15[0]+cell15[1])/2; l0=(Fraction(231,400)+Fraction(3697,6400))/2
    q0=1-mu0*mu0+l0*l0*(t0-mu0)*(t0-mu0)
    w0=(base._point(mu0*mu0+l0*l0*e0)).sqrt()
    inv0=arb(1)/w0/base._point(q0)/base._point(q0).sqrt()
    c5=inv.lower()<=inv0.lower() and inv0.upper()<=inv.upper() and inv.lower()>0 and inv.is_finite()
    generic=w*qpos*qpos.sqrt()
    c6=qraw.lower()<=0 and qpos.lower()>0 and generic.lower()<=0 and c5
    print("C1B_V28_C5_INV_ENDPOINT","PASS" if c5 else "FAIL","point",inv0,"hull",inv)
    print("C1B_V28_C6_TWO_STAGE","PASS" if c6 else "FAIL","naive_q_lower",qraw.lower(),"qpos_lower",qpos.lower(),"generic_den_lower",generic.lower(),"inv",inv)
    if not (c5 and c6): raise SystemExit("C1B_V28_C56_FAIL")

    # V28-C7: exact canonical first Newton/MV contraction.
    slab=Slab(102,3,Fraction(231,400),Fraction(3697,6400))
    cells=[]
    for a,b in split(root_lo,root_hi,ROOT_GL_T_CELLS):
        v,_,_=glam_box(a,b,slab.ll,slab.lr,ROOT_GL_PANELS); cells.append(v.is_finite())
    rok,rstar,work,steps,reason=root_localize(slab,root_lo,root_hi)
    step=steps[0] if steps else {}
    oldw=root_hi-root_lo; neww=step.get("width",oldw); ratio=neww/oldw
    c7=all(cells) and rok and step.get("T_next") is not None and neww<oldw
    print("C1B_V28_C7_CONTRACTION","PASS" if c7 else "FAIL","T_k",step.get("T_k"),"T_next",step.get("T_next"),"width_old",oldw,"width_new",neww,"ratio",ratio,"reason",reason)
    if not c7: raise SystemExit("C1B_V28_C7_FAIL")

    # V281-C1/C2/C3: unique reciprocal path, positive q endpoints, logical work identity.
    import inspect
    src=inspect.getsource(_glam_density)
    c81=(src.count('inv_wq32 = _positive_reciprocal_wq32')==1 and 'pref = lam * inv_wq32' in src and
         'regular_rg_term = -(gam * R - 1) * gam * eps * k * inv_wq32' in src and
         'lam / (W * q * rootq)' not in src)
    bad=False
    try: _certified_positive_q(mu,tb,lb,arb('nan'))
    except REndpointDomainGuard: bad=True
    _,_,work_a=glam_box(cell15[0],cell15[1],slab.ll,slab.lr,64)
    _,_,work_b=glam_box(cell15[0],cell15[1],slab.ll,slab.lr,64)
    c82=qpos.upper()>=qpos.lower()>0 and bad
    c83=(work_a==work_b==64)
    print("C1B_V281_C1_UNIQUE_PATH","PASS" if c81 else "FAIL")
    print("C1B_V281_C2_Q_ENDPOINTS","PASS" if c82 else "FAIL","q",qpos)
    print("C1B_V281_C3_WORK_IDENTITY","PASS" if c83 else "FAIL","work",work_a,work_b)
    if not (c81 and c82 and c83): raise SystemExit("C1B_V281_FAIL")


def endpoint_regression_controls():
    tp=Fraction(546857674007,2**39); ll=Fraction(231,400); lr=Fraction(3697,6400); t=interval(tp,tp); L=interval(ll,lr); c4=c5=True
    for i in (40,41,42):
        sb=base._box(base._point(Fraction(i,4096)),base._point(Fraction(i+1,4096)))
        st={"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0}
        legacy=_legacy_g_density_stable(sb,t,L,st); fresh=_g_density_stable(sb,t,L,{"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0}); gl=_glam_density(sb,t,L,{"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0})
        c4 = c4 and (not legacy.is_finite()) and fresh.is_finite(); c5 = c5 and fresh.is_finite() and gl.is_finite()
        print("C1B_R_REGRESSION_VALUE",i,"legacy",legacy.str(50),"new_g",fresh.str(50),"new_gl",gl.str(50))
    print("C1B_R_REGRESSION_CONTROL",4,"PASS" if c4 else "FAIL"); print("C1B_GL_REGRESSION_CONTROL",5,"PASS" if c5 else "FAIL")
    if not (c4 and c5): raise SystemExit("C1B_R_REGRESSION_FAIL")
    slab=Slab(102,3,Fraction(231,400),Fraction(3697,6400)); tc=Fraction(512497935639,2**39)
    out=tube_stage(slab,tc,T_STAGES[0]); c5_t0=out[0] and len(out[10])==0
    print("C1B_ABORT154_T0_CONTROL",5,"PASS" if c5_t0 else "FAIL")
    if not c5_t0: raise SystemExit("C1B_ABORT154_T0_CONTROL_FAIL")

def bob_preflight():
    data = BOB_RECEIPT.read_bytes()
    text = data.decode()
    header = f"blob {len(data)}\0".encode()
    blob = hashlib.sha1(header + data).hexdigest()
    required = (
        "MACHINE_PASS / C1B_SUBGATE_ONLY / FULL_C1B_NOT_YET_CLOSED",
        BOB_EVIDENCE_HEAD, BOB_CONTRACT_BLOB, BOB_AMENDMENT_BLOB,
        "B_ob(lambda) < 0 for every lambda in [9/20,5/8]",
    )
    ok = all(x in text for x in required) and blob == BOB_RECEIPT_BLOB
    print("C1B_BOB_PIN_CHECK", "PASS" if ok else "FAIL",
          "receipt_blob", blob, "expected_receipt_blob", BOB_RECEIPT_BLOB,
          "evidence_head", BOB_EVIDENCE_HEAD,
          "contract_blob", BOB_CONTRACT_BLOB, "amendment_blob", BOB_AMENDMENT_BLOB)
    if not ok:
        raise SystemExit("BOB_RECEIPT_PIN_FAIL")

def predictor_scan(slab):
    lm = (slab.ll + slab.lr) / 2
    prev_t = T_LO
    work = 0
    try:
        prev, c = g_box(prev_t, prev_t, lm, lm, PRED_SCAN_PANELS); work += c
        if not _arb_bounds_finite(prev):
            rec = _nonfinite_record("ARB_NONFINITE", "g_box", "PREDICTOR", "SCAN", slab.depth,
                                    prev_t, prev_t, lm, lm)
            print("C1B_PREDICTOR_NONFINITE", slab.coarse, slab.depth, rec)
            return None, work, rec
        prev_mid = prev.mid()
        for k in range(1, 513):
            t = T_LO + Fraction(k, PRED_GRID_DEN)
            v, c = g_box(t, t, lm, lm, PRED_SCAN_PANELS); work += c
            if not _arb_bounds_finite(v):
                rec = _nonfinite_record("ARB_NONFINITE", "g_box", "PREDICTOR", "SCAN", slab.depth,
                                        t, t, lm, lm)
                print("C1B_PREDICTOR_NONFINITE", slab.coarse, slab.depth, rec)
                return None, work, rec
            if prev_mid > 0 and v.mid() < 0:
                return (prev_t, t), work, None
            prev_t, prev_mid = t, v.mid()
    except REndpointDomainGuard as exc:
        rec = _nonfinite_record("R_ENDPOINT_DOMAIN_GUARD", "g_box", "PREDICTOR", "SCAN", slab.depth,
                                prev_t, prev_t, lm, lm, str(exc))
        print("C1B_PREDICTOR_NONFINITE", slab.coarse, slab.depth, rec)
        return None, work, rec
    return None, work, None

def select_predictor_candidate(continuation, bracket):
    if not isinstance(continuation, Fraction):
        raise TypeError("PREDICTOR_CONTINUATION_NOT_FRACTION")
    if bracket is None:
        return None, None
    s_lo, s_hi = bracket
    if not isinstance(s_lo, Fraction) or not isinstance(s_hi, Fraction):
        raise TypeError("PREDICTOR_SCAN_BRACKET_NOT_FRACTION")
    scan_mid = (s_lo + s_hi) / 2
    if abs(continuation - scan_mid) <= ROOT_TARGET:
        return continuation, "continuation"
    return scan_mid, "relocated"

def predictor_selection_controls():
    controls = (
        (Fraction(9,16), (Fraction(583,1024), Fraction(585,1024)), Fraction(9,16), "continuation"),
        (Fraction(9,16), (Fraction(584,1024), Fraction(586,1024)), Fraction(585,1024), "relocated"),
    )
    for index, (continuation, bracket, expected_tc, expected_mode) in enumerate(controls, 1):
        tc, mode = select_predictor_candidate(continuation, bracket)
        ok = tc == expected_tc and mode == expected_mode
        print("C1B_PREDICTOR_SELECTION_CONTROL", index, "PASS" if ok else "FAIL",
              "continuation", continuation, "bracket", bracket,
              "selected", tc, mode, "expected", expected_tc, expected_mode)
        if not ok:
            raise SystemExit("PREDICTOR_SELECTION_CONTROL_FAIL")


def root_nonfinite_controls():
    finite_cases = ((Fraction(3, 2), Fraction(3, 2)), (Fraction(-5, 8), Fraction(-5, 8)))
    ok1 = all(_arb_exact_fraction(base._point(src)) == expected for src, expected in finite_cases)
    print("C1B_ROOT_NONFINITE_CONTROL", 1, "PASS" if ok1 else "FAIL")
    if not ok1:
        raise SystemExit("ROOT_NONFINITE_CONTROL_FAIL")
    for index, value in ((2, arb("+inf")), (3, arb("nan"))):
        ok = False
        try:
            _arb_exact_fraction(value)
        except RuntimeError as exc:
            ok = str(exc) == "ROOT_NONFINITE_ARB_BOUND"
        print("C1B_ROOT_NONFINITE_CONTROL", index, "PASS" if ok else "FAIL")
        if not ok:
            raise SystemExit("ROOT_NONFINITE_CONTROL_FAIL")
    cand = _newton_candidate(Fraction(3, 4), arb("nan"), base._point(Fraction(-1, 2)))
    ok4 = cand is None
    print("C1B_ROOT_NONFINITE_CONTROL", 4, "PASS" if ok4 else "FAIL")
    if not ok4:
        raise SystemExit("ROOT_NONFINITE_CONTROL_FAIL")
    balls = (base._box(base._point(Fraction(-2)), base._point(Fraction(-1))),
             base._box(base._point(Fraction(1)), base._point(Fraction(3))))
    hull = _outward_hull(balls)
    expected_lo = min(_arb_exact_fraction(v.lower()) for v in balls)
    expected_hi = max(_arb_exact_fraction(v.upper()) for v in balls)
    ok5 = _arb_exact_fraction(hull.lower()) <= expected_lo and _arb_exact_fraction(hull.upper()) >= expected_hi
    print("C1B_ROOT_NONFINITE_CONTROL", 5, "PASS" if ok5 else "FAIL")
    if not ok5:
        raise SystemExit("ROOT_NONFINITE_CONTROL_FAIL")

def mono_closure_controls():
    controls = (
        ("L", -1, 1, 2, True),
        ("L", -1, 0, 2, False),
        ("L", 0, 1, 2, False),
        ("R", -1, -2, -1, True),
        ("R", -1, -2, 0, False),
    )
    for index, (side, gt_upper, wall_lower, wall_upper, expected) in enumerate(controls, 1):
        got = _mono_truth(side, gt_upper, wall_lower, wall_upper)
        ok = got is expected
        print("C1B_EXTERIOR_MONO_CONTROL", index, "PASS" if ok else "FAIL")
        if not ok:
            raise SystemExit("EXTERIOR_MONO_CONTROL_FAIL")
    invalid = (
        EBox("L", T_LO, Fraction(9, 16), L_LO, L_LO + DLAM),
        EBox("R", Fraction(9, 16), T_MID_HI, L_LO, L_LO + DLAM),
    )
    invalid_ok = True
    for box in invalid:
        try:
            _validate_mono_box_side(box, Fraction(17, 32), Fraction(19, 32))
            invalid_ok = False
        except RuntimeError as exc:
            invalid_ok = invalid_ok and str(exc) == "MONO_BOX_SIDE_INVALID"
    print("C1B_EXTERIOR_MONO_CONTROL", 6, "PASS" if invalid_ok else "FAIL")
    if not invalid_ok:
        raise SystemExit("EXTERIOR_MONO_CONTROL_FAIL")
    mono_work, skipped_cap, guards = MONO_WORK_CAP, 0, []
    if not _mono_cap_allows(mono_work, E_STAGES[-1][1]):
        skipped_cap += 1
    else:
        guards.append(("E2", "L_MONO", T_LO, T_LO, L_LO, L_LO, False))
    cap_ok = skipped_cap == 1 and not guards
    print("C1B_EXTERIOR_MONO_CONTROL", 7, "PASS" if cap_ok else "FAIL")
    if not cap_ok:
        raise SystemExit("EXTERIOR_MONO_CONTROL_FAIL")

def _nonfinite_record(kind, evaluator, side, stage, depth, tl, tr, ll, lr, detail=None):
    return {"kind": kind, "evaluator": evaluator, "side": side, "stage": stage,
            "depth": depth, "t": (tl, tr), "lambda": (ll, lr), "detail": detail}

def _checked_finite(value, evaluator, side, label, depth, tl, tr, ll, lr, nonfinite):
    if _arb_bounds_finite(value):
        return True
    nonfinite.append(_nonfinite_record("ARB_NONFINITE", evaluator, side, label, depth,
                                      tl, tr, ll, lr))
    return False

def tube_stage(slab, tc, stage):
    label, nt, nl, panels = stage
    tm, tp = max(T_LO, tc-W0), min(T_HI, tc+W0)
    lclamp, rclamp = tm == T_LO, tp == T_HI
    gt_bad = left_bad = right_bad = corner = cells = 0
    gt_worst = left_worst = right_worst = None
    guards, corner_boxes, nonfinite = [], [], []
    for tl, tr in split(tm, tp, nt):
        for ll, lr in split(slab.ll, slab.lr, nl):
            try:
                v, charts, c = gt_box(tl, tr, ll, lr, panels)
                cells += c; ch = int(charts.get("corner_hull", 0)); corner += ch
                finite = _checked_finite(v, "gt_box", "GT", label, slab.depth, tl, tr, ll, lr, nonfinite)
                good = finite and v.upper() < 0
                if ch:
                    corner_boxes.append((tl, tr, ll, lr))
                if not finite: v = None
            except REndpointDomainGuard as exc:
                nonfinite.append(_nonfinite_record("R_ENDPOINT_DOMAIN_GUARD", "gt_box", "GT", label,
                                                  slab.depth, tl, tr, ll, lr, str(exc)))
                v, good = None, False
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            guards.append((label, "GT", tl, tr, ll, lr, bool(good)))
            gt_bad += 0 if good else 1
            if v is not None and (gt_worst is None or v.upper() > gt_worst[0]):
                gt_worst = (v.upper(), tl, tr, ll, lr)
    for ll, lr in split(slab.ll, slab.lr, nl):
        try:
            v, c = g_box(tm, tm, ll, lr, panels); cells += c
            finite = _checked_finite(v, "g_box", "LEFT", label, slab.depth, tm, tm, ll, lr, nonfinite)
            good = finite and v.lower() > 0
            if not finite: v = None
        except REndpointDomainGuard as exc:
            nonfinite.append(_nonfinite_record("R_ENDPOINT_DOMAIN_GUARD", "g_box", "LEFT", label,
                                              slab.depth, tm, tm, ll, lr, str(exc)))
            v, good = None, False
        except (ValueError, ZeroDivisionError):
            v, good = None, False
        guards.append((label, "LEFT", tm, tm, ll, lr, bool(good)))
        left_bad += 0 if good else 1
        if v is not None and (left_worst is None or v.lower() < left_worst[0]):
            left_worst = (v.lower(), ll, lr)
        if not rclamp:
            try:
                v, c = g_box(tp, tp, ll, lr, panels); cells += c
                finite = _checked_finite(v, "g_box", "RIGHT", label, slab.depth, tp, tp, ll, lr, nonfinite)
                good = finite and v.upper() < 0
                if not finite: v = None
            except REndpointDomainGuard as exc:
                nonfinite.append(_nonfinite_record("R_ENDPOINT_DOMAIN_GUARD", "g_box", "RIGHT", label,
                                                  slab.depth, tp, tp, ll, lr, str(exc)))
                v, good = None, False
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            guards.append((label, "RIGHT", tp, tp, ll, lr, bool(good)))
            right_bad += 0 if good else 1
            if v is not None and (right_worst is None or v.upper() > right_worst[0]):
                right_worst = (v.upper(), ll, lr)
    ok = gt_bad == left_bad == right_bad == 0
    print("C1B_TUBE_STAGE", slab.coarse, slab.depth, slab.ll, slab.lr, label,
          "tc", tc, "walls", (tm, tp), "left_clamp", lclamp, "right_clamp", rclamp,
          "right_mode", "B_ob_receipt" if rclamp else "finite_t_wall",
          "gt_bad", gt_bad, "left_bad", left_bad, "right_bad", right_bad,
          "nonfinite", len(nonfinite), "corner_hull", corner,
          "gt_worst_upper", None if gt_worst is None else gt_worst[0].str(50),
          "left_worst_lower", None if left_worst is None else left_worst[0].str(50),
          "right_worst_upper", None if right_worst is None else right_worst[0].str(50))
    for rec in nonfinite:
        print("C1B_NONFINITE", rec)
    return ok, tm, tp, lclamp, rclamp, corner, cells, label, guards, corner_boxes, nonfinite

def tube_first_pass(slab, tc):
    total = corner = 0
    all_guards, all_corner_boxes, all_nonfinite = [], [], []
    last = None
    for stage in T_STAGES:
        out = tube_stage(slab, tc, stage)
        last = out; total += out[6]; corner += out[5]
        all_guards.extend(out[8]); all_corner_boxes.extend(out[9]); all_nonfinite.extend(out[10])
        if out[0]:
            print("C1B_TUBE_FIRST_PASS", slab.coarse, slab.depth, stage[0])
            return True, out[1], out[2], out[3], out[4], corner, total, stage[0], all_guards, all_corner_boxes, all_nonfinite
    return False, last[1], last[2], last[3], last[4], corner, total, None, all_guards, all_corner_boxes, all_nonfinite

def _outward_hull(values):
    if not values:
        raise RuntimeError("ROOT_EMPTY_GT_CELL_SET")
    lo = min(v.lower() for v in values)
    hi = max(v.upper() for v in values)
    return base._box(lo, hi)

def root_localize(slab, tm, tp):
    lo, hi, work = tm, tp, 0
    lambda_c = (slab.ll + slab.lr) / 2
    lambda_c_ball = base._point(lambda_c)
    dlambda = interval(slab.ll, slab.lr) - lambda_c_ball
    reason = "MAX_STEPS"
    steps = []
    for step in range(1, ROOT_MV_STEPS + 1):
        work_before = work
        if hi - lo <= ROOT_TARGET:
            reason = "TARGET_WIDTH"
            break
        t_ref = (lo + hi) / 2
        T_k = (lo, hi)
        G0 = Gt = Gl = Gpar = candidate = None
        gt_cells, gt_values = [], []
        gl_cells, gl_values = [], []
        gt_charts = defaultdict(int)
        gl_stats = defaultdict(int)
        try:
            work += ROOT_G_PANELS
            G0, _ = g_box(t_ref, t_ref, lambda_c, lambda_c, ROOT_G_PANELS)
            for cell_lo, cell_hi in split(lo, hi, ROOT_GT_T_CELLS):
                work += ROOT_GT_PANELS
                value, charts, _ = gt_box(cell_lo, cell_hi, slab.ll, slab.lr, ROOT_GT_PANELS)
                for key, count in charts.items():
                    gt_charts[key] += count
                gt_values.append(value)
                gt_cells.append({
                    "t_cell": (cell_lo, cell_hi),
                    "Gt": _arb_snapshot(value),
                    "guard": bool(value.upper() < 0),
                    "corner_hull": int(charts.get("corner_hull", 0)),
                    "work": ROOT_GT_PANELS,
                })
            Gt = _outward_hull(gt_values)
            for cell_lo, cell_hi in split(lo, hi, ROOT_GL_T_CELLS):
                work += ROOT_GL_PANELS
                value, stats, _ = glam_box(cell_lo, cell_hi, slab.ll, slab.lr, ROOT_GL_PANELS)
                for key, count in stats.items():
                    gl_stats[key] += count
                gl_values.append(value)
                gl_cells.append({
                    "t_cell": (cell_lo, cell_hi),
                    "Gl": _arb_snapshot(value),
                    "gl_stats": dict(stats),
                    "work": ROOT_GL_PANELS,
                })
            Gl = _outward_hull(gl_values)
        except REndpointDomainGuard as exc:
            reason = "MV_NONFINITE_ENCLOSURE"
            steps.append({
                "step": step, "T_k": T_k, "t_ref": t_ref, "lambda_c": lambda_c,
                "G0": None if G0 is None else _arb_snapshot(G0),
                "Gt": None if Gt is None else _arb_snapshot(Gt), "Gt_cells": gt_cells,
                "Gl": None if Gl is None else _arb_snapshot(Gl), "Gl_cells": gl_cells,
                "Gpar": None, "N_k": None, "T_next": None, "width": hi-lo,
                "division_guard": False, "empty_intersection": False,
                "gt_charts": dict(gt_charts), "gl_stats": dict(gl_stats),
                "nonfinite": {"kind": "R_ENDPOINT_DOMAIN_GUARD", "detail": str(exc)},
                "step_work": work-work_before,
            })
            print("C1B_ROOT_NONFINITE", slab.coarse, slab.depth, step, "kind",
                  "R_ENDPOINT_DOMAIN_GUARD", "detail", str(exc))
            break
        except (ValueError, ZeroDivisionError):
            reason = "MV_EVAL_UNRESOLVED"
            break
        Gpar = G0 + Gl * dlambda
        nonfinite = {
            "G0": not _arb_bounds_finite(G0),
            "Gt": not _arb_bounds_finite(Gt),
            "Gl": not _arb_bounds_finite(Gl),
            "Gpar": not _arb_bounds_finite(Gpar),
        }
        all_guards = all(cell["guard"] for cell in gt_cells)
        candidate = _newton_candidate(t_ref, Gpar, Gt) if all_guards and not any(nonfinite.values()) else None
        guard = candidate is not None
        base_rec = {
            "step": step, "T_k": T_k, "t_ref": t_ref, "lambda_c": lambda_c,
            "G0": _arb_snapshot(G0), "Gt": _arb_snapshot(Gt), "Gt_cells": gt_cells,
            "Gl": _arb_snapshot(Gl), "Gl_cells": gl_cells, "Gpar": _arb_snapshot(Gpar),
            "division_guard": guard, "gt_charts": dict(gt_charts), "gl_stats": dict(gl_stats),
            "nonfinite": nonfinite, "empty_intersection": False,
            "step_work": ROOT_G_PANELS + ROOT_GT_T_CELLS*ROOT_GT_PANELS + ROOT_GL_T_CELLS*ROOT_GL_PANELS,
        }
        if any(nonfinite.values()):
            base_rec.update({"N_k": None, "T_next": None, "width": hi-lo})
            steps.append(base_rec)
            reason = "MV_NONFINITE_ENCLOSURE"
            print("C1B_ROOT_MV_STEP", slab.coarse, slab.depth, step,
                  "guard", False, "reason", reason, "T_k", T_k, "t_ref", t_ref,
                  "lambda_c", lambda_c, "nonfinite", nonfinite)
            break
        if not guard:
            base_rec.update({"N_k": None, "T_next": None, "width": hi-lo})
            steps.append(base_rec)
            reason = "GT_DIVISION_GUARD_UNRESOLVED"
            print("C1B_ROOT_MV_STEP", slab.coarse, slab.depth, step,
                  "guard", False, "T_k", T_k, "t_ref", t_ref, "lambda_c", lambda_c)
            break
        try:
            new_lo, new_hi = _intersect_newton(lo, hi, candidate)
        except RuntimeError as exc:
            if str(exc) != "ROOT_EMPTY_INTERSECTION":
                raise
            base_rec.update({"N_k": _arb_snapshot(candidate), "T_next": None,
                             "width": hi-lo, "empty_intersection": True})
            steps.append(base_rec)
            raise
        base_rec.update({"N_k": _arb_snapshot(candidate), "T_next": (new_lo, new_hi),
                         "width": new_hi-new_lo})
        steps.append(base_rec)
        print("C1B_ROOT_MV_STEP", slab.coarse, slab.depth, step,
              "guard", True, "T_k", T_k, "t_ref", t_ref, "lambda_c", lambda_c,
              "T_next", (new_lo, new_hi), "width", new_hi-new_lo,
              "G0", G0.str(40), "Gt", Gt.str(40), "Gl", Gl.str(40),
              "Gpar", Gpar.str(40), "N_k", candidate.str(40))
        lo, hi = new_lo, new_hi
        if hi - lo <= ROOT_TARGET:
            reason = "TARGET_WIDTH"
            break
    ok = hi - lo <= ROOT_TARGET
    print("C1B_ROOT_ENCLOSURE", "PASS" if ok else "UNRESOLVED",
          slab.coarse, slab.depth, "T_star", (lo, hi), "width", hi-lo, "reason", reason)
    return ok, (lo, hi), work, steps, reason

def predictor_accept(tc, root):
    representative = (root[0] + root[1]) / 2
    err = abs(tc - representative)
    ok = err <= PRED_ACCEPT
    print("C1B_PREDICTOR_ACCEPT", "PASS" if ok else "FAIL",
          "tc", tc, "T_star", root, "representative", representative,
          "mid_error", err, "limit", PRED_ACCEPT)
    return ok, err

def _e0_counts(tm, tp):
    wl = max(Fraction(0), tm - T_LO)
    wr = max(Fraction(0), T_MID_HI - tp)
    if wl == 0 and wr == 0: return 0, 0
    if wl == 0: return 0, E0_TBOXES
    if wr == 0: return E0_TBOXES, 0
    q = Fraction(E0_TBOXES) * wl / (wl + wr)
    nl = max(1, min(23, q.numerator // q.denominator))
    return nl, E0_TBOXES - nl

def exterior_seed(slab, tm, tp):
    nl, nr = _e0_counts(tm, tp)
    out = []
    if nl:
        for tl, tr in split(T_LO, tm, nl):
            for ll, lr in split(slab.ll, slab.lr, E0_LBOXES):
                out.append(EBox("L", tl, tr, ll, lr))
    if nr:
        for tl, tr in split(tp, T_MID_HI, nr):
            for ll, lr in split(slab.ll, slab.lr, E0_LBOXES):
                out.append(EBox("R", tl, tr, ll, lr))
    print("C1B_E0_ALLOCATION", slab.coarse, slab.depth, "left_t_boxes", nl, "right_t_boxes", nr,
          "left_range", (T_LO, tm), "right_range", (tp, T_MID_HI))
    return out

def e_children(b):
    tm, lm = (b.tl+b.tr)/2, (b.ll+b.lr)/2
    return [EBox(b.side, a, c, d, e) for a,c in ((b.tl,tm),(tm,b.tr))
            for d,e in ((b.ll,lm),(lm,b.lr))]

def _mono_truth(side, gt_upper, wall_lower, wall_upper):
    if side == "L":
        return gt_upper < 0 and wall_lower > 0
    if side == "R":
        return gt_upper < 0 and wall_upper < 0
    raise RuntimeError("MONO_BOX_SIDE_INVALID")

def _mono_cap_allows(mono_work, panels):
    return mono_work + 2 * panels <= MONO_WORK_CAP

def _validate_mono_box_side(box, tm, tp):
    if box.side == "L":
        if box.tr > tm:
            raise RuntimeError("MONO_BOX_SIDE_INVALID")
    elif box.side == "R":
        if box.tl < tp:
            raise RuntimeError("MONO_BOX_SIDE_INVALID")
    else:
        raise RuntimeError("MONO_BOX_SIDE_INVALID")

def mono_closure_box(box, tm, tp, panels):
    _validate_mono_box_side(box, tm, tp)
    if box.side == "L":
        gt, _, _ = gt_box(box.tl, tm, box.ll, box.lr, panels)
        wall, _ = g_box(tm, tm, box.ll, box.lr, panels)
    else:
        gt, _, _ = gt_box(tp, box.tr, box.ll, box.lr, panels)
        wall, _ = g_box(tp, tp, box.ll, box.lr, panels)
    closed = _mono_truth(box.side, gt.upper(), wall.lower(), wall.upper())
    return closed, gt, wall

def eval_exterior(boxes, panels, label, tm, tp, mono_work, depth):
    unresolved, resolved, work, worstL, worstR = [], [], 0, None, None
    sign_guards, mono_guards, nonfinite = [], [], []
    for box in boxes:
        try:
            value, c = g_box(box.tl, box.tr, box.ll, box.lr, panels); work += c
            finite = _checked_finite(value, "g_box", box.side, label, depth,
                                     box.tl, box.tr, box.ll, box.lr, nonfinite)
            good = finite and (value.lower() > 0 if box.side == "L" else value.upper() < 0)
            if not finite: value = None
        except REndpointDomainGuard as exc:
            nonfinite.append(_nonfinite_record("R_ENDPOINT_DOMAIN_GUARD", "g_box", box.side, label,
                                              depth, box.tl, box.tr, box.ll, box.lr, str(exc)))
            value, good = None, False
        except (ValueError, ZeroDivisionError):
            value, good = None, False
        sign_guards.append((label, box.side, box.tl, box.tr, box.ll, box.lr, bool(good)))
        (resolved if good else unresolved).append(box)
        if value is not None and box.side == "L" and (worstL is None or value.lower() < worstL):
            worstL = value.lower()
        if value is not None and box.side == "R" and (worstR is None or value.upper() > worstR):
            worstR = value.upper()

    mono_attempted = mono_closed = mono_skipped = stage_mono_work = 0
    worst_gt = None
    worst_wall = None
    still_unresolved = []
    ordered = sorted(unresolved, key=lambda b: ((tm - b.tr) if b.side == "L" else (b.tl - tp), b.ll, b.tl))
    for box in ordered:
        if not _mono_cap_allows(mono_work, panels):
            mono_skipped += 1; still_unresolved.append(box); continue
        mono_attempted += 1; mono_work += 2 * panels; stage_mono_work += 2 * panels; work += 2 * panels
        try:
            closed, gt, wall = mono_closure_box(box, tm, tp, panels)
            finite_gt = _arb_bounds_finite(gt); finite_wall = _arb_bounds_finite(wall)
            if not finite_gt:
                nonfinite.append(_nonfinite_record("ARB_NONFINITE", "gt_box", box.side+"_MONO", label,
                                                  depth, box.tl, box.tr, box.ll, box.lr))
            if not finite_wall:
                nonfinite.append(_nonfinite_record("ARB_NONFINITE", "g_box", box.side+"_MONO", label,
                                                  depth, box.tl, box.tr, box.ll, box.lr))
            if not (finite_gt and finite_wall): closed, gt, wall = False, None, None
        except REndpointDomainGuard as exc:
            nonfinite.append(_nonfinite_record("R_ENDPOINT_DOMAIN_GUARD", "mono_closure_box", box.side+"_MONO",
                                              label, depth, box.tl, box.tr, box.ll, box.lr, str(exc)))
            closed, gt, wall = False, None, None
        except (ValueError, ZeroDivisionError):
            closed, gt, wall = False, None, None
        mono_guards.append((label, box.side + "_MONO", box.tl, box.tr, box.ll, box.lr, bool(closed)))
        if gt is not None and (worst_gt is None or gt.upper() > worst_gt): worst_gt = gt.upper()
        if wall is not None:
            wall_bound = wall.lower() if box.side == "L" else wall.upper()
            wall_margin = wall_bound if box.side == "L" else -wall_bound
            if worst_wall is None or wall_margin < worst_wall[0]: worst_wall = (wall_margin, wall_bound)
        if closed: mono_closed += 1; resolved.append(box)
        else: still_unresolved.append(box)
    mono_stats = {"attempted": mono_attempted, "closed": mono_closed, "skipped_cap": mono_skipped,
                  "work": stage_mono_work, "worst_gt_upper": worst_gt,
                  "worst_wall": None if worst_wall is None else worst_wall[1]}
    return still_unresolved, resolved, work, worstL, worstR, sign_guards + mono_guards, mono_work, mono_stats, nonfinite

def exterior_cover(slab, tm, tp):
    current = exterior_seed(slab, tm, tp)
    terminal, work, mono_work = 0, 0, 0
    all_guards, all_nonfinite = [], []
    if not current:
        print("C1B_EXTERIOR", slab.coarse, slab.depth, "EMPTY_REMAINDER", "PASS")
        return True, work, all_guards, all_nonfinite
    for idx, (label, panels) in enumerate(E_STAGES):
        unresolved, resolved, w, worstL, worstR, guards, mono_work, mono, nonfinite = eval_exterior(
            current, panels, label, tm, tp, mono_work, slab.depth)
        all_guards.extend(guards); all_nonfinite.extend(nonfinite)
        work += w; terminal += len(resolved)
        live_terminal = terminal + len(unresolved)
        print("C1B_EXTERIOR_STAGE", slab.coarse, slab.depth, label,
              "input", len(current), "resolved_now", len(resolved), "unresolved", len(unresolved),
              "live_terminal", live_terminal,
              "worst_left_lower", None if worstL is None else worstL.str(50),
              "worst_right_upper", None if worstR is None else worstR.str(50),
              "nonfinite", len(nonfinite))
        for rec in nonfinite:
            print("C1B_NONFINITE", rec)
        print("C1B_EXTERIOR_MONO", slab.coarse, slab.depth, label,
              "attempted", mono["attempted"], "closed", mono["closed"],
              "skipped_cap", mono["skipped_cap"], "work", mono["work"],
              "worst_gt_upper", None if mono["worst_gt_upper"] is None else mono["worst_gt_upper"].str(50),
              "worst_wall", None if mono["worst_wall"] is None else mono["worst_wall"].str(50))
        if live_terminal > E_BOX_CAP:
            return False, work, all_guards, all_nonfinite
        if not unresolved:
            print("C1B_EXTERIOR_FIRST_PASS", slab.coarse, slab.depth, label)
            return True, work, all_guards, all_nonfinite
        if idx == len(E_STAGES)-1:
            return False, work, all_guards, all_nonfinite
        current = [c for box in unresolved for c in e_children(box)]
        if terminal + len(current) > E_BOX_CAP:
            return False, work, all_guards, all_nonfinite
    return False, work, all_guards, all_nonfinite

def exact_middle_partition(tm, tp):
    pieces = []
    if T_LO < tm: pieces.append(("L", T_LO, tm))
    pieces.append(("TUBE", max(T_LO, tm), min(T_MID_HI, tp)))
    if tp < T_MID_HI: pieces.append(("R", tp, T_MID_HI))
    nonempty = [(k,a,b) for k,a,b in pieces if a < b]
    ok = bool(nonempty) and nonempty[0][1] == T_LO and nonempty[-1][2] == T_MID_HI \
         and all(x[2] == y[1] for x,y in zip(nonempty, nonempty[1:]))
    return ok, nonempty

def _tube_failure_reason(nonfinite):
    return "TUBE_NONFINITE" if nonfinite else "TUBE"

def _exterior_failure_reason(nonfinite):
    return "EXTERIOR_NONFINITE" if nonfinite else "EXTERIOR"

def _attempt_with_tc(slab, tc, mode, predictor_work):
    work = {"predictor":predictor_work, "tube":0, "root":0, "exterior":0}
    if tc is None:
        return False, None, None, None, work, "PREDICTOR"
    tok, tm, tp, lc, rc, corner, w, tstage, tube_guards, corner_boxes, tube_nonfinite = tube_first_pass(slab, tc); work["tube"] += w
    base_rec = {"slab":slab, "tc":tc, "mode":mode, "root":None, "sup_error":None,
                "tm":tm, "tp":tp, "left_clamp":lc, "right_clamp":rc,
                "corner_hull":corner, "corner_boxes":corner_boxes, "tube_stage":tstage,
                "tube_guards":tube_guards, "tube_nonfinite":tube_nonfinite, "exterior_guards":[],
                "exterior_nonfinite":[], "pieces":[],
                "root_steps":[], "root_reason":None}
    if not tok:
        return False, base_rec, None, tc, work, _tube_failure_reason(tube_nonfinite)
    rok, root, w, root_steps, root_reason = root_localize(slab, tm, tp); work["root"] += w
    base_rec.update({"root":root, "root_steps":root_steps, "root_reason":root_reason})
    if not rok:
        return False, base_rec, root, tc, work, "ROOT:" + root_reason
    aok, err = predictor_accept(tc, root)
    base_rec["sup_error"] = err
    if not aok:
        return False, base_rec, root, tc, work, "PREDICTOR_ACCEPT"
    eok, w, exterior_guards, exterior_nonfinite = exterior_cover(slab, tm, tp); work["exterior"] += w
    base_rec["exterior_guards"] = exterior_guards; base_rec["exterior_nonfinite"] = exterior_nonfinite
    if not eok:
        return False, base_rec, root, tc, work, _exterior_failure_reason(exterior_nonfinite)
    pok, pieces = exact_middle_partition(tm, tp)
    print("C1B_MIDDLE_T_PARTITION", "PASS" if pok else "FAIL", slab.coarse, slab.depth, pieces)
    base_rec["pieces"] = pieces
    if not pok:
        return False, base_rec, root, tc, work, "T_PARTITION"
    return True, base_rec, root, tc, work, "PASS"

def attempt_replay(slab, previous_root, expected_tc):
    # The producer-selected exact A.1 t_c is fixed replay input. Checker still
    # executes its own bracket scan for work/proof diagnostics, but cannot alter t_c.
    bracket, predictor_work, predictor_nonfinite = predictor_scan(slab)
    if predictor_nonfinite is not None:
        work = {"predictor": predictor_work, "tube": 0, "root": 0, "exterior": 0}
        rec = {"mode": None, "predictor_only": True, "predictor_nonfinite": [predictor_nonfinite]}
        return False, rec, None, expected_tc, work, "PREDICTOR_NONFINITE"
    if expected_tc is None:
        return _attempt_with_tc(slab, None, None, predictor_work)
    if not isinstance(expected_tc, Fraction):
        raise TypeError("CHECKER_REPLAY_TC_NOT_FRACTION")
    mode = "fixed_replay"
    print("C1B_PREDICTOR_REPLAY", slab.coarse, slab.depth, slab.ll, slab.lr,
          "P1", bracket, "fixed_t_c", expected_tc, "scan_cells", predictor_work)
    return _attempt_with_tc(slab, expected_tc, mode, predictor_work)

def diagnostic_controls():
    global g_box, gt_box, mono_closure_box
    slab=Slab(0,0,L_LO,L_LO+DLAM); tc=Fraction(9,16)
    saved_g, saved_gt, saved_mono = g_box, gt_box, mono_closure_box
    def guard(*args, **kwargs): raise REndpointDomainGuard("R_ENDPOINT_DOMAIN_GUARD")
    def unrelated(*args, **kwargs): raise RuntimeError("C1B_C6_UNRELATED")
    def gt_ok(*args, **kwargs): return arb(-1), {}, 1
    def g_zero(*args, **kwargs): return arb(0), 1
    results=[]
    try:
        # tube
        gt_box=gt_ok; g_box=guard
        out=tube_stage(slab,tc,("C6T",1,1,1)); caught=any(r["kind"]=="R_ENDPOINT_DOMAIN_GUARD" for r in out[10])
        g_box=unrelated; propagated=False
        try: tube_stage(slab,tc,("C6T",1,1,1))
        except RuntimeError as exc: propagated=(str(exc)=="C1B_C6_UNRELATED")
        results.append(("tube",caught and propagated))
        # exterior sign
        box=EBox("L",T_LO,tc,L_LO,L_LO+DLAM); g_box=guard
        out=eval_exterior([box],1,"C6E",tc,tc+W0,MONO_WORK_CAP,0); caught=any(r["kind"]=="R_ENDPOINT_DOMAIN_GUARD" for r in out[8])
        g_box=unrelated; propagated=False
        try: eval_exterior([box],1,"C6E",tc,tc+W0,MONO_WORK_CAP,0)
        except RuntimeError as exc: propagated=(str(exc)=="C1B_C6_UNRELATED")
        results.append(("exterior_sign",caught and propagated))
        # exterior MONO
        g_box=g_zero; mono_closure_box=guard
        out=eval_exterior([box],1,"C6M",tc,tc+W0,0,0); caught=any(r["kind"]=="R_ENDPOINT_DOMAIN_GUARD" for r in out[8])
        mono_closure_box=unrelated; propagated=False
        try: eval_exterior([box],1,"C6M",tc,tc+W0,0,0)
        except RuntimeError as exc: propagated=(str(exc)=="C1B_C6_UNRELATED")
        results.append(("exterior_mono",caught and propagated))
        # root g/Gl boundary
        mono_closure_box=saved_mono; g_box=guard; gt_box=saved_gt
        rok,root,work,steps,reason=root_localize(slab,T_LO,tc); caught=(not rok and reason=="MV_NONFINITE_ENCLOSURE" and steps and steps[-1].get("nonfinite",{}).get("kind")=="R_ENDPOINT_DOMAIN_GUARD")
        g_box=unrelated; propagated=False
        try: root_localize(slab,T_LO,tc)
        except RuntimeError as exc: propagated=(str(exc)=="C1B_C6_UNRELATED")
        results.append(("root",caught and propagated))
        # predictor
        g_box=guard; pout=attempt_replay(slab,None,tc)
        prec=pout[1]; caught=(pout[5]=="PREDICTOR_NONFINITE" and prec is not None and
                              prec.get("predictor_nonfinite", [{}])[0].get("kind")=="R_ENDPOINT_DOMAIN_GUARD")
        g_box=unrelated; propagated=False
        try: predictor_scan(slab)
        except RuntimeError as exc: propagated=(str(exc)=="C1B_C6_UNRELATED")
        results.append(("predictor",caught and propagated))
        # plain Arb non-finite values map to the dedicated terminal-reason classes.
        gt_box=gt_ok
        def g_nan(*args, **kwargs): return arb("nan"), 1
        g_box=g_nan
        tout=tube_stage(slab,tc,("C6N",1,1,1))
        box=EBox("L",T_LO,tc,L_LO,L_LO+DLAM)
        eout=eval_exterior([box],1,"C6N",tc,tc+W0,MONO_WORK_CAP,0)
        plain=(bool(tout[10]) and _tube_failure_reason(tout[10])=="TUBE_NONFINITE" and
               bool(eout[8]) and _exterior_failure_reason(eout[8])=="EXTERIOR_NONFINITE")
        results.append(("plain_nonfinite_reasons",plain))
    finally:
        g_box, gt_box, mono_closure_box = saved_g, saved_gt, saved_mono
    for label,ok in results: print("C1B_NONFINITE_DIAGNOSTIC_CONTROL",label,"PASS" if ok else "FAIL")
    if len(results)!=6 or not all(ok for _,ok in results): raise SystemExit("C1B_NONFINITE_DIAGNOSTIC_CONTROL_FAIL")

def empty_remainder_control():
    slab=Slab(0,0,L_LO,L_LO+DLAM)
    # Force exterior_seed to be empty by making the tube cover the full middle domain.
    out=exterior_cover(slab,T_LO,T_MID_HI)
    ok=(len(out)==4 and out[0] is True and out[1]==0 and out[2]==[] and out[3]==[])
    print("C1B_EMPTY_REMAINDER_CONTROL","PASS" if ok else "FAIL","arity",len(out),"value",out)
    if not ok: raise SystemExit("C1B_EMPTY_REMAINDER_CONTROL_FAIL")

def preflight():
    ok = (L_LO < L_HI and DLAM > 0 and N_COARSE == 140 and MAX_DEPTH == 3)
    print("GLOBAL_AXIAL_C1B_CHECKER — IMPLEMENTED_PROTOTYPE / MACHINE_NOT_RUN / NOT_BINDING")
    print("CHECKER_KERNEL TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION")
    print("INDEPENDENCE_SCOPE PRECISION/PARTITION/GATING")
    print("BITS", BITS, "DEG", DEG, "USTAR", USTAR)
    print("LAMBDA_DOMAIN", L_LO, L_HI, "direction increasing")
    print("FIXED_REPLAY_DOMAIN_CONTRACT", "PASS" if ok else "FAIL", "coarse_count", N_COARSE, "dlambda", DLAM, "max_depth", MAX_DEPTH)
    print("PREDICTOR_ORDER continuation -> bracket_scan -> relocated")
    print("PREDICTOR_ACCEPT", PRED_ACCEPT, "ROOT_TARGET", ROOT_TARGET)
    print("CLAMP_RULE", "max(1/2,tc-w0)", "min(1,tc+w0)", "w0", W0)
    print("CORNER_RULE", "tr==1 and first s-panel => checker corner_hull")
    print("T_STAGES", T_STAGES, "ROOT_MV", (ROOT_MV_STEPS,ROOT_G_PANELS,ROOT_GT_PANELS,ROOT_GL_PANELS), "ROOT_GT_T_CELLS", ROOT_GT_T_CELLS, "ROOT_GL_T_CELLS", ROOT_GL_T_CELLS)
    print("E_POLICY", E0_TBOXES, E0_LBOXES, E_STAGES, "cap", E_BOX_CAP)
    print("MONO_RULE left: Gt<0 on [a,t-]xL and G(t-)>0 => G>0 ; right: Gt<0 on [t+,b]xL and G(t+)<0 => G<0")
    print("MONO_WORK_CAP", MONO_WORK_CAP)
    print("CAPS", "coarse", N_COARSE, "accepted", MAX_ACCEPTED, "attempted", MAX_ATTEMPTED,
          "max_depth", MAX_DEPTH)
    print("WORK_CEILINGS", ATTEMPT_WORK_CEILING, ACCEPTED_WORK_CEILING, GLOBAL_ATTEMPT_WORK_CEILING)
    if not ok: raise SystemExit("PREFLIGHT_FAIL")
    numeric_import_closure_preflight()
    numeric_import_closure_controls()
    endpoint_light_controls()
    endpoint_regression_controls()
    v28_preflight_controls()
    diagnostic_controls()
    empty_remainder_control()
    predictor_selection_controls()
    root_nonfinite_controls()
    mono_closure_controls()
    bob_preflight()

