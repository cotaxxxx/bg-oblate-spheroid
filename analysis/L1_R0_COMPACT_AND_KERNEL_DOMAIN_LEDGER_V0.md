# L1-R0 — exact compact instance & denominator-safe ledger V0

2026-10-17 JST / PAPER-ONLY / CHAT AUDIT REQUESTED

**総合判定：PARTIAL — §R0-2 の境界核を内部へそのまま適用する経路は STOP。**

compact instance、L0 compatibility、分母の紙上下界、許可された K_H 表示の pairing ledger は整理できた。指定された WB 出発式には、prefactor とは別に適用領域の問題がある。新しい interior WB kernel は以下で紙上導出案として分離し、凍結済み境界 kernel の差し替え・採用済み証明とは扱わない。

interval / certification / diagnostic run は行っていない。commit / push、D5 へのアクセスも行っていない。

## 1. 依頼・原典・未確認事項

今回の Judge 指示から次を固定する。

\[
S_{\rm L1}=\Sigma\cap\{\delta_0\le1-r^2\le15/64\},
\qquad\delta_0=3/10^8.
\]

§R0-2 以外の条項は変更しない。本稿は正式指示書そのものの改訂ではなく、実行により見つかった適用域の問題と紙上 ledger の提出物である。

確認した原典：現行 L3 V0.2（原本および同名コピーの本文一致）、FTQ_SIGNED_REDUCTION_PARTIAL_V0 §§3–6、固定 P1、L2、L0、PREDECLARE v1.2。L3 の FT_q 証明は境界 face 上のものであり、L3 は QM transfer により薄い境界層へ結論を延長している。

**未確認**：前版 L1-R0 指示書の全文と「pin 8件」の指定一覧は、今回の検索では取得できなかった。履歴には一覧が存在するとの要約があるが、名前・commit・SHA の8件を再構成できない。下記の確認原典を勝手に「指定8件」と同定しない。G2 原本・その exact pin も未特定のまま維持する。

## 2. Concrete compact instance / L0 compatibility

固定座標を

\[
R(\tau)=\frac{1-\tau^2}{1+\tau^2},\qquad
Z(\tau)=\frac{2\tau}{1+\tau^2},\qquad
p=(rR,0,\lambda rZ)
\]

とする。領域は exact に

\[
\lambda\in[2/5,93/200],\quad\tau\in[7/8,1],
\quad r\in[7/8,\sqrt{1-3/10^8}].
\]

上端の平方根を有限小数へ置換しない。\(r\ge0\)、\(49/64\le r^2\le1-3/10^8\) という有理多項式条件でも同じ領域を記述できる。閉有界 parameter set の連続像なので compact であり、全点が楕円体の内部にある。τ=1 の軸を含む。

\[
(1-\tau^2)^2+4\tau^2=(1+\tau^2)^2
\]

から \(\rho^2+z^2/\lambda^2=r^2\)。また

\[
112\tau^2+30\tau-112=(8\tau-7)(14\tau+16)\ge0
\]

から \(112\lambda\rho\le15z\)。従って L0 の

\[
S_{\rm AN}=\{\rho,z\ge0,\ 49/64\le\rho^2+z^2/\lambda^2\le1,
\ 112\lambda\rho\le15z\}
\]

に包含される。L3 層との共通端点は \(\delta=\delta_0\)。域の縮小・追加分割はしていない。

## 3. R0-K1 — WB の境界限定条件

§R0-2 の \(\lambda/(4\pi)\) は、採用済み **境界** signed reduction に対して正しい。問題はその prefactor ではない。

原典 FTQ_SIGNED_REDUCTION_PARTIAL_V0 §6 は明示的に

\[
|\xi|=|Q|=1,\qquad p=L_\lambda Q,\qquad
L_\lambda=\operatorname{diag}(1,1,\lambda)
\]

を使って

\[
h=\lambda(1-\xi\cdot Q)=\lambda\sigma^2/2,
\quad\gamma=\frac{\lambda\sigma}{2wk},
\quad e=\gamma T(1-2k^2)
\]

を導出する。ここで \(\sigma=|\xi-Q|\)、\(k^2=J\)。これらが境界核 B の根拠である。

L1 の点は \(p=L_\lambda(rQ)\) なので、\(\sigma=|\xi-rQ|\)、\(\delta=1-r^2>0\) とおけば

\[
\sigma^2=1+r^2-2r\xi\cdot Q,
\]
\[
\boxed{h=\lambda(1-r\xi\cdot Q)=\frac\lambda2(\sigma^2+\delta)}.
\]

従って内部では

\[
\boxed{\gamma=\frac{\lambda(\sigma^2+\delta)}{2w\sigma k}},
\]

であり、境界の \(\gamma=\lambda\sigma/(2wk)\) と一致しない。違いは L1 全体で \(\delta>0\) によって生じる。

**exact geometry witness（sampling ではない）**：\(r=7/8,\tau=1,\xi=Q=(0,0,1)\) は L1 の幾何条件を満たす。\(\sigma=1/8,w=1,k=\lambda\) で、正しい h は \(\lambda/8\)、境界式を流用すると \(\lambda/128\)。正しい γ は1、流用式は1/16である。これは表示の適用域の反例であり、H の positivity の反例ではない。

**結論**：既存 W と既存境界 B をそのまま L1 内部の核として扱うことはできない。L3 V0.2 は境界でその表示を使い、内部には QM で移しているので、本指摘は L3 の normalization bridge を否定しない。

## 4. 許可済み K_H route の source → definition → equivalence

### 4.1 Source and full-azimuth representation

P1 §8.2、L2 §§2–4 に基づき、\(F_E=h\arccos^2\gamma\) と書く（V3 の polynomial F との混同を避ける）。

\[
H(p)=\frac1{4\pi\lambda}\int_{-1}^1\int_0^{2\pi}K_H\,d\phi\,d\mu,
\]
\[
K_H=\frac{\partial_\rho F_E(\rho,b)-\partial_\rho F_E(-\rho,b)}{2\rho}
\quad(\rho>0),\qquad b=\sqrt{1-\mu^2}\cos\phi.
\]

内部 compact 上では、分母 ρ を計算上使わない等価式

\[
\boxed{K_H=\frac12\int_{-1}^1
\partial_{\rho\rho}F_E(v\rho,z;\mu,\phi)\,dv}
\]

を使える。これは FTC と \(s=v\rho\) の変数変換による。ρ=0 では直接 \(K_H=\partial_{\rho\rho}F_E(0,z)\) となる。

FTC swept points は \(p_v=(v\rho,0,z)\)、\(-1\le v\le1\)。S_AN の radial lower bound を外れることはあり得るが、P1 の全内部域で kernel の定義・微分が有効なので問題ない。swept points 全体の positivity を追加で仮定するものではない。

### 4.2 Reflection / half-turn pairing

\(h,D^2\) の依存から \(F_E(-\rho,b)=F_E(\rho,-b)\)。微分して

\[
\partial_\rho F_E(-\rho,b)=-\partial_\rho F_E(\rho,-b).
\]

従って K_H は b→−b に不変であり、

\[
K_{\rm pair}(\phi)=K_H(\phi)+K_H(\phi+\pi)=2K_H(\phi).
\]

full azimuth を二つに分け、後半で \(\phi'=\phi-\pi\)、Jacobian1 とすると

\[
\boxed{H=\frac1{4\pi\lambda}\int_{-1}^1\int_0^\pi K_{\rm pair}\,d\phi\,d\mu}.
\]

prefactor は変えず、branch multiplicity2を K_pair に含めている。

### 4.3 s=cosφ と arcsine measure

\([0,\pi]\) で \(d\phi=-ds/\sqrt{1-s^2}\)。\(d\omega=ds/(\pi\sqrt{1-s^2})\) とすると

\[
H=\frac1{4\lambda}\int_{-1}^1\int_{-1}^1K_{\rm pair}(s)d\omega\,d\mu
=\frac1{2\lambda}\int_{-1}^1\int_{-1}^1K_H(s)d\omega\,d\mu.
\]

この **K_H** は定義上 s-even なので、さらに

\[
\boxed{H=\frac1\lambda\int_{-1}^1\int_0^1K_H(s)d\omega\,d\mu}.
\]

これは raw WB / F_yy density の s-evenness を主張しない。一般の raw kernel では両枝を明示して和を取る必要がある。

### 4.4 WB との関係

回転対称性から \(E_{yy}=E_\rho/\rho=H\)、軸は連続延長で同じである。よって \(K_H\) の積分と \(F_{E,yy}\) の積分は一致する。点別 \(K_H=F_{E,yy}\) は仮定しない。

境界 r=1 でのみ、既存 signed reduction により
\(F_{E,yy}=\lambda^2\int_0^1WB\,dt\)。ここから \(1/(4\pi\lambda)\) が \(\lambda/(4\pi)\) へ移る。**異なる kernel normalization の接続であり、同じ kernel の係数訂正ではない。**

## 5. Interior WB への exact extension 案（新規導出・未採用）

境界表示を内部へ接続するなら、次の追加量が必要となる。

\[
\eta=1+\frac\delta{\sigma^2},\qquad
\nu=\frac{\xi-rQ}{\sigma},\quad k^2=\nu_x^2+\nu_y^2+\lambda^2\nu_z^2,
\quad V=\nu_y^2.
\]

P1 の generic directional kernel（FTQ partial V0 §5）では

\[
F_{E,yy}=\frac{2w}{D}
\{R_a[\gamma^2(1-T^2)-2e^2]-\gamma R_a'e^2\},
\]

\(R_a=\arccos\gamma/\sqrt{1-\gamma^2}\)、\(T=\nu_y/k\)。表面 unit normal の y 成分は \(\lambda\sigma\nu_y/w\) なので

\[
\gamma=\frac{\lambda\sigma\eta}{2wk},\qquad
e=\gamma T\left(1-\frac{2k^2}{\eta}\right).
\]

共通積分 \(R_a=2\int_0^1 A^{-1}dt\)、\(R_a'=-2\int_0^1(1-t^2)A^{-2}dt\) を代入・合成してから整理すると、既存と同じ
\(W=\sigma/(wk^5A^2)\) に対し

\[
\boxed{B_{\rm int}=A\eta^2(k^2-V)
-(2A-\gamma c)V(\eta-2k^2)^2},\qquad c=1-t^2,
\]

\[
\boxed{F_{E,yy}=\lambda^2\int_0^1WB_{\rm int}\,dt}
\]

となる。境界 δ=0 では η=1 となり既存 B を回復する。L1 では η>1 であり、B_int を既存 B と同一視しない。

\(n=V/k^2\) とすると、paired branch target は

\[
\boxed{\frac\lambda2WB_{\rm int}
=\frac{\gamma\eta}{k^2A^2}
\left[A(1-n)-(2A-\gamma c)n\left(1-\frac{2k^2}{\eta}\right)^2\right]}.
\]

η=1 の場合だけ V3 の \(\mathcal P=\gamma F/(k^2A^2)\) になる。L1 に V3 の4変数核をそのまま移すことはできない。η の dependency を追加で保持する必要がある。

この節は紙上での修正候補である。新たな interval enclosure、Bernstein、certificate 実行や positivity claim は含まない。採用は chat → Judge に戻す。

## 6. Denominator-safe ledger

\(r_* =\sqrt{1-\delta_0}\)、\(\varepsilon=\delta_0/2=3/(2\cdot10^8)\)、\(d_*=(2/5)\varepsilon=3/(5\cdot10^8)\) とする。後者は今回の内部 compact から得た幾何下界であり、D4 の定数を流用していない。

すべての FTC point で \(|L_\lambda^{-1}p_v|\le r\le r_*\)。任意の表面点 x=L_λξ、|ξ|=1 に対し

\[
|\xi-L_\lambda^{-1}p_v|\ge1-r
=\frac\delta{1+r}\ge\frac{\delta_0}2=\varepsilon,
\]

\[
D\ge\lambda(1-r)\ge d_*,\qquad
h=\lambda(1-\xi\cdot L_\lambda^{-1}p_v)\ge\lambda(1-r)\ge d_*.
\]

| 因子 | exact 情報 | 操作上の扱い |
|---|---|---|
| 1+τ² | ≥113/64 | 座標の正分母 |
| r、1+r | r≥7/8、1+r≥15/8 | 必要な除算は正 |
| λ、w | λ≥2/5、w≥λ | 正の係数として保持 |
| σ | ≥3/(2·10⁸) | L1 内部と FTC sweep に限る |
| D、h | ≥3/(5·10⁸) | 共通の正下界、face には持ち出さない |
| J=k²、k | J≥λ²≥4/25、k≥2/5 | ν が単位ベクトルであることから |
| γ | 0<γ≤1 | P1 の h≤wD を利用 |
| A=1+t²+(1−t²)γ | 1≤A≤2 | removable γ=1 も安全 |
| wk⁵A² | ≥(2/5)⁶=64/15625 | W の分母 |
| η=1+δ/σ² | >1、σ²>0 | interior correction、boundary では1 |
| ρ、2ρ | τ=1で0 | 直接除算禁止、FTC / 連続延長を使う |
| √(1−γ²) | γ=1で0になり得る | R_a の見かけの特異性。解析的延長または共通t表示を使う |
| c=1−t² | t=1で0 | c での除算を導入しない |
| √(1−s²) | s=±1で0 | arcsine の可積分 Jacobian。正の一様下界を仮定しない |

これらは symbolic geometry による分母の符号保証であり、認証計算による enclosure の成功や practical conditioning を意味しない。特に d_* は非常に小さく、これだけで効率的な証明方式が得られたとはいえない。

## 7. Sign-inequality ledger

| 対象 | 使用可能な符号 / 推論 | 使用しない推論 |
|---|---|---|
| h,w,D,λ,W | L1 で正 | 正の weight だけから積分 H>0 |
| V、k²−V | V≥0、k²−V=ν_x²+λ²ν_z²≥0 | B_int 全体が正 |
| A、2A−γc | A≥1、2A−γc=2(1+t²)+cγ>0 | 正負二項の大小の未証明比較 |
| B_int | 非負項 − 非負項 | 点別 positivity の仮定 |
| R_a、R_a' | R_a≥1、R_a'≤0 | signed composite の早期絶対値化 |
| −γR_a'e² | ≥0 | 残りの R_a 項の自動的正値性 |
| K_H / K_pair | 積分同値性と軸延長 | 全点で非負という仮定 |
| 正分母での除算 | 不等号の向きを保持 | 分母と分子の dependency の無条件切断 |
| sign-unknown numerator | 符号を区別して上下界を使う | 負項にも正項と同じ denominator bound を使うこと |
| 平方操作 | 両辺の符号確認後のみ同値化 | sign-unknown inequality の単純二乗 |
| M=295346256371/10¹² | 境界 H(q) の証明済み lower bound | exact inf H、upper bound、または内部 H(p)≥M という主張 |
| G2 | 原本未特定 | 具体式・既証明範囲・margin の推定 |

境界から得られる \(H(p)\ge M-\omega_E(\delta)\) は有効でも、L3 が閉じたのは δ≤δ₀ の層である。今回の δ≥δ₀ の全域 positivity は別の L1 義務として残る。

## 8. Fail-closed / 次工程

1. **§R0-2 の境界 WB 核を無変更で内部へ使う段階は STOP。** 理由は原典の |Q|=1 仮定と δ>0 の不一致。
2. 許可された K_H route の紙上 ledger は上記のとおり構成できる。新しい B_int も未採用の導出案として区別した。
3. 指定8 pin・前版全文は SOURCE_NOT_FOUND / UNVERIFIED。ここを推測で完了扱いしない。
4. G2 は UNVERIFIED のまま。新規の H 数値評価・区間計算・certificate run は0件。
5. L1-R0 の完全 PASS / READY は宣言しない。positivity 不成立・数学的反例とも判定しない。

**推奨する次工程：本 ledger を chat に渡し、WB の boundary-only scope と interior B_int または K_H 接続を監査した後、Judge が §R0-2 の適用域を確定する。**

その他の前版条項を変更する裁定は行っていない。FT_q / L3 の既存成果を取り消すものではない。L1 は PAPER-ONLY、interval / certification run と commit / push は NOT AUTHORIZED、D5 は NO ACCESS / NO MUTATION を維持する。

## 付録. Source pins

以下は本稿で照合した原典であり、未取得の「前版指定8 pin」を代替する一覧ではない。

全 GitHub 原典の repository: `cotaxxxx/bg-oblate-spheroid`。

- `sources/P1_PIN.md`
  - commit: `6c6282a8acbf467bcbe6a7e32236e1d32a91f400`
  - path: `analysis/D_OB_P1_DESIGN_NOTE.md`
  - SHA-256: `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`
- `sources/L2_PIN.md`
  - commit: `9eb8ddee96cbb1703618aa606eeb9e81f7697549`
  - path: `analysis/D_OB_P2_D_AN1_L2_DRAFT.md`
  - SHA-256: `0a83e411e51582674c5490cb8e92defd171481c6271c48c6760681b8f5e839cb`
- `sources/L0_PIN.md`
  - commit: `3cabe008b95ed7f81597a45f74303a5b7c53907f`
  - path: `analysis/D_OB_P2_D_AN1_L0_DRAFT.md`
  - SHA-256: `41b6be56e6e81f6b0f90e155865f9fc9fcd75129215cfd5df8be6845755c639e`
- `sources/PREDECLARE_V1_2_PIN.md`
  - commit: `e9c8b1caa3ad502a3d01dafe354b61108787eed2`
  - path: `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`
  - SHA-256: `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217`
- `sources/D_OB_P2_D_AN1_L3_BODY_DRAFT_V0_2.md`
  - SHA-256: `d4d2591e0a800202e50224eb9caa697a35054db6971885bc727d87aad5766997`
- `sources/FTQ_SIGNED_REDUCTION_PARTIAL_V0.md`
  - SHA-256: `91d1702836410e6a2ce78593079e166afd7a1a887839af86d92cc64b0f8e9208`

`SOURCE_LEDGER.json` は照合範囲と未取得資料を記録する。計算結果を装う certificate / run manifest は生成していない。
