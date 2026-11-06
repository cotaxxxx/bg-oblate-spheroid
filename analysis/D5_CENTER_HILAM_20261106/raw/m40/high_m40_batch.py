#!/usr/bin/env python3
"""High-lambda M40' DIAGNOSTIC, 416 box pairs. Imports unchanged old modules."""
from pathlib import Path
from multiprocessing import get_context,TimeoutError as MpTimeoutError
from fractions import Fraction as F
import sys,json,hashlib,time,os,argparse,traceback
ROOT=Path(__file__).resolve().parent
OLD=Path('/home/daybreak/D5_M40_work/m40_run_20261105')
sys.path.insert(0,str(OLD))
import m40_batch as OLD_BATCH
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic(path,data):
  t=path.with_suffix(path.suffix+'.tmp')
  t.write_text(json.dumps(data,sort_keys=True,ensure_ascii=False)+'\n')
  t.replace(path)
def available_gib():
  return int(next(line.split()[1] for line in open('/proc/meminfo') if line.startswith('MemAvailable:')))/1048576
def build_cover():
  boxes=[];vboxes=[]
  for i in range(13):
    llo=F(119,200)+F(i,200);lhi=llo+F(1,200)
    for j in range(8):
      rlo=F(j,64);rhi=F(j+1,64)
      for k in range(4):
        zlo=k*lhi/32;zhi=(k+1)*lhi/32
        boxes.append({'id':f'L{i:02d}_R{j}_Z{k}','lambda':[str(llo),str(lhi)],
                      'rho':[str(rlo),str(rhi)],'z':[str(zlo),str(zhi)]})
        vboxes.append({'lam':[str(llo),str(lhi)],'rho':[str(rlo),str(rhi)],
                       'z':[str(zlo),str(zhi)]})
  assert len(boxes)==len(vboxes)==416
  return boxes,vboxes
def main():
  ap=argparse.ArgumentParser();ap.add_argument('role',choices=['producer','verifier'])
  ap.add_argument('--workers',type=int,required=True);a=ap.parse_args()
  fixed,chat=build_cover()
  coverfile=ROOT/'high_m40_cover_candidate.json'
  if not coverfile.exists():
    atomic(coverfile,{'status':'CANDIDATE_ONLY_NOT_JUDGE_PINNED','outer_box_count':416,'boxes':fixed})
  loaded=json.loads(coverfile.read_text())['boxes']
  assert loaded==fixed
  coverhash=sha(coverfile)
  OLD_BATCH.FIXED['m40_cover.json']=coverhash
  u=[str(F(i,64)) for i in range(33)]+[str(F(i,16)) for i in range(9,17)]
  cells={'u':u,'t':16}
  assert len(u)-1==40
  out=ROOT/a.role
  (out/'boxes').mkdir(parents=True,exist_ok=True)
  original_cover=sha(OLD/'m40_cover.json')
  assert original_cover=='ebcd3f6ce22a4f28a9ef9f8855292f8b9ed393b2f46faf01b40273ce0d9c751a'
  if available_gib()<8:raise RuntimeError('LOW_MEMORY_PRESTART')
  done=set()
  for i in range(416):
    p=out/'boxes'/f'{i:04d}.json'
    if p.exists():
      r=json.loads(p.read_text())
      assert r['index']==i and r['cover_sha256']==coverhash and r['role']==a.role
      done.add(i)
  state=lambda phase:atomic(out/'state.json',{'role':a.role,'phase':phase,
    'completed':len(done),'total':416,'workers':a.workers if phase=='RUNNING' else 0,
    'mem_available_gib':available_gib(),'timestamp':time.time(),'cover_sha256':coverhash})
  state('RUNNING')
  boxlist=fixed if a.role=='producer' else chat
  jobs=[(a.role,i,boxlist[i],{'u':32,'t':32} if a.role=='producer' else cells)
         for i in range(416) if i not in done]
  started=time.monotonic()
  with get_context('fork').Pool(a.workers,maxtasksperchild=20) as pool:
    it=pool.imap_unordered(OLD_BATCH.worker,jobs,chunksize=1)
    remaining=len(jobs)
    while remaining:
      try: rec=it.next(timeout=8)
      except MpTimeoutError:
        if available_gib()<8:
          state('PAUSED_LOW_MEMORY');pool.terminate();raise RuntimeError('MEMORY_GUARD')
        continue
      i=rec['index']
      if 'error' in rec:
        atomic(out/'ERROR.json',rec);state('HALTED_ERROR')
        pool.terminate();raise RuntimeError('BOX_ERROR '+str(i)+' '+rec['error'])
      assert rec['cover_sha256']==coverhash
      assert rec['role']==a.role
      assert F(rec['lower'])>=-400,('BOUND_BELOW_THRESHOLD',i)
      atomic(out/'boxes'/f'{i:04d}.json',rec)
      done.add(i);remaining-=1
      if len(done)%4==0:state('RUNNING')
      print('BOX',a.role,i,'LOWER',rec['lower_float_reference'],'DONE',len(done),'/416',flush=True)
      if available_gib()<8:
        state('PAUSED_LOW_MEMORY');pool.terminate();raise RuntimeError('MEMORY_GUARD')
  rows=[json.loads((out/'boxes'/f'{i:04d}.json').read_text()) for i in range(416)]
  vals=[F(r['lower']) for r in rows]
  worst=min(range(416),key=lambda i:vals[i])
  atomic(out/'DONE.json',{'role':a.role,'count':416,'all_ge_minus_400':all(x>=-400 for x in vals),
    'cover_sha256':coverhash,'worst_index':worst,'worst_lower_exact':str(vals[worst]),
    'status':'DIAGNOSTIC_COMPUTATION_COMPLETED_PENDING_FIXED_COVER_AUDIT'})
  state('DONE_DIAGNOSTIC')
  print('COMPLETE',a.role,'WORST',worst,str(vals[worst]),float(vals[worst]),'ELAPSED',time.monotonic()-started,flush=True)
if __name__=='__main__':main()
