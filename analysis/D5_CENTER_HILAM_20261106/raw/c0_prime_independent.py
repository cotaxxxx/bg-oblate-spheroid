#!/usr/bin/env python3
"""Dig independent exact-rational C0' Bernstein coefficient calculation.
Not an independent proof of inherited P1 normalization.
"""
import json,hashlib
from fractions import Fraction as F
from math import comb
from pathlib import Path
ROOT=Path(__file__).resolve().parent
lo=F(119,200);hi=F(33,50)
a=1-hi**2;b=1-lo**2
g=2*lo/(1+lo*lo)
pref=3*g/(2+g)
n=18
power=[F(0) for _ in range(n+1)]
for j in range(17):
 power[j]+=(j+1)*(F(1,2*j+1)+F(1,2*j+3))
 power[j+1]-=(j+1)*F(2,2*j+3)
 power[j+2]+=(j+1)*(-F(2,2*j+5)+F(2,2*j+7))
d=b-a
cx=[sum((power[i]*comb(i,k)*a**(i-k)*d**k for i in range(k,n+1)),F(0)) for k in range(n+1)]
bern=[sum((cx[k]*F(comb(i,k),comb(n,k)) for k in range(i+1)),F(0)) for i in range(n+1)]
i=min(range(n+1),key=lambda t:bern[t])
mine=bern[i];bound=pref*mine
assert n==18 and len(bern)==19
assert bound>=F(7,5)
res={'status':'DIG_INDEPENDENT_EXACT_BERNSTEIN_CALC_PASS_PENDING_CHAT_COEFFICIENT_MATCH',
  'lambda_interval':[str(lo),str(hi)],'c_interval':[str(a),str(b)],
  'gamma_lower_exact':str(g),'gammaR_lower_exact':str(pref),
  'I16_power_coefficients':[str(x) for x in power],
  'I16_Bernstein_coefficients':[str(x) for x in bern],
  'min_coefficient_index':i,'min_bernstein_exact':str(mine),
  'H_lower_exact':str(bound),'H_lower_float':float(bound),
  'margin_above_7_over_5_exact':str(bound-F(7,5)),
  'n':n,'moment_truncation':16}
out=ROOT/'c0_prime_dig_exact.json';out.write_text(json.dumps(res,ensure_ascii=False,separators=(',',':'))+'\n')
print('MIN_BETA_INDEX',i,'MIN_BETA_EXACT',mine)
print('GAMMA_R_LOWER',pref)
print('H_LOWER_EXACT',bound,'H_FLOAT',float(bound),'MARGIN',float(bound-F(7,5)))
print('OUTPUT_SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
