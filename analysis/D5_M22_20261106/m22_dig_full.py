#!/usr/bin/env python3
"""Dig-side full 156-box M22 evaluation, using unchanged Astra pilot kernel.
Fixed cover and mesh, no adaptive subdivision. Writes only its own output area.
"""
import os,sys,json,hashlib,time
from pathlib import Path
from fractions import Fraction as F
from multiprocessing import Pool
ASTRA='/home/daybreak/bg-oblate-spheroid-c1b/research/astra/ASTRA_D5_M22_LOCAL_BOUND_CANDIDATES_20261105'
sys.path.insert(0,ASTRA)
import pilot as P
ROOT=Path(__file__).resolve().parent
COVER=Path('/home/daybreak/ダウンロード/m22_cover_39x4.json')
HASH=hashlib.sha256(COVER.read_bytes()).hexdigest()
SOURCE_HASH=hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest()
CONTRACT_HASH=hashlib.sha256((Path(ASTRA)/'contract.json').read_bytes()).hexdigest()
COVER_BOXES=json.loads(COVER.read_text())['boxes']
def evaluate(data):
    idx,box=data
    start=time.monotonic()
    ll,lh=map(F,box['lam']);zl,zh=map(F,box['z'])
    Z=max(abs(zl),abs(zh))
    fcap=((1+ll*ll)/2+Z)/(ll-Z)
    qcap=(fcap-1)/(fcap+1)
    assert F(0)<qcap<F(1)
    cells=P.CONTRACT['u_cells'];assert cells==32
    h=F(1,cells)
    total=F(0);midtotal=F(0);curvtotal=F(0);tailtotal=F(0)
    rows=[]
    for eps in (-1,1):
      for j in range(cells):
        a,b=F(j,cells),F(j+1,cells);m=(a+b)/2
        qm,nm,_=P.kernel(m,m,ll,lh,zl,zh,eps,qcap)
        qc,_,nc=P.kernel(a,b,ll,lh,zl,zh,eps,qcap)
        im,fm,tm,_=P.moment(nm,4,qm);ic,fc,tc,_=P.moment(nc,6,qc)
        mid=h*F(fm.lo,P.SCALE)
        curv=h**3/24*F(fc.lo,P.SCALE)
        tail=h*F(tm,P.SCALE)+h**3/24*F(tc,P.SCALE)
        low=mid+curv-tail
        total+=low;midtotal+=mid;curvtotal+=curv;tailtotal+=tail
        rows.append({'epsilon':eps,'cell':j,'u':[str(a),str(b)],
          'midpoint_q':qm.rec(),'cell_q':qc.rec(),
          'N2_midpoint':[v.rec() for v in nm],'N4_cell':[v.rec() for v in nc],
          'midpoint_bound':im.rec(),'curvature_bound':ic.rec(),
          'finite_midpoint_contribution':str(mid),'finite_curvature_contribution':str(curv),
          'tail_loss':str(tail),'lower_contribution':str(low)})
    assert len(rows)==64
    return {'index':idx,'box':box,'q_plus':str(qcap),'source_sha256':SOURCE_HASH,
        'cover_sha256':HASH,'contract_sha256':CONTRACT_HASH,
        'u_cells':cells,'moment_N':P.CONTRACT['moment_N'],
        'lower':str(total),'lower_float_reference':float(total),
        'finite_midpoint_sum':str(midtotal),'finite_curvature_sum':str(curvtotal),
        'tail_loss':str(tailtotal),'meets_minus_400':total>=-400,
        'elapsed_seconds':time.monotonic()-start,'records':rows}
def main():
    assert len(COVER_BOXES)==156
    for idx,box in enumerate(COVER_BOXES):
      i,k=divmod(idx,4);lh=F(2,5)+F(i+1,200);ll=lh-F(1,200)
      assert list(map(F,box['lam']))==[ll,lh]
      assert list(map(F,box['z']))==[k*lh/32,(k+1)*lh/32]
    P.checks()
    workers=int(os.environ.get('M22_WORKERS','8'))
    allrows=[]
    with Pool(workers) as pool, (ROOT/'m22_producer_results.jsonl').open('w') as out:
      for row in pool.imap_unordered(evaluate,enumerate(COVER_BOXES)):
        out.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
        out.flush()
        allrows.append(row)
        print('FINISHED',len(allrows),'/156','INDEX',row['index'],
            'LOWER',row['lower_float_reference'],'PASS',row['meets_minus_400'],flush=True)
    allrows.sort(key=lambda x:x['index'])
    assert [r['index'] for r in allrows]==list(range(156))
    worst=min(allrows,key=lambda x:F(x['lower']))
    info={'cover_sha256':HASH,'producer_source_sha256':SOURCE_HASH,
          'contract_sha256':CONTRACT_HASH,'producer':allrows,
          'producer_DONE':{'status':'COMPUTATION_COMPLETED_AWAITING_CHAT_COMPARISON',
            'count':156,'all_ge_minus_400':all(r['meets_minus_400'] for r in allrows),
            'worst_index':worst['index'],'worst_lower_exact':worst['lower']}}
    # Canonical compact JSON with exact rational strings
    target=Path.home()/'m22_dig_bundle.json'
    assert not target.exists(), 'Refusing to replace existing bundle'
    target.write_text(json.dumps(info,ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'M22_DONE.json').write_text(json.dumps(info['producer_DONE'],indent=2)+'\n')
    print('FINAL_FILE',target,flush=True)
    print('BUNDLE_SHA256',hashlib.sha256(target.read_bytes()).hexdigest(),flush=True)
    print('WORST',worst['index'],worst['lower'],float(F(worst['lower'])),flush=True)
    print('ALL_GE_-400',info['producer_DONE']['all_ge_minus_400'],flush=True)
if __name__=='__main__':main()
