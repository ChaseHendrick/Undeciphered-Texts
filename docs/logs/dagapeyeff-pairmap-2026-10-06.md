# Different pairs under any one-to-one pair cipher, 6 October 2026

Not a reading. No letter string is stored.

A cipher that sends each plaintext pair to one cipher pair, the same way every time, cannot change how many different pairs a text uses. That holds for four-square, two-square, Playfair after its padding, a 2 by 2 Hill matrix, and any keyed table of 625 pairs, whatever the key. `engine.dagapeyeff_pairmap` checks the count in code: four-square with all four squares drawn at random left it unchanged on 201 of 201 held-out windows.

`engine.dagapeyeff_pairmap` counts every fourth 196-letter window of the 1,916,398-letter public training file, 479,051 windows, with J folded into I. Pairs are taken from the first letter (98 pairs) and from the second (97 pairs, first and last letters left over).

| Text | Phase | Different pairs | Windows with as many |
| --- | --- | --- | --- |
| Printed cells | from the first | 79 | 29,336 (6.1 percent) |
| Printed cells | from the second | 80 | 11,539 (2.4 percent) |
| Regrouping `01432` | from the first | 85 | 325 (0.07 percent) |
| Regrouping `01432` | from the second | 85 | 161 (0.03 percent) |

The printed cells have an ordinary count once both phases are kept, so this does not exclude a one-to-one pair cipher on them. The four-square count in [the four-square note](dagapeyeff-foursquare-2026-10-06.md) is the narrower test that does exclude four-square there.

The regrouping uses 85 different pairs at either phase, which at most 1 prose window in about 1,500 reaches. A one-to-one pair cipher of ordinary English prose is very unlikely to give the regrouping. The windows overlap, so they are not 479,051 independent passages.

A code that gives each plaintext letter one fixed pair of cells could show at most 25 different pairs. The cells show 79 and 80, so such a code is excluded without a corpus. A cipher that changes its pairing as it goes, a homophonic pair code, or one with nulls mixed in is not covered by this count.

Not a reading. No letter string is stored.
