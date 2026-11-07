# chat 検収記録：D5 外側境界の面 B′ v2（832 箱）

2026-11-07 / 検収: chat / 判定者: Judge

## 定理（面の下界）

τ ∈ [0, 1]、λ ∈ [2/5, 33/50] のすべてで、外側の面の点 L_λQ(τ) において **H ≥ 1/5**（m_∂ ＝ 1/5、Judge 裁定）。
得られた最小値：chat verifier ＋0.3204609366（τ ∈ [1/32, 1/16]、λ ∈ [2/5, 41/100]）、Dig producer ＋0.2642053359（τ ∈ [1/16, 3/32]、λ ∈ [2/5, 41/100]）。

## 採用の条件（仕様 v1 §4）と照合結果

| 条件 | 結果 |
|---|---|
| 被覆の検査 | PASS。`bprime_cover_32x26.json`（ファイル SHA 071062a9…、正規化 SHA deb6bc3b…）、τ 32 × λ 26 の直積、隙間・重なりなし、内側 32×32 |
| producer が全箱で ≥ 1/5 | PASS。832/832、`bprime_v2_pilot.py` d60fe187… |
| verifier が全箱で ≥ 1/5 | PASS。832/832、`chat_bprime_iv.py` 93b9431d…、log の最終行 `BPRIME VERDICT: PASS` |
| verifier の Muse 監査 | PASS（2026-11-07、追加の条件なし） |
| chat の抜き取り再計算 | **20/20 が分数の文字列まで一致**（verifier の下界が小さい10箱 ＋ シード 20261107 で選んだ10箱） |

## 証拠

- 証拠 ZIP：`DIG_D5_BPRIME_V2_832_FULL_EVIDENCE_20261107.zip` SHA 027f42f0140144bfaf90eec958d05b7e5b8ac24f81e995ef316bec2fe8a99b81
- `verifier/chat_bprime_verifier_full.jsonl` 781e82ad…、`producer/dig_bprime_producer_full.jsonl` dad8c364…、`logs/chat_verifier_run.log` 50b9b0e9…
- chat の照合：`check_ev.py` 4d116619…、`sample20.json` 5de56f53…、`sample20_out.jsonl` f64a3729…

## 記録しておくこと

1. **γ ∈ [0, 1] の根拠**（Muse 監査 §4 の申し送り）：ξ ＝ (x, y, z)、Q ＝ (a, 0, b) として
   σ²(4w²K − λ²σ²)/4 ＝ y²·[λ²a² ＋ (1−λ²)²(z ＋ λ²b/(1−λ²))²] ＋ [λ²bx − z(a − (1−λ²)x)]²
   （a² ＋ b² ＝ 1、x² ＋ y² ＋ z² ＝ 1 のもとで恒等式。Muse が構成し、chat も sympy で確認）。
2. **Dig producer の q ＝ 1 の端**：N ＝ 30（偶数）の有限 Taylor 剰余 T_N − E_N ≤ K_n ≤ T_N を使う。x ≥ 0 のすべてで成り立つので、q ＝ 1 でも正しい（chat 確認）。

## 範囲（Muse 監査 §10 と同じ）

- 閉じるのは面 r ＝ 1 そのものだけ。面の内側の薄い層（カラー）と一般域は OPEN。**D5 全体は OPEN**。
- FT_q V4 の再認証を兼ねられるかどうかは未照合。
