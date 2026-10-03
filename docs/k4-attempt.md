# Kryptos K4: bounded attempt

This note records one small search. The result is **not solved**. No plaintext is claimed.

The search does not say that no method of any kind can read K4. It says that the certified classical routines already in this repo, inside the bounds below, do not produce a 97-letter string that places the public cribs and clears the English check fixed before the run.

## Sources fetched on 2026-10-02

- CIA artifact page, https://www.cia.gov/legacy/museum/artifact/kryptos/ : the page describes the sculpture and says a solution to the fourth section remains elusive. It does not print the 97 letters.
- Wikipedia, "Kryptos", https://en.wikipedia.org/wiki/Kryptos : the passage 4 transcription used below, and the position clues.
- Scientific American, 16 October 2025, https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/ : reports that two writers found Sanborn's plaintext on scraps in a Smithsonian file, that Sanborn confirmed it, and that the file was then sealed. The article does not print the plaintext and says the method was not what they recovered. This search does not use, guess, or restate that sealed text.

## Ciphertext

Wikipedia's passage 4 transcription, letters only, 97 characters, starting at OBKR. The question mark that ends passage 3 is not included. SHA-256 of this ASCII string: `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.

```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

97 is prime, so the only complete rectangles are 1 by 97 and 97 by 1.

## Cribs

Positions are 1-based, as on the Wikipedia page fetched above. The ciphertext fragments on that page match this string.

| Plaintext | Positions | Ciphertext on the page |
| --- | --- | --- |
| EAST | 22 through 25 | FLRV |
| NORTHEAST | 26 through 34 | QQPRNGKSS |
| BERLIN | 64 through 69 | NYPVTT |
| CLOCK | 70 through 74 | MZFPK |

Wikipedia attributes BERLIN (November 2010) and CLOCK (November 2014) to Sanborn via The New York Times, NORTHEAST to a New York Times article of 29 January 2020, and EAST to Sanborn in August 2020.

## Acceptance rule, fixed before the run

A decrypt would count as recovered only if both of these hold:

1. The 97 letters contain EAST, NORTHEAST, BERLIN, and CLOCK at the positions in the table.
2. Its quadgram score from `engine/language.py` is greater than or equal to the score of this known phrase, the first 97 letters of the published K3 plaintext already in the repo: `SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWI`.

The floor is that K3 stretch, not a cutoff tuned on K4. Strings that fail either test are not plaintexts of this attempt. Nothing that passed is stored.

## Methods and bounds

Only certified functions: `vigenere_decrypt`, `search_vigenere_crib`, `solve_vigenere`, `beaufort_decrypt`, `keyed_vigenere_decrypt` (alphabet keyword `KRYPTOS`, the K1 mixed alphabet), `columnar_decrypt_right_to_left`, `double_columnar_decrypt`, and `route_decrypt` (the one certified route, `spiral-cw-top-right`).

Repeating-key periods are 1 through 12. For those periods the four cribs together touch every key column, so each period is either one key or a contradiction. No free key letter was searched. The keyed alphabet is not a search over other keywords. Index letters are A through Z on the fixed `KRYPTOS` alphabet.

Columnar widths are 2 through 12, single and double. The certified columnar code requires a complete rectangle, and no width in that range divides 97, so every columnar call is illegal for this length.

Route widths are 1 through 12, fills `rows` and `cols`. The only width in that range that divides 97 is 1. Those two grids were decrypted. Neither places the cribs.

The Vigenere n-gram solver (`solve_vigenere`, max period 12) returns one best string under the English model. That string does not place the cribs. It is not recorded and it is not a claimed plaintext.

The crib slide (`search_vigenere_crib` on EASTNORTHEAST, periods 1 through 12) can pass only at offset 21, the published start of EAST. It produced no fully determined key there.

Counts from `engine/solvers/k4_attempt.py` (the test checks these lines):

```
vigenere: bound periods 1 through 12; tried 12; decrypted 0; crib-consistent 0; english-pass 0
vigenere-crib-slide: bound search_vigenere_crib EASTNORTHEAST, periods 1 through 12, accept only offset 21; tried 1; decrypted 0; crib-consistent 0; english-pass 0
vigenere-ngram: bound solve_vigenere max_period 12, one run; tried 1; decrypted 1; crib-consistent 0; english-pass 0
beaufort: bound periods 1 through 12; tried 12; decrypted 0; crib-consistent 0; english-pass 0
keyed-alphabet: bound KRYPTOS mixed alphabet, index A through Z, periods 1 through 12; tried 312; decrypted 0; crib-consistent 0; english-pass 0
columnar: bound widths 2 through 12, single and double right-to-left columnar; tried 132; decrypted 0; crib-consistent 0; english-pass 0
route: bound widths 1 through 12, fill rows or cols, route spiral-cw-top-right; tried 24; decrypted 2; crib-consistent 0; english-pass 0
```

## Result

not solved. No plaintext claimed.

`search_k4()` sets `solved` false and `claimed_plaintext` to null. The test `tests/test_k4_attempt.py` asserts that.
