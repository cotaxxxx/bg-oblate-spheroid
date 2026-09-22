#!/home/daybreak/.pyenv/versions/3.11.16/bin/python
"""D-OB P2 producer. Implements sealed SPEC V2 and PRE-RUN CONTRACT V2."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import multiprocessing as mp
import os
import sys
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

from flint import arb, ctx

BITS = 160
GAMMA_STAR = Q(7, 10)
MAX_CELL_COUNT = 2**16
MAX_CELL_DEPTH = 10
MAX_BOX_DEPTH = 12
RHO0 = Q(1, 8)
NWORKERS = 12
N_MU = 64
N_PHI = 32
N_INITIAL_CELLS = N_MU * N_PHI

ctx.prec = BITS
PI = arb.pi()
C1 = PI * PI / 4 + 2 * PI
C2 = 9 * PI + 8


def aq(q: Q) -> arb:
    return arb(q.numerator) / q.denominator


def boxq(lo: Q, hi: Q) -> arb:
    lo_a, hi_a = aq(lo), aq(hi)
    return (lo_a + hi_a) / 2 + arb(0, (hi_a - lo_a) / 2)


def hull(x: arb, y: arb) -> arb:
    lo = min(x.lower(), y.lower())
    hi = max(x.upper(), y.upper())
    return (lo + hi) / 2 + arb(0, (hi - lo) / 2)


def intersect(x: arb, lo: Q, hi: Q) -> arb:
    a, b = max(x.lower(), aq(lo)), min(x.upper(), aq(hi))
    if a > b:
        raise ValueError("empty interval intersection")
    return (a + b) / 2 + arb(0, (b - a) / 2)


def sq_nonnegative(x: arb) -> arb:
    lo, hi = x.lower(), x.upper()
    if lo <= 0 <= hi:
        top = max(lo * lo, hi * hi)
        return (top / 2) + arb(0, top / 2)
    return hull(lo * lo, hi * hi)


def pos_pow(x: arb, k: int) -> arb:
    lo, hi = x.lower(), x.upper()
    if not lo > 0:
        raise ValueError("pos_pow")
    return hull(lo**k, hi**k)


def pos_mul(x: arb, y: arb) -> arb:
    xl, xh, yl, yh = x.lower(), x.upper(), y.lower(), y.upper()
    if not (xl > 0 and yl > 0):
        raise ValueError("pos_mul")
    return hull(xl*yl, xh*yh)


def finite_ball(x: arb) -> bool:
    try:
        x.lower().man_exp(); x.upper().man_exp()
        return True
    except Exception:
        return False


def width(x: arb) -> arb:
    return x.upper() - x.lower()


def _dyadic(a: arb) -> Q:
    m,e=a.man_exp()
    m,e=int(m),int(e)
    return Q(m*(1<<e),1) if e>=0 else Q(m,1<<(-e))


def exact_upper(x: arb) -> Q:
    return _dyadic(x.mid()) + _dyadic(x.rad())


def qstr(q: Q) -> str:
    return f"{q.numerator}/{q.denominator}"


def ceil_sqrt_fraction_scaled(r2: Q) -> Q:
    if r2 <= 0:
        raise ValueError("R2 must be positive")
    n, d = r2.numerator, r2.denominator
    target_num = n * (1 << 64)
    k = math.isqrt(target_num // d)
    while k * k * d < target_num:
        k += 1
    while k > 0 and (k - 1) * (k - 1) * d >= target_num:
        k -= 1
    return Q(k, 1 << 32)


@dataclass(frozen=True)
class PBox:
    r0: Q; r1: Q
    t0: Q; t1: Q
    l0: Q; l1: Q
    depth: int

    def bounds(self):
        rho_lo = self.r0 * (1 - self.t1*self.t1) / (1 + self.t1*self.t1)
        rho_hi = self.r1 * (1 - self.t0*self.t0) / (1 + self.t0*self.t0)
        z_lo = self.l0 * self.r0 * 2*self.t0 / (1 + self.t0*self.t0)
        z_hi = self.l1 * self.r1 * 2*self.t1 / (1 + self.t1*self.t1)
        return rho_lo, rho_hi, z_lo, z_hi

    def column(self):
        a, b, _, _ = self.bounds()
        if a >= RHO0:
            return "far"
        if b <= 2*RHO0:
            return "near"
        return "straddle"

    def split(self):
        wr, wt = self.r1-self.r0, self.t1-self.t0
        wl = (self.l1-self.l0) / Q(13, 50)
        if wr >= wt and wr >= wl:
            m=(self.r0+self.r1)/2
            return (PBox(self.r0,m,self.t0,self.t1,self.l0,self.l1,self.depth+1),
                    PBox(m,self.r1,self.t0,self.t1,self.l0,self.l1,self.depth+1))
        if wt >= wl:
            m=(self.t0+self.t1)/2
            return (PBox(self.r0,self.r1,self.t0,m,self.l0,self.l1,self.depth+1),
                    PBox(self.r0,self.r1,m,self.t1,self.l0,self.l1,self.depth+1))
        m=(self.l0+self.l1)/2
        return (PBox(self.r0,self.r1,self.t0,self.t1,self.l0,m,self.depth+1),
                PBox(self.r0,self.r1,self.t0,self.t1,m,self.l1,self.depth+1))


@dataclass(frozen=True)
class Cell:
    m0: Q; m1: Q
    p0: Q; p1: Q
    depth: int

    def area(self):
        return aq((self.m1-self.m0)*(self.p1-self.p0))*PI

    def order_key(self):
        return (self.m0, self.p0, self.m1, self.p1)

    def split(self):
        mm=(self.m0+self.m1)/2; pm=(self.p0+self.p1)/2; d=self.depth+1
        return (Cell(self.m0,mm,self.p0,pm,d), Cell(self.m0,mm,pm,self.p1,d),
                Cell(mm,self.m1,self.p0,pm,d), Cell(mm,self.m1,pm,self.p1,d))


def initial_cells():
    out=[]
    for i in range(N_MU):
        m0=Q(-1)+Q(2*i,N_MU); m1=Q(-1)+Q(2*(i+1),N_MU)
        for j in range(N_PHI):
            out.append(Cell(m0,m1,Q(j,N_PHI),Q(j+1,N_PHI),0))
    return out


def centre_radius(B: PBox, column: str):
    r0,r1,z0,z1=B.bounds(); zc=(z0+z1)/2
    if column=="far":
        rc=(r0+r1)/2
        r2=((r1-r0)/2)**2+((z1-z0)/2)**2
        R=ceil_sqrt_fraction_scaled(r2)
        return (rc,zc),(-rc,zc),R
    r2=r1*r1+((z1-z0)/2)**2
    R=ceil_sqrt_fraction_scaled(r2)
    return (Q(0),zc),None,R


def surface_intervals(cell: Cell, B: PBox):
    mu=boxq(cell.m0,cell.m1)
    phi=PI*boxq(cell.p0,cell.p1)
    mx2=max(cell.m0*cell.m0, cell.m1*cell.m1)
    mn2=Q(0) if cell.m0<=0<=cell.m1 else min(cell.m0*cell.m0, cell.m1*cell.m1)
    a=hull(aq(1-mx2).sqrt(), aq(1-mn2).sqrt())
    cp=phi.cos(); sp=phi.sin()
    lam=boxq(B.l0,B.l1)
    return mu,a,cp,sp,lam


def distance2(cell: Cell, B: PBox, centre):
    mu,a,cp,sp,lam=surface_intervals(cell,B)
    cx,cz=centre
    x=a*cp; y=a*sp; zz=lam*mu
    return sq_nonnegative(x-aq(cx))+sq_nonnegative(y)+sq_nonnegative(zz-aq(cz))


def regular_flags(cell: Cell, B: PBox, column, c, cbar, R):
    threshold=aq(4*R*R)
    try:
        okp=(distance2(cell,B,c)-threshold).lower() >= 0
        if column=="far":
            okm=(distance2(cell,B,cbar)-threshold).lower() >= 0
            return okp and okm, okp, okm
        return okp, okp, True
    except Exception:
        return False, False, False


def series_chart(gamma: arb):
    u=intersect(arb(1)-gamma*gamma,Q(0),Q(1))
    U=u.upper()
    coeff=[Q(1)]
    for n in range(80):
        coeff.append(coeff[-1]*Q((2*n+1)**2,(2*n+2)*(2*n+3)))
    R=arb(0); S=arb(0); upow=arb(1)
    powers=[upow]
    for _ in range(80):
        powers.append(powers[-1]*u)
    for n in range(80):
        R += aq(coeff[n])*powers[n]
    for n in range(1,80):
        S += aq(n*coeff[n])*powers[n-1]
    c80=aq(coeff[80])
    den=arb(1)-U
    if den.lower() <= 0:
        raise ValueError("series tail denominator")
    t0=c80*(U**80)/den
    t1=80*c80*(U**79)/den
    R += (t0/2)+arb(0,t0/2)
    S += (t1/2)+arb(0,t1/2)
    Rg=-2*gamma*S
    return R,Rg,u


def direct_chart(gamma: arb):
    u=intersect(arb(1)-gamma*gamma,Q(0),Q(1))
    if u.lower() <= 0:
        raise ValueError("direct u includes zero")
    R=gamma.acos()/u.sqrt()
    Rg=(gamma*R-1)/u
    return R,Rg,u


def chart(gamma: arb):
    gamma=intersect(gamma,Q(0),Q(1))
    gs=aq(GAMMA_STAR)
    if gamma.lower() >= gs:
        return series_chart(gamma)
    if gamma.upper() <= gs:
        return direct_chart(gamma)
    gd=intersect(gamma,Q(0),GAMMA_STAR)
    gsx=intersect(gamma,GAMMA_STAR,Q(1))
    Rd,Rgd,ud=direct_chart(gd)
    Rs,Rgs,us=series_chart(gsx)
    return hull(Rd,Rs),hull(Rgd,Rgs),hull(ud,us)


def kernel_point(rho: arb, z: arb, mu: arb, a: arb, cp: arb, sp: arb, lam: arb, second=False):
    b=a*cp
    w2=lam*lam*(arb(1)-sq_nonnegative(mu))+sq_nonnegative(mu)
    if w2.lower() <= 0: raise ValueError("w2")
    w=w2.sqrt()
    D2=sq_nonnegative(b-rho)+sq_nonnegative(a*sp)+sq_nonnegative(lam*mu-z)
    if D2.lower() <= 0: raise ValueError("D2")
    D=D2.sqrt()
    h=lam*(arb(1)-rho*b)-z*mu
    Dw=pos_mul(D,w)
    D3w=pos_mul(pos_pow(D,3),w)
    gamma=intersect(h/Dw,Q(0),Q(1))
    R,Rg,u=chart(gamma)
    G=u*R*R
    gr=-lam*b/Dw+h*(b-rho)/D3w
    if not second:
        out=-lam*b*G-2*h*R*gr
        if not finite_ball(out): raise ValueError("nonfinite kernel")
        return out
    wD3=pos_mul(w,pos_pow(D,3)); wD5=pos_mul(w,pos_pow(D,5))
    grr=(-2*lam*b*(b-rho)-h)/wD3+3*h*sq_nonnegative(b-rho)/wD5
    out=4*lam*b*R*gr-2*h*(Rg*sq_nonnegative(gr)+R*grr)
    if not finite_ball(out): raise ValueError("nonfinite kernel")
    return out


def kernel(cell: Cell, B: PBox, column):
    mu,a,cp,sp,lam=surface_intervals(cell,B)
    rlo,rhi,zlo,zhi=B.bounds()
    z=boxq(zlo,zhi)
    if column=="far":
        rp=boxq(rlo,rhi)
        rm=-rp
        fp=kernel_point(rp,z,mu,a,cp,sp,lam,False)
        fm=kernel_point(rm,z,mu,a,cp,sp,lam,False)
        den=2*rp
        if den.lower() <= 0: raise ValueError("rho denominator")
        return (fp-fm)/den
    rs=boxq(-rhi,rhi)
    return kernel_point(rs,z,mu,a,cp,sp,lam,True)


def classify_and_bound(B: PBox, cells):
    column=B.column()
    if column=="straddle": return None
    c,cbar,R=centre_radius(B,column)
    regular=[]; cut=[]; sum_p=arb(0); sum_m=arb(0); L=arb(0)
    for cell in cells:
        reg,okp,okm=regular_flags(cell,B,column,c,cbar,R)
        kval=None
        if reg:
            try: kval=kernel(cell,B,column)
            except Exception: reg=False; okp=False
        if reg:
            area=cell.area(); L += area*kval.lower()
            regular.append((cell,kval,area*width(kval)))
        else:
            cut.append(cell)
            area=cell.area()
            if column=="far":
                if not okp: sum_p += area
                if not okm: sum_m += area
    if column=="far":
        rho_lo=B.bounds()[0]
        Bcut=C1/aq(rho_lo)*(sum_p+sum_m)
    else:
        area=sum((c0.area() for c0 in cut),arb(0))
        Bcut=2*C2/aq(B.l0)*(4*PI*area).sqrt()
    accepted=(L-Bcut).lower()>0
    return dict(column=column,c=c,cbar=cbar,R=R,regular=regular,cut=cut,L=L,Bcut=Bcut,accepted=accepted)

def refine_cells(B: PBox):
    cells=initial_cells()
    while True:
        data=classify_and_bound(B,cells)
        if data["accepted"]: return cells,data
        cutset=set(data["cut"])
        cut_b=[c for c in cells if c in cutset and c.depth<MAX_CELL_DEPTH]
        reg_b=[x for x in data["regular"] if x[0].depth<MAX_CELL_DEPTH]
        nreg=len(reg_b)
        take=(nreg+3)//4
        reg_b.sort(key=lambda x:(-exact_upper(x[2]),x[0].order_key()))
        selected=set(cut_b+[x[0] for x in reg_b[:take]])
        if not selected or len(cells)+3*len(selected)>MAX_CELL_COUNT:
            return None,data
        new=[]
        for c in cells:
            new.extend(c.split() if c in selected else (c,))
        cells=new


def cell_tree(cells):
    leaves={(c.m0,c.m1,c.p0,c.p1):c for c in cells}
    bits=[]
    def walk(c):
        key=(c.m0,c.m1,c.p0,c.p1)
        if key in leaves:
            bits.append("0"); return
        bits.append("1")
        for ch in c.split(): walk(ch)
    for c in initial_cells(): walk(c)
    return "".join(bits)


def box_obj(B: PBox, cells, data):
    c,cbar,R=data["c"],data["cbar"],data["R"]
    return {
        "endpoints":[qstr(x) for x in (B.r0,B.r1,B.t0,B.t1,B.l0,B.l1)],
        "box_depth":B.depth,
        "column":data["column"],
        "c":[qstr(c[0]),"0/1",qstr(c[1])],
        "cbar":None if cbar is None else [qstr(cbar[0]),"0/1",qstr(cbar[1])],
        "R":qstr(R),
        "cell_tree":cell_tree(cells),
        "L":data["L"].str(40),
        "B_cut":data["Bcut"].str(40),
    }


def solve_initial(index):
    ctx.prec=BITS
    ir,it,il=index
    root=PBox(Q(ir,8),Q(ir+1,8),Q(it,8),Q(it+1,8),
              Q(2,5)+Q(il,4)*Q(13,50), Q(2,5)+Q(il+1,4)*Q(13,50),0)
    bits=[]; leaves=[]; unresolved=[]
    def walk(B):
        col=B.column()
        if col=="straddle":
            if B.depth>=MAX_BOX_DEPTH:
                bits.append("0"); unresolved.append(B); return
            bits.append("1")
            for ch in B.split(): walk(ch)
            return
        result,data=refine_cells(B)
        if result is not None:
            bits.append("0"); leaves.append(box_obj(B,result,data)); return
        if B.depth>=MAX_BOX_DEPTH:
            bits.append("0"); unresolved.append(B); return
        bits.append("1")
        for ch in B.split(): walk(ch)
    walk(root)
    return {"initial":[ir,it,il],"box_tree":"".join(bits),"leaves":leaves,
            "unresolved":len(unresolved)}


def all_indices():
    return [(i,j,k) for i in range(8) for j in range(8) for k in range(4)]


def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def write_certificate(results,outpath):
    with open(outpath,"wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as gz:
            for rec in results:
                clean={k:v for k,v in rec.items() if k!="unresolved"}
                gz.write((json.dumps(clean,sort_keys=True,separators=(",",":"))+"\n").encode())


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--run-dir",required=True)
    ap.add_argument("--workers",type=int,default=NWORKERS)
    ap.add_argument("--initial",action="append",help="smoke-only i,j,k restriction")
    args=ap.parse_args()
    ctx.prec=BITS
    run=Path(args.run_dir); run.mkdir(parents=True,exist_ok=True)
    indices=all_indices()
    if args.initial:
        indices=[tuple(map(int,s.split(","))) for s in args.initial]
    if args.workers==1:
        results=[solve_initial(i) for i in indices]
    else:
        with mp.Pool(args.workers) as pool:
            results=list(pool.imap(solve_initial,indices))
    cert=run/"certificate.jsonl.gz"
    write_certificate(results,cert)
    unresolved=sum(r["unresolved"] for r in results)
    summary={"bits":BITS,"gamma_star":"7/10","initial_boxes":len(indices),
             "accepted_leaves":sum(len(r["leaves"]) for r in results),
             "unresolved":unresolved,"certificate_sha256":sha256(cert)}
    with open(run/"producer_summary.json","w",encoding="utf-8",newline="\n") as f:
        json.dump(summary,f,sort_keys=True,indent=2); f.write("\n")
    print(json.dumps(summary,sort_keys=True))
    return 0 if unresolved==0 else 1


if __name__=="__main__":
    raise SystemExit(main())
