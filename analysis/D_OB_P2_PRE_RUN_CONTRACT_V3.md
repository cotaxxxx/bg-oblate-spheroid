# D-OB P2 PRE-RUN CONTRACT V3

**Status**: `DRAFT / NOT_FROZEN / NOT_RUN / NOT_BINDING`

**Base.** Branch `design/d-ob-p2`. Specification `analysis/D_OB_P2_CERTIFICATION_SPEC_V3.md`, SHA-256 `0e07fb4ec8c45ea366ba4abf4cddacdc1a10ce4bd1ed2eca5e32a69b3a90e26f`, cited below as SPEC. This contract fixes how SPEC V3 is executed on `P'`; it changes no numerical kernel, chart, cut, budget, or subdivision rule in SPEC.

**Supersedes.** CONTRACT V2 (`analysis/D_OB_P2_PRE_RUN_CONTRACT_V2.md`, SHA-256 `8461069aad635efe517008c52ce571a09b8d552f43726a9fccac508a2c093e27`). By Judge ruling 2026-10-13, V3 executes the retained 254 initial boxes of SPEC V3, continues through all retained initial boxes even after an `UNRESOLVED` result, and replaces smoke rerun by the accepted resume controls plus a 254-box enumeration dry run. All other execution obligations are inherited from V2.

## 1. Files and independence

- Producer: `producer/d_ob_p2_producer.py`. Checker: `checker/d_ob_p2_checker.py`.
- Each imports only the Python standard library and `flint` (python-flint). The checker imports no producer module and no module shared with the producer.
- Independence scope: both are written by the same implementation actor; the checker is a separate implementation that uses its own precision (192 bits), its own chart threshold (`gamma_* = 5/8`), its own cell classification and its own recomputation of every quantity. It is not an independent mathematical derivation. Both sources are read in full by the chat audit before any run counted as evidence.

## 2. Environment and identity

- Interpreter `/home/daybreak/.pyenv/versions/3.11.16/bin/python`, python-flint 0.9.0.
- Recorded before the producer and after the terminal machine stage: HEAD, empty `git status --porcelain`, interpreter path and version, python-flint version, CPU, and the SHA-256 of SPEC, of this contract, of the producer and of the checker as present in the working tree. On a PASS candidate the terminal stage is the checker; on a completed 254-box producer FAIL due to unresolved leaves it is the producer terminal stage.
- The SPEC SHA-256 must equal the value above. The required identity fields and the consequence of a mismatch are fixed in §6.

## 3. Output paths

Outside the repository, one directory per run, `~/basepoint-geometry-artifacts/D_OB_P2/run_<UTC timestamp>/`, containing `identity_before.txt`, `identity_after.txt`, `producer.log`, `certificate.jsonl.gz`, `producer_summary.json`, and, on a checker-executed path, `checker.log` and `checker_report.json`. The producer summary records the SHA-256 of `certificate.jsonl.gz`; when the checker is executed, the checker report records the same identity field independently. The repository receives only the receipt `analysis/D_OB_P2_MACHINE_RECEIPT.md`.

## 4. Certificate

**Canonical order.** Initial boxes are indexed by `(i_r, i_tau, i_lambda)` in `{0..7} x {0..7} x {0..3}` and ordered lexicographically, with exactly `(7,7,0)` and `(0,0,3)` omitted. Thus the active list contains 254 initial boxes and is the canonical 256-box order with those two entries skipped. Within an initial box, boxes are ordered depth-first, preorder, the lower half of a bisection before the upper half. Cells are ordered by SPEC §3 (lexicographic in `(mu_lo, phi_lo)`); the four children of a bisected cell are, in order, (low `mu`, low `phi`), (low `mu`, high `phi`), (high `mu`, low `phi`), (high `mu`, high `phi`).

**Encoding.** `certificate.jsonl.gz` holds one JSON line per active initial box, in canonical order, written with `gzip` at `mtime = 0`:

- `initial`: `[i_r, i_tau, i_lambda]`;
- `box_tree`: a preorder string over `{0, 1}` of the box bisection tree, `1` for a bisected box and `0` for a leaf; the bisection coordinate is not encoded, since SPEC §6 determines it from the box;
- `leaves`: in canonical order, one object per leaf box with its endpoints as rational strings `"p/q"`, box depth, column, `c`, `cbar` (far column), `R`, and `cell_tree`, the concatenation over the 2048 initial cells in cell order of the preorder `{0, 1}` string of each cell's bisection tree;
- informational only: producer values of `L` and `B_cut` as decimal strings.

A leaf's partition is fully determined by `cell_tree`; the producer's cell labels are not written. `box_tree` is a complete preorder encoding of a full binary tree, and each initial cell's segment of `cell_tree` is a complete preorder encoding of a full 4-ary tree; both are self-delimiting.

**Checker obligations** (in addition to SPEC §7): parse `box_tree`, and the 2048 consecutive segments of each `cell_tree`, as self-delimiting codes, and require each string to be consumed exactly; regenerate every leaf box from `initial` and `box_tree` by the SPEC §6 bisection rule and require equality with the listed endpoints, so that the leaves cover `P'`; regenerate every cell partition from `cell_tree` and require it to cover `[-1, 1] x [0, pi]`.

## 5. Parallelism and determinism

The unit of work is an initial box. The producer and the checker may each use 12 worker processes; units are dispatched in canonical order and results are collected in canonical order (`imap`-style ordered collection). Each unit's computation depends only on its initial box, so the logical content of the certificate and of the report does not depend on scheduling. Byte-level reproducibility of the gzip file is not claimed.

## 6. Execution and gates

1. Pre-run: verify the SPEC SHA-256; verify that the producer and checker are committed and the tree is clean; record `identity_before.txt`.
2. Producer: enumerates all 254 active initial boxes in canonical order. An `UNRESOLVED` result in one active initial box SHALL NOT terminate dispatch of later active initial boxes. After all 254 have completed, the producer writes the certificate and summary. It exits 0 if and only if all 254 resolve with no `UNRESOLVED`; if one or more remain unresolved after the complete 254-box traversal, it exits 1 and the run verdict is `FAIL`.
3. Checker: if the producer exits 0, reads the certificate and writes the report; exit status 0 if and only if every obligation of SPEC §7 and of §4 above holds. If the producer exits 1 solely because the completed 254-box traversal contains unresolved leaves, the run is already `FAIL`; checker execution is not required to convert or qualify that verdict.
4. Record `identity_after.txt`.

The required identity fields are: HEAD, empty `git status --porcelain`, interpreter path and version, python-flint version, and the SHA-256 of SPEC, of this contract, of the producer and of the checker. CPU is recorded but not required.

The run is `PASS` if and only if (i) the producer exits 0 after completing all 254 active initial boxes, (ii) the checker exits 0, (iii) every required identity field agrees between `identity_before.txt` and `identity_after.txt`, and (iv) the certificate SHA-256 recorded in the checker report equals the one recorded in the producer summary and that of the file in the run directory. If the producer completes all 254 active initial boxes but reports one or more unresolved leaves, producer exit 1 gives verdict `FAIL`, and the receipt SHALL retain the unresolved map rather than stopping at the first unresolved box. A failure of (iii) makes the run `NOT_EVIDENCE`; any other failure makes it `FAIL`.

## 7. Pre-run acceptance controls

Smoke is not rerun. Before the main run, rerun the accepted resumable-execution controls C-R1, C-R2 and C-R3 from `analysis/D_OB_P2_RESUME_CORRECTION_PREDECLARE.md` / `tests/d_ob_p2_resume_controls.py` against the implementation candidate. In addition, perform an enumeration-only dry run that evaluates no mathematical kernel and require: (a) exactly 254 active initial-box ids, (b) exact canonical order inherited from the 256-box list, and (c) excluded-id set exactly `{(7,7,0),(0,0,3)}`. Any failure is fail-closed and blocks the main run. The historical smoke #4 remains diagnostic history and is not evidence.

## 8. Receipt and backup

After the terminal machine stage, `analysis/D_OB_P2_MACHINE_RECEIPT.md` records the two identities, the SHA-256 of the certificate, summary, report and logs that exist for the terminal path, the counts of leaves and cells, and `PASS`, `FAIL` or `NOT_EVIDENCE`. If any active initial box is unresolved, the receipt additionally records the complete unresolved map after all 254 active boxes have been traversed: initial-box id, unresolved-leaf count, and the exact coordinate range(s) of those unresolved leaves. The result then awaits the human Judge.

Before the main run, one backup unit is written outside the machine and verified by SHA-256 at the destination, containing the P1 diagnostic script and log, SPEC, this contract, the committed producer and checker sources and the audit records. After the run, the terminal-path certificate, summary, report (when produced) and logs are added and verified in the same way.
