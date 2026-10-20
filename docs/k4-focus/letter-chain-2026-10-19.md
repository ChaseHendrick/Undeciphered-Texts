# K4 under lagged-Fibonacci letter keys, 19 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

Code: `engine/k4_letter_chain.py`, tests `tests/test_k4_letter_chain.py`. Only the two public clues are used (EASTNORTHEAST at zero-based 21, BERLINCLOCK at 63). This answers the second promised item of the [Gromark family](family-net-2026-10-18.md): "lagged-Fibonacci letter keys exactly, with planted controls", and with it the whole Gromark half of that family except digit keys over two keyed alphabets.

## The model

One cipher alphabet, in place: each plaintext index i sits at alphabet position (plain index + s* R[i]) mod 26, with the key stream R over Z26 a lagged-Fibonacci letter chain,

R[i] = R[i-a] + rec_sign * R[i-b] mod 26, i >= m,

from an m-letter primer R[0..m-1], any lag pair 1 <= a < b <= m, rec_sign +1 or -1 the stream construction, and s = +1 (Vigenere sense) or -1 (Beaufort sense) the application. The digit Gromark is this shape over 0..9 with a head of k and a period wrap; the letter chain has no wrap, which makes the whole model linear.

## Why linear algebra settles it exactly

Every R[i] is a known linear combination of the primer: R[i] = w_i . R[0..m-1] with w_i built by the same recurrence. Two uses of one ciphertext letter at crib positions i and j (the cribs reuse 14 letters, giving 17 pairs) give

(w_i - w_j) . R[0..m-1] = s * (plain_j - plain_i) mod 26.

So the placements are the solutions of a small congruence system in m unknowns. `linear_probe` row-reduces it over Z26 (unit pivots), enumerates the whole affine solution space, and keeps only primers whose stream is consistent across every use and gives the 14 crib letters distinct alphabet indexes (the alphabet is a permutation). Excluded means no primer survives; the enumeration is complete whenever the affine space has at most 200,000 points.

## Result on K4

Canonical lag a = m, b = m - 1 (the Gromark digit rule lifted to letters):

| stream sense | primers excluded | primers that fit |
| --- | --- | --- |
| rec +/-, apply +/- (add stream) | 2 to 10 | 11 (1 primer), 12 (5), 13 (142) |
| rec -, apply +/- (subtract stream) | 2 to 11 | 12 (2), 13 (186) |

The two application senses (adding or subtracting the stream) give identical verdicts letter for letter: the congruence only sees the sign through the right-hand side, and K4's pattern rules both out at the same primer lengths. From the first fitting primer length upward, models exist, so beyond the exclusion window the chain slack no longer constrains the clues - and long primers are anyway the running-key question, whose short-prose half is already excluded and whose general half is an open family of its own.

General lags: every lag pair (a, b) with 1 <= a < b <= m was swept at primer lengths 2 to 10 for both stream senses and both application senses (336 shapes):

- primer lengths 2 to 8: all 84 lag pairs excluded, in all four sign combinations.
- primer length 9: 34 of 36 excluded in the elimination per sign combination; the 2 remaining pairs per combination are SAT-decided and excluded there too, in all four sign combinations.
- primer length 10: 40 or 41 of 45 excluded in the elimination per sign combination; the exact SAT resolves the rest. Every resolved pair is excluded except lag (8, 10), which admits models in both stream senses and both application senses, and in the subtract stream except lag (2, 10) as well.

So the exclusion window is complete for every sign combination: all lag pairs at primer lengths 2 to 9, and at primer length 10 everything except lag (8, 10) and, in the subtract stream, lag (2, 10); the canonical lag runs further (to 10 in the add stream, 11 in the subtract stream) before its first model appears. Across the sweep of 336 lag shapes, 330 are excluded and 3 shapes - each in both application senses - admit models at primer length 10. Every sat answer was confirmed against planted controls of the same shape.

## Cross-checks and controls

- The exact SAT (`check`, stream one-hot per position with the chain added by implication) agrees at the boundary: unsat at canonical m = 2, 3, 5, 8, 10 in both stream senses, sat at m = 11, 12, 13 - the algebra's exclusion windows end exactly where its counting says a primer survives.
- Planted texts under random primers and a shuffled alphabet: the linear probe finds the true primer among the survivors (uniquely at m = 3 and 5; among 3 at m = 13) and the SAT accepts the planted ciphertext at every shape tried: canonical add shapes (m = 3, 5, 13, 14, 20), subtract-recurrence shapes with generic lags (m = 4 with lag (2, 3), m = 6 with lag (1, 4)), and the flipped application sense (m = 5 with lag (1, 2)).
- Two encoding bugs were caught exactly this way before anything was claimed, and each forced a rerun of the affected part from scratch: an enumeration draft read pivot rows without adjusting for the chosen free variables (the planted m = 13 case exposed it, since the true primer's free coordinates were nonzero), and the first SAT wrote R[i] = -(R[i-a] + R[i-b]) under the subtract recurrence instead of R[i] = R[i-a] - R[i-b] - the sign belongs to the b term only, and subtract-shape planted controls are what exposed it. The subtract-stream SAT results in this note are from the corrected model; the elimination ran the correct model throughout.

## What this does not cover

- Digit chains over two keyed alphabets (the Quagmire-Gromark shape), the last untested Gromark-family member promised by the family row.
- Key streams that are not linear in the primer (multiplicative coefficients, nonlinear recurrences, plaintext-dependent chains).
- Fractionation and transposition remains its own open families.

## Computation

PySAT 1.9.dev16 with CaDiCaL 153; the linear sweeps are stock Python runs in seconds; each SAT solve is under half a minute (the boundary case m = 10 takes 23 to 34 seconds). Frozen run records: `work/k4_gromark_variants_scan.json` for the periodic module and the lag-resolver script `work/resolve_lag_pairs.py` for the pending lag pairs (not committed).
