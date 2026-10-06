# A repeating shift on a keyed square, 6 October 2026

Not a reading. No letter string is stored.

The classical step after a plain Polybius square is to add a short repeating key to the coordinates, row and column each modulo 5. `engine.dagapeyeff_add` and its period-4 sequel searched periods 2 to 4 on the book's own letter order under the old 8,689-letter model, with no planted text. `engine.dagapeyeff_additive` leaves the square unknown and anneals it together with the shifts (`engine/dagapeyeff_additive.c`), at periods 2, 3, 4, 5, 7 and 14, under the default model with J folded into I.

**The count.** A repeating shift spreads each letter over several cells. Held-out Austen, Doyle and Wells in 196-letter windows, under random squares and random shift keys, 915 draws for each of 18 cases (periods 2 to 14, shifting both coordinates, the column only or the row only), 16,470 draws in all, never use fewer than 20 different symbols. The cells use 18, with 177 of 196 in the three busiest rows of the square. No draw reaches both. This assumes a key drawn at random; a key that repeats one shift is a plain square, which the [corpus count](dagapeyeff-corpus-2026-10-05.md) already covers.

**The search.** Four restarts of 4,000,000 steps a case. Planted held-out English came back 11 of 12 times, every letter right in 10 of them; the one miss, a column shift of period 7, ended with 84 percent of letters right, a search failure. The weakest planted text scores -2.0789 a letter. On the cells and the regrouping, in 24 cases (2 directions of shift, 6 periods, 2 texts) with 3 shuffles each, the best is -3.3261 a letter (the regrouping, both coordinates, period 14). Period 14 gives the key the most freedom, and the shuffles there score -3.3953 to -3.5185; with three shuffles a case that comparison is weak. The gap to English, 1.25 a letter, is the result.

A repeating coordinate shift of period 2 to 14 on a keyed square does not read the cells.

Not a reading. No letter string is stored.
