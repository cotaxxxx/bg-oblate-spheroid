#!/usr/bin/env python3
"""§8.2 implementation acceptance controls C1-C4."""
import json, tempfile
from fractions import Fraction
from pathlib import Path
from flint import ctx
from producer import global_axial_c1d_driver as P
from checker import global_axial_c1c_checker as CE
C1=(Fraction(31,32)-Fraction(1,2048),Fraction(31,32),Fraction(5,8),Fraction(1007,1600),8192)
C2=(Fraction(31,32)-Fraction(1,512),Fraction(31,32),Fraction(5,8),Fraction(1007,1600),2048)
C3=(Fraction(29,32),Fraction(31,32),Fraction(5,8),Fraction(1007,1600),2048)
def checker_eval(box):
    ctx.prec=CE.BITS; CE.base.ctx.prec=CE.BITS; stats=CE._stats()
    try: v=CE._integrate(*box,stats)
    except P.BOX_LOCAL as e: return {"outcome":"exception","exception":type(e).__name__},False
    if not v.is_finite(): return {"outcome":"nonfinite"},False
    good=bool(v.upper()<0); return {"outcome":"accepted" if good else "not_accepted","enclosure":v.str(80)},good
def main():
    ctx.prec=P.ev.BITS; P.ev.base.ctx.prec=P.ev.BITS
    p1,g1=P.eval_box(*C1); p2,g2=P.eval_box(*C2); p3,g3=P.eval_box(*C3)
    c1,h1=checker_eval(C1); c2,h2=checker_eval(C2); c3,h3=checker_eval(C3)
    assert g1 and h1 and p1["outcome"]==c1["outcome"]=="accepted"
    assert not g2 and not h2 and p2["outcome"]==c2["outcome"]=="not_accepted"
    assert not g3 and not h3 and p3["outcome"]==c3["outcome"]=="exception" and p3["exception"]==c3["exception"]=="ValueError"
    with tempfile.TemporaryDirectory() as d:
        L=P.Ledger(Path(d)/"control.jsonl")
        exact={"j":61,"k":0,"depth":7,"t":[P.frac(C1[0]),P.frac(C1[1])],"lambda":[P.frac(C1[2]),P.frac(C1[3])],"N_s":C1[4],"outcome":p1["outcome"],"enclosure":p1["enclosure"]}
        L.add({"type":"control","name":"C1",**exact})
        exc={"j":0,"k":0,"depth":0,"t":[P.frac(C3[0]),P.frac(C3[1])],"lambda":[P.frac(C3[2]),P.frac(C3[3])],"N_s":C3[4],"outcome":p3["outcome"],"exception":p3["exception"]}
        L.add({"type":"control","name":"C3",**exc})
        rows=[json.loads(x) for x in Path(L.path).read_text().splitlines()]
        for src,row in ((exact,rows[0]),(exc,rows[1])):
            for q in ("j","k","depth","t","lambda","N_s","outcome"): assert row[q]==src[q]
        assert isinstance(rows[0]["enclosure"],str)
    print("C1 PASS producer/checker accepted")
    print("C2 PASS producer/checker not_accepted without exception")
    print("C3 PASS producer/checker ValueError handled as failed evaluation")
    print("C4 PASS ledger exact fields round-trip; enclosure canonical string")
if __name__=="__main__": main()
