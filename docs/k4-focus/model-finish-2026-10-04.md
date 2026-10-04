# K4 finite model space finish, 4 October 2026

**No historical plaintext is claimed.** This run finishes the family space left partial by the [3 October 2026 model experiment](model-experiments-2026-10-03.md). `claimed_plaintext` is null and `solved` is false. A crib fit is not a decipherment.

The machine-readable record is [model-finish-2026-10-04.json](model-finish-2026-10-04.json).

## What was searched

The ciphertext is the 97-letter `K4_CIPHERTEXT` constant in `engine/solvers/k4_attempt.py`. Its ASCII SHA-256 is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.

Each call uses one family, alphabets A-Z and `KRYPTOSABCDEFGHIJLMNQUVWXZ`, orders substitute-then-transpose and transpose-then-substitute, `max_period=32`, `max_width=32`, `max_checks=10000`, and `max_candidates=10000`. One family is 8,128 hypotheses, so it finishes under the check cap. Four families are the 32,512 hypotheses of one fold. Two folds make eight searches.

Fold A fits only EASTNORTHEAST at offset 21 and afterwards checks BERLINCLOCK at offset 63. Fold B fits only BERLINCLOCK at offset 63 and afterwards checks EASTNORTHEAST at offset 21. The reserved word is not passed into search. Comparison uses original plaintext coordinates. A question mark is not a match. A determined mismatch is a contradiction and is counted; those candidates are not dropped.

A reserved exact prediction means every letter of the reserved word is present and equal, and the candidate has a complete key (`key_complete` true and no unknown key slots). A full reserved-span match with an incomplete key is counted separately. It is not an exact prediction and not a solve.

## Counts

| Fold | Family | Checks | Search complete | Compatible | Complete keys | Reserved contradictions | Underdetermined | Incomplete span matches | Reserved exact predictions |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | repeating | 8,128 | yes | 3,212 | 146 | 2,790 | 422 | 0 | 0 |
| A | plaintext-autokey | 8,128 | yes | 3,214 | 147 | 2,786 | 428 | 0 | 0 |
| A | ciphertext-autokey | 8,128 | yes | 2 | 0 | 2 | 0 | 0 | 0 |
| A | beaufort | 8,128 | yes | 3,220 | 148 | 2,798 | 422 | 0 | 0 |
| B | repeating | 8,128 | yes | 3,713 | 150 | 3,284 | 429 | 0 | 0 |
| B | plaintext-autokey | 8,128 | yes | 3,708 | 148 | 3,273 | 435 | 0 | 0 |
| B | ciphertext-autokey | 8,128 | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| B | beaufort | 8,128 | yes | 3,707 | 149 | 3,280 | 427 | 0 | 0 |
| both | all | 65,024 | yes | 20,776 | 888 | 18,213 | 2,563 | 0 | 0 |

Checks per call are in the JSON `checks_per_call` list. Compatible models total 20,776. Reserved contradictions total 18,213. Reserved exact predictions total 0.

## Result

Every call returned `search_complete` true. Each call used 8,128 checks, matching its requested model count. Eight calls used 65,024 checks. That is one full 32,512-hypothesis fold for EASTNORTHEAST and one full fold for BERLINCLOCK.

The completed family space produced no reserved exact predictions. No model with a complete key predicted the reserved word at its public offset.

Complete keys: 888. All 888 contradicted the reserved crib. None left a reserved letter unknown, and none was a reserved exact prediction.

Incomplete-key reserved span matches: 0. No compatible model spelled the full reserved word while leaving a key slot unknown.

Underdetermined reserved comparisons: 2,563. At least one reserved letter stayed unknown, and no determined letter disagreed.

Completing an unknown key slot from the reserved letters would change the experiment and remove that group's heldout role. This run does not do that.

Coverage of this finite list is not a unique key and not a historical reading. Other alphabets, arbitrary column permutations, extra layers, transcription edits, and other mechanisms stay outside this space. The 3 October run stopped at `check_limit` after 4,916 checks per fold. Where this record shows `search_complete` true, those previously untested combinations in the same family list were included.

No historical plaintext is claimed.
