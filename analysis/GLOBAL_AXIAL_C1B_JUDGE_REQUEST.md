# Global axial C1b — external Judge request

Status: `EXTERNAL_JUDGE_REQUESTED / NOT_BINDING`

## Target claim

Judge only the following, and only as statements about the certified interval
enclosures recorded in the pinned C1b machine receipt.

For every accepted C1b slab `Lambda` in the exact accepted cover of
`[9/20, 5/8]`:

```text
(A)  the certified tube-guard enclosure recorded by the pinned machine
     lineages for the quantity denoted Gt over
     [t_minus(Lambda), t_plus(Lambda)] x Lambda
     has strictly negative upper endpoint;

(B)  the certified enclosure of the machine wall quantity recorded for
     g_axis_ob(t_minus(Lambda), lambda), lambda in Lambda,
     has strictly positive lower endpoint;

(C)  the certified enclosure of the machine wall quantity recorded for
     g_axis_ob(t_plus(Lambda), lambda), lambda in Lambda,
     has strictly negative upper endpoint,

     where for the right-clamped slabs (t_plus = 1) this right-wall condition
     is supplied by the separately pinned B_ob gate over the required
     extension [931/1600, 5/8].
```

No identification of the machine quantity `Gt` with the function-theoretic
derivative `partial_t g_axis_ob` on the C1b domain is requested here. (A) is a
statement about the enclosure the machine lineages actually recorded, not about
a derivative in the analytic sense.

together with the exactness of the cover itself:

```text
(D)  the realised accepted cover: the 159 accepted slabs form an exact cover
     of [9/20, 5/8]: first lambda_lo = 9/20, last lambda_hi = 5/8, and
     consecutive accepted endpoints are exactly equal;

(E)  the normative underlying coarse partition consists of exactly 140 slabs
     (Delta_lambda = 1/800 on a domain of width 7/40), with final exact
     interface lambda = 5/8.
```

`t_minus(Lambda)` and `t_plus(Lambda)` are not functions of `lambda` alone.
They are per-slab machine data recorded in the sealed ledgers, and the claim is
stated slab-wise for that reason.

## Explicitly out of scope

A `PASS` on the above must not be read as approving any of the following. None
of them is requested, and none follows automatically from (A)–(E).

```text
- No root-existence claim. No intermediate-value argument is in scope.
- No root-uniqueness claim. "Exactly one zero in the tube" is NOT requested.
- No strict-monotonicity claim in the function-theoretic sense. Only the sign
  of the certified derivative enclosure is in scope.
- No claim identifying the machine quantity denoted Gt with the
  function-theoretic derivative partial_t g_axis_ob anywhere on the C1b
  domain is requested.
- No claim about the regularity (continuity, differentiability) of
  g_axis_ob on [9/20, 5/8]. See "Open regularity obligation" below.
- No C1c assembly consequence. No global stationary-point census consequence.
- No claim that g(31/32, lambda) > 0 extends below lambda = 5/8.
```

## Open regularity obligation — declared, not requested

Passing from (A)–(C) to a root-existence and uniqueness statement requires
continuity and differentiability of `g_axis_ob` on the C1b domain. That premise
is **not** established by the currently pinned material:

- `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md`
  (blob `7cb9b8091596510203d74e09387bc1e8188b8b47`,
  status `EXTERNAL_AUDIT_PENDING / NOT_BINDING`) fixes
  `lambda in [5/8, 33/50]` and `t in [63/64, 1]`. It shares only the single
  point `lambda = 5/8` with the C1b domain, and its majorant estimates use
  `lambda_- = 5/8` explicitly.
- `analysis/endpoint_kernel_lemma.md`
  (blob `d0d3c45ced474c3346e85de84b08fd64dfcaa345`) and
  `analysis/endpoint_lambda_derivative_kernel.md`
  (blob `62149982f48581e15e437317397f0896e8f0416b`) are both
  `DIAGNOSTIC_ONLY / NOT_BINDING`, `PROTOTYPE / NOT_AUDITED`, and are likewise
  scoped to `[5/8, 33/50]`.
- The "already established C1 endpoint lemma" referenced in §6 of the C2
  interchange lemma has not been located as a binding artefact in this
  repository.

This request therefore does not rely on any regularity premise. Establishing
regularity on `[9/20, 5/8]` and deriving the root statement from it is a
separate obligation, to be predeclared, audited and pinned on its own.

## Pinned machine lineage

C1b machine receipt

```text
analysis/GLOBAL_AXIAL_C1B_MACHINE_RECEIPT.md
blob   bdcafce74b24fbb8ddbbef9fbe381aeaae16caca
commit 0e6040d63b621089883ca28bcba19179aa60b07d
status MACHINE_PASS / C1B_MACHINE_CLOSED / JUDGE_NOT_YET_ISSUED
```

repository head at receipt time = `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`
branch = `implementation/gt-boundary-two-chart`

Implementation blobs

```text
analysis/c1b_resumable_driver.py          5fd308bb4c02c6ddbd612ddbedb18f6b9e22bc3d
producer/global_axial_c1b_producer.py     0616fbd7c9c85f77c8e80b61a5b3b536b45012a8
producer/global_axial_c1b_gating.py       a93ca173ae0bededcd5a0248aa07ac3348f9a243
producer/global_axial_c1b_kernel.py       67dda838369302010ef3d589937b834b96ede4d8
checker/global_axial_c1b_checker.py       0760764ef7592be1ddd4ffec3966e9c6ec930a5b
checker/global_axial_c1b_gating.py        03df262012bfbebcf4d2ea173933186c70abafbf
checker/global_axial_c1b_kernel.py        4eaca55ddf79b437fc756d666294372e5d1a6ba4
```

Contracts and subgate

```text
analysis/GLOBAL_AXIAL_C1B_PRE_RUN_AMENDMENT.md        8e04e2efaf816bab9d9d1f3fd0a9d753538b31ad
analysis/GLOBAL_AXIAL_C1B_BOB_BRIDGE_CONTRACT.md      215193e2fc2a1abcf2aee2527c4c2e6f3176ea6c
analysis/GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md      0f19e3877b9675506ac8f35a5702147a84723c43
producer/global_axial_c1b_bob_producer.py             1a54875e1b93281c32f030081cdccd415827dcea
checker/global_axial_c1b_bob_checker.py               1cded03e6c769adf26ead8b79f31e90dfbf7ce9d
```

Sealed run artefacts

```text
phase 1 (producer) seal   phase1_v212s_seal_20260918T222551Z
  ledger sha256           1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f
phase 2 (checker) seal    phase2_v212s_seal_20260920T140743Z
  ledger sha256           09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38
replay plan sha256        c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69
cross-lineage comparison  c1b_cross_lineage_comparison_20260920T155138Z.json
  sha256                  bb78c0cf36da89877a18fae2ff8067541d12d2e0d3b554ed9b14319988c4bde1
canonical extract table   c1b_receipt_extract.json
  sha256                  8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b
```

Seal directories are mode 555; their `ledger.jsonl` files are mode 444, with
per-file SHA-256 pins. The replay-plan hash equals the value self-declared by
the Phase 1 `segment_end` record, so the checker input is bit-bound to the
producer ledger.

## Machine contract

```text
lambda domain        = [9/20, 5/8]
direction            = increasing lambda
Delta_lambda         = 1/800
coarse slabs         = 140
max depth            = 3
attempted slabs      = 178          (cap 2100)
accepted slabs       = 159          (cap 1120)
producer bits        = 160
checker bits         = 192
series degree        = 50
u_star               = 3/5
tube stages          = T0 (8 t-cells, 4 lambda-cells, 4096 panels)
                       T1 (16, 8, 4096)
                       T2 (32, 16, 8192)
exterior stages      = E0 (1024), E1 (2048), E2 (4096)
left-clamp events    = 0
right-clamp events   = 35   (coarse 105..139, contiguous)
lambda_B             = 931/1600
corner_hull total    = 2212 over 35 slabs
accepted-leaf work   = 356,643,328 panel evaluations
cumulative work      = 408,173,824 panel evaluations
B_ob work            = 81,920 s-panel evaluations per lineage (ceiling 344,064)
```

The checker lineage reconstructs the slab tree, the tube and exterior covers,
the chart inventories and the density independently of the producer, at a
different working precision.

## Evidence to audit

1. **Two-phase replay and its comparison.** The producer searched and certified
   the accepted slab tree; the checker replayed that tree from the bit-bound
   replay plan. The pinned comparison
   (`analysis/c1b_cross_lineage_compare.py`, schema
   `C1B_CROSS_LINEAGE_COMPARISON_V2_4_2`) returned PASS over 178 attempts and
   159 accepts, asserting `A1_EXACT_EQUALITY`, `A2_LINEAGE_INDEPENDENT`,
   `A3_CROSS_LINEAGE_CONSISTENCY`.

2. **Scope of the equality layer.** A.1 has 15 replay-plan data fields; the
   replay record carries those 15 plus `schema`. Generic producer/checker
   equality is applied to 14 of them (`attempt_sequence`, `tree_node`,
   `coarse_index`, `refinement_depth`, `lambda_lo`, `lambda_hi`, `decision`,
   `t_c`, `left_clamp`, `right_clamp`, `t_minus`, `t_plus`, `T_0`,
   `root_gt_t_cells`). `producer_accept_root_outcome` is checked instead by the
   explicit ACCEPT branch, with the checker independently required to report
   `RESOLVED_WITH_CERTIFIED_T_STAR`. Audit that this separation is sound and
   that nothing gated is left uncompared.

3. **Lineage independence.** A.2 retains the lineage-specific tube stage,
   corner boxes, tube guards, exterior guards, root-MV steps, root
   reason/outcome, work, and the Arb enclosures inside those structures; these
   are not equality-compared. The comparison enforces a forbidden-key set
   (`T_star`, `G0`, `Gt`, `Gl`, `Gpar`, `N_k`, `root_mv_steps`) on the replay
   plan and terminates with `COMPARE_REPLAY_A2_LEAK` if any appears. Audit that
   this boundary is drawn correctly — in particular that (A)–(C) do not
   secretly depend on an A.2 quantity being equal across lineages.

4. **The exact cover.** Audit (D) and (E) against the sealed ledgers: coarse
   indices `0..139` distinct and complete; accepted endpoints exactly adjacent;
   first `9/20`, last `5/8`.

5. **The B_ob subgate.** The pinned B_ob machine receipt certifies
   `B_ob(lambda) < 0` on `[9/20, 5/8]`, first passing at stage B1 (32 lambda
   boxes, 2048 s-panels, zero unresolved), worst exact lambda box
   `[793/1280, 5/8]`. The required extension for this run,
   `[931/1600, 5/8]`, is a subinterval of the certified domain. Audit that the
   right-wall condition for the 35 right-clamped slabs is legitimately supplied
   this way.

6. **The reproduced worst upper bound.** The original B_ob run recorded its
   worst enclosure only as `[+/- 0.0421]`, from which the upper endpoint cannot
   be recovered; the acceptance test used `value.upper() < 0` on the Arb object
   and that endpoint was not serialised. The values below are a **reproduction
   measurement** obtained by re-executing the pinned implementation without
   modification. They are not values recorded by the original run.

   ```text
   producer, 160 bit
     [-0.0047719233937436607837435475002795559827518210547840 +/- 2.94e-53]
   checker, 192 bit
     [-0.0047719233937548464067652235739161574663010135954551 +/- 1.39e-53]
   ```

   The reproduction was accepted only after five conditions held in both
   lineages: first pass at B1; unresolved = 0; worst box `[793/1280, 5/8]`;
   default display of the worst ball equal to `[+/- 0.0421]` as in the original
   receipt; upper strictly negative. Audit whether this provenance is adequate,
   and say so explicitly if it is not.

7. **Corner branch interface difference.** The two lineages differ in the
   return-value convention of the corner-cell evaluator: the producer returns
   `(chart, terms)` and sums the three terms at the call site, whereas the
   checker returns `(value, chart)` with the three terms already summed. On the
   35 slabs where the corner branch was actually taken, both lineages reported
   identical `corner_hull` totals (2212) and identical accept decisions. The
   receipt records this as an observed agreement on this run, **not** as a
   general claim of harmlessness. Audit whether the difference can affect any
   quantity entering (A)–(E).

8. **The certified tube versus the bookkeeping cut.** The monotonicity region
   in (A) is `[t_minus, t_plus] x Lambda` and is not truncated at `31/32`. The
   value `T_MID_HI = 31/32` appears in the `middle_partition` bookkeeping: on
   all 35 right-clamped slabs the ledger records
   `["L", 1/2, t_minus]` and `["TUBE", t_minus, 31/32]` while the certified
   tube endpoint is `t_plus = 1`. Audit that no claim is being smuggled across
   that distinction in either direction.

9. **Identification of the wall quantities.** (B) and (C) are stated in terms
   of the machine wall quantities recorded for `g_axis_ob` at `t_minus` and
   `t_plus`. Audit whether those machine quantities are already bindingly
   identified with the stated values of `g_axis_ob`, independently of the open
   regularity obligation above. If that identification itself rests on
   unaudited analytic material, say so rather than treating (B) and (C) as
   settled.

## Requested Judge output

Record exactly one of:

```text
PASS
FAIL: <specific mathematical or provenance defect>
UNRESOLVED: <specific missing obligation>
```

A `PASS` must identify the audited blobs and sealed artefacts, and must be
limited to (A)–(E) as stated above. It must not promote root existence, root
uniqueness, strict monotonicity, the identification of `Gt` with
`partial_t g_axis_ob`, any regularity statement, the C1c assembly consequence,
or any census or global no-fold claim.
