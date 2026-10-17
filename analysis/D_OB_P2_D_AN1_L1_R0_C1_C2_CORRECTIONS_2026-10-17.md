# D-OB P2 / D-AN-1 — L1-R0 C1/C2 correction record

2026-10-17 JST

対象：`L1_R0_COMPACT_AND_KERNEL_DOMAIN_LEDGER_V0.md`

この addendum は Astra exact re-audit と chat independent audit が一致して採用した二つの文言修正を固定する。

## C1 — boundary specialization / contact point

旧記載の単純な「`delta=0` で `eta=1`」は適用点を限定する。

正しい記載：

> `delta=0` かつ `sigma>0` なら
> \[
> \eta=1,
> \]
> したがって `B_int=B` が exact に成立する。
>
> contact point `delta=sigma=0` では
> \[
> \eta=1+\frac{\delta}{\sigma^2}
> \]
> 自体が未定義なので、その点で直接 `eta=1` と代入したとは書かない。combined density の極限で扱い、integral-value extension は継承 Lemma V による。任意の interior path で `eta→1` と主張しない。

## C2 — `eta=1` の意味

旧記載「`eta=1` の場合だけ V3 になる」は必要十分条件と読めるため修正する。

`K=k^2`, `C=2A-gamma c` とすると

\[
\mathcal P_{\rm int}-\mathcal P_{V3}
=\frac{\gamma(\eta-1)}{KA^2}
\left[A(1-n)-Cn\left(1-\frac{4K^2}{\eta}\right)\right].
\]

したがって `eta!=1` でも bracket が0なら pointwise numerical equality は起こり得る。

正しい記載：

> `eta=1` は V3 の式族を恒等的に回復する特殊化である。一般の interior `eta>1` では追加 dependency を省けず、V3 certificate を無変更流用できない。

この修正は `BOUNDARY-KERNEL SCOPE STOP` を変更しない。
