# D5 M22 full-run computational record (2026-11-06)

## Results

- Fixed cover: 39 lambda bands x 4 z bands = 156 boxes, geometric cover PASS.
- Dig producer using Astra's unchanged pilot kernel: 156/156 bounds >= -400 (PASS).
- Independent chat verifier (chat_m22iv.py): 156/156 bounds >= -400 (PASS).
- Paired check: same 156 cover boxes, no missing or duplicate index, all >= -400.
- Both worst cases: index 003, lambda [2/5, 81/200], z [243/6400, 81/1600].
- Dig producer worst: -168.70343052642772 (exact value in bundle).
- Chat verifier worst: -124.51254823389328 (exact value in JSONL).
- Numerical bounds are independent lower bounds; equality is not required for the three
  paired numerical criteria requested in the later Judge instruction.

## SHA-256

- Frozen cover m22_cover_39x4.json:
  aa82f3f8d6f05dd2e5931baabbc99615aa9a1f53169fc678029a4305655b2bd8
- m22_dig_bundle.json:
  73c8aa5fa4817bf65b88f9178c3cef4598f2624389f5c3ffde6e709dd5fe0d74
- Astra pilot.py source:
  a9001a18f322c3d6f1ad3d7afc025f9f82b92f228572177977f31d649d6d46fc
- Dig driver m22_dig_full.py:
  b0f7908b184ded75a85f03ff94e53459c8b3fd5fe9b36304b261bc9e27b65bc5
- chat_m22iv.py:
  b4ea57e134150e57be8ced020eafa4cfd6c740af75d27939b108e23de38d6a89
- chat_m22iv_out.jsonl:
  f398dbc4feda3883f2079c8a5e798c7f2f91850aca364d2d9018fecdd336c4a0

## Audit boundaries

- Computation and aggregation are complete; all three latest Judge paired
  comparison criteria (cover identity, one-to-one correspondence, exact >= -400) PASS.
- An older Dig instruction also asked that Dig/chat midpoint partial sums agree
  digit for digit. This additional condition has NOT been established: sampled
  interval lower bounds for the midpoint sum (indices 000, 003) differ between
  the two independently organized bounds. This alone does not contradict either
  lower bound, but any claim of identical midpoint sums needs separate resolution.
- The Muse one-off verifier-code audit PASS is reported by chat/Judge and was
  not reperformed in this registration.
- Overall D5 integration retains upstream P1 prerequisites (normalization
  and differentiation under the integral).
- The registration does not modify B7 or M40 computations.
