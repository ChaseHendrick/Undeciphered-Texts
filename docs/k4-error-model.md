# Kryptos K4: ciphertext error models

This note records one bounded test. The question was whether K4 stays unsolved because one letter of the ciphertext is wrong. The result is **not solved**. No plaintext is claimed.

The test does not say that no error model of any kind can read K4. It says that the models and bounds below do not produce a string that places the four public cribs and clears the English bar already fixed in [k4-attempt.md](k4-attempt.md).

## Sources fetched on 2026-10-03

- Wikipedia, "Kryptos", https://en.wikipedia.org/wiki/Kryptos : the passage 4 transcription and the position clues. The ciphertext fragments on that page match the string below.
- The 97 letters and the English bar are the ones already fixed in `docs/k4-attempt.md` and `engine/solvers/k4_attempt.py`. This search does not use, guess, or restate any sealed plaintext.

## Ciphertext

Wikipedia's passage 4 transcription, letters only, 97 characters, starting at OBKR. SHA-256 of this ASCII string: `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.

```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

## Cribs

Positions are 1-based, as on the Wikipedia page fetched above.

| Plaintext | Positions | Ciphertext on the page |
| --- | --- | --- |
| EAST | 22 through 25 | FLRV |
| NORTHEAST | 26 through 34 | QQPRNGKSS |
| BERLIN | 64 through 69 | NYPVTT |
| CLOCK | 70 through 74 | MZFPK |

## Acceptance rule

A decrypt would be recorded only as an unverified candidate, and only if both of these hold:

1. After the edit, EAST, NORTHEAST, BERLIN, and CLOCK sit at the positions that edit assigns. A substitution or a neighbor swap keeps the published positions. A deletion or insertion keeps each crib word contiguous and shifts a crib only when the edit is strictly before that crib.
2. The quadgram score from `engine/language.py` meets the bar in `docs/k4-attempt.md`: the score of the first 97 letters of the published K3 plaintext. A 97-letter string is compared by that total (higher is better). A 96-letter or 98-letter string is compared by the mean per quadgram, so a shorter string does not pass by summing fewer terms.

The search does not call any such string a solution. `claimed_plaintext` stays null. In this run the second test was never reached, because no edit produced a key.

## Why the search stops early

On the unmodified ciphertext, Vigenere and Beaufort at periods 1 through 8 are already key-inconsistent: 16 trials, 0 keys. NORTHEAST is 9 consecutive letters, and 9 covers every residue of periods 1 through 8, including after a tail shift that keeps that word intact. A returned key would have no free letter. The code raises if a residue is uncovered. It does not search a free key letter.

A substitution outside the 24 crib letters cannot change that forced key. Those 73 positions are not enumerated. A neighbor swap that does not touch a crib letter is skipped for the same reason. A deletion or insertion inside a crib word would split the word, so those sites are skipped.

## Methods and bounds

Only `vigenere_decrypt` and `beaufort_decrypt` (the integer maps were checked against those two functions). Periods are 1 through 8. No other cipher, and no period above 8.

1. One substituted letter. Only the 24 crib positions, and only the 25 other letters. 24 times 25 times 2 ciphers times 8 periods.
2. One adjacent transposition. Only a swap of neighbors that touches a crib letter: 26 swaps.
3. One deleted letter, or one inserted letter, only where every crib word stays contiguous. 73 deletion sites. 78 insertion sites (before EAST, between EAST and NORTHEAST, between NORTHEAST and BERLIN, between BERLIN and CLOCK, and after CLOCK), each with 26 inserted letters. Cribs that start after the edit shift by one.

Counts from `engine/solvers/k4_error_model.py` (the test checks these lines):

```
unmodified-precondition: bound no edit; Vigenere and Beaufort periods 1 through 8; must be key-inconsistent; tried 16; key-consistent 0; crib-consistent 0; bar-pass 0
substitution: bound one substituted letter at a crib position only (24 positions, 25 other letters); 73 non-crib positions skipped because the forced key cannot change; Vigenere and Beaufort periods 1 through 8; tried 9600; key-consistent 0; crib-consistent 0; bar-pass 0
adjacent-swap: bound one neighbor swap that touches a crib letter (26 swaps); swaps outside the cribs skipped; Vigenere and Beaufort periods 1 through 8; tried 416; key-consistent 0; crib-consistent 0; bar-pass 0
deletion: bound one deleted letter that leaves every crib word contiguous, tail cribs shifted (73 sites); Vigenere and Beaufort periods 1 through 8; bar is the per-quadgram mean of the K3 control; tried 1168; key-consistent 0; crib-consistent 0; bar-pass 0
insertion: bound one inserted A-Z letter that leaves every crib word contiguous, tail cribs shifted (78 sites, 26 letters); Vigenere and Beaufort periods 1 through 8; bar is the per-quadgram mean of the K3 control; tried 32448; key-consistent 0; crib-consistent 0; bar-pass 0
```

## Result

not solved. No plaintext claimed.

`search_k4_errors()` sets `solved` false, `claimed_plaintext` to null, and `unverified` empty. Every model has `key-consistent` 0, `crib-consistent` 0, and `bar-pass` 0. The test `tests/test_k4_error_model.py` asserts that the search does not emit a claimed plaintext.
