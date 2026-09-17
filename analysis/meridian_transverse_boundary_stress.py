#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_BINDING targeted transverse stress scan.

Targets the risk region identified by the coarse quotient scan:
near-boundary q and large prolate lambda. Binary64 finite grid only;
no interval certification.
"""
import math
import numpy as np
from analysis.meridian_off_axis_scan import MeridianEvaluator

LAMBDAS = [0.40,0.50,0.5819,0.80,0.95,0.99,1.01,1.05,1.20,2.0,2.0654,3.0,5.0,7.5,10.0,15.0,20.0]
QS = [0.970,0.985,0.992,0.996,0.998,0.999,0.9995]
NTH = 40
NMU = 180
NPHI = 288


def main():
    print('MERIDIAN TRANSVERSE BOUNDARY STRESS — DIAGNOSTIC_ONLY / NOT_BINDING')
    print('q_levels', QS, 'theta_grid', NTH, 'quadrature', NMU, NPHI)
    for lam in LAMBDAS:
        ev = MeridianEvaluator(lam, NMU, NPHI)
        best = None
        all_positive = True
        for q in QS:
            for th in np.linspace(0.015, math.pi/2-0.015, NTH):
                _,_,Er,Ez,viol = ev.gradient_qtheta(float(q),float(th))
                r=q*math.sin(th); z=lam*q*math.cos(th)
                v = Er/r if lam < 1 else Ez/z
                if not math.isfinite(v):
                    print('NONFINITE',lam,q,th,v); raise SystemExit(2)
                all_positive = all_positive and (v > 0)
                rec=(v,q,th,r,z,viol)
                if best is None or v < best[0]: best=rec
        v,q,th,r,z,viol=best
        print(f'lambda={lam:.6g} component={"Er/r" if lam<1 else "Ez/z"} '
              f'min={v:+.12e} all_positive={all_positive} min_q={q:.6f} '
              f'min_theta={th:.6f} min_r={r:.6f} min_z={z:.6f} clamp={viol:.3e}')

if __name__=='__main__': main()
