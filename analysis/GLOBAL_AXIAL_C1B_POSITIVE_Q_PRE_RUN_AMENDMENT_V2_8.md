# C1b Pre-Run Amendment v2.8 — Positive-Structure Enclosures for q and q^(-3/2)

Status: PREDECLARED / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent: v2.7.1 clarification at commit dfbe94ad318a763ceb80b6333f9ceeca071eaf2b.
This amendment retains the v2.7 algebraic Gl regrouping and adds the two positive-structure
enclosures required by the canonical stiff corner. No numerical implementation is authorized before
raw audit of this document passes.

## 0. Diagnostic basis and scope

Read-only exploratory evaluation of the canonical coarse-102/depth-3 root box showed that v2.7
removes the removable 1/u division but naive interval evaluation of

    q = e + lambda^2 d^2,       e = 1-mu^2,       d = t-mu

can still enclose negative values because dependency and square non-negativity are lost. Merely
clamping d^2 to a nonnegative interval is insufficient: if d contains zero its true squared lower
bound is zero, and even a certified positive lower bound for q is not by itself enough. Forming
`w*q*sqrt(q)` as successive Arb ball products can again produce an interval containing zero although
all three mathematical factors are strictly positive.

The binding v2.8 repair therefore has two inseparable parts:

1. a certified box minimum `q_box_min` obtained from the geometry of q itself; and
2. direct endpoint evaluation of the positive reciprocal factor `1/(w*q*sqrt(q))`, without forming
   the denominator as a generic ball product.

This amendment does not authorize an additional e/q^(5/2) regrouping. Exploratory diagnostics show
that the two positive-structure enclosures above are sufficient to make all 16 canonical Gl cells
finite and to obtain strict Newton contraction.

## 1. Binding q box-minimum theorem

For

    q(mu,t,lambda) = 1 - mu^2 + lambda^2*(t-mu)^2

on the C1b domain `lambda in [9/20,5/8]`, the following facts are binding:

    d2q/dmu2 = 2*(lambda^2 - 1) < 0,
    d2q/dt2  = 2*lambda^2 > 0,
    dq/dlambda = 2*lambda*(t-mu)^2 >= 0.

Thus q is concave in mu, convex in t, and nondecreasing in positive lambda. The minimum over a
rectangular `(mu,t,lambda)` box is therefore attained at `lambda=lambda_lo`, at one of the two mu
endpoints, and for that fixed mu at the minimizer of `(t-mu)^2` over the t interval. Define

    t_star(mu) = clamp(mu, t_lo, t_hi),
    q_endpoint(mu) = 1 - mu^2 + lambda_lo^2*(t_star(mu)-mu)^2,
    q_box_min = min(q_endpoint(mu_lo), q_endpoint(mu_hi)).

`q_box_min` is the exact mathematical box minimum before outward rounding. It is not
`max(0,q.lower())`, not a generic interval evaluation of q, and not an endpoint-square shortcut for
d when d crosses zero.

The implementation must construct a positive q enclosure whose lower endpoint is no greater than the
outward-rounded `q_box_min` and whose upper endpoint safely contains the existing q enclosure upper
bound. If `q_box_min <= 0` at an authorized evaluation boundary, the code must fail closed through an
explicit diagnostic; it must not invent a positive epsilon.

## 2. Binding positive reciprocal-power enclosure

Where `q_box_min > 0`, q is strictly positive on the whole box. From v2.7.1,

    w2 = lambda^2 + mu^2*(1-lambda^2) >= 81/400 > 0,

so w is also strictly positive. The factor used by `gt` and the regrouped Gl term,

    inv_wq32 = 1/(w*q*sqrt(q)),

must be enclosed as a positive quantity by monotone endpoint evaluation. The implementation must not
obtain it by first forming the generic Arb product `w*q*sqrt(q)` and then dividing by that product.
For positive intervals `w in [w_lo,w_hi]` and `q in [q_lo,q_hi]`, use outward-rounded endpoint values
consistent with

    inv_wq32 in [1/(w_hi*q_hi*sqrt(q_hi)),
                  1/(w_lo*q_lo*sqrt(q_lo))].

The endpoint computation itself must preserve positivity throughout. Equivalent algebra that yields
the same or tighter certified positive hull is permitted only if predeclared before implementation.
No zero-containing denominator ball may be used as an intermediate representation of this factor.

## 3. Authorized implementation boundary

v2.8 is a delta on top of the still-unimplemented v2.7/v2.7.1 source change. The eventual
implementation commit may contain the four source paths already authorized by v2.7.1 plus only the
minimal C1b-local code needed inside those kernel paths to evaluate `q_box_min` and `inv_wq32`.
Shared C0/C0a geometry remains byte-untouched; v2.8 must not repair dependency loss by changing the
shared geometry producer.

The v2.7.1 authorized effects remain binding: `_glam_density` uses the regrouped
`regular_rg_term`, `_R_Rg_endpoint_safe` is removed from imports and endpoint modules,
`_checked_finite` accepts depth directly, and `exterior_cover` remains byte-preserved. The new q and
positive-reciprocal logic is C1b-kernel-local and must be independently transcribed in producer and
checker notation.

No gating, persistence, driver, comparison, monotone, C1a, C1c, BOB, or shared C0/C0a file may change
in the implementation commit. A.1/A.2 schemas, reason serialization, work accounting, refinement
rules, root decision rules, and every existing work ceiling remain unchanged except for a new
fail-closed q-positive diagnostic if required by the implementation.

## 4. Binding exact controls for q_box_min

V28-C1 — exact calculus identities. Using exact rational arithmetic, verify on representative C1b
lambda values that

    d2q/dmu2 = 2*(lambda^2-1) < 0,
    d2q/dt2 = 2*lambda^2 > 0,
    dq/dlambda = 2*lambda*(t-mu)^2 >= 0.

The algebraic identities are exact; no floating tolerance is permitted. The sign assertions are
checked under the frozen C1b domain bounds.

V28-C2 — clamp branch coverage. Exercise both cases of `t_star(mu)`:

- an endpoint mu lying inside `[t_lo,t_hi]`, so `t_star=mu` and the squared term vanishes;
- an endpoint mu lying outside `[t_lo,t_hi]`, so `t_star` is the nearest t endpoint.

Both producer and checker controls must demonstrate the same exact rational q minimum on each control
box.

V28-C3 — lower-bound soundness and negative controls. For each control box, require exact-rational
checks that every sampled interior point satisfies `q(point) >= q_box_min`. Subdivide parent boxes
and require every child `q_box_min >= parent q_box_min`; violation is FAIL. Include d intervals that
cross zero and verify that no endpoint-square rule assigns a positive lower bound to d^2 merely
because both endpoint squares are positive. These are soundness controls, not evidence that random
sampling proves the theorem; the theorem in §1 is the proof.

V28-C4 — canonical exact lower bounds. On the historical coarse-102/depth-3 cell-15 s-panels 0 and 1,
record the exact rational `q_box_min` values and require them to be strictly positive. The exploratory
reference values are approximately

    panel 0: 9.268383695764426e-6,
    panel 1: 9.298133621284376e-6.

The exact rational values, not these decimal renderings, are the binding preflight records.

## 5. Binding controls for the positive reciprocal enclosure

V28-C5 — positive endpoint enclosure. On ordinary and stiff-corner boxes with `q_box_min>0`, compare
the direct positive `inv_wq32` hull against exact-rational/high-precision point evaluations. Every
point value must lie in the hull. The hull lower endpoint must be strictly positive and finite, and
no intermediate denominator representation may contain zero.

V28-C6 — demonstrate necessity of both stages. On the canonical control box, separately record:

(a) naive q evaluation, showing the historical zero-crossing/NaN pathology;
(b) q with the certified positive lower bound but a generic `w*q*sqrt(q)` ball product, showing that
    this product can still contain zero;
(c) q_box_min plus direct positive `inv_wq32`, showing a finite result.

The purpose is to prevent a future simplification from silently deleting either required stage.

## 6. Strengthened canonical regression and diagnostic reference

V28-C7 supersedes only the implementation mechanism underlying V27-C3; its pass criterion remains
strict contraction, not reproduction of a frozen floating ratio. For the exact historical
coarse-102/depth-3 root box:

1. all 16 root t-cell Gl enclosures must be finite;
2. cell 15 s-panels 0 and 1 must be finite;
3. execute the first complete production Newton/MV update;
4. record exact `T_k`, exact `T_next`, exact widths, and the contraction ratio;
5. require `T_next` to be a strict subset of `T_k` and `width(T_next) < width(T_k)`;
6. if the first update already meets `ROOT_TARGET`, record `TARGET_WIDTH` exactly as production does.

The read-only exploratory diagnostic, which is NOT_EVIDENCE, produced

    width(T_k) = 1/8,
    width(T_next) = 474232477/274877906944,
    ratio = 474232477/34359738368
          ~= 0.013801981607684866,

and reached `TARGET_WIDTH` after the first update. These numbers are reference diagnostics only. A
future implementation is not required to reproduce the ratio bit-for-bit; the binding pass condition
remains strict decrease plus all existing root correctness conditions.

## 7. Carry-forward obligations and required sequence

All v2.7.1 obligations not explicitly superseded remain binding, including the intentional g-path
`chart_unresolved` relaxation, local gt equivalence control, `PREDICTOR_NONFINITE` reason separation,
R endpoint range guarantee, w2 positive lower bound, revised diagnostics/C6, moving-u=0 comparison,
dead-code control, numeric import closure, and the four-file implementation boundary.

Before any full Phase-1 rerun, preflight must pass V28-C1 through V28-C7 in both lineages where
applicable. Failure of q positivity, positive reciprocal enclosure, all-16 finiteness, or strict
contraction returns to design adjudication; no third full run is allowed.

Required order:

    v2.7.1 clarification dfbe94ad...
      -> v2.8 predeclare commit
      -> chat verbatim/raw audit PASS
      -> combined v2.7/v2.8 implementation commit
      -> chat raw implementation audit
      -> explicit push approval and push
      -> manifest refresh
      -> preflight including V27 carry-forward and V28-C1..C7
      -> only if preflight PASS: NEW third Phase-1 RUN_DIR
      -> Phase 2 checker -> comparison -> chat adjudication -> receipt.

The historical RUN_DIR `c1b_producer_20260908T091151Z` and every exploratory monkey-patch diagnostic
remain control/diagnostic material only and must never be resumed or cited as numerical certificate
evidence. Until the later sequence completes, this document is PREDECLARED / MACHINE_NOT_RUN /
NOT_EVIDENCE.
