# C1b Pre-Run Amendment v2.7.1 — Clarifications for Regrouped Gl Density

Status: PREDECLARED_CLARIFICATION / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_EVIDENCE.
Parent amendment: v2.7 at commit d423901cfe3bedf5ca17d1faa41b876365b9ff8f.
This clarification resolves the implementation-boundary ambiguity and strengthens the analytic and
preflight obligations before any v2.7 implementation begins.

## 0. Scope and supersession discipline

v2.7 remains the governing regrouping amendment except where this document explicitly clarifies or
corrects it. No numerical implementation is authorized before raw audit of this clarification passes.
The existing v2.6 implementation is retained as the implementation baseline; v2.7 is applied as a
minimal delta on top of that lineage and is not a rewrite from the pre-v2.6 parent.

## 1. Exact algebraic correction and singular-order statement

The binding identities remain:

    h = mu + l2*d,
    k = mu - l2*d,
    N = -e*h,
    mu*mu*q - l2*d*d*w2 = e*h*k,
    gamma_lam*gt/u = -gamma*e*k/(w*q*sqrt(q)).

The second displayed identity is the denominator-cleared factorization used to establish the
`gamma_lam` bracket; the third is its consequence after multiplication by `gt` and division by `u`
on u > 0, followed by continuous extension through the regrouped expression.

The v2.7 sentence claiming that the regrouped term has the same denominator order as `gt` is
superseded. Since

    gamma = lam*A/(w*sqrt(q)),

`regular_rg_term = -(gamma*R - 1)*gamma*e*k/(w*q*sqrt(q))` may contain q-dependence through gamma in
addition to the explicit denominator. Expanding only for singular-order bookkeeping, the strongest
q-power carried by the gamma-containing factor is of order q^(-5/2) before numerator cancellations.
This is NOT a new singularity introduced by v2.7: the regrouped term is algebraically identical to
the legacy product wherever u > 0. The only singularity removed by v2.7 is the removable `1/u`
factor. Any q-singularity is the same legacy q-structure, now exposed without the artificial u
ball-division pathology.

Across the full C1b lambda domain, not merely the canonical diagnostic band,

    w2 = mu*mu + l2*e = l2 + mu*mu*(1-l2),
    lambda in [9/20, 5/8],

so `w2 >= lambda^2 >= (9/20)^2 = 81/400 = 0.2025`. Therefore w2 = 0 is impossible anywhere in the
C1b domain. The only denominator singular set that remains to be controlled is q = 0, which is
already present in the legacy `gt`/Gl structure and is not created by the regrouping.

## 2. Endpoint-safe R range and intentional chart relaxation

`R(u)` is continuous and strictly increasing on [0,1]. Therefore for any mathematically clamped
u-enclosure [u_lo,u_hi], `_R_endpoint_safe` returns the exact range hull

    [R(u_lo), R(u_hi)]

up to outward endpoint rounding. Removing the glam-side legacy R/Rg chart cannot widen the true R
range relative to a valid legacy chart enclosure; it may only preserve or tighten the R enclosure.

The g path continues to use `_R_endpoint_safe` directly. This intentionally evaluates boxes that the
legacy R/Rg chart could reject with `chart_unresolved`/ValueError. That change in evaluability is
binding and deliberate: for R alone, the certified monotone endpoint enclosure replaces the legacy
chart restriction. No claim of bit-identical legacy chart coverage is made for g.

The v2.6 direct-branch Rg counter obligation disappears because `_R_Rg_endpoint_safe` is removed from
the C1b glam path and deleted as dead C1b code.

## 3. Exact authorized implementation delta

To remove the v2.7 ambiguity between "change only `_glam_density`" and the required dead-import
cleanup, the authorized delta is exactly:

1. `producer/global_axial_c1b_kernel.py`
   - replace only the former `Rg*gamma_lam*gt` evaluation inside `_glam_density` by the v2.7
     regrouped `regular_rg_term`;
   - change the endpoint import tuple to remove `_R_Rg_endpoint_safe`;
   - simplify `_checked_finite` to accept `depth` directly instead of a slab object, and update only
     its existing call sites (`slab.depth` in tube calls, existing `depth` in exterior calls).
2. `checker/global_axial_c1b_kernel.py`
   - independent transcription of the same three effects using checker symbol names.
3. `producer/global_axial_c1b_endpoint_r.py`
   - delete `_R_Rg_endpoint_safe`;
   - update only the module docstring if needed to remove the obsolete `Rg` description.
4. `checker/global_axial_c1b_endpoint_r.py`
   - the corresponding deletion and optional docstring cleanup.

No other source file may change in the v2.7 implementation commit. In particular, shared C0/C0a,
monotone, C1a, C1c, BOB, gating, persistence, driver, and comparison files are byte-preserved.
`exterior_cover` already returns four values on every path, including EMPTY_REMAINDER; that v2.6 fix
is carried forward unchanged and must not be reimplemented in v2.7.

The `_checked_finite(depth)` change is explicitly non-mathematical: it removes the synthetic
`type("S", (), {"depth": depth})()` object creation in `eval_exterior` without changing diagnostics,
reason codes, work, decisions, or serialized schema.

## 4. Carry-forward controls from v2.6 raw audit

The following obligations remain binding after the v2.7 regrouping:

A. g-path chart relaxation control. Exercise a box for which the legacy R/Rg chart reports
`chart_unresolved`/ValueError while `_R_endpoint_safe` returns a finite R enclosure; require the C1b
g density to remain finite and record that this is the intended relaxation, not a silent branch
mismatch.

B. gt equivalence control. Because both C1b kernels retain a local `_g_density_stable`, compare its
local

    gt = lam*N/(w*q*sqrt(q))

(producer notation; checker transcribed notation) against the pinned lineage geometry/base gt on a
representative grid, including the canonical stiff-corner neighborhood. Require enclosure
intersection/equality as appropriate and zero disjoint cases.

C. predictor non-finite reason separation. Predictor guard or Arb non-finite samples remain a
separate terminal reason `PREDICTOR_NONFINITE`, with immediate scan termination, no inferred sign
change across the failed sample, and no conflation with ordinary `PREDICTOR` or
`PREDICTOR_ACCEPT` failure.

The former direct-branch counter obligation is removed with `_R_Rg_endpoint_safe` and is not carried
forward.

## 5. Strengthened V27-C3 — finite is insufficient; strict root contraction is required

The v2.7 canonical-regression control is strengthened. It is not enough for all 16 canonical
`glam_box` t-cells to become finite or merely to advance beyond the former step-1
`MV_NONFINITE_ENCLOSURE`.

For the exact coarse-102/depth-3 canonical root box from historical RUN_DIR
`c1b_producer_20260908T091151Z`, preflight must:

1. evaluate all 16 root t-cells and require every `glam_box` finite, including t-cell 15 and the
   s-panels 0 and 1 responsible for the historical blocker;
2. execute the first complete Newton/MV root update using the production root mechanism;
3. record exact `T_k`, exact candidate/intersection `T_next`, their exact widths, and a contraction
   ratio diagnostic;
4. require strict containment/contraction:

       T_next subset T_k,
       width(T_next) < width(T_k).

Equality of widths, an unchanged interval, `ROOT:MAX_STEPS`, or a return to
`MV_NONFINITE_ENCLOSURE` at the canonical first update is FAIL. The contraction ratio is recorded for
both lineages; no fixed numerical ratio threshold beyond strict decrease is imposed by this
clarification unless a later predeclared amendment strengthens it before implementation.

This control is a preflight gate specifically to detect the case in which v2.7 merely converts a
non-finite Gl enclosure into a finite but uselessly wide enclosure. A failure here returns to design
adjudication before any third full Phase-1 run is allowed.

## 6. Remaining v2.7 controls and sequencing

V27-C1 exact rational identities remains binding, with the identity ordering clarified by §1.
V27-C2 legacy finite-grid whole-density intersection remains binding.
V27-C4 revised diagnostics/C6 remains binding, with the glam zero-denominator guard expected to be
unreachable because glam no longer evaluates Rg.
V27-C5 replacement moving-u=0 control remains binding.
V27-C6 dead-code/boundary control remains binding and additionally checks that only the four source
paths authorized in §3 differ from this clarification commit's parent implementation tree.
Numeric import-closure verification remains binding after implementation with refreshed expected
C1b blobs.

Required order is unchanged except that this clarification is now inserted before implementation:

    v2.7 predeclare d423901...
      -> v2.7.1 clarification commit
      -> chat verbatim/raw audit PASS
      -> v2.7 implementation commit
      -> chat raw implementation audit
      -> explicit push approval and push
      -> manifest refresh
      -> preflight including strengthened V27-C3
      -> only if preflight PASS: NEW third Phase-1 RUN_DIR
      -> Phase 2 checker -> comparison -> chat adjudication -> receipt.

The historical RUN_DIR `c1b_producer_20260908T091151Z` remains control only and must not be resumed.
Until the later sequence completes, this clarification is PREDECLARED / MACHINE_NOT_RUN /
NOT_EVIDENCE.
