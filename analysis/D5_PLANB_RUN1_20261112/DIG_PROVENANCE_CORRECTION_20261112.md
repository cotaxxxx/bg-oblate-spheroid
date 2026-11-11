# 証拠の出所訂正：PB-RUN-1 Muse監査受領記録

2026-11-12 / 証拠管理訂正（Digへの引渡し補助）

## 取り消し

コミット `1fae26479b2578ab7d4c53d5e142dff5d899a295` で登録された `CHAT_RECEIPT_MUSE_AUDIT_D5_PLANB_RUN_TOOL_20261112.md`（SHA-256 `850bbbdfd010a6738c84d14c82c26f86ad7f99c618f804164c9b6f7d04a012c5`）は、chatの発行済み原本ではない。代理作成された文書をchatの正式記録と誤表示していたため、現行証拠ブランチから取り消した。

この取消は履歴を改ざんするものではない。旧コミットはGit履歴上に残るが、**正式受領記録の根拠として引用・使用してはならない**。

## 未受領の真正原本

chat発行の真正原本 `CHAT_RECEIPT_MUSE_AUDIT_D5_PLANB_RUN_TOOL_20261112.md` は、ユーザー指定のSHA-256が `836a3f0c…` である。2026-11-12時点でファイル実体がないため、未受領のままとする。原本を受領した際はバイト列のSHA-256を照合し、代理記述や整形を行わず、正式な元ファイルとして別コミットに登録する。

同様にB7のchat検収原本 `CHAT_ACCEPTANCE_B7_V54_L0_T0_D4_20261112.md`（指定SHA `f6581db7…`）および `CHAT_BOX_CHECK_L0_T0_D4_20261112.log`（指定SHA `6bbc727d…`）も真正原本ファイルが届くまで作り直してはならない。

## 変更しない対象

Muse監査原本 `MUSE_AUDIT_D5_PLANB_RUN_TOOL_20261112.md`（SHA-256 `aef3b3b5e6846c14ebbb30f290c7170cc27603548db0f93b03cd983977f637db`）、Plan B凍結ソース、実行結果、B7旧V5.3凍結原本、GitHub main/STATE.mdには変更を加えない。
