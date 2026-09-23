#!/home/daybreak/.pyenv/versions/3.11.16/bin/python
"""Independent D-OB P2 certificate checker for sealed SPEC V2."""
from __future__ import annotations
import argparse, gzip, hashlib, json, math, multiprocessing as mp
import os, fcntl, socket, signal, threading, time
from datetime import datetime, timezone
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from flint import arb, ctx

Q=Fraction
BITS=192
CUT=Q(5,8)
RHO0=Q(1,8)
N_MU,N_PHI=64,32
MAX_BOX_DEPTH=12
SMOKE=[(7,0,0),(7,7,0),(0,0,3),(3,3,1)]
ctx.prec=BITS
PI=arb.pi()
C1=PI*PI/4+2*PI
C2=9*PI+8

def ball(q): return arb(q.numerator)/q.denominator
def interval(lo,hi):
    a,b=ball(lo),ball(hi)
    return (a+b)/2+arb(0,(b-a)/2)
def join(x,y):
    a=min(x.lower(),y.lower()); b=max(x.upper(),y.upper())
    return (a+b)/2+arb(0,(b-a)/2)
def clip(x,lo,hi):
    a=max(x.lower(),ball(lo)); b=min(x.upper(),ball(hi))
    if a>b: raise ArithmeticError("empty intersection")
    return (a+b)/2+arb(0,(b-a)/2)
def square(x):
    a,b=x.lower(),x.upper()
    if a<=0<=b:
        u=max(a*a,b*b)
        return u/2+arb(0,u/2)
    return join(a*a,b*b)
def positive_power(x,k):
    lo,hi=x.lower(),x.upper()
    if not lo>0:raise ArithmeticError("positive power")
    return join(lo**k,hi**k)
def positive_product(x,y):
    xl,xh=x.lower(),x.upper();yl,yh=y.lower(),y.upper()
    if not (xl>0 and yl>0):raise ArithmeticError("positive product")
    return join(xl*yl,xh*yh)
def finite(x):
    try:
        x.lower().man_exp();x.upper().man_exp()
        return True
    except Exception:return False
def rational(s):
    n,d=s.split("/"); return Q(int(n),int(d))
def rtext(q): return f"{q.numerator}/{q.denominator}"
def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for z in iter(lambda:f.read(1048576),b""): h.update(z)
    return h.hexdigest()

@dataclass(frozen=True)
class Box:
    r0:Q;r1:Q;t0:Q;t1:Q;l0:Q;l1:Q;depth:int
    def physical(self):
        pl=self.r0*(1-self.t1**2)/(1+self.t1**2)
        ph=self.r1*(1-self.t0**2)/(1+self.t0**2)
        zl=self.l0*self.r0*2*self.t0/(1+self.t0**2)
        zh=self.l1*self.r1*2*self.t1/(1+self.t1**2)
        return pl,ph,zl,zh
    def kind(self):
        lo,hi,_,_=self.physical()
        if lo>=RHO0:return "far"
        if hi<=2*RHO0:return "near"
        return "straddle"
    def children(self):
        widths=(self.r1-self.r0,self.t1-self.t0,(self.l1-self.l0)/Q(13,50))
        k=max(range(3),key=lambda j:(widths[j],-j))
        if k==0:
            m=(self.r0+self.r1)/2
            return Box(self.r0,m,self.t0,self.t1,self.l0,self.l1,self.depth+1),Box(m,self.r1,self.t0,self.t1,self.l0,self.l1,self.depth+1)
        if k==1:
            m=(self.t0+self.t1)/2
            return Box(self.r0,self.r1,self.t0,m,self.l0,self.l1,self.depth+1),Box(self.r0,self.r1,m,self.t1,self.l0,self.l1,self.depth+1)
        m=(self.l0+self.l1)/2
        return Box(self.r0,self.r1,self.t0,self.t1,self.l0,m,self.depth+1),Box(self.r0,self.r1,self.t0,self.t1,m,self.l1,self.depth+1)

@dataclass(frozen=True)
class Cell:
    m0:Q;m1:Q;p0:Q;p1:Q;depth:int
    def kids(self):
        m=(self.m0+self.m1)/2;p=(self.p0+self.p1)/2;d=self.depth+1
        return Cell(self.m0,m,self.p0,p,d),Cell(self.m0,m,p,self.p1,d),Cell(m,self.m1,self.p0,p,d),Cell(m,self.m1,p,self.p1,d)
    def area(self): return ball((self.m1-self.m0)*(self.p1-self.p0))*PI

def roots():
    return [Cell(Q(-1)+Q(2*i,N_MU),Q(-1)+Q(2*(i+1),N_MU),Q(j,N_PHI),Q(j+1,N_PHI),0) for i in range(N_MU) for j in range(N_PHI)]

def radius(q):
    if q<=0: raise ArithmeticError("nonpositive R2")
    n,d=q.numerator,q.denominator
    k=math.isqrt((n*(1<<64))//d)
    while k*k*d<n*(1<<64):k+=1
    return Q(k,1<<32)

def geometry(B):
    lo,hi,z0,z1=B.physical(); z=(z0+z1)/2
    if B.kind()=="far":
        x=(lo+hi)/2; R=radius(((hi-lo)/2)**2+((z1-z0)/2)**2)
        return (x,z),(-x,z),R
    R=radius(hi**2+((z1-z0)/2)**2)
    return (Q(0),z),None,R

def surface(C,B):
    mu=interval(C.m0,C.m1); ph=PI*interval(C.p0,C.p1)
    qmax=max(C.m0*C.m0,C.m1*C.m1)
    qmin=Q(0) if C.m0<=0<=C.m1 else min(C.m0*C.m0,C.m1*C.m1)
    aa=join(ball(1-qmax).sqrt(),ball(1-qmin).sqrt())
    return mu,aa,ph.cos(),ph.sin(),interval(B.l0,B.l1)

def dist2(C,B,c):
    mu,a,co,si,la=surface(C,B); cx,cz=c
    return square(a*co-ball(cx))+square(a*si)+square(la*mu-ball(cz))

def analytic(g):
    g=clip(g,Q(0),Q(1)); u=clip(1-square(g),Q(0),Q(1))
    def ser(gg):
        uu=clip(1-square(gg),Q(0),Q(1)); U=uu.upper()
        cs=[Q(1)]
        for n in range(80):cs.append(cs[-1]*Q((2*n+1)**2,(2*n+2)*(2*n+3)))
        powers=[arb(1)]
        for n in range(80):powers.append(powers[-1]*uu)
        R=sum((ball(cs[n])*powers[n] for n in range(80)),arb(0))
        S=sum((ball(n*cs[n])*powers[n-1] for n in range(1,80)),arb(0))
        den=1-U
        if den.lower()<=0:raise ArithmeticError("series tail")
        e0=ball(cs[80])*U**80/den; e1=80*ball(cs[80])*U**79/den
        R+=e0/2+arb(0,e0/2);S+=e1/2+arb(0,e1/2)
        return R,-2*gg*S,uu
    def direct(gg):
        uu=clip(1-square(gg),Q(0),Q(1))
        if uu.lower()<=0:raise ArithmeticError("direct zero")
        R=gg.acos()/uu.sqrt()
        return R,(gg*R-1)/uu,uu
    q=ball(CUT)
    if g.lower()>=q:return ser(g)
    if g.upper()<=q:return direct(g)
    x=direct(clip(g,Q(0),CUT)); y=ser(clip(g,CUT,Q(1)))
    return join(x[0],y[0]),join(x[1],y[1]),join(x[2],y[2])

def Fder(r,z,mu,a,co,si,la,second):
    b=a*co
    w2=la*la*(1-square(mu))+square(mu)
    if w2.lower()<=0:raise ArithmeticError("w")
    w=w2.sqrt()
    d2=square(b-r)+square(a*si)+square(la*mu-z)
    if d2.lower()<=0:raise ArithmeticError("D")
    d=d2.sqrt(); h=la*(1-r*b)-z*mu
    dw=positive_product(d,w); d3w=positive_product(positive_power(d,3),w)
    g=clip(h/dw,Q(0),Q(1)); R,Rg,u=analytic(g); G=u*R*R
    gv=-la*b/dw+h*(b-r)/d3w
    if not second:
        out=-la*b*G-2*h*R*gv
        if not finite(out):raise ArithmeticError("nonfinite integrand")
        return out
    wd3=positive_product(w,positive_power(d,3));wd5=positive_product(w,positive_power(d,5))
    gvv=(-2*la*b*(b-r)-h)/wd3+3*h*square(b-r)/wd5
    out=4*la*b*R*gv-2*h*(Rg*square(gv)+R*gvv)
    if not finite(out):raise ArithmeticError("nonfinite integrand")
    return out

def K(C,B):
    mu,a,co,si,la=surface(C,B); lo,hi,z0,z1=B.physical(); z=interval(z0,z1)
    if B.kind()=="far":
        r=interval(lo,hi)
        return (Fder(r,z,mu,a,co,si,la,False)-Fder(-r,z,mu,a,co,si,la,False))/(2*r)
    return Fder(interval(-hi,hi),z,mu,a,co,si,la,True)

def parse_cells(code):
    pos=0; leaves=[]
    def one(C):
        nonlocal pos
        if pos>=len(code):raise ValueError("short cell_tree")
        b=code[pos];pos+=1
        if b=="0":leaves.append(C);return
        if b!="1":raise ValueError("bad cell bit")
        for ch in C.kids():one(ch)
    for C in roots():one(C)
    if pos!=len(code):raise ValueError("trailing cell_tree")
    return leaves

def parse_boxes(code,root):
    pos=0; leaves=[]
    def one(B):
        nonlocal pos
        if pos>=len(code):raise ValueError("short box_tree")
        b=code[pos];pos+=1
        if b=="0":leaves.append(B);return
        if b!="1":raise ValueError("bad box bit")
        if B.depth>=MAX_BOX_DEPTH:raise ValueError("split beyond depth")
        for ch in B.children():one(ch)
    one(root)
    if pos!=len(code):raise ValueError("trailing box_tree")
    return leaves

def check_leaf(B,obj):
    if B.kind()=="straddle":raise ValueError("straddle leaf")
    ep=[rtext(x) for x in (B.r0,B.r1,B.t0,B.t1,B.l0,B.l1)]
    if obj.get("endpoints")!=ep or obj.get("box_depth")!=B.depth or obj.get("column")!=B.kind():raise ValueError("leaf geometry")
    c,cb,R=geometry(B)
    ce=[rtext(c[0]),"0/1",rtext(c[1])]
    cbe=None if cb is None else [rtext(cb[0]),"0/1",rtext(cb[1])]
    if obj.get("c")!=ce or obj.get("cbar")!=cbe or obj.get("R")!=rtext(R):raise ValueError("centre/radius")
    cells=parse_cells(obj["cell_tree"])
    L=arb(0); Ap=arb(0); Am=arb(0); cutarea=arb(0); threshold=ball(4*R*R)
    for C in cells:
        okp=okm=False
        try:
            okp=(dist2(C,B,c)-threshold).lower()>=0
            okm=True if cb is None else (dist2(C,B,cb)-threshold).lower()>=0
        except Exception:
            okp=okm=False
        regular=okp and okm
        val=None
        if regular:
            try:val=K(C,B)
            except Exception:
                regular=False;okp=False
        ar=C.area()
        if regular:L+=ar*val.lower()
        else:
            cutarea+=ar
            if B.kind()=="far":
                if not okp:Ap+=ar
                if not okm:Am+=ar
    if B.kind()=="far":
        lo=B.physical()[0]; Bc=C1/ball(lo)*(Ap+Am)
    else:Bc=2*C2/ball(B.l0)*(4*PI*cutarea).sqrt()
    margin=L-Bc
    if not margin.lower()>0:raise ValueError("nonpositive checker margin")
    return len(cells),margin.lower().str(30)

def initial_box(i,j,k):
    return Box(Q(i,8),Q(i+1,8),Q(j,8),Q(j+1,8),Q(2,5)+Q(k,4)*Q(13,50),Q(2,5)+Q(k+1,4)*Q(13,50),0)

def check_record(rec,expected):
    if rec.get("initial")!=list(expected):raise ValueError("initial order")
    B=initial_box(*expected); boxes=parse_boxes(rec["box_tree"],B); listed=rec.get("leaves")
    if not isinstance(listed,list) or len(listed)!=len(boxes):raise ValueError("leaf count")
    total=0
    for b,o in zip(boxes,listed):
        n,_=check_leaf(b,o);total+=n
    return len(boxes),total

def check_unit(item):
    ctx.prec=BITS
    rec,expected=item
    try:
        leaves,cells=check_record(rec,expected)
        return {"ok":True,"initial":list(expected),"leaves":leaves,"cells":cells}
    except Exception as e:
        return {"ok":False,"initial":list(expected),"error":f"{type(e).__name__}: {e}"}

def utc_now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def checker_identity(cert):
    return {"head":os.popen("git rev-parse HEAD").read().strip(),"checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"certificate_sha256":sha(cert)}
def append_checker_ledger(path,rec):
    with open(path,"ab",buffering=0) as f:
        fcntl.flock(f,fcntl.LOCK_EX);f.write((json.dumps(rec,sort_keys=True,separators=(",",":"))+"\n").encode());os.fsync(f.fileno());fcntl.flock(f,fcntl.LOCK_UN)
def load_checker_ledger(path,identity):
    p=Path(path)
    if not p.exists(): return {}
    data=p.read_bytes()
    if data and not data.endswith(b"\n"): raise SystemExit("CHECKER_LEDGER_TRAILING_PARTIAL_LINE")
    rows=[json.loads(x) for x in data.splitlines()]
    if not rows or rows[0]!={"record_type":"header","identity":identity}: raise SystemExit("CHECKER_LEDGER_IDENTITY_MISMATCH")
    out={}
    for r in rows[1:]:
        if r.get("record_type")=="interruption": continue
        if r.get("record_type")!="unit_complete": raise SystemExit("CHECKER_LEDGER_RECORD_TYPE")
        k=tuple(r["initial"])
        if k in out: raise SystemExit("CHECKER_LEDGER_DUPLICATE")
        out[k]=r["result"]
    return out
def checker_lock(run):
    p=run/"checker.LOCK"; payload={"pid":os.getpid(),"host":socket.gethostname(),"started_utc":utc_now()}
    try: fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    except FileExistsError:
        try: old=json.loads(p.read_text())
        except Exception: raise SystemExit("CHECKER_LOCK_INVALID")
        if old.get("host")==socket.gethostname():
            try: os.kill(int(old["pid"]),0)
            except (ProcessLookupError,ValueError,KeyError): pass
            else: raise SystemExit("CHECKER_LOCK_LIVE_WRITER")
        p.unlink();fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    with os.fdopen(fd,"w") as f: json.dump(payload,f,sort_keys=True);f.write("\n");f.flush();os.fsync(f.fileno())
    return p

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--certificate",required=True);ap.add_argument("--report",required=True);ap.add_argument("--smoke",action="store_true")
    ap.add_argument("--resume");ap.add_argument("--heartbeat-seconds",type=float,default=60.0)
    args=ap.parse_args();ctx.prec=BITS
    cert=Path(args.certificate); report=Path(args.report)
    result={"bits":BITS,"gamma_star":"5/8","certificate_sha256":sha(cert),"mode":"smoke" if args.smoke else "full","pass":False}
    run=report.parent;run.mkdir(parents=True,exist_ok=True)
    ledger=Path(args.resume) if args.resume else run/"checker_ledger.jsonl"
    if ledger.parent.resolve()!=run.resolve(): raise SystemExit("CHECKER_LEDGER_OUTSIDE_RUN_DIR")
    identity=checker_identity(cert)
    if ledger.exists() and not args.resume: raise SystemExit("CHECKER_LEDGER_EXISTS_USE_RESUME")
    saved=load_checker_ledger(ledger,identity) if args.resume else {}
    if not ledger.exists():
        ledger.write_text(json.dumps({"record_type":"header","identity":identity},sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    lock=checker_lock(run);completed=0;stop=threading.Event()
    def interrupted(signum,frame):
        append_checker_ledger(ledger,{"record_type":"interruption","utc":utc_now(),"actor":f"signal:{signum}","pid":os.getpid()});raise SystemExit(128+signum)
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    def heartbeat():
        while not stop.wait(args.heartbeat_seconds): print(f"CHECKER_HEARTBEAT completed_units={completed}",flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
    try:
        records=[]
        with gzip.open(cert,"rt",encoding="utf-8") as f:
            for line in f:records.append(json.loads(line))
        expected=SMOKE if args.smoke else [(i,j,k) for i in range(8) for j in range(8) for k in range(4)]
        if len(records)!=len(expected):raise ValueError("record count")
        units=[]; leaves=cells=0
        for rec,exp in zip(records,expected):
            if exp in saved:
                unit=saved[exp];completed+=1
                if not unit["ok"]:raise ValueError(f"initial {unit['initial']}: {unit['error']}")
                leaves+=unit["leaves"];cells+=unit["cells"]
            else: units.append((rec,exp))
        with mp.Pool(12) as pool:
            for unit in pool.imap(check_unit,units):
                append_checker_ledger(ledger,{"record_type":"unit_complete","initial":unit["initial"],"result":unit});completed+=1
                if not unit["ok"]: raise ValueError(f"initial {unit['initial']}: {unit['error']}")
                leaves+=unit["leaves"];cells+=unit["cells"]
        result.update(initial_boxes=len(expected),accepted_leaves=leaves,cells=cells);result["pass"]=True
    except Exception as e:
        result["error"]=f"{type(e).__name__}: {e}"
    finally:
        stop.set();thread.join(timeout=1);lock.unlink(missing_ok=True)
    with open(report,"w",encoding="utf-8",newline="\n") as f:json.dump(result,f,sort_keys=True,indent=2);f.write("\n")
    print(json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["pass"] else 1
if __name__=="__main__":raise SystemExit(main())
