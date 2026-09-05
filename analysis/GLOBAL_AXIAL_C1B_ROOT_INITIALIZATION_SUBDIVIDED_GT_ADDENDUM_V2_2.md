# C1b root initialization and subdivided-Gt addendum v2.2

Status: `PREDECLARED_ADDENDUM / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_BINDING`

This addendum is committed before the correction implementation. It supplements the PREDECLARED parametric mean-value root-localization amendment and addendum v2.1. The v2.1 three-layer comparison rule, checker replay obligation, and fail-closed semantics remain unchanged.

This addendum changes only two root-localization details: the exact initial root bracket and the construction of the `Gt` denominator enclosure. All other C1b gates and limits remain as previously declared.

## 1. Exact initial bracket

For every attempted producer slab, after the predictor and tube stage have fixed `t_c`, define

```text
t_minus = max(1/2, t_c - W0),
t_plus  = min(1,   t_c + W0),
W0      = 1/16,
T_0     = [t_minus, t_plus].
```

`t_c`, `W0`, `t_minus`, `t_plus`, and `T_0` are exact rationals. The construction is exactly the same clamp construction used by `tube_stage`; it is therefore lineage-independent and belongs to the v2.1 `A1_EXACT_EQUALITY` layer.

If `t_plus=1`, every `Gt` subcell touching `t=1` inherits the existing mandatory `corner_hull` treatment. This addendum does not weaken or replace the existing corner rule.

## 2. Subdivided `Gt` enclosure

At parametric mean-value iteration `k`, let the current certified interval be the exact-rational interval

```text
T_k = [a_k,b_k].
```

Set the single declared subdivision constant

```text
ROOT_GT_T_CELLS = 16.
```

Partition `T_k` uniformly into exactly 16 exact-rational t-cells. On each cell `J_j`, evaluate

```text
Gt_j = [partial_t g](J_j x Lambda)
```

with exactly 8192 s-panels, using the existing ordinary/corner chart policy. Define the denominator enclosure

```text
Gt_hull = hull_j(Gt_j).
```

The strict division guard is

```text
upper(Gt_j) < 0 for every j=1,...,16.
```

This is equivalent to `upper(Gt_hull)<0`. If any cell fails to certify the strict sign, no division is permitted and root localization returns `UNRESOLVED`, with the existing response of exact lambda bisection only and maximum refinement depth 3.

The parametric mean-value numerator is unchanged:

```text
lambda_c = exact midpoint of Lambda,
t_ref    = exact midpoint of T_k,
G0       = g(t_ref,lambda_c) with 32768 s-panels,
Gl       = [partial_lambda g](T_k x Lambda) with 8192 s-panels,
Gpar     = G0 + Gl*(Lambda-lambda_c).
```

The Newton image is now formed with the subdivided denominator hull:

```text
N_k     = t_ref - Gpar/Gt_hull,
T_{k+1} = N_k intersect T_k.
```

The empty-intersection rule, outward-rounded endpoint rule, target `width(T_*)<=1/128`, and maximum `ROOT_MV_STEPS=8` are unchanged.

`ROOT_GT_T_CELLS=16` and `T_0` are `A1_EXACT_EQUALITY` quantities. The individual 16-cell partition of a later `T_k`, and the resulting `Gt_j` and `Gt_hull` interval values, are lineage-derived because `T_k` may differ between producer and checker; they therefore belong to `A2_LINEAGE_INDEPENDENT` under addendum v2.1 §C.

For avoidance of ambiguity, the v2.1 A.1 requirement to match the identity of `corner_hull` boxes continues to apply to the pre-existing tube-stage boxes. The new root-localization `Gt_j` cells are A.2 lineage-derived cells; each lineage must independently apply the unchanged corner rule to any such cell touching `t=1`, but exact equality of those lineage-derived cell endpoints is not required.

## 3. Work accounting and ceilings

Every interval integration is charged at its actual s-panel count. With `ROOT_GT_T_CELLS=16`, one mean-value iteration is charged as

```text
G0:              32768
Gt: 16 * 8192 = 131072
Gl:               8192
-----------------------
total:          172032 panel evaluations.
```

At the unchanged maximum of 8 iterations, the root-localization maximum is

```text
8 * 172032 = 1376256 panel evaluations.
```

This remains below the previously declared root-localization allowance

```text
12 * 16 * 8192 = 1572864 panel evaluations.
```

Therefore this addendum does not increase the predeclared per-attempt, accepted-work, or global-attempted ceilings. Every `Gt_j` evaluation is charged even if a later cell fails the guard, the intersection is empty, the slab is refined, or the attempt aborts. Existing interrupted-attempt and resumable-ledger charging rules remain unchanged.

## 4. Read-only M diagnostic — reported, non-gating

Before this addendum was written, one read-only diagnostic compared `M=8` and `M=16` on the historical left-edge box

```text
Lambda = [9/20,2881/6400]
T_0    = [1/2,5/8].
```

Both candidates certified the first-step derivative guard in producer and checker. The initial worst-cell `Gt.upper()` values were approximately

```text
M=8:  producer -8.118e-2, checker -8.118e-2
M=16: producer -1.045e-1, checker -1.045e-1.
```

`M=16` is declared because it gives the larger negative guard margin while remaining below the existing work allowance. There is no panel or M ladder in the binding algorithm.

With `M=16`, the same read-only diagnostic produced:

```text
producer step 1: T_1 approximately [0.572371,0.603110], width approximately 3.074e-2
producer step 2: final width approximately 7.058e-3, target reached in 2 iterations
checker  step 1: T_1 approximately [0.572075,0.603960], width approximately 3.189e-2
checker  step 2: width approximately 8.001e-3, target not yet reached
checker  step 3: final width approximately 6.196e-3, target reached in 3 iterations.
```

All values in this section are `REPORTED / NON_GATING`. They do not authorize any change to `M=16`, the sign predicate, panel counts, target width, iteration limit, lambda-refinement depth, precision, or ceilings.

## 5. Supersession and regression-control update

This addendum supplements v2 §2 by defining the previously implicit initial root bracket as `T_0=[t_minus,t_plus]` from the exact tube clamp. It also supersedes the single-box `Gt=[partial_t g](T_k x Lambda)` denominator in v2 §2 with the 16-cell hull construction of §2 above.

The phrase “replaces midpoint-sign bisection” retains its original meaning. No midpoint-sign prefix is part of the binding algorithm.

The former v2 development smoke beginning from

```text
T_0 = [9/16,19/32]
```

is retained only as a historical diagnostic control. That bracket was produced by the certified prefix of the superseded midpoint-sign procedure and is not an authorized initializer for a new evidence run.

The binding development regression for the correction implementation instead begins from the exact tube-clamp bracket

```text
Lambda = [9/20,2881/6400]
T_0    = [1/2,5/8]
ROOT_GT_T_CELLS = 16.
```

Both producer and checker regression smokes must execute this new initialization and subdivided-`Gt` path. Failure of either lineage to certify the strict per-cell guard or to reach `1/128` within 8 iterations is a smoke failure; the contract is not weakened to accommodate it.

## 6. Invariants and v2.1 preservation

The following remain unchanged:

```text
domain and coarse slab count,
predictor construction,
W0 = 1/16,
tube monotonicity gate and wall signs,
clamp and corner rules,
T0/T1/T2 and E0/E1/E2 policies,
MAX_DEPTH = 3,
predictor acceptance threshold = 1/64,
ROOT_TARGET = 1/128,
ROOT_MV_STEPS = 8,
G0 panels = 32768,
Gl panels = 8192,
per-Gt-cell panels = 8192,
Arb precision = producer 160 bits / checker 192 bits,
all accepted/attempted/work ceilings.
```

Addendum v2.1 remains fully binding as the intended post-audit policy: its A.1 exact-equality layer, A.2 lineage-independent proof layer, A.3 overlap/dual-acceptance layer, checker fixed-tree replay rule, and §C comparison-record labels are not superseded by this addendum.

In particular, `T_0` and `ROOT_GT_T_CELLS=16` are added to the A.1 exact-equality audit set, while later `T_k` cell endpoints and their interval values remain A.2 evidence. Any A.1 or A.3 mismatch remains fail-closed.

## 7. Required sequence after this addendum

No manifest or evidence run may be created from the failed implementation commit `a0724f09666996f83a58b1bbb7407eef03f16691`.

After this PREDECLARED addendum commit, the required order is:

```text
1. chat verbatim audit of this addendum;
2. one correction commit implementing, in the same unit:
   - v2.1 §B fixed-tree checker replay,
   - v2.1 A.1/A.3 fail-closed comparison enforcement,
   - this v2.2 exact T_0 initialization and 16-cell Gt hull;
3. chat raw audit of that correction, including the previously fixed six replay/comparison checks and initialization checks;
4. a new manifest pinning every changed source/blob;
5. fresh environment preflight;
6. fresh C1c calibration;
7. a new previously nonexistent producer RUN_DIR, followed by the fixed-tree checker replay under its own ledger and work accounting.
```

The historical ABORT ledger, the failed implementation commit, and all read-only diagnostics remain immutable historical controls and are not machine evidence.
