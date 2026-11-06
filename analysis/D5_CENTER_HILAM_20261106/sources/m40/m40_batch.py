#!/usr/bin/env python3
"""D5 M40 checkpointed isolated batch. No changes to B7, Git, or frozen cover.
Each completed box is atomically stored; launcher is resumable, not a proof verifier.
"""
import argparse, contextlib, fcntl, hashlib, io, json, multiprocessing as mp
import os, sys, time, traceback
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
FIXED={
    'm40_cover.json':'ebcd3f6ce22a4f28a9ef9f8855292f8b9ed393b2f46faf01b40273ce0d9c751a',
    'm40_pilot.py':'98c0194fa86b23f2ffaf37eda2cc90533564318f7571364432e4b619095879da',
    'calibration_contract.json':'3949bb68dcaff6ef97f10888f208ae6de3507d6e904a1785eecb2d7d0eaa937d',
    'chat_m40iv.py':'d39be478485cb1faaf804ddbf970ce1c790b0d7a5d0bf7f2fb400561c2cdad1b',
    'chat_m22iv.py':'b4ea57e134150e57be8ced020eafa4cfd6c740af75d27939b108e23de38d6a89',
    'm40_cover_proposal_39x8x4.json':'fb56bb167653d0da313c1a9ea4589f9524930d426508013d4070dcf4cfc296a7'
}
TARGET=1248
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def gate():
    for name,expected in FIXED.items():
        h=sha(ROOT/name)
        if h!=expected:raise RuntimeError('SOURCE_FROZEN_HASH_MISMATCH '+name+' '+h)
    frozen=json.loads((ROOT/'m40_cover.json').read_text())
    chat=json.loads((ROOT/'m40_cover_proposal_39x8x4.json').read_text())
    fb=frozen['boxes'];cb=chat['boxes']
    assert len(fb)==len(cb)==TARGET
    assert frozen['calibration_mesh']=={'u':32,'t':32}
    assert len(chat['cells']['u'])-1==40 and chat['cells']['t']==16
    for i,(a,b) in enumerate(zip(fb,cb)):
        for aa,bb in [('lambda','lam'),('rho','rho'),('z','z')]:
            if tuple(map(F,a[aa]))!=tuple(map(F,b[bb])):
                raise RuntimeError('OUTER_MISMATCH '+str(i))
    # An independent geometrical cover audit is already published in this folder.
    return frozen,chat

def avail_gib():
    with open('/proc/meminfo') as f:
        for s in f:
            if s.startswith('MemAvailable:'):return int(s.split()[1])/1048576
    raise RuntimeError('No MemAvailable')

def proof_record_good(path,idx,role):
    if not path.exists():return False
    try:
        row=json.loads(path.read_text())
        return row['index']==idx and row['role']==role and row['cover_sha256']==FIXED['m40_cover.json'] and (
            row['source_sha256']==FIXED['m40_pilot.py'] if role=='producer' else row['source_sha256']==FIXED['chat_m40iv.py'])
    except Exception as e:raise RuntimeError('INVALID_EXISTING_CHECKPOINT '+str(path)) from e

def worker(job):
    role,idx,box,cells=job
    started=time.monotonic()
    try:
        if role=='producer':
            import m40_pilot as p
            case={'name':f'M40_{idx:04d}', 'lambda':box['lambda'],
                  'rho':box['rho'],'z':box['z']}
            # Suppress per-angle progress but preserve exact output.
            with contextlib.redirect_stdout(io.StringIO()):
                r=p.run_case(case,32)
            ans={
                'index':idx,'role':role,'box':{'lam':box['lambda'],'rho':box['rho'],'z':box['z']},
                'q_plus':r['q_plus'],'lower':r['lower'],
                'lower_float_reference':float(F(r['lower'])),
                'midpoint_raw':r['midpoint'],'curvature_raw':r['curvature'],
                'tail_loss_raw':r['tail_loss'],'raw_lower':r['raw_lower'],
                'elapsed_seconds':time.monotonic()-started,'cells':{'u':32,'t':32},
                'producer_pass_candidate':F(r['lower'])>=-400,
                'cover_sha256':FIXED['m40_cover.json'],
                'source_sha256':FIXED['m40_pilot.py'],
                'status':'PRODUCER_BOUND_NOT_MATHEMATICALLY_ADOPTED'
            }
        else:
            import chat_m40iv as v
            low,raw=v.box_lower(box,cells)
            ans={
                'index':idx,'role':role,'box':box,
                'lower':str(low),'lower_float_reference':float(low),
                'raw_interval':[str(raw.a),str(raw.b)],
                'elapsed_seconds':time.monotonic()-started,
                'cells':cells,
                'verifier_pass_candidate':low>=-400,
                'cover_sha256':FIXED['m40_cover.json'],
                'source_sha256':FIXED['chat_m40iv.py'],
                'status':'INDEPENDENT_BOUND_NOT_FULL_CERTIFICATE'
            }
        return ans
    except Exception as e:
        return {'index':idx,'role':role,'error_type':type(e).__name__,
                'error':str(e),'traceback':traceback.format_exc(),
                'elapsed_seconds':time.monotonic()-started}

def atomic_json(path,row):
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:
        json.dump(row,f,ensure_ascii=False,sort_keys=True)
        f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def state(role,done,total,workers,phase,other=None):
    atomic_json(ROOT/role/'state.json',{
        'role':role,'completed':done,'total':total,'workers':workers,
        'phase':phase,'available_gib':avail_gib(),
        'timestamp_unix':time.time(),'note':other})
    print('STATE',role,phase,done,'/',total,'workers',workers,
          'MemAvailable_GiB',round(avail_gib(),2),other or '',flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('role',choices=['producer','verifier'])
    parser.add_argument('--workers',type=int,required=True)
    opts=parser.parse_args()
    role=opts.role
    if role=='producer' and opts.workers>8:raise RuntimeError('producer >8: not in initial resource budget')
    if role=='verifier' and opts.workers!=4:raise RuntimeError('verifier initial workers must be 4')
    fixed,chat=gate()
    cells=chat['cells'] if role=='verifier' else {'u':32,'t':32}
    boxes=chat['boxes'] if role=='verifier' else fixed['boxes']
    out=ROOT/role
    (out/'boxes').mkdir(parents=True,exist_ok=True)
    lockfile=(out/'RUN.lock').open('w')
    try:fcntl.flock(lockfile,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise RuntimeError('DUPLICATE_RUNNER '+role)
    lockfile.write(str(os.getpid())+'\n');lockfile.flush()
    workers=opts.workers
    with (out/'results.jsonl').open('a',buffering=1) as ledger:
        while True:
            done={i for i in range(TARGET) if proof_record_good(out/'boxes'/f'{i:04d}.json',i,role)}
            if len(done)==TARGET:
                rows=[json.loads((out/'boxes'/f'{i:04d}.json').read_text()) for i in range(TARGET)]
                lows=[F(x['lower']) for x in rows]
                atomic_json(out/'DONE.json',{'role':role,'count':TARGET,
                    'cover_sha256':FIXED['m40_cover.json'],
                    'worst_lower_exact':str(min(lows)),
                    'all_ge_minus_400':all(x>=-400 for x in lows),
                    'status':'COMPUTATION_COMPLETED_AWAITING_INDEPENDENT_ADOPTION'})
                state(role,TARGET,TARGET,0,'COMPUTED_NO_GLOBAL_ADOPTION')
                return
            if avail_gib()<7:
                state(role,len(done),TARGET,0,'PAUSED_LOW_MEMORY')
                time.sleep(30);continue
            desired=workers
            if role=='verifier' and (ROOT/'producer'/'DONE.json').exists():
                # 24 logical CPUs, keep 4 B7 producers + >=6 logical cores spare.
                # A target of 16 is reduced to 14 while B7 still needs its 4 cores.
                desired=min(16,max(1,(os.cpu_count() or 24)-4-6))
            if desired!=workers:
                workers=desired
                state(role,len(done),TARGET,workers,'RESTARTING_AFTER_PRODUCER')
            pending=[(role,i,boxes[i],cells) for i in range(TARGET) if i not in done]
            state(role,len(done),TARGET,workers,'RUNNING')
            pool=mp.get_context('fork').Pool(workers,maxtasksperchild=30)
            reason=None
            try:
                it=pool.imap_unordered(worker,pending,chunksize=1)
                remaining=len(pending)
                while remaining:
                    try:result=it.next(timeout=5)
                    except mp.TimeoutError:
                        if avail_gib()<6:
                            reason='MEMORY_GUARD';break
                        if role=='verifier' and (ROOT/'producer'/'DONE.json').exists() and workers<min(16,(os.cpu_count() or 24)-10):
                            reason='UPGRADE_VERIFIER';break
                        continue
                    idx=result['index'];remaining-=1
                    if 'error' in result:
                        atomic_json(out/'ERROR.json',result)
                        print('FATAL_BOX_ERROR',role,idx,result['error'],flush=True)
                        reason='ERROR';break
                    f=out/'boxes'/f'{idx:04d}.json'
                    atomic_json(f,result)
                    ledger.write(json.dumps(result,ensure_ascii=False,sort_keys=True)+'\n')
                    done.add(idx)
                    if len(done)%8==0 or len(done)==TARGET:
                        state(role,len(done),TARGET,workers,'RUNNING')
                    print('BOX',role,idx,'lower',result['lower_float_reference'],
                          '>=-400',F(result['lower'])>=-400,
                          'seconds',round(result['elapsed_seconds'],1),flush=True)
                    if avail_gib()<6:reason='MEMORY_GUARD';break
                    if role=='verifier' and (ROOT/'producer'/'DONE.json').exists() and workers<min(16,(os.cpu_count() or 24)-10):
                        reason='UPGRADE_VERIFIER';break
            finally:
                if reason:
                    pool.terminate()
                else:
                    pool.close()
                pool.join()
            if reason=='ERROR':
                state(role,len(done),TARGET,0,'HALTED_ERROR');return 1
            if reason=='MEMORY_GUARD':
                workers=max(1,workers//2)
                state(role,len(done),TARGET,workers,'M40_WORKERS_REDUCED')
                time.sleep(30)
            if reason=='UPGRADE_VERIFIER':
                state(role,len(done),TARGET,workers,'RESTART_AFTER_PRODUCER')
            # All completed results persisted. Any in-flight incomplete boxes will retry.
if __name__=='__main__':sys.exit(main() or 0)
