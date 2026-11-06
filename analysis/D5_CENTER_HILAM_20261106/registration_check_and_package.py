from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib,shutil,datetime
SRC=Path('/home/daybreak/D5_HIGH_LAMBDA_DIAG_20261106')
REPO=Path('/tmp/d5-hilam-registration-20261106-16pzueyd/repo')
OUT=REPO/'analysis/D5_CENTER_HILAM_20261106'
assert not OUT.exists()
OUT.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
manifest=[]
def copy(p,rel):
 q=OUT/rel;q.parent.mkdir(parents=True,exist_ok=True)
 h=sha(p);shutil.copyfile(p,q);assert sha(q)==h
 manifest.append({'source_path':str(p),'registered_path':str(q.relative_to(OUT)),'size_bytes':p.stat().st_size,'sha256':h})
for p in sorted(SRC.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.tmp']:
  copy(p,'raw/'+str(p.relative_to(SRC)))
OLD=Path('/home/daybreak/D5_M40_work/m40_run_20261105')
for n in ['m40_pilot.py','m40_batch.py','chat_m40iv.py','chat_m22iv.py','calibration_contract.json']:
 copy(OLD/n,'sources/m40/'+n)
copy(Path('/home/daybreak/D5_M22_work/m22_run_20261106/m22_dig_full.py'),'sources/m22/m22_dig_full.py')
ASTRA=Path('/home/daybreak/bg-oblate-spheroid-c1b/research/astra/ASTRA_D5_M22_LOCAL_BOUND_CANDIDATES_20261105')
for n in ['pilot.py','contract.json']:copy(ASTRA/n,'sources/astra/'+n)
copy(Path(__file__),'registration_check_and_package.py')
def canon(b):return tuple(tuple(F(x) for x in b[k]) for k in (('lam' if 'lam' in b else 'lambda'),'rho','z') if k in b)
audit={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'READ_ONLY_COMPLETENESS_GEOMETRY_AND_EXACT_BOUND_CHECK_NOT_FRESH_INTERVAL_RECOMPUTATION','formal_adoption':'PENDING_CHAT_AUDIT_AND_JUDGE_DISPOSITION','lambda_interval':['119/200','33/50'],'original_sources_unchanged':True,'checks':{}}
for kind,count,threshold in [('m40',416,-400),('m22',52,-200)]:
 cover=SRC/('m40/high_m40_cover_candidate.json' if kind=='m40' else 'm22_high_cover_candidate.json')
 boxes=json.loads(cover.read_text())['boxes'];expected=[]
 for i in range(13):
  a,b=F(119+i,200),F(120+i,200)
  for j in (range(8) if kind=='m40' else [0]):
   for k in range(4):
    x=((a,b),)
    if kind=='m40':x+=((F(j,64),F(j+1,64)),)
    expected.append(x+((k*b/32,(k+1)*b/32),))
 assert [canon(x) for x in boxes]==expected and len(set(expected))==count
 if kind=='m40':
  rows={role:[json.loads((SRC/'m40'/role/'boxes'/f'{i:04d}.json').read_text()) for i in range(count)] for role in ['producer','verifier']}
  dones={role:json.loads((SRC/'m40'/role/'DONE.json').read_text()) for role in rows}
 else:
  rows={'producer':json.loads((SRC/'m22_high_producer_diagnostic.json').read_text())['producer'],'verifier':[json.loads(x) for x in (SRC/'m22_high_chat_verifier_diagnostic.jsonl').read_text().splitlines()]}
  dones=None
 entry={'box_count':count,'geometry_against_instruction_formula':'PASS','one_to_one_pairing':'PASS','actual_cover_sha256':sha(cover),'threshold_exact':str(threshold),'roles':{}}
 for role,rr in rows.items():
  assert len(rr)==count and [canon(x['box']) for x in rr]==expected
  assert all(x.get('index',i)==i for i,x in enumerate(rr))
  assert all(x.get('cover_sha256',sha(cover))==sha(cover) for x in rr)
  if kind=='m40':
   assert all(x['role']==role for x in rr)
   assert all(x['source_sha256']==sha(OLD/('m40_pilot.py' if role=='producer' else 'chat_m40iv.py')) for x in rr)
  elif role=='producer':
   assert all(x['source_sha256']==sha(ASTRA/'pilot.py') and x['contract_sha256']==sha(ASTRA/'contract.json') for x in rr)
  vals=[F(x['lower']) for x in rr];w=min(range(count),key=lambda i:vals[i]);assert min(vals)>=threshold
  entry['roles'][role]={'count':len(rr),'all_meet_threshold':True,'worst_index':w,'worst_lower_exact':str(vals[w]),'worst_lower_float_reference':float(vals[w])}
  if dones:
   d=dones[role];assert d['count']==count and d['cover_sha256']==sha(cover) and F(d['worst_lower_exact'])==vals[w] and d['worst_index']==w and d['all_ge_minus_400']
 audit['checks'][kind]=entry
 bundle={'status':'COMPUTATION_COMPLETE_NOT_FORMALLY_ADOPTED','cover':json.loads(cover.read_text()),'cover_sha256':sha(cover),'producer':rows['producer'],'verifier':rows['verifier'],'original_done_records':dones,'registration_completion_check':entry}
 write(OUT/(kind+'_hilam_bundle.json'),bundle)
 compact=[{'index':i,'box':rows['producer'][i]['box'],'producer_lower':rows['producer'][i]['lower'],'verifier_lower':rows['verifier'][i]['lower']} for i in range(count)]
 (OUT/(kind+'_hilam_bounds_compact.jsonl')).write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in compact))
c=json.loads((SRC/'c0_prime_dig_exact.json').read_text());a,b=map(F,c['c_interval']);n=18
power=list(map(F,c['I16_power_coefficients']))
bern=[sum((power[j]*sum((F(comb(j,k))*a**(j-k)*(b-a)**k*F(comb(i,k),comb(n,k)) for k in range(min(i,j)+1)),F(0)) for j in range(n+1)),F(0)) for i in range(n+1)]
assert bern==list(map(F,c['I16_Bernstein_coefficients']))
assert min(bern)==F(c['min_bernstein_exact'])
assert F(c['H_lower_exact'])==F(23800,25987)*min(bern)>=F(7,5)
audit['checks']['c0']={'stored_polynomial_to_Bernstein_exact_recalculation':'PASS','H_lower_exact':c['H_lower_exact'],'H_lower_float_reference':float(F(c['H_lower_exact'])),'all_19_coefficients_internal_match':True,'original_chat_c0_hilam_reference_comparison':'PENDING_REFERENCE_NOT_LOCATED','P1_proof_reaudit':'NOT_PERFORMED'}
audit['fixed_cover_pins']={'m40_expected':'2082e711a4d0e9a68947ed40ed358aff6eb9bab2f6fe34213b068ea3b8a03d87','m22_expected':'d7fc47723f35600a0753984e60ca0c1c0494fab3515494f744412a5fc4925580','status':'ACTUAL_BYTES_DIFFER_FIXED_FILES_NOT_LOCATED','note':'Box geometry matches the construction in the instruction. Equality to the unavailable pinned file contents, including mesh metadata, remains pending. Never overwrite raw cover hashes.'}
for m in manifest:assert sha(Path(m['source_path']))==m['sha256']
write(OUT/'SOURCE_MANIFEST.json',manifest)
write(OUT/'REGISTRATION_CHECK.json',audit)
readme="""# D5 high-lambda center column: computation evidence, adoption pending

Registered 2026-11-06 JST by Dig/Codex at the user's request.
Target: lambda in [119/200,33/50]; M40' on 0 <= rho <= 1/8, 0 <= z <= lambda/8; M22' on rho=0, 0 <= z <= lambda/8.

**All three computations exist and satisfy their numerical thresholds. This registration is not formal adoption.**
The old M40 1,248-box and M22 156-box runs cover [2/5,119/200], not this high-lambda band.

| Component | Completed computation | Existing second implementation | Formal adoption |
|---|---|---|---|
| C0' | Dig exact Bernstein calculation, H lower = 1.4641310094381321... >= 7/5 | Original chat reference coefficient comparison pending | Pending |
| M40' | Producer 416/416 >= -400; worst -47.40499577249319... | chat verifier 416/416 >= -400; worst -68.6322956611115... | Pending |
| M22' | Producer 52/52 >= -200; worst -46.75005927034623... | chat verifier 52/52 >= -200; worst -42.69154354653672... | Pending |

All decimals are references only; exact rational values are retained in the bundles and compact indices.

## Evidence

- [C0' original exact result](raw/c0_prime_dig_exact.json) and [original script](raw/c0_prime_independent.py).
- [M40' paired full bundle](m40_hilam_bundle.json), [compact exact bounds](m40_hilam_bounds_compact.jsonl).
- [M22' paired full bundle](m22_hilam_bundle.json), [compact exact bounds](m22_hilam_bounds_compact.jsonl).
- [Read-only registration check](REGISTRATION_CHECK.json).
- [Byte-preserving source manifest](SOURCE_MANIFEST.json).
- Original computation files, statuses, per-box records, and M40 DONE files are copied unchanged under raw/.
- Unchanged evaluator/driver snapshots are under sources/. The scripts retain their original absolute paths; this is an evidence snapshot, not a newly portable execution environment.
- M22 had no standalone DONE.json in the source directory. The new bundle explicitly stores original_done_records=null and a separately labeled registration completeness check; no original completion marker was invented.

## Checks performed during registration

Exact rational construction check: 13 adjacent lambda intervals from 119/200 to 33/50, eight rho intervals for M40, four z intervals up to each lambda band's upper endpoint divided by 8. All producer/verifier rows match their cover one-to-one; indices are complete and unique. All exact lower bounds meet -400 (M40) or -200 (M22). Existing M40 DONE minima match the raw rows.

The C0 stored polynomial was independently converted to all 19 Bernstein coefficients and matched exactly, with H >= 7/5. This is an internal arithmetic consistency check, not a comparison with the absent original chat c0_hilam.py, nor a new proof of the inherited analytic assumptions.

No expensive interval integrations were rerun. The independent verifier outputs already present on the external PC were inspected. M40 verifier source SHA matches d39be478485cb1faaf804ddbf970ce1c790b0d7a5d0bf7f2fb400561c2cdad1b; M22 verifier source matches b4ea57e134150e57be8ced020eafa4cfd6c740af75d27939b108e23de38d6a89. M22 verifier rows do not embed source hashes; the driver and current source snapshot supply provenance, subject to chat review.

## Remaining adoption conditions

1. C0': compare the exact coefficients/minimum with chat's original high-lambda reference (c0_hilam.py, reported SHA prefix e3b65e0f).
2. Fixed-cover identity: actual high-lambda files were explicitly marked diagnostic candidates. Their byte hashes differ from the instruction's pins:
   - M40 actual cfd50476b22b1d01997939688d51893a3d3ceac2c06391b809bfd0a43c719329; expected 2082e711a4d0e9a68947ed40ed358aff6eb9bab2f6fe34213b068ea3b8a03d87.
   - M22 actual f5d0ce5a3169b4bf823c1b81f43eb6bfee5f0f948c62f0ee2fdc9dcd5ce011f5; expected d7fc47723f35600a0753984e60ca0c1c0494fab3515494f744412a5fc4925580.
   Their geometry matches the instruction formula, but the pinned source files were not located. Chat must check full cover/mesh equivalence and Judge must dispose of the differing pins. Do not silently rewrite the recorded hashes or promote diagnostic statuses.
3. Chat's independent audit of these registered results and Judge's formal disposition remain pending.
4. The center-column conclusion retains the upstream P1 hypotheses. With the three bounds formally accepted, the stated arithmetic margin is 7/5 - (1/64)*max(400/6,(33/50)^2*200/2) = 43/120 > 0.

Existing calculation processes, source files, certificates, and the working repository were not changed. Only copies and registration documents were created in a separate checkout.
"""
(OUT/'README.md').write_text(readme)
files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS']
(OUT/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(OUT))+'\n' for p in sorted(files)))
print(json.dumps({'registered_directory':str(OUT),'file_count':len(files)+1,'total_bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),'audit':audit},indent=2))
