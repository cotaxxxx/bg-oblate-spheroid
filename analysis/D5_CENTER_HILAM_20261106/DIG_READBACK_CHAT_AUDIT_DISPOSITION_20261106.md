# Dig readback — D5 high-lambda centre column audit disposition (2026-11-06)

**Provenance:** Dig-prepared readback of the user's report of chat's completed independent audit and Judge's ruling. **This is not the original chat-authored audit** `CHAT_AUDIT_D5_CENTER_HILAM_20261106.md`. That original was not accessible in GitHub, the available file library or the connected external PC at registration time. No claim is made that Dig has inspected the missing document.

**Reported ruling (user relay):** chat audit PASS; Judge CLOSED for the centre column on `lambda in [2/5,33/50]`, **conditional on the inherited P1 normalization and analytic regularity/derivative-interchange assumptions**. This applies to the centre column only, not all D5 or D4.

## Evidence already registered

Source: `analysis/D5_CENTER_HILAM_20261106/` (C0' exact rational coefficients; paired producer/verifier evidence in M40' and M22' bundles; source snapshots and `REGISTRATION_CHECK.json`).

| Component | Exact acceptance criterion | Recorded calculation |
| --- | --- | --- |
| C0' | `H(0,0;lambda)>=7/5`, lambda in [119/200,33/50] | Dig exact calculation H lower 1.4641310094381321...; 19 rational Bernstein coefficients |
| M40' | `E_rhorhorhorho >= -400`, 0<=rho<=1/8, 0<=z<=lambda/8 | 416/416 producer and 416/416 independent verifier satisfy criterion |
| M22' | `E_rhorhozz >= -200`, axis 0<=z<=lambda/8 | 52/52 producer and 52/52 independent verifier satisfy criterion |

The user's chat audit report states that (a) C0', M40', M22' and (C7') acceptance conditions were independently checked; (b) M40' output-line source SHA data were checked; (c) M22' was independently recomputed on four boxes with audited code; (d) exact normalized outer-endpoint lists matched all producer and verifier rows.

### Cover identities — distinguish byte hashes from geometric normalization

Raw diagnostic cover file SHA-256 (from registered evidence):
- M40': `cfd50476b22b1d01997939688d51893a3d3ceac2c06391b809bfd0a43c719329`
- M22': `f5d0ce5a3169b4bf823c1b81f43eb6bfee5f0f948c62f0ee2fdc9dcd5ce011f5`

Original fixed-file pins in the instruction (different **bytes**):
- M40': `2082e711a4d0e9a68947ed40ed358aff6eb9bab2f6fe34213b068ea3b8a03d87`
- M22': `d7fc47723f35600a0753984e60ca0c1c0494fab3515494f744412a5fc4925580`

**User-supplied normalized geometry SHA-256 (64 hexadecimal digits, not independently recomputed by Dig):** M40' (416 boxes) `8bd4725fe89408f35796607db6d3cb4c1ca384a61e1567327d946e93b780be07`; M22' (52 boxes) `8886d04376b60172df71502ce4c2cbabc7c2cd498f15e1c1b4a4aeda2c55446a`. Normalization is the sorted list of box endpoints rendered as strings of reduced rational fractions. The user reports that chat's independent audit compared the canonical endpoint lists and the producer/verifier results one-to-one and found matching geometry; the raw-byte cover file hashes above remain different, due to serialization/key/order. The original independent audit document is still **not** present for Dig byte-level inspection. Preserve the historical `REGISTRATION_CHECK.json` unchanged as its earlier-time record.

### Arithmetic and domain

With `h=33/50`, the accepted candidate bounds imply, on the high-lambda centre column,

```
H >= 7/5 - (1/64)*max(400/6, h^2*200/2)
  = 7/5 - 25/24 = 43/120 > 0.
```

The low-lambda centre column `lambda in [2/5,119/200]` joins at an included endpoint. Under inherited P1 hypotheses, their union gives `H>0` throughout `r<=1/8`, `tau in [0,1]`, `lambda in [2/5,33/50]`.

`rho=r(1-tau^2)/(1+tau^2)`, `z=lambda*r*2*tau/(1+tau^2)`; hence `rho^2+(z/lambda)^2=r^2`. In particular the D4 delegated box `B_003=[0,1/8]_r x [0,1/8]_tau x [119/200,33/50]_lambda` is contained **including all faces and r=0** in the high-lambda column. D4's separate remaining tasks and D5 general-domain V4 remain open.

## Archival status / allowed further steps

- **Reported mathematical governance status:** `CHAT_AUDIT_PASS / JUDGE_CLOSED_CONDITIONAL_ON_P1` (per user report).
- **Original audit document registration:** `PENDING_ORIGINAL_SOURCE`. User-supplied expected SHA-256 for `CHAT_AUDIT_D5_CENTER_HILAM_20261106.md`: `7eae9f035cac17f806cbdef372f49c68d372918d469d6ec769fa6756459249c4`. The file bytes were not available, so this hash is **not yet verified against the original**. This Dig readback is supplementary, not a replacement for the chat-authored record.
- On receipt of the actual `CHAT_AUDIT_D5_CENTER_HILAM_20261106.md`, add its exact bytes under this directory, independently compare the already recorded complete normalized-cover hashes and source provenance, and replace the provisional references with fixed Git commit/blob identities.
- Do not imply `UPSTREAM_PINS.md` verified promotion, D4 global CLOSED, or D5 V4 FREEZE/full run authorization.
