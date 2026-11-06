#!/usr/bin/env python3
"""Diagnostic only. Same unchanged Astra and chat evaluators, new high-lambda cover."""
from pathlib import Path
from fractions import Fraction as F
from multiprocessing import get_context
import json,sys,hashlib,time
ROOT=Path(__file__).resolve().parent
LOW=Path('/home/daybreak/D5_M22_work/m22_run_20261106')
sys.path.insert(0,str(LOW))
import m22_dig_full as D
source=Path('/home/daybreak/D5_M40_work/m40_run_20261105')
sys.path.insert(0,str(source))
import chat_m22iv as V
def fmt(x):return str(x)
def main():
  boxes=[]
  for i in range(13):
    ll=F(119,200)+F(i,200);lh=ll+F(1,200)
    for k in range(4):
      boxes.append({'lam':[fmt(ll),fmt(lh)],'z':[fmt(k*lh/32),fmt((k+1)*lh/32)]})
  assert len(boxes)==52 and F(boxes[-1]['lam'][1])==F(33,50)
  cover={'boxes':boxes,'scope':'DIAGNOSTIC_CANDIDATE_COVER_NOT_JUDGE_PINNED'}
  cov_path=ROOT/'m22_high_cover_candidate.json'
  cov_path.write_text(json.dumps(cover,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
  D.HASH=hashlib.sha256(cov_path.read_bytes()).hexdigest()
  D.COVER_BOXES=boxes
  print('COVER_HASH',D.HASH,flush=True)
  start=time.monotonic()
  # fork copies the immutable evaluator definitions, preserving source hashes.
  with get_context('fork').Pool(2) as pool:
    p=list(pool.imap(D.evaluate,enumerate(boxes)))
  assert [x['index'] for x in p]==list(range(52))
  from fractions import Fraction as Q
  worst=min(p,key=lambda x:Q(x['lower']))
  rec={'role':'Dig_Astra_producer','cover_sha256':D.HASH,'producer':p,'source_sha256':D.SOURCE_HASH,
       'worst_index':worst['index'],'worst_lower':worst['lower'],'all_ge_minus_200':all(Q(x['lower'])>=-200 for x in p)}
  (ROOT/'m22_high_producer_diagnostic.json').write_text(json.dumps(rec,separators=(',',':'))+'\n')
  print('PRODUCER_DONE',len(p),'all_ge_-200',rec['all_ge_minus_200'],'worst',worst['index'],float(Q(worst['lower'])),'elapsed',time.monotonic()-start,flush=True)
  ver=[]
  with get_context('fork').Pool(2) as pool:
    for item in pool.imap(V.work,[(b,32) for b in boxes]):
      ver.append(item);print('VER',len(ver),'lower',item['lower_float'],flush=True)
  assert [r['box'] for r in ver]==boxes
  worstv=min(enumerate(ver),key=lambda x:Q(x[1]['lower']))
  (ROOT/'m22_high_chat_verifier_diagnostic.jsonl').write_text(''.join(json.dumps(row,separators=(',',':'))+'\n' for row in ver))
  print('VERIFIER_DONE',len(ver),'all_ge_-200',all(Q(r['lower'])>=-200 for r in ver),'worst',worstv[0],worstv[1]['lower_float'],'elapsed',time.monotonic()-start,flush=True)
  print('STATUS_DIAGNOSTIC_NOT_FORMAL_ADOPTION',flush=True)
if __name__=='__main__':main()
