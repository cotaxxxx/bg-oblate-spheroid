# L1-R0 exact paper re-audit — 2026-10-17

**判定：PASS WITH CORRECTIONS。**

**BOUNDARY-KERNEL SCOPE STOP: PASS。K_H route は表示・適用域・正規化について有効。B_int は本再検算上 AUDITED CANDIDATE。L1 positivity は未証明。**

対象：`L1_R0_COMPACT_AND_KERNEL_DOMAIN_LEDGER_V0.md`、SHA-256 `da36508507015ed968c4a386fdcc2becb6523408fea078faba16e840fda868e6`。

本稿は同じ会話内で前稿を担当した実行主体による、原典の再取得と新規 exact algebra による再検算である。第三者 chat の独立性を主張せず、その独立監査の代替とは数えない。Judge に提出できる再現資料として、原典 bytes、差分恒等式検算、結果を同梱する。

## 1. Source audit

指定8 pin は **8/8 MATCH**。内訳は7文書の SHA-256 と PREDECLARE の commit 1件である。取得した GitHub UTF-8 本文を変更せず、SHA-256 と Git blob SHA-1 を再計算した。PREDECLARE は指定 commit の metadata と、その commit における本文を照合した。

L3 V0.2、L3 audit/freeze、L1 restart brief は、設計 branch の読み戻しで得た固定 commit `332adcaaedd0403430645e7192d392e8a1231367` から再取得した。本文に残る過去の PAUSED / NOT FROZEN 表示は、その後の Judge 裁定を撤回するものではない。

| 指定項目 | exact pin | 判定 |
|---|---|---|
| PREDECLARE V1.2 SHA | `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217` | MATCH |
| PREDECLARE commit | `e9c8b1caa3ad502a3d01dafe354b61108787eed2` | MATCH |
| L3-MRA | `b13e07d63b3f3035b7b983cc39acbae893d4a184dfa030eaf73bb9f243a0d842` | MATCH |
| L0 | `41b6be56e6e81f6b0f90e155865f9fc9fcd75129215cfd5df8be6845755c639e` | MATCH |
| QM | `e8588c1b677e10aceac22e79784e41111cffe2c2cffce1636804485dafb09edc` | MATCH |
| L3 V0.2 | `d4d2591e0a800202e50224eb9caa697a35054db6971885bc727d87aad5766997` | MATCH |
| L3 audit / conditional FREEZE | `37419196a0c6f5ccb2d0e02a7b30da7e6e0b03608e58f7440ad7d3030db68d42` | MATCH |
| L1 restart brief | `8b2ad090e70dcd144a2a2c4ad0f31f6e8caadc46dbc15abfa17be48d4ce6a533` | MATCH |

補助 P1 は commit `6c6282a8acbf467bcbe6a7e32236e1d32a91f400`、SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`、L2 は commit `9eb8ddee96cbb1703618aa606eeb9e81f7697549`、SHA-256 `0a83e411e51582674c5490cb8e92defd171481c6271c48c6760681b8f5e839cb` に一致した。

補助 FTQ signed reduction V0 の artifact bytes は SHA-256 `91d1702836410e6a2ce78593079e166afd7a1a887839af86d92cc64b0f8e9208` に一致した。この資料は保存済み artifact と現行全文 readback で照合したものであり、GitHub commit の照合とは表示しない。全文 read API は末尾 LF を省略しており、元 bytes 132,840 と readback 132,839 の差は末尾 LF 1 byte だけである。指定8 pin の GitHub bytes 照合とは区別する。

完全な path / ref / blob / SHA / byte count は `provenance.json`。R0 V0 にあった「指定8 pin 未取得」は今回解消した。G2 の特定や、その内容の推定はしていない。pin 一致は、継承する解析的前提すべての再証明を意味しない。

## 2. Audit A・B：boundary scope と exact witness

表面点を x=L_λ ξ、基点を p=L_λ(rQ)、|ξ|=|Q|=1 とする。以後、表面 unit normal は N、正規化 chord の方向は ν と書いて区別する。

P1 §1 の wN=(λξ_x,λξ_y,ξ_z) より

\[
h=w(x-p)\cdot N=\lambda(1-r\xi\cdot Q).
\]

一方

\[
\sigma^2=|\xi-rQ|^2=1+r^2-2r\xi\cdot Q,\qquad\delta=1-r^2
\]

だから

\[
\boxed{h=\frac\lambda2(\sigma^2+\delta)},\qquad
D=\sigma k,\qquad
\boxed{\gamma=\frac{\lambda(\sigma^2+\delta)}{2w\sigma k}}.
\]

境界 r=1 では δ=0。内部では δ>0 なので、境界の h=λσ²/2 をそのまま代入できない。weight W の式を保持することは可能だが、境界 B との組を内部表示として無変更使用する経路は STOP である。

r=7/8、τ=1、ξ=Q=(0,0,1) では δ=15/64、σ=1/8、w=1、k=λ、D=λ/8。従って

| 量 | 内部の正しい値 | 境界式を誤流用した値 |
|---|---|---|
| h | λ/8 | λ/128 |
| γ=h/(wD) | 1 | 1/16 |

この witness は compact の端点 r=7/8 に属する。表示の適用域の反例であり、H の正値性の反例ではない。L3 が境界表示と QM transfer を区別していることとも矛盾しない。

## 3. Audit C・D・E：K_H と正規化

P1 §8.2 の原典は

\[
H=\frac1{4\pi\lambda}\int_{-1}^1\int_0^{2\pi}K_H\,d\phi\,d\mu,
\quad K_H=\frac{F_{E,\rho}(\rho,b)-F_{E,\rho}(-\rho,b)}{2\rho}.
\]

ここで F_{E,ρ}(−ρ,b) は「第一引数で微分してから −ρ で評価」である。合成関数 F_E(−ρ,b) の ρ 微分そのものとは区別する。

FTC により

\[
F_{E,\rho}(\rho,b)-F_{E,\rho}(-\rho,b)
=\int_{-\rho}^{\rho}F_{E,\rho\rho}(u,b)\,du.
\]

u=vρ、du=ρdv と置けば

\[
\boxed{K_H=\frac12\int_{-1}^1F_{E,\rho\rho}(v\rho,z;\mu,\phi)\,dv}.
\]

内部 compact と sweep 全体で密度は滑らかである。従って ρ→0 の極限は F_{E,ρρ}(0,z)。軸ではこの積分表示を定義として用い、1/ρ を評価しない。

P1 §1・§8.1 の h と D² は ρb と ρ² に依存するため、F_E(−ρ,b)=F_E(ρ,−b)。chain rule から

\[
-F_{E,\rho}(-\rho,b)=F_{E,\rho}(\rho,-b),\qquad
K_H=\frac{F_{E,\rho}(\rho,b)+F_{E,\rho}(\rho,-b)}{2\rho}.
\]

よって K_H は b-even。軸でも連続極限によって成立する。後半の azimuth に φ′=φ−π を用いると Jacobian は1、b は反転し、

\[
K_{\rm pair}=K_H(\phi)+K_H(\phi+\pi)=2K_H(\phi),
\quad H=\frac1{4\pi\lambda}\int_{-1}^1\int_0^\pi K_{\rm pair}\,d\phi\,d\mu.
\]

次に s=cosφ は [0,π] を [1,−1] へ写し、dφ=−ds/√(1−s²)。dω=ds/(π√(1−s²)) とすると

\[
H=\frac1{4\lambda}\int_{-1}^1\int_{-1}^1 K_{\rm pair}\,d\omega\,d\mu
=\frac1{2\lambda}\int_{-1}^1\int_{-1}^1 K_H\,d\omega\,d\mu
=\boxed{\frac1\lambda\int_{-1}^1\int_0^1 K_H\,d\omega\,d\mu}.
\]

最後の2倍は K_H の s-evenness と dω の対称性から来る。raw WB / F_yy の s-evenness を使っていない。因子 π、2、1/2 は上の各段階で明示され、λ/(4π) の WB 表示と混同していない。L2 §§3–6 と一致する。

## 4. Audit F：compact と FTC sweep の分母

\[
\delta_0=\frac3{10^8},\quad
\frac78\le r\le r_*:=\sqrt{1-\delta_0},\quad
p_v=(v\rho,0,z),\quad -1\le v\le1.
\]

\(r_v:=|L_\lambda^{-1}p_v|\le r\)。従って |ξ−L_λ⁻¹p_v|≥1−r_v≥1−r。そして

\[
1-r=\frac\delta{1+r}\ge\frac{\delta_0}{2}=\frac3{2\cdot10^8}.
\]

λ≤1 なので L_λ の最小特異値は λ。従って

\[
D_v\ge\lambda(1-r),\qquad
h_v=\lambda(1-\xi\cdot L_\lambda^{-1}p_v)\ge\lambda(1-r),
\]

\[
\boxed{D_v,h_v\ge\frac3{5\cdot10^8}}.
\]

ここで添字 v は swept point での値であり、方向微分記号ではない。P1 の h≤wD と h>0 より 0<γ≤1。さらに

\[
w\ge\lambda\ge\frac25,\quad k^2\ge\lambda^2\ge\frac4{25},\quad
A=1+t^2+(1-t^2)\gamma\in[1,2],
\]

\[
\boxed{wk^5A^2\ge(2/5)^6=64/15625}.
\]

FTC sweep は S_AN の radial lower bound から外れ得るが、P1 §2 の内部正則性の範囲内にある。r≥7/8 は元の基点に対する条件であり、r_v≥7/8 を仮定しない。B_int を swept point に書くなら δ_v=1−r_v² を用い、元の δ を固定したまま代入してはならない。

ρ、√(1−γ²)、√(1−s²) には一様正下界を主張しない。順に FTC、R の可除特異点の延長、arcsine の可積分測度として処理する。c=1−t² で除算する必要もない。これらの下界は紙上の分母安全性を保証するだけで、signed integral の正値性や数値的 conditioning を保証しない。

## 5. Audit G：generic directional kernel からの独立再導出

固定表面点 x に対し Y=x−p、T=Y_y/D、a_y=N_y と書く。P1 の h_y=−wa_y、D_y=−T から

\[
e=\gamma T-a_y,\qquad \gamma_y=e/D.
\]

T_y=(T²−1)/D なので、もう一度微分すると

\[
\gamma_{yy}=\frac{\gamma(3T^2-1)-2a_yT}{D^2}.
\]

F_E=hG(γ)、h_yy=0、G′=−2R、G″=−2R′ を使って

\[
F_{E,yy}=-4h_yR\gamma_y-2hR'\gamma_y^2-2hR\gamma_{yy}.
\]

h=wDγ を代入し、R と R′ の係数をそれぞれ収集すると

\[
\boxed{F_{E,yy}=\frac{2w}{D}
\{R[\gamma^2(1-T^2)-2e^2]-\gamma R'e^2\}}.
\]

これは P1 Lemma 3.3–3.4 からの直接合成であり、FTQ V0 §5 の式を結果として再現する。係数単位の exact 差は0。

meridional base point では p_y=0 なので ξ_y=σν_y。従って

\[
a_y=\frac{\lambda\sigma\nu_y}{w},\quad
T=\frac{\nu_y}{k},\quad V=\nu_y^2,\quad
\eta=1+\frac\delta{\sigma^2}>1,
\]

\[
\gamma=\frac{\lambda\sigma\eta}{2wk},\qquad
\boxed{e=\gamma T(1-2k^2/\eta)}.
\]

共通積分表示は

\[
R(\gamma)=2\int_0^1\frac{dt}{A},\qquad
R'(\gamma)=-2\int_0^1\frac{c\,dt}{A^2},\qquad c=1-t^2.
\]

0≤γ<1 では前者の積分は
\(2\arctan\sqrt{(1-\gamma)/(1+\gamma)}/\sqrt{1-\gamma^2}
=\arccos\gamma/\sqrt{1-\gamma^2}\)。γ=1 は連続極限。A≥1 のためこの積分の微分も正当である。

generic kernel に代入し、**同じ t の下で** R と R′ の項をまとめる。得られる t-integrand は

\[
\frac{4w\gamma^2}{\sigma k^3A^2}
\left[A(k^2-V)-(2A-\gamma c)V(1-2k^2/\eta)^2\right].
\]

ここで γ²=λ²σ²η²/(4w²k²) を代入すると

\[
\frac{\lambda^2\sigma}{wk^5A^2}
\left[A\eta^2(k^2-V)-(2A-\gamma c)V(\eta-2k^2)^2\right].
\]

従って W=σ/(wk⁵A²) と

\[
\boxed{B_{\rm int}=A\eta^2(k^2-V)-(2A-\gamma c)V(\eta-2k^2)^2}
\]

により

\[
\boxed{F_{E,yy}=\lambda^2\int_0^1 WB_{\rm int}\,dt}.
\]

その積分は回転対称性による E_yy=H と接続する。K_H=F_{E,yy} の点別同一性は不要で、主張もしない。

## 6. Paired target と必要な文言修正

n=V/k² とし、λσ/(2w)=kγ/η を用いると

\[
\frac\lambda2WB_{\rm int}
=\frac{\gamma}{\eta k^4A^2}B_{\rm int}
=\boxed{\frac{\gamma\eta}{k^2A^2}
\left[A(1-n)-(2A-\gamma c)n(1-2k^2/\eta)^2\right]}.
\]

係数 λ/2 はこの target に取り込み済み。後掛けしない。

**修正 C1：境界特殊化の適用点。** δ=0、σ>0 なら η=1、B_int=B が exact に成立する。接触点 δ=σ=0 では η=1+δ/σ² 自体が未定義なので、その点で直接 η=1 と代入したとは書かない。境界の combined density は σ の因子、w,k,A の安全な正分母、bounded B により O(σ) で0へ延長する。方向 ν や k の一意極限は不要。内部から境界への**積分値**の延長は継承 Lemma V による。内部から接触点へ任意の経路で η→1 と主張しない。

**修正 C2：「η=1 の場合だけ」の厳密化。** V3 target を恒等的に回復する特殊化は η=1 である。しかし点別の数値的一致の必要十分条件と読むのは強すぎる。K=k²、C=2A−γc とおくと

\[
\boxed{\mathcal P_{\rm int}-\mathcal P_{
V3}=\frac{\gamma(\eta-1)}{KA^2}
\left[A(1-n)-Cn(1-4K^2/\eta)\right]}.
\]

η≠1 でも角括弧が0なら差は0となる。正しい記載は「η=1 で V3 の式族を回復する。一般の内部 η>1 では追加依存を省けず、V3 certificate を無変更流用できない」。この修正は boundary scope STOP の結論を変えない。

## 7. Sign ledger と二つの route

\[
V\ge0,\quad k^2-V=\nu_x^2+\lambda^2\nu_z^2\ge0,
\quad A\ge1,\quad 2A-\gamma c=2(1+t^2)+c\gamma>0.
\]

従って B_int は非負項と非負項の差であり、B_int≥0 は導かれない。generic formula では −γR′e²≥0 だが、残りの R 項の負寄与を処理する義務が残る。W>0 のみから H>0 を結論できない。

| 評価 | Route K：K_H / K_pair | Route B：B_int |
|---|---|---|
| 表示 | P1 §8.2・L2 と一致 | generic P1 formula から exact 導出 |
| 分母 | compact と FTC sweep 上で安全 | 同じ compact で安全、σ² と η の依存を保持 |
| 対称性 | K_H は s-even | raw density の s-evenness は仮定不可、明示両枝が必要 |
| 符号 | centered derivative / FTC 積分の残余が未評価 | 非負項−非負項の signed 積分の残余が未評価 |
| 境界整合 | 継承連続延長 | δ=0、σ>0 で boundary kernel、contact は密度の極限 |
| 紙上 closure | 有効な出発点、閉じる保証はまだない | 有効な候補、η と geometry の依存評価が追加義務 |

η は固定 compact 上でも独立な小さい摂動ではない。紙上では

\[
\frac{2}{1+r}\le\eta\le\frac{2}{1-r}\le\frac4{\delta_0}=\frac{400000000}{3}
\]

までしかこの単純な幾何だけからは言えない。これは exact な解析的範囲であり、interval computation の出力ではない。η、γ、σ を独立 worst-case 化すれば cancellation を失い得る。実用的な bound が閉じるかは本監査の結論に含めない。

M=295346256371/10¹² は既存の境界 H の lower bound としてのみ保持する。exact inf、upper bound、内部の H≥M とは扱わない。L3 の δ≤δ₀ での結論も、L1 全域を閉じたことにはならない。

## 8. 再現検算と判断範囲

`python exact_audit.py` は標準 Python Fraction と新規 sparse Laurent polynomial 実装で11項目を検査する。generic second derivative、共通 t 合成、B_int、boundary specialization、paired normalization、差の因数分解は展開後の全係数差0を確認した。witness、分母定数、L0 座標・sector factor も exact に確認した。

FTC、変数変換、積分交換の解析的根拠は本文の紙上証明と固定 P1/L2 による。有限個の代数チェックがそれらを自動的に証明したとは扱わない。今回の環境に SymPy はなく、導入せず、SymPy を実行したとも表示しない。

`python make_provenance.py` は同梱の原典 snapshot と GitHub response metadata から指定 pin / blob を再計算する。再実行時にネットワーク接続は不要。これは snapshot の再検証であり、再実行時点の GitHub 再取得ではない。

interval computation、H の数値 sampling、certification run、分割変更、commit/push、D5 access/mutation は実施していない。原典の未再監査 status を昇格していない。

## 9. Judge 向け推奨と状態

**非拘束推奨：DUAL-TRACK PAPER COMPARISON。** K_H を既存の正典表示として維持し、B_int を本再検算済み候補として比較する。B_int の正式採用、target/PREDECLARE 書換え、interval architecture は Judge の別裁定に委ねる。計算認証が必要と判明した場合も、先に G-numbered predeclare を提出する。

本再検算 verdict は **PASS WITH CORRECTIONS（C1・C2 の適用条件／文言）**。数学的 contradiction は発見していない。独立外部 chat の audit PASS を代行宣言しない。

FT_q：DISCHARGED conditional／L3：FREEZE conditional／L1：RESTART paper-only／L1-R0：PARTIAL／T1：NOT CLOSED／D-P2：NOT_CERTIFIED。状態変更なし。
