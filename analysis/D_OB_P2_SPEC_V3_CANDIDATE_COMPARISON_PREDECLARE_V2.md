# D-OB P2 — SPEC V3 候補比較実験 Predeclare
## v2 — candidate comparison draft

Status: DRAFT FOR CHAT AUDIT / DIAGNOSTIC / NOT_EVIDENCE / NOT_FROZEN

# 0. Purpose and provenance
本書は v1 `analysis/D_OB_P2_SPEC_V3_CANDIDATE_COMPARISON_PREDECLARE.md` を version up し、Phase 0、candidate (a) pilot A4、extended pilot の結果確認後に決定した candidate comparison 値を固定する draft である。
本書の全充填値は **Phase 0・A4・extended pilot の結果を確認した後の決定**であり、事前登録値を装わない。
candidate comparison は本書の chat 全文監査と **v2 FREEZE countersign** が成立するまで BLOCKED。

# 1. Canonical baseline and evidence boundary
v1 の Canonical baseline、§2 Evidence boundary、G1-G7、§20 Harness isolation、§21 Stop conditions、§22 Adoption を継承する。
D-P2 は NOT_CERTIFIED。本比較は DIAGNOSTIC / NOT_EVIDENCE であり、point result、floating J、accepted count を box proof または formal evidence へ昇格しない。

# 2. Phase 0 closure and C3 pin
Phase 0 B44 は P0-A: POSITIVE=44, NEGATIVE=0, INCONCLUSIVE=0。
- harness commit: `bb2bdbd56de6d020f9227ef9b85c8c8979d1c0d3`
- harness SHA-256: `7268ee90518c752658fa7744e956a3efc5386e2ce56544e547a056dcb3e05eda`
- input results_192.tsv SHA-256: `6ad29461e42c265ce136e8df114400072e939335d72e2033b79741461e93fa90`
- phase0_points.tsv SHA-256: `361db4a7c5fbe3bc6c8afc335282af8b26a1bf653dd5edf1dde56d08e634b4e0`
- summary.json SHA-256: `acdda12d653815894e455e4f53ed72c3e8122d59ca9973fdcc285cf0b07f362d`
- run log SHA-256: `0662b73304d345170cd55455763a8b23a9e130d2ffb118c90311c5cb43d0b3df`
これは sampled B44 の J>0 と整合する diagnostic であり proof ではない。C3 はこの pin を参照する。
# 3. Candidate (a) closure — CLOSED
固定分割 rho-enclosure 路線の (a) と (a)+(b) は比較集合から除外する。

A4:
- output `sigma_pilot_k1248.tsv` SHA-256: `afed07837353095344befb865c3ee94c9a7020a67b2d4e86f68973dc20635d54`
- predeclare SHA-256: `dbef315750f1ccacc037d6962450319a74bdb47578323e995dfc495fbf1c0b08`
- judge SHA-256: `8e481042d4e3b7bde30fce400cbfc15c42f905df89fbe550b7cf7ae1440ad746`
- verdict: `NOT READY at k<=8`。

Extended pilot:
- output `sigma_pilot_ext_k1_8_16_32_64.tsv` SHA-256: `8dd1fb2581619140c66d6f4e0f31f1ca2e4a60450fbefce6b157c261a5a7a286`
- predeclare SHA-256: `b80a565f7e4a0e81e8397ac7c97b261550b1a5a9738e0303f3093eba27287392`
- judge SHA-256: `7ff450e69cd516a69179d59598c5ada393dd51a108a9d0085afdee4c9346b507`
- verdict: `candidate (a) NOT READY at fixed partition, k<=64`。
- count series: k=8/16/32/64 = `120/121/122/122` of 240。

この飽和曲線は記述的設計材料としてのみ使用する。k=8→16 以後の改善が小さいため、固定 partition の sigma-split 追加より partition/resource 側を比較対象とする。これは soundness/certification の証明ではない。

**唯一の復活条項:** candidate (c) 比較完了後、結果に基づき `(a)+(c)` 複合構成を **新 version の新項目**として提案し得る。それ以外の黙示的復活、現 v2 への後付けは禁止する。

# 4. Candidate set in v2
比較対象は **(c), (d), (e)** のみ。(a), (a)+(b) は CLOSED。(b) 単独は引き続き存在しない。

# 5. Candidate (c) — spherical-cell/resource redesign
Baseline C0 は SPEC V2 のまま:
`MAX_CELL_COUNT=2^16`, `MAX_CELL_DEPTH=10`, `MAX_BOX_DEPTH=12`。
cell round は全 bisectable cut cell + score 最大の `ceil(N_reg/4)` regular cells。
score は `upper(|C| * width(K(C,B)))` の exact comparison、tie は cell order。
box split は normalized width 最大座標、normalization `r:1, tau:1, lambda:13/50`、tie order `r,tau,lambda`。
## 5.1 One-change-at-a-time configurations
| ID | C0 からの唯一の変更 | 固定値 | 帰属 |
|---|---|---|---|
| C-count | cell-count budget | `MAX_CELL_COUNT=2^17` | 純粋な cell resource 増加 |
| C-cell-depth | cell depth | `MAX_CELL_DEPTH=11` | より深い spherical-cell refinement |
| C-box-depth | box depth | `MAX_BOX_DEPTH=13` | parameter-box resource 増加 |
| C-regular | regular selection fraction | `ceil(N_reg/2)` | 1 round 当たりの bound-quality 改善を狙う selection 変更 |

各構成では表にない値を C0 から変更しない。組合せ構成は v2 比較に含めない。
特に C-count/C-box-depth は **resource increase**、C-cell-depth/C-regular は enclosure refinement による **bound-quality improvement candidate** として別集計する。ただし後二者も runtime/cell resource を消費するため cost は別途記録する。
A4/extended pilot の飽和はこの比較を選んだ設計動機に限り引用し、(c) の成功を予告しない。

# 6. Candidate (d) — finite RHO0 set
RHO0 は次の有限集合だけを比較する:
`{1/16, 3/32, 1/8, 5/32, 1/4}`。
baseline は `1/8`。各値は独立 candidate ID とし、他の SPEC V2 値は変更しない。
continuous search、補間による best RHO0、結果確認後の追加値、best-only reporting を禁止する。
全5値を同一 frozen sets C1-C5 と同一 recorded quantities で報告する。

# 7. Candidate (e) — NOT READY
現時点で near-pole analytic handoff に必要な sound analytic bound を、analytic region・numeric region・overlap・boundary double evaluation・handoff claim を含め監査可能な形で提示できていない。
したがって candidate (e) は **NOT READY** と確定し、v2 candidate comparison では実行しない。
completeness のためだけの実装・実行は禁止する。将来 sound bound が提示される場合は新 version で事前監査・freezeする。

# 8. Frozen point/box sets C1-C5
C1: 770 full 192 points。
C2: independent H 9 points（2 A + 7 N）。A/N 別集計し J-L, SumUpper-J を記録。
C3: B44 全44点。§2 の P0-A pin を参照し、Phase 0 の sign diagnostic を再解釈しない。
C4: P003 correct target: `r={.010,.014,.018,.022,.030,.060,.100}`, `t=1/64`, `lambda=251/400`。7点、G4。point behavior only。
C5: source `full_terminal_map.tsv`, SHA-256 `0584110495c9d3b98a96d88e3d9fbe717bde326f2b76dcc465db784ad3bd26f8`。
C5 selection は v1 から不変:
1. C1各点 → containing 7,7,0 depth-12 box。
2. C4各点 → containing terminal 0,0,3 box。
3. membership は `[lo,hi)`、global upper endpoint のみ `[lo,global_hi]`。
4. target ごと exactly-one assert。0 または複数なら C5 selection INVALID、除外継続禁止。
5. 選択 box bounds を全記録。box-center J は reference only、box proof ではない。

# 9. Recorded quantities — v2
(c)(d)(e) に対する必須列:
candidate ID, candidate status, code/config identity, initial-box index, exact r/t/lambda, C5 box bounds, accepted/unresolved, cut/regular cells, L, B_cut, independent J, C5 center-J flag, upper sum, enclosure width, J-L, SumUpper-J, cell count, max cell depth, max box depth, runtime/CPU, resource settings, failure reason, missing reason。
(e) は NOT READY のため execution rows を作らず、status/reason を comparison summary に記録する。

# 10. Comparison order
1. Soundness
2. Identity/reproducibility
3. Width
4. Certification utility
5. Cost
6. Independent checking

Soundness failureは reject。accepted count で復活させない。
N width は J-L / upper-J。B は Phase 0 sign diagnostic と区別する。
Certification utility は C5 のみ。C1-C4 は diagnostic。
resource increase と bound-quality improvement を別欄で比較し、単一 scalar winner score は作らない。

# 11. Guards and isolation
v1 の G1-G7、stop conditions、evidence boundary をそのまま適用する。
比較 harness は DIAGNOSTIC only、formal producer/checker から import せず、formal RUN_DIR 外に置く。
candidate implementation と F-list correction を同一 commit に混ぜない。
target membership/pin mismatch/consistency failure/ambiguous candidate/post-hoc threshold があれば停止し、同 freeze version の fix-run として続行しない。

# 12. Fixed conclusions entering v2
1. D-P2 = NOT_CERTIFIED。
2. Phase 0 B44 = P0-A, 44/44 conclusive POSITIVE; DIAGNOSTIC / NOT_EVIDENCE。
3. A4 candidate (a) = NOT READY at k<=8。
4. Extended candidate (a) = NOT READY at fixed partition, k<=64。
5. fixed-partition sigma-split count は k=8/16/32/64 で 120/121/122/122; descriptive saturation only。
6. candidate (a) fixed-partition route = CLOSED。(a)+(b) も current comparison から除外。
7. (a) の唯一の再提案経路は、(c) 比較後の `(a)+(c)` を新 version 項目として明示する場合。
8. candidate (e) = NOT READY; v2 では実行禁止。
9. candidate comparison は v2 FREEZE 前 BLOCKED。
# 13. Provenance of filled values
§5 の (c) 構成、§6 の RHO0 有限集合、§7 の (e) NOT READY 分類は、**Phase 0・A4・extended pilot の結果を確認した後に決定した値/分類**である。
特に extended pilot の 120/121/122/122 飽和は (c) を優先して比較する設計動機であり、事前知識または formal evidence ではない。

# 14. v2 freeze items
FREEZE 対象:
1. §2 Phase 0 closure pins。
2. §3 candidate (a)/(a)+(b) closure pins、verdict、唯一の復活条項。
3. §5 C0 と C-count/C-cell-depth/C-box-depth/C-regular の厳密値・one-change attribution。
4. §6 RHO0 finite set 全5値。
5. §7 candidate (e) NOT READY / no execution。
6. §8 C1-C5 と deterministic membership rule。
7. §9 mandatory columns。
8. §10 comparison order。
9. §11 guards/isolation。
10. §12 fixed conclusions。
11. §13 provenance。

# 15. Execution order
1. この v2 draft を単独 commit し、commit/file SHA/blob/worktree を報告する。
2. chat が **全文監査**する。
3. 修正があれば新 commit として再監査する。
4. chat が **v2 FREEZE countersign** を明示する。
5. FREEZE 後にのみ §20 isolation に従う comparison harness の着工を許す。
6. harness 完成後、source/config/pins/expected execution を別途 chat 監査する。
7. harness audit/countersign 前に candidate comparison を点火しない。
8. 点火後の結果は DIAGNOSTIC / NOT_EVIDENCE として提出し、human adoption decision を待つ。

# 16. Adoption boundary
比較結果から採用候補を決めても、それ自体は SPEC V3 certification ではない。
採用後に SPEC V3 text を別途作成・監査・freezeし、独立 producer/checker、F-list corrections、fresh pins、fresh formal run を必要とする。
旧 smoke、Phase 0、A4、extended pilot、candidate comparison を formal evidence として再利用しない。

# 17. Status
**v2 — DRAFT FOR CHAT AUDIT / NOT_FROZEN**
candidate comparison: BLOCKED。
comparison harness construction: BLOCKED until v2 FREEZE countersign。
次の入力はこの draft の commit identity と全文監査である。
