# D-OB P2 修正方針 Predeclare
## 監査反映確定版

### 0. 文書の目的
本書は D-OB P2 smoke 不合格後の checker replay、770 point-limit、N帯監査、003 point-limit を受け、SPEC V3 候補比較の前に証拠強度、不変条件、候補、guard、受理順序を固定する。machine evidence ではない。

SPEC V2 §6 Versioning に従い、候補 (a)〜(e) はすべて SPEC V3 候補であり、採用時には新version・fresh run・新identityを必要とする。本書では候補を選ばない。

# 1. Canonical identity
- P1 design note SHA-256: 2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9
- SPEC V2 SHA-256: 19af6f7f4aa68771707bc3ffe1abf06fabbbc3098b4bfe0710db00631b8bb069
- predeclare/correction SHA-256: 315e1d9e017986d796f71274367dcf155ffa75f03fa88927be0b4cb578000901
- producer SHA-256: dff79bc40d78d53a1491c3edbe368034b2d28a4894da45ac13b3b04c3ad0f19b
- checker SHA-256: 762bcf380b091a6fa7c1da50bba06ea0d89a7a56dbe83ce7fb1477b827fc6290
- canonical HEAD at diagnosis: c0f099f946b28e00db95d9ece6c1da703a6dc3b9

P1 §8.2 (ii),(iv) を near-column kernel と F_rhorho 包み込みの基礎定義として用いる。

# 2. Established

## 2.1 Smoke
producer smoke は完走。accepted 505、unresolved 7,662、terminal 8,167。§7 unresolved=0 gate 不合格につき D-P2 = NOT_CERTIFIED。7,662 unresolved はすべて near column、すべて depth 12。

## 2.2 Far column
far column 455葉は全accept。7,0,0 は独立checkerでも249葉、8,963,877セルを再評価してPASS。D-P2全体のcertificationを意味しない。

## 2.3 Checker replay
read-only verifier は VERDICT REPLAY_AS_PREREGISTERED pass=22 fail=0。これは事前登録どおりのreplayであり、D-P2 certification PASSではない。

## 2.4 770 point-limit
192点は A=68、N=80、B=44 の三帯。B帯44点すべてで B_cut > 10 L。
point box では lambda-z < 2rho なら B_cut>0。逆向きは成立せず、境界付近に4反例。

# 3. Strong diagnostic evidence

## 3.1 診断した N 型の点は enclosure-width failure である
N7 v3 の Σupper<0 解釈は撤回。kval.lower() を先に取り出したため midpoint/width が lower sum の言い換えとなり、gateもlower再構成しか検査していなかった。「N=(i-a)、真値が負」は Empty。

独立計算は区間証明ではなく非区間浮動小数点診断。7,7,0 ではA/Nを含む9点（cut=1024の2点も分類上N）、correct-target 0,0,3 では7点を計算。7,7,0 のHは独立2経路で約+1.16〜+1.25、0,0,3 のJは約+6.17〜+6.20。比較可能点で L < J < Σupper。

よって、診断したN型点について「真のJは正だがenclosure widthでlower boundが負になる」をStrong diagnostic evidenceとする。B帯へ拡張しない。

## 3.2 Near enclosure 健全性の診断
7,7,0 のpoint box 4点、各約5.9万〜6.0万セル、合計約24万セルで、各セル中心の独立真値がproducer interval外となる例は0件。セル中心のみでありセル全体の包含証明ではない。0,0,3 では同じセル中心包含検査は未実施。

# 4. P003 point-limit

## 4.1 Wrong-target
旧実行 lambda=173/400 は initial box 0,0,3 のlambda範囲 [119/200,33/50] 外。wrong-target diagnostic として履歴保存しP003判定には使わない。

## 4.2 Correct-target
t=1/64、lambda=251/400、r={.010,.014,.018,.022,.030,.060,.100}。
対象box [0,1/8]×[0,1/8]×[119/200,33/50] membership を実行前assert。

.010,.014,.018,.022 はaccepted、.030,.060,.100 はmax_cell_count。全7点 cut=0、B_cut=0。P003-1=PASS。
境界は 0.022 < r* < 0.030 で1/64を挟まず、lambda=173/400 の境界とも異なる。P003-2=FAIL。

correct-target は先にchat側 commit 69393c5 で再現し、その後実行側でも同じ7点を再実行して数値一致。chat側・実行側の2環境再現とする。

## 4.3 含意
depth-8のr方向accept境界がpoint-limit境界そのものという説明は棄却。有限幅boxで失敗した r∈[1/64,0.022] にpoint-limitではaccept点が存在する。さらに細かい有限幅boxでaccept増加の可能性はあるが、単調性は未証明。

# 5. Not established
1. 有限幅box細分化がpoint-limitへ単調に近づくこと。
2. depth 12より先で全unresolvedがacceptされること。
3. P全体でH>0。
4. point-limit境界を有限幅box境界として使えること。
5. セル中心診断だけでnear enclosureのセル全体健全性が証明されたこと。
6. 候補(a)〜(e)のいずれかがunresolvedを解消すること。
7. B帯の真のJの符号。B分類点の独立計算は未実施。
8. 3,3,1 の独立checker検証。
9. lambda-z<2rho ⇒ B_cut>0 の逆命題。4反例あり。

# 6. 現在の分類
診断したN型点のenclosure-width failureは Strong diagnostic evidence。
near-column unresolved全体の改善で enclosure width 縮小を主要設計課題として調査すべき、という一般化は Design inference。B帯J符号未確認につき全near原因がwidthとはしない。

# 7. SPEC V3候補
全候補はSPEC変更でありfresh runを要する。

## (a) rho enclosure変更
現行 S(B)=[-rho_hi,+rho_hi] 全体評価をsoundに分割、または別のsoundな評価へ変更する候補。

## (b) exclusion ball中心変更 — (a)との連成候補
SPEC §3 は全 p_s=(s,0,z), s∈S(B) が球内にあることを要求する。現行S(B)のまま中心だけ移す案は不可。(a)で評価点集合を変更・分割し、各集合の全p_s包含を証明する。(a)+(b)の連成候補として扱う。

## (c) 球面セル細分化・resource budget変更
SPEC §6 の MAX_CELL_COUNT=2^16、MAX_CELL_DEPTH=10、MAX_BOX_DEPTH=12、regular cell selection、ceil(N_reg/4)、score、split rule はすべてSPEC事項。budget/depth/selection/split/score変更はいずれもSPEC V3変更。

## (d) RHO0変更
SPEC変更。(d)だけが特別なのではなく(a)〜(e)すべてSPEC V3。

## (e) 解析処理への委譲
極近傍を解析評価へ委譲し軸上C系と接続する候補。解析領域・数値領域・接続条件を事前固定する。

# 8. 不変条件
1. Soundness: 包含根拠を明示。セル中心独立包含controlを常設するがproofの代替にしない。
2. Producer/checker independence: producer import・共有kernel化で一致させない。SPEC V2 L72,L76,L93 の独立性を保つ。
3. F1修正: signal inheritance/deadlock対策をproducer/checker双方へ。数学変更と分離。
4. Checker diagnostic mode: 3,3,1等を独立検証可能にするがformal fail-closed semanticsは変更しない。

# 9. Harness / guard
G1 Lower consistency: producer lower sumと独立再構成を照合。
G2 Upper consistency: upper sumも照合。
G3 Operation-order identity: upperの演算順序まで固定し、異なる量をbitwise同一視しない。
G4 Target membership: initial-box index,r,t,lambdaを記録し、対象box内を実行前assert。
G5 Independent reproduction: 重大結論前に可能な限り別環境・別経路で再現。
G6 Evidence separation: DIAGNOSTIC / NOT_EVIDENCE をmachine evidenceへ混入しない。
G7 Process/exit-code capture: 長時間走行は原則 setsid nohup。wrapperで実際の終了コードを必ずファイル保存し、PID、開始時刻、終了コード、log、identityを監査可能にする。

# 10. SPEC V3候補比較で記録する量
accepted/unresolved、cut cells、regular cells、L、B_cut、独立J、upper sum、enclosure width、cell count、maximum depth、runtime/CPU、failure reason。

N型では J-L と Σupper-J を追跡。B型では独立J符号が未確認であることを保持。

# 11. 受理順序
1. Soundness
2. Identity / reproducibility
3. Width reduction
4. Certification utility
5. Cost
6. Independent checking

accept数改善だけでsoundness/independenceを弱める案は不採用。候補比較runはすべてDIAGNOSTIC。採用案をSPEC V3として固定した後、fresh formal runを行う。

# 12. 本書で裁定しない事項
(a)〜(e)の優先順位、採用案、RHO0、新cell budget/depth/split rule、exclusion ball中心、新S(B)、解析/数値境界は決めない。次工程の「SPEC V3候補比較実験 predeclare」で実行前凍結する。

# 13. 固定結論
D-P2 = NOT_CERTIFIED。

診断したN型点では、真のJ>0でenclosure widthによりlower boundが負になることがStrong diagnostic evidenceで支持される。

N型診断、770三帯、correct-target P003から、SPEC V3候補ではnear-column enclosure width縮小を主要設計課題として調査する、というDesign inferenceを置く。

ただしB帯J符号、P全体H>0、有限幅box単調性は未確定。near unresolved全体の原因がwidth、または細分化で必ず解決する、とは主張しない。

次工程は(a)〜(e)を具体的SPEC V3候補へ落とし込み、比較実験predeclareを実行前に固定することである。
