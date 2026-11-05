from fractions import Fraction as F
from pathlib import Path
import json
import pilot as p
count=0
for eps in (-1,1):
    for u in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        q,n2,_=p.kernel(u,u,F(1),F(1),F(0),F(0),eps,F(0))
        val,_,_,_=p.moment(n2,4,q)
        mu=eps*(1-u*u)/(1+u*u);jac=4*u/(1+u*u)**2
        exact=jac*(10*mu**4-F(23,3)*mu*mu-F(1,3))
        assert F(val.lo,p.SCALE)<=exact<=F(val.hi,p.SCALE)
        count+=1
integral=10*F(2,5)-F(23,3)*F(2,3)-F(2,3)
assert integral==F(-16,9)
r={'sphere_exact_point_controls':count,'sphere_integrated_polynomial':str(integral),
   'scope':'auxiliary consistency only; not full-domain physical jet verification'}
Path(__file__).with_name('normalization_checks_result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))

