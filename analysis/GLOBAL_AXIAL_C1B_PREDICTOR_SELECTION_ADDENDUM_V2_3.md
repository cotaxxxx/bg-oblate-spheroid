# C1b predictor selection addendum v2.3

Status: `PREDECLARED_ADDENDUM / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_BINDING`

This addendum is committed after v2.2.2 and before the correction implementation. It changes only the exact selection rule between the continuation candidate and an available bracket-scan midpoint. The three-stage predictor ladder itself remains unchanged:

```text
continuation -> bracket scan -> relocated
```

All v2/v2.1/v2.2/v2.2.1/v2.2.2 replay, comparison, root-localization, fail-closed, work-accounting, and evidence obligations remain otherwise unchanged.

## 1. Exact continuation-versus-scan selection rule

If bracket scan returns an exact rational bracket

```text
[s_lo,s_hi],
```

define, using exact rational arithmetic only,

```text
scan_mid = (s_lo+s_hi)/2.
```

Let `continuation` denote the exact rational continuation candidate already produced by the existing first predictor stage. The selection rule is:
```text
if |continuation-scan_mid| <= ROOT_TARGET:
    t_c = continuation
else:
    t_c = scan_mid
```

The equality case belongs to the continuation branch. The comparison and both absolute-value operands are `Fraction` values; no binary or decimal floating-point conversion is permitted anywhere in this selection.

If bracket scan returns no bracket for a slab, the previously declared predictor behavior is unchanged. This addendum does not alter when bracket scan is run, when the relocated stage is entered, or any later rescue rule.

The selected `t_c` remains an exact rational `A1_EXACT_EQUALITY` quantity and must match exactly in producer/checker replay.

## 2. Threshold provenance and no new constant

This addendum introduces no new numerical threshold. The selection threshold is the already declared

```text
ROOT_TARGET = 1/128.
```

The existing final predictor-acceptance threshold remains

```text
PRED_ACCEPT = 1/64.
```

These quantities have different roles and are not interchangeable: `ROOT_TARGET` selects between two exact predictor candidates when scan has returned a bracket; `PRED_ACCEPT` remains the final check against the midpoint of each lineage's own certified `T_*`.
## 3. No weakening and unchanged rescue semantics

The following remain unchanged:

```text
three-stage predictor ladder,
W0 = 1/16,
PRED_ACCEPT = 1/64,
MAX_DEPTH = 3,
all panel counts,
producer/checker Arb precisions 160/192 bits,
all accepted/attempted/work ceilings,
exact lambda bisection and recentering after an acceptance failure.
```

In particular, if the selected `t_c` later fails the existing `1/64` predictor-acceptance test against that lineage's certified `T_*`, the slab follows the same existing fail-closed rescue path: exact lambda bisection plus recentering only, subject to the unchanged maximum depth. This addendum does not turn an acceptance failure into acceptance and does not add a checker-only rescue.

The selection itself requires only exact rational arithmetic and therefore carries zero numerical integration work. It does not change any work ledger, per-attempt ceiling, accepted-work ceiling, or global attempted-work ceiling.

## 4. Historical regression control — relocated path

For the historical left-edge regression slab

```text
Lambda = [9/20,2881/6400],
continuation = 9/16,
scan bracket = [591/1024,37/64],
```
the exact scan midpoint is

```text
scan_mid = 1183/2048.
```

Because

```text
|9/16 - 1183/2048| = 31/2048 > 1/128,
```

the binding v2.3 selection is the relocated candidate

```text
t_c = 1183/2048.
```

The exact tube-clamp initializer is therefore

```text
T_0 = [1055/2048,1311/2048].
```

A read-only diagnostic using the already predeclared v2.2 root policy (`ROOT_GT_T_CELLS=16`, 8192 panels per Gt cell, G0=32768, Gl=8192) reported:

```text
producer: 2 MV iterations; final width = 734794521/137438953472 ≈ 5.346e-3;
          worst Gt.upper step 1 ≈ -1.19733e-1, step 2 ≈ -2.07149e-1;
          final 1/64 predictor acceptance = PASS.
checker:  2 MV iterations; final width = 430136647/68719476736 ≈ 6.259e-3;
          worst Gt.upper step 1 ≈ -1.19733e-1, step 2 ≈ -2.06001e-1;
          final 1/64 predictor acceptance = PASS.
```
All values in this section are `REPORTED / NON_GATING`. They authorize no change to thresholds, panels, precision, refinement depth, iteration cap, or ceilings.

The immediately preceding historical smoke with the former continuation selection `t_c=9/16` is retained as a fail-closed control: root localization reached the width target in both lineages but the final `1/64` predictor acceptance failed in both. That control demonstrates that the existing acceptance gate remained active; it is not an authorized expected result for the v2.3 regression.

## 5. Synthetic exact-selection controls

The correction implementation must include two exact, zero-integration synthetic controls that exercise both sides of the selection predicate.

Continuation-side control, including the equality boundary:

```text
continuation = 9/16,
scan bracket = [583/1024,585/1024],
scan_mid = 73/128,
|continuation-scan_mid| = 1/128,
expected selected t_c = 9/16.
```

Relocated-side control:

```text
continuation = 9/16,
scan bracket = [584/1024,586/1024],
scan_mid = 585/1024,
|continuation-scan_mid| = 9/1024 > 1/128,
expected selected t_c = 585/1024.
```

Both controls are exact `Fraction` controls. Their expected outputs are pinned by this addendum and are part of the correction raw audit; no float conversion is permitted.
## 6. Correction raw-audit carry-forward

The previously fixed eleven correction-audit items remain mandatory. A twelfth item is added:

```text
12. Predictor selection:
    - diff names the Fraction-only implementation of scan_mid and the comparison;
    - equality uses the continuation branch: <= ROOT_TARGET;
    - strict excess uses the relocated branch: > ROOT_TARGET;
    - no new threshold constant is introduced;
    - the historical regression slab actually executes the relocated path and starts root localization from T_0=[1055/2048,1311/2048];
    - both synthetic selection controls in §5 execute and match their pinned exact outputs.
```

The raw audit must also retain the existing checks for replay-schema purity, deletion of checker-autonomous tree generation, `CHECKER_REPLAY_UNRESOLVED`, producer-REFINE record-only behavior, A.1/A.3 enforcement, §C labels, exact T_0 and 16-cell Fraction subdivision, outward Gt hull construction, corner handling, actual work charging, 160/192 precision inheritance, outward rational point-ball containment, and two-phase resume pins.

## 7. Required sequence

After this PREDECLARED addendum commit, the required order is:

```text
1. chat verbatim audit of v2.3;
2. one correction commit containing the four C1b producer/checker source changes, the cross-lineage comparison stage, and this predictor-selection implementation as one audited unit;
3. chat raw audit of the eleven prior items plus item 12 above;
4. new manifest;
5. fresh preflight;
6. fresh C1c calibration;
7. fresh previously nonexistent RUN_DIR for the full producer run, followed by fixed-tree checker replay.
```

Push and tag remain approval-controlled. No push or tag is authorized by this addendum.
