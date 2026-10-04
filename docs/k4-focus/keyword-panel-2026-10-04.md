# K4 keyword panel, 4 October 2026

This note records one keyword panel. The result is **not solved**. No plaintext is claimed.

The keyword list is the published K1/K2 keys plus the KRYPTOS alphabet keyword, not a search over a dictionary. The three strings are already printed in this repo:

- `PALIMPSEST`, the published K1 key in `tests/test_keyed_vigenere.py`
- `ABSCISSA`, the published K2 key in the same file
- `KRYPTOS`, `KEYED_ALPHABET_KEYWORD` in `engine/solvers/k4_attempt.py`

No other word was tried. A crib match is not a K4 decipherment. `keyword_panel()` sets `solved` false and `claimed_plaintext` to null. A 97-letter decrypt that places the public cribs would be stored only as unverified, and at most 20 of those. This run stored none.

## Ciphertext

The panel uses `K4_CIPHERTEXT` from `engine/solvers/k4_attempt.py`: 97 letters, starting at OBKR. SHA-256 of that ASCII string, the same digest recorded in `docs/k4-attempt.md`:

`eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`

97 is odd. Playfair and two-square fold J to I inside `two_square_letters` and still see 97 letters, so the odd length remains. Both decryptors raise when the length is odd. The panel does not drop a letter and does not pad with a letter that was not in the ciphertext.

## Methods

Each call uses a decryptor already in this repo. `tried` counts only returns of 97 letters. A raise, or a return of any other length, counts as `rejected`. `tried` + `rejected` is 3 for each single-keyword method and 6 for two-square.

- `playfair_decrypt`: one keyword square for each of the three keywords.
- `porta_decrypt`: one repeating keyword for each of the three keywords. All three returned 97 letters. None placed the cribs. None cleared the English check in `english_pass`.
- `gromark_decrypt`: the key argument is the keyword alone. That function also requires a 5-digit primer (`split_gromark_key`). No primer is among the three keywords, and none was added. Each of the three calls raised and is rejected.
- `two_square_decrypt`: squares come from `square_from_keyword` (the helper re-exported by `engine/solvers/two_square.py`, defined in `engine/ciphers.py`). Every ordered pair of two different keywords is called: 6 pairs, not 9. Same-keyword pairs are not called. A pair would be skipped only if the square helper raised; it did not. All six decrypt calls raised because the length is odd.

Cribs are the four public positions checked by `cribs_in_place`. The English check is `english_pass` against the K3 control already fixed in `k4_attempt.py`. Neither check promotes a string to a claimed plaintext.

## Tallies

Counts from `engine/k4_keyword_panel.py`:

```
playfair: bound one square per keyword PALIMPSEST, ABSCISSA, KRYPTOS; odd length rejected, not padded; tried 0; rejected 3; crib-consistent 0; english-pass 0
porta: bound one repeating keyword per PALIMPSEST, ABSCISSA, KRYPTOS; tried 3; rejected 0; crib-consistent 0; english-pass 0
gromark: bound keyword alone for PALIMPSEST, ABSCISSA, KRYPTOS; no primer added; tried 0; rejected 3; crib-consistent 0; english-pass 0
two-square: bound 6 ordered pairs of two different keywords; same-keyword pairs not called; odd length rejected, not padded; tried 0; rejected 6; crib-consistent 0; english-pass 0
```

Unverified crib-consistent strings: 0.

## Result

not solved. No plaintext claimed.

`tests/test_k4_keyword_panel.py` runs this panel and asserts that `solved` is false, that `claimed_plaintext` is null, that the four methods above are covered, and that `tried` + `rejected` equals 3 for each keyword method and 6 for the ordered pairs.

The panel does not say that no keyword of any kind can read K4. It says that these three published strings, under these four decryptors, do not.
