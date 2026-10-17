# D-OB P2 / D-AN-1 — L1 dual-track paper comparison baseline

2026-10-17 JST

**Status: BASELINE FOR 2026-10-24 COMPARISON / PAPER-ONLY / NO COMPUTATION AUTHORIZED**

## 1. Purpose

Judge の dual-track 裁定に基づき、Route K (`K_H / K_pair`) と Route B (`B_int`) を同じ評価軸で比較するための baseline を固定する。

この文書は route 選定そのものではない。

## 2. Shared target

両 route の L1 target は同一：

\[
S_{L1}=\Sigma\cap\{3/10^8\le\delta\le15/64\},\qquad \delta=1-r^2.
\]

L1 positivity は未証明。

## 3. Current comparison

| 評価軸 | Route K: `K_H / K_pair` | Route B: `B_int` |
|---|---|---|
| representation | P1 §8.2 / L2 の canonical representation | generic P1 directional kernel から exact derivation 済み candidate |
| current audit status | VALID | AUDITED CANDIDATE |
| denominator safety | compact + FTC sweep 上で exact positive bounds | 同じ compact 上で safe。ただし `sigma^2`, `eta` dependency 保持が必要 |
| symmetry | `K_H` は `s`-even | raw density の `s`-evenness は仮定不可。explicit branches が必要 |
| remaining sign issue | centered derivative / FTC integral の residue が未評価 | nonnegative term − nonnegative term の signed residue が未評価 |
| boundary relation | inherited continuous extension | `delta=0, sigma>0` で boundary kernel。contact は combined-density limit |
| extra dependency risk | canonical source dependencies を維持 | `eta`・`sigma`・`gamma` joint dependency を新規設計要件として保持 |
| naive interval risk | 未判定 | `eta` の独立 rectangularization は cancellation loss の危険大 |
| paper closure | plausible starting route; 未証明 | plausible candidate; geometry dependency の追加処理が必要 |

## 4. Mandatory 2026-10-24 report fields

各 route について同じ四項目を提出する。

1. remaining exact residues
2. interval computation needed? `NO / LIKELY / YES / UNDETERMINED`
3. newly required inherited conditions
4. Route B: joint dependency preservation (`eta`, `sigma`, `gamma`)

## 5. Selection rule

1. interval-free route を優先。
2. 両方 interval-required なら remaining residue が少ない方。
3. 新規 inherited condition が少ない方。
4. tie の場合 Route K。

## 6. Route B design constraint

Route B では

\[
\eta=1+\frac{\delta}{\sigma^2},\qquad
\gamma=\frac{\lambda\sigma\eta}{2wk}
\]

という joint structure を保持する。

`eta`, `sigma`, `gamma` を独立 boxes に置換してはならない。もし将来 interval architecture が必要なら、この dependency を保存する lift / constraint system を先に predeclare する。

## 7. Governance

2026-10-24 までは paper-only comparison。

- no interval run
- no certification run
- no result-dependent partition
- no V1 route instruction before Judge selection
- no D5 access / mutation
