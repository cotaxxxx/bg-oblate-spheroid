# B7 V5.4 T2/T3 — 未採用 chat verifier 数値候補（2026-11-09）

**分類：VERIFIER_NUMERIC_ONLY / NOT_ACCEPTED / 公式B7=26/40。**

Muse監査済み不変verifier ZIPのSHA256：
68747f031bb89c1237c45322ad6c6b6f645458e6da923e3b9237056526dd7ec9。
2つの結果ZIPの各SHA256SUMS.txtの11件すべて一致。
stageB 20,549セル、nearはそれぞれ18,633/17,839葉。
2026-11-09 07:47:22 JST開始、07:58:45/47 JSTにmid/far完了、08:16 JSTに最終数値JSON/ZIP作成。

| 箱 | near葉 | min r | J_totalの表示 | 厳密H_lowerの表示 | ZIP SHA256 |
|---|---:|---:|---:|---:|---|
| L0_T2_D3 | 18633 | 8 | +1.7521556146078228 | +0.44612329440206083 | 8b35ee40849d9fc3e68a556d2cb89a521c01be86fdd9ac37efbb2a91cf4d82cc |
| L0_T3_D3 | 17839 | 8 | +1.9111148461882392 | +0.48660193030846877 | ac97049d0159e1846a9c2812570eb22c348a4cea2306fe05d3dd5cbde1441de0 |

**重要：初回near実行はPythonの整数文字列変換4300桁制限で停止。**
数学核やMuse監査済みverifierソースは変更せず、
整数文字列変換制限を解除して同じコードと入力でnearを再実行。
別添のL0_T2_D3_near_per_r_retry.logおよびL0_T3_D3_near_per_r_retry.log
には16小箱の完走が記録される。
結果ZIPに同梱されたnear_per_r.logは初回停止のログである。
途中の数値結果は流用せず、再実行で完成したnear JSONのみをcombineに使用。

各ZIP同梱のDIG_ARITHMETIC_READBACK.jsonは、
20,549セル×16小箱の有理数和、near別の全16下界、J/Hの厳密算術一致を示す。
**数学核の独立照合ではない。**

採用条件：（1）Muse監査済みverifierを無変更使用、
（2）chat_box_check.pyの4項目〔被覆、J/H分数再計算、20セル×16再計算、
最悪rの近帯全葉再計算〕全PASS、（3）厳密H>0。
**（2）は現時点で未実施のため正式採用・STATE増加は禁止。**
すべて成立すれば箱ごとの新しいJudge操作は不要。
