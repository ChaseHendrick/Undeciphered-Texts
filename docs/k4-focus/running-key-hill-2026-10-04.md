# K4 running key and Hill heldout, 4 October 2026

Two bounded checks. Not solved. No plaintext claimed.

Both functions return `solved: false` and `claimed_plaintext: null`. A crib match from either check would be stored as unverified and would still not be a claimed plaintext. Nothing was stored.

These checks are not the repeating Vigenere, Beaufort, keyed Vigenere (`KRYPTOS`), columnar, route, or Vigenere crib-slide bounds in `engine/solvers/k4_attempt.py`.

Ciphertext: the 97-letter `K4_CIPHERTEXT` in that module, beginning `OBKR`. Crib placement uses `cribs_in_place`. The English floor uses `english_pass` (the K3 control already fixed there). `english_pass` was called only after a crib match, because that helper rebuilds its quadgram model on every call. With zero crib matches it was not called.

## Running key

`engine.k4_running_key.search_k4_running_key` decrypts with `engine.solvers.running_key.running_key_decrypt`.

Key texts are plaintext constants already in the repo. A K2 plaintext was not typed in. Letters are counted after dropping non-letters. The key is not repeated and is not wrapped. An offset is a start index that still leaves 97 unused key letters. The offset count is `max(0, letters - 96)`. A text shorter than 97 letters is skipped.

| Key | Source | Letters | Offsets | Tried | Crib-consistent | English-pass | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `KRYPTOS_K3_PLAINTEXT` | `engine.solvers.columnar.KRYPTOS_K3_PLAINTEXT` | 336 | 240 | 240 | 0 | 0 | searched |
| `PUBLISHED_K1_PLAINTEXT` | `tests.test_keyed_vigenere.PUBLISHED_K1_PLAINTEXT` | 63 | 0 | 0 | 0 | 0 | skipped |

K1 skip reason, recorded by the function: "63 letters is shorter than 97. A running key is not repeated, so this text was not used."

Totals over searched keys: tried 240, crib-consistent 0, english-pass 0. Unverified plaintexts stored: 0 (cap 20).

This does not speak to other books, other passages, or a repeated key. It says these two constants, under a non-wrapping running key, did not place the public cribs.

Measured local call: 0.018 seconds.

## Hill 2x2 heldout

`engine.k4_hill_heldout.search_k4_hill_heldout` calls `engine.solvers.hill_inference.infer_hill`. `hill_inference.py` was not changed.

Cribs, zero-based, and not passed together:

| Fold | Fitted crib | Reserved crib, checked only on returned candidates |
| --- | --- | --- |
| A | `Crib(21, "EASTNORTHEAST")` | `BERLINCLOCK` at offset 63 |
| B | `Crib(63, "BERLINCLOCK")` | `EASTNORTHEAST` at offset 21 |

`max_checks` was 100000 and `max_candidates` was 20, both inside the ranges `infer_hill` accepts (`max_checks` 0..100000, `max_candidates` 1..100).

K4 has 97 letters, an odd length. `infer_hill` rejects that before any row trial: "Hill ciphertext requires complete two-letter blocks; missing letters are not padded". Both folds hit that limitation. The call is caught and recorded. No letter was dropped and no padding was added.

| Fold | Candidates checked | Reserved matches | `infer_hill` checks | Search ran |
| --- | ---: | ---: | ---: | --- |
| A | 0 | 0 | 0 | no |
| B | 0 | 0 | 0 | no |

Totals: candidates checked 0, reserved matches 0, unverified stored 0. `reserved_passed_to_fitter` is false on both folds.

A reserved match, had one been returned, would be unverified, not a solve. None was returned, because the fitter did not run. This is a limit of this 2x2 block rule on a 97-letter string, not a test of every Hill-like matrix.

Measured local call: 0.0001 seconds.

## Hill endpoint windows

`search_k4_hill_endpoints` does not pad the 97-letter string. It drops one endpoint so the rest has 96 letters, then runs the same heldout folds.

| Window | Letters used | Fitted examples | Checks per fold | Compatible keys | Reserved matches | Search complete |
| --- | --- | ---: | --- | ---: | ---: | --- |
| drop last letter | first 96 | EASTNORTHEAST at 21, then BERLINCLOCK at 63 | 1352 | 0 | 0 | yes |
| drop first letter | last 96 | offsets shifted by -1 | 1352 | 0 | 0 | yes |

Both public cribs sit inside either window. The reserved crib is not passed to the fitter. Each fold stops after the two row enumerations (676 + 676) because no inverse row satisfies the fitted crib. Pair trials are zero. This is a completed negative for 2x2 Hill on these two windows, not a claim about other matrix sizes or a padded 97-letter model.

## Result

Not solved. No plaintext claimed.

`search_k4_running_key()`, `search_k4_hill_heldout()`, and `search_k4_hill_endpoints()` all leave `solved` false and `claimed_plaintext` null.
