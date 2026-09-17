# C1b Pre-Run Amendment v2.7 — Algebraically Regrouped Gl Density at the Removable u-Denominator

Status: PREDECLARED / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_EVIDENCE.
Scope: only the C1b `_glam_density` evaluation in both lineages and the now-unused C1b Rg helper.
The endpoint-safe R primitive and the v2.6 non-finite diagnostics remain in force. Existing shared
C0/C0a/C1a/C1c/BOB/monotone evaluators are byte-untouched by this amendment.

## 0. Canonical diagnostic control — second blocker exposed after the v2.6 tube fix

Historical run `c1b_producer_20260908T091151Z` is retained unchanged and is not resumable.
At coarse 102, depth 3, lambda in [231/400, 3697/6400], the v2.6 tube stage passes T0 with
`nonfinite 0`, `gt_bad 0`, `left_bad 0`, `right_bad 0`; representative certified margins are
`gt_worst_upper < -0.669`, `left_worst_lower > +0.050`, and `right_worst_upper < -0.062`.
This fixes the old right-wall NaN class of the earlier attempt-154 control: the old NaN blocker is
therefore closed and is not reopened by v2.7.

The new failure occurs only after the tube pass, in root localization step 1. For each refinement
depth 0, 1, 2, 3, the C1b Gl path reports
`R_ENDPOINT_DIRECT_BRANCH_ZERO_DENOMINATOR`, then
`MV_NONFINITE_ENCLOSURE`; depth 3 therefore fails closed and ABORTs.

Read-only isolation of the depth-3 root box identifies the offending location as t-cell 15, at the
`t_p` side, and s-panels 0 and 1, i.e. the stiff corner s -> 0, t -> 1 in the canonical lambda band.
At the same cell/panels, the legacy R/Rg path raises its unresolved-chart ValueError. This establishes
that the new ABORT is not a regression introduced by endpoint-safe R: the same blocker was latent in
the predecessor path and was previously hidden behind the earlier tube NaN.

A t-cell half split removes the explicit zero-denominator guard, but the right half of the whole
`glam_box` remains non-finite. Splitting is therefore not a cure: after the guard disappears, direct
ball division in `Rg = (gamma*R - 1)/u` still carries the same removable singularity as unbounded
interval width. No subdivision-only repair is permitted by this amendment.

## 1. Binding algebraic regrouping of the C1b Gl density

Use the existing C0/C0a geometry symbols, without modifying their definitions:

    d  = t - mu
    e  = 1 - mu*mu
    l2 = lam*lam
    A  = 1 - t*mu
    q  = e + l2*d*d
    w2 = mu*mu + l2*e
    w  = sqrt(w2)
    sq = sqrt(q)
    gamma = lam*A/(w*sq)
    h = mu*(1-l2) + l2*t
    u = e*h*h/(w2*q)                 # mathematical identity before enclosure clamping
    N = -mu*q - A*l2*d

The following three identities are binding mathematical controls of v2.7, not numerical guesses.
They are checked exactly over rational test points in preflight, including stiff-corner points.

First,

    h = mu + l2*d,
    mu*d + A = e,
    N = -e*h.

Second, with

    k = mu - l2*d,

one has

    1/lam - lam*e/w2 - lam*d*d/q
      = e*h*k/(lam*w2*q),

and therefore

    gamma_lam = gamma * e*h*k/(lam*w2*q).

Third, since

    gt = lam*N/(w*q*sq) = -lam*e*h/(w*q*sq),
    u  = e*h*h/(w2*q),

then wherever u > 0,

    gamma_lam*gt/u = -gamma*e*k/(w*q*sq),

hence

    Rg*gamma_lam*gt
      = ((gamma*R - 1)/u) * gamma_lam*gt
      = -(gamma*R - 1) * gamma*e*k/(w*q*sq).

The right-hand side contains no division by u. It has the same denominator order
`1/(w*q*sqrt(q))` already present in `gt`, and carries an explicit factor e at the stiff corner.
For u > 0 it is algebraically identical to the legacy expression; both sides have the same continuous
extension to u = 0 through the regrouped right-hand side. The regrouped expression is therefore the
binding C1b evaluation of this product on the full enclosure domain, including boxes that contain
u = 0.

The C1b `_glam_density` in each lineage is changed only at this one product. In mathematical
pseudo-source the binding form is:

    R = _R_endpoint_safe(u, stats)
    wl_over_w = lam*e/w2
    gamma_lam = gamma * (1/lam - wl_over_w - lam*d2/q)
    L = lam/(w*q*sq)
    N_lam = -2*lam*(mu*d2 + A*d)
    L_lam = L * (1/lam - wl_over_w - 3*lam*d2/q)
    gt = L*N
    gt_lam = L_lam*N + L*N_lam
    k = mu - l2*d
    regular_rg_term = -(gamma*R - 1) * gamma*e*k/(w*q*sq)
    return s * (2*mu*R*gamma_lam - 2*A*(regular_rg_term + R*gt_lam))

`gt_lam` and all of its current definitions remain unchanged. In particular, v2.7 does not replace,
refactor, or otherwise broaden the change around `N_lam`, `L_lam`, `gt`, or `gt_lam`. The regrouping
is limited to the former `Rg*gamma_lam*gt` product.

Because glam now needs R but not Rg, glam uses `_R_endpoint_safe` for all u. There is no glam-side
series/direct Rg chart, no glam-side zero-denominator guard, and no division by u. The endpoint-safe
Rg design is explicitly rejected for v2.7: the removable singularity belongs to the product, not to
Rg as a standalone interval quantity.

## 2. Exact implementation boundary and dead-code rule

Only these implementation effects are authorized:

1. `producer/global_axial_c1b_kernel.py`: change only `_glam_density` as specified in §1.
2. `checker/global_axial_c1b_kernel.py`: independent transcription of the same mathematical change,
   using the checker lineage's existing symbol names.
3. `producer/global_axial_c1b_endpoint_r.py`: delete `_R_Rg_endpoint_safe` because no authorized C1b
   call site may use it after this amendment.
4. `checker/global_axial_c1b_endpoint_r.py`: delete the corresponding checker helper for the same
   dead-code reason.

`_R_endpoint_safe`, `R_point`, and `REndpointDomainGuard` remain. No shared C0/C0a primitive,
geometry, series implementation, monotone evaluator, BOB evaluator, C1a evaluator, or C1c evaluator
is modified. In particular the pinned C0/C0a source blobs remain the source of the definitions used
in §1; v2.7 consumes those definitions but does not rewrite them.

The g density, gt density, tube logic, exterior logic, root subdivision/localization mechanism,
predictor selection mechanism, refinement rules, decision rules, and work accounting remain
unchanged. A.1 remains exactly the 15-key producer schema, replay exactly the 16-key schema, and
comparison `A1_KEYS` exactly the 14-key set. No A.1 key is added, removed, renamed, or reinterpreted.
Logical panel/cell charging and every existing work ceiling remain unchanged because the amendment
changes only algebra inside an already charged density evaluation.

## 3. Explicit supersession of the v2.6 Rg obligations

This amendment supersedes only the following v2.6 obligations, and is their sole binding replacement
for C1b glam evaluation:

- v2.6 §1 statements that `_glam_density` takes R and Rg from `_R_Rg_endpoint_safe`, that the Rg path
  preserves the legacy small-u/moving-u=0 series branch bit-for-bit, and that its direct branch uses
  `Rg = (gamma*R - 1)/u` guarded by `u.lower() > 0`;
- v2.6 C5b, whose purpose was to prove that the moving-u=0 Rg series path was not disturbed.

Those requirements are removed because the glam path no longer evaluates Rg at all.
`_R_Rg_endpoint_safe` must not survive as unused alternate C1b code.

Replacement C5b is:

    On representative boxes in the legacy series region, including a box containing the moving
    u = 0 locus, evaluate the legacy bundle glam term and the v2.7 regrouped glam term wherever the
    legacy result is finite. Their enclosures must intersect in both lineages. The v2.7 result must
    remain finite on the full control box, including the moving-u=0 enclosure.

C6 is correspondingly amended only for its expected glam behavior. The C1b glam path must no longer
produce `R_ENDPOINT_DIRECT_BRANCH_ZERO_DENOMINATOR`; a synthetic test that reaches the former
zero-denominator geometry must complete through the regrouped path. Endpoint/domain guards that are
still reachable through R itself remain fail-closed and retain the existing v2.6 conversion and
recording semantics at their authorized C1b boundaries. Plain Arb non-finite diagnostics and
unrelated RuntimeError propagation requirements remain unchanged.

All other v2.6 obligations remain in force, including endpoint-safe R, the explicit non-finite
recording layer, worst-tracker rules, work accounting, numeric import-closure verification, and the
controls not expressly replaced above.

## 4. Predeclared controls

V27-C1 — exact algebraic identities. At multiple exact rational points spanning the ordinary region
and stiff-corner samples, verify exactly:

    N == -e*h
    mu*mu*q - l2*d*d*w2 == e*h*k
    (the cross-multiplied form of gamma_lam*gt/u)

No floating tolerance is permitted in this control. The third identity is checked after clearing all
nonzero denominators, so no control evaluation itself divides by u.

V27-C2 — legacy finite-grid agreement. On a representative grid where the legacy glam evaluation is
finite, the legacy and regrouped whole-density enclosures intersect. Zero disjoint cases are
permitted. This is run separately in producer and checker lineages.

V27-C3 — canonical regression. For coarse 102, depth 3, lambda [231/400, 3697/6400], and the exact
root-localization T_k used by the failed historical run, evaluate all 16 root t-cells. Every
`glam_box` must be finite. In particular t-cell 15 and its s-panels 0 and 1 must be finite under the
new path. The control then executes the canonical root step far enough to demonstrate progress past
the former step-1 `MV_NONFINITE_ENCLOSURE`; reproducing that reason at the former location is FAIL.

V27-C4 — revised diagnostics/C6. Exercise the five existing guard-boundary classes with the guards
that remain reachable, verify their v2.6 fail-closed records, verify unrelated RuntimeError still
propagates, and separately exercise the former glam zero-denominator geometry to prove that it now
returns a finite regrouped density and emits no `R_ENDPOINT_DIRECT_BRANCH_ZERO_DENOMINATOR`.

V27-C5 — replacement moving-u=0 control. On the replacement C5b box of §3, require finite regrouped
glam through u = 0 and enclosure intersection with the finite legacy result on every subbox where the
legacy chart resolves.

V27-C6 — dead-code and boundary control. No C1b kernel imports or references
`_R_Rg_endpoint_safe`; the helper is absent from both lineage endpoint modules; `_R_endpoint_safe`
remains present and is the only new R-family helper used by `_glam_density`. The shared C0/C0a,
monotone, C1a, C1c and BOB files are byte-identical to their pre-v2.7 pinned blobs.

The existing v2.6 numeric import-closure control remains binding and must be rerun after implementation
with the new expected C1b blobs. Any closure mismatch remains a hard preflight failure.

## 5. Required sequence and evidence status

The binding sequence is:

    v2.7 predeclare commit
      -> chat verbatim/raw audit of this predeclare
      -> implementation commit
      -> chat raw implementation audit
      -> explicit push approval and push
      -> refresh fixed-schema manifest
      -> preflight including the amended controls
      -> NEW Phase 1 RUN_DIR, full producer rerun from the beginning
      -> Phase 2 checker
      -> cross-lineage comparison
      -> chat comparison adjudication
      -> receipt stamping/signing

No implementation commit is authorized before the predeclare raw audit passes. Push and tag
operations remain explicit-approval-gated. The failed RUN_DIR
`c1b_producer_20260908T091151Z` is historical control only and must never be resumed. The next full
producer run is a new RUN_DIR and is the third full Phase 1 run in this repair sequence.

Until every later step completes, this document is PREDECLARED / MACHINE_NOT_RUN / NOT_EVIDENCE and
must not be cited as a numerical certificate.
