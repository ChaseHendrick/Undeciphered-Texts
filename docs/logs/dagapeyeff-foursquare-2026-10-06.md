# Four-square on the cells, 6 October 2026

Not a reading. No letter string is stored.

In four-square, the first symbol of each cipher pair comes from one square and the second from another. Which cell is hit depends only on the plaintext letters' rows and columns in the plain squares, so the number of different symbols on each side is fixed before any cipher key is chosen.

The printed cells use 13 symbols on one side and 18 on the other, at either pair phase. Held-out Austen, Doyle and Wells, cut into 196-letter windows (370 windows) with standard plain squares, never have fewer than 21 symbols on the larger side. With all four squares keyed at random (18,500 draws, 50 a window), the larger side never drops below 19, and 0 draws reach 13 and 18 together. Horizontal two-square is a four-square whose plain and cipher squares coincide, so it is inside the keyed draws. Four-square and two-square on ordinary English prose do not produce the printed cells. The regrouped cells (`01432`) use 21 and 19, which this count does not exclude.

`engine/dagapeyeff_foursquare.c` is a compiled annealing kernel for the two cipher squares, under the default model with J folded into I. In a scratch run, 10 restarts of 1,000,000 steps at temperature 8 recovered 4 of 4 planted held-out texts of 196 letters (99 to 100 percent of letters), about 6 seconds a text. Temperature 4 recovered 0 of 4 and temperature 15 recovered 2 of 4. Gariazzo reached 83 percent key recovery.

`engine.dagapeyeff_foursquare.foursquare_report` runs that search on 6 planted texts, then on the cells and the regrouping at both phases, with 20 shuffles each. It was started and not finished in this session, so no frozen result exists yet. Running it takes about ten minutes and writes `engine/data/swarm_cache/dagapeyeff-foursquare.json`; the cache count in `tests/test_dagapeyeff_checks.py`, the board page and the provenance chain then need regenerating.

Not a reading. No letter string is stored.
