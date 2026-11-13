"""PB-RUN-1 acceptance: structural checks + progressive exact resample of 200 final records (seed 20261110) + the minimum box."""
import sys, os, json, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from multiprocessing import Pool
import chat_planb_run as R
out, res, part = sys.argv[1], sys.argv[2], sys.argv[3]
recs = {}
for l in open(out):
    r = json.loads(l); assert r['box']['name'] not in recs, 'duplicate name'; recs[r['box']['name']] = r
if part == 'struct':
    G = {b['name']: b for b in R.gen()}
    base = {n: r for n, r in recs.items() if int(r['box'].get('level', 0)) == 0}
    print('records', len(recs), 'base', len(base), 'base == frozen gen:', set(base) == set(G) and all(base[n]['box'] == G[n] for n in G))
    neg = [r for r in base.values() if not Fr(r['H_lower']) > 0]
    kids = {c['name']: c for r in neg for c in R.refine(r)}
    ch = {n: r for n, r in recs.items() if int(r['box'].get('level', 0)) > 0}
    print('non-positive base', len(neg), 'children', len(ch), 'children == R1B(level 1) of them:', set(ch) == set(kids) and all(ch[n]['box'] == kids[n] for n in kids))
    print('children all positive:', all(Fr(r['H_lower']) > 0 for r in ch.values()), 'min child %.6f' % min(float(Fr(r['H_lower'])) for r in ch.values()))
    print('method', {r['method'] for r in recs.values()}, 'spec', {r.get('spec') for r in recs.values()}, 'pos flag consistent:', all(r['pos'] == (Fr(r['H_lower']) > 0) for r in recs.values()))
    from collections import Counter
    print('REFINE by parent j:', sorted(Counter(r['box']['j'] for r in neg).items()))
    sys.exit(0)
fin = [r for n, r in recs.items() if (n + '_h0') not in recs and (n + '_h1') not in recs]
random.seed(20261110); pick = random.sample(fin, 200)
mn = min(fin, key=lambda r: Fr(r['H_lower']))
sel = {'a': pick[:100], 'b': pick[100:] + ([mn] if mn not in pick else [])}[part]
done = set()
if os.path.exists(res):
    for l in open(res): done.add(json.loads(l)['name'])
todo = [r for r in sel if r['box']['name'] not in done]
ref = {r['box']['name']: r['H_lower'] for r in sel}
def one(bx): return R.one(bx)
with Pool(int(sys.argv[4]), maxtasksperchild=1) as pool, open(res, 'a') as f:
    for q in pool.imap_unordered(one, [r['box'] for r in todo]):
        n = q['box']['name']
        f.write(json.dumps({'name': n, 'level': q['box'].get('level', 0), 'H_run': ref[n], 'H_chat': q['H_lower'], 'match': ref[n] == q['H_lower'], 'sec': q['sec']}) + '\n'); f.flush()
