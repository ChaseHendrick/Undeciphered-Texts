# Esperanto against the cells' letter counts, 6 October 2026

Not a reading. No letter string is stored.

Esperanto has been proposed for the challenge (Tim Marland's project, 2026; see [prior work](dagapeyeff-prior-work-2026-10-05.md)). Universal Dependencies has no Esperanto treebank, so the [language screen](dagapeyeff-screen-2026-10-06.md) left it out. Like Latin it has no Q, W, X or Y, which is one reason Latin fits the cells' counts.

`engine.dagapeyeff_esperanto` takes ten Esperanto books from Project Gutenberg (ebooks 17482, 20006, 21195, 23093, 23670, 24145, 24763, 26359, 31348 and 45612), 948,257 letters after folding, fetched into the ignored `work/` folder. Books in the x-system (cx for the hatted c) are turned back into hatted letters, the hats are removed and J is folded into I, as in the book's square. The count is the screen's: the fewest single-cell errors that turn a 196-letter window into the cells' counts, under any one-to-one key and any order.

| Text | Fewest errors | Median | Windows within 8 |
| --- | --- | --- | --- |
| Esperanto (10 books) | 9 | 28 | 0 |
| Latin (ITTB) | 4 | 22 | 294 |
| English (prose corpus) | 8 | 28 | |

Esperanto uses few letters (26,441 of 237,016 windows use 18 letters or fewer, as the cells do) but spreads them unevenly, so it is no closer than English. Under a one-to-one key it is not a lead. Latin stays the outlier.

Not a reading. No letter string is stored.
