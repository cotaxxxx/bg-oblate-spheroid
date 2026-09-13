# C1b parametric mean-value root-localization pre-run amendment

Status: `PREDECLARED_AMENDMENT / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_BINDING`

This amendment is committed before any implementation of the root-localization change described below. It supersedes only the C1b root-localization procedure in the existing C1 contract stack. It does not alter the C1b domain, predictor, tube width, tube monotonicity gate, wall signs, clamp rules, corner treatment, T0/T1/T2 stages, E0/E1/E2 exterior policy, lambda-refinement rule or depth, accepted/attempted slab caps, Arb precision, strict-sign predicates, or declared work ceilings.

No implementation under this amendment may be used as evidence until producer and checker implementations receive a chat raw audit and all post-audit source/blob pins are fixed in a later manifest commit.

## 1. Reason for the amendment

The first external C1b producer run at HEAD `c0449a341cb1e67942ed1f080626cb758d857c7b` terminated fail-closed on the leftmost coarse slab after exact lambda refinement to depth 3. The terminal slab was

```text
Lambda = [9/20, 2881/6400]
initial root bracket = [9/16, 19/32]
terminal reason = MID_SIGN_UNRESOLVED
```

That ABORT ledger remains historical `NOT_EVIDENCE` and is not resumable. Read-only diagnostics performed outside the ledger showed that the 8192-panel point-evaluation enclosure of `g` has an s-panel integration width floor large enough to prevent the predeclared rigid midpoint-sign localization from reaching width `1/128`. Increasing Arb bit precision does not address that floor.

The same diagnostics showed stable first-order panel convergence for thin-lambda point evaluations and a certified narrow lambda sweep. This amendment therefore replaces midpoint-sign bisection by a parametric mean-value interval enclosure that separates the thin-lambda value from the lambda sweep.

## 2. Replacement root-localization map

For an attempted slab `Lambda=[lambda_l,lambda_r]` and the root bracket `T_k=[a_k,b_k]`, define the exact rational midpoints

```text
lambda_c = (lambda_l + lambda_r)/2
t_ref    = (a_k + b_k)/2
```

At each iteration evaluate independently:

```text
G0 = g(t_ref, lambda_c)                         with 32768 s-panels,
Gt = [partial_t g](T_k x Lambda)               with 8192 s-panels,
Gl = [partial_lambda g](T_k x Lambda)          with 8192 s-panels,
Dlambda = Lambda - lambda_c.
```

The `partial_lambda g` evaluator must implement the already audited fixed-t lambda-derivative algebra with the same removable-locus analytic continuation policy as the C0/C1 kernels. Producer and checker must carry independent transcriptions and may not import one another.

Form the certified parametric numerator enclosure

```text
Gpar = G0 + Gl * Dlambda.
```

The derivative division guard is strict:

```text
upper(Gt) < 0.
```

If that guard is not certified, the iteration is `UNRESOLVED`; no division is permitted.

The next enclosure is

```text
N_k     = t_ref - Gpar / Gt,
T_{k+1} = N_k intersect T_k.
```

The intersection is performed with outward-rounded interval endpoints. If the intersection is empty, the run stops fail-closed with a contradiction/error record; it may not be converted into lambda refinement or acceptance.

Because of the explicit intersection, every successful step satisfies `T_{k+1} subseteq T_k`. No per-step contraction-ratio requirement is imposed.

## 3. Termination and existing lambda refinement

The root-localization target is unchanged:

```text
width(T_*) <= 1/128.
```

The maximum number of parametric mean-value iterations is

```text
ROOT_MV_STEPS = 8.
```

The first iterate satisfying the target is the certified `T_*`. If the target is not reached after 8 iterations, or if any required `G0`, `Gt`, or `Gl` enclosure is unresolved, root localization returns `UNRESOLVED`.

`UNRESOLVED` retains the existing C1b response: exact lambda bisection only, left child before right child, with maximum lambda-refinement depth 3. At depth 3 an unresolved localization is an `ABORT` exactly as before. The new root-localization map does not remove, increase, or weaken the lambda-refinement depth rule.

## 4. Predictor acceptance

The existing predictor-acceptance threshold is unchanged:

```text
|t_c - mid(T_*)| <= 1/64.
```

The numerical threshold `1/64` is unchanged. For this test the representative root location is the exact rational midpoint `t_*^rep = mid(T_*)` of the certified enclosure. A predictor that does not satisfy the threshold causes exact lambda refinement only; the tube width may not be shrunk to evade the threshold.

## 5. Work accounting and ceilings

Every interval integration is charged at its actual s-panel count. For one parametric mean-value iteration the root-localization charge is therefore

```text
G0: 32768
Gt:  8192
Gl:  8192
----------------
total: 49152 panel evaluations.
```

With at most 8 iterations, the maximum new root-localization charge per attempted slab is `393216` panel evaluations. The superseded midpoint-sign root-localization allowance was `12 * 16 * 8192 = 1572864` panel evaluations. The replacement therefore does not require an increase in the predeclared per-attempt, accepted-work, or global-attempted ceilings.

All `G0`, `Gt`, and `Gl` work, including work from an ultimately unresolved iteration, is added to the existing root component and then to the existing cumulative attempt/global accounting. Interrupted-attempt charging, attempt caps, accepted caps, and all existing resumable-ledger accounting rules remain unchanged.

No work may be omitted because an interval later becomes empty, unresolved, refined, or aborted.

## 6. Development regression smoke

Before any post-audit manifest is created, both producer and checker implementations must run a non-evidence regression smoke on the historical failure box

```text
Lambda = [9/20, 2881/6400]
T_0    = [9/16, 19/32].
```

The smoke must exercise the exact new parametric mean-value code path, including the 32768-panel thin-lambda `G0`, the 8192-panel `Gt` and `Gl` enclosures, the strict `upper(Gt)<0` division guard, interval intersection, empty-intersection failure path, and work accounting. It is a development regression, not a C1b mathematical gate and not machine evidence.

Reported diagnostic expectation only, not a gating decimal:

```text
pre-implementation diagnostic step-1 width approximately 1.126e-2,
pre-implementation diagnostic step-2 width approximately 6.292e-3,
expected target attainment in about 2--3 iterations.
```

If either lineage fails to reach `1/128` on this regression box, implementation does not advance to the post-audit manifest. The contract is not weakened to accommodate the failure.

## 7. Reported depth expectation — not gating

Read-only diagnostics predict that lambda-width contribution is relevant near the left endpoint. Coarser left-edge slabs may remain too wide for the mean-value enclosure, while depth-2 or depth-3 descendants should enter the localization regime. This is expected behavior and does not authorize any increase of `MAX_DEPTH=3`.

Any numerical width or depth estimate in this section or the regression-smoke expectation is `REPORTED / NON_GATING`. Only the exact interval predicates and limits stated above are binding.

## 8. Producer/checker audit requirements

The raw audit before implementation pinning must verify, for both lineages:

```text
exact rational construction of lambda_c and t_ref,
G0 uses a thin lambda point and exactly 32768 s-panels,
Gt encloses partial_t g on T_k x Lambda with exactly 8192 s-panels,
Gl encloses partial_lambda g on T_k x Lambda with exactly 8192 s-panels,
upper(Gt) < 0 is checked before any interval division,
Gpar = G0 + Gl*(Lambda-lambda_c) is assembled with outward-rounded Arb arithmetic,
N_k = t_ref - Gpar/Gt,
T_{k+1} = N_k intersect T_k,
empty intersection is a fail-closed error,
maximum iteration count is exactly 8,
width target is exactly 1/128,
UNRESOLVED returns to the unchanged exact lambda-bisection/depth-3 policy,
predictor acceptance remains exactly 1/64,
all three integrations are charged by actual panel count,
producer and checker implementations are independent transcriptions.
```

The producer/checker comparison record must include, step by step, `T_k`, `t_ref`, `lambda_c`, the canonical `mid/rad/lower/upper` forms of `G0`, `Gt`, `Gl`, `Gpar`, `N_k`, and the exact interval endpoints of `T_{k+1}`, widths, guards, iteration count, work, and final `T_*`. Any disagreement is fail-closed.

## 9. Required sequence after this amendment

After this PREDECLARED amendment commit, no machine evidence run may begin until the following sequence completes:

```text
1. chat raw audit of this amendment;
2. producer and checker implementation plus the regression smoke;
3. chat raw audit of the implementation and smoke output;
4. a new post-audit manifest pinning the amendment and all changed source blobs;
5. fresh environment preflight;
6. fresh C1c calibration under the pinned driver/environment;
7. a new, previously nonexistent producer RUN_DIR, followed later by an independent checker RUN_DIR.
```

The historical ABORT ledger and the read-only diagnostics that motivated this amendment remain immutable historical controls and must be referenced in the eventual receipt. They may not be relabelled as evidence or reused as a resumable run.
