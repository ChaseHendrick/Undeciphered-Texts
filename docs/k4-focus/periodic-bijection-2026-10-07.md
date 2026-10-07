# K4 periodic bijection bound, 7 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

`engine.k4_periodic_bijection`. The model is any in-place periodic substitution: column `i mod p` uses one fixed alphabet, and nothing is assumed about the alphabets. That covers Quagmire I to IV with any keyword, keyed Vigenere, Beaufort and Porta at that period.

Each column alphabet is a bijection. Two crib letters in one column with the same plaintext need the same ciphertext, and the other way round. Both clues are used together: EASTNORTHEAST at 21 and BERLINCLOCK at 63.

| Result | Periods (1 to 32) |
| --- | --- |
| Blocked for every alphabet | 1, 2, 3, 4, 5, 6, 7, 9, 10, 14, 15, 17, 21, 25 |
| Not blocked | 8, 11, 12, 13, 16, 18, 19, 20, 22, 23, 24, 26 to 32 |

Above 32, periods 34, 42, 43, 45 and 50 are also blocked. Example witnesses: at period 1, E at 21 gives F but E at 30 gives G. At period 7, T at 24 and L at 66 both give V.

The control plants both clues in a random text under fresh random alphabets at every period 1 to 32. None is blocked (`tests/test_k4_periodic_bijection.py`).

A period that is not blocked is not fitted. Those periods still need the stronger Quagmire constraint, which says every column is a shift of one keyed alphabet. That needs an SMT search, for example with the optional Z3 engine. This bound says nothing about models that move letters (transpositions) or whose key is not periodic.
