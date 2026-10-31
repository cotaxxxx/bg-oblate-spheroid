# D-OB P2 / D-AN-1 — L1 Route K／Route B 紙上比較報告 V0

2026-10-31 JST  
**提出：Dig（ChatGPT）／DRAFT FOR chat AUDIT／NOT AUDITED／PAPER-ONLY**  
**Judge 裁定：2026-10-17 `bd041c0bc904431eff66007f278174b30a68151d`／旧期限：2026-10-24（超過）**

## 0. 判定の範囲と原典

本稿は Judge 裁定 §2 の四項目と §3 の選定順序に従う**比較と非拘束推奨**であり、route の裁定、証明書、区間計算、positivity の証明ではない。

固定対象：`S_L1 = Σ ∩ {3/10^8 ≤ δ ≤ 15/64}`、`δ=1-r²`。比較のために領域・閾値を変更しない。L1-R0 は PARTIAL、L1 は RESTART / paper-only、T1 NOT CLOSED、D-P2 NOT_CERTIFIED のまま。

取得した一次資料（すべて `cotaxxxx/bg-oblate-spheroid`、commit `bd041c0` の `analysis/` 以下）：

- `L1_R0_COMPACT_AND_KERNEL_DOMAIN_LEDGER_V0.md`
- `L1_R0_EXACT_REAUDIT_20261017.md`
- `D_OB_P2_D_AN1_L1_DUAL_TRACK_COMPARISON_BASELINE_2026-10-17.md`
- `D_OB_P2_D_AN1_L1_R0_C1_C2_CORRECTIONS_2026-10-17.md`
- `JUDGE_RULING_D_AN1_L1_ROUTE_DUAL_TRACK_2026-10-17.md`
- 同commit内 `CHAT_AUDIT_D_AN1_L1_R0_EXACT_REAUDIT_2026-10-17.md`。本稿自体へのchat監査ではない。

原典の既存監査上、Route K の representation は **VALID**、Route B の exact algebra は **AUDITED CANDIDATE**。いずれも L1 の正値性は未証明。今回の作業では interval／certification run、numerical positivity sampling、D5へのアクセス・変更を行っていない。

## 1. 共通の安全性・障害

固定 compact：`λ∈[2/5,93/200]`、`τ∈[7/8,1]`、`r∈[7/8,√(1-3/10^8)]`。FTC swept points も内部正則域にあり、既存紙上 ledger は `D,h≥3/(5·10^8)`、`k²≥4/25`、`A∈[1,2]`、`wk⁵A²≥64/15625` を与える。これらは分母の正値性であり、signed integral の正値性を示さない。

**境界核適用域 STOP**：境界 `h=λσ²/2` は `r=1` の式であり、内部では `h=λ(σ²+δ)/2`。従って V3 境界証明書を L1 内部に無変更適用できない。

C1：`δ=0,σ>0` でのみ `η=1` と境界特殊化を述べる。`δ=σ=0` の contact では `η=1+δ/σ²` は未定義であり、combined-density の極限と Lemma V の継承が必要。

C2：`η=1` は V3 式族の恒等的回復であって、点別一致の必要十分条件ではない。

## 2. Judge §2 の四項目比較

| 必須評価軸 | Route K — `K_H / K_pair` | Route B — `B_int` |
|---|---|---|
| (1) 未処理の厳密な項 | `K_H = 1/2 ∫_{-1}^1 ∂_{ρρ}F_E(vρ,z;μ,φ)dv` の**符号不定な中心二階微分／FTC平均残余**。軸 `ρ=0` はFTC延長で定義できるが、正の一様下界は未構成。`K_pair=2K_H` と `s` 偶性は積分の表示変換であり、符号の解消ではない。 | `B_int=Aη²(k²-V)-(2A-γc)V(η-2k²)²` の**非負項−非負項の符号付き残余**。正のweightだけでは積分正値性を導けない。raw density の `s` 偶性は使えず、両枝の明示和が必要。contact と境界との接続にも注意。 |
| (2) 区間計算の要否 | **UNDETERMINED**。canonical表示・分母下界は紙上で得られているが、残余の解析的不等式が未構成。現時点で「NO」とも「YES」とも断定不可。 | **UNDETERMINED（実務上の負担はKより大きい可能性）**。signed残余を依存関係ごと処理する解析的不等式が未構成。区間計算必須との証明もない。 |
| (3) 新規に必要な継承条件 | 固定 P1 §8.2、L2 の canonical表示、内部正則性・FTC、軸延長、compact分母条件を使用。**新しい外部継承条件の追加は現時点で特定されていない**が、正値性の新しい補題は必要。 | generic P1 directional kernel、C1/C2、境界への Lemma V 接続を使用。**`η,σ,γ` のjoint dependency保存**と明示的両枝を新たな方式条件として課す。別個の新規外部補題が必要かは未決。 |
| (4) Route B joint dependency | 対象外。K側でも変数依存を無根拠に切断してよい意味ではない。 | **紙上の式では保持、正値性を閉じる方式では未実証**。`η=1+δ/σ²`、`γ=λση/(2wk)`、`δ=1-r²`、`σ=|ξ-rQ|` を同時に保持する。独立 rectangular box 化は禁止。`η` の粗い上界だけでは cancellation を失い得る。 |

### 2.1 Route K の未処理部分を正確に限定する

既存の等式は
`H=(1/(4πλ))∫_{-1}^1∫_0^{2π}K_H dφ dμ`、
`K_H=[∂_ρF_E(ρ,b)-∂_ρF_E(-ρ,b)]/(2ρ)`（`ρ>0`）。
FTC により上表の `v` 平均を得る。軸は `∂_{ρρ}F_E(0,z)` へ連続延長する。`K_H` は `b→-b` 偶であり、半周 pairing は有効。しかし `∂_{ρρ}F_E` の符号とFTC平均の下界はこの等式からは従わない。sweep 中の基点は `S_AN` の radial lower bound を外れ得るので、`S_AN` 上だけの未証明正値性を流用しない。

### 2.2 Route B の未処理部分を正確に限定する

`W=σ/(wk⁵A²)>0`、`c=1-t²`、`V=ν_y²` とすると、原典で導出された `F_{E,yy}=λ²∫_0^1 W B_int dt` を用いる。`k²-V≥0` と `2A-γc>0` だが、二項の差の符号は決まらない。`η` を独立変数にすれば大きな範囲（原典：`2/(1+r)≤η≤2/(1-r)≤4/δ₀`）を持ち、負項と正項の相関が壊れる可能性がある。これは危険の特定であり、区間計算失敗の実測ではない。

## 3. Judge §3 の選定基準を順番どおり適用

1. **区間不要を優先**：どちらも区間不要と証明されていない。判定は両者 **UNDETERMINED**。従ってこの基準だけで決着しない。
2. **両方が区間必要なら残余の少ない方**：前提「両方必要」が未確定なので、この条件分岐を適用して勝者を断定しない。定性的にはKはcanonicalなFTC符号残余、Bはsigned残余に加えjoint dependencyと両枝の扱いが残るが、**項数の厳密比較は未確定**。
3. **新規継承条件の少なさ**：Kは既存P1/L2中心。Bはjoint dependency保存という新しい方式義務を持つ。Kを支持する。ただし新しい外部定理の個数が確定したわけではない。
4. **同点ならcanonical Route K**：上位基準で優劣が確定しない場合のJudge明示タイブレークを適用する。

**非拘束推奨：Route K（`K_H / K_pair`）を次段階の第一候補とする。** Route B は AUDITED CANDIDATE として保持し、捨てない。これは証明の成功可能性を保証せず、Judgeによる正式選定でもない。もしJudgeが区間要否や残余の未決定性を重く見るなら **HOLD / REDESIGN** も許された裁定である。

## 4. 監査・次工程

- 本報告を **chat が監査**し、その後 **Muse の独立監査**へ回す。Dig自身の報告に監査PASSを付けない。
- 新しい提出期限は **Judge未指定**。運用提案として **2026-11-07** を提示するが、Judge裁定までは確定期限としない。
- Judgeがrouteを選ぶまで **V1指示書は起草しない**。
- interval／certification run、数値サンプリング、結果依存分割・閾値調整、境界V3証明書の内部無変更流用、D5アクセス・変更を行わない。
- **L1-R0 PARTIAL／T1 NOT CLOSED／D-P2 NOT_CERTIFIED** を維持する。
