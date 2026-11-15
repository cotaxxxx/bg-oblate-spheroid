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

## F7（推奨・保留）

c1b_receipt_extract.json のスキーマ別件数照合は未実装。封印台帳をFREEZE前に読まない契約を優先した。accepted 159、clamped 35、unclamped 124は両系統のハッシュ連鎖台帳で照合する。抽出表の「空でない辞書」検査を件数検査済みと主張しない。FREEZE前に原典のschemaを監査し、別途実装してよい。

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
