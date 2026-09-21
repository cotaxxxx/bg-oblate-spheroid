# D-OB P1 DIAGNOSTIC — RESULT RECORD

**Status**: `DIAGNOSTIC_ONLY / NOT_EVIDENCE / STRATEGY_SELECTED`

**Predeclaration.** `analysis/D_OB_P1_DIAGNOSTIC_PREDECLARE.md`, commit `1105c162bc9c6407ef7c6f96cd45f15a95ee4a94`, blob `371391c570674ce6dd0be16f804b2d49fefafc85`, pushed to `origin` before the run.

## Run

Run on 2026-09-22, outside the repository.

~~~
script   /home/daybreak/d_ob_notes/d_ob_p1_diagnostic.py
         SHA-256 8a8128d5620ecaa8a4d0a3849ba50312f771f8f8b5813a04626cfc388a5f25ea
log      /home/daybreak/d_ob_notes/d_ob_p1_diagnostic.log
         SHA-256 5b11418b1320e1a7a5d92d77f964d509380afe4152d4a50378f78a23d0446d08
env      dedicated virtual environment /home/daybreak/d_ob_notes/.venv
         Python 3.11.16, NumPy 2.4.6, SciPy 1.17.1
wall     220 s, no exception
~~~

The chat audit read the script before it was run. Two defects found in that review were fixed before the recorded SHA-256: the series coefficients of `R` near `gamma = 1`, and the step and tolerance of the finite-difference self-check. `IntegrationWarning` is raised as an exception, and a sample at which any exception occurs counts as sign `0`, hence answer `NO`, in line with §4 of the predeclaration.

## Self-check

`SELF_CHECK_ONLY`; not an input to the decision.

~~~
axis_Erho_zero       PASS
E_fd_vs_Erho         PASS
Erhorho_vs_fd_Erho   PASS
~~~

## Answers

~~~
Q1  H has a uniform sign on Q_lambda          YES(+)
Q2  E_rhorho has a uniform sign on Q_lambda   NO
~~~

## Consequence

By §8.4 of the design note, the certification target is `H > 0` on `Q_lambda`, through the kernel `K_H` of §8.2. The single-`E_rhorho` design is not used. No value, location or other information from the run is used beyond these two answers. This record is not evidence of the sign of `H`.
