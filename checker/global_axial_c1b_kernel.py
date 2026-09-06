#!/usr/bin/env python3
"""Full-source 192-bit C1b checker.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Status: IMPLEMENTED_PROTOTYPE / MACHINE_NOT_RUN / NOT_BINDING.
"""
from __future__ import annotations
import argparse
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
E0_TBOXES, E0_LBOXES = 24, 8
E_STAGES = (("E0", 1024), ("E1", 2048), ("E2", 4096))
E_BOX_CAP = 4096
PRED_GRID_DEN, PRED_SCAN_PANELS = 1024, 256
ATTEMPT_WORK_CEILING = 23_560_192
GLOBAL_ATTEMPT_WORK_CEILING = 49_476_403_200
ACCEPTED_WORK_CEILING = 26_387_415_040
BOB_RECEIPT = Path("analysis/GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md")
BOB_EVIDENCE_HEAD = "25efb59b851eb9d7a3d5ce30309eb8903d976930"
BOB_CONTRACT_BLOB = "215193e2fc2a1abcf2aee2527c4c2e6f3176ea6c"
BOB_AMENDMENT_BLOB = "8e04e2efaf816bab9d9d1f3fd0a9d753538b31ad"
BOB_RECEIPT_BLOB = "0f19e3877b9675506ac8f35a5702147a84723c43"

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
    R, _, _, _ = base._R(u, gam, stats)
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

def _glam_density(s, t, lam, stats):
    s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = grouped._primitives(s, t, lam)
    R, Rg, _, _ = base._R(u, gam, stats)
    wlog = lam * eps / W2
    glam = gam * (1 / lam - wlog - lam * delta_sq / q)
    pref = lam / (W * q * rootq)
    nlam = -2 * lam * (mu * delta_sq + A * delta)
    preflam = pref * (1 / lam - wlog - 3 * lam * delta_sq / q)
    gt = pref * n
    gtlam = preflam * n + pref * nlam
    return s * (2 * mu * R * glam - 2 * A * (Rg * glam * gt + R * gtlam))

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

def _newton_candidate(t_ref, gpar, gt):
    if not gt.upper() < 0:
        return None
    return base._point(t_ref) - gpar / gt

def _intersect_newton(lo, hi, candidate):
    nlo = _arb_exact_fraction(candidate.lower())
    nhi = _arb_exact_fraction(candidate.upper())
    new_lo, new_hi = max(lo, nlo), min(hi, nhi)
    if new_hi < new_lo:
        raise RuntimeError("ROOT_EMPTY_INTERSECTION")
    return new_lo, new_hi

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
    prev, work = g_box(prev_t, prev_t, lm, lm, PRED_SCAN_PANELS)
    prev_mid = prev.mid()
    for k in range(1, 513):
        t = T_LO + Fraction(k, PRED_GRID_DEN)
        v, c = g_box(t, t, lm, lm, PRED_SCAN_PANELS)
        work += c
        if prev_mid > 0 and v.mid() < 0:
            return (prev_t, t), work
        prev_t, prev_mid = t, v.mid()
    return None, work

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

def tube_stage(slab, tc, stage):
    label, nt, nl, panels = stage
    tm, tp = max(T_LO, tc-W0), min(T_HI, tc+W0)
    lclamp, rclamp = tm == T_LO, tp == T_HI
    gt_bad = left_bad = right_bad = corner = cells = 0
    gt_worst = left_worst = right_worst = None
    guards, corner_boxes = [], []
    for tl, tr in split(tm, tp, nt):
        for ll, lr in split(slab.ll, slab.lr, nl):
            try:
                v, charts, c = gt_box(tl, tr, ll, lr, panels)
                cells += c; ch = int(charts.get("corner_hull", 0)); corner += ch; good = v.upper() < 0
                if ch:
                    corner_boxes.append((tl, tr, ll, lr))
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            guards.append((label, "GT", tl, tr, ll, lr, bool(good)))
            gt_bad += 0 if good else 1
            if v is not None and (gt_worst is None or v.upper() > gt_worst[0]):
                gt_worst = (v.upper(), tl, tr, ll, lr)
    for ll, lr in split(slab.ll, slab.lr, nl):
        try:
            v, c = g_box(tm, tm, ll, lr, panels); cells += c; good = v.lower() > 0
        except (ValueError, ZeroDivisionError):
            v, good = None, False
        guards.append((label, "LEFT", tm, tm, ll, lr, bool(good)))
        left_bad += 0 if good else 1
        if v is not None and (left_worst is None or v.lower() < left_worst[0]):
            left_worst = (v.lower(), ll, lr)
        if not rclamp:
            try:
                v, c = g_box(tp, tp, ll, lr, panels); cells += c; good = v.upper() < 0
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
          "corner_hull", corner,
          "gt_worst_upper", None if gt_worst is None else gt_worst[0].str(50),
          "left_worst_lower", None if left_worst is None else left_worst[0].str(50),
          "right_worst_upper", None if right_worst is None else right_worst[0].str(50))
    return ok, tm, tp, lclamp, rclamp, corner, cells, label, guards, corner_boxes

def tube_first_pass(slab, tc):
    total = corner = 0
    all_guards, all_corner_boxes = [], []
    last = None
    for stage in T_STAGES:
        out = tube_stage(slab, tc, stage)
        last = out; total += out[6]; corner += out[5]
        all_guards.extend(out[8]); all_corner_boxes.extend(out[9])
        if out[0]:
            print("C1B_TUBE_FIRST_PASS", slab.coarse, slab.depth, stage[0])
            return True, out[1], out[2], out[3], out[4], corner, total, stage[0], all_guards, all_corner_boxes
    return False, last[1], last[2], last[3], last[4], corner, total, None, all_guards, all_corner_boxes

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
        if hi - lo <= ROOT_TARGET:
            reason = "TARGET_WIDTH"
            break
        t_ref = (lo + hi) / 2
        T_k = (lo, hi)
        G0 = Gl = Gpar = candidate = None
        gt_cells = []
        gt_values = []
        gt_charts = defaultdict(int)
        gl_stats = {}
        empty_intersection = False
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
            work += ROOT_GL_PANELS
            Gl, gl_stats, _ = glam_box(lo, hi, slab.ll, slab.lr, ROOT_GL_PANELS)
        except (ValueError, ZeroDivisionError):
            reason = "MV_EVAL_UNRESOLVED"
            break
        Gpar = G0 + Gl * dlambda
        all_guards = all(cell["guard"] for cell in gt_cells)
        candidate = _newton_candidate(t_ref, Gpar, Gt) if all_guards else None
        guard = candidate is not None
        base_rec = {
            "step": step, "T_k": T_k, "t_ref": t_ref, "lambda_c": lambda_c,
            "G0": _arb_snapshot(G0), "Gt": _arb_snapshot(Gt), "Gt_cells": gt_cells,
            "Gl": _arb_snapshot(Gl), "Gpar": _arb_snapshot(Gpar),
            "division_guard": guard, "gt_charts": dict(gt_charts), "gl_stats": gl_stats,
            "empty_intersection": False,
            "step_work": ROOT_G_PANELS + ROOT_GT_T_CELLS*ROOT_GT_PANELS + ROOT_GL_PANELS,
        }
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

def eval_exterior(boxes, panels, label):
    unresolved, resolved, work, worstL, worstR = [], [], 0, None, None
    guards = []
    for box in boxes:
        try:
            value, c = g_box(box.tl, box.tr, box.ll, box.lr, panels); work += c
            good = value.lower() > 0 if box.side == "L" else value.upper() < 0
        except (ValueError, ZeroDivisionError):
            value, good = None, False
        guards.append((label, box.side, box.tl, box.tr, box.ll, box.lr, bool(good)))
        (resolved if good else unresolved).append(box)
        if value is not None and box.side == "L" and (worstL is None or value.lower() < worstL):
            worstL = value.lower()
        if value is not None and box.side == "R" and (worstR is None or value.upper() > worstR):
            worstR = value.upper()
    return unresolved, resolved, work, worstL, worstR, guards

def exterior_cover(slab, tm, tp):
    current = exterior_seed(slab, tm, tp)
    terminal, work = 0, 0
    all_guards = []
    if not current:
        print("C1B_EXTERIOR", slab.coarse, slab.depth, "EMPTY_REMAINDER", "PASS")
        return True, work, all_guards
    for idx, (label, panels) in enumerate(E_STAGES):
        unresolved, resolved, w, worstL, worstR, guards = eval_exterior(current, panels, label)
        all_guards.extend(guards)
        work += w; terminal += len(resolved)
        live_terminal = terminal + len(unresolved)
        print("C1B_EXTERIOR_STAGE", slab.coarse, slab.depth, label,
              "input", len(current), "resolved_now", len(resolved), "unresolved", len(unresolved),
              "live_terminal", live_terminal,
              "worst_left_lower", None if worstL is None else worstL.str(50),
              "worst_right_upper", None if worstR is None else worstR.str(50))
        if live_terminal > E_BOX_CAP:
            return False, work, all_guards
        if not unresolved:
            print("C1B_EXTERIOR_FIRST_PASS", slab.coarse, slab.depth, label)
            return True, work, all_guards
        if idx == len(E_STAGES)-1:
            return False, work, all_guards
        current = [c for box in unresolved for c in e_children(box)]
        if terminal + len(current) > E_BOX_CAP:
            return False, work, all_guards
    return False, work, all_guards

def exact_middle_partition(tm, tp):
    pieces = []
    if T_LO < tm: pieces.append(("L", T_LO, tm))
    pieces.append(("TUBE", max(T_LO, tm), min(T_MID_HI, tp)))
    if tp < T_MID_HI: pieces.append(("R", tp, T_MID_HI))
    nonempty = [(k,a,b) for k,a,b in pieces if a < b]
    ok = bool(nonempty) and nonempty[0][1] == T_LO and nonempty[-1][2] == T_MID_HI \
         and all(x[2] == y[1] for x,y in zip(nonempty, nonempty[1:]))
    return ok, nonempty

def _attempt_with_tc(slab, tc, mode, predictor_work):
    work = {"predictor":predictor_work, "tube":0, "root":0, "exterior":0}
    if tc is None:
        return False, None, None, None, work, "PREDICTOR"
    tok, tm, tp, lc, rc, corner, w, tstage, tube_guards, corner_boxes = tube_first_pass(slab, tc); work["tube"] += w
    base_rec = {"slab":slab, "tc":tc, "mode":mode, "root":None, "sup_error":None,
                "tm":tm, "tp":tp, "left_clamp":lc, "right_clamp":rc,
                "corner_hull":corner, "corner_boxes":corner_boxes, "tube_stage":tstage,
                "tube_guards":tube_guards, "exterior_guards":[], "pieces":[],
                "root_steps":[], "root_reason":None}
    if not tok:
        return False, base_rec, None, tc, work, "TUBE"
    rok, root, w, root_steps, root_reason = root_localize(slab, tm, tp); work["root"] += w
    base_rec.update({"root":root, "root_steps":root_steps, "root_reason":root_reason})
    if not rok:
        return False, base_rec, root, tc, work, "ROOT:" + root_reason
    aok, err = predictor_accept(tc, root)
    base_rec["sup_error"] = err
    if not aok:
        return False, base_rec, root, tc, work, "PREDICTOR_ACCEPT"
    eok, w, exterior_guards = exterior_cover(slab, tm, tp); work["exterior"] += w
    base_rec["exterior_guards"] = exterior_guards
    if not eok:
        return False, base_rec, root, tc, work, "EXTERIOR"
    pok, pieces = exact_middle_partition(tm, tp)
    print("C1B_MIDDLE_T_PARTITION", "PASS" if pok else "FAIL", slab.coarse, slab.depth, pieces)
    base_rec["pieces"] = pieces
    if not pok:
        return False, base_rec, root, tc, work, "T_PARTITION"
    return True, base_rec, root, tc, work, "PASS"

def attempt_replay(slab, previous_root, expected_tc):
    # The producer-selected exact A.1 t_c is fixed replay input. Checker still
    # executes its own bracket scan for work/proof diagnostics, but cannot alter t_c.
    bracket, predictor_work = predictor_scan(slab)
    if expected_tc is None:
        return _attempt_with_tc(slab, None, None, predictor_work)
    if not isinstance(expected_tc, Fraction):
        raise TypeError("CHECKER_REPLAY_TC_NOT_FRACTION")
    mode = "fixed_replay"
    print("C1B_PREDICTOR_REPLAY", slab.coarse, slab.depth, slab.ll, slab.lr,
          "P1", bracket, "fixed_t_c", expected_tc, "scan_cells", predictor_work)
    return _attempt_with_tc(slab, expected_tc, mode, predictor_work)

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
    print("T_STAGES", T_STAGES, "ROOT_MV", (ROOT_MV_STEPS,ROOT_G_PANELS,ROOT_GT_PANELS,ROOT_GL_PANELS), "ROOT_GT_T_CELLS", ROOT_GT_T_CELLS)
    print("E_POLICY", E0_TBOXES, E0_LBOXES, E_STAGES, "cap", E_BOX_CAP)
    print("CAPS", "coarse", N_COARSE, "accepted", MAX_ACCEPTED, "attempted", MAX_ATTEMPTED,
          "max_depth", MAX_DEPTH)
    print("WORK_CEILINGS", ATTEMPT_WORK_CEILING, ACCEPTED_WORK_CEILING, GLOBAL_ATTEMPT_WORK_CEILING)
    if not ok: raise SystemExit("PREFLIGHT_FAIL")
    predictor_selection_controls()
    bob_preflight()

