# K4 under Gromark variants: the digit bound generalized and Periodic Gromark as SAT, 19 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

Code: `engine/k4_gromark_variants.py`, tests `tests/test_k4_gromark_variants.py`. Only the two public clues are used (EASTNORTHEAST at zero-based 21, BERLINCLOCK at 63), so each result holds whatever language the rest of K4 is in. This closes the Gromark half of the family the [neural prior](family-net-2026-10-18.md) opened and the [fractionation note](fractionation-2026-10-18.md) narrowed.

## The digit bound, in its general form

The committed obstruction (`engine/k4_gromark_obstruction.py`) blocks in-place ACA Gromark for any keyword because ciphertext letters F, K and P cannot share one alphabet index with both clues while every shift is a digit 0 to 9. That argument never used the chain addition, the primer length or the alphabet construction. The module states it in its general form and machine-checks it: with one cipher alphabet and shifts by digits only, the same argument covers

- the ACA add sense and the Beaufort subtract sense (the condition d1 - d2 congruent to the plain-index difference is the same set of allowed differences both ways),
- any primer length, recurrence and lag, because the argument ties single-letter pairs only.

So "Gromark with other digit keys on one keyed alphabet" is excluded in full, not just for the ACA rule. Controls: the ACA sheet example is first recovered as a known-plaintext check, then 20 planted 97-letter windows with both clues under random keywords and primers are enciphered with the repo's `gromark_encrypt`; none produces an empty domain under either sense.

## Periodic Gromark, keyword left free

`engine.solvers.periodic_gromark` with a head of k distinct letters encrypts each plaintext index i at alphabet position (plain index + s[(i//k)%k] + r[i]) mod 26, where s are the head letters' positions in the keyword-built mixed alphabet and r is the rank-digit chain extended by (r[i-k] + r[i-k+1]) mod 10. With the keyword left free, the model is written as SAT (CaDiCaL through PySAT) over a **relaxed space that is a superset of every real head of length k**:

- s[g] is any distinct value in 0 to 25 (a real head gives distinct positions, but not every set is realizable at once);
- rho is any permutation of 1 to k as the primer (in a real head the ranks are tied to the same head letters, not to s freely);
- the cipher index of each crib letter is free per letter (a real alphabet ties all of them into one permutation).

An unsatisfiable model in the relaxed space is therefore unsatisfiable for every keyword of that length. Fitted clue letters are unit-facts; held-back clue letters are guarded constraints counted as forced right, forced wrong or free, the convention of `engine/k4_fractionation.py`.

| head length k | both clues | fit EASTNORTHEAST (11 of BERLINCLOCK held back: right/wrong/free) | fit BERLINCLOCK (13 of EASTNORTHEAST held back) |
| --- | --- | --- | --- |
| 2 | unsat | unsat | unsat |
| 3 | unsat | sat, 0/6/5 | unsat |
| 4 | unsat | unsat | sat, 0/3/10 |
| 5 | unsat | unsat | sat, 0/3/10 |
| 6 | unsat | sat, 0/2/9 | sat, 0/0/13 |
| 7 | unsat | sat, 0/3/8 | sat, 0/2/11 |
| 8 | unsat | sat, 0/0/11 | sat, 0/0/13 |
| 9 | unsat | sat, 0/0/11 | sat, 0/0/13 |

Read together with the both-clue column: head lengths 2 to 4 cannot place EASTNORTHEAST and 2 to 3 cannot place BERLINCLOCK even alone; the fits that run at 3, 4, 5, 6 and 7 force held-back clue letters to be wrong letters; head lengths 8 and 9 fit each clue alone but no key places both, which is the strongest form of the exclusion there is for those lengths.

Cross-checks and controls:

- Exhaustive enumeration of the relaxed space (all distinct s values, all rank permutations, per-letter cipher indexes) places both clues at 0 of 1,300 configs at head length 2 and 0 of 93,600 at head length 3, matching the SAT answers.
- Three independent solvers (CaDiCaL, Glucose, MiniSat) give the same unsat answer on shared head lengths (2, 5, 8), ruling out a solver-specific artifact.
- 16 planted ciphertexts under random keywords (head lengths 2 to 9 cycling) with both clues at the public offsets are never blocked; the true key pinned as SAT assumptions is always accepted.
- On 8 further planted texts each clue was fitted in turn; the held-back clue letters are never forced wrong (wrong = 0 everywhere), so the fold probe has no false contradictions.
- The SAT encoding was compared against the repo's own encryptor letter by letter on planted instances before any K4 run.

## What this does not cover

- Gromark-like digit keys over per-group alphabets (two keyed alphabets, a Quagmire-Gromark shape): one alphabet is what the F, K, P bound needs, and Periodic Gromark's one alphabet is what the SAT above needs.
- A lagged-Fibonacci chain over letters (mod 26) instead of digits: the key stream then leaves 0..25 shifts, which is more than the digit rule allows.
- Fractionation away from in-place letter positions: fractionated Morse shifts the letters, so the published positions cannot be applied as they stand; a 6 by 6 bifid square and cubes beyond 27 cells hold all 26 letters.
- Any transposition before or after (the wide-columnar family is its own open row).

## Computation

PySAT 1.9.dev16, CaDiCaL 153, one process per head length, 8 workers on a 10-core M1 Pro. The full scan (both clues, both folds, head lengths 2 to 9) plus controls runs in minutes; the frozen JSON result of the run is `work/k4_gromark_variants_scan.json` (not committed; the numbers above are the frozen record).

## Ledger

The open family is narrowed to "Fractionation beyond one 25-cell square and standard trifid": bigger squares and cubes, other cell counts and reading conventions, and fractionated Morse. The next listed step is exact clue models for a 6 by 6 bifid square and larger cubes with planted controls, and no Morse-framed search without a sourced convention for where the clues would sit.
