# FT_q V3 — 原本所在・欠落台帳（2026-10-31）

**STATUS: INCOMPLETE / PROVENANCE GAP / NOT A CERTIFICATE / NOT RECONSTRUCTED**

本台帳は FT_q V3 の証明書一式ではない。2026-10-31 の Judge→chat→Dig 依頼に従い、確認できた既存採用記録と、登録に必要だが原本未取得の部品を分離する。原本の再構成、擬似証明書生成、未検証の SHA-256 付与は行わない。chat／Muse の監査 PASS を本台帳に付与しない。

## 1. 既存の採用記録（証明書本体とは区別）

- 既存資料：`analysis/D_OB_P2_D_AN1_L3_BODY_DRAFT_V0_2.md`、`bg-oblate-spheroid` branch `design/d-ob-p2`。既知の採用記録 pin：`1b65c7c`。
- 採用済み表示用下界：`M = 295346256371/10^12`。これは whole-face `H` の境界下界であり、内部 `H(p) >= M` の主張ではない。
- L3 V0.2 §1 の readback 記録：`m_V3=a/b` の分子90,766桁・分母90,767桁、分母正、gcd=1、`10^12 a >= 295346256371 b`、`10^12 a < 295346256372 b`。同節は「4096 certificates の再生成ではない」と明記する。
- 別実装 chat の4096枝・正2230／零0／負1866・argmin (0,0) の報告は、JSON・スクリプト・最終SHAが未受領であると L3 V0.2 §1 に明記される。ここでは監査済みartifactとして登録しない。
- 依頼書記載の集計：seed 3913、fallback 183、CHECK_ERROR 0、RESOURCE_LIMIT 0。**原本未取得のため本台帳で再検証していない**。

## 2. 要求された原本と欠落状況

| # | 必須部品 | 状態 | 検証・SHA-256 |
|---|---|---|---|
| 1a | 凍結仕様：被積分量 `P` の完全定義 | **MISSING ORIGINAL** | 未取得／未計算 |
| 1b | 凍結仕様：2048 folded boxes、`τ4×μ16×s2×λ4×t4`、active order `(t,γ,k,n)` | **MISSING ORIGINAL** | 未取得／未計算 |
| 1c | 凍結仕様：joint constraints `Q₁…Q₈` の厳密な式 | **MISSING ORIGINAL** | 未取得／未計算 |
| 1d | 凍結仕様：multiplier／residual 次数、`k²A²≥4/25`、primal／dual の厳密な受理等式 | **MISSING ORIGINAL** | 未取得／未計算 |
| 2a | FT_q V3 producer ソース | **MISSING ORIGINAL** | 未取得／未計算 |
| 2b | FT_q V3 checker ソース | **MISSING ORIGINAL** | 未取得／未計算 |
| 2c | producer／checker の実行環境、Python・ライブラリ版の固定記録 | **MISSING ORIGINAL** | 未取得／未計算 |
| 3a | 4096枝の全証明書出力、manifest、完全な集計 | **MISSING ORIGINAL** | 未取得／未計算 |
| 3b | `m_V3=a/b` の exact 原本（例：`sources/M0_LIBRARY_CURRENT.txt`） | **MISSING ORIGINAL** | 未取得／未計算 |
| 3c | chat 独立再計算のJSON／スクリプト／SHA | **NOT RECEIVED** | 未取得／未計算 |
| 4 | 1〜3の原本SHA-256一覧 | **BLOCKED BY MISSING ORIGINALS** | SHAを捏造しない |

**重要：** 2048 folded boxes の因子 `4×16×2×4×4=2048` と、4096枝は別のカウントである。対応規則の原本がないため、両者を推定で対応づけない。仕様（1）の全文がない状態では、Muse に「凍結仕様」として渡さない。

## 3. 探索範囲・限界

- GitHub の既知 `bg-oblate-spheroid` 設計ブランチで L3 V0.2 を取得。FT_q V3 の producer／checker／証明書原本はこの作業で確認できなかった。
- 研究用PC `daybreak-works` の `/home/daybreak` 配下をファイル名で探索。FT_q V3 の完全な原本一式は確認できなかった。名称を変えた保管物や他の保存先の不存在まで証明するものではない。
- `D_OB_P2_CERTIFICATION_SPEC_V3.md` 等の **D5 V3** 関連資料は FT_q V3 と別物。流用・改変・D5実行はしていない。
- GitHub の他のrepo・branchの全履歴を完全走査したとの主張はしない。Judge の「3 repo のどのbranchにも本体なし」という報告と整合するが、独立した全探索済み判定ではない。

## 4. 引継ぎとゲート

1. 原本を取得した場合のみ、原本byteを保存しSHA-256を計算して、仕様・ソース・証明書・環境の独立したmanifestを追加登録する。
2. checkerの実行と証明書の再現は、必要な原本・実行条件を固定してから別工程とする。本台帳はPASSを意味しない。
3. Museへ渡すのは、**原本で照合した凍結仕様（1）のみ**。現時点では原本未取得のため引渡し不可。
4. `FT_q V3` の数学的採用記録（条件付き）と、再現可能な証明書一式のGitHub保管完了は区別する。
