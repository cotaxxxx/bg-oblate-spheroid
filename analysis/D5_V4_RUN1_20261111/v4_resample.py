"""resample the same 200 boxes chat_v4_run.cover --sample 200 would pick (seed 20261110), writing each result as it completes."""
import sys, os, json, random
sys.path.insert(0, sys.argv[1])
from multiprocessing import Pool
import chat_v4_run as R
out, part, res = sys.argv[2], int(sys.argv[3]), sys.argv[4]
recs = {}
for l in open(out):
    r = json.loads(l); recs[(r['box']['name'], int(r['box'].get('level', 0)))] = r
lev = {}
for (n, l) in recs: lev[n] = max(lev.get(n, -1), l)
fin = [r for (n, l), r in recs.items() if l == lev[n] and (n + '_h0') not in lev and (n + '_h1') not in lev]
random.seed(20261110); pick = random.sample(fin, 200)
pick = pick[:100] if part == 0 else pick[100:]
done = set()
if os.path.exists(res):
    for l in open(res): done.add(json.loads(l)['name'])
todo = [p for p in pick if p['box']['name'] not in done]
with Pool(2, maxtasksperchild=1) as pool, open(res, 'a') as f:
    for p, q in zip(todo, pool.imap(R.one, [p['box'] for p in todo])):
        f.write(json.dumps({'name': p['box']['name'], 'match': p['H_lower'] == q['H_lower'], 'H': q['H_float']}) + '\n'); f.flush()
print('part', part, 'done')
