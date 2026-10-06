# Enciphering errors cannot hide English under a one-to-one key, 6 October 2026

Not a reading. No letter string is stored.

D'Agapeyeff's own worked exercise has about four faults in 92 letters: 89 pairs for 92 letters, and AREA written as ARYA ([prior work](dagapeyeff-prior-work-2026-10-05.md)). At that rate the 196-cell challenge might carry about eight. `engine.dagapeyeff_errors` asks whether errors at that rate could hide English enciphered with a one-to-one letter key, with or without a transposition, which keeps the letter counts.

**Counts, best case.** Each error moves one count from one symbol to another, so the fewest errors that turn a text's counts into the cells' counts, under any relabeling, is half the distance between the two sorted count vectors. Over 5,116 windows of 196 letters of held-out Austen, Doyle and Wells, the fewest is 15 and the median 29. None needs 8 or fewer. The closest of the 479,051 windows of the 1.9-million-letter corpus is at distance 16 ([corpus](dagapeyeff-corpus-2026-10-05.md)), so 8 errors, every one of them chosen to move the counts toward the cells.

**Counts, random errors.** A digit slip changes the row digit or the column digit of a pair, which moves the letter to one of the eight cells sharing its row or column of the square. A free error moves it to any other cell. With 4 to 48 errors of either kind, 20,464 draws for each of 14 cases (286,496 in all), no draw reaches the cells' counts, the fewest errors still needed afterwards is never below 13, and the median rises from 29 to 37. Random errors move English away from the cells, not toward them.

**Search.** Planted held-out English under a random keyed square with k digit slips, 3 texts for each k, solved by the keyed-square search (2 restarts of 300,000 steps). With no errors it scores -1.78 to -2.12 a letter. With 4 errors -2.09 to -2.29, 97 percent of letters right or more. With 8 errors -2.29 to -2.49, 95 percent or more. With 16 errors -2.99 to -3.08. The cells, solved the same way, score -3.9003. Planted English falls to that level only at 48 errors, a quarter of the cells, where 25 percent of its letters are right.

Errors at the book's rate cannot turn ordinary English under a one-to-one key into the cells, and could not stop the searches from finding it. This does not cover errors combined with a family that is still open, such as a turning grille or another language.

Not a reading. No letter string is stored.
