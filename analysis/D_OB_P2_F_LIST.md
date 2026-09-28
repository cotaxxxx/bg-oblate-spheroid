# D-OB P2 F-list (post-smoke correction targets)
Status: AUDIT LEDGER / NOT_EVIDENCE
Scope: canonical implementation c0f099f9 (producer dff79bc4..., checker 762bcf38...)

F1 - medium - signal/flock deadlock risk (producer AND checker)
  A process holding the ledger flock (producer pool worker, checker parent,
  or producer parent under --workers 1) can receive SIGTERM/SIGINT while
  appending. The inherited handler then opens another fd and tries to flock
  the same ledger again, which can block -> hang. Fix: mask signals around
  ledger append or add a re-entrancy guard; apply to both lineages;
  separate process-control commit, never mixed with mathematical changes.
  Registered behavior (not a defect): after a primary unit failure,
  mp.Pool context exit TERMs workers; their handlers can emit interruption
  records = secondary cleanup class (valid only after primary failure).
  One such cleanup record was observed in the smoke checker replay.
  If the F1 fix changes worker signal handling (for example SIG_DFL), this
  cleanup-record behavior may change; preregister the new expectation
  before the next formal rerun.

F2 - low - heartbeat counter resets on resume
  _COUNTER starts at 0 per process; after --resume, completed counts show
  new work only. Fix option: seed from ledger at startup. Telemetry only.

F3 - low - LOCK-adjacent minor issues
  Conditional-pass audit recorded three concrete issues:
  (1) a LOCK created by another host is treated as stale unconditionally;
  (2) ledger header writing occurs before LOCK acquisition;
  (3) os.kill-based liveness probing does not catch PermissionError.
  Stale-lock recovery itself is control-tested. Fix scope is these recorded
  issues and must not be expanded from memory.

F4 - medium - controls do not cover full production/resume paths
  Existing C-R1 through C-R3 are insufficient as end-to-end controls:
  C-R1 uses a fake refine_cells and exercises only a one-node tree.
  C-R3 runs with --workers 1 and therefore does not exercise the Pool path.
  The fail-closed paths PARTIAL_LINE, NON_PREFIX, DUPLICATE,
  EXISTS_USE_RESUME, and OUTSIDE_RUN_DIR have not been deliberately fired.
  Add production-path controls for each. Also add a resume control that
  stops after partial progress, resumes from the ledger, and verifies that
  the final certificate bytes are identical to an uninterrupted run.

F5 - CLOSED — SPEC V2 compliant
  SPEC V2 lines 72, 76, and 93 (SHA-256 19af6f7f...) explicitly prescribe
  different gamma_star and precision settings for producer and checker.
  The execution-side audit originally registered this as F5; the
  interpretation "gamma_star 5/8 = stale metadata" is withdrawn.
  Residual documentation may state that checker report gamma_star denotes
  the checker's own chart-switch constant, CUT=Q(5,8).

F6 - low - os.popen zombie
  runtime_identity()/checker_identity() call os.popen("git rev-parse
  HEAD") without close -> zombie child until process exit. Fix:
  subprocess.run or explicit close. Both lineages.

Fix policy: F1/F2/F3/F4/F6 ride the next correction cycle (SPEC V3
implementation), each with end-to-end write-through controls per the
standing "everything added gets a production-path test" principle.
F5 is CLOSED and requires no mathematical or implementation correction.
