# Latin under a one-to-one key, 6 October 2026

Not a reading. No letter string is stored.

The [language screen](dagapeyeff-screen-2026-10-06.md) found Latin the closest of 39 languages to the cells' letter counts. `engine.dagapeyeff_latin` searches it. A quadgram model is fit on the first 90 percent of the Index Thomisticus treebank (UD_Latin-ITTB, 1,983,658 letters). The texts are fetched into the ignored `work/` folder; only scores are stored.

**Power.** Planted Latin under random keyed squares, solved by the keyed-square search (2 restarts of 400,000 steps): the held-out tail of the Thomistic text comes back 3 of 3 with every letter right, and 3 of 3 with 8 digit slips (95 to 96 percent of letters right). Classical Latin from UD_Latin-Perseus, a different style the model never saw, scores only -2.96 to -3.30 a letter under the Thomistic model, yet comes back 3 of 3 (97 to 98 percent) and 3 of 3 with 8 slips (91 to 94 percent).

**The cells.** The plain keyed square scores -4.5513 a letter, and 5 of 8 shuffles score as high. With the book's dummy rule (every phase of every 3rd, 4th or 5th cell dropped) the best of 13 variants is -3.9424 (dropping every third cell from place 1), and 7 of 8 shuffles of all the cells reach a best at least as high (-3.6429 to -3.975). The regrouping: -4.9211 for the square (4 of 8 as high) and -4.3179 at best (6 of 8).

**Counts with random slips.** Windows of either Latin text with 4, 8 or 16 random digit slips (1,856 draws for each count) never reach the cells' counts; at least 7 further errors are always needed.

Latin under a one-to-one key, with or without the book's dummy rule and errors at the book's rate, does not read the cells. Latin under a large transposition, such as the 14-column key closed here only for English, has not been searched.

Not a reading. No letter string is stored.
