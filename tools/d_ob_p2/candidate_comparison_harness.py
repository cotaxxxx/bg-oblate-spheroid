#!/home/daybreak/.pyenv/versions/3.11.16/bin/python
"""D-OB P2 SPEC V3 candidate-comparison harness draft.

DIAGNOSTIC / NOT_EVIDENCE. This wrapper never edits the pinned producer.
It verifies producer bytes, loads read-only, and applies frozen runtime overrides.
Execution remains blocked pending an audited execution addendum.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

PINNED_PRODUCER_SHA256="dff79bc40d78d53a1491c3edbe368034b2d28a4894da45ac13b3b04c3ad0f19b"
V2_PREDECLARE_SHA256="06fe184c565982cf295d03f7dd421662ec7672a48686229d5a44d69b5badbb7d"
LABEL="DIAGNOSTIC / NOT_EVIDENCE"

@dataclass(frozen=True)
class Config:
    cid:str; max_cell_count:int=2**16; max_cell_depth:int=10
    max_box_depth:int=12; regular_num:int=1; regular_den:int=4
    rho0:Q=Q(1,8); family:str="baseline"

CONFIGS={
 "C0":Config("C0"),
 "C-count":Config("C-count",max_cell_count=2**17,family="c"),
 "C-cell-depth":Config("C-cell-depth",max_cell_depth=11,family="c"),
 "C-box-depth":Config("C-box-depth",max_box_depth=13,family="c"),
 "C-regular":Config("C-regular",regular_num=1,regular_den=2,family="c"),
 "D-rho-1-16":Config("D-rho-1-16",rho0=Q(1,16),family="d"),
 "D-rho-3-32":Config("D-rho-3-32",rho0=Q(3,32),family="d"),
 "D-rho-5-32":Config("D-rho-5-32",rho0=Q(5,32),family="d"),
 "D-rho-1-4":Config("D-rho-1-4",rho0=Q(1,4),family="d"),
}
# D-rho-1-8 aliases C0: 9 unique executions, 10 comparison configurations.

def sha256(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()

def config_obj(c):
 return {"candidate_id":c.cid,"family":c.family,
  "MAX_CELL_COUNT":c.max_cell_count,"MAX_CELL_DEPTH":c.max_cell_depth,
  "MAX_BOX_DEPTH":c.max_box_depth,
  "regular_selection":f"ceil(N_reg*{c.regular_num}/{c.regular_den})",
  "RHO0":f"{c.rho0.numerator}/{c.rho0.denominator}",
  "score":"exact_upper(area*width(kernel))","score_tie":"cell.order_key",
  "box_split_normalization":{"r":"1","tau":"1","lambda":"13/50"},
  "box_split_tie_order":["r","tau","lambda"]}

def validate_one_change():
 b=config_obj(CONFIGS["C0"]); ignored={"candidate_id","family"}
 allowed={"C-count":{"MAX_CELL_COUNT"},"C-cell-depth":{"MAX_CELL_DEPTH"},
 "C-box-depth":{"MAX_BOX_DEPTH"},"C-regular":{"regular_selection"},
 "D-rho-1-16":{"RHO0"},"D-rho-3-32":{"RHO0"},
 "D-rho-5-32":{"RHO0"},"D-rho-1-4":{"RHO0"}}
 for cid,c in CONFIGS.items():
  if cid=="C0": continue
  x=config_obj(c); changed={k for k in b if k not in ignored and x[k]!=b[k]}
  if changed!=allowed[cid]: raise SystemExit(f"ONE_CHANGE_FAIL {cid} {sorted(changed)}")
def load_pinned(path):
 got=sha256(path)
 if got!=PINNED_PRODUCER_SHA256: raise SystemExit(f"PRODUCER_PIN_MISMATCH got={got}")
 spec=importlib.util.spec_from_file_location("d_ob_p2_candidate_base",path)
 if spec is None or spec.loader is None: raise SystemExit("PRODUCER_LOAD_FAIL")
 mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod
 spec.loader.exec_module(mod); return mod

def apply_config(mod,c):
 mod.MAX_CELL_COUNT=c.max_cell_count; mod.MAX_CELL_DEPTH=c.max_cell_depth
 mod.MAX_BOX_DEPTH=c.max_box_depth; mod.RHO0=c.rho0
 if (c.regular_num,c.regular_den)==(1,4): return
 # The pinned producer hard-codes: take=(nreg+3)//4.
 # C-regular cannot be represented by a module-global override. It therefore
 # requires a separately pinned derived producer whose ONLY source delta is
 # take=(nreg+1)//2. The execution addendum must pin base bytes, derived bytes,
 # and the exact one-line diff before this candidate can run.
 raise SystemExit("C_REGULAR_REQUIRES_PINNED_DERIVED_PRODUCER")

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--producer",required=True); ap.add_argument("--candidate",choices=sorted(CONFIGS),required=True)
 ap.add_argument("--out-dir",required=True); ap.add_argument("--check-only",action="store_true")
 args=ap.parse_args(); validate_one_change()
 p=Path(args.producer).resolve(); c=CONFIGS[args.candidate]
 manifest={"label":LABEL,"predeclare_sha256":V2_PREDECLARE_SHA256,
  "producer_path":str(p),"producer_sha256":sha256(p),"config":config_obj(c),
  "d_rho_1_8_alias":"C0"}
 if args.check_only:
  if manifest["producer_sha256"]!=PINNED_PRODUCER_SHA256: raise SystemExit("PRODUCER_PIN_MISMATCH")
  print(json.dumps(manifest,sort_keys=True)); print("CHECK_ONLY_OK"); return 0
 raise SystemExit("EXECUTION_BLOCKED_PENDING_ADDENDUM_AUDIT")

if __name__=="__main__": raise SystemExit(main())
