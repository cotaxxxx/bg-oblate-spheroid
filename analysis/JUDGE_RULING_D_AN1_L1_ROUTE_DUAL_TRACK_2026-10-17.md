# Judge ruling — D-OB P2 / D-AN-1 / L1 route dual-track

2026-10-17 JST

**発行：Judge**

## 1. 裁定

L1 は、以下の二つの paper route を並行比較する。

- Route K: canonical `K_H / K_pair` route
- Route B: audited-candidate `B_int` route

現段階ではどちらか一方へ固定しない。

**L1-R0 は PARTIAL のまま。L1 は RESTART / paper-only。T1 は NOT CLOSED。D-P2 は NOT_CERTIFIED。**

interval / certification run は承認しない。V1 指示書も route 選定前には起草しない。

## 2. 比較期限

**比較報告提出期限：2026-10-24**

両 route は同じ四項目で比較する。

1. まだ残っている項
2. 区間計算が必要か
3. 新しく必要になる継承条件
4. Route B のみ：`eta`・`sigma`・`gamma` の joint dependency を切り離さず扱えているか

## 3. 選定基準

優先順位は次の通り。

1. 区間計算が不要な route を優先する。
2. 両方とも区間計算が必要なら、残る項が少ない route を優先する。
3. さらに、新しい継承条件を増やさない route を優先する。
4. それでも決まらない場合は、既に canonical representation として VALID が確認されている Route K (`K_H`) を採る。

## 4. Route B 固有要件

`B_int` を進める場合、

\[
\eta=1+\frac{\delta}{\sigma^2}
\]

を独立 worst-case 変数として切り離さないこと。

`eta`・`sigma`・`gamma` の joint dependency を保持することを設計要件とする。特に、naive rectangularization による cancellation loss を避ける。

## 5. C1 / C2

Astra exact re-audit と chat 独立監査で採用された文言修正を route comparison の前提にする。

- C1: boundary recovery は `delta=0, sigma>0` で述べる。contact point `delta=sigma=0` では `eta` を直接定義せず combined density の極限で扱う。
- C2: `eta=1` は V3 の式族を恒等的に回復する特殊化である。点別一致の必要十分条件とは記さない。

## 6. 監査の区別

- `L1_R0_EXACT_REAUDIT_20261017.md` は Astra 側の exact 再検算であり、第三者独立監査の代替ではない。
- 別セッションの chat 独立監査は PASS と報告され、Astra re-audit の主要 algebra、C1/C2、dual-track 推奨を独立確認している。
- 本裁定以前に Judge 自身が GitHub で確認済みなのは、L1 restart brief とその上流原典との整合である。

## 7. 禁止事項

- interval / certification run
- numerical positivity sampling
- result-dependent subdivision / threshold tuning
- V3 boundary certificate の interior への無変更流用
- V1 route 指示書の先行起草
- T1 CLOSED / D-P2 CERTIFIED の自己宣言
- D5 access / mutation

## 8. 次工程

2026-10-24 の dual-track comparison report 提出後、Judge が Route K / Route B / HOLD・REDESIGN のいずれかを裁定する。
