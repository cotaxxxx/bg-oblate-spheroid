# D-OB P2 / FT_q Boundary Pair Lemma — 証明書39′の独立検証

検証日：2026-10-08。判定：**PARTIALLY PROVED**。

本書の新しい命題は、提示された FT_q 対称分解、\(1\leq\bar R\leq\pi/2\)、\(-1\leq\kappa_R\leq0\) を前提とする数学的証明である。元の FT_q reduction 全体を再認証するものではない。核の既存下界 \(207/5000\) は今回の依頼で指定された入力として使用する。正式台帳の CLOSED 更新は行わない。

## A. 結論

1. **元の \(\beta\) による \(\mu^\dagger=2/5\) は反証される。** 実際、\(\mu=1/4\) では全パラメータについて \(\beta<0\)。さらに \(\lambda=93/200,\ m=112/113,\rho=15/113,\mu=1/8192\) に exact な反例がある。
2. **元の \(\beta\) でも短い区間では正質量を証明できる。** \([-1/4,-1/8]\) で \(\beta>81/1750\)、その積分寄与は \(1/1000\) より大きい。
3. **別の評価で、南側 \(J=(-1/4,\mu_C)\) 全体の点ごとの正寄与を証明できる。** 有利な \(B_1q\) と secant の平方構造を保持すると
   \[
   \boxed{-\frac{F}{S_3}\geq[-C_0(\mu)]\sin^2\phi+\frac{3}{200}\cos^2\phi>0}
   \quad(\mu\in J)
   \]
   が成立する。したがって \(G(\mu)>0\) である。
4. この別経路では、当初の区間 \((-1/4,2/5)\) に対して
   \[
   \boxed{\int_{-1/4}^{2/5}G(\mu)\,d\mu>\frac18}
   \]
   を得る。残りの南側にも負の損失は不要であり、新しい証明の採用後は \(U_{\rm south,rem}=0\) とできる。
5. **全体認証は未完成。** 残る十分条件は
   \[
   U_{\rm north}+U_{\rm near}<\frac{207}{5000}+\frac18=\boxed{\frac{104}{625}}.
   \]
   この上界は本検証では証明していない。Boundary Pair Lemma は OPEN、D-P2 は NOT_CERTIFIED のままである。

## B. 反例探索と exact な確定

### B1. 探索と証明の区別

最初に、\(\lambda\in\{2/5,93/200\}\)、\(\tau\in\{7/8,1\}\)、\(\mu\in\{-1/4,-1/8,-1/16,0,1/8,1/4,3/8,2/5\}\) を診断し、正値性が失われる候補を探した。その後 \(\mu=1/8192\) を追加した。この有限標本は全域証明ではない。浮動小数点探索は添付コードの `--diagnostic` に分離し、NOT_EVIDENCE として出力する。

以下の反証には浮動小数点値を使用しない。また、\(\beta<0\) は \(G<0\) を意味しない。本書では逆に \(G>0\) を証明する。

### B2. \(\mu=1/4\) は全パラメータで反例

以下、\(B=B_1,\ C=C_0,\ M_E=m(1-\mu^2)\) と略記し、
\[
P_+=\int_0^\pi E_+\,d\phi,\qquad
\widetilde g=\frac{M_E}{2}+C
\]
とする。\(\int E_-=P_+-\pi\widetilde g\) である。

\(\mu=1/4\) において
\[
\partial_L\widetilde g=(m-\mu)(1-\mu^2)>0,
\quad
\partial_m\widetilde g=-\left(\frac12-L\right)-\left(\frac12+L\right)\mu^2<0.
\]
よって
\[
\widetilde g\geq\widetilde g(4/25,1,1/4)=\frac{21}{320}.
\]
ここでは \(B<0\) なので \(B_+=0\)。\(w_{\max}\geq w_{\min}>0\) と \(\pi/2>1\) より
\[
\begin{aligned}
\beta
&=\left(w_{\min}-\frac\pi2w_{\max}\right)P_+
 -\pi w_{\min}\widetilde g-\frac\pi{10}w_{\max}\\
&\leq-\frac{53\pi}{320}w_{\min}<0.
\end{aligned}
\]
後述する \(C(2/5)<0\) の一様評価により、\(\mu=1/4\) は全パラメータで確かに \(J\) 内にある。

### B3. さらに小さい有理点での反例

\[
(\lambda,\tau,m,\rho,\mu)
=\left(\frac{93}{200},\frac78,\frac{112}{113},\frac{15}{113},\frac1{8192}\right).
\]
有理区間演算で
\[
\boxed{-\frac{47419}{100000000}\leq\beta\leq-\frac{23709}{50000000}<0}
\]
を確認した。同じパラメータの \(\mu=0\) では
\[
\frac{38717}{50000000}\leq\beta(0)\leq\frac{15487}{20000000}>0.
\]
従って、この点を含む正の有理端点への一様 \(\beta>0\) 拡張はできない。連続性により、端点をちょうど \(1/8192\) とした開区間にも反例が入る。最適な切断点の探索・認証は行っていない。

平方根は整数平方根による上下有理近似、\(\arctan\) は交代級数、\(\pi\) は Machin の恒等式で囲んだ。方法は C6 と添付コードに記す。

## C. exact に成立した不等式と証明

### C1. 共通領域と幾何学的評価

\[
\mathcal B=\left[\frac4{25},\frac{8649}{40000}\right]
\times\left[\frac{112}{113},1\right]
\times\left[-\frac14,\frac35\right]
\]
を \((L,m,\mu)\) の順で使用する。\(r=\rho^2=1-m^2\) とし、独立変数としての \(\rho\) に領域を拡張しない。\(\phi\) の全域は \(0\leq q\leq a^2\) で扱う。

\(h=1-m\mu\)、\(s=m-\mu\) とおく。\(d_L=s^2>0\)、
\[
d_m=-2[(1-L)m+L\mu]<0.
\]
最後の括弧は、例えば \(L<1/4,m\geq112/113,\mu\geq-1/4\) から \((3/4)(112/113)-1/16>0\)。\(d\) は \(\mu\) の凹二次式だから、最小値の候補は区間端点である。従って
\[
d\geq\min\left\{d\left(\frac4{25},1,-\frac14\right),
d\left(\frac4{25},1,\frac35\right)\right\}
=\min\left\{\frac{19}{16},\frac{416}{625}\right\}=\frac{416}{625}.
\]
一方、平方完成すると
\[
d=2-\frac{1-2L}{1-L}m^2
 -(1-L)\left(\mu+\frac{Lm}{1-L}\right)^2.
\]
\(L<2/9\)、\(m^2>49/50\) より
\[
d<2-\frac57\frac{49}{50}=\frac{13}{10}.
\]

\(v^2=d^2-4rq\) から
\[
\frac{4rq}{d^2}\leq
\frac{4(225/12769)}{(416/625)^2}
=\frac{87890625}{552438016}<\frac{23}{144},
\qquad \frac vd>\frac{11}{12}.
\]
\(t=v/d\) とすれば
\[
\theta d=\psi(t)=\frac{2(2+t)}{(1+t)(2-t)},\qquad
\psi'(t)=\frac{2t(t+4)}{(1+t)^2(2-t)^2}\geq0.
\]
従って、\(0<t\leq1\) を使い
\[
\boxed{\frac{14}{5d}<\theta\leq\frac3d},
\qquad \psi(11/12)=\frac{840}{299}>\frac{14}{5}.
\]

必要な補助結果も次のように確認できる。\(J\) で
\[
C'>\frac{23}{25}-\frac{11L}{5}
\geq\frac{88861}{200000}>\frac25,
\quad -\frac32<C<0,\quad -\frac32<E<1.
\]
また \(a^2>16/25\)、\(h>2/5\)、
\[
v^2\geq(a^2-r)^2,\quad
v>\frac35,\quad u^2=2(d+v)>\frac{62}{25},\quad u>\frac32.
\]
これらは \(\rho=0\) においても有効である。

### C2. 元の \(\beta\) が正となる短区間

\(J_0=[-1/4,-1/8]\) では \(g=ma^2+C\) は \(L,m,\mu\) のそれぞれについて増加する。実際、\(g_L=sa^2>0\)、\(g_\mu=C'-2m\mu>0\)、
\[
g_m=L-(1+L)\mu^2\geq\frac4{25}-\frac{1+8649/40000}{16}>0.
\]
したがって
\[
E\leq g\leq g(8649/40000,1,-1/8)
=-\frac{496017}{20480000}<0.
\]
ゆえに \(\int E_+=0\)。同様に \(-C-ma^2/2\) の単調性を用いると
\[
-C-\frac{ma^2}{2}\geq
\frac{1189049017}{2314240000}>\frac12.
\]
ここでは、\(\mu\) 微分が \(-C'+m\mu<0\)、\(L\) 微分が \(-sa^2<0\)、\(m\) 微分が \((1/2-L)+(L+1/2)\mu^2>0\) なので、最小値は \((L,m,\mu)=(8649/40000,112/113,-1/8)\) である。

\(B_L=-sh<0\)、\(B_\mu<0\)、\(B_m<0\) がこの区間で成立する。後二者は
\[
B_\mu=2m(1-L)\mu+((1+L)m^2+L-2)<0,
\]
\[
B_m=(1-L)\mu^2+2(1+L)m\mu-L
\leq\frac{21}{400}-\frac4{25}<0
\]
から従う。したがって
\[
B_+\leq\frac{43773}{638450}<\frac7{100}.
\]
\(d\) のパラメータ単調性と \(\mu\) の凹性から、両端を比較して
\[
d\geq\frac{1899}{1600}>\frac{59}{50}>\frac76,
\quad \theta<\frac{18}{7},
\quad \int_0^\pi\theta B_+q\,d\phi\leq\frac{9\pi}{100}.
\]
さらに \(2\rho a\leq30/113\) から
\[
\left(\frac{w_{\max}}{w_{\min}}\right)^2
\leq\left(\frac{8167}{5167}\right)^3<4.
\]
\(d+2\rho a<13/10+3/10=8/5\) と \((8/5)^3<400/81\) より \(w_{\min}>9/10\)。従って
\[
\begin{aligned}
\frac{\beta}{\pi w_{\min}}
&>\frac12-2\left(\frac{11}{7}\frac9{100}+\frac1{10}\right)
=\frac3{175},\\
\beta&>3\frac9{10}\frac3{175}=\frac{81}{1750}.
\end{aligned}
\]
外側係数は
\[
\frac{Ls}{w}\geq\frac4{25}\left(\frac{112}{113}+\frac18\right)
=\frac{1009}{5650}>\frac7{40}.
\]
よって
\[
\boxed{\int_{-1/4}^{-1/8}G\,d\mu>
\frac18\frac7{40}\frac{81}{1750}
=\frac{81}{80000}>\frac1{1000}}.
\]
これは元の \(\beta\) による質問①②への、短区間での肯定的回答である。

### C3. secant の相関を保持した新しい評価

次を定義する。
\[
c_*=h-d,\quad T=(1-L)m-(2-L)\mu,\quad
Y=hc_*+rq,
\]
\[
Z=T-\frac{mq}{h}+\theta E,\qquad
M=hu-\frac{4rq}{u}.
\]
直接展開で
\[
B=mc_*+rT,\quad C+hT=\mu(L-1)s^2,
\quad \frac{K_R}{S_3}=B+\theta rE=\frac mhY+rZ.
\]
これらの恒等式は添付コードで記号的にゼロを確認する。

以前の定義 \(h_\pm=\lambda(h\mp\rho b)\)、\(\gamma_\pm=h_\pm/(wD_\pm)\) を用いる。\(D_+-D_-=-4\rho b/u\) より
\[
h_+D_-+h_-D_+=\lambda M.
\]
有限差分式の \(X=L Y\) を代入すると
\[
\frac{b\Delta R}{\rho}=\frac{2\kappa_R\lambda qY}{wvM}.
\]
従って、\(\mathcal A=E+\theta Bq\) と書けば
\[
\boxed{\frac F{S_3}=\bar R\mathcal A+
\frac{2\kappa_R\lambda q}{wvM}
Y\left(\frac mhY+rZ\right)}.
\]
この式は \(\rho\) による除算を含まず、\(\rho=0\) に連続延長できる。

平方完成
\[
Y\left(\frac mhY+rZ\right)
=\frac mh\left(Y+\frac{rhZ}{2m}\right)^2-
\frac{r^2hZ^2}{4m}
\]
と \(-1\leq\kappa_R\leq0\) により、secant 項の敵対寄与は
\[
J_{\rm sec}=\frac{\lambda q r^2hZ^2}{2mwvM}
\]
以下である。ここには \(E<0\) の仮定はない。

\(-2<T<13/10\)、\(0\leq mq/h<5/2\)、\(\theta<75/16\)、\(-3/2<E<1\) から
\[
-\frac{369}{32}<Z<\frac{479}{80},\qquad |Z|<12.
\]
さらに
\[
\frac{4rq}{hu^2}<\frac{28125}{395839}<\frac1{14},
\quad M>\frac{13}{14}hu.
\]
ここで **\(h\) を約分してから** 評価する。\(\lambda/w\leq1\) を使うと
\[
J_{\rm sec}\leq
\frac{7q r^2 Z^2}{13mvu}
\leq\frac{506250}{18757661}q
<\frac{27}{1000}q<\frac3{100}q\quad(q>0).
\]
\(q=0\) では secant 項はゼロであるから、一様に
\[
\boxed{\frac F{S_3}\leq\bar R\mathcal A+\frac3{100}q}.
\]
旧一様定数 \(1/10\) より小さいだけでなく、\(q\) 因子を残したことが次の補間に必要である。

### C4. 144 個の正 Bernstein 係数による南側符号補題

\(\varepsilon=3/100\)、\(\eta=3/200\) とし、二つの多項式
\[
\Pi_t=-(g+\varepsilon a^2)d-tBa^2,
\qquad t\in\left\{3,\frac{14}{5}\right\}
\]
を考える。C1 の箱 \(\mathcal B\) を
\[
L=\frac4{25}+\frac{2249}{40000}z_0,\quad
m=\frac{112+z_1}{113},\quad
\mu=-\frac14+\frac{17}{20}z_2,\quad 0\leq z_i\leq1
\]
で単位立方体へ移す。

各多項式の多重次数は \((2,3,5)\)。テンソル Bernstein 基底で表した全係数は正で、最小係数は次のとおりである。

| 多項式 | 係数数 | 最小係数 | 最小係数の添字 |
|---|---:|---:|---|
| \(\Pi_3\) | 72 | \(106592/1953125\) | \((0,3,5)\) |
| \(\Pi_{14/5}\) | 72 | \(40192/1953125\) | \((0,3,5)\) |

全144係数は `certificate39prime_coefficients.json` に収録する。係数生成には、変換後の冪基底係数を \(p_j\)、多重次数を \(n\) として
\[
\beta_k=\sum_{j\leq k}p_j
\prod_{i=0}^2\frac{\binom{k_i}{j_i}}{\binom{n_i}{j_i}}
\]
を用いる。コードは係数の正値性だけでなく、元の多項式への再構成も厳密に検査する。Bernstein 基底は非負で和が1だから、箱全体で最小係数が下界になる。

\[
\frac{40192}{1953125}-\frac{39}{2000}
=\frac{33697}{31250000}>0,
\qquad \eta d<\frac3{200}\frac{13}{10}=\frac{39}{2000}.
\]
従って双方について \(\Pi_t/d>\eta\)。

ここで \(z=q/a^2=\cos^2\phi\) とする。\(B\geq0\) なら \(t=3\)、\(B<0\) なら \(t=14/5\) を選ぶ。C1 の \(\theta\) の両側評価により、いずれの場合も
\[
\begin{aligned}
\mathcal A+\varepsilon q
&\leq C+q\left(m+\varepsilon+\frac{tB}{d}\right)\\
&=(1-z)C-z\frac{\Pi_t}{d}\\
&\leq(1-z)C-\eta z<0\qquad(\mu\in J).
\end{aligned}
\]
最後は \(C<0\)、\(0\leq z\leq1\)、\(\eta>0\) による。よって \(\mathcal A<0\)。\(\bar R\geq1\) と C3 から
\[
\frac F{S_3}\leq\bar R\mathcal A+\varepsilon q
\leq\mathcal A+\varepsilon q
\leq C(1-z)-\eta z.
\]
すなわち
\[
\boxed{-\frac F{S_3}\geq[-C]\sin^2\phi+\frac3{200}\cos^2\phi>0\quad\text{on }J.}
\]
\(B=0\)、\(E=0\)、\(q=0\) を除外していない。\(\rho=0\) でも C3 の非特異な式により有効。\(\mu=\mu_C\) では右辺の \(-C\) はゼロになるが、角度積分はなお正である。

### C5. 正の積分質量 \(C_{\rm core}=1/8\)

\(x=2\rho b\) に関して \((d-x)^{-3/2}+(d+x)^{-3/2}\) は \(x=0\) で最小なので
\[
H_w:=\frac{S_3}{v^3}=D_+^{-3}+D_-^{-3}
\geq2d^{-3/2}>\frac54.
\]
最後の比較は \(d<13/10\) と \((13/10)^3<64/25\) による。\(w\leq1\) より
\[
\frac{Ls}{w}\geq\frac4{25}\left(\frac{112}{113}-\mu\right)>0.
\]
C4 を角度積分し、\(\int_0^\pi\sin^2\phi\,d\phi=\int_0^\pi\cos^2\phi\,d\phi=\pi/2\) を使うと
\[
\boxed{G(\mu)>\frac\pi{10}\left(\frac{112}{113}-\mu\right)
\left[-C(\mu)+\frac3{200}\right]>0.}
\]

\(C_L=sa^2>0\)、\(C_m=-L\mu^2-(1-L)<0\) より
\[
C(\mu)\leq C_*(\mu):=C\left(\frac{8649}{40000},\frac{112}{113},\mu\right),
\]
\[
C_*(\mu)=-\frac{31351}{40000}\mu^3
-\frac{60543}{282500}\mu^2
+\frac{71351}{40000}\mu-\frac{219457}{282500}.
\]
\[
C_*(2/5)=-\frac{41747957}{282500000}<0.
\]
\(C\) は増加するため、一様に \(2/5<\mu_C\)。従って \(\pi>3\) を使い
\[
\begin{aligned}
\int_{-1/4}^{2/5}G(\mu)\,d\mu
&>\frac3{10}\int_{-1/4}^{2/5}
\left(\frac{112}{113}-\mu\right)
\left[-C_*(\mu)+\frac3{200}\right]d\mu\\
&=\frac{10778024217619399}{81721600000000000}
>\boxed{\frac18}.
\end{aligned}
\]
これは有理係数多項式の厳密積分であり、数値求積を用いない。

なお依頼文の外側係数について
\[
\frac4{25}\left(\frac{112}{113}-\frac25\right)
=\frac{1336}{14125}>\frac{884}{14125}.
\]
提示された \(884/14125\) は**有効だが弱い下界**であり、誤った不等式ではない。\(884/14125\) は端点 \(3/5\) を代入した値である。

### C6. 方位角正部分を有理数で囲む方法

\(M_E=ma^2>0\)、\(k=-C/M_E>0\) とする。正規化した関数
\[
\Phi(k)=\int_0^\pi(\cos^2\phi-k)_+\,d\phi
\]
は \(0<k<1\) で
\[
\Phi(k)=(1-2k)\alpha+\sqrt{k(1-k)},\qquad
\alpha=\arccos\sqrt{k},\quad \Phi'(k)=-2\alpha<0.
\]
\(k\geq1\) ではゼロ、\(\Phi(0)=\pi/2\)、\(\Phi(1/2)=1/2\) である。\(\int E_+=M_E\Phi(k)\)。この微分は \(M_E\) を固定した正規化変数での微分であって、\(\mu\) に沿う全微分を主張していない。

有理区間 \(0<M_-\leq M_E\leq M_+\)、\(C_-\leq C\leq C_+<0\) に対して
\[
k_-=\frac{-C_+}{M_+}\leq k\leq\frac{-C_-}{M_-}=k_+,
\]
\[
M_-\Phi(k_+)\leq\int E_+\leq M_+\Phi(k_-).
\]
従って \(k(\mu)\) 自体の単調性を仮定する必要はない。

有理数 \(x\geq0\) に対する平方根包絡は、\(N=10^{32}\)、\(n=\lfloor N\sqrt{x}\rfloor\) を整数平方根で求め、\(n/N\leq\sqrt{x}\leq(n+1)/N\) とする。両端の二乗で包含を再検査する。

\(0\leq z\leq1\) に対して
\[
S_{96}(z)\leq\arctan z\leq S_{97}(z),\qquad
S_N(z)=\sum_{j=0}^{N-1}\frac{(-1)^jz^{2j+1}}{2j+1}.
\]
\(k\geq1/2\) なら \(\alpha=\arctan\sqrt{(1-k)/k}\)、\(k<1/2\) なら \(\alpha=\pi/2-\arctan\sqrt{k/(1-k)}\) を使用する。
\[
\pi=16\arctan(1/5)-4\arctan(1/239)
\]
も同じ方法で囲む。係数 \(1-2k\) の符号を考慮する区間積で \(\Phi\) を計算する。これにより \(3<\pi<22/7\) も有理数比較で確認する。

全パラメータ箱を保った \(\mu\) 分割による \(\int E_+\) の例は次のとおり。表示した上下端はすべて外向きに丸めた**有理数**であり、浮動小数点近似ではない。

| \(\mu\) 区間 | 下界 | 上界 |
|---|---:|---:|
| \([-1/4,-1/8]\) | \(0\) | \(0\) |
| \([-1/8,0]\) | \(0\) | \(2879/20000\) |
| \([0,1/8]\) | \(68433/1000000\) | \(411177/1000000\) |
| \([1/8,1/4]\) | \(126993/500000\) | \(724083/1000000\) |
| \([1/4,2/5]\) | \(437159/1000000\) | \(67993/62500\) |

この表は角度積分包絡の構成例であり、C4–C5 の強い正値性証明には使用していない。各箱の \(M_E,C,k\) の端点も JSON に記録した。

### C7. 評価損失の切り分け

最も決定的なのは、質問に列挙された定数の大小だけでなく、**\(B<0\) の有利な項をゼロに置き換えたこと**である。\(\mu=1/4\) では \(B_+=0\) にもかかわらず \(\beta<0\)。さらに、仮に重み比の損失を1、\(\bar R\) を1、secant の敵対寄与を0としても、\(E\) だけの評価は
\[
w_0\left(\int E_- -\int E_+\right)
=-\pi w_0\widetilde g<0\quad(w_0>0)
\]
となる。この地点では、これらの定数改善だけで \(E\) 単独経路を正にすることはできない。

各損失への exact な改善は次のとおりである。

| 損失 | 改善 |
|---|---|
| \(w_{\max}/w_{\min}\) | 対を保持すると \(2d^{-3/2}\leq H_w\leq(w_{\max}+w_{\min})/2\)。偶関数 \((d-x)^{-3/2}+(d+x)^{-3/2}\) が \(x\geq0\) で増加することによる。 |
| \(\bar R\leq\pi/2\) | \(\mathcal A<0\) を先に示せば、\(\bar R\mathcal A\leq\mathcal A\)。C4 では上界 \(\pi/2\) を使わない。 |
| \(J_{\rm sec}<1/10\) | \(h/M\) の約分と \(q\) の保持で \(J_{\rm sec}\leq(506250/18757661)q<(3/100)q\)（\(q>0\)）。 |
| \(B_+\) | \([-1/4,-1/8]\) でだけ正になり得る。符号別に \(\theta\) の両側評価を使えば、有利な \(B<0\) も保持できる。 |

参考として B3 と同じパラメータ、\(\mu=0\) における元の \(\beta\) の項別区間は次のとおり。

| 項 | exact 有理区間 |
|---|---|
| \(w_{\min}\int E_-\) | \([55748589/50000000,\ 111497179/100000000]\) |
| \((\pi/2)w_{\max}\int E_+\) | \([11273069/25000000,\ 45092277/100000000]\) |
| \((\pi/10)w_{\max}\) | \([66327467/100000000,\ 16581867/25000000]\) |

この地点では旧 secant 包絡が大きく、残る差が小さい。ただし一点での大小を、全領域での損失順位と解釈してはならない。

W-16 については
\[
1+\frac{75}{16}\frac54=\frac{439}{64},\qquad
\frac{11}{7}\frac{439}{64}+\frac1{10}<11
\]
を確認した。\(437/64\) は誤記で、訂正後も粗い \(f<11\) は維持される。出典ファイル自体は変更していない。

## D. 未証明部分と正式状態

本書の南側符号補題を独立監査で採用した場合、
\[
C_{\rm core}=\frac18,\qquad U_{\rm south,rem}=0
\]
が使用可能になる。残る全体予算は
\[
\frac{104}{625}-U_{\rm north}-U_{\rm near}>0.
\]
不足しているのは、この予算内に収まる **全パラメータで一様な北側・近傍の片側上界** と、その分割の被覆・重複・退化極限を含む結合証明である。本書はこれらの上界、正の最終 gap、\(c_{FT}\)、\(m_0\)、L3、L1 を与えない。

「南側が正」と「全積分が正」は別の命題である。旧下界 \(-221\) が不十分だったことも、全体の反例を意味しない。本書の結果から日数・完成率・最終閉包の確率は推定しない。

正式台帳は依頼文のまま保持する：20″ CLOSED / 35–38 CHAT AUDIT PASS / 39 OPEN / 40 CHAT AUDIT PASS（粗い評価）/ W-16 訂正待ち / 39′ NEXT / 21″ OPEN / U OPEN / \(c_{FT}\) UNSET / Boundary Pair Lemma OPEN / \(m_0\) UNAVAILABLE / L3 BLOCKED / L1 PAUSED / D-P2 NOT_CERTIFIED。

新規成果は「39′独立証明候補：本書と exact 計算を提出、別監査待ち」として追加できる。正式 CLOSED への昇格は本書から自動的には行わない。

## E. 推奨する次の一手

**最小の次単位は、本書 C4 の南側符号補題の独立監査・採否判定とする。** 対象を
\[
-F/S_3\geq[-C_0]\sin^2\phi+(3/200)\cos^2\phi
\]
の一命題に限定し、(i) secant 平方完成と \(h/M\) の約分、(ii) 全144 Bernstein 係数、(iii) \(B\) の符号による \(\theta\) の使い分け、を照合する。

この一命題が採用されれば、C5 の有理多項式積分は機械的に再現でき、南側の負残差が除去される。以後の解析を、残る北側・近傍の合計損失 \(<104/625\) の証明に集中できる。元の \(\beta\) の端点を \(2/5\) まで伸ばす試みは、反例があるため中止すべきである。

## F. 独立検証用資料と provenance

### F1. 再現手順

同梱のファイル：

- `certificate39prime_exact.py`：整数・有理数・記号多項式による検査コード。
- `certificate39prime_coefficients.json`：144係数、最小係数、反例の有理区間、角度積分の箱、積分定数、未証明項目。
- 本報告書：コードだけでは表現していない解析的推論と依存関係。

SymPy 1.14.0 / Python 3 で実行した。標準実行に浮動小数点計算や数値求積は含まれない。

```bash
python certificate39prime_exact.py --write-certificate reproduced_coefficients.json
```

標準出力には次が含まれる。

```text
EXACT ALGEBRA CHECKS: PASS
Pi_3: degree [2, 3, 5] coefficients 72 minimum 106592/1953125
Pi_14/5: degree [2, 3, 5] coefficients 72 minimum 40192/1953125
beta(0) interval: ['38717/50000000', '15487/20000000']
beta(1/8192) interval: ['-47419/100000000', '-23709/50000000']
Original beta positive on [-1/4,-1/8]; mass >1/1000.
Alternative analytic proof: G>0 on J; core mass >1/8.
Remaining required budget: U_north+U_near <104/625; UNPROVED.
```

探索を再現する場合のみ `python certificate39prime_exact.py --diagnostic` を用いる。このモードは証明モードと別であり、出力に NOT_EVIDENCE が付く。

生成時 SHA-256：

| ファイル | SHA-256 |
|---|---|
| `certificate39prime_exact.py` | `4b51bd9b57bb83c40737f6c10ce61fab736ed08334f29ed430a5825d8b0d8888` |
| `certificate39prime_coefficients.json` | `853d022e0fa8720a99f34a81b5ff5664e0c2c6f6fa6fa2e6fdccc78fe4d40a80` |

### F2. 照合した出典

依頼文に記載された最新の監査状態を採用する。出典の draft 表記は履歴上の表記であり、それだけを根拠に最新台帳を戻したり昇格したりしない。今回読んだ原文は以下の commit に固定した。同 commit を指定した再取得で、内容と Git blob SHA の一致を確認した。

Repository: `cotaxxxx/bg-oblate-spheroid`。Commit: `69e104602e939817b6f4d71df3f6bd63cbc729e0`。

| 原文 | Git blob SHA | 今回の利用範囲 |
|---|---|---|
| `D_OB_P2_D_AN1_FT_Q_EXTERIOR_SOUTH_TRIAL.md` | `e0599520cc5907fb02457bfa0c7f771902a98a0a` | 35–37の定義、secant 恒等式、補助評価を照合。主要代数・補助不等式は本書で再計算。 |
| `D_OB_P2_D_AN1_FT_Q_EXTERIOR_SOUTH_WEIGHTED_38_40_TRIAL.md` | `d7e92a23b694da9c23ae6f4ebaf694cb0f199b7e` | \(\beta\) と符号換算、旧粗い南側下界、W-16 誤記の所在を確認。 |
| `D_OB_P2_D_AN1_FT_Q_KERNEL_CONSTANT_STRENGTHENING_TRIAL_DRAFT.md` | `6b36cc4103fa081f6e6793fa5ea880573da9cab2` | \(207/5000\) の原文を確認。核の全依存補題を今回再監査したとは主張しない。 |

Commit 固定の raw URL：

- [南側35–37](https://raw.githubusercontent.com/cotaxxxx/bg-oblate-spheroid/69e104602e939817b6f4d71df3f6bd63cbc729e0/analysis/D_OB_P2_D_AN1_FT_Q_EXTERIOR_SOUTH_TRIAL.md)
- [重み付き38–40](https://raw.githubusercontent.com/cotaxxxx/bg-oblate-spheroid/69e104602e939817b6f4d71df3f6bd63cbc729e0/analysis/D_OB_P2_D_AN1_FT_Q_EXTERIOR_SOUTH_WEIGHTED_38_40_TRIAL.md)
- [核の定数強化](https://raw.githubusercontent.com/cotaxxxx/bg-oblate-spheroid/69e104602e939817b6f4d71df3f6bd63cbc729e0/analysis/D_OB_P2_D_AN1_FT_Q_KERNEL_CONSTANT_STRENGTHENING_TRIAL_DRAFT.md)

新しい Bernstein 証明と \(C_{\rm core}=1/8\) は本検証で得た結果であり、これらの出典に元々記載されている結果ではない。
