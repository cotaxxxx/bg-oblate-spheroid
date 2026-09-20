# Global axial C1b machine receipt

Status: `MACHINE_PASS / C1B_MACHINE_CLOSED / JUDGE_NOT_YET_ISSUED`

This receipt records the two-phase C1b replay: a producer run that searched and
certified the accepted slab tree, an independent checker run that replayed that
tree, and the fail-closed cross-lineage comparison between them. It also records
the evidence required by the C1c assembly gate.

Every numeric value below is transcribed from a single machine-extracted
canonical table produced from the sealed artifacts:

```
/home/daybreak/basepoint-geometry-artifacts/C1b/c1b_receipt_extract.json
sha256 = 8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b
```

No value in this receipt was entered by hand from conversation notes.

---

## 1. Evidence identity

repository = cotaxxxx/bg-oblate-spheroid (working clone `bg-oblate-spheroid-c1b`)
branch = implementation/gt-boundary-two-chart
head = 85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b
worktree = clean

### 1.1 Sealed run artifacts

| role | path | ledger sha256 |
|---|---|---|
| Phase 1 (producer) | `phase1_v212s_seal_20260918T222551Z` | `1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f` |
| Phase 2 (checker) | `phase2_v212s_seal_20260920T140743Z` | `09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38` |

replay plan (`checker_replay_exact.jsonl`, Phase 1 seal)
= `c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69`

Both seal directories are non-writable (mode 555); their `ledger.jsonl` files are
mode 444, with per-file SHA-256 pins recorded for the sealed contents. The
replay-plan hash equals the value self-declared by the Phase 1 `segment_end`
record (`checker_replay_sha256`), so the checker input is bit-bound to the
producer ledger.

### 1.2 Source blobs

| path | blob |
|---|---|
| `analysis/c1b_resumable_driver.py` | `5fd308bb4c02c6ddbd612ddbedb18f6b9e22bc3d` |
| `producer/global_axial_c1b_producer.py` | `0616fbd7c9c85f77c8e80b61a5b3b536b45012a8` |
| `producer/global_axial_c1b_gating.py` | `a93ca173ae0bededcd5a0248aa07ac3348f9a243` |
| `producer/global_axial_c1b_kernel.py` | `67dda838369302010ef3d589937b834b96ede4d8` |
| `checker/global_axial_c1b_checker.py` | `0760764ef7592be1ddd4ffec3966e9c6ec930a5b` |
| `checker/global_axial_c1b_gating.py` | `03df262012bfbebcf4d2ea173933186c70abafbf` |
| `checker/global_axial_c1b_kernel.py` | `4eaca55ddf79b437fc756d666294372e5d1a6ba4` |

Both sealed ledgers carry a `post_identity` block whose blob map equals the
pinned `expected_blobs`, with `clean_status = ""`.

### 1.3 Pinned contracts and subgate receipts

| path | blob |
|---|---|
| `analysis/GLOBAL_AXIAL_C1B_PRE_RUN_AMENDMENT.md` | `8e04e2efaf816bab9d9d1f3fd0a9d753538b31ad` |
| `analysis/GLOBAL_AXIAL_C1B_BOB_BRIDGE_CONTRACT.md` | `215193e2fc2a1abcf2aee2527c4c2e6f3176ea6c` |
| `analysis/GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md` | `0f19e3877b9675506ac8f35a5702147a84723c43` |
| `producer/global_axial_c1b_bob_producer.py` | `1a54875e1b93281c32f030081cdccd415827dcea` |
| `checker/global_axial_c1b_bob_checker.py` | `1cded03e6c769adf26ead8b79f31e90dfbf7ce9d` |

The C1b kernel hard-codes `BOB_AMENDMENT_BLOB` and `BOB_RECEIPT_BLOB` and
verifies the receipt blob at run time, so the B_ob subgate is a pinned
dependency of this run rather than an external reference.

---

## 2. Exact cover ledger

direction = increasing lambda
C1b domain = `[9/20, 5/8]`
Delta_lambda = `1/800`; `(5/8 - 9/20) / (1/800) = 140`

### 2.1 Coarse partition

coarse indices present in the sealed ledgers = `0 … 139`
distinct = 140; complete `0..139` = **true** (both lineages)

### 2.2 Accepted (refined) cover

attempted slabs = 178
accepted slabs = 159
first accepted `lambda_lo` = `9/20`
last accepted `lambda_hi` = `5/8`
adjacent exactness (`a.lambda_hi == b.lambda_lo` for consecutive accepted
slabs) = **true**

`exact_union = true` in both `segment_end` records. The machine check behind
that flag is precisely: first accepted slab starts at `L_LO`, last ends at
`L_HI`, and consecutive accepted endpoints are exactly equal.

The two cover layers are reported separately on purpose: the 140-coarse count
is normative (it follows from the domain and `Delta_lambda`), whereas
`exact_union` is the machine check on the realised accepted cover.

### 2.3 Final interface

final exact interface lambda = `5/8`

---

## 3. Clamp events and lambda_B

left-clamp events among accepted slabs = **0**
right-clamp events among accepted slabs = **35**
right-clamped coarse indices = `105 … 139` (contiguous)

lambda_B = smallest exact left endpoint among accepted slabs whose right wall
is clamped = **`931/1600`** (the `lambda_lo` of coarse 105).

lambda_B is therefore not `NONE`, and the B_ob extension gate is non-vacuous.

---

## 4. B_ob extension gate

The B_ob subgate certifies `B_ob(lambda) < 0`, i.e. `g(1, lambda) < 0`, which
supplies the right-wall condition for every right-clamped slab (`t_plus = 1`).

certified domain (B_ob machine receipt) = `[9/20, 5/8]`
required extension for this run = `[931/1600, 5/8]` ⊂ certified domain

### 4.1 Stage ledger

| stage | lambda boxes | s panels | outcome |
|---|---|---|---|
| B0 | 16 | 1024 | unresolved remained |
| B1 | 32 | 2048 | **first pass** |
| B2 | 64 | 4096 | not executed |

worst exact lambda box at B1 = `[793/1280, 5/8]`

### 4.2 Strict-negative worst upper bound

The original B_ob run recorded the worst enclosure only in its default display
form, `[+/- 0.0421]`, from which the upper endpoint cannot be recovered. The
acceptance test itself used `value.upper() < 0` on the Arb object, but that
upper endpoint was not serialised.

The values below are therefore a **reproduction measurement**: the pinned B_ob
implementation was re-executed, without modification, solely to serialise the
upper endpoint. They are *not* values recorded by the original run.

| lineage | precision | worst upper (`.str(50)`) |
|---|---|---|
| producer | 160 bit | `[-0.0047719233937436607837435475002795559827518210547840 +/- 2.94e-53]` |
| checker | 192 bit | `[-0.0047719233937548464067652235739161574663010135954551 +/- 1.39e-53]` |

The reproduction was accepted only after five fixed conditions held in both
lineages: first pass at B1; unresolved = 0; worst box `[793/1280, 5/8]`; default
display of the worst ball equal to `[+/- 0.0421]` as recorded in the original
receipt; and upper strictly negative.

The two reproduced values are retained separately by lineage; they are not
merged into a single bound. Both reproduced upper bounds are strictly negative.

---

## 5. Corner and tube evidence

### 5.1 corner_hull counts

corner_hull total over accepted slabs = **2212**
accepted slabs with nonzero corner_hull = **35**

The 35 slabs with nonzero corner_hull coincide exactly with the 35
right-clamped slabs. This is structural: the corner branch is taken only when
`tr == T_HI`. Both sealed ledgers report the same totals.

### 5.2 Certified tube region versus the bookkeeping cut at 31/32

For every accepted slab `Lambda`, the certified statements are

```
sup   over (t,lambda) in [t_minus, t_plus] x Lambda   of  d/dt g(t,lambda)  <  0
inf   over lambda in Lambda                           of  g(t_minus,lambda) >  0
sup   over lambda in Lambda                           of  g(t_plus,lambda)  <  0   (unclamped)
                                                          g(1,lambda) = B_ob(lambda) < 0   (clamped)
```

The monotonicity region is `[t_minus, t_plus] x Lambda`. It is **not** truncated
at 31/32. Together with the two wall conditions this yields, for each fixed
lambda in the slab, a unique zero of `g` inside the tube.

Separately, `T_MID_HI = 31/32` appears in the `middle_partition` bookkeeping. On
a right-clamped slab the ledger records

```
["L",    "1/2",   t_minus]
["TUBE", t_minus, "31/32"]
```

even though the certified tube endpoint is `t_plus = 1`. The value 31/32 is the
interface with the already certified boundary band on
`[31/32, 1] x [5/8, 33/50]`; it is a bookkeeping cut, not the tube endpoint.

No claim `g(31/32, lambda) > 0` is extended below `lambda = 5/8`.

---

## 6. C1c anchor supply

The C1c assembly gate requires, for every accepted C1b slab, a positive anchor
at `t = 1/2`, i.e. `Phi(1/4, lambda) = 2 g(1/2, lambda) > 0`, supplied either by
a left tube wall at `t_minus = 1/2` (path A) or by a certified left exterior
cover connecting `1/2` to the tube wall (path B).

| supply path | count |
|---|---|
| A — `t_minus = 1/2` directly | **0** |
| B — certified left exterior cover on `[1/2, t_minus]` | **159** |
| missing | **0** |

All 159 accepted slabs are supplied by path B. Path A does not occur in the
sealed accepted-slab ledger.

Final exterior stage at which the left cover closed:

| stage | slabs |
|---|---|
| E0 | 120 |
| E1 | 37 |
| E2 | 2 |
| total | 159 |

For all 159 slabs the final exterior stage reports `unresolved = 0`, and the
`exterior_nonfinite` list is empty.

---

## 7. Work ledger

The pre-run amendment requires that B_ob extension-gate work be reported
separately and states that it "may not be absorbed silently into the slab
budget". The two budgets are therefore kept apart.

### 7.1 Slab work

accepted-leaf work = **356,643,328** panel evaluations
cumulative attempted work = **408,173,824** panel evaluations

per-attempted-slab ceiling = 23,560,192
absolute machine-work safety ceiling = `2100 x 23,560,192 = 49,476,403,200`
accepted-leaf safety ceiling = `1120 x 23,560,192 = 26,387,415,040`

### 7.2 B_ob extension-gate work

executed = B0 `16 x 1024 = 16,384` + B1 `32 x 2048 = 65,536`
actual = **81,920** s-panel evaluations per lineage
B2 not executed
predeclared ceiling = **344,064** per lineage
(`16*1024 + 32*2048 + 64*4096`)

---

## 8. Caps

| cap | value |
|---|---|
| MAX_COARSE_SLABS | 140 |
| MAX_ACCEPTED_SLABS | 1120 |
| MAX_ATTEMPTED_SLABS | 2100 |
| actual attempted | 178 |
| actual accepted | 159 |

---

## 9. Cross-lineage comparison

Both sealed ledgers were compared with the pinned implementation
`analysis/c1b_cross_lineage_compare.py`.

schema = `C1B_CROSS_LINEAGE_COMPARISON_V2_4_2`
result = **PASS**
attempts = 178; accepted = 159

labels asserted:
`A1_EXACT_EQUALITY`, `A2_LINEAGE_INDEPENDENT`, `A3_CROSS_LINEAGE_CONSISTENCY`

artifact = `c1b_cross_lineage_comparison_20260920T155138Z.json`
sha256 = `bb78c0cf36da89877a18fae2ff8067541d12d2e0d3b554ed9b14319988c4bde1`

The three input hashes recorded inside the artifact equal the sealed values in
§1.1.

### 9.1 Scope of A.1

A.1 has 15 replay-plan data fields; the replay record carries those 15 plus
`schema`, i.e. 16 keys. Generic producer/checker equality is applied to 14 of
them:

```
attempt_sequence, tree_node, coarse_index, refinement_depth,
lambda_lo, lambda_hi, decision, t_c,
left_clamp, right_clamp, t_minus, t_plus, T_0, root_gt_t_cells
```

`producer_accept_root_outcome` is deliberately excluded from generic equality
and is checked instead by the explicit ACCEPT branch, with the checker
independently required to report `RESOLVED_WITH_CERTIFIED_T_STAR`. This is a
separation of concerns, not an omission.

### 9.2 Scope of A.2

A.2 retains the lineage-specific tube stage, corner boxes, tube guards,
exterior guards, root-MV steps, root reason/outcome, work, and the Arb
enclosures contained in those recorded structures; these are not
equality-compared as A.1 data.

Separately, the comparison implementation enforces an explicit forbidden-key set
on the replay plan — `T_star`, `G0`, `Gt`, `Gl`, `Gpar`, `N_k`, `root_mv_steps` —
so an A.2 leak into the exact-equality layer terminates the comparison with
`COMPARE_REPLAY_A2_LEAK`.

### 9.3 Independent agreement on receipt quantities

Beyond the comparison implementation, every slab-side quantity reported in this
receipt was extracted independently from each sealed ledger and found equal
across lineages: attempted, accepted, coarse cover, accepted cover, clamp
counts, right-clamped coarse set, lambda_B, corner_hull totals, accepted work
and cumulative work.

---

## 10. Conclusions

```
C1B_MACHINE_STATUS      PASS
C1B_MACHINE_CLOSED      YES
C1B_JUDGE_STATUS        NOT_YET_ISSUED
```

What this receipt establishes:

- The accepted slabs form an exact cover of `[9/20, 5/8]` with exact endpoint
  agreement, over the normative 140-coarse partition, terminating exactly at
  `5/8`.
- An independent checker lineage replayed the producer tree. The fourteen A.1
  equality keys agreed across all 178 attempts; for the 159 accepts, the
  additional condition on `producer_accept_root_outcome` and the checker's own
  certified outcome also held.
- The B_ob subgate supplies the right-wall condition on `[931/1600, 5/8]`, with
  a strictly negative worst upper bound in both lineages.
- For every accepted slab, a positive `t = 1/2` anchor is supplied by a
  certified left exterior cover.

What this receipt does **not** establish:

- It is not a Judge decision. The Judge layer has not been issued.
- It does not claim that the corner-branch return-value interface difference
  between the two lineages is harmless in general; it records only that on the
  35 slabs where the corner branch was actually taken, both lineages reported
  identical corner_hull totals.
- The B_ob worst upper bounds are reproduction measurements from the pinned
  implementation, not values recorded by the original B_ob run.

---

## 11. Comparison status

The one-chat comparison of §§1–10 against the canonical table
(`8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b`) and the
pinned contracts recorded:

```
numeric / identity mismatches   0
unsupported claims              0
wording precision corrections   1   (§9.2, A.2 description — applied)
```

The §9.2 correction has been applied in this revision, together with a matching
refinement of the second claim in §10. No item remains open from the comparison.

Resolved during drafting: the three previously truncated blob values in §1.3 are
filled from the canonical table, and the target path follows the existing naming
series (`GLOBAL_AXIAL_C1A_MACHINE_RECEIPT.md`,
`GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md`,
`GLOBAL_AXIAL_C1C_MACHINE_RECEIPT.md`), i.e.
`analysis/GLOBAL_AXIAL_C1B_MACHINE_RECEIPT.md`.
