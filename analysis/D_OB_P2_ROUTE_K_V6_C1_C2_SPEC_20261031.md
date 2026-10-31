# D-OB P2 / Route K — V6-C1/C2 certification specification (2026-10-31)

**Evidence class:** DESIGN / NOT CERTIFIED.  
**Target:** prove \(\inf_{a\in D}\mathcal I(a)>0\), with \(a=(\lambda,\tau,\delta)\) and
\[
D=[2/5,93/200]\times[7/8,1]\times[3/10^8,15/64].
\]

## Status and provenance
- V3 fixed-point outward-rounded interval evaluator: previously independently audited (single-cell evaluator only).
- V4/V5 floating-point continuity and boundary-layer diagnostics: **PASS (DIAGNOSTIC ONLY)**. Reported SHA-256 for V4 diagnostic: `8925b5ad9ec86cbadadf90c212cad8a62e7f7380b4cf15a5c3b9bafd70d5f67e`; V5: `fba2b91b0674581d4f6a30c3b9d2283e6a6d06b352937f2c7993818c27160766`.
- C1 rigorous uniform derivative bounds: **OPEN**.
- C2 rigorous four-dimensional quadrature certificate: **OPEN**.
- C1+C2 positivity assembly: **OPEN**.

## Domain and normalization
Use the parameter-independent cutoff \(p_0=1/20{,}000{,}000\), with \(\sigma_0=40{,}000{,}000/400{,}000{,}000{,}000{,}001\). Let \(J\) be the truncated integral of the two angular branches **without** the outer prefactor; then
\[
\mathcal I_{\rm trunc}=\frac{2\lambda}{\pi}J,\qquad
\mathcal I(a)\ge\mathcal I_{\rm trunc}(a)-2\lambda K_{\mathbb Q}\sigma_0,
\quad K_{\mathbb Q}=859375/16.
\]
The contact-loss bound is uniform, and \(2(93/200)K_{\mathbb Q}\sigma_0<0.005\).

## C1 — outer-cell-uniform continuity certificate
For each **whole outer box** \(A_j=\Lambda_j\times T_j\times D_j\), and each inner box \(K\) in \((y,p,t,u)\), compute fixed-point interval bounds
\[
B_{i,j,K}\ge \sup_{a\in A_j,\ z\in K}|\partial_i f(a,z)|,
\quad i\in\{\lambda,\tau,\log\delta\},
\]
where \(f\) includes \(2\lambda/\pi\), both \(\varepsilon=\pm1\) branches, and all Jacobians. Then
\[
L_{i,j}=\sum_K |K|B_{i,j,K}
\quad\Rightarrow\quad
\sup_{a\in A_j}|\partial_i\mathcal I_{\rm trunc}(a)|\le L_{i,j}.
\]
**Never substitute pointwise bounds at the outer-box center for whole-box bounds.** For the log direction evaluate \(\delta\partial_\delta\).

Include the prefactor derivative:
\[
\partial_\lambda\mathcal I_{\rm trunc}=\frac2\pi(J+\lambda\partial_\lambda J),\quad
\partial_\tau\mathcal I_{\rm trunc}=\frac{2\lambda}{\pi}\partial_\tau J,\quad
\delta\partial_\delta\mathcal I_{\rm trunc}=\frac{2\lambda}{\pi}\delta\partial_\delta J.
\]
Use rational outward enclosures for \(2/\pi\), never a floating-point constant in a certificate.

**Differentiation under the integral:** the integration domain is parameter-independent (fixed \(p_0\)); on the compact domain \(\sigma\ge\sigma_0>0\), \(\delta\ge3/10^8>0\), the integrand and parameter derivatives are continuous wherever all denominators are nonzero. The interval implementation **must certify positive denominator bounds**, then compactness supplies a uniform dominating bound.

**Inner grid:** define \(y=1-v\), and calculate \(x=1-v^2=y(2-y)\) directly, not by subtracting rounded squares. Thus
\[
M=\delta+(1-\delta)A^2y(2-y),\quad
N=1-A^2y(2-y),\quad
Q_x=(1-y)A/\sqrt N.
\]
Use a parameter-independent geometric grid in \(y\): \(0,10^{-10},10^{-9},\ldots,10^{-1},1\) (11 intervals), and \(p\) grid \(5\cdot10^{-8},10^{-7},10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},1\) (7 intervals). Split \(t,u\) into at least 8 cells each initially: \(11\cdot7\cdot8\cdot8=4928\) inner boxes per outer box. Adaptively refine or use centered forms if intervals are too wide. A secondary convergence grid splits \([10^{-2},1]\) into \([10^{-2},0.1],[0.1,0.3],[0.3,1]\).

Initial **unproved performance targets**: \(L_\lambda\le4\), \(L_\tau\le1\), \(L_{\log\delta}\le1/2\). Start with one wide \(\lambda\) interval and one wide \(\tau\) interval; \(\delta\) geometric boxes with ratio 2 (23 boxes). Any need for finer outer boxes is decided by certified, not FLOAT, bounds.

## C2 — certified four-dimensional integral lower bound
At each outer reference point \(a_j\), use outward-rounded fixed-point intervals and interval automatic differentiation to second order. For each inner box \(K\) of side lengths \(\ell_i\) and midpoint \(m\),
\[
\int_K f\ge |K|\left(f(m)^-+\sum_i\frac{\ell_i^2}{24}(\partial_{ii}f(K))^-\right).
\]
This signed midpoint remainder formula is the **design**; a working AD implementation, independently verifiable certificate, and completed integral bounds are still OPEN. Check square-root, reciprocal, and denominator domains on every box.

## Assembly
For every \(a\in A_j\), with certified \(B_j\le\mathcal I_{\rm trunc}(a_j)\) and certified outer-cell derivative bounds,
\[
\boxed{\mathcal I(a)\ge B_j-\sum_iL_{i,j}h_{i,j}-2\lambda K_{\mathbb Q}\sigma_0.}
\]
Here \(h_{i,j}\) is the maximum distance from the reference point to any point in the cell, using \(|\log(\delta/\delta_j)|\) for the third direction, enclosed rationally (e.g. \(|\log x|\le|x-1|/\min(1,x)\)). The contact-loss term **must not be omitted**.

A simple sufficient condition is \(B_j-\sum_iL_{i,j}h_{i,j}>0.005\) for all boxes, since the contact loss is strictly below 0.005.

## Next action
Implement C1 on one complete outer box using whole-box interval inputs, 4928 or adaptively refined inner boxes, and report actual outward-rounded \(L_i\), runtime, denominator-domain failures, and bound inflation. Do **not** mark C1 PASS until a checkable certificate and independent verification exist.
