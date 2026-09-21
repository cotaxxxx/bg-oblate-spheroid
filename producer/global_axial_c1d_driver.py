#!/usr/bin/env python3
"""C1d adaptive producer driver. Frozen contract: 957848e9."""
import argparse, hashlib, json, os, platform, stat, subprocess, sys
from fractions import Fraction
from pathlib import Path
import flint
from flint import arb, ctx
from producer import global_axial_c1c_producer as ev

CONTRACT="957848e9e76725e9167c1babd0b7438f613cfa79"
DRIVER_PATH="producer/global_axial_c1d_driver.py"
PRODUCER_EVALUATOR="producer/global_axial_c1c_producer.py"
CHECKER_EVALUATOR="checker/global_axial_c1c_checker.py"
PRODUCER_BLOB="fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62"
CHECKER_BLOB="3ecbda1b3e9acd8134fdd94505721b1780e14edc"
MAX_ATTEMPTED_NODES=32768
MAX_TOTAL_PANEL_EVALS=1<<28
BOX_LOCAL=(ValueError,ZeroDivisionError)
ZERO_HASH="0"*64

def frac(x): return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def roots():
    for j in range(62):
        for k in range(8):
            yield j,k,Fraction(j,64),Fraction(j+1,64),Fraction(1000+7*k,1600),Fraction(1007+7*k,1600)
def git(*a): return subprocess.check_output(["git",*a],text=True).strip()
def blob(path): return git("rev-parse",f"HEAD:{path}")
def clean(): return subprocess.check_output(["git","status","--porcelain"],text=True)==""
def cpu():
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"): return line.split(":",1)[1].strip()
    except OSError: pass
    return platform.processor()
def import_closure():
    repo=Path(git("rev-parse","--show-toplevel")).resolve(); out={}
    for m in list(sys.modules.values()):
        f=getattr(m,"__file__",None)
        if not f or str(f).startswith("<"): continue
        try: rel=Path(f).resolve().relative_to(repo)
        except (ValueError,OSError): continue
        path=rel.as_posix()
        if path.endswith(".pyc") and "__pycache__" in path:
            q=Path(path); path=(q.parent.parent/(q.name.split(".cpython-",1)[0]+".py")).as_posix()
        try: out[path]=blob(path)
        except subprocess.CalledProcessError: raise RuntimeError(f"imported repository file not tracked at HEAD: {path}")
    return dict(sorted(out.items()))
def identity():
    return {"head":git("rev-parse","HEAD"),"clean":clean(),"driver_blob":blob(DRIVER_PATH),
            "producer_evaluator_blob":blob(PRODUCER_EVALUATOR),"checker_evaluator_blob":blob(CHECKER_EVALUATOR),
            "interpreter":sys.executable,"python":platform.python_version(),"python_flint":getattr(flint,"__version__","UNKNOWN"),
            "cpu":cpu(),"import_closure":import_closure()}
def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=True)
_STATS_KEYS={"series","direct","series_hits_moving_u0","chart_unresolved"}
def safe_stats(x):
    if not isinstance(x,dict): raise TypeError("stats must be dict")
    keys=set(x)
    if not _STATS_KEYS <= keys or keys-_STATS_KEYS-{"four_group_width_max"}:
        raise TypeError(f"stats keys mismatch: {sorted(keys)}")
    out={}
    for k in _STATS_KEYS:
        if type(x[k]) is not int: raise TypeError(f"stats {k} must be int")
        out[k]=x[k]
    if "four_group_width_max" in x:
        fg=x["four_group_width_max"]
        if not isinstance(fg,dict) or set(fg)!={"series","direct"}: raise TypeError("four_group_width_max schema")
        z={}
        for chart in ("series","direct"):
            vals=fg[chart]
            if not isinstance(vals,list) or len(vals)!=4: raise TypeError("four_group_width_max list schema")
            row=[]
            for v in vals:
                if v is None: row.append(None)
                elif isinstance(v,arb): row.append("NONFINITE" if not v.is_finite() else v.str(40))
                else: raise TypeError(f"four_group_width_max element: {type(v).__name__}")
            z[chart]=row
        out["four_group_width_max"]=z
    return out
def evaluation_record(j,k,d,tl,tr,ll,lr,panels,result):
    r={"type":"evaluation","j":j,"k":k,"depth":d,"t":[frac(tl),frac(tr)],
       "lambda":[frac(ll),frac(lr)],"N_s":panels,**result}
    if "stats" in r: r["stats"]=safe_stats(r["stats"])
    return r
class Ledger:
    def __init__(self,path,resume=False):
        self.path=Path(path); self.prev=ZERO_HASH
        if self.path.exists():
            if not resume: raise RuntimeError("ledger exists; use a new run directory or --resume")
            self._verify()
        else:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            if any(self.path.parent.iterdir()): raise RuntimeError("run directory is not new/empty")
            self.path.touch()
    def _verify(self):
        prev=ZERO_HASH
        for raw in self.path.read_text().splitlines():
            r=json.loads(raw); h=r.pop("hash"); expect=hashlib.sha256((prev+canonical(r)).encode()).hexdigest()
            if r.get("prev_hash")!=prev or h!=expect: raise RuntimeError("broken ledger hash chain")
            prev=h
        self.prev=prev
    def add(self,rec):
        rec=dict(rec); rec["prev_hash"]=self.prev
        h=hashlib.sha256((self.prev+canonical(rec)).encode()).hexdigest(); rec["hash"]=h
        with self.path.open("a",encoding="ascii") as f: f.write(canonical(rec)+"\n"); f.flush(); os.fsync(f.fileno())
        self.prev=h; return rec
def eval_box(tl,tr,ll,lr,panels):
    stats=ev._stats()
    try:
        value=ev._integrate(tl,tr,ll,lr,panels,stats)
    except BOX_LOCAL as e:
        return {"outcome":"exception","exception":type(e).__name__,"stats":stats},False
    if not value.is_finite():
        return {"outcome":"nonfinite","stats":stats},False
    good=bool(value.upper()<0)
    return {"outcome":"accepted" if good else "not_accepted","enclosure":value.str(80),"stats":stats},good
class Run:
    def __init__(self,ledger):
        self.L=ledger; self.nodes=0; self.panels=0; self.leaves=[]; self.unresolved=None
    def node(self,j,k,tl,tr,ll,lr,d):
        self.nodes+=1
        if self.nodes>MAX_ATTEMPTED_NODES: raise RuntimeError("MAX_ATTEMPTED_NODES")
        last=None
        for panels in ((2048,8192) if d<7 else (2048,8192,16384)):
            if self.panels+panels>MAX_TOTAL_PANEL_EVALS: raise RuntimeError("MAX_TOTAL_PANEL_EVALS")
            self.panels+=panels; result,good=eval_box(tl,tr,ll,lr,panels)
            rec=evaluation_record(j,k,d,tl,tr,ll,lr,panels,result)
            self.L.add(rec); last=rec
            if good:
                leaf={q:rec[q] for q in ("j","k","depth","t","lambda","N_s","enclosure")}
                self.leaves.append(leaf); self.L.add({"type":"leaf",**leaf}); return True
        if d==7:
            self.unresolved=last; self.L.add({"type":"unresolved","j":j,"k":k,"depth":d,"t":[frac(tl),frac(tr)],"lambda":[frac(ll),frac(lr)],"N_s":16384,"final_outcome":last["outcome"],**({"enclosure":last["enclosure"]} if "enclosure" in last else {}),**({"exception":last["exception"]} if "exception" in last else {})}); return False
        mid=(tl+tr)/2
        return self.node(j,k,tl,mid,ll,lr,d+1) and self.node(j,k,mid,tr,ll,lr,d+1)
def run(out,resume=False):
    ctx.prec=ev.BITS; ev.base.ctx.prec=ev.BITS
    out=Path(out).resolve()
    repo=Path(git("rev-parse","--show-toplevel")).resolve()
    try: out.relative_to(repo); inside=True
    except ValueError: inside=False
    if inside: raise RuntimeError("run directory must be outside repository worktree")
    L=Ledger(out/"producer.jsonl",resume)
    if resume:
        raise RuntimeError("resumption of an incomplete traversal is deliberately fail-closed in v1; use a new run directory")
    before=identity()
    if not before["clean"] or before["producer_evaluator_blob"]!=PRODUCER_BLOB or before["checker_evaluator_blob"]!=CHECKER_BLOB: raise RuntimeError("identity/pin mismatch")
    L.add({"type":"identity","when":"before","identity":before,"contract":CONTRACT})
    R=Run(L); status="PASS"
    try:
        for j,k,tl,tr,ll,lr in roots():
            if not R.node(j,k,tl,tr,ll,lr,0): status="UNRESOLVED"; break
    except BOX_LOCAL:
        raise AssertionError("box-local exception escaped eval_box")
    except Exception as e:
        status="ABORT"; L.add({"type":"abort","exception":type(e).__name__,"message":str(e)})
    after=identity()
    if after!=before: status="NOT_EVIDENCE"
    L.add({"type":"identity","when":"after","identity":after,"contract":CONTRACT})
    L.add({"type":"final","status":status,"attempted_nodes":R.nodes,"panel_evaluations":R.panels,"accepted_leaves":len(R.leaves)})
    os.chmod(L.path,stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)
    seal=hashlib.sha256(L.path.read_bytes()).hexdigest()
    (Path(out)/"producer.seal.sha256").write_text(seal+"  producer.jsonl\n")
    return status
def main():
    p=argparse.ArgumentParser(); p.add_argument("run_dir"); p.add_argument("--resume",action="store_true"); a=p.parse_args()
    s=run(a.run_dir,a.resume); print(s); raise SystemExit(0 if s=="PASS" else 2)
if __name__=="__main__": main()
