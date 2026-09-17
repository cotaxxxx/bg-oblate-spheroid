#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_BINDING coarse transverse-monotonicity scan.

Uses the existing MeridianEvaluator.  This is reconnaissance only: binary64,
finite grid, no interval certification.
"""
import math
import numpy as np
from analysis.meridian_off_axis_scan import MeridianEvaluator

LAMBDAS = [0.40,0.50,0.5819,0.80,0.95,0.99,1.01,1.05,1.20,2.0,2.0654,3.0,5.0]
NQ = 24
NTH = 24
NMU = 120
NPHI = 192


def main():
    print('MERIDIAN TRANSVERSE COARSE — DIAGNOSTIC_ONLY / NOT_BINDING')
    print('grid',NQ,NTH,'quadrature',NMU,NPHI)
    for lam in LAMBDAS:
        ev=MeridianEvaluator(lam,NMU,NPHI)
        vals=[]
        loc=[]
        # q up to .985 deliberately probes a coarse near-boundary layer.
        for q in np.linspace(0.03,0.985,NQ):
            for th in np.linspace(0.03,math.pi/2-0.03,NTH):
                _,_,Er,Ez,viol=ev.gradient_qtheta(float(q),float(th))
                r=q*math.sin(th); z=lam*q*math.cos(th)
                if lam < 1:
                    v=Er/r
                elif lam > 1:
                    v=Ez/z
                else:
                    continue
                if not math.isfinite(v):
                    print('NONFINITE',lam,q,th,v); raise SystemExit(2)
                vals.append(v); loc.append((q,th,r,z,viol))
        a=np.asarray(vals)
        k=int(np.argmin(a)); q,th,r,z,viol=loc[k]
        print(f'lambda={lam:.6g} component={"Er/r" if lam<1 else "Ez/z"} '
              f'min={a.min():+.12e} max={a.max():+.12e} all_positive={bool(np.all(a>0))} '
              f'min_q={q:.6f} min_theta={th:.6f} min_r={r:.6f} min_z={z:.6f} clamp={viol:.3e}')

if __name__=='__main__': main()
