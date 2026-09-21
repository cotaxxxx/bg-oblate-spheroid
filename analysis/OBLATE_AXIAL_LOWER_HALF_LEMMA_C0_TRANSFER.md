# LOWER-HALF ANALYTIC LEMMA - TRANSFER TO THE C0 BOX

**Status**: `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`

**Premise.** `analysis/OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA.md`,
blob `6fba6e4f981d08201a779be2a435b49954c8b659` (the C1c lemma),
stated on `B = { |t| <= 1/2, 9/20 <= lambda <= 5/8 }`.

**Statement.** Every conclusion of the premise (Lemmas 1-11 and 14-17,
Proposition 12, Corollaries 13 and 18) holds with `B` replaced by

~~~
B0 = { (t,lambda) : |t| <= 1/2,  2/5 <= lambda <= 83/200 },
~~~

with the numerical constants of §1 below and every argument otherwise unchanged.

## §1 Where the lambda-range enters, re-verified on B0

- Lemma 3: `q >= lambda^2/4 >= 1/25`.
- Lemma 4: `w >= lambda >= 2/5`.
- Lemma 5, upper bound: `(1 - lambda^2/2)^2` decreases in `lambda`,
  so its maximum on B0 is at `2/5`: `u <= (23/25)^2 = 529/625 < 1`.
- Lemma 5, interior critical point: `L/a = lambda^2/(1-lambda^2)` increases in `lambda`,
  so `|L t / a| <= (1/2)(83/200)^2/(1 - (83/200)^2) = 6889/66222 < 1`.
- Lemma 6 and Lemma 10: `u_max = 529/625`.
- Lemmas 8 and 9: the lower bounds on `q` and `w` become `1/25` and `2/5`.

## §2 Arguments independent of the lambda-range

Lemmas 1-2 use only `0 < lambda < 1`. The definitions of §2 of the premise use only `0 < a < 1`.
§3.1 and §3.2 use `A >= 1/2` (from `|t| <= 1/2`) and the positivity statements of Lemmas 3-5.
Lemma 7 uses only `|gamma| <= 1`. §3.6 uses the zero locus (`mu = 1`, `mu = -1`, or `a mu + L t = 0`) and continuity.
Lemma 10 uses `|A| <= 3/2` and `u_max`. §4 (Lemma 11, Proposition 12, Corollary 13),
§5 (Lemmas 14-16) and §6 (Lemma 17, Corollary 18) use the lambda-range only through the lemmas above.

## §3 Consequences used by C0 and B

On B0: the C0a quantity is `partial_t^3 g_axis_ob` (Proposition 12 with the §3.6 assembly);
the C0b quantity is `g_axis_ob(1/2,lambda)` (Lemma 11, with `alpha^2 = u R^2` from §3.2),
and `Phi(1/4,lambda) = 2 g_axis_ob(1/2,lambda)` (Lemma 14);
C0a implies that `Phi` is strictly decreasing in `tau` on `[0,1/4]` (Corollary 18);
`Phi(0,lambda) = H_axis_ob(lambda)` (Lemma 15); and
`partial_tau Phi(0,lambda) = (1/6) partial_t^3 g_axis_ob(0,lambda) = c3_ob(lambda)` (Lemma 16),
so C0a at `t = 0` gives the claim of contract B.

Not claimed: any sign; any statement outside B0.
