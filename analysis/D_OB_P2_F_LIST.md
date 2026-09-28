# D-OB P2 F-list (post-smoke correction targets)
Status: AUDIT LEDGER / NOT_EVIDENCE
Scope: canonical implementation c0f099f9 (producer dff79bc4..., checker 762bcf38...)

F1 - medium - signal/flock deadlock risk (producer AND checker)
  Inherited SIGTERM/SIGINT handlers in pool workers append an interruption
  record via a fresh flock on the ledger. A worker signalled while itself
  holding the ledger flock during an append can block on the handler's
  second flock -> hang. Fix: mask signals around ledger append or add a
  re-entrancy guard; apply to both lineages; separate process-control
  commit, never mixed with mathematical bound changes.
  Registered behavior (not a defect): after a primary unit failure,
  mp.Pool context exit TERMs workers; their handlers emit interruption
  records = secondary cleanup class (valid only after the primary failure).

F2 - low - heartbeat counter resets on resume
  _COUNTER starts at 0 per process; after --resume, completed counts show
  new work only. Fix option: seed from ledger at startup. Telemetry only.

F3 - low - LOCK-adjacent minor issues
  As recorded in the conditional-pass audit (low importance; stale-lock
  recovery works and is control-tested). Enumerate precisely from source
  at fix time; scope must not be expanded from memory.

F5 - WITHDRAWN
  "gamma_star 5/8 = stale metadata" registration withdrawn: CUT=Q(5,8)
  is used computationally (checker chart switch). Legitimate independent-
  implementation divergence from producer GAMMA_STAR=7/10. Residual
  action: one documentation line that the checker report's gamma_star
  denotes the checker's own switch constant.

F6 - low - os.popen zombie
  runtime_identity()/checker_identity() call os.popen("git rev-parse
  HEAD") without close -> zombie child until process exit. Fix:
  subprocess.run or explicit close. Both lineages.

Fix policy: F1/F2/F3/F6 ride the next correction cycle (SPEC V3
implementation), each with end-to-end write-through controls per the
standing "everything added gets a production-path test" principle.

