# Four-square on the cells, 6 October 2026


In four-square, the first symbol of each cipher pair comes from one square and the second from another. Which cell is hit depends only on the plaintext letters' rows and columns in the plain squares, so the number of different symbols on each side is fixed before any cipher key is chosen.

The printed cells use 13 symbols on one side and 18 on the other, at either pair phase. Held-out Austen, Doyle and Wells, cut into 196-letter windows (370 windows) with standard plain squares, never have fewer than 21 symbols on the larger side. With both plain squares keyed at random (7,400 draws, 20 a window), the larger side never drops below 20, and 0 draws reach 13 and 18 together. The cipher squares cannot change these counts. A scratch run with 50 draws a window (18,500 draws) found a floor of 19 and also 0 draws reaching the cells; the frozen numbers are the 20-a-window run. Horizontal two-square is a four-square whose plain and cipher squares coincide, so it is inside the keyed draws. Four-square and two-square on ordinary English prose do not produce the printed cells. The regrouped cells (`01432`) use 21 and 19, which this count does not exclude.

`engine/dagapeyeff_foursquare.c` is a compiled annealing kernel for the two cipher squares, under the default model with J folded into I. `engine.dagapeyeff_foursquare.foursquare_report` runs it with 10 restarts of 1,000,000 steps at temperature 8.

| Run | Result |
| --- | --- |
| 6 planted held-out texts, 196 letters, both cipher squares random | 4 recovered (98 to 100 percent of letters); 1 at 76 percent; 1 failed at 18 percent |
| Printed cells, pairs from the first symbol | -3.5591 a letter; 15 of 20 shuffles as high |
| Printed cells, pairs from the second symbol | -3.5543 a letter; 19 of 20 shuffles as high |
| Regrouping, pairs from the first symbol | -3.3427 a letter; 9 of 20 shuffles as high |
| Regrouping, pairs from the second symbol | -3.4407 a letter; 15 of 20 shuffles as high |

Planted English scores -1.76 to -2.02 a letter. The cells and the regrouping score more than 1.3 a letter below the weakest planted text and sit inside their own shuffles. A scratch run before this one recovered 4 of 4; the frozen run recovers 4 of 6, so the search finds a planted key about two times in three at this budget. Gariazzo reached 83 percent key recovery.

[The pair-count note](dagapeyeff-pairmap-2026-10-06.md) adds that any one-to-one pair cipher of ordinary English is very unlikely to give the regrouping, which agrees with this search.

Not a reading. No letter string is stored.

## Correction, 6 October 2026

The side count is fixed by the plaintext and the two plain squares; only the cipher squares drop out. It is key-free only when the plain squares are the standard alphabet. The 7,400 keyed draws above used plain squares drawn at random, which is a statement about random keys, not about every key. `engine.dagapeyeff_fskeyed` climbs the plain squares toward the cells' side counts instead, and with chosen squares 15 of 15 held-out windows reach 13 and 18 exactly ([finding](../../papers/dagapeyeff-exclusions/notes/review-1.md)). The search above also used standard plain squares only. So four-square with standard plain squares is closed; four-square with keyed plain squares, and two-square, whose squares are all keyed, are neither excluded by the count nor searched.

Not a reading. No letter string is stored.

