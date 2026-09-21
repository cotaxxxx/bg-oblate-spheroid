#!/usr/bin/env python3
"""§8.2 implementation acceptance controls C1-C4."""
import json, tempfile
from fractions import Fraction
from pathlib import Path
from flint import arb, ctx
from producer import global_axial_c1d_driver as P
from checker import global_axial_c1d_checker as C
from checker import global_axial_c1c_checker as CE
C1=(Fraction(31,32)-Fraction(1,2048),Fraction(31,32),Fraction(5,8),Fraction(1007,1600),8192)
C2=(Fraction(31,32)-Fraction(1,512),Fraction(31,32),Fraction(5,8),Fraction(1007,1600),2048)
C3=(Fraction(29,32),Fraction(31,32),Fraction(5,8),Fraction(1007,1600),2048)
def checker_raw(box):
    ctx.prec=CE.BITS; CE.base.ctx.prec=CE.BITS; stats=CE._stats()
    try: v=CE._integrate(*box,stats)
    except P.BOX_LOCAL as e: return {"outcome":"exception","exception":type(e).__name__,"stats":stats},False
    if not v.is_finite(): return {"outcome":"nonfinite","stats":stats},False
    good=bool(v.upper()<0); return {"outcome":"accepted" if good else "not_accepted","enclosure":v.str(80),"stats":stats},good
def rec(box,result,depth,j=61,k=0):
    return P.evaluation_record(j,k,depth,*box,result)
def leaf(box,depth=5):
    return {"j":61,"k":0,"depth":depth,"t":[P.frac(box[0]),P.frac(box[1])],
            "lambda":[P.frac(box[2]),P.frac(box[3])],"N_s":box[4],"enclosure":"producer"}
def assert_strings(x):
    if isinstance(x,dict):
        for v in x.values(): assert_strings(v)
    else: assert not isinstance(x,arb)
def main():
    ctx.prec=P.ev.BITS; P.ev.base.ctx.prec=P.ev.BITS
    p1,g1=P.eval_box(*C1); p2,g2=P.eval_box(*C2); p3,g3=P.eval_box(*C3)
    q1,h1=checker_raw(C1); q2,h2=checker_raw(C2); q3,h3=checker_raw(C3)
    assert g1 and h1 and p1["outcome"]==q1["outcome"]=="accepted"
    assert not g2 and not h2 and p2["outcome"]==q2["outcome"]=="not_accepted"
    assert not g3 and not h3 and p3["outcome"]==q3["outcome"]=="exception" and p3["exception"]==q3["exception"]=="ValueError"
    r1=rec(C1,p1,5); r2=rec(C2,p2,3); r3=rec(C3,p3,0)
    syn=P.evaluation_record(0,0,0,Fraction(0),Fraction(1,64),Fraction(5,8),Fraction(1007,1600),2048,
        {"outcome":"nonfinite","stats":{"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0,"four_group_width_max":{"series":[arb(1),arb("nan"),None,arb(2)],"direct":[arb(3),None,arb(4),None]}}})
    with tempfile.TemporaryDirectory() as d:
        L=P.Ledger(Path(d)/"records"/"control.jsonl")
        originals=[("C1",r1),("C2",r2),("C3",r3),("SYNTHETIC_NONFINITE",syn)]
        for name,r in originals: L.add({"type":"control","name":name,**{k:v for k,v in r.items() if k!="type"}})
        rows=[json.loads(x) for x in Path(L.path).read_text().splitlines()]
        for (name,src),row in zip(originals,rows):
            assert row["name"]==name
            for q in ("j","k","depth","t","lambda","N_s","outcome"): assert row[q]==src[q]
            assert_strings(row.get("stats",{}))
        assert rows[3]["stats"]["four_group_width_max"]["series"][1]=="NONFINITE"
        assert all(x is None or isinstance(x,str) for x in rows[3]["stats"]["four_group_width_max"]["series"])
        assert all(x is None or isinstance(x,str) for x in rows[3]["stats"]["four_group_width_max"]["direct"])
    with tempfile.TemporaryDirectory() as d:
        L=P.Ledger(Path(d)/"node"/"control.jsonl"); R=P.Run(L)
        assert R.node(61,0,C1[0],C1[1],C1[2],C1[3],5)
        rows=[json.loads(x) for x in Path(L.path).read_text().splitlines()]
        assert rows[0]["type"]=="evaluation" and rows[0]["depth"]==5 and rows[0]["N_s"]==2048
        assert rows[1]["type"]=="evaluation" and rows[1]["depth"]==5 and rows[1]["N_s"]==8192
        assert rows[2]["type"]=="leaf" and rows[2]["depth"]==5 and rows[2]["N_s"]==8192
        assert_strings(rows[0]["stats"]); assert_strings(rows[1]["stats"])
    with tempfile.TemporaryDirectory() as d:
        L=P.Ledger(Path(d)/"sweep"/"control.jsonl")
        for j in range(62):
            box=(Fraction(j,64),Fraction(j+1,64),Fraction(5,8),Fraction(1007,1600),2048)
            result,_=P.eval_box(*box)
            L.add(P.evaluation_record(j,0,0,*box,result))
        rows=[json.loads(x) for x in Path(L.path).read_text().splitlines()]
        assert len(rows)==62
        for row in rows:
            st=row["stats"]; assert set(st) in (P._STATS_KEYS,P._STATS_KEYS|{"four_group_width_max"})
            if "four_group_width_max" in st:
                assert set(st["four_group_width_max"])=={"series","direct"}
                for vals in st["four_group_width_max"].values():
                    assert len(vals)==4 and all(v is None or isinstance(v,str) for v in vals)
    print("SCHEMA_SWEEP PASS 62 Lambda_0 roots at N_s=2048")
    ctx.prec=CE.BITS; CE.base.ctx.prec=CE.BITS
    assert isinstance(C.evaluate(leaf(C1)),str)
    for box,depth in ((C2,3),(C3,0)):
        try: C.evaluate(leaf(box,depth))
        except RuntimeError: pass
        else: raise AssertionError("checker driver did not fail closed")
    repo=Path(P.git("rev-parse","--show-toplevel"))
    bad=repo/"_c1d_forbidden_run_dir"
    assert not bad.exists()
    try: P.run(bad)
    except RuntimeError as e: assert "outside repository worktree" in str(e)
    else: raise AssertionError("in-worktree run directory accepted")
    assert not bad.exists()
    print("C1 PASS producer and checker-driver evaluate")
    print("C2 PASS producer not_accepted; checker-driver fail-closed")
    print("C3 PASS producer ValueError; checker-driver fail-closed")
    print("C4 PASS production constructor/Ledger C1-C3+SYNTHETIC_NONFINITE and end-to-end depth-5 node")
    print("RUN_DIR PASS in-worktree path refused before creation")
if __name__=="__main__": main()
