# Prior-work audit for the radial–normal angle landscape

Status: working literature map for paper preparation.  
Audit principle: **PROVEN ≠ NOVEL ≠ CERTIFIED**. “Direct precedent not found” means only that the targeted audit has not found one; it is not a proof of novelty.

## Object under study

For a convex body (K) and (p\in\operatorname{int}K),

[
E_K(p)=\int_{\partial K}\alpha_{K,p}(x)^2\,d\mu_{K,p}(x),
]

where

[
\alpha_{K,p}(x)=\arccos\frac{(x-p)\cdot\nu_K(x)}{|x-p|},
\qquad
d\mu_{K,p}(x)=\frac{(x-p)\cdot\nu_K(x)}{n\operatorname{Vol}(K)}\,dA .
]

The research object is the shape-induced landscape (p\mapsto E_K(p)), and subsequently its gradient, critical/Morse structure, and bifurcations under deformation of (K).

## 1. Radial Gauss geometry and Minkowski theory — CLASSICAL / KNOWN

Radial maps, Gauss maps, radial Gauss maps, radial Gauss images, cone-volume measures, dual curvature measures, and associated Minkowski/Gauss-image problems are established convex geometry. The ingredients “radial direction”, “normal direction”, and cone-volume weighting are therefore not claimed as new.

Paper use: mathematical background and terminology; connect (E_K) to established radial/Gauss and measure-transport geometry.

## 2. Support, pedal, polar, and centro-affine geometry — CLASSICAL / KNOWN

The support quantity

[
h_p(x)=(x-p)\cdot\nu_K(x)
]

is classical. Pedal geometry records closely related projection data. Centro-affine geometry classically uses the position vector, support functions, polarity, affine support functions, and centro-affine curvature. Polarity exchanges radial/normal structures in established ways.

For centered ellipsoids, the present work proves the specialization (E_A(0)=E_{A^{-1}}(0)), but this identity is **PROVEN, NOT CLAIMED NOVEL** pending literature audit.

Conceptual distinction: (h_p) is a projection length, whereas

[
\frac{h_p(x)}{|x-p|}=\cos\alpha_{K,p}(x)
]

is a normalized Euclidean angular discrepancy. The latter is not generally (SL(n))-invariant.

## 3. Visual-angle integral geometry — CLASSICAL

The Crofton–Hurwitz–Masotti–Santaló tradition studies integrals involving the visual angle of a convex set, including angle-squared expressions. Therefore neither “integrating an angle” nor “integrating an angle squared” is claimed as new.

Important distinction: classical visual angle is typically defined from an exterior observation point by supporting tangents (or its higher-dimensional analogue). Here (p\in\operatorname{int}K), and the angle is between (x-p) and the surface normal at each boundary point.

Terminology consequence: avoid using “visual angle” as the formal name for the present observable; use **radial–normal angle**.

Modern entry point:
- Cufí, Gallego, Reventós, work on Crofton/Hurwitz visual-angle integral formulas and their historical lineage.

## 4. Radial–normal shape descriptors — KNOWN

Computer-vision / shape-retrieval literature uses alignment between a radial direction and a surface normal as a shape feature. In particular, density-based 3D shape descriptors have used quantities of the form

[
A=|\langle \hat R,\hat N\rangle|
]

with a centroid-based reference frame, together with feature distributions for retrieval.

Therefore:
- radial–normal alignment as a shape feature: **KNOWN**;
- using radial/normal discrepancy as a local or distributional sphericity-related descriptor: **KNOWN / adjacent**.

The present work does not claim invention of the radial–normal comparison itself.

## 5. Moving reference points and viewpoint-quality fields — KNOWN

Computer vision and graphics contain moving-reference-point and viewpoint methods. Viewpoint entropy and viewpoint-quality measures assign a global scalar score to an observation position based on how an object or scene is seen from that position. Surface-based descriptors also use many local reference points.

Therefore the following general ideas are **KNOWN**:
- move an observer/reference point;
- evaluate an object from each position;
- construct a scalar score over a viewpoint domain;
- optimize extrema of that score.

Representative line:
- Vázquez, Feixas, Sbert, Heidrich, “Viewpoint Selection Using Viewpoint Entropy” (2001).
- Subsequent viewpoint-quality work by Sbert and collaborators.

Distinction relevant here: the present domain is the **interior of the convex body**, each (p) produces a global boundary integral, and the goal is not merely to choose an optimal viewpoint but to study the complete critical/Morse/bifurcation geometry of the induced field.

## 6. Moving interior-point convex geometry: Santaló — CLASSICAL / KNOWN

The Santaló functional

[
p\mapsto \operatorname{Vol}((K-p)^\circ)
]

is a classical moving-basepoint landscape. Its strict convexity and unique minimizer provide an especially important comparator.

Thus “moving an interior base point to obtain a scalar landscape” is not claimed as new.

Research contrast: the Santaló landscape is strictly convex with a unique minimum, whereas the radial–normal angle landscape can exhibit noncentral stationary branches/orbits, boundary entry, degeneracy walls, and Morse-index changes.

Paper TODO: identify and cite the primary source for strict convexity for arbitrary convex bodies (not only a secondary citation through recent Santaló-geometry literature).

## 7. Scalar landscapes, Morse theory, and shape analysis — CLASSICAL / KNOWN

The pipeline

[
\text{shape}\to\text{scalar field}\to\text{critical/Morse structure}
]

is established in Morse theory, computational topology, and shape analysis. Morse–Smale complexes, distance fields, scalar surface functions, basins, separatrices, and related descriptors are not methodological novelties of this project.

Consequently “landscape”, “critical points”, “Morse index”, “gradient field”, and “bifurcation analysis” are standard mathematical machinery used to study the specific observable (E_K).

## 8. Rigorous / validated numerics — KNOWN

Interval arithmetic, adaptive subdivision, computer-assisted proof, validated numerics, and rigorous global bifurcation/root certification are established fields. Relevant traditions include Tucker, Nakao and collaborators, CAPD, formalized rigorous numerics, and rigorous global bifurcation work.

The project does **not** claim invention of global certification. Its result is certification of the specific radial–normal landscape over specified parameter ranges.

The producer/checker, predeclaration, hash/ledger, and fail-closed audit architecture should be treated as reproducibility/certification infrastructure unless a separate novelty audit establishes otherwise.

## 9. Volume-preserving ellipsoid shape space — KNOWN

Centered unit-volume ellipsoids can be represented by determinant-one positive-definite matrices. In logarithmic semiaxes,

[
u_1+u_2+u_3=0.
]

Modulo axis permutations, the natural geometry is the (A_2) Weyl chamber. Shape triangles and axis-ratio diagrams also have established precedents in several applied literatures.

Therefore the ellipsoid shape space itself is not claimed as new. The research question is the (E_K)-specific landscape/bifurcation atlas over this known shape space.

## 10. Geometric tomography and inverse shape problems — KNOWN neighboring framework

Support functions, brightness/projection data, X-ray/section data, covariograms, and related transforms provide classical frameworks for asking how geometric data determine a convex body.

This is the appropriate neighboring literature for the later inverse question:

[
E_K(\cdot)\text{ or }(E_K,\nabla E_K)\quad\text{determines how much of }K?
]

No injectivity/reconstruction claim is made at present.

## Current novelty-status map

| Item | Status |
|---|---|
| radial/Gauss maps | CLASSICAL / KNOWN |
| cone-volume measure | CLASSICAL / KNOWN |
| support/pedal/polar/centro-affine ingredients | CLASSICAL / KNOWN |
| angle and angle-squared integral geometry | CLASSICAL |
| radial–normal alignment as shape feature | KNOWN |
| moving observer/reference point | KNOWN |
| global viewpoint-dependent scalar score | KNOWN |
| moving interior-point scalar landscape | KNOWN |
| shape → scalar field → Morse analysis | CLASSICAL / KNOWN |
| rigorous/validated global numerics | KNOWN |
| ellipsoid shape/Weyl chamber | KNOWN |
| cone-volume-weighted radial–normal (L^2) observable (E_K(p)) | DIRECT PRECEDENT NOT FOUND |
| full interior landscape (p\mapsto E_K(p)) | DIRECT PRECEDENT NOT FOUND |
| global critical/Morse classification of this (E_K) | DIRECT PRECEDENT NOT FOUND |
| shape-parameter bifurcation atlas of this (E_K) | DIRECT PRECEDENT NOT FOUND |
| novelty of the preceding four items | NOVELTY NOT YET ESTABLISHED |

## Paper-positioning rule

Do **not** claim novelty for the individual ingredients or for the generic methodology “move a base point / build a landscape / use Morse theory.”

The paper should instead:
1. cite the neighboring literatures explicitly;
2. state their overlap with the present construction;
3. distinguish the specific observable (E_K);
4. make the mathematical results about this specific landscape carry the contribution: stationary branches/orbits, boundary entry, Morse-index changes, degeneracies, and certified global classifications.

A safe summary is:

> The neighboring literatures separately contain radial Gauss geometry, cone-volume measures, radial–normal alignment, angle integrals, moving observation points, viewpoint-dependent scalar scores, and Morse-theoretic landscape analysis. The object studied here is the cone-volume-weighted radial–normal angle landscape over the interior of a convex body, together with its global critical and bifurcation structure.

## Audit rule for future additions

Every literature item added here should be classified as one of:
- **CLASSICAL / KNOWN**
- **PROVEN** (proved in this project)
- **CERTIFIED** (computer-assisted certification completed)
- **DIRECT PRECEDENT NOT FOUND**
- **NOVELTY NOT YET ESTABLISHED**

A search miss must never be promoted to a novelty claim.

## Reference-verification TODO

Before paper submission, replace discovery/search links with primary bibliographic records (publisher/DOI/original paper where available) and verify exact claims against the source text. In particular:
- primary radial-Gauss / cone-volume / Gauss-image references;
- Crofton, Hurwitz, Masotti, Santaló and the modern Cufí–Gallego–Reventós entry point;
- the original density-based 3D shape-descriptor paper using radial–normal alignment;
- Vázquez–Feixas–Sbert–Heidrich (2001) and subsequent viewpoint-quality papers;
- primary source for strict convexity of the Santaló landscape for arbitrary convex bodies;
- representative Morse/shape-analysis references;
- representative validated-numerics/CAP references;
- primary references for determinant-one SPD / (SL(3)/SO(3)) and (A_2) Weyl-chamber description of unit-volume ellipsoids.
