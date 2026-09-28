# D-OB P2 — SPEC V3 候補比較実験 Predeclare
## v1 — Phase 0 execution predeclare

Status: PHASE 0 FREEZE CANDIDATE / DIAGNOSTIC / NOT_EVIDENCE

# 0. 文書の目的
本書は、内容 CLOSED の `analysis/D_OB_P2_REVISION_DIRECTION_PREDECLARE.md` を唯一の設計入力として、SPEC V3 候補比較に先立つ Phase 0 と、その後の候補比較の versioning 境界を実行前固定する。

入力 predeclare:
- commit: `1a868473f252a293ee7b93b14a96b00865c2e4ad`
- file SHA-256: `993c174c1f43de7b3fdf8cfeae0ff27711d6190623c210897020c090ece278c4`
- git blob: `08a02290309d7f01d2bfbb57813bf34fc4b214d7`
- candidate ref `candidate/dob-p2-revision-predeclare` = `1a868473`。2026-09-28、chat 側が `git fetch` により、blob `08a02290`、SHA-256 `993c174c`、親の commit `c0f099f9`、差分（1ファイル・138行の追加）を照合し、すべて一致した。canonical ブランチ `design/d-ob-p2` には未反映（`c0f099f9` のまま）。

全比較は DIAGNOSTIC / NOT_EVIDENCE。v1 は Phase 0 のみを認可し、candidate comparison は BLOCKED。Phase 0 gate 後、続行可能時だけ §23.2 を具体化し v2 として再監査・再freezeする。

# 1. Canonical baseline
- diagnosis HEAD: `c0f099f946b28e00db95d9ece6c1da703a6dc3b9`
- producer SHA-256: `dff79bc40d78d53a1491c3edbe368034b2d28a4894da45ac13b3b04c3ad0f19b`
- checker SHA-256: `762bcf380b091a6fa7c1da50bba06ea0d89a7a56dbe83ce7fb1477b827fc6290`
- P1 note SHA-256: `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`
- SPEC V2 SHA-256: `19af6f7f4aa68771707bc3ffe1abf06fabbbc3098b4bfe0710db00631b8bb069`

Smoke: accepted 505, unresolved 7662, terminal 8167, NOT_CERTIFIED。770 map: A68/N80/B44。results_192.tsv SHA-256 `6ad29461e42c265ce136e8df114400072e939335d72e2033b79741461e93fa90`。N diagnostic 既知点では true J positive。B44 の true J sign は Phase 0 前には未確定。

# 2. Evidence boundary
禁止:
1. diagnostic を formal evidence と呼ぶ。
2. point result を box proof へ昇格する。
3. floating H/J を interval proof へ昇格する。
4. accepted count を soundness とみなす。
5. diagnostic harness を formal producer/checker lineage へ流用する。
6. 結果確認後の変更を versioning なしで行う。
変更時は停止し、version up → 再監査 → 再freeze。

# 3. Phase 0 — B-band baseline sign diagnostic
B44 全点を使用し、代表点抽出をしない。pinned results_192.tsv の class=B 44行を機械生成する。各点座標は厳密分数として構成・記録する。

# 4. G4 target membership
各点について計算前に initial-box index、cell index、exact r/t/lambda、target bounds を記録し、厳密分数で membership assert。1点でも失敗なら Phase 0 全体 INVALID。その点だけ除外して続行禁止。

# 5. Phase 0 independent computation
新規 harness を使用する。数学関数 `geom`, `F`, `Frho` は commit `dabc2a3b` の `tools/d_ob_p2/independent_H_sign.py`、SHA-256 `2dcd16673c214369ba0555e653dae51fca7d3f3cf13c83aeac4fd000d5bfccd7` から逐語再利用する。tolerance、step sizes、B44 I/O は新規コード。harness SHA-256 は v1 freeze 時に pin する。producer enclosure kernel / interval lower-upper / accept logic は import しない。

`J = 2*pi*lambda*H`。sign decision は H に基づく。

Route B: `K_H=(F_rho(rho)-F_rho(-rho))/(2*rho)` を評価して H を積分する。
Route A: `F=h*alpha^2` から E を直接積分し、rho 中心差分で H を求める。
Route A step sizes: `d in {1e-2*rho,1e-3*rho,1e-4*rho}`。baseline `d0=1e-4*rho`。3値すべて記録。非有限/評価失敗は conclusive にしない。

# 6. Numerical convergence
Standard:
- inner phi: epsabs=1e-11, epsrel=1e-10, limit=200
- outer mu: epsabs=1e-10, epsrel=1e-9, limit=400
- points=[0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2]

Tightened:
- inner: epsabs=1e-12, epsrel=1e-11, limit=200
- outer: epsabs=1e-11, epsrel=1e-10, limit=400
- points/limits は standard と同一。
全設定を machine-readable header に echo する。

# 7. Sign decision
各点を POSITIVE / NEGATIVE / INCONCLUSIVE とする。Conclusive iff:
1. Route B と Route A が同符号。
2. Route A の3 step sizes が同符号。
3. Route B と baseline Route A で `|H_B-H_A| <= 1e-4*|H|`。
4. standard→tightened の各 route で `|Delta H| <= 1e-4*|H|`。
5. nonfinite / integration failure は conclusive でない。IntegrationWarning は全記録するが warning 単独では INCONCLUSIVE にしない。
相対基準の `|H|` は比較する2値の絶対値の小さい方。absolute floor なし。0近傍で不安定なら INCONCLUSIVE。post-hoc floor 禁止。

# 8. Phase 0 gates
P0-A: 44/44 conclusive POSITIVE → sampled B は J>0 と整合。v2 起草可。(a)+(b) を候補に含めてよい。proof ではない。
P0-B: conclusive NEGATIVE >=1 → candidate comparison 停止。G5 separate reproduction → H=0 locus → P1再監査 → SPEC scope監査。
P0-C: NEGATIVE=0 かつ INCONCLUSIVE>=1 → v2へ自動進行禁止。追加高精度等は別裁定/version。

# 9. Candidate comparison boundary
v1では (a), (a)+(b), (c), (d), (e) は BLOCKED。すべて SPEC V3 change。

# 10. Candidate (a)
rho enclosure redesign。全 S(B) coverage、gapなし。split count/positions は v2 で固定。

# 11. Candidate (a)+(b)
(b)単独禁止。各 p_s inclusion を sound に扱う coupled exclusion geometry とする。具体式は v2 固定。

# 12. Candidate (c)
resource/spherical-cell redesign。MAX_CELL_COUNT, MAX_CELL_DEPTH, MAX_BOX_DEPTH, regular-cell selection, ceil(N_reg/4), score, split rule を v2 固定。

# 13. Candidate (d)
finite RHO0 candidate set を v2 固定。continuous post-hoc best-only 禁止。

# 14. Candidate (e)
analytic handoff near pole。analytic/numeric regions, overlap, claim/bound, handoff, boundary double-eval を v2 固定。sound bound 不在なら NOT READY。

# 15. Point / box sets
C1: 770 full 192 points。
C2: independent H 9 points（2 A + 7 N）。A/N別集計。J-L, SumUpper-J。
C3: B44。
C4: P003 correct target: r={.010,.014,.018,.022,.030,.060,.100}, t=1/64, lambda=251/400。7点、G4。point behavior only。

C5 finite-width:
source `full_terminal_map.tsv`, SHA-256 `0584110495c9d3b98a96d88e3d9fbe717bde326f2b76dcc465db784ad3bd26f8`。
1. C1各点 → containing 7,7,0 depth-12 box。
2. C4各点 → containing terminal 0,0,3 box。

## C5 deterministic membership rule
各座標の box membership は半開区間 `[lo,hi)`。ただし、その座標/domain の global upper endpoint に box の `hi` が一致するときだけ `[lo,global_hi]` とする。
- normal: `lo <= x < hi`
- `hi == global_hi`: `lo <= x <= hi`

各 target point について、この規則を満たす candidate box が **ちょうど1個** であることを assert する。0個または2個以上なら **C5 selection INVALID** として停止し、その点だけ除外して続行してはならない。
C1にも同じ規則を適用する。C4の `t=1/64` 共有面はこの規則により上側隣接箱（`lo=1/64`）へ一意帰属する。選択した全 box bounds を記録する。
finite-width J difference には **box-center Jを参考値としてのみ**使用し、box proofではないことを明記する。

# 16. Recorded quantities
candidate ID, code/config identity, initial-box index, exact r/t/lambda, C5 box bounds, accepted/unresolved, cut/regular cells, L, B_cut, independent J, C5 center-J flag, upper sum, enclosure width, J-L, SumUpper-J, cell count, max cell depth/box depth, runtime/CPU, resources if available, failure reason。missing reasonを記録。

# 17. Comparison
順序:
1. Soundness
2. Identity/reproducibility
3. Width
4. Certification utility
5. Cost
6. Independent checking

Soundness failureはreject。countsで復活させない。N widthはJ-L, upper-J。BはPhase0 gateに従う。Certification utilityはC5のみ。C1-C4はdiagnostic。MAX_BOX_DEPTH/splitはC5で評価。resource増加とbound-quality改善を区別する。

# 18. No scalar winner score
weighted scalar winner score禁止。gate順を維持し、tradeoffはhuman auditへ送る。

# 19. G1-G7
G1: lower consistency independent reconstruction。
G2: upper consistency independent reconstruction。
G3: operation-order identity。
G4: target membership exact/index before compute; fail closed。
G5: independent reproduction for negative/soundness/new sign/boundary where possible。
G6: DIAGNOSTIC/NOT_EVIDENCE separation。formal RUN_DIR/receipt/certificate/Judge evidenceへ混入禁止。
G7: process/exit capture。long runはsetsid/nohup、PID、UTC start/end、actual exit code、log、script/input SHA、config、git identityを保存。

# 20. Harness isolation
Diagnostic only。formal importsなし、formal RUN_DIR外、premature canonical merge禁止。F1/F2/F3/F4/F6 correctionはmath candidate changesと別commit/validation。

# 21. Stop conditions
1. Phase0 negative。
2. target membership fail。
3. lower/upper consistency fail。
4. containment/soundness fail。
5. pin mismatch。
6. candidate ambiguous。
7. post-hoc threshold/evaluationが必要。
8. formal artifact contamination疑い。
9. candidate条件が比較不能。
10. C5 deterministic membershipがtargetごとexactly oneでない。
停止後のfix runを同freeze-version continuation扱いしない。

# 22. Adoption
diagnostic results audit → soundness → human adoption decision → SPEC V3 text → freeze → independent producer/checker implementation → F-list corrections separately → fresh pins → fresh formal run。旧smokeをSPEC V3 formal evidenceへ再利用しない。

# 23. Versioned freeze items
## 23.1 v1
1. B44 input + SHA。
2. geom/F/Frho source pin。
3. Phase0 harness SHA。
4. H/J definitions + H-sign decision。
5. P0 gates。
6. exact Phase0 numerical settings: d set/d0、standard/tightened inner/outer、points。
7. C5 selection: C1→770 depth12、C4→003 terminal。半開 `[lo,hi)`、global upper endpointのみ閉。targetごとexactly-one assert。box bounds記録。finite-width J differenceはbox-center Jをreference only。

v1 freeze後、Phase0のみ実行可。candidate comparisonはBLOCKED。

## 23.2 v2 — candidate comparison 前
Phase 0 gate 後、candidate comparison へ進むことが許可された場合に限り、次を具体化する。
1. candidate (a) の S(B) 分割数・分割位置。
2. candidate (a)+(b) の exclusion-ball center/radius の具体式。
3. candidate (c) の cell budget/depth/selection/split/score。
4. candidate (d) の RHO0 candidate set。
5. candidate (e) の analytic/numeric boundary と analytic bound。

これらは **Phase 0 の結果を確認した後に決定した値であることを明記する。**
その後、文書を version up、再監査・再freezeする。v2 freeze 前に candidate comparison を実行してはならない。

# 24. Phase 0 execution order
1. Phase 0 harness の source identity / SHA-256 を照合する。
2. pinned `results_192.tsv` から B44 を機械生成する。
3. B44 がちょうど44点であることを assert する。
4. 全44点について G4 target membership を実行する。
5. 1点でも G4 が失敗した場合、Phase 0 全体を INVALID として停止する。
6. standard tolerance で44点を計算する。
7. tightened tolerance で44点を計算する。
8. Route A の3 step sizes を含む整合判定を行う。
9. `IntegrationWarning` を全件記録する。
10. 各点を POSITIVE / NEGATIVE / INCONCLUSIVE に機械判定する。
11. H および `J=2*pi*lambda*H` を記録する。
12. raw output、summary、input/output SHA-256、actual exit code、identity を監査へ提出する。
13. P0-A / P0-B / P0-C を裁定する。
14. candidate comparison は実行しない。

P0-Aならv2起草可。P0-Bならcandidate comparison停止、G5/H=0/P1-SPEC再監査。P0-Cならv2へ自動進行せず別裁定。

# 25. Pre-registered numerical-risk note
小さい rho では center difference が numerical cancellation の影響を受ける可能性がある。このため `1e-5*rho` は使用せず、`d in {1e-2*rho,1e-3*rho,1e-4*rho}` を事前固定する。
それでも小rho側でINCONCLUSIVEが集中する可能性を実行前登録する。その場合、結果確認後にstep size、tolerance、absolute floorを変更して同じv1として救済してはならない。P0-Cとして処理し、追加計算は別裁定・別versionとする。

# 26. Fixed conclusions before Phase 0
1. D-P2 = NOT_CERTIFIED。
2. 診断済み N 型点の enclosure-width failure は Strong diagnostic evidence。
3. B44 の true J sign は Phase 0 前には未確定。
4. Phase 0 は B44 全数を使用し、代表点抽出を行わない。
5. conclusive NEGATIVE が1点でもあれば candidate comparison を停止する。
6. Phase 0 の全結果は DIAGNOSTIC / NOT_EVIDENCE。
7. candidate (b) 単独は存在せず、(a)+(b) のみ。
8. (a)〜(e) はすべて SPEC V3 change。
9. v1 は Phase 0 だけを実行認可する。
10. candidate comparison は v2 freeze まで BLOCKED。
11. Phase 0 結果確認後に決定した candidate parameter は、その事実を v2 に記録する。
12. candidate run の成功は SPEC V3 certification ではない。
13. 採用候補決定後に SPEC V3 を別途 freeze し、その後にのみ fresh formal run を許す。

# 27. Status
**v1 — PHASE 0 FREEZE CANDIDATE**

v1 freeze scope は §3〜§8、§23.1、§24〜§26、およびそれらが依存する identity / evidence boundary / C5 deterministic selection rule とする。
v1 freeze 成立後、Phase 0 のみ実行可能とする。
candidate (a)、(a)+(b)、(c)、(d)、(e) comparison は BLOCKED。
Phase 0 gate 後、candidate comparison への移行が許可された場合のみ §23.2 を具体化する。
その値が Phase 0 結果確認後に決定されたことを記録し、文書を version up、再監査、v2 freeze する。
v2 freeze 前に candidate comparison を実行してはならない。
