"""Isolated M40 calibration experiment (NOT a full-domain certificate).
Exact rational/dyadic interval arithmetic, fixed midpoint line estimate.
Do not run as a D5 production process or treat output as mathematical adoption.
"""
import sys, json, time, hashlib, argparse
from pathlib import Path
from fractions import Fraction as F
from math import comb
BASE=Path('/home/daybreak/bg-oblate-spheroid-c1b/research/astra/ASTRA_D5_M22_LOCAL_BOUND_CANDIDATES_20261105')
SHA='a9001a18f322c3d6f1ad3d7afc025f9f82b92f228572177977f31d649d6d46fc'
assert hashlib.sha256((BASE/'pilot.py').read_bytes()).hexdigest()==SHA, 'upstream evaluator changed'
sys.path.insert(0,str(BASE))
from pilot import I,J,SCALE,ipadd,ipmul,ips,ish,moment
ROOT=Path(__file__).resolve().parent
CONTRACT=json.loads((ROOT/'calibration_contract.json').read_text())
assert CONTRACT['moment_N']==24 and CONTRACT['bits']==128
Z=I(0)
def interval(q): return F(q.lo,SCALE),F(q.hi,SCALE)
def upper_root(q):
    return F(I(q).sqrt().hi,SCALE)
def physical_q_cap(ll,lh,rh,zh):
    # All parameters are exact rationals. Upper roots are dyadic rational.
    rr=upper_root(rh*rh+(zh/ll)**2) if rh or zh else F(0)
    pp=upper_root(rh*rh+zh*zh) if rh or zh else F(0)
    if rr>=1:raise ValueError('r_box>=1')
    ff=((1+lh*lh)/2+pp)/(ll*(1-rr))
    qc=(ff-1)/(ff+1)
    if qc<0 or qc>=1:raise ValueError('q_cap out of [0,1): '+str(qc))
    return rr,pp,ff,qc

def poly(ks):return [x if isinstance(x,J) else J(x) for x in ks]
def extract(ks,i,j,scale=1):return [k.c[i,j]*scale for k in ks]
def theta_curv(n,q,axis):
    q0=q.c[0,0]
    ix=(1,0) if axis=='u' else (0,1)
    ix2=(2,0) if axis=='u' else (0,2)
    q1=q.c[ix];q2=2*q.c[ix2]
    nn=extract(n,0,0);n1=extract(n,*ix);n2=extract(n,*ix2,scale=2)
    yy=[I(1),q0]
    p1=ipmul(ipmul(yy,yy),n2)
    p2=ips(ish(ipmul(yy,n1),1),-8*q1)
    p3=ipmul(ipadd(ips(ish([I(1)],2),20*q1*q1),
                    ips(ish(yy,1),-4*q2)),nn)
    out=ipadd(ipadd(p1,p2),p3)
    assert len(out)==6
    return out

def kernel(u_lo,u_hi,t_lo,t_hi,ll,lh,rl,rh,zl,zh,em,ec,geom):
    u=J.var(I(u_lo,u_hi),0);t=J.var(I(t_lo,t_hi),1)
    lam=J(I(ll,lh));rho=J(I(rl,rh));z=J(I(zl,zh))
    U=1+u*u;T=1+t*t
    mu=(em*(1-u*u)/U).cap(-1,1)
    sinth=(2*u/U).cap(0,1)
    cosphi=ec*(1-t*t)/T
    sinphi=2*t/T
    xx=(sinth*cosphi).cap(-1,1)
    yy=(sinth*sinphi).cap(0,1)
    jac=4*u/(U*U)
    kt=2/T
    wsq=(lam*lam+(1-lam*lam)*mu*mu).cap(ll*ll,1)
    w=wsq.sqrt()
    ss=(1-(1-lam*lam)*mu*mu-2*rho*xx-2*lam*z*mu+rho*rho+z*z)
    rbox,pbox,_,qcap=geom
    ss=ss.cap((ll*(1-rbox))**2,(1+pbox)**2)
    d=ss.sqrt()
    h=(lam-lam*rho*xx-z*mu).cap(ll*(1-rbox),lh*(1+rbox))
    br=xx-rho;h1=-lam*xx
    dn=[J(0),1/d]
    for n in range(4):
        # d_{n+1}=((2n+1)*br*d_n-n*d_{n-1})/((n+1)*S)
        dn.append(((2*n+1)*br*dn[-1]-n*dn[-2])/((n+1)*ss))
    assert len(dn)==6
    g=[(h*dn[n+1]+h1*dn[n])/w for n in range(5)]
    aa=1+g[0]
    bb=(1-lam*lam)*mu+lam*z
    L=w*d+h
    qsos=(yy*yy*bb*bb+(xx*bb-mu*rho)**2+lam*lam*rho*rho*yy*yy)/(L*L)
    q=qsos.cap(0,qcap)
    # By cross-product Gram identity q=(1-g0)/(1+g0), here computed
    # via SOS to avoid subtraction near q=0.
    b0=h*g[4]+h1*g[3]
    b1=-h*(g[1]*g[3]+g[2]*g[2]/2)-h1*g[1]*g[2]
    b2=h*g[1]*g[1]*g[2]+h1*g[1]**3/3
    b3=-h*g[1]**4/4
    d0,d1,d2,d3=b0/aa,b1/aa**2,b2/aa**3,b3/aa**4
    v0=d0+d1+d2+d3
    v1=3*q*d0+(2*q-1)*d1+(q-2)*d2-3*d3
    v2=3*q*q*d0+(q*q-2*q)*d1+(1-2*q)*d2+3*d3
    v3=q**3*d0-q*q*d1+q*d2-d3
    n=[(-96)*jac*kt*v for v in (v0,v1,v2,v3)]
    return q.c[0,0],[x.c[0,0] for x in n],theta_curv(n,q,'u'),theta_curv(n,q,'t')

def lower_pi_prefactor(raw,ll,lh):
    # 333/106 < pi < 355/113.
    return raw*F(113,710*lh) if raw>=0 else raw*F(53,333*ll)

def run_case(case,cells):
    ll,lh=map(F,case['lambda']);rl,rh=map(F,case['rho']);zl,zh=map(F,case['z'])
    rbox,pbox,ff,qcap=physical_q_cap(ll,lh,rh,zh)
    geom=(rbox,pbox,ff,qcap)
    h=F(1,cells);now=time.monotonic()
    middle=F(0);curve=F(0);tail=F(0)
    # Center-line in t, full u for the uu term; centered u for the tt term.
    # Integral lower bound: h^2 [ F(mid) + h^2/24 F_uu(C)
    #                                   + h^2/24 F_tt(u_mid,t_cell)].
    for em in (-1,1):
        for ec in (-1,1):
            for ui in range(cells):
                ul=F(ui,cells);uh=F(ui+1,cells);um=(ul+uh)/2
                for ti in range(cells):
                    tl=F(ti,cells);th=F(ti+1,cells);tm=(tl+th)/2
                    qm,nm,_,_=kernel(um,um,tm,tm,ll,lh,rl,rh,zl,zh,em,ec,geom)
                    qc,_,nu,_=kernel(ul,uh,tl,th,ll,lh,rl,rh,zl,zh,em,ec,geom)
                    qt,_,_,nt=kernel(um,um,tl,th,ll,lh,rl,rh,zl,zh,em,ec,geom)
                    mm,fm,tm_loss,_=moment(nm,4,qm)
                    uu,fu,tu_loss,_=moment(nu,6,qc)
                    tt,ft,tt_loss,_=moment(nt,6,qt)
                    area=h*h;fac=area*h*h/24
                    middle+=area*F(fm.lo,SCALE)
                    curve+=fac*(F(fu.lo,SCALE)+F(ft.lo,SCALE))
                    tail+=area*F(tm_loss,SCALE)+fac*(F(tu_loss,SCALE)+F(tt_loss,SCALE))
                # Output only after an entire u row.
                print('PROGRESS',case['name'],cells,em,ec,ui+1,'/',cells,flush=True)
    raw=middle+curve-tail
    out=dict(name=case['name'],cells_u=cells,cells_t=cells,lambda_box=case['lambda'],
        rho_box=case['rho'],z_box=case['z'],r_box=str(rbox),P=str(pbox),
        F=str(ff),q_plus=str(qcap),raw_lower=str(raw),
        lower=str(lower_pi_prefactor(raw,ll,lh)),midpoint=str(middle),
        curvature=str(curve),tail_loss=str(tail),
        elapsed_seconds=time.monotonic()-now,
        meets_minus_400=lower_pi_prefactor(raw,ll,lh)>=-400)
    print('RESULT',case['name'],cells,'LOWER',float(F(out['lower'])),
        'MID',float(middle),'CURV',float(curve),'TAIL',float(tail),
        'TIME',out['elapsed_seconds'],flush=True)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--cells',type=int,choices=(16,32),default=16)
    ap.add_argument('--case',choices=[c['name'] for c in CONTRACT['cases']]+['all'],default='all')
    opts=ap.parse_args()
    results={'contract_sha256':hashlib.sha256((ROOT/'calibration_contract.json').read_bytes()).hexdigest(),
             'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'upstream_moment_sha256':SHA,'cases':[],'status':'CALIBRATION_ONLY'}
    for case in CONTRACT['cases']:
        if opts.case!='all' and case['name']!=opts.case:continue
        results['cases'].append(run_case(case,opts.cells))
        f=ROOT/('calibration_result_'+str(opts.cells)+'_'+opts.case+'.json')
        f.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
