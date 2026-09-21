#!/usr/bin/env python3
"""C1d checker: sealed producer ledger is the sole evidence input."""
import argparse, hashlib, json, os, platform, stat, subprocess, sys
import flint
from fractions import Fraction
from pathlib import Path
from flint import ctx
from checker import global_axial_c1c_checker as ev
ZERO_HASH="0"*64
BOX_LOCAL=(ValueError,ZeroDivisionError)
def F(s): return Fraction(s)
def canonical(o): return json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def git(*a): return subprocess.check_output(["git",*a],text=True).strip()
def blob(path): return git("rev-parse",f"HEAD:{path}")
def clean(): return subprocess.check_output(["git","status","--porcelain"],text=True)==""
def import_closure():
    repo=Path(git("rev-parse","--show-toplevel")).resolve(); out={}
    for m in list(sys.modules.values()):
        f=getattr(m,"__file__",None)
        if not f: continue
        try: rel=Path(f).resolve().relative_to(repo)
        except (ValueError,OSError): continue
        path=rel.as_posix()
        if path.endswith(".pyc") and "__pycache__" in path:
            q=Path(path); path=(q.parent.parent/(q.name.split(".cpython-",1)[0]+".py")).as_posix()
        try: out[path]=blob(path)
        except subprocess.CalledProcessError: raise RuntimeError(f"imported repository file not tracked at HEAD: {path}")
    return dict(sorted(out.items()))
def identity():
    return {"head":git("rev-parse","HEAD"),"clean":clean(),"interpreter":sys.executable,
            "python":platform.python_version(),"python_flint":getattr(flint,"__version__","UNKNOWN"),
            "import_closure":import_closure()}
def load(path):
    path=Path(path)
    if stat.S_IMODE(path.stat().st_mode)!=0o444: raise RuntimeError("ledger not mode 444")
    seal=path.with_name("producer.seal.sha256")
    if not seal.exists() or seal.read_text().split()[0]!=hashlib.sha256(path.read_bytes()).hexdigest(): raise RuntimeError("seal mismatch")
    prev=ZERO_HASH; rows=[]
    for raw in path.read_text().splitlines():
        r=json.loads(raw); h=r.pop("hash"); expect=hashlib.sha256((prev+canonical(r)).encode()).hexdigest()
        if r.get("prev_hash")!=prev or h!=expect: raise RuntimeError("hash chain mismatch")
        r["hash"]=h; rows.append(r); prev=h
    return rows
def leaves(rows):
    finals=[r for r in rows if r.get("type")=="final"]
    if len(finals)!=1 or finals[0].get("status")!="PASS": raise RuntimeError("producer final is not PASS")
    ids=[r for r in rows if r.get("type")=="identity"]
    if [r.get("when") for r in ids]!=["before","after"] or ids[0]["identity"]!=ids[1]["identity"]: raise RuntimeError("identity mismatch")
    return [r for r in rows if r.get("type")=="leaf"]
def verify_tiling(ls):
    by={}
    for r in ls:
        j,k,d=r["j"],r["k"],r["depth"]; tl,tr=map(F,r["t"]); ll,lr=map(F,r["lambda"])
        if not(0<=j<62 and 0<=k<8 and 0<=d<=7): raise RuntimeError("leaf index/depth")
        if (ll,lr)!=(Fraction(1000+7*k,1600),Fraction(1007+7*k,1600)): raise RuntimeError("lambda endpoint")
        if tr-tl!=Fraction(1,64*(2**d)): raise RuntimeError("t width")
        if (tl*64*(2**d)).denominator!=1 or not(Fraction(j,64)<=tl<tr<=Fraction(j+1,64)): raise RuntimeError("t dyadic/alignment")
        by.setdefault((j,k),[]).append((tl,tr))
    for j in range(62):
        for k in range(8):
            a=sorted(by.get((j,k),[]))
            if not a or a[0][0]!=Fraction(j,64) or a[-1][1]!=Fraction(j+1,64) or any(a[i][1]!=a[i+1][0] for i in range(len(a)-1)): raise RuntimeError(f"tiling {j},{k}")
def evaluate(r):
    tl,tr=map(F,r["t"]); ll,lr=map(F,r["lambda"]); n=r["N_s"]; stats=ev._stats()
    try: v=ev._integrate(tl,tr,ll,lr,n,stats)
    except BOX_LOCAL as e: raise RuntimeError(f"checker box-local failure {r['j']},{r['k']}: {type(e).__name__}")
    if not v.is_finite(): raise RuntimeError("checker nonfinite")
    if not v.upper()<0: raise RuntimeError("checker sign failure")
    return v.str(80)
def verify(path,out=None):
    ctx.prec=ev.BITS; ev.base.ctx.prec=ev.BITS
    checker_before=identity()
    rows=load(path); ls=leaves(rows); verify_tiling(ls)
    rec=[]
    for r in ls: rec.append({"j":r["j"],"k":r["k"],"depth":r["depth"],"t":r["t"],"lambda":r["lambda"],"N_s":r["N_s"],"enclosure":evaluate(r)})
    checker_after=identity()
    status="PASS" if checker_after==checker_before else "NOT_EVIDENCE"
    result={"status":status,"checker_identity_before":checker_before,"checker_identity_after":checker_after,"leaves":rec}
    if out: Path(out).write_text(canonical(result)+"\n")
    if status!="PASS": raise RuntimeError("checker identity changed")
    return result
def main():
    p=argparse.ArgumentParser(); p.add_argument("sealed_ledger"); p.add_argument("--output"); a=p.parse_args(); x=verify(a.sealed_ledger,a.output); print("PASS",len(x["leaves"]))
if __name__=="__main__": main()
