# D-OB P2 — D-AN-1 L2 Paired Representation and Axis Extension — DRAFT

**Status:** PAPER-PROOF DRAFT / AWAITING CHAT AUDIT / NOT A THEOREM
**Frozen parent:** `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_1.md`, commit `6de8a178b3f9c278952ac68590f97f3f100ed9f9`, SHA-256 `1461fc081c99cfd820792248bc2f6fe2401a182a8a4941df46a4288f49f8cc78`, **FROZEN** by chat countersign.
**Normative premise annex:** `analysis/D_OB_P2_D_AN1_L2_MRA_DRAFT.md`, commit `4e60b1ed32f862455450d38af6a5e440c64aa3ec`, SHA-256 `7e0337379bff33ef3ba63e71069287cb849aad9de688c466775ef68f31cb3185`, **AUDIT PASS**.
**P1 source:** commit `6c6282a8`, file `analysis/D_OB_P1_DESIGN_NOTE.md`, SHA-256 `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`.

## 1. Claim

For fixed `lambda in [2/5,93/200]` and `(rho,z) in M_lambda`, the pinned `K_H` representation of P1 may be written on the half azimuth `phi in [0,pi)` by pairing the surface points with azimuths `phi` and `phi+pi`. For `rho>0`, writing

`a=sqrt(1-mu^2)`, `b=a cos(phi)`,

the pointwise centered kernel obeys

`K_H(rho,z;mu,phi) = [F_rho(rho,b)+F_rho(rho,-b)]/(2 rho)`,

and hence, with

`K_pair(rho,z;mu,phi) := K_H(rho,z;mu,phi)+K_H(rho,z;mu,phi+pi)`,

we have

`H(rho,z) = (1/(4 pi lambda)) integral_{-1}^{1} integral_0^pi K_pair dphi dmu`.

The paired representation introduces no new analytic assumption. Its absolute integrability is inherited from P1 §8.2. It is compatible with the inherited continuous extension

`H(0,z)=E_rhorho(0,z)`

of P1 Lemma 6.1(iii). No sign at `(0,lambda)` is asserted here; that is the separate frozen NP-T obligation.

## 2. Pinned identities used

From P1 §1, for `p=(rho,0,z)` and the boundary point `x(mu,phi)`, verbatim source definitions give

> `D = |x - p|,     h = w (x - p).nu,     gamma = h/(w D),     alpha = arccos(gamma),     R = alpha/sin(alpha),`
>
> `E(p) = (1/(4 pi lambda)) integral_{bd K} F dA/w,     F := h alpha^2.`

and P1 states

> `h = lambda (1 - rho b) - z mu` with `b = a cos phi`.

P1 §8.1 also gives

> `D^2 = D0 - D1 cos phi`

with `D1=2 rho a`; equivalently the `rho,phi` dependence of `D^2` is through `rho b` and `rho^2`.

From P1 §8.2, verbatim:

> `H(rho, z)        = (1/(4 pi lambda)) integral integral K_H dphi dmu,`
>
> `K_H(rho, z; mu, phi) := [ F_rho(rho, b) - F_rho(-rho, b) ] / (2 rho)   (rho > 0),`
>
> `K_H(0, z; mu, phi)   := F_rhorho(0, b),`

and

> `(i) since E_rho is odd in rho, (1/(4 pi lambda)) integral integral K_H = [E_rho(rho, z) - E_rho(-rho, z)]/(2 rho) = H(rho, z); (ii) K_H(rho) = (1/(2 rho)) integral_{-rho}^{rho} F_rhorho(s, b) ds;`

The P1 §8.2 property (iii) supplies uniform absolute integrability of `K_H`, including `rho -> 0`.

## 3. Pointwise azimuthal reflection identity

Fix `mu,z,lambda`. Regard the density as `F(rho,b)` with `b=a cos(phi)`.

Under simultaneous replacement `(rho,b)->(-rho,-b)`, the product `rho b` and `rho^2` are unchanged. Therefore the explicit formulas above give

`h(-rho,-b)=h(rho,b)`,

`D(-rho,-b)=D(rho,b)`.

Consequently `gamma`, `alpha^2`, and hence the density itself are unchanged:

`F(-rho,-b)=F(rho,b)`.                                      (3.1)

Equivalently, replacing `b` by `-b`,

`F(-rho,b)=F(rho,-b)`.                                      (3.2)

For points where the ordinary `rho` derivative is taken, differentiate (3.2) with respect to `rho`. The left side has the chain-rule sign from its argument `-rho`, so

`-F_rho(-rho,b)=F_rho(rho,-b)`,

or

`F_rho(-rho,b)=-F_rho(rho,-b)`.                             (3.3)

Substitution into the pinned centered-difference definition yields, for `rho>0`,

`K_H(rho,z;mu,phi)=[F_rho(rho,b)+F_rho(rho,-b)]/(2 rho)`.    (3.4)

This is an algebraic consequence of the pinned density and does not assume an additional symmetry theorem.

## 4. Half-azimuth pairing

Split the full azimuth integral exactly:

`integral_0^{2pi} K_H(phi) dphi = integral_0^pi K_H(phi) dphi + integral_pi^{2pi} K_H(phi) dphi`.

In the second integral put `phi'=phi-pi`. Then `phi' in [0,pi]`, `dphi=dphi'`, and

`cos(phi'+pi)=-cos(phi')`, hence `b(phi'+pi)=-b(phi')`.

Therefore

`integral_0^{2pi} K_H(phi) dphi`

`= integral_0^pi [K_H(phi)+K_H(phi+pi)] dphi`

`= integral_0^pi K_pair(phi) dphi`.                         (4.1)

Combining (4.1) with the pinned full-azimuth representation gives

`H(rho,z)=(1/(4 pi lambda)) integral_{-1}^{1} integral_0^pi K_pair(rho,z;mu,phi) dphi dmu`.  (4.2)

Using (3.4), the pair may if desired be written explicitly as

`K_pair = [F_rho(rho,b)+F_rho(rho,-b)]/rho`.                (4.3)

Indeed the expression in (3.4) is itself unchanged by `b->-b`, so the two half-turn terms are equal. Formula (4.3) is only an algebraic rewriting; no positivity of either summand is asserted.

## 5. Absolute integrability

P1 §8.2(iii) gives absolute integrability of `K_H` on the full parameter surface, uniformly in `rho` down to `rho=0`. Hence by the triangle inequality

`|K_pair(phi)| <= |K_H(phi)|+|K_H(phi+pi)|`.

The change of variables in §4 preserves Lebesgue measure. Thus

`integral_{-1}^{1} integral_0^pi |K_pair| dphi dmu`

`<= integral_{-1}^{1} integral_0^{2pi} |K_H| dphi dmu < infinity`.

Therefore the split, substitution, and recombination above are legitimate. No new majorant or interchange assumption is introduced by azimuthal pairing.

## 6. Compatibility with rho=0 and the axis identity

The normative L2-MRA dispositions R1 and R2 apply directly. Lemma V(b)(c) supplies the interior second derivative and its continuous closure value `E_rhorho`. P1 Lemma 6.1(iii) already states, verbatim,

> `H(rho, z) := integral_0^1 E_rhorho(tau rho, z) dtau` is continuous on `M_lambda`, satisfies `H = E_rho/rho` for `rho > 0`, and `H(0, z) = E_rhorho(0, z)`.

Thus (4.2) represents the same inherited `H` for every `rho>0`, while its axis value is fixed by the unique continuous extension

`H(0,z)=E_rhorho(0,z)`.                                    (6.1)

No separate `t`-derivative/interchange theorem is required to obtain (6.1). In particular the domain-inapplicable C2 interchange lemma `f66ffe5a` is not used.

At the north-pole anchor,

`H(0,lambda)=E_rhorho(0,lambda)`,                           (6.2)

but L2 makes **no sign claim** for this value. The strict sign in (6.2) is precisely NP-T, an independent internal node in frozen v1.1.

## 7. Dependency and scope closure

L2 has used only:

1. the pinned P1 density and `K_H` definitions/properties;
2. Lemma V(b)(c) for the continuous closure second derivative;
3. Lemma 6.1(i)-(iii) for rho symmetry and the continuous `H` axis identity;
4. the normative L2-MRA premise classification.

No Phase 0, N7, B44, diagnostic margin, interval computation, endpoint C1 sign, C2 interchange statement, or NP-T sign has been used. Hence the frozen L2 target is discharged conditional only on the inherited P1/Lemma-V audit dependency already declared by D-AN-1 v1.1.
