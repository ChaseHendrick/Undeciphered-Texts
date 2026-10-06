# Every double transposition up to width 6, any language, 5 October 2026

Double transposition is the book's own method, copied from Kerckhoffs, and Pelling (Cipher Mysteries, 5 March 2017) suspected the challenge used it. Gariazzo's method D searched it with simulated annealing at free widths, but recovery of planted keys was not reported for it. Two columnar passes with different keys move single cells, not whole columns.

`engine.dagapeyeff_double` tries every pair of orders at widths 2 to 6 for each pass, both passes undone and both passes done (the book's reversed direction), with a short last row allowed. That is 25 width pairs in each direction, up to 518,400 order pairs each. The score is successive-symbol information, which no letter key can change, so the plaintext language does not matter. Each text is compared with the best pair of orders on shuffles of its own symbols.

Planted English and German, each with a random letter key and random orders, beat their shuffles by 0.037 to 0.3085. The margin is smallest at widths 6 and 6 undone, where power is thinnest. The cells' margins run from -0.1266 to 0.0378. In all 50 cases the cells beat their shuffles by less than either planted text beats its own.

Double columnar transposition with any two keys up to width 6, in either direction, followed by any one-to-one substitution in any language, does not read the cells. The keyword pass covered the same method with one key used twice at any width, for listed words.

Not a reading. No letter string is stored.
