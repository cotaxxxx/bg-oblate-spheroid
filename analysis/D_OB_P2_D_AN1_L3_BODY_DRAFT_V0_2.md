# D-OB P2 / D-AN-1 — L3 BODY DRAFT V0.2

2026-10-17 — Judge 指示に基づく本文更新・chat 監査提出版

**DRAFT / ARITHMETIC CHECK PASS / CHAT AUDIT REQUESTED / NOT FROZEN / NOT CERTIFIED**

## 0. 結論と採用範囲

Judge の本チャット上の裁定に従い、FT_q は **DISCHARGED（条件付き）**として扱う。条件は P1 normalization、paired density、boundary extension / Lemma V、endpoint NP-T 接続である。これらの既存定理の独立再監査を本稿で完了したとは主張しない。

V3 の whole-face certificate 下界と L3 の入力下界の換算係数は **1** である。採用する表示用下界と新しい境界層幅は

\[
M=\frac{295346256371}{10^{12}},\qquad
\boxed{\delta_0=\frac3{100000000}}.
\]

固定 QM modulus と継承条件の下で、L3 の閉境界層全体について

\[
\boxed{H(p)>\frac{273790294597}{7000000000000}>0}
\]

を得る。これは L3 V0.2 の条件付き数学的結論であり、L3 FREEZE、L1 再開、D-P2 CERTIFIED の裁定ではない。

## 1. exact m₀ の照合と証拠の区別

V3 の exact 分数を \(m_{\rm V3}=a/b\) とする。添付 `sources/M0_LIBRARY_CURRENT.txt` を読み直し、整数演算で次を確認した。

| 検査 | 結果 |
|---|---|
| 分子 / 分母の十進桁数 | 90,766 / 90,767 |
| 分母 | 正 |
| gcd(a,b) | 1 |
| 下側比較 | \(10^{12}a\ge295346256371b\) |
| 上側比較 | \(10^{12}a<295346256372b\) |

従って

\[
M\le m_{\rm V3}<\frac{295346256372}{10^{12}}.
\]

この検査は分数の包囲確認であり、4096 certificates の再生成ではない。既存 V3 production / checker は再実行・変更していない。

Judge から受領した chat 独立再計算の報告は、別実装で4096枝を完了し、positive / zero / negative certificate lower bounds が2230 / 0 / 1866、argmin が(0,0)、独立正下界を得たとする。本稿ではこれを **受領済み監査報告・Judge 採否の記録**として引用する。別環境の chat JSON / スクリプト本文とその最終 SHA は未受領であり、本作業による再検算済み artifact とは表示しない。

chat の下界は Astra の \(M\) より小さいため、chat の小数表示だけから \(M\) を導くことはしない。\(M\) は採用済み V3 exact certificate と上記整数比較に基づく。独立 chat 証明は positivity の別証明・整合監査として区別する。

2026-10-09 の旧 m₀ は PROVENANCE GAP / NOT EVIDENCE とし、本稿の定数選択・証明入力に使わない。V1.1 / V2 の METHOD FAIL は履歴として保持する。

## 2. Normalization bridge — exact coefficient 1

### 2.1 L3 側の入力は whole-face H

L3 V0.1 §§0,3、および固定 L3 MRA §4 の仮定は、境界 face 上の正規化済み量

\[
H(q;\lambda)\ge m_0
\]

である。V0.1 本文は「lower-half 積分を m₀ とする」とは定義していない。半域の表現は積分の対化に由来するため、ここで別の1/2を追加してはならない。

P1 §1 の正規化は

\[
E(p)=\frac1{4\pi\lambda}\int_{-1}^{1}\int_0^{2\pi}F\,d\phi\,d\mu.
\]

内部の回転対称性から \(E_{yy}(\rho,0,z)=E_\rho/\rho=H\)（\(\rho>0\)）。Lemma V(c) と Lemma 6.1(iii) による連続延長で境界へ移り、軸では \(E_{yy}=E_{\rho\rho}=H\) となる。これは積分の同値性であり、P1 の paired kernel と \(F_{yy}\) の点別一致ではない。

### 2.2 V0/V1.1 の signed density から V3 へ

採用済み signed reduction で \(k=\sqrt J\)、\(A=1+t^2+(1-t^2)\gamma\) とし、幾何学的 weight を

\[
W=\frac{\sigma}{wk^5A^2}
\]

と書く。この \(W\) と V3 の \(\mathcal W\) は区別する。共通 t 積分表示は

\[
H=\frac{\lambda}{4\pi}\int_{-1}^1\int_0^{2\pi}\int_0^1 WB\,dt\,d\phi\,d\mu.
\]

\(s=\cos\phi\) とおく。\(\phi\mapsto-\phi\) の鏡映は使えるが、raw density の \(s\mapsto-s\) 偶性は仮定しない。恒等式

\[
\int_0^{2\pi}f(\cos\phi)d\phi
=2\int_{-1}^1\frac{f(s)}{\sqrt{1-s^2}}ds
\]

と明示的な両枝の和により、\(d\omega=ds/(\pi\sqrt{1-s^2})\) を用いて

\[
H=\int_{-1}^1\int_0^1\int_0^1
[\mathcal P_++\mathcal P_-],dt\,d\omega\,d\mu,
\qquad \mathcal P_\epsilon=\frac\lambda2 W_\epsilon B_\epsilon.
\]

V2/V3 の恒等式

\[
\sigma=\frac{2wk\gamma}{\lambda},\quad B=k^2F,
\quad F=A(1-n)-(2A-\gamma(1-t^2))n(1-2k^2)^2
\]

を代入すると

\[
\boxed{
\frac\lambda2 WB
=\frac\lambda2\frac{\sigma}{wk^5A^2}k^2F
=\frac{\gamma F}{k^2A^2}
=\mathcal P.
}
\]

よって **λ/2 は V3 branch target にすでに含まれる**。後掛けの λ/2、1/2、2、π は不要。検算付録はこの代入を形式的 Laurent monomial として有理係数で確認する。積分交換・境界延長そのものは継承する解析的仮定である。

### 2.3 μ16 の重みと parameter aggregation

\[
\omega([0,1/2])=1/6,\quad \omega([1/2,1])=1/3,
\quad\Delta\mu=1/8,\quad\Delta t=1/4.
\]

従って各 folded physical cell の寄与は

\[
L_{ijhab}=\begin{cases}
(\ell_++\ell_-)/192,&h=0,\\
(\ell_++\ell_-)/96,&h=1.
\end{cases}
\]

\(S_{ia}=\sum_{j,h,b}L_{ijhab}\)、\(m_{\rm V3}=\min_{i,a}S_{ia}\)。τ と λ は積分せず、16 parameter cells 間は加算しない。閉 cell の共通端点もそれぞれの bound に含まれる。

したがって \(H(q)\ge m_{\rm V3}\ge M\) であり、L3 入力への換算係数は1である。定数密度 \(\mathcal P_\pm=1\) を形式的に代入した積分値は2で、離散重みの総和も2となる。μ 測度を確率測度へ再正規化しない。

## 3. 閉境界層への transfer

\[
\lambda\in[2/5,93/200],\quad \tau\in[7/8,1],
\quad q=(R,\lambda Z),
\quad R=\frac{1-\tau^2}{1+\tau^2},\ Z=\frac{2\tau}{1+\tau^2}.
\]

\(R^2+Z^2=1\)、\(\lambda\le1\) より \(|q|\le1\)。L3 の深さ変数は **\(\delta=1-r^2\)** であり、距離そのものではない。\(p=rq\)、\(r=\sqrt{1-\delta}\) に対し

\[
|p-q|=(1-r)|q|\le1-r=\frac\delta{1+r}\le\delta.
\]

固定 λ における P1 の表示

\[
H(\rho,z)=\int_0^1E_{\rho\rho}(v\rho,z)dv
\]

と \(|(v\rho,z)-(v\rho',z')|\le|p-p'|\) により、固定 QM の modulus はそのまま H に移る。

\[
|H(p)-H(q)|\le\omega_E(|p-q|),\qquad
H(p)\ge M-\omega_E(\delta).
\]

この argument は同じ λ の点を比較する。λ 方向の modulus を新たに仮定しない。軸で割り算は行わず連続延長を使う。

## 4. δ₀ の有理数再計算

### 4.1 固定 modulus

\[
\omega_E(d)=50C_2d+25C_3d\{1+2\log(1/d)\},
\quad C_2=9\pi+8,\ C_3=8788+39\pi.
\]

QM 原典の適用範囲内で使用する。\(0<d\le\delta_0\) では
\(\omega'_E(d)=50C_2+25C_3(2\log(1/d)-1)>0\)。\(\omega_E(0)=0\) は連続延長である。

### 4.2 π と log の rational upper bounds

\(\pi<22/7\) は

\[
0<\int_0^1\frac{x^4(1-x)^4}{1+x^2}dx=22/7-\pi
\]

から得る。付録は正分母による多項式除算と有理数積分部分を確認する。

\(z=(x-1)/(x+1)\in(0,1)\) に対し

\[
\log x=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1}+R_N,
\quad0<R_N\le\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

\(N=2\)、\(\log10=3\log2+\log(5/4)\)、それぞれ \(z=1/3,1/9\) を使い

\[
\log10\le\frac{1007233}{437400}<\frac73.
\]

したがって \(10^{-8}\le d\le10^{-7}\) なら \(\log(1/d)\le8\log10<56/3\)。

### 4.3 単純な有理数への下方丸め

この decade 上で

\[
50C_2<\frac{12700}7,\quad25C_3<\frac{1559350}7,
\quad\omega_E(d)<Cd,
\quad C=\frac{179363350}{21}.
\]

\[
\frac MC=\frac{6202271383791}{179363350000000000000},
\qquad \frac3{10^8}<\frac MC<\frac4{10^8}.
\]

よって有効数字1桁の有理数へ下方丸めして \(\delta_0=3/10^8\) とする。これは証明済み入力 M と解析的 envelope の有理比較で選んだ値であり、production diagnostic からの tuning ではない。

\[
\omega_E(\delta_0)<\frac{3587267}{14000000},
\]
\[
\boxed{
M-\frac{3587267}{14000000}
=\frac{273790294597}{7000000000000}>0.
}
\]

\(d<10^{-8}\) に同じ log upper bound を直接適用してはいけない。\(0\le d\le\delta_0\) 全体への結論は \(\omega_E\) の単調性から得る。

旧幅との比は

\[
\frac{3/10^8}{3/20000000000}=200.
\]

最大許容幅の最適化は行わない。V0.1 の旧 m₀ に依存する threshold bracket は本稿へ継承しない。

## 5. FT_q V3 の採用記録

| 項目 | 採用済み記録 |
|---|---|
| physical partition | τ4 × μ16 × s2 × λ4 × t4 = 2048 folded boxes |
| branches / mandatory LP | 4096 / 4096、P-only |
| active order | (t,γ,k,n) |
| joint constraints | 凍結済み Q₁,…,Q₈ |
| multiplier / residual degree | (0,2,2,1) / (4,4,6,2) |
| certificate | nonnegative Bernstein multipliers + nonnegative residual + exact primal/dual equality |
| denominator | \(k^2A^2\ge4/25\)、physical D_min は使わない |
| producer counts | float-seed3913 + exact fallback183 =4096 |
| CHECK_ERROR / RESOURCE_LIMIT | 0 / 0 |
| existing independent checker | PASS、4096枝 |
| chat independent recomputation | PASS と報告・Judge ACCEPTED。最終 chat artifact hash は未受領 |
| argmin | (0,0) |

negative branch lower bounds は physical integrand の負値認定ではない。moving diagonal \(\gamma=0\) は閉領域に含まれ、P=0。個別枝の正値性を要求しない。

## 6. 継承 pin と六段階 L3 の対応

以下は今回読んだ固定原典の対応表である。原典の draft / external-audit-pending 等の status を、本稿によって独立に昇格させない。**今後の FREEZE は以下の継承条件を仮定するものとして明記する。**

| L3 段階 | 対応する原典と使用内容 |
|---|---|
| 1. uniform boundary-layer bounds | L0 の座標・sector包含、P1 §1・§4 の λ帯共通の重み・面積評価、QM の共通定数 |
| 2. D/h comparison | P1 Lemma3.1: 0≤h≤wD。D の一様正下界を要求しない |
| 3. γ derivatives | P1 Lemma3.3: \(|\gamma_v|\le2/D\)、\(|\gamma_{vv}|\le5/D^2\) |
| 4. uniform L¹ control | P1 Lemma3.4、Lemmas4.1–4.2、Cor4.3、§8.2 の paired kernel control |
| 5. interchange / boundary limit | P1 Lemma V(a)(b)(c)、Lemma6.1、L2 §§3–4,6。uniform integrability / Vitali による連続延長 |
| 6. strict closed-corner extension | accepted V3 whole-face bound + QM transfer + 本稿 §§2–4 |

原典との一対一の参照位置は整理したが、1–5 の既存証明を今回独立に再証明・再監査したとはしない。chat はこの対応と継承範囲を V0.2 監査で確認する。

τ=1 では \(H(0,\lambda)=E_{\rho\rho}(0,\lambda)\)。NP-T (9.1) の中間量 \(\lambda13/1000\) に \(1/(2\lambda)\) を適用すると、正規化後は \(13/2000\)。これは endpoint の独立 cross-check であり、V3 の直接 whole-face bound を \(\min(M,13/2000)\) に切り下げる必要はない。NP-T の接続条件自体は Judge 指示どおり残す。

P1 normalization、paired density / H=Eyy の積分同値性、boundary extension、NP-T 接続に加え、QM の固定 modulus を前提とする。継承する量を検算スクリプトの PASS だけで証明済みへ変更しない。

## 7. V0.1 からの差分

| 項目 | V0.1 | V0.2 |
|---|---|---|
| whole-face m₀ | 旧値の exact provenance 未確認 | accepted V3、整数包囲確認済み M を採用 |
| normalization | H(q)≥m₀ を仮定 | V3 P から換算係数1を明示、half-domain の再係数を排除 |
| FT_q | provenance HOLD | Judge により DISCHARGED（継承条件付き） |
| δ₀ | 3/20000000000 | 3/100000000、200倍 |
| log / margin | 旧入力に依存する算術 | 固定 log-series rational bound、正の exact margin |
| six-stage readback | 対応整理を残す | 固定原典と段階の対応を明記、独立再監査とは区別 |
| L3 | FREEZE HOLD | V0.2 CHAT AUDIT REQUESTED、FREEZE HOLD 維持 |
| L1 / D-P2 | PAUSED / NOT_CERTIFIED | 変更なし |

## 8. Handoff と状態

\(0\le\delta\le\delta_0\) の L3 層では条件付き正値性を得る。Σ の深さ上端は \(15/64\) なので、残る compact 側の接続候補は \([\delta_0,15/64]\)。共有端点 δ₀ を含む。L1 の proof / execution 条件を本稿で変更・再開しない。

次工程は **chat V0.2 監査 → Judge L3 FREEZE 裁定 → L1 再開可否の別裁定**。

FT_q: DISCHARGED（指定継承条件付き）／ L3: ARITHMETIC PASS・FREEZE HOLD（V0.2監査待ち）／ L1: PAUSED ／ D-P2: NOT_CERTIFIED。D5 にはアクセスしていない。commit / push は行っていない。

## 付録A. 検算と資料

`python l3_v02_checks.py` を本 bundle 内で実行すると、exact fraction、source hashes、形式的正規化代入、μ16 weights、log bound、δ₀、margin、旧幅比を標準 Python の整数・Fraction 演算で再確認できる。

`l3_v02_checks_result.json` は今回の実行結果。`source_ledger.json` は各原典の commit / path / SHA-256。`sources/M0_LIBRARY_CURRENT.txt` は canonical exact m₀ の全文。巨大分数は本文へ転記しない。

SHA-256 と固定 source pin の完全表は以下に続く。


### 固定原典 pins

全 GitHub 原典の repository は `cotaxxxx/bg-oblate-spheroid`。

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
- `sources/NP_T_PIN.md`
  - commit: `99467ed5e51a9b60c88073fda7a8f0094ebe770c`
  - path: `analysis/D_OB_P2_D_AN1_NP_T_DRAFT.md`
  - SHA-256: `e929d95631a5e6a5dac86dad86f5285b69429e5ff9bcb33c1695f24eff8b196b`
- `sources/QM_PIN.md`
  - commit: `7f9119f7cbe7d5dab95e42300bb9563c974e23f5`
  - path: `analysis/D_OB_P2_D_AN1_QM_DRAFT.md`
  - SHA-256: `e8588c1b677e10aceac22e79784e41111cffe2c2cffce1636804485dafb09edc`
- `sources/L3_MRA_PIN.md`
  - commit: `5fc0341216f4e0f6722a96f3d8edb2e1c9fbc47c`
  - path: `analysis/D_OB_P2_D_AN1_L3_MRA_DRAFT.md`
  - SHA-256: `b13e07d63b3f3035b7b983cc39acbae893d4a184dfa030eaf73bb9f243a0d842`
- `sources/PREDECLARE_V1_2_PIN.md`
  - commit: `e9c8b1caa3ad502a3d01dafe354b61108787eed2`
  - path: `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`
  - SHA-256: `f27a568b2996eb29e3756612dac3cb40ac2796b19dd81729742082a62abcf217`
- `sources/FT_Q_PIN.md`
  - commit: `20c5c59bd74f940fe0b1e05892bd2169e09d4fde`
  - path: `analysis/D_OB_P2_D_AN1_FT_Q_DRAFT.md`
  - SHA-256: `46443f0e981f360e57fb70d99754b0e480042d246e22d36732b00b96102a9cd1`
- `sources/L3_BODY_V0_1.md`
  - SHA-256: `19c6d31f231b4ac8c101841c118c92560bbdeb4bab20f3df6ae236b7ae5291ee`
- `sources/M0_LIBRARY_CURRENT.txt`
  - SHA-256: `207b9617d61645e2c89f125debac2e40576f11f790feb09f81471564a1fd7d17`
- `sources/FTQ_SIGNED_REDUCTION_PARTIAL_V0.md`
  - SHA-256: `91d1702836410e6a2ce78593079e166afd7a1a887839af86d92cc64b0f8e9208`
- `sources/FTQ_5_VARIABLE_ARCHITECTURE_V1_1.md`
  - SHA-256: `cafc0516b794d2a7643fcfa2b2d975333ce2cbe851f55573590310478dc57e3a`
- `sources/FTQ_CORRELATION_RECOVERY_ARCHITECTURE_V2.md`
  - SHA-256: `03f6a799db51a7813f622391f67373b858e64344f2c68c02f0218eade17420b5`
- `sources/FTQ_V3_JOINT_CONSTRAINT_ARCHITECTURE.md`
  - SHA-256: `e6660d52caf482837961962d4df5bf53b335fa4d8529849a6303b142cfcec62b`
- `sources/ftq_v3_joint_constraint_spec.py`
  - SHA-256: `d17cd115ee1da13a1470cf5afb17414db158b0f1cf447847dbc27ec0054b153a`
- `sources/ftq_v3_architecture_checks.py`
  - SHA-256: `68c96f1c5c35bd4e7e8c541190a57cebc98d43d538dfc092d18d841996770c08`
- `sources/ftq_algebra.py`
  - SHA-256: `e24ff38dae62d7457aedc65ab46e528c8a737c5887e3ff037b098c4fdb6ed30b`
- `sources/ftq_v2_fixed_enclosure.py`
  - SHA-256: `c83709482525da48fe7fb28fdd15d5dd7f999909a51be855e808847d6f1f1b1f`
- `sources/partition_manifest.json`
  - SHA-256: `16988a142142bf9708fbf475e5ade8304a13f0dc6414879893635e1f06528455`
- `sources/SHA256SUMS.json`
  - SHA-256: `5c2c2d9af95dd89b4865007606b770a48c7a9a5f21bbe0b84e165d93b57d120e`
- `sources/FTQ_V3_EXACT_PRODUCTION_REPORT_20261017.md`
  - SHA-256: `6b9e51e5a13d7dcef09fa04c96b0510bd22e552fa477903e32bd5058cb282d6d`

### 検算付録 hashes

- `l3_v02_checks.py`: `cc83a259730c563736c5a7b22f76e024fed01eb2bf68bd18a176fc815c68cd8d`
- `l3_v02_checks_result.json`: `bb2743ed0b8d99bd721dbd511940bf9728c71322778ee343801f2e17006c7d71`
- `source_ledger.json`: `9eda281f7bc1624ceec3369171c81f57fbd2a209c33b13fea9bbd6783ccfc4e7`

既存 V3 audit bundle（再生成していない）SHA-256: `abd1202ca69e815eddc83919cee3797d67875a3020635735dc312818eca60f93`。

chat 独立再計算の最終 JSON / script SHA: **NOT RECEIVED**。本稿に架空の pin を追加しない。

既存 result / checker の16区画和の exact 一致、最小値と分数ファイルの一致、argmin (0,0)、source4件の契約 SHA 一致も読み戻した。`v3_result_readback.json` SHA-256: `46482bb5b26f3aa42ca26012d7d9ae7c0e1353d04d65cf1806f570a8b762ba69`。これは保存済み結果の整合確認であり、certificate 再実行ではない。
