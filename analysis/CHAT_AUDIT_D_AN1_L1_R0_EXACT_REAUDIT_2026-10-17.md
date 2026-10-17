# chat independent audit — D-OB P2 / D-AN-1 / L1-R0 exact re-audit

2026-10-17 JST

**Verdict: PASS.**

対象：`L1_R0_EXACT_REAUDIT_20261017.md`

Astra re-audit report SHA-256:

`f4ea0b2bf81d0ecffd41891e65a4e0db64da4191134dc819d9c0e4992b014030`

対象 L1-R0 V0 SHA-256:

`da36508507015ed968c4a386fdcc2becb6523408fea078faba16e840fda868e6`

## 1. Source / provenance

- Judge 指定8 pin：8/8 MATCH。
- 補助 P1 / L2 / FTQ signed reduction V0 の SHA も一致。
- FTQ V0 の readback で末尾 LF 1 byte が省略されるという Astra 注記は妥当。

## 2. Boundary-kernel scope

`BOUNDARY-KERNEL SCOPE STOP` を確認。

境界式

\[
h=\lambda\sigma^2/2
\]

は `r=1` の boundary geometry に依存し、interior では

\[
h=\frac{\lambda}{2}(\sigma^2+\delta),\qquad \delta=1-r^2>0
\]

となる。したがって boundary `WB` kernel を L1 interior へ無変更適用できない。

これは表示の適用域に対する STOP であり、`H>0` の反例ではない。

## 3. Route K

`K_H / K_pair` route は canonical representation として有効。

FTC、axis extension、half-turn pairing、arcsine normalization、compact / FTC sweep 上の denominator bounds を確認。

## 4. Route B / exact algebra

Astra re-audit §5 の t-integrand

\[
\frac{4w\gamma^2}{\sigma k^3A^2}
\left[A(k^2-V)-(2A-\gamma c)V(1-2k^2/\eta)^2\right]
\]

へ

\[
\gamma^2=\frac{\lambda^2\sigma^2\eta^2}{4w^2k^2}
\]

を代入すると、

\[
\frac{\lambda^2\sigma}{wk^5A^2}B_{\rm int}
\]

へ一致することを独立確認。

`B_int` は **AUDITED CANDIDATE** と評価する。

## 5. C1

boundary specialization は

\[
\delta=0,\qquad \sigma>0
\]

で `eta=1`, `B_int=B` と述べるのが正しい。

contact point `delta=sigma=0` では `eta=1+delta/sigma^2` は未定義であり、combined density の極限と継承 Lemma V で扱う。

## 6. C2

差分恒等式

\[
\mathcal P_{\rm int}-\mathcal P_{V3}
=\frac{\gamma(\eta-1)}{KA^2}
\left[A(1-n)-Cn(1-4K^2/\eta)\right]
\]

を独立 symbolic check で確認。

したがって正しい記載は、

> `eta=1` で V3 の式族を恒等的に回復する。一般の interior `eta>1` では追加依存を省けず、V3 certificate を無変更流用できない。

である。

`eta=1` を点別一致の必要十分条件とはしない。

## 7. eta range / joint dependency

\[
\frac{2}{1+r}\le\eta\le\frac{2}{1-r}\le\frac4{\delta_0}
\]

を exact に確認。

この粗い上界は、Route B で `eta` を独立変数として naive に区間化すると cancellation を失う危険を示す。

Route B を進める場合、`eta`・`sigma`・`gamma` の joint dependency を保持することを設計要件とすべきである。

## 8. Recommendation

**DUAL-TRACK PAPER COMPARISON** を推奨する。

- Route K: canonical / VALID
- Route B: AUDITED CANDIDATE

L1 全域 positivity は未証明。L1-R0 は PARTIAL のまま。

interval / certification computation は本監査の範囲外であり、承認もしない。
