# Every window of The Latin Library, 6 October 2026

Not a reading. No letter string is stored.

The [larger Latin library](dagapeyeff-latinlib-2026-10-06.md) of 8.9 million letters had no window within 2 errors of the cells' letter counts; its closest needed 4. [The Latin Library](https://www.thelatinlibrary.com/) holds classical, Christian, medieval and neo-Latin texts, far more than that. Under a one-to-one letter key and any transposition, a window whose sorted letter counts equal the cells' would be a possible source text.

`engine.dagapeyeff_latinlibrary` crawled the site one request at a time, half a second apart, skipping the course and teaching folders that mix in English, and kept only paragraphs led by Latin function words. The crawl was stopped after 1,777 fetched pages so the time could go to searches. The frozen result covers the 1,750 pages reached from the home page among them (their sorted list hashes to `3482d5bb...`); 1,516 have at least 196 letters. That is 50,826,522 letters and 50,530,902 windows, each one letter apart.

| Count | Windows |
| --- | --- |
| Fewest errors | 3 |
| Within 2 errors | 0 |
| Within 4 errors | 91 |
| Within 8 errors | 19,888 |
| Median of the page medians | 23 |

The two closest windows, at 3 errors each, are in Livy, book 42 (`/livy/liv.42.shtml`), and in book 7 of the Theodosian Code (`/theodosius/theod07.shtml`). The next ten, at 4, are in Aelred, the passion of Agnes, the Royal Frankish Annals, Apuleius (three), Augustine's *De Trinitate* (two), the *Bellum Africum* and Cicero's *Brutus*. Only page and letter offset are stored.

Across 59.8 million letters of Latin from the two screens, no window is a clean source: every one needs at least 3 wrong cells. Any transposition can turn a window with the right counts into the cells, so these windows are not candidates on their own; they say that under a one-to-one key a Latin message needs a few enciphering errors, as the book's own exercise has, and that the remaining Latin case is an order-destroying system with a few errors. The [width-14](dagapeyeff-latin14-2026-10-06.md) and other Latin searches with shown power cover the ordered systems.

Not a reading. No letter string is stored.
