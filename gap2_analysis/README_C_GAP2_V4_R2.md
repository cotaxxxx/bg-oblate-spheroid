# C空白② v4-r2｜F1〜F6 実装修正提出

**状態：IMPLEMENTATION CANDIDATE / NOT FROZEN / EXECUTION PROHIBITED / NOT_EVIDENCE。**
原点は凍結run4 26d81e1049340d44ef7f08ae8e17d0692983395b。現実装は45617d0を直親とする追加単一コミットで提出する。

監査：CHAT_AUDIT_C_GAP2_IMPL_45617D0_20261115.md（chat、2026-11-15）。
kernel・gatingの数学的中身は既監査PASS。g_box、gt_box、精度160/192、次数50、panel8192、chart、U_cum<0は変更しない。

## F1：独立系統の比較器

追加：gap2_analysis/lineage_compare.py
producer/checkerのmanifest・台帳SHA256とrun4方式のhash chainを検査。124親ごとに双方のt_e一致、双方それぞれのACCEPT葉の厳密分数による被覆、木の完全性、ABORT不在、合格葉のseed/cumulative上界負を必須にする。最悪上界は親・系統別の表にする。片側だけのPASSはFAIL。

## F2：実行時の同一性の記録

追加：gap2_analysis/runtime_identity.py
実行前と後にcommit、直親、working tree clean、変更・追加ファイルのgit blob/sha256、run4の25blob、読み込まれたrepo内import closure、Python・python-flint・mpmath・OS環境を記録。前後の不一致はNOT_EVIDENCEとし、合格に使わない。

## F3：回帰の静的・数値的対照

- endpoint_driver.py の静的preflightは一般の分割公式からt_e=31/32のrun4の16箱との完全一致をassert。993/1024でN=16、63/64でN=8、1023/1024でN=1もassert。
- run4_regression.py は既存run4台帳の先頭・中間・末尾を比較する。これ自体は旧コードと同じ枝なので、次の合成対照が必須。
- 追加：gap2_analysis/synthetic_preflight.py。封印を使わない合成のλ区間 [1/2,1/2+1/1600] と可変t_e=993/1024・63/64で双方の門を実行し、seedとGt箱の区間交差、分割・判定一致を検査する。NOT_EVIDENCE。**まだ数値実行していない。**

## F4〜F6

- 出力台帳をpersistence.Ledgerによるレコード単位のSHA256連鎖追記に変更。異常時はABORT/NOT_EVIDENCEを出力。自動再開は行わない。
- 資源の検査は全履歴の反復再直列化を廃止し、ファイルサイズと加算カウンタで実行。CPU48 core-hours、RAM32GiB、出力10GiB、セル上限1,048,576、ノード数124×15を維持。
- λ二分深さ0〜3はC1bの親が既に持っているrefinement_depthとは別。各封印親のλ区間を深さ0として再起算。子の最小幅はその親幅の1/8であり、親のt_eを継承する。右側子優先。

## F7（非停止の補助記録、実物はFREEZE後に確認）

c1b_receipt_extract.json はSHA固定済みだが、件数キーの意味は未確認。受理159・右clamp35・未clamp124は両系統のハッシュ連鎖台帳から厳密に検証し、抽出表から見つかる候補の経路・値・一致状態は補助情報として記録する。候補ゼロ・不一致・未知schemaを理由にL0(c)を停止しない。抽出表の意味は本走後にchatが検収する。

## 実施済み・未実施

実施：静的コンパイル、producer/checker静的preflight、ソース変更範囲のAST比較（差分チェック）。
未実施：数値回帰、合成区画での数値対照、封印台帳L0(c)(d)、本走、Judge FREEZE。

### chat差分監査後のpreflight

run4回帰（公開済みrun4台帳のみ）：
python -m gap2_analysis.run4_regression --role producer --run4-ledger <RUN4_PRODUCER>
python -m gap2_analysis.run4_regression --role checker --run4-ledger <RUN4_CHECKER>

合成対照：
python -m gap2_analysis.synthetic_preflight --role producer --output <PRODUCER_JSON>
python -m gap2_analysis.synthetic_preflight --role checker --output <CHECKER_JSON>
python -m gap2_analysis.synthetic_preflight --compare --producer <PRODUCER_JSON> --checker <CHECKER_JSON>

Judge FREEZE後、producer/checker本走が共に完了した後の比較：
python -m gap2_analysis.lineage_compare --producer-run <RUN_PRODUCER> --checker-run <RUN_CHECKER> --output <RESULT_JSON>

**この文書、実装commit、静的preflightはFREEZE・本走の許可ではない。空白② OPEN / D-OB global OPEN。**


## G1〜G5（chat監査 CHAT_AUDIT_C_GAP2_IMPL_FF07E09_20261115.md への対応）

- G1：gating の endpoint_seed_t は有理数文字列なので、駆動部で Fraction に戻して親の t_e と比較。トップレベル t_e も照合し、子の seed 継承を強制する。
- G2：full_run（Judge FREEZE後の封印入力読込）と run_parent_set（本物の kernel/gating・Ledger・manifest・runtime_identity による共通計算経路）を分離。end_to_end_preflight.py が隣接する合成親2本を流し、producer・checker・compare まで実動作する。別の合成限定フックで、最初の本物の門を評価後に ABORT / segment_end / ABORT_NOT_EVIDENCE を確認する。
- G3：系統共通のファイル pin と、系統別に実際に import された閉包を別辞書で記録。後者は自分の系統内で前後照合。直親 ff07e09、祖父 45617d0、run4 原親 26d81e1 の関係を固定。
- G4：比較器が N・Δt・各 t 箱・Gt の upper_j と contribution を厳密分数で再計算し、seed_upper + Δt Σ max(0,U_j) <= recorded_cumulative_upper < 0 を独立に検査。最後の corner dispatch も照合。
- G5：ハッシュ連鎖そのものの検証を維持し、header・segment_end直後の lscpu_raw_trace のみ数学の台帳から除外。それ以外の未知レコードはFAIL。
- F7：receipt_extract.jsonのaccepted・right_clamped候補（経路、値、台帳との一致・不一致・未発見）をmanifestのreceipt_countsに記録するだけとした。推測したキー名の不一致では停止せず、chatの本走後検収へ渡す。台帳の159/35/124検証は従来どおり厳格。

### G2：chat差分監査後にのみ実行するNOT_EVIDENCE preflight

python -m gap2_analysis.end_to_end_preflight --role producer --run-dir <FRESH_SYNTH_PRODUCER>
python -m gap2_analysis.end_to_end_preflight --role checker --run-dir <FRESH_SYNTH_CHECKER>
python -m gap2_analysis.end_to_end_preflight --compare --producer-run <FRESH_SYNTH_PRODUCER> --checker-run <FRESH_SYNTH_CHECKER> --output <NEW_JSON>
python -m gap2_analysis.end_to_end_preflight --role producer --run-dir <FRESH_SYNTH_ABORT> --force-abort

合成入力は、λ ∈ [1/2, 1/2+1/1600] と隣接区画、t_e = 993/1024 と 63/64 だけ。実C1b台帳と隔離。ABORTフックは合成モードに限り、最初の真の門を評価してからABORTにする。数学的な反例とは解釈しない。

**状態：未監査の修正コード / NOT FROZEN / EXECUTION PROHIBITED / NOT_EVIDENCE。** 数値回帰・合成門の本実行・L0(c)・空白②本走はまだ未実施。


## 最終実装 H1・F7（chat 3bd5113 監査PASS後）

H1：SEALEDのcross-lineage比較では両manifestの入力pinが互いに等しいだけでなく、sealed_contract.PINNEDに記された元の4ファイルの完全なSHA256と完全一致することを検査する。さらに、外から引数で渡すJudge FREEZE裁定のSHA256（厳密な64桁小文字hex）に両manifestとheader記録の裁定SHAが一致することを必須とする。Judge SHA不在のSEALED比較を許さない。合成NOT_EVIDENCEモードは裁定SHAを要求せず、模擬固定値しか認めない。

正式比較の呼び出しは次のとおり。

    python -m gap2_analysis.lineage_compare --producer-run <RUN_PRODUCER> --checker-run <RUN_CHECKER> --judge-ruling-sha256 <EXACT_64_HEX_SHA_OF_JUDGE_FREEZE_RULING> --output <NEW_RESULT_JSON>

F7：sealed_contract.verify_receipt_extract_countsはaccepted/right-clampedらしいキーを候補としてのみ抽出する。候補ごとのpath・observed_value・matches_ledgerと、NOT_FOUND/ALL_MATCH/NONE_MATCH/MIXED_MATCHをmanifest.receipt_countsに格納。未知schema・候補不在・不一致は停止理由にならない。真正なaccepted 159、clamped 35、unclamped 124はC1bの独立ハッシュ連鎖台帳から厳格検査し、抽出表の意味付けは本走後chatが検収する。

runtime_identityは途中のcommitを固定しない。凍結run4の26d81e1がHEADの祖先であることをgit merge-base --is-ancestorで検査し、run4から変更された17ファイル（当初13＋監査追加4）と宣言集合の完全一致を要求する。HEAD SHAと直親は実行記録に残す。最終HEAD SHAはJudge FREEZEで固定する。

**今回の新実装の静的模擬検査だけPASS。最終差分のchat監査待ち。数値preflightはまだ禁止、L0(c)・本走も未実施。**


## 7b337a0後の最終訂正（chat差分監査 PASS待ち）

監査記録 CHAT_AUDIT_C_GAP2_IMPL_7B337A0_20261115.md に従い、F7の未確認スキーマを非停止の補助記録に変更。receipt_count候補は観測値・経路・台帳との比較状態としてmanifestに残す。L0(c)の厳格条件はC1b封印4 SHA、producer/checker/replayの記録、受理159・右clamp35・未clamp124の台帳検査。receipt候補値の不一致のみで計算を止めない。H1のJudge SHAと封印4 SHA固定は維持する。

今回の修正は7b337a0を直親とする単一commitにする。凍結run4 26d81e1の祖先性、変更ファイル17件の完全一致、HEAD SHAによる運用pinを使う。

新コミットのchat差分監査PASS後のみ数値preflight一式を実行。すべてNOT_EVIDENCE。Judge FREEZE前にはL0(c)(d)と空白②本走をしない。
