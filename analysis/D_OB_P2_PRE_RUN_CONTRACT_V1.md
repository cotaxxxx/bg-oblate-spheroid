# D-OB P2 PRE-RUN CONTRACT V1

**Status**: `SEALED / NOT_RUN / NOT_BINDING`

**Base.** Branch `design/d-ob-p2`. Specification `analysis/D_OB_P2_CERTIFICATION_SPEC_V1.md`, commit `4513b420e395d4dcde26914c8a54f4867fddd5d4`, blob `e2204b19447ceb233ec94fe68091dcf45ee68499`, SHA-256 `93dd6d12b8ab29191bd4b878ab99b84de3ff015179941689fc851f81cca9c8c3`, cited below as SPEC. This contract fixes how SPEC is executed; it changes nothing in SPEC.

## 1. Files and independence

- Producer: `producer/d_ob_p2_producer.py`. Checker: `checker/d_ob_p2_checker.py`.
- Each imports only the Python standard library and `flint` (python-flint). The checker imports no producer module and no module shared with the producer.
- Independence scope: both are written by the same implementation actor; the checker is a separate implementation that uses its own precision (192 bits), its own chart threshold (`gamma_* = 5/8`), its own cell classification and its own recomputation of every quantity. It is not an independent mathematical derivation. Both sources are read in full by the chat audit before any run counted as evidence.

## 2. Environment and identity

- Interpreter `/home/daybreak/.pyenv/versions/3.11.16/bin/python`, python-flint 0.9.0.
- Recorded before the producer and after the checker: HEAD, empty `git status --porcelain`, interpreter path and version, python-flint version, CPU, and the SHA-256 of SPEC, of this contract, of the producer and of the checker as present in the working tree.
- The SPEC SHA-256 must equal the value above. The required identity fields and the consequence of a mismatch are fixed in §6.

## 3. Output paths

Outside the repository, one directory per run, `~/basepoint-geometry-artifacts/D_OB_P2/run_<UTC timestamp>/`, containing `identity_before.txt`, `identity_after.txt`, `producer.log`, `certificate.jsonl.gz`, `producer_summary.json`, `checker.log`, `checker_report.json`. The producer summary and the checker report each record the SHA-256 of `certificate.jsonl.gz`. The repository receives only the receipt `analysis/D_OB_P2_MACHINE_RECEIPT.md`.

## 4. Certificate

**Canonical order.** Initial boxes are indexed by `(i_r, i_tau, i_lambda)` in `{0..7} x {0..7} x {0..3}` and ordered lexicographically. Within an initial box, boxes are ordered depth-first, preorder, the lower half of a bisection before the upper half. Cells are ordered by SPEC §3 (lexicographic in `(mu_lo, phi_lo)`); the four children of a bisected cell are, in order, (low `mu`, low `phi`), (low `mu`, high `phi`), (high `mu`, low `phi`), (high `mu`, high `phi`).

**Encoding.** `certificate.jsonl.gz` holds one JSON line per initial box, in canonical order, written with `gzip` at `mtime = 0`:

- `initial`: `[i_r, i_tau, i_lambda]`;
- `box_tree`: a preorder string over `{0, 1}` of the box bisection tree, `1` for a bisected box and `0` for a leaf; the bisection coordinate is not encoded, since SPEC §6 determines it from the box;
- `leaves`: in canonical order, one object per leaf box with its endpoints as rational strings `"p/q"`, box depth, column, `c`, `cbar` (far column), `R`, and `cell_tree`, the concatenation over the 2048 initial cells in cell order of the preorder `{0, 1}` string of each cell's bisection tree;
- informational only: producer values of `L` and `B_cut` as decimal strings.

A leaf's partition is fully determined by `cell_tree`; the producer's cell labels are not written. `box_tree` is a complete preorder encoding of a full binary tree, and each initial cell's segment of `cell_tree` is a complete preorder encoding of a full 4-ary tree; both are self-delimiting.

**Checker obligations** (in addition to SPEC §7): parse `box_tree`, and the 2048 consecutive segments of each `cell_tree`, as self-delimiting codes, and require each string to be consumed exactly; regenerate every leaf box from `initial` and `box_tree` by the SPEC §6 bisection rule and require equality with the listed endpoints, so that the leaves cover `P`; regenerate every cell partition from `cell_tree` and require it to cover `[-1, 1] x [0, pi]`.

## 5. Parallelism and determinism

The unit of work is an initial box. The producer and the checker may each use 12 worker processes; units are dispatched in canonical order and results are collected in canonical order (`imap`-style ordered collection). Each unit's computation depends only on its initial box, so the logical content of the certificate and of the report does not depend on scheduling. Byte-level reproducibility of the gzip file is not claimed.

## 6. Execution and gates

1. Pre-run: verify the SPEC SHA-256; verify that the producer and checker are committed and the tree is clean; record `identity_before.txt`.
2. Producer: writes the certificate and summary; exit status 0 if and only if every initial box resolves with no `UNRESOLVED` box.
3. Checker: reads the certificate, writes the report; exit status 0 if and only if every obligation of SPEC §7 and of §4 above holds.
4. Record `identity_after.txt`.

The required identity fields are: HEAD, empty `git status --porcelain`, interpreter path and version, python-flint version, and the SHA-256 of SPEC, of this contract, of the producer and of the checker. CPU is recorded but not required.

The run is `PASS` if and only if (i) the producer exits 0, (ii) the checker exits 0, (iii) every required identity field agrees between `identity_before.txt` and `identity_after.txt`, and (iv) the certificate SHA-256 recorded in the checker report equals the one recorded in the producer summary and that of the file in the run directory. A failure of (iii) makes the run `NOT_EVIDENCE`; any other failure makes it `FAIL`.

## 7. Implementation-only smoke test

Before the main run, the producer and checker are run on four initial boxes fixed here: `(7, 0, 0)`, a boundary box near the equator; `(7, 7, 0)`, a boundary box near the axis; `(0, 0, 3)`, a box containing the centre; and `(3, 3, 1)`, an interior far-column box (`rho_lo = 9/40 > 1/8`). The smoke test checks only that both programs run to completion and that the checker reproduces the producer's leaves and cell partitions. Changes permitted after it are corrections of implementation errors or of disagreement with SPEC; each such change is a new commit and is read by the chat audit before the main run. The smoke test is not evidence. If its acceptance outcomes motivate any change to SPEC, that change is a new specification version whose text states this motivation, and SPEC V1 is closed as failed.

## 8. Receipt and backup

After the checker, `analysis/D_OB_P2_MACHINE_RECEIPT.md` records the two identities, the SHA-256 of the certificate, summary, report and logs, the counts of leaves and cells, and `PASS`, `FAIL` or `NOT_EVIDENCE`. The result then awaits the human Judge.

Before the main run, one backup unit is written outside the machine and verified by SHA-256 at the destination, containing the P1 diagnostic script and log, SPEC, this contract, the committed producer and checker sources and the audit records. After the run, the certificate, summary, report and logs are added and verified in the same way.
