# D5 M22実核：固定32分割による局所下界候補
2026-11-05 JST / Astra継続解析 / isolated local pilot

**判定：LOCAL BOUND CANDIDATES FOUND。M22全域認証はOPEN。**
**M40、D5 V4 FREEZE、D5全域本走の状態は変更しない。**

## 1. 結果

| ケース | λ | z | 有理下界の参考小数 | 厳密な丸め下界 |
|---|---|---|---:|---:|
| center_half | 1/2 | 0 | −11.355921100665386 | −12 |
| hard_axis_enlarged_rectangle | [2/5,81/200] | [7/200,81/1600] | −190.61027893223647 | −191 |

両者ともρ=0の \(E_{\rho\rho zz}(0,0,z;\lambda)\) を対象とする。M40のρ外箱は使用しない。

今回得た計算候補は
\[
E_{\rho\rho zz}(0,0,0;1/2)\ge L_{\rm center}>-12>-400,
\]
\[
E_{\rho\rho zz}(0,0,z;\lambda)\ge L_{\rm hard}>-191>-400
\]
である。ただし、これらの認証の採用には物理jet生成・原kernel正規化の独立監査が残る。数式と外向き演算に基づく局所下界候補であり、全対象域PASSとはしない。

### 正確な下界

\[
L_{\rm center}
=-\frac{1519473017763337040732287893283870359046133225}
{133804471191183738849214309635890169035882496}.
\]

\[
L_{\rm hard}
=-\frac{3188063447016491501593387742336897551732021843}
{16725558898897967356151788704486271129485312}.
\]

−12、−191との比較は浮動小数を使わず、Fractionによる整数有理算術で確認した。

## 2. 実行前に固定した契約

contract.jsonを評価開始前に作成した。

- 2ケースのみ。
- μ半角uは[0,1]の一様32分割。
- μ符号は±の両方。
- 1ケース64セル寄与、2ケース合計128セル寄与。
- 128-bit dyadic grid、全四則演算を外向き丸め。
- 平方根は整数isqrtによる下側・上側witness。
- 共通momentの打切り次数N=24。
- R補助積分のK=32は変更しない。今回のmoment積分は、同じ32補助セルのべき積分を先に望遠和したexactな全区間式で評価する。
- adaptive subdivisionなし。
- 外箱分割なし、再試行によるmesh変更なし。
- 外部PC、既存producer/verifier、B7、Git、D5本走への操作なし。

独立したローカル試作であり、既存証明書を置き換えていない。

## 3. 使用した数学的核

M22追補の軸上K20を使用。
\[
a^2=1-\mu^2,\quad d^2=a^2+(\lambda\mu-z)^2,\quad
h=\lambda-z\mu,\quad w^2=\lambda^2+(1-\lambda^2)\mu^2,
\]
\[
L=wd+h,\quad V=h-\lambda d^2,
\]
\[
P=\frac{h^2(2d^2-a^2)-2a^2V^2}{d^4},\qquad
Q_0=\frac{a^2hV^2}{d^4}.
\]
\[
q=\frac{a^2\{(1-\lambda^2)\mu+\lambda z\}^2}{L^2}.
\]
μ半角Jacobian \(j(u)=4u/(1+u^2)^2\) を含めて
\[
\mathsf a=\frac{jP}{\lambda L},\quad
\mathsf b=\frac{jQ_0}{\lambda L^2},\quad
U(x)=(\mathsf a+\mathsf b)+(\mathsf a q-\mathsf b)x.
\]
\[
\Psi=\frac{U(v^2)}{(1+qv^2)^2}.
\]
\[
E_{\rho\rho zz}=\sum_{\epsilon=\pm1}\int_0^1\int_0^1\Psi_{zz}\,dv\,du.
\]

z²×u²の9係数jetを構成し、
\[
\Psi_{zz}=\frac{N_2(v^2)}{(1+qv^2)^4},\qquad
\Psi_{zzuu}=\frac{N_4(v^2)}{(1+qv^2)^6}
\]
を計算した。N2は4係数、N4は6係数。
j′とj″はjetに含む。方位角の係数・πを後掛けしない。

有限moment部分を共通qのHorner式で評価し、尾部は前報のmonomial正部分上界とBernstein正部分上界の小さい方を採用。双方とも独立に有効な上界である。これは実行前に試作コードで固定した処理であり、結果に応じた方式切替ではない。

## 4. 矩形拡大の扱いとqの安全上界

厳しい軸上外箱は、λ=2/5付近で元の \(|z|\le\lambda/8\) をわずかに越える。
本試作は交差領域だけでなく、その拡大矩形全体を包囲した。
従ってこのケースにはM22追補のq≤2/7を使用しなかった。

\(Z=81/1600\) と置くと
\[
wd\le(1+\lambda^2)/2+Z,\qquad h\ge\lambda-Z>0.
\]
\[
F(\lambda)=\frac{(1+\lambda^2)/2+Z}{\lambda-Z}
\]
の微分の分子は
\[
(\lambda^2-1)/2-\lambda Z-Z<0
\]
なので、λ帯上で最大はλ=2/5。
\[
\frac{wd}{h}\le\frac{1009}{559},\qquad
\gamma\ge\frac{559}{1009},
\]
\[
\boxed{q\le\frac{225}{784}.}
\]
この上界をcontractに事前固定した。

中心点には元の軸上全域補題からq≤2/7を使用した。

幾何capsとして
\[
d\ge\lambda_{\rm lo}-|z|_{\max},\qquad
d\le1+|z|_{\max},\qquad w\ge\lambda_{\rm lo}
\]
等を使用する。capsはjetの0次係数のみとの交差であり、その下端・上端を微分していない。導関数係数はexactな滑らかな核のjetから生成する。

## 5. 損失台帳

以下は全64寄与を加算した値。小数は表示用のみ。

| ケース | finite midpoint下界の和 | finite curvature寄与 | moment尾部損失 | 最終下界 |
|---|---:|---:|---:|---:|
| 中心点 | −3.9514956049220795 | −7.404425495743306 | 9.1591×10^-20 | −11.355921100665386 |
| 厳しい軸上外箱 | −117.57188675682568 | −73.03839217540303 | 7.7705×10^-12 | −190.61027893223647 |

厳密な台帳はresults.jsonに保存。
\[
L=\sum_C\left(h_C A_C^-+\frac{h_C^3}{24}B_C^- - e_C\right).
\]

ここから言えるのは、**今回の2ケースではmoment尾部支払いが支配していない**こと。
中心点と厳しい外箱は幾何点も異なるため、両者の差を外箱幅だけの損失と解釈してはいけない。
finite midpointの負値も真のintegrandの符号分類ではなく、認証下界である。

## 6. 実施済みの検算

### A. 区間演算・jetの基本確認

- interval積の端点をFractionの正確な四隅積と比較。
- 逆数jetの積が恒等1の全係数を包囲すること。
- 平方根jetの二乗が元jetの全係数を包囲すること。
- 正の平方根の整数上下witness。
- 極u=0でq=0、j=0に対応してN2が0を包囲すること。

これらは限定的な単体検算であり、実装全体の独立検証の代替ではない。

### B. 球でのexact normalization control

λ=1,z=0は対象λ帯の外であり、補助整合検査としてのみ使用した。

軸上kernelをzで二階微分して中心化すると
\[
K_{20,zz}(0,1,\mu)=10\mu^4-\frac{23}{3}\mu^2-\frac13.
\tag{6.1}
\]
従って
\[
\int_{-1}^1K_{20,zz}\,d\mu
=4-\frac{46}{9}-\frac23=-\frac{16}{9}.
\]

導出の中間式：\(a^2=1-\mu^2\) とすると
\[
\gamma=1-\frac{a^2}{2}z^2+O(z^3),\quad
\gamma R(\gamma)=1-\frac{a^2}{3}z^2+O(z^3),
\]
\[
U=\mu z+(3\mu^2-1)z^2+O(z^3),
\quad
C=\frac12+2\mu z+(7\mu^2-1)z^2+O(z^3).
\]
前報のK20へ代入するとz²係数が
\(5\mu^4-\frac{23}{6}\mu^2-\frac16\)。
二階微分で2倍して(6.1)。

u=0,1/4,1/2,3/4,1の両μ枝、計10個の有理点で、試作のmoment包囲が
\[
j(u)\left(10\mu^4-\frac{23}{3}\mu^2-\frac13\right)
\]
を含むことをFractionで検査した。
これは数値positivity samplingではなく、既知のexact恒等式との有限な実装controlである。全域正当性の証明には読み替えない。

### C. 別実装のmoment・集計checker

check_moments.pyは、producerのIクラスやmoment関数をimportせず、
Fraction端点の区間演算で、保存された係数包囲から再構成する。

- 256件のmoment包囲：全件、producerの包囲が再構成包囲を包含。
- 128セル寄与：欠落・重複なし。
- uセル端点：正典j/32,(j+1)/32から再構成。
- 中点重みh、曲率重みh³/24：一致。
- 全セル合計：exact一致。
- −12、−191、−400との有理比較：成立。

判定：
**MOMENT_AND_AGGREGATION_CHECK_PASS**。

**未検証：物理幾何からN2,N4の区間jetを生成する部分は別実装で再構成していない。**
このcheckerは渡されたN2/N4/q区間が実核を包含することまでは証明しない。
原kernelの正規化と物理jet生成の独立検証が、正式採用前の残課題である。

## 7. 再現手順

同じディレクトリで
\[
\texttt{python pilot.py}
\]
次に
\[
\texttt{python check_moments.py}
\]
を実行する。標準Pythonライブラリのみを使用する。

pilotはローカルresults.jsonを生成する。外部PCやGitHubを操作しない。
小数への変換は最終表示のみ。成立判定はすべて有理数または整数で行う。

本環境では各ケース約1秒だったが、これは今回の2ケース・試作・実行環境の計測値であり、全域計算のruntime見積りや旧実装との公平な性能比較ではない。

## 8. 次に必要な最小作業

1. chat/MuseによるK20原定義・正規化・物理jet生成の独立検証。
2. Judgeが固定した既存のM22外箱被覆を受け取り、この評価器が適用可能な全箱の有無を確認。
3. その被覆に対する下界評価と全域集計。局所2ケースから全域へ外挿しない。
4. M40は同じmoment evaluatorの候補があるが、実核の局所試験・全域評価は未実施。

今回だけでM22全域PASS、M40 PASS、D5 V4 FREEZEを宣言しない。
既存の他工程は変更しない。

## 9. 同梱ファイル

- contract.json：評価前固定条件。
- pilot.py：実核・jet・有理moment・中点則のローカル試作。
- results.json：全128セルの係数包囲、下界、尾部、合計。
- check_moments.py：別実装のmomentと集計checker。
- moment_checker_result.json：検証結果と未検証範囲。
- normalization_checks.py / normalization_checks_result.json：球・極の補助整合検査。
- SHA256SUMS：同梱ファイルのbytesハッシュ。
