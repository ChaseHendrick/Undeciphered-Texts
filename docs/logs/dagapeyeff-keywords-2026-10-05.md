# A keyword dictionary attack on the book's transpositions, 5 October 2026

The book's double transposition, copied from Kerckhoffs, turns a keyword into a column order by alphabetical rank and was printed in the decryption direction (Pelling, Cipher Mysteries, 5 March 2017). If the challenge used a keyword transposition, its order comes from a word, and words can be listed.

`engine.dagapeyeff_keywords` takes every word of 5 to 20 letters in the repository's 40,000-word list, every 14-letter pair of words from its 2,000 most common words, and 24 names from the book and its sources (SCHUVALOW and its misprints, KERCKHOFFS, NIHILIST, DAGAPEYEFF and others). That is 379,521 keywords. Each is applied to the cells in up to six ways: single columnar undone and done, double columnar with the same key undone twice and done twice, and, for 14 letters, the same key on the rows and columns of the 14 by 14 square, both ways. Doing where undoing was meant covers the book's reversed direction. That is 2,208,702 orders. The columnar readings use the repository's own `columnar_encrypt` and `columnar_decrypt`.

The screen is successive-symbol information, which no letter key can change. Six planted texts, training prose with a random letter key under a random keyword and variant, all surfaced with a top score of 0.9661 or more; four had their exact order on top, and in the other two a different order scored slightly higher. The cells' best is 0.8161. The best orders of two shuffled copies of the cells score 0.829 and 0.8107. The three best orders on the cells, run through the default substitution solver, score -3.8112 to -4.1244 a letter, against about -2 for English. Their order gate reads true only because these readings were chosen for that score.

No keyword in these lists orders the cells into a readable text under these methods.

Not a reading. No letter string is stored.
