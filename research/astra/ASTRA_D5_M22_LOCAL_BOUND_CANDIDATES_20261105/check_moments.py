"""Independent Fraction-arithmetic audit of recorded moment bounds and aggregation.
Does NOT independently regenerate physical jets: that audit remains open.
"""
from fractions import Fraction as F
from math import comb,factorial,prod
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
def cv(x):return x if isinstance(x,tuple) else (F(x),F(x))
def add(a,b):
    a,b=cv(a),cv(b);return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    a,b=cv(a),cv(b);v=[x*y for x in a for y in b];return min(v),max(v)
def bounds(raw):return tuple(map(F,raw))
def moment(cs,r,q):
    N=24;J=len(cs)-1
    coefficients=[]
    for m in range(N+1):
        a=(F(0),F(0))
        for j,c in enumerate(cs):a=add(a,mul(c,F(1,2*(j+m)+1)))
        coefficients.append(mul(a,(-1)**m*comb(r+m-1,m)))
    finite=coefficients[-1]
    for a in coefficients[-2::-1]:finite=add(mul(finite,q),a)
    beta=[]
    for i in range(J+1):
        b=(F(0),F(0))
        for j in range(i+1):b=add(b,mul(cs[j],F(comb(i,j),comb(J,j))))
        beta.append(b)
    w=[F(comb(J,i)*2**(J-i)*factorial(J-i),prod(51+2*i+2*l for l in range(J-i+1))) for i in range(J+1)]
    C=comb(r+24,25)*q[1]**25
    et_lo=C*min(sum(max(0,b[1])*wi for b,wi in zip(beta,w)),
                sum(max(0,b[1])/F(51+2*j) for j,b in enumerate(cs)))
    et_hi=C*min(sum(max(0,-b[0])*wi for b,wi in zip(beta,w)),
                sum(max(0,-b[0])/F(51+2*j) for j,b in enumerate(cs)))
    return finite[0]-et_lo,finite[1]+et_hi

data=json.loads((ROOT/'results.json').read_text())
contract=json.loads((ROOT/'contract.json').read_text())
assert data['contract']==contract
assert contract['u_cells']==32 and contract['moment_N']==24
assert len(data['cases'])==2
assert data['source_sha256']==hashlib.sha256((ROOT/'pilot.py').read_bytes()).hexdigest()
assert data['contract_sha256']==hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest()
count=0;out=[]
for case in data['cases']:
    rows=case['records']
    assert len(rows)==64
    assert {(r['epsilon'],r['cell']) for r in rows}=={(e,j) for e in (-1,1) for j in range(32)}
    total=F(0)
    for row in rows:
        j=row['cell'];a,b=map(F,row['u'])
        assert (a,b)==(F(j,32),F(j+1,32))
        for key,qk,ik,r,deg in [('N2_midpoint','midpoint_q','midpoint_bound',4,4),('N4_cell','cell_q','curvature_bound',6,6)]:
            co=list(map(bounds,row[key]));q=bounds(row[qk]);claimed=bounds(row[ik])
            assert len(co)==deg and 0<=q[0]<=q[1]<1
            check=moment(co,r,q)
            assert claimed[0]<=check[0] and claimed[1]>=check[1],(case['name'],j,key)
            count+=1
        low=F(row['lower_contribution'])
        recomputed=(b-a)*F(row['midpoint_bound'][0])+(b-a)**3/F(24)*F(row['curvature_bound'][0])
        assert low==recomputed
        assert low==F(row['finite_midpoint_contribution'])+F(row['finite_curvature_contribution'])-F(row['tail_loss'])
        total+=low
    assert total==F(case['lower'])
    limit=-12 if case['name']=='center_half' else -191
    assert total>limit
    out.append({'name':case['name'],'lower':str(total),'strict_rational_comparison':f'lower > {limit} > -400'})
result={'status':'MOMENT_AND_AGGREGATION_CHECK_PASS','moments_checked':count,
        'physical_cells_checked':128,'cases':out,
        'not_checked':'independent physical jet reconstruction and original K20 normalization'}
(ROOT/'moment_checker_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

