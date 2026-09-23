#!/home/daybreak/.pyenv/versions/3.11.16/bin/python
"""Fast implementation controls for D-OB P2 resumable execution."""
import importlib.util
import json
import multiprocessing as mp
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

P=load("dobp",Path("producer/d_ob_p2_producer.py"))
C=load("dobc",Path("checker/d_ob_p2_checker.py"))

def configure(path,identity,resume):
    P._LEDGER_PATH=str(path);P._IDENTITY=identity;P._RESUME=resume;P._COUNTER=mp.Value("Q",0)

def fake_refine(B):
    return [object()], {"regular":[],"cut":[]}

def fake_box(B,cells,data):
    return {"endpoints":[P.qstr(x) for x in (B.r0,B.r1,B.t0,B.t1,B.l0,B.l1)],"cell_tree":"CONTROL"}

def main():
    old_refine,old_box=P.refine_cells,P.box_obj
    P.refine_cells,P.box_obj=fake_refine,fake_box
    try:
        with tempfile.TemporaryDirectory() as td:
            td=Path(td);identity=P.runtime_identity()
            full=td/"full.jsonl";full.write_text(json.dumps({"record_type":"header","identity":identity},sort_keys=True,separators=(",",":"))+"\n")
            configure(full,identity,{})
            uninterrupted=P.solve_initial((0,0,0))
            rows=[json.loads(x) for x in full.read_text().splitlines()]
            node=next(x for x in rows if x.get("record_type")=="node_decision")

            resumed=td/"resumed.jsonl";resumed.write_text(json.dumps({"record_type":"header","identity":identity},sort_keys=True,separators=(",",":"))+"\n")
            configure(resumed,identity,{})
            P.append_ledger({"record_type":"interruption","utc":P.utc_now(),"actor":"control-kill","pid":0})
            P.append_ledger(node)
            state=P.load_ledger(resumed,identity);configure(resumed,identity,state)
            after=P.solve_initial((0,0,0))
            a={tuple(x["endpoints"]) for x in uninterrupted["leaves"]}
            b={tuple(x["endpoints"]) for x in after["leaves"]}
            assert a==b
            print(f"C-R1 LEAF_SET_MATCH uninterrupted={len(a)} kill_resume={len(b)} equal={a==b}")

            bad=dict(identity);bad["head"]="BAD"
            try:P.load_ledger(resumed,bad)
            except SystemExit as exc: fail=str(exc)
            else:raise AssertionError("identity mismatch did not fail closed")
            assert node["decision"]=="accepted" and node["panels"]==1
            print(f"C-R2 WRITE_THROUGH success=node_decision fail_closed={fail}")

            cledger=td/"checker.jsonl";cid={"head":"H","checker_sha256":"C","certificate_sha256":"Z"}
            cledger.write_text(json.dumps({"record_type":"header","identity":cid},sort_keys=True,separators=(",",":"))+"\n")
            C.append_checker_ledger(cledger,{"record_type":"unit_complete","initial":[0,0,0],"result":{"ok":True,"initial":[0,0,0],"leaves":1,"cells":1}})
            assert C.load_checker_ledger(cledger,cid)[(0,0,0)]["ok"]
            print("C-R2 CHECKER_WRITE_THROUGH success=unit_complete")
            lockdir=td/"locks";lockdir.mkdir();configure(lockdir/"producer_ledger.jsonl",identity,{})
            (lockdir/"LOCK").write_text(json.dumps({"pid":99999999,"host":P.socket.gethostname()})+"\n")
            lk=P.acquire_lock(lockdir);assert lk.exists();lk.unlink()
            (lockdir/"LOCK").write_text(json.dumps({"pid":P.os.getpid(),"host":P.socket.gethostname()})+"\n")
            try:P.acquire_lock(lockdir)
            except SystemExit as exc: live=str(exc)
            else:raise AssertionError("live producer lock accepted")
            (lockdir/"LOCK").unlink()
            (lockdir/"checker.LOCK").write_text(json.dumps({"pid":99999999,"host":C.socket.gethostname()})+"\n")
            clk=C.checker_lock(lockdir);assert clk.exists();clk.unlink()
            print(f"C-R2 LOCK_GATES stale_recovered=True live_fail={live} checker_stale_recovered=True")
    finally:
        P.refine_cells,P.box_obj=old_refine,old_box

    with tempfile.TemporaryDirectory() as td:
        cmd=[sys.executable,str(ROOT/"producer/d_ob_p2_producer.py"),"--run-dir",td,"--workers","1","--initial","0,0,3","--heartbeat-seconds","0.05"]
        proc=subprocess.Popen(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        time.sleep(0.22);proc.send_signal(signal.SIGTERM)
        out,_=proc.communicate(timeout=10)
        beats=[x for x in out.splitlines() if x.startswith("HEARTBEAT completed_nodes=")]
        assert beats, out
        print("C-R3 HEARTBEAT_EXISTS "+beats[0])
        ledger=Path(td)/"producer_ledger.jsonl"
        rows=[json.loads(x) for x in ledger.read_text().splitlines()]
        assert any(x.get("record_type")=="interruption" for x in rows)
        print("C-R3 INTERRUPTION_PROVENANCE present=True")
    print("CONTROLS_PASS C-R1 C-R2 C-R3")

if __name__=="__main__":
    main()
