# D5カラー：境界面から内部への一様正値性の延長
## Astra依頼への数学設計回答案 — 2026年11月8日

作成：Codex。対象：D-OB P2／D5の外側カラー。
区分：**解析的補題・紙上証明案／新補題の独立監査待ち／Judge未採用**。
証明書作成、本走、既存工程の状態更新は行っていない。

依頼文はPlan Bの途中で切れている。本稿は、全文が提示されたPlan Aを主対象に回答する。Plan B後半の未受領条件を補って推測しない。

## 結論

P1のエネルギーとHの正規化、および採用済みB′ v2の境界定理
\[
H(1,\tau;\lambda)\ge\frac15,\qquad
\lambda\in[2/5,33/50],\quad\tau\in[0,1]
\]
を入力とすると、次の**具体的なカラー補題案**が得られる。

\[
\boxed{\varepsilon=\frac1{60000},\qquad
H(r,\tau;\lambda)\ge\frac{607}{6000}>\frac1{10}
\quad\left(\frac{59999}{60000}\le r\le1\right).}
\tag{T}
\]

この数値はサンプリングや箱数外挿から選んだものではなく、以下の一様評価から有理演算で得る。

\[
\boxed{
|H(r,\tau;\lambda)-H(1,\tau;\lambda)|
\le90\sqrt\kappa
  +275(1-r)\log\frac2\kappa
}
\tag{M}
\]
は、全 \(\lambda\in[2/5,33/50]\)、全 \(\tau\in[0,1]\)、
\(15/16\le r\le1\)、\(0<\kappa<2\) で成立する。

特に
\[
\kappa=\frac1{10^8},\qquad\varepsilon=\frac1{60000}
\]
とすると
\[
|H(r)-H(1)|\le
\frac9{1000}+\frac{5390}{60000}
=\frac{593}{6000}<\frac1{10}.
\]
ゆえに(T)が従う。

ここで示すのは新しい解析的論証である。既存のJudge裁定を更新したという意味ではない。D5カラーの正式採用には、本稿の核の対応・新しい定数9と66・積分評価の独立照合が残る。

# 1. 正典との対応と記号

## 1.1 固定する表示

正典P1 §1の楕円体と線形写像を
\[
L_\lambda=\operatorname{diag}(1,1,\lambda),\qquad
K_\lambda=L_\lambda\overline{B(0,1)}
\]
とする。単位球上の積分点を \(\xi\in S^2\)、物理空間の表面点を
\(x=L_\lambda\xi\) とする。

\[
Q=(a,0,b),\qquad
a=\frac{1-\tau^2}{1+\tau^2},\quad
b=\frac{2\tau}{1+\tau^2},\qquad |Q|=1,
\]
\[
p_r=rL_\lambda Q.
\]

以下では、内部半径をr、角度の有理化変数をuとし、両者を区別する。

| 記号 | 定義 |
|---|---|
| \(d=1-r\) | 内部への半径方向の深さ |
| \(c=\xi\cdot Q,\ q=1-c\) | 接触方向との関係。\(0\le q\le2\) |
| \(\sigma=|\xi-rQ|\) | 単位球側の距離 |
| \(v=x-p_r=L_\lambda(\xi-rQ)\) | 物理空間の差ベクトル |
| \(D=|v|\), \(\omega=v/D\) | 物理距離と単位方向。D>0の点で定義 |
| \(w=\sqrt{\lambda^2(\xi_x^2+\xi_y^2)+\xi_z^2}\) | 表面の面積係数 |
| \(n=(\lambda\xi_x,\lambda\xi_y,\xi_z)/w\) | 表面の外向き単位法線 |
| \(h=w\,v\cdot n\) | P1のh |
| \(\gamma=n\cdot\omega=h/(wD)\) | P1の角度変数 |

ここでnは単位法線であり、B′仕様のスカラー \(n=\nu_y^2/K\) とは異なる。後者には§3で \(n_B\) を使う。

\[
dA=w\,d\Omega,\qquad dA/w=d\Omega
\]
で、\(d\Omega\) は単位球の面積測度である。余分なwや \(1/w\) を挿入しない。

\[
E(p)=\frac1{4\pi\lambda}\int_{S^2}F_E(x,p)\,d\Omega,\qquad
F_E=h\,g(\gamma),\quad g(\gamma)=\arccos^2\gamma.
\tag{1}
\]

これはP1 §1の表示そのものである。物理座標のy方向は、以後固定されたCartesian方向 \(e_y=(0,1,0)\) とする。

## 1.2 Hと横方向二階微分

内部の回転対称性から、\(\rho>0\) の点 \((\rho,0,z)\) では
\[
E_{yy}(\rho,0,z)=\frac{E_\rho(\rho,z)}{\rho}=H(\rho,z).
\]
軸 \(\rho=0\) では回転対称性によって \(E_{yy}=E_{xx}=H\) となる。

内部点には表面まで正の距離があるので、(1)をy方向に二回微分してよい。したがって
\[
\boxed{
H(r,\tau;\lambda)
=\frac1{4\pi\lambda}\int_{S^2}\mathscr K_r(\xi)\,d\Omega,\qquad
\mathscr K_r=F_{E,yy}(x,p_r).
}
\tag{2}
\]
境界では接触点を除いて同じ核を定義する。§3でB′核との完全な一致を示し、§5で絶対可積分性を示す。この接続は、境界上の三階正則性を前提にしない。

# 2. \(\eta\) を導入しない共通内部核

## 2.1 幾何の相関

直接計算から
\[
h=\lambda(1-rc)=\lambda(d+rq),
\tag{3}
\]
\[
\sigma^2=d^2+2rq=d^2+4r\sin^2(\psi/2).
\tag{4}
\]
また
\[
\lambda\sigma\le D\le\sigma,\qquad
\lambda\le w\le1.
\tag{5}
\]

凸性より
\[
0\le h\le wD,\qquad 0\le\gamma\le1
\tag{6}
\]
が成り立つ。これはhとDを独立に粗く包囲した結果ではなく、\(\gamma=n\cdot\omega\) という幾何学的相関である。

\(\eta=1+(1-r^2)/\sigma^2\) は本証明で用いない。r=1、\(\xi=Q\) の接触点ではD=σ=0であり、\(\omega,\gamma\) を商から定義しない。積分ではこの一点を除く。値を任意に補っても積分は変わらない。

## 2.2 角度関数の安全な表示

\[
R(\gamma)=\frac{\arccos\gamma}{\sqrt{1-\gamma^2}}
=2\int_0^1\frac{dt}{1+t^2+(1-t^2)\gamma}.
\tag{7}
\]
右辺は \(\gamma=1\) でも正則であり、R(1)=1。
\[
g'=-2R,\quad
R'=-2\int_0^1\frac{1-t^2}{A_t^2}\,dt,\quad
R''=4\int_0^1\frac{(1-t^2)^2}{A_t^3}\,dt,
\]
\[
A_t=1+t^2+(1-t^2)\gamma\ge1+t^2\ge1.
\]
よって
\[
0<R\le\frac\pi2,\qquad |R'|\le1,\qquad
0\le R''\le\frac{32}{15}<3.
\tag{8}
\]
第二の評価には
\[
2\int_0^1\frac{1-t^2}{(1+t^2)^2}\,dt
=2\left[\frac{t}{1+t^2}\right]_0^1=1
\]
を用いた。

## 2.3 相殺済みの二階核

\[
T=\omega_y,\qquad e=\gamma T-n_y,\qquad
S=\gamma^2(1-T^2)-2e^2.
\tag{9}
\]
すると
\[
\boxed{
\mathscr K_r
=\frac{2w}{D}
\left\{R(\gamma)S-\gamma R'(\gamma)e^2\right\}.
}
\tag{10}
\]

**導出。** 表面点xを固定して基点pをy方向に微分すると
\[
h_y=-wn_y,\quad D_y=-T,\quad
\gamma_y=\frac eD,\quad
\gamma_{yy}=\frac{2eT-\gamma(1-T^2)}{D^2}.
\]
\(h_{yy}=0,\ g'=-2R,\ g''=-2R'\) より
\[
F_{E,yy}
=-4h_yR\gamma_y-2hR'\gamma_y^2-2hR\gamma_{yy}.
\]
\(h=wD\gamma,\ n_y-\gamma T=-e\) を代入すると(10)となる。□

この式は既存Route B ledgerのgeneric directional kernelと同じものである。内部に境界専用の \(\eta=1\) を代入した式ではない。

# 3. B′ v2境界核との正規化の完全一致

r=1、\(\sigma>0\) とする。球側の単位方向と係数を
\[
\nu=\frac{\xi-Q}{\sigma},\qquad
K=\nu_x^2+\nu_y^2+\lambda^2\nu_z^2,\quad k=\sqrt K,
\quad n_B=\frac{\nu_y^2}{K}
\]
とする。すると
\[
D=\sigma k,\quad T=\frac{\nu_y}{k},\quad T^2=n_B,\qquad
\gamma=\frac{\lambda\sigma}{2wk}.
\]
Q_y=0だから
\[
n_y=\frac{\lambda\xi_y}{w}
=\frac{\lambda\sigma\nu_y}{w}
=2\gamma K T,\qquad
e=\gamma T(1-2K).
\]
従ってB′仕様の
\[
\alpha_B=1-n_B-2n_B(1-2K)^2,\qquad
\beta_B=n_B(1-2K)^2
\]
に対し
\[
S=\gamma^2\alpha_B,\qquad e^2=\gamma^2\beta_B.
\]
(10)は
\[
\mathscr K_1
=\frac{2w\gamma^2}{\sigma k}
 [\alpha_BR-\gamma\beta_BR']
=\frac{\lambda\gamma}{K}
 [\alpha_BR-\gamma\beta_BR'].
\]
B′の
\[
f=\frac{\gamma}{2K}[\alpha_BR-\gamma\beta_BR']
\]
と比べれば
\[
\boxed{\mathscr K_1=2\lambda f.}
\tag{11}
\]
したがって
\[
\frac1{4\pi\lambda}\int_{S^2}\mathscr K_1\,d\Omega
=\frac1{2\pi}\int_{S^2}f\,d\Omega
=\frac1\pi\int_{\xi_y\ge0}f\,d\Omega.
\]
最後の式はy反射対称性を使ったものであり、B′ v2の
\[
H(1)=\frac1\pi\int_0^\pi\int_0^\pi
 f(\psi,\theta)\sin\psi\,d\psi\,d\theta
\]
と完全に一致する。**追加の1/2やλ換算は不要。** 数値的一致に頼る正規化確認ではない。

# 4. 新しい核定数：9と66

以下は表面点xを固定した核の評価である。積分済みHの一様な三階微分可能性を主張するものではない。

## 4.1 射影の相関

\[
\gamma=n\cdot\omega,\qquad |n|=|\omega|=1
\]
なので
\[
|\gamma\omega-n|^2=1-\gamma^2.
\]
eはこのベクトルのy成分だから
\[
\boxed{|e|\le\sqrt{1-\gamma^2}\le1.}
\tag{12}
\]
\(|\gamma T|+|n_y|\le2\) と早期に分離するより鋭く、接触点に近づいても有効である。

\[
0\le\gamma^2(1-T^2)\le1,\qquad 0\le e^2\le1
\]
より
\[
-2\le S\le1,\qquad |S|\le2.
\tag{13}
\]

## 4.2 絶対値核上界

(8)(10)(12)(13)から
\[
|\mathscr K_r|
\le\frac{2w}{D}\left(2\frac\pi2+1\right)
\le\frac{2\pi+2}{D}<\frac9D.
\]
従って安全な有理定数として
\[
\boxed{|\mathscr K_r|\le\frac9D.}
\tag{14}
\]
これは接触近傍の制御に用いる。特異性を無視した一様定数ではなく、D^{-1}という可積分な特異性を残す。

## 4.3 接触点の外側で使う混合三階核上界

基点pに関する任意の固定単位方向vの微分を \(\partial_v\) とする。表面点x、w、nは固定する。
\[
|\partial_vD|\le1,\qquad
\partial_v\omega
=\frac{-v+\omega(\omega\cdot v)}D,\qquad
|\partial_v\omega|\le\frac1D.
\]
ゆえに
\[
|\partial_v\gamma|\le\frac1D,\quad
|\partial_vT|\le\frac1D,\quad
|\partial_ve|
=|(\partial_v\gamma)T+\gamma\partial_vT|
\le\frac2D.
\tag{15}
\]
\[
|\partial_vS|
\le\frac{2+2+8}{D}
=\frac{12}{D}.
\tag{16}
\]

\(B=RS-\gamma R'e^2\) とおくと
\[
|B|\le\pi+1,
\]
\[
\partial_vB=
R'(\partial_v\gamma)S+R\partial_vS
-(R'+\gamma R'')(\partial_v\gamma)e^2
-2\gamma R'e\,\partial_ve.
\]
各項に(8)(12)–(16)を適用すると
\[
|\partial_vB|
\le\frac{2+6\pi+4+4}{D}
=\frac{10+6\pi}{D}.
\]
従って
\[
|\partial_v\mathscr K_r|
=\left|\partial_v\left(\frac{2wB}{D}\right)\right|
\le\frac{2\{(\pi+1)+(10+6\pi)\}}{D^2}
=\frac{22+14\pi}{D^2}.
\]
\(\pi<22/7\) より
\[
\boxed{|\partial_vF_{E,yy}(x,p)|\le\frac{66}{D^2}.}
\tag{17}
\]

(17)は必要な「固定y方向二回＋任意v方向一回」の核微分評価である。既存QM-1の全ての任意三方向評価や、その採用状態を差し替える主張ではない。

# 5. 接触近傍と補集合の積分評価

\(r\ge15/16\)、\(\lambda\ge2/5\) とする。半径をrから1へ動かす全経路について、(4)(5)より
\[
D_s^2\ge\lambda^2\sigma_s^2
\ge2\lambda^2s q
\ge2\left(\frac25\right)^2\frac{15}{16}q
=\frac3{10}q,\qquad r\le s\le1.
\tag{18}
\]
特に
\[
D_s\ge\frac12\sqrt q.
\tag{19}
\]
(18)を遠方の二乗分母、(19)を近傍の一次分母に使用する。

## 5.1 正しい測度

Qを中心に球面極座標を取ると \(q=1-\cos\psi\) だから
\[
d\Omega=\sin\psi\,d\psi\,d\theta=dq\,d\theta.
\]
よってqだけの非負関数Jについて
\[
\int_{S^2}J(q)\,d\Omega=2\pi\int_0^2J(q)\,dq.
\tag{20}
\]

これはP1の \(dA/w\) と一致する測度である。物理表面の面積だけを使って、核の特異性を無視する評価ではない。

## 5.2 接触球冠 \(q<\kappa\)

(14)(19)をrと1の両方に使うと
\[
|\mathscr K_r-\mathscr K_1|
\le\frac9{D_r}+\frac9{D_1}
\le\frac{36}{\sqrt q}.
\]
(20)と \(1/\lambda\le5/2\) より、正規化後の近傍寄与は
\[
\begin{aligned}
N_\kappa
&=\frac1{4\pi\lambda}
 \int_{q<\kappa}|\mathscr K_r-\mathscr K_1|\,d\Omega\\
&\le\frac1{4\pi\lambda}
 2\pi\int_0^\kappa36q^{-1/2}\,dq\\
&=\frac{36}{\lambda}\sqrt\kappa
\le90\sqrt\kappa.
\end{aligned}
\tag{21}
\]
したがって
\[
\boxed{A(\kappa)=90\sqrt\kappa\longrightarrow0.}
\]
q=0の一点は除外して積分し、右辺が有限なので絶対可積分性も確認できる。

## 5.3 補集合 \(q\ge\kappa\)

固定ξに対して、経路 \(p_s=sL_\lambda Q\) の速さは
\[
|p_s'|=|L_\lambda Q|\le1.
\]
(17)(18)から
\[
\left|\frac d{ds}F_{E,yy}(x,p_s)\right|
\le\frac{66}{D_s^2}
\le\frac{220}{q}.
\]
従って
\[
|\mathscr K_r-\mathscr K_1|
\le\frac{220(1-r)}q.
\tag{22}
\]
要求された点別形としては、q≥κで
\[
|\mathscr K_r-\mathscr K_1|
\le\frac{220}{\kappa}(1-r)
\]
も成立する。ただし積分時にはq依存を残した(22)が鋭い。

\[
\begin{aligned}
F_\kappa
&=\frac1{4\pi\lambda}
 \int_{q\ge\kappa}|\mathscr K_r-\mathscr K_1|\,d\Omega\\
&\le\frac1{4\pi\lambda}
 2\pi\int_\kappa^2\frac{220(1-r)}q\,dq\\
&=\frac{110}{\lambda}(1-r)\log\frac2\kappa\\
&\le275(1-r)\log\frac2\kappa.
\end{aligned}
\tag{23}
\]
したがって
\[
\boxed{B(\kappa)=275\log(2/\kappa).}
\]

近傍では核の絶対値だけを使い、微分は接触から離れた補集合でだけ使った。
\(|\partial_rH|\le C\) を全領域で仮定していない。

## 5.4 合成

(21)(23)を足すと(M)が得られる。全ての定数はτに依存せず、λについても指定範囲全体で共通である。軸τ=1、赤道τ=0も含む。ρやaによる除算は現れない。

# 6. 有理数のカラー幅

\[
\kappa=\frac1{100000000},\qquad \sqrt\kappa=\frac1{10000}.
\]
\[
2/\kappa=200000000<2^{28},\qquad \log2<\frac7{10}
\]
だから
\[
\log(2/\kappa)<28\cdot\frac7{10}=\frac{98}{5}.
\]
従って
\[
A(\kappa)=\frac9{1000},\qquad B(\kappa)\le5390.
\]

\[
\varepsilon=\frac1{60000}<\frac1{16}
\]
とすれば、全r∈[1−ε,1]について(18)の前提を満たし、
\[
|H(r)-H(1)|
\le\frac9{1000}+\frac{5390}{60000}
=\frac{593}{6000}.
\]
入力 \(H(1)\ge1/5\) より
\[
\boxed{
H(r)\ge\frac15-\frac{593}{6000}
=\frac{607}{6000}
=\frac1{10}+\frac7{6000}.
}
\]

\(\delta=1-r^2\) で表すと、この層は
\[
\boxed{
0\le\delta\le
\frac{119999}{3600000000}
}
\]
に等しい。r≥0を前提とした同値換算である。既存L3のδ₀やB7の区画定義を変更する指示ではない。

## 定量的一様連続性としての補足

(M)でκを深さdとともに動かしてよい。例えば
\[
\sqrt\kappa=\frac{55}{9}d
\]
とすれば、κ<2を満たす小さいdで
\[
|H(1-d)-H(1)|
\le550d+275d\log\frac{162}{3025d^2}.
\]
これは \(O(d\log(1/d))\) で0へ収束する。今回の具体幅は、この漸近表記ではなく、固定した有理κと有理数比較で証明した。

# 7. 接触点中心座標を内部へ拡張する方法

B′ v2と同じ
\[
e_1=(-b,0,a),\quad e_2=(0,1,0),\quad
e(\theta)=e_1\cos\theta+e_2\sin\theta,
\]
\[
\xi=Q\cos\psi+e(\theta)\sin\psi
\]
を使う。

角度の有理化変数を **\(u=\tan(\psi/4)\)** とすると
\[
s_h=\frac{2u}{1+u^2},\qquad c_h=\frac{1-u^2}{1+u^2},
\]
\[
q=2s_h^2=\frac{8u^2}{(1+u^2)^2},\qquad
\sin\psi=2s_hc_h,
\]
\[
\xi-rQ=(d-q)Q+\sin\psi\,e(\theta),
\]
\[
\boxed{
\sigma^2=d^2+\frac{16ru^2}{(1+u^2)^2},\qquad
h=\lambda\left(d+\frac{8ru^2}{(1+u^2)^2}\right).
}
\tag{24}
\]

w,nはξから、物理距離Dは \(L_\lambda(\xi-rQ)\) から構成する。γは同じh,w,Dから構成し、\(\gamma=n\cdot\omega\) の相関を使う。ηを別の区間変数にしない。

### 接触点での扱い

境界面r=1ではB′ v2が \(\sigma=4u/(1+u^2)\) を消去できる。一方、内部を含む(24)では、(d,u)=(0,0)に
\[
\sqrt{d^2+16ru^2/(1+u^2)^2}
\]
が現れる。境界面での正則化を、そのままr,uの共同正則性の証明として流用しない。

今回のPlan Aは、この点を一律に微分する代わりにq<κの積分を(21)で制御する。座標の利点は、特異点を同じ辺に固定でき、測度が \(dq\,d\theta\) となり、qに関する積分を厳密に実行できることである。

# 8. Dig／chatへの具体的な引継ぎ

## 8.1 この補題の確認に必要な作業

| 項目 | 検査内容 |
|---|---|
| 正典対応 | P1の \(F_E=h\arccos^2\gamma\)、\(dA/w=d\Omega\)、\(H=E_{yy}\) |
| 核の恒等式 | (10)をP1から独立に導出 |
| 境界正規化 | \(\mathscr K_1=2\lambda f\)、全球から半球への係数 |
| 幾何相関 | \(|\gamma\omega-n|^2=1-\gamma^2\)、(18) |
| 新定数 | \(9/D\)、\(66/D^2\) の各項の確認 |
| 積分 | 近傍90√κ、遠方275d log(2/κ) |
| 有理比較 | κ、ε、593/6000、607/6000、δ上端 |
| 範囲 | λ全帯、τ全域、r∈[59999/60000,1]、軸と接触点の扱い |

この補題案の数学的確認には、832箱の再計算や新しい大規模区間本走は必要ない。必要なのは新しい解析証明の独立照合である。既存の境界証拠を再認証したという扱いにはしない。

## 8.2 今回行った確認と限界

- 指定commitにあるB′仕様v1・v2差分、chat検収記録、Muse監査を取得して本文を確認。
- 同commitのP1とRoute B ledgerを読み、内部と境界の核を代数的に接続。
- 標準ライブラリの有理数・Laurent多項式演算で、P1微分式と(10)の差が**零多項式**になることを確認。
- 定数とカラー幅の全比較をFractionで確認。
- 既存QMの証明と監査記録は位置づけの比較に使用。QMの旧定数や監査状態を更新していない。
- Hの数値サンプリング、producer本走、独立verifier、Judge採用、GitHubへの書込みは行っていない。

## 8.3 採用後に得られる縮小範囲

新補題が正式採用された場合、D5の未解決集合から
\[
r\in[59999/60000,1]
\]
の一様な薄層を除ける。より内側の未解決部分は別課題である。D-OB全体の完了やB7の箱数変更をこの補題から主張しない。

# 9. Plan Bについての補助案

Plan Aで第一目標の薄層は構成できたため、その存在のためにPlan Bを実行する必要はない。さらに広いカラーが必要な場合には、同じ核と球冠分割が使える。

r≥15/16では、(14)(19)を内部核だけに適用して
\[
\frac1{4\pi\lambda}\int_{q<\kappa}|\mathscr K_r|\,d\Omega
\le45\sqrt\kappa
\]
を得る。従って
\[
\boxed{
H(r)\ge
\frac1{4\pi\lambda}\int_{q\ge\kappa}\mathscr K_r\,d\Omega
-45\sqrt\kappa.
}
\tag{25}
\]
補集合の符号付き積分を、r,τ,λを外側普遍量として直接下から包めばよい。ここでも \(\eta,\sigma,\delta\) の独立区間化を避ける。

これは追加設計の入口であり、切れているPlan B依頼文の未受領条件を補完するものではない。本走は開始していない。

# 付録A. 有理上界の根拠

## A.1 \(\pi<22/7\)

\[
\frac{22}{7}-\pi
=\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx>0.
\]
右辺の等式は多項式除算と \(\int_0^1(1+x^2)^{-1}dx=\pi/4\) で確認できる。

## A.2 \(\log2<7/10\)

\[
\log2
=2\sum_{j=0}^\infty\frac{(1/3)^{2j+1}}{2j+1}
\le\frac23+\frac23\sum_{j=1}^\infty(1/3)^{2j+1}
=\frac{25}{36}<\frac7{10}.
\]
従って、計算機の浮動小数のπやlogを証明入力に使わない。

# 付録B. 固定した一次資料

Repository: `cotaxxxx/bg-oblate-spheroid`  
Branch: `design/d-ob-p2`  
取得基準commit: `8da3174f847fd4e9fd58ceaf1cd613b66b72fde4`

| 資料（commit固定リンク） | Git blob SHA | 内容SHA256 |
|---|---|---|
| [D5_BOUNDARY_FACE_BPRIME_SPEC_20261106.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/D5_BPRIME_V2_20261107/D5_BOUNDARY_FACE_BPRIME_SPEC_20261106.md) | bdf779c00ef1537d8433f7ed40dd649dee1065fe | d97d7cbb4e1101d85214506e81db978b0c96989bac96563e79e556af5dedf532 |
| [D5_BOUNDARY_FACE_BPRIME_SPEC_V2_DELTA_20261107.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/D5_BPRIME_V2_20261107/D5_BOUNDARY_FACE_BPRIME_SPEC_V2_DELTA_20261107.md) | 91ba50f6ef0646c81d77028070734efd39e5925a | 2d27f944e2a8f6890d37ea0d4883f06a8e83fc250c62568bc10e936451b7ec27 |
| [CHAT_ACCEPTANCE_D5_BPRIME_V2_FACE_20261107.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/D5_BPRIME_V2_20261107/CHAT_ACCEPTANCE_D5_BPRIME_V2_FACE_20261107.md) | 3e01d51474b9900a17f14786cd24272894cf8351 | f0b11a64925089142a713bba0ab96181415d6a6bfa06b446d2d9d30ac35a480c |
| [MUSE_AUDIT_D5_BPRIME_V2_VERIFIER_20261107.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/D5_BPRIME_V2_20261107/MUSE_AUDIT_D5_BPRIME_V2_VERIFIER_20261107.md) | 110418a036b21ed6f6b3b2e61ce8f7f917630108 | 7e5997a059abfc92061514c6d4d90bfa3a93365ee5b3e5286c10ad5d85dbb033 |
| [D_OB_P1_DESIGN_NOTE.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/D_OB_P1_DESIGN_NOTE.md) | f81e120e44a866d206117d4fab5fac627f26ccd1 | 2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9 |
| [L1_R0_COMPACT_AND_KERNEL_DOMAIN_LEDGER_V0.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/L1_R0_COMPACT_AND_KERNEL_DOMAIN_LEDGER_V0.md) | 029728ef8e331bc1777d3670feccc00e3aa3a6b6 | da36508507015ed968c4a386fdcc2becb6523408fea078faba16e840fda868e6 |
| [D_OB_P2_D_AN1_QM_DRAFT.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/D_OB_P2_D_AN1_QM_DRAFT.md) | 7e99ce86914df0ef3fc1eda21885fcd9a2ca722f | e8588c1b677e10aceac22e79784e41111cffe2c2cffce1636804485dafb09edc |
| [CHAT_AUDIT_D_AN1_QM_PROOF_SCOPE_2026-10-18.md](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/8da3174f847fd4e9fd58ceaf1cd613b66b72fde4/analysis/CHAT_AUDIT_D_AN1_QM_PROOF_SCOPE_2026-10-18.md) | a78ba2c975a0261368631c1fcbf029a322f9400c | 03e55f9f91b876b73ac01526db551f13d18ed5ed98e3efbfd7c00a93b8de3b87 |

B′採用記録の定理 \(H(1)\ge1/5\) を入力としている。producer最小値約0.2642やverifier最小値約0.3205を、勝手に境界定理の新しい余裕へ置き換えていない。

P1・QM文書内の古い工程ステータスは、その文書時点の記録として読む。本稿は依頼者から提示された2026年11月8日の工程状態を上書きしない。

# 付録C. 厳密代数・算術確認

以下は紙上証明の計算補助であり、独立監査やカラー証明書ではない。

```json
{
  "status": "EXACT_PAPER_ALGEBRA_CHECKS_ONLY_NOT_CERTIFICATE_OR_AUDIT",
  "directional_kernel_laurent_identity": "zero polynomial",
  "pi_upper_integral_identity": "exact",
  "C2": "9",
  "C3": "66",
  "A_coefficient": "90",
  "B_log_coefficient": "275",
  "kappa": "1/100000000",
  "epsilon": "1/60000",
  "A": "9/1000",
  "B_rational_upper": "5390",
  "error_upper": "593/6000",
  "H_lower_from_boundary_input": "607/6000",
  "delta_max": "119999/3600000000",
  "not_run": [
    "H numerical sampling",
    "production",
    "independent verifier",
    "Judge adoption"
  ]
}
```

## C.1 check_collar_algebra.py

```python
"""Exact algebra and rational-constant checks for a paper lemma.
No quadrature, positivity sampling, certificate run, or independent audit.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib

# Laurent polynomials in g,T,n,R,Rp,w,D; D is strictly positive.
NV=7
def const(x): return {(0,)*NV:F(x)} if x else {}
def var(i,power=1):
    e=[0]*NV;e[i]=power
    return {tuple(e):F(1)}
def add(*ps):
    r={}
    for p in ps:
        for e,v in p.items():r[e]=r.get(e,F(0))+v
    return {e:v for e,v in r.items() if v}
def mul(*ps):
    r=const(1)
    for p in ps:
        z={}
        for e,a in r.items():
            for f,b in p.items():
                h=tuple(x+y for x,y in zip(e,f));z[h]=z.get(h,F(0))+a*b
        r={e:v for e,v in z.items() if v}
    return r
def scale(p,a):return mul(const(a),p)
def neg(p):return scale(p,-1)
g,T,n,R,Rp,w,D=[var(i) for i in range(NV)]
invD=var(6,-1)
e=add(mul(g,T),neg(n))
gy=mul(e,invD)
gyy=mul(add(scale(mul(e,T),2),neg(mul(g,add(const(1),neg(mul(T,T)))))),invD,invD)
h=mul(w,D,g);hy=neg(mul(w,n))
direct=add(scale(mul(hy,R,gy),-4),scale(mul(h,Rp,gy,gy),-2),scale(mul(h,R,gyy),-2))
S=add(mul(g,g,add(const(1),neg(mul(T,T)))),scale(mul(e,e),-2))
compact=scale(mul(w,invD,add(mul(R,S),neg(mul(g,Rp,e,e)))),2)
assert not add(direct,neg(compact))

# Exact polynomial division proving integral x^4(1-x)^4/(1+x^2) = 22/7-pi.
poly=[F(0)]*9
for k,a in enumerate([1,-4,6,-4,1],4):poly[k]=F(a)
quot=[F(0)]*7
for k in range(8,1,-1):
    a=poly[k];quot[k-2]=a;poly[k]-=a;poly[k-2]-=a
assert poly[0]==-4 and all(v==0 for v in poly[1:])
assert sum((v/F(i+1) for i,v in enumerate(quot)),F(0))==F(22,7)

pi_upper=F(22,7)
C2=F(9);C3=F(66)
assert 2*pi_upper+2<C2
assert F(32,15)<3
assert 2*((pi_upper+1)+(10+6*pi_upper))==C3
assert F(25,36)<F(7,10) # atanh series bound for log 2
m=F(2,5);r0=F(15,16)
assert 2*r0*m*m==F(3,10)
assert F(3,10)>F(1,4)
near_coefficient=2*C2/(m*F(1,2));far_coefficient=C3/(2*m*F(3,10))
assert near_coefficient==90 and far_coefficient==275
kappa=F(1,100000000);sqrt_kappa=F(1,10000);epsilon=F(1,60000)
assert sqrt_kappa**2==kappa and 1-epsilon>=r0
assert 2/kappa<2**28
log_upper=28*F(7,10)
A=near_coefficient*sqrt_kappa;B=far_coefficient*log_upper
error=A+B*epsilon;lower=F(1,5)-error
assert A==F(9,1000) and B==5390
assert error==F(593,6000)<F(1,10)
assert lower==F(607,6000)>F(1,10)
result={'status':'EXACT_PAPER_ALGEBRA_CHECKS_ONLY_NOT_CERTIFICATE_OR_AUDIT',
        'directional_kernel_laurent_identity':'zero polynomial',
        'pi_upper_integral_identity':'exact',
        'C2':str(C2),'C3':str(C3),'A_coefficient':str(near_coefficient),
        'B_log_coefficient':str(far_coefficient),'kappa':str(kappa),'epsilon':str(epsilon),
        'A':str(A),'B_rational_upper':str(B),'error_upper':str(error),
        'H_lower_from_boundary_input':str(lower),'delta_max':str(2*epsilon-epsilon**2),
        'not_run':['H numerical sampling','production','independent verifier','Judge adoption']}
p=Path(__file__).with_name('collar_algebra_result.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
```

