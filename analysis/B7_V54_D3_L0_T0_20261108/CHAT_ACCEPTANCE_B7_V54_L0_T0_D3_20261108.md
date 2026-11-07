# chat 検収記録：B7 V5.4 — 外箱 `L0_T0_D3`

2026-11-08 / 検収: chat / 判定者: Judge（採用、2026-11-08）

## 結果

外箱 `L0_T0_D3`（λ ∈ [2/5, 173/400]、τ ∈ [7/8, 29/32]、δ ∈ [1/25, 4/25]）で **H ≥ ＋0.3787774915**（分数は `D3_L0T0_chat_final.json`）。B7 の公式 PASS 数は **24/40 → 25/40**。

| 条件 | 結果 |
|---|---|
| 中くらいの帯と遠い帯の被覆 [0,1]×[1/100,1]×[0,1] | PASS（20,549 セル） |
| 近い帯の被覆 [0,1]×[P₀,1/100]×[0,1]² | PASS（19,590 葉、V5.3 の凍結された分け方。下界は chat が小箱ごとに計算し直した） |
| J ＝ min_r (J_near,r ＋ S_r) | ＋1.4876892648（r ＝ 8） |
| H ≥ λ_lo c₋ J − 2λ_hi(275/4)σ(P₀) | ＋0.3787774915 |
| verifier の Muse 監査 | PASS（2026-11-08。全量を独立に計算し直し、分数まで一致） |
| Dig producer（参考） | ＋0.1457（入力には使わない） |

## コードと証拠

- verifier：`chat_b7v54_iv.py` 5233959c…、`chat_b7v54_run.py` 41ce0d93…、`chat_near_per_r.py` d7558c23…、`combine.py` 5c092793…
- 流用：`b7iv_ia.py` b2d26146…、`b7iv_vk.py` f2d6c4a9…、`b7iv_vleaf.py` 1c1ee3b4…（2026-11-04 Muse 監査済み）
- 入力：`DIG_HANDOFF_D3_V54_20549_LEAVES_NEAR19590_OUTER16_20261107.zip` 3942ad12…
- 出力：`stageB_chat_ps8.jsonl.gz` a787e831…、`near_per_r.json` 9f55ba0e…、`D3_L0T0_chat_final.json` bfd22209…
- Muse パッケージ：`MUSE_PACKAGE_B7_V54_D3_VERIFIER_20261107.zip` 40701d5f…
- 設計：Codex `ASTRA_B7_V54_DESIGN_20261107.md` dd9a96ed…、`ASTRA_B7_V54_D3_CURVATURE_REDESIGN_20261107.md` 3b30c8c5…（chat 監査 ACCEPT 766fd4b2…、67380932…）

## 記録しておくこと

1. **prefactor**：V5.4 は負の J に c₊ ＝ 636619773/10⁹、正の J に c₋ ＝ 636619772/10⁹ を使う（V5.3 は負の J に 2/3）。本箱は J ≥ 0 なので c₋ を使用。
2. **近い帯**：V5.3 の葉の分け方だけを使い、下界は外側の小箱 r ごとに B7IV で計算し直した（V5.3 の外箱全体の値 −1.332 に対し、小箱ごとは −0.919〜−0.089）。
3. **chat verifier の改良の経緯**：1回目（6通りの順序、p の分割なし）は Jfar ＝ −1.973。p を固定しない2階微分の評価域を p について8分割（PSPLIT ＝ 8、inf は部分の inf の最小）して ＋2.296。両方の log を残す。
4. Muse 報告 §8 の「正式数 23/40」は誤記で、採用前の正式数は 24/40。
