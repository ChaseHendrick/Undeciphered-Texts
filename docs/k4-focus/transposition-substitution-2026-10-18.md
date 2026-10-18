Not solved. No plaintext claimed.

# K4 as transposition plus periodic substitution, 18 October 2026

`solved` is false and `claimed_plaintext` is null. Nothing below is a reading of K4.

Code: `engine/k4_transposition_sub.py` with the compiled kernel `engine/k4_transposition_sub.c`. Tests: `tests/test_k4_transposition_sub.py`.

## Model and evidence

A hypothesis is a transposition T, an order of composition and a period p from 1 to 26. T[j] is the ciphertext position of plaintext position j.

- Transpose then substitute: C[i] = sub(i mod p)(Pt[i]) with Pt[T[j]] = P[j]. Clue letter P[j] shows at ciphertext position T[j] and uses column T[j] mod p.
- Substitute then transpose: S[j] = sub(j mod p)(P[j]) and C[T[j]] = S[j]. Clue letter P[j] uses column j mod p and shows at T[j].

The only evidence is the two published clues, EASTNORTHEAST at zero-based plaintext position 21 and BERLINCLOCK at 63 (`CRIB_SPANS` in `engine/k4_gromark_obstruction.py`). Each hypothesis gives 24 (column, plaintext letter, ciphertext letter) triples. Nothing about the other 73 letters is scored, so a hypothesis excluded here is excluded whatever language the plaintext is in.

1. Bijection bound (the test of `engine/k4_periodic_bijection.py`). Any alphabet in each column is allowed. A hypothesis is excluded when one column needs one plaintext letter to go to two ciphertext letters, or two plaintext letters to go to one. This is exact.
2. Strong filter, only on bijection survivors. Straight Vigenere (rank(c) = rank(p) + k) or Beaufort (rank(c) = k - rank(p)) on the A-Z alphabet or on the KRYPTOS keyed alphabet `KRYPTOSABCDEFGHIJLMNQUVWXZ`, one shift per column. Variant Beaufort imposes the same one-shift-per-column condition as Vigenere, so it is covered by the Vigenere count. A hypothesis survives when no column needs two shifts. Its key is complete when every column holds at least one clue letter; only then can the whole text be decrypted.

Two text lengths are run.

- n = 97 is K4 as carved (`K4_CIPHERTEXT` in `engine/solvers/k4_attempt.py`).
- n = 98 puts the "?" that ends K3 on the sculpture in front of K4 as ciphertext position 0. The clue positions move up by one (22 and 64). The bijection bound treats "?" as a 27th symbol. The strong filter never lets a clue letter encipher to "?".

## Transposition families and why each was built

**a. Columnar, every column order.** Write the text in rows of width w with an incomplete last row (the first n mod w columns are one letter longer), then read whole columns in any order. Direction 0 is that reading; direction 1 is its inverse (write down the columns in order, read rows). Widths 2 to 10, all w! orders, so 4,037,912 orders and 8,075,824 transpositions per length (not deduplicated across directions). Reason: K3 is a keyed columnar transposition in the NSA description quoted in `engine/solvers/columnar.py`, and the earlier layered run only tried identity and keyword orders. Width 10 was run in full; it did not need projecting.

**b. K3-style double rotation.** Sanborn's K3 coding chart writes the text in a grid, turns it a quarter turn, rewrites it into a second grid and turns it again ([Wikipedia, Kryptos](https://en.wikipedia.org/wiki/Kryptos); the repo's `kryptos_k3_sanborn_encrypt` uses 8 rows of 42 then rows of 14). One step here: write n letters in rows of w; the last row is short when w does not divide n, with its letters either in the leftmost cells ("left") or the rightmost ("right"); turn clockwise (read the columns left to right, each bottom to top) or anticlockwise (columns right to left, each top to bottom); empty cells are skipped. Two steps are composed with every w1 and w2 from 1 to n, both turn directions for each step, and both alignments for each step where the row is short. That is 147,456 raw pairs for n = 97 (144,846 distinct) and 144,400 for n = 98 (140,566 distinct).

K3 check: with w1 = 42, w2 = 14 and two clockwise turns on 336 letters, the same code turns `KRYPTOS_K3_PLAINTEXT` into `KRYPTOS_K3_CIPHERTEXT` exactly and back. K3 is reproduced, so the family includes the K3 method itself.

**c. Routes.** Every rectangle of width 2 to n - 1 (rows = ceil(n / w)), filled by rows, empty cells at the right end of the last row. Base routes: rows, row boustrophedon, columns, column boustrophedon, spiral inward clockwise and anticlockwise, and diagonals in both diagonal directions, each read down, up, or zigzag. Each base route is taken from all four corners (the four reflections of the grid), forwards and backwards, both as the reading route (write rows, read route) and as the writing route (the inverse). 18,240 raw for n = 97 (6,994 distinct) and 18,432 for n = 98 (7,052 distinct). Reason: route transpositions are the classic family next to columnar ([Wikipedia, Transposition cipher](https://en.wikipedia.org/wiki/Transposition_cipher)), and K2 as first published ended "ID BY ROWS".

**d. Keyed columnar and Myszkowski.** Frozen keywords: KRYPTOS, PALIMPSEST, ABSCISSA (the K1 to K3 keywords), BERLIN, CLOCK, BERLINCLOCK, EASTNORTHEAST (the published clues), SANBORN, SCHEIDT, LANGLEY, SHADOW, IQLUSION, UNDERGRUUND, LAYERTWO, plus IDBYROWS (the original K2 ending that Sanborn corrected to "X LAYER TWO" in 2006) and CARTER (K3 paraphrases Howard Carter's account of opening Tutankhamun's tomb), both from [Wikipedia, Kryptos](https://en.wikipedia.org/wiki/Kryptos). For each keyword: keyed columnar (alphabetical order, ties left to right) and the inverse convention of the same key, each in both directions; and Myszkowski as on the [ACA sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Myszkowski.pdf) and its inverse. 96 raw, 80 distinct per length. Keywords of 10 letters or fewer are also inside family a.

## Results on K4

Hypotheses = transpositions x 26 periods, for each order of composition. Strong survivors count hypotheses that pass at least one of the four strong variants. 855,465,832 hypotheses in all.

| Family | n | Transpositions | Order | Hypotheses | Excluded by bijection | Bijection survivors | Strong survivors (any of 4) | Complete-key strong survivors |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| a columnar | 97 | 8,075,824 | transpose then substitute | 209,971,424 | 155,308,675 | 54,662,749 | 52,967 | 2,338 |
| a columnar | 97 | 8,075,824 | substitute then transpose | 209,971,424 | 118,127,105 | 91,844,319 | 1,316,078 | 0 |
| a columnar | 98 | 8,075,824 | transpose then substitute | 209,971,424 | 154,635,165 | 55,336,259 | 51,061 | 2,518 |
| a columnar | 98 | 8,075,824 | substitute then transpose | 209,971,424 | 120,737,850 | 89,233,574 | 1,109,259 | 0 |
| b rotation | 97 | 144,846 | transpose then substitute | 3,765,996 | 2,689,621 | 1,076,375 | 17,620 | 342 |
| b rotation | 97 | 144,846 | substitute then transpose | 3,765,996 | 2,164,875 | 1,601,121 | 20,093 | 0 |
| b rotation | 98 | 140,566 | transpose then substitute | 3,654,716 | 2,604,836 | 1,049,880 | 17,764 | 477 |
| b rotation | 98 | 140,566 | substitute then transpose | 3,654,716 | 2,090,560 | 1,564,156 | 15,359 | 0 |
| c route | 97 | 6,994 | transpose then substitute | 181,844 | 120,155 | 61,689 | 813 | 65 |
| c route | 97 | 6,994 | substitute then transpose | 181,844 | 104,326 | 77,518 | 935 | 0 |
| c route | 98 | 7,052 | transpose then substitute | 183,352 | 121,424 | 61,928 | 903 | 90 |
| c route | 98 | 7,052 | substitute then transpose | 183,352 | 104,644 | 78,708 | 839 | 0 |
| d keyword | 97 | 80 | transpose then substitute | 2,080 | 1,549 | 531 | 3 | 0 |
| d keyword | 97 | 80 | substitute then transpose | 2,080 | 1,197 | 883 | 15 | 0 |
| d keyword | 98 | 80 | transpose then substitute | 2,080 | 1,540 | 540 | 2 | 0 |
| d keyword | 98 | 80 | substitute then transpose | 2,080 | 1,196 | 884 | 7 | 0 |

### Where the survivors are

- Bijection bound: periods 1 and 2 are excluded for every transposition in every family, order and length. For substitute then transpose, period 3 is also fully excluded everywhere, and period 9 is fully excluded except 21 columnar hypotheses at n = 98. Survivors grow with the period. Per-period counts are in the tables below.
- Strong filter: no hypothesis in any family, order or length survives at any period from 1 to 20. Families a, c and d have none at 21 either; family b at n = 98 has 2 at period 21. Every strong survivor is at period 21 to 26. For substitute then transpose they are all at 24 to 26 and none has a complete key.
- Complete keys occur only for transpose then substitute at periods 21 to 24. At period p a complete key fixes p shifts from 24 clue letters, so only 24 - p clue letters test anything: 3 at most, and 0 at period 24. The 3,968 period-24 complete-key records of family a at n = 97 (4,896 at n = 98) and the 148 of family c (four variants per transposition) come from transpositions that put all 24 clue letters in 24 different columns; every key fits them, and the same number appears on the shuffled controls below.

### Complete-key candidates (unverified)

Every complete-key survivor was decrypted. The clue letters come back by construction. Records counted (one per variant): 5,332 (a, 97), 6,190 (a, 98), 527 (b, 97), 635 (b, 98), 180 (c, 97), 204 (c, 98), 0 (d). The best English quadgram score per letter (`engine.language`, letters only) in each group is listed below. For scale: the first 97 letters of the K3 plaintext score -1.92; 300 strings of random letters with both clues planted average -6.46, best -5.68. None of these is a reading.

| Family | n | Transposition | Order, period, variant | Clue letters tested | Score | IC | Unverified decryption |
| --- | ---: | --- | --- | ---: | ---: | ---: | --- |
| a | 97 | width 10, order 4 7 6 3 9 1 8 5 2 0, direction 1 | transpose then substitute, 24, Beaufort KRYPTOS | 0 | -5.388 | 0.0427 | QVCKTOPBIVHLFGCOSQIYJEASTNORTHEASTPLPEOXYRTVSGUBUTNNCZOVVISAHABBERLINCLOCKYTROVHGCINYVTKDMGIRESIB |
| a | 98 | width 10, order 5 3 7 4 8 0 9 6 1 2, direction 1 | transpose then substitute, 24, Beaufort KRYPTOS | 0 | -5.306 | 0.0427 | QVCKTOPBIVOVHGCINYVTYJEASTNORTHEASTPLPEOHLFGCOSQI?XYRTVSGUBSAHABBERLINCLOCKYTRKDMGIRESIBUTNNCZOVVI |
| b | 97 | w1 41 clockwise left, w2 82 clockwise left | transpose then substitute, 24, Beaufort KRYPTOS | 0 | -5.145 | 0.0406 | RXWFGIEIICHRISKYSSYIREASTNORTHEASTKBKJWGQNUBULYNDIKDTUMRIRPJJDSBERLINCLOCKBOYPTTMEPWBXLGPENSAFTOY |
| b | 98 | w1 40 clockwise left, w2 32 clockwise right | transpose then substitute, 23, Beaufort A-Z | 1 | -5.233 | 0.0447 | LLUBRLELLSOCRIOCEJQPXYEASTNORTHEASTTWMIADSBONEKSWNGYYPQHGUOPKBS?BERLINCLOCKFOELPJOYYODGUNIYNFGTBOP |
| c | 97 | width 5, column boustrophedon, corner 1, written | transpose then substitute, 24, Vigenere A-Z | 0 | -5.723 | 0.0447 | VPCQSTGSEIVJAJUYORLHJEASTNORTHEASTHRPTIPHCURBSYBLIPIMQUUEOJYREHBERLINCLOCKMYJLUMLWYHULHRETMIICFGC |
| c | 98 | width 62, row boustrophedon, corner 1, reversed, read | transpose then substitute, 24, Beaufort A-Z | 0 | -5.688 | 0.0374 | HKZZMIGHBHVWUNBZTPNDLLEASTNORTHEASTWOURWWWOYRAVUXYMFKKCZZHVTTSIMBERLINCLOCKAPSYRJTBAFPCXNAAKFLIAV? |

Each of these is the maximum over hundreds or thousands of fits that test at most one clue letter. The shuffled controls below give best scores in the same range, so the scores are what selection alone produces.

## Controls

### Planted clues are never excluded

For each family, 200 trials (alternating n = 97 and 98): random letters with both clues planted at their positions, a random transposition from the family, a random order, a random period 1 to 26 and a random alphabet in every column. The bound in Python and in the C kernel was applied to the true (T, order, p).

| Family | Trials | True hypothesis excluded | Strong-filter trials (random Vigenere or Beaufort key on A-Z or KRYPTOS) excluded | Complete keys | Plaintext recovered exactly |
| --- | ---: | ---: | ---: | ---: | ---: |
| a columnar | 200 | 0 | 0 | 111 | 111 |
| b rotation | 200 | 0 | 0 | 110 | 110 |
| c route | 200 | 0 | 0 | 116 | 116 |
| d keyword | 200 | 0 | 0 | 104 | 104 |

The test also plants a width-6 columnar with a Vigenere or Beaufort key at period 7 and checks that the full enumeration of all 720 orders lists the true order, direction, period and variant among its complete-key survivors, at both lengths. The kernel agrees with the Python reference count for count on random permutations, and with the identity permutation it reproduces the in-place blocked periods of `engine.k4_periodic_bijection` (1 to 7, 9, 10, 14, 15, 17, 21, 25).

### Power: how often a wrong hypothesis is excluded

On 10 planted texts per family (random alphabets), 400 random wrong transpositions from the same family were each checked at all 26 periods and both orders. Fraction excluded by the bijection bound:

| p | a TS | a ST | b TS | b ST | c TS | c ST | d TS | d ST |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 2 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.999 | 1.000 | 1.000 | 1.000 |
| 4 | 0.996 | 1.000 | 0.999 | 1.000 | 1.000 | 1.000 | 0.998 | 1.000 |
| 5 | 0.986 | 0.998 | 0.993 | 1.000 | 0.993 | 1.000 | 0.993 | 1.000 |
| 6 | 0.954 | 0.792 | 0.977 | 0.778 | 0.922 | 0.790 | 0.970 | 0.779 |
| 7 | 0.928 | 0.738 | 0.915 | 0.714 | 0.860 | 0.685 | 0.933 | 0.696 |
| 8 | 0.895 | 0.614 | 0.941 | 0.664 | 0.853 | 0.692 | 0.920 | 0.655 |
| 9 | 0.921 | 1.000 | 0.929 | 1.000 | 0.947 | 1.000 | 0.918 | 1.000 |
| 10 | 0.860 | 0.505 | 0.887 | 0.544 | 0.786 | 0.553 | 0.842 | 0.564 |
| 11 | 0.787 | 0.459 | 0.775 | 0.459 | 0.739 | 0.448 | 0.890 | 0.473 |
| 12 | 0.774 | 0.374 | 0.802 | 0.400 | 0.674 | 0.442 | 0.828 | 0.413 |
| 13 | 0.746 | 0.331 | 0.700 | 0.358 | 0.612 | 0.353 | 0.746 | 0.357 |
| 14 | 0.612 | 0.365 | 0.658 | 0.354 | 0.560 | 0.330 | 0.654 | 0.326 |
| 15 | 0.662 | 0.975 | 0.712 | 0.974 | 0.684 | 0.972 | 0.757 | 0.974 |
| 16 | 0.619 | 0.242 | 0.652 | 0.269 | 0.490 | 0.290 | 0.666 | 0.249 |
| 17 | 0.599 | 0.968 | 0.634 | 0.971 | 0.662 | 0.971 | 0.680 | 0.973 |
| 18 | 0.671 | 0.240 | 0.690 | 0.235 | 0.535 | 0.270 | 0.723 | 0.261 |
| 19 | 0.547 | 0.968 | 0.568 | 0.973 | 0.656 | 0.972 | 0.581 | 0.970 |
| 20 | 0.569 | 0.326 | 0.579 | 0.357 | 0.516 | 0.392 | 0.584 | 0.362 |
| 21 | 0.549 | 0.365 | 0.493 | 0.354 | 0.433 | 0.330 | 0.581 | 0.326 |
| 22 | 0.462 | 0.297 | 0.470 | 0.310 | 0.430 | 0.310 | 0.579 | 0.328 |
| 23 | 0.499 | 0.232 | 0.452 | 0.246 | 0.452 | 0.266 | 0.498 | 0.274 |
| 24 | 0.466 | 0.148 | 0.434 | 0.179 | 0.352 | 0.200 | 0.665 | 0.160 |
| 25 | 0.500 | 0.099 | 0.401 | 0.116 | 0.356 | 0.112 | 0.513 | 0.145 |
| 26 | 0.412 | 0.042 | 0.356 | 0.038 | 0.298 | 0.036 | 0.385 | 0.038 |
| all | 0.731 | 0.580 | 0.732 | 0.588 | 0.685 | 0.593 | 0.766 | 0.589 |

TS is transpose then substitute, ST substitute then transpose. On K4 the bound excluded these fractions: a 0.740 and 0.563 (n = 97), 0.737 and 0.575 (n = 98); b 0.714 and 0.575, 0.713 and 0.572; c 0.661 and 0.574, 0.662 and 0.571; d 0.745 and 0.576, 0.740 and 0.575. Those are close to the wrong-hypothesis rates. The K4 survivor counts are about what chance gives and point to no particular transposition.

### Shuffled K4 as a null

The full enumeration was rerun on three shuffles of K4's own letters (same letter counts, no clue structure; seed 97). Ranges over the three, against K4:

| Family, n | Bijection survivors TS (null / K4) | Bijection survivors ST (null / K4) | Complete-key survivors (null / K4) | Best complete-key score (null / K4) |
| --- | --- | --- | --- | --- |
| a, 97 | 49,919,123 to 53,753,797 / 54,662,749 | 87,154,144 to 93,583,354 / 91,844,319 | 1,563 to 2,976 / 2,338 | -5.640 to -5.477 / -5.388 |
| a, 98 | 51,226,455 to 54,460,647 / 55,336,259 | 88,612,487 to 91,135,123 / 89,233,574 | 1,778 to 3,030 / 2,518 | -5.603 to -5.307 / -5.306 |
| b, 97 | 1,011,996 to 1,038,799 / 1,076,375 | 1,591,414 to 1,608,623 / 1,601,121 | 332 to 505 / 342 | -5.474 to -5.411 / -5.145 |
| b, 98 | 993,333 to 1,025,122 / 1,049,880 | 1,553,423 to 1,574,772 / 1,564,156 | 280 to 425 / 477 | -5.376 to -5.321 / -5.233 |
| c, 97 | 58,977 to 63,255 / 61,689 | 76,034 to 81,800 / 77,518 | 69 to 79 / 65 | -5.485 to -5.254 / -5.723 |
| c, 98 | 59,265 to 63,867 / 61,928 | 77,147 to 82,939 / 78,708 | 85 to 106 / 90 | -5.646 to -5.413 / -5.688 |
| d, 97 | 510 to 522 / 531 | 879 to 909 / 883 | 0 / 0 | none / none |
| d, 98 | 487 to 514 / 540 | 838 to 880 / 884 | 0 / 0 | none / none |

On the nulls too, every strong survivor is at period 21 or above. For transpose then substitute, K4 has slightly more bijection survivors than each of the three shuffles in families a and b (2 to 4 percent above the highest shuffle); three shuffles cannot say whether that exceeds the spread, and it singles out no transposition. K4's best rotation scores sit a little above the three null maxima, but each such fit tests 0 or 1 clue letters and the texts read as random letters; three nulls do not make a significance test, and nothing is claimed.

## Per-period bijection survivors on K4

Survivors / hypotheses at each period. TS is transpose then substitute, ST substitute then transpose.

n = 97:

| p | a TS | a ST | b TS | b ST | c TS | c ST | d TS | d ST |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0/8,075,824 | 0/8,075,824 | 0/144,846 | 0/144,846 | 0/6,994 | 0/6,994 | 0/80 | 0/80 |
| 2 | 0/8,075,824 | 0/8,075,824 | 0/144,846 | 0/144,846 | 0/6,994 | 0/6,994 | 0/80 | 0/80 |
| 3 | 2,101/8,075,824 | 0/8,075,824 | 45/144,846 | 0/144,846 | 16/6,994 | 0/6,994 | 0/80 | 0/80 |
| 4 | 15,534/8,075,824 | 935/8,075,824 | 343/144,846 | 24/144,846 | 23/6,994 | 0/6,994 | 0/80 | 0/80 |
| 5 | 17,271/8,075,824 | 10,643/8,075,824 | 1,023/144,846 | 32/144,846 | 37/6,994 | 0/6,994 | 1/80 | 0/80 |
| 6 | 136,101/8,075,824 | 1,976,847/8,075,824 | 3,735/144,846 | 35,017/144,846 | 496/6,994 | 1,734/6,994 | 1/80 | 21/80 |
| 7 | 467,120/8,075,824 | 2,754,455/8,075,824 | 9,401/144,846 | 43,378/144,846 | 501/6,994 | 1,608/6,994 | 4/80 | 23/80 |
| 8 | 540,930/8,075,824 | 3,377,847/8,075,824 | 13,469/144,846 | 52,800/144,846 | 1,586/6,994 | 2,572/6,994 | 5/80 | 30/80 |
| 9 | 1,153,170/8,075,824 | 0/8,075,824 | 12,671/144,846 | 0/144,846 | 607/6,994 | 0/6,994 | 12/80 | 0/80 |
| 10 | 315,119/8,075,824 | 4,448,160/8,075,824 | 15,039/144,846 | 71,250/144,846 | 1,345/6,994 | 3,158/6,994 | 6/80 | 41/80 |
| 11 | 1,591,855/8,075,824 | 4,588,145/8,075,824 | 28,385/144,846 | 83,695/144,846 | 1,928/6,994 | 4,026/6,994 | 9/80 | 50/80 |
| 12 | 2,694,606/8,075,824 | 5,317,628/8,075,824 | 33,900/144,846 | 91,428/144,846 | 3,584/6,994 | 5,007/6,994 | 13/80 | 50/80 |
| 13 | 2,447,357/8,075,824 | 5,239,587/8,075,824 | 54,312/144,846 | 98,820/144,846 | 3,470/6,994 | 5,113/6,994 | 29/80 | 46/80 |
| 14 | 2,337,761/8,075,824 | 5,365,382/8,075,824 | 50,559/144,846 | 95,117/144,846 | 2,672/6,994 | 4,187/6,994 | 24/80 | 47/80 |
| 15 | 708,915/8,075,824 | 214,302/8,075,824 | 44,186/144,846 | 3,560/144,846 | 2,061/6,994 | 186/6,994 | 23/80 | 1/80 |
| 16 | 2,964,758/8,075,824 | 6,089,539/8,075,824 | 53,020/144,846 | 107,763/144,846 | 3,807/6,994 | 5,510/6,994 | 22/80 | 60/80 |
| 17 | 3,172,097/8,075,824 | 190,968/8,075,824 | 55,340/144,846 | 4,265/144,846 | 2,418/6,994 | 251/6,994 | 31/80 | 4/80 |
| 18 | 3,970,692/8,075,824 | 6,620,383/8,075,824 | 54,739/144,846 | 114,252/144,846 | 4,373/6,994 | 5,935/6,994 | 28/80 | 65/80 |
| 19 | 3,030,080/8,075,824 | 208,349/8,075,824 | 69,233/144,846 | 4,495/144,846 | 2,528/6,994 | 254/6,994 | 44/80 | 0/80 |
| 20 | 1,522,868/8,075,824 | 5,857,807/8,075,824 | 67,383/144,846 | 96,410/144,846 | 3,816/6,994 | 4,323/6,994 | 27/80 | 63/80 |
| 21 | 4,170,507/8,075,824 | 5,365,382/8,075,824 | 71,506/144,846 | 95,117/144,846 | 2,916/6,994 | 4,187/6,994 | 38/80 | 47/80 |
| 22 | 4,658,788/8,075,824 | 5,717,297/8,075,824 | 82,243/144,846 | 104,143/144,846 | 4,344/6,994 | 5,025/6,994 | 43/80 | 57/80 |
| 23 | 5,306,142/8,075,824 | 6,323,708/8,075,824 | 88,766/144,846 | 111,434/144,846 | 4,524/6,994 | 5,607/6,994 | 49/80 | 64/80 |
| 24 | 4,119,202/8,075,824 | 6,725,209/8,075,824 | 88,122/144,846 | 119,956/144,846 | 5,282/6,994 | 6,048/6,994 | 23/80 | 65/80 |
| 25 | 3,949,445/8,075,824 | 7,650,301/8,075,824 | 75,335/144,846 | 128,456/144,846 | 4,090/6,994 | 6,016/6,994 | 37/80 | 71/80 |
| 26 | 5,370,330/8,075,824 | 7,801,445/8,075,824 | 103,620/144,846 | 139,709/144,846 | 5,265/6,994 | 6,771/6,994 | 62/80 | 78/80 |

n = 98:

| p | a TS | a ST | b TS | b ST | c TS | c ST | d TS | d ST |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0/8,075,824 | 0/8,075,824 | 0/140,566 | 0/140,566 | 0/7,052 | 0/7,052 | 0/80 | 0/80 |
| 2 | 0/8,075,824 | 0/8,075,824 | 0/140,566 | 0/140,566 | 0/7,052 | 0/7,052 | 0/80 | 0/80 |
| 3 | 473/8,075,824 | 0/8,075,824 | 24/140,566 | 0/140,566 | 14/7,052 | 0/7,052 | 0/80 | 0/80 |
| 4 | 23,669/8,075,824 | 384/8,075,824 | 316/140,566 | 11/140,566 | 23/7,052 | 0/7,052 | 0/80 | 0/80 |
| 5 | 16,034/8,075,824 | 13,770/8,075,824 | 794/140,566 | 39/140,566 | 32/7,052 | 0/7,052 | 1/80 | 0/80 |
| 6 | 121,384/8,075,824 | 2,143,740/8,075,824 | 3,197/140,566 | 36,315/140,566 | 544/7,052 | 1,720/7,052 | 3/80 | 26/80 |
| 7 | 493,006/8,075,824 | 2,772,365/8,075,824 | 8,853/140,566 | 42,393/140,566 | 495/7,052 | 1,664/7,052 | 6/80 | 27/80 |
| 8 | 817,115/8,075,824 | 2,319,042/8,075,824 | 12,579/140,566 | 52,487/140,566 | 1,496/7,052 | 2,564/7,052 | 3/80 | 25/80 |
| 9 | 1,099,456/8,075,824 | 21/8,075,824 | 11,974/140,566 | 0/140,566 | 573/7,052 | 0/7,052 | 13/80 | 0/80 |
| 10 | 298,279/8,075,824 | 3,313,373/8,075,824 | 14,562/140,566 | 70,158/140,566 | 1,294/7,052 | 3,212/7,052 | 12/80 | 41/80 |
| 11 | 1,298,781/8,075,824 | 4,536,140/8,075,824 | 29,647/140,566 | 81,222/140,566 | 1,915/7,052 | 4,129/7,052 | 7/80 | 45/80 |
| 12 | 2,802,615/8,075,824 | 5,251,462/8,075,824 | 33,255/140,566 | 88,867/140,566 | 3,538/7,052 | 5,066/7,052 | 12/80 | 47/80 |
| 13 | 2,510,475/8,075,824 | 5,452,595/8,075,824 | 51,490/140,566 | 95,204/140,566 | 3,558/7,052 | 5,207/7,052 | 24/80 | 54/80 |
| 14 | 2,375,575/8,075,824 | 5,807,142/8,075,824 | 50,424/140,566 | 93,482/140,566 | 2,562/7,052 | 4,298/7,052 | 36/80 | 58/80 |
| 15 | 543,585/8,075,824 | 256,354/8,075,824 | 41,028/140,566 | 3,727/140,566 | 2,007/7,052 | 192/7,052 | 20/80 | 3/80 |
| 16 | 2,938,226/8,075,824 | 5,776,407/8,075,824 | 49,460/140,566 | 104,356/140,566 | 3,773/7,052 | 5,580/7,052 | 21/80 | 61/80 |
| 17 | 3,420,890/8,075,824 | 279,587/8,075,824 | 57,478/140,566 | 4,492/140,566 | 2,428/7,052 | 262/7,052 | 34/80 | 0/80 |
| 18 | 3,914,326/8,075,824 | 6,637,919/8,075,824 | 51,521/140,566 | 110,264/140,566 | 4,342/7,052 | 5,960/7,052 | 34/80 | 57/80 |
| 19 | 3,393,971/8,075,824 | 170,843/8,075,824 | 67,350/140,566 | 4,475/140,566 | 2,541/7,052 | 256/7,052 | 40/80 | 5/80 |
| 20 | 1,852,104/8,075,824 | 4,300,922/8,075,824 | 66,570/140,566 | 94,689/140,566 | 3,732/7,052 | 4,404/7,052 | 36/80 | 51/80 |
| 21 | 3,933,425/8,075,824 | 5,807,142/8,075,824 | 69,624/140,566 | 93,482/140,566 | 3,163/7,052 | 4,298/7,052 | 34/80 | 58/80 |
| 22 | 4,955,264/8,075,824 | 6,110,744/8,075,824 | 82,534/140,566 | 101,426/140,566 | 4,352/7,052 | 5,146/7,052 | 36/80 | 51/80 |
| 23 | 5,230,851/8,075,824 | 6,271,057/8,075,824 | 87,427/140,566 | 109,282/140,566 | 4,613/7,052 | 5,688/7,052 | 52/80 | 62/80 |
| 24 | 4,530,028/8,075,824 | 6,666,434/8,075,824 | 85,119/140,566 | 116,641/140,566 | 5,271/7,052 | 6,146/7,052 | 22/80 | 65/80 |
| 25 | 3,207,500/8,075,824 | 7,579,850/8,075,824 | 75,911/140,566 | 125,358/140,566 | 4,208/7,052 | 6,067/7,052 | 36/80 | 76/80 |
| 26 | 5,559,227/8,075,824 | 7,766,281/8,075,824 | 98,743/140,566 | 135,786/140,566 | 5,454/7,052 | 6,849/7,052 | 58/80 | 72/80 |

## What this run says

- Within these four families, any composition with an arbitrary per-column substitution of period 1 or 2 is excluded by the clues alone, in both orders and both lengths.
- Within these families, straight Vigenere or Beaufort on A-Z or on the KRYPTOS alphabet is excluded at every period from 1 to 20, both orders, both lengths. At 21 to 26 the clues test too few letters to decide.
- The bijection bound leaves many survivors from period 3 or 4 upward. Their numbers match the rate at which the bound excludes wrong hypotheses on planted texts and on shuffled K4, so they carry no signal for any particular transposition.

## Not covered

- Columnar widths 11 and up with arbitrary orders (11! = 39,916,800 orders; at the measured rate of about 0.16 million orders per second on 2 threads, each order with both directions, both compositions and 26 periods, roughly 4 to 5 minutes per length for width 11 and about 50 minutes per length for width 12). Keyed orders from the keyword list are covered at any width.
- Columnar variants with a short last row placed elsewhere, nulls or padding letters, and double columnar with two arbitrary orders (only the double rotation of family b, which is two fixed-order steps, is covered).
- Routes on shapes other than rectangles with a short last row, and routes not in the listed set (for example knight's moves or arbitrary grilles).
- Rotation pairs other than two single quarter turns (half turns or three steps).
- Periods above 26, non-periodic substitution (autokey, running key, progressive keys), substitution families between "any alphabet" and the four strong variants (for example Quagmire I to IV with unknown keywords, which only the bijection bound covers), and any third layer.
- A "?" anywhere other than in front of K4, and clue positions other than the published ones.

## Reproduce

- Full run, controls, power and three shuffled nulls: `python3 -m engine.k4_transposition_sub 10 3` (3 min 40 s wall on 2 threads; the K4 part alone is 57 s, of which family a is 25 to 26 s per length and families b to d about 1.5 s per length).
- Tests: `python3 -m unittest tests.test_k4_transposition_sub -v` (9 tests, about 4 s).

Not solved. No plaintext claimed.
