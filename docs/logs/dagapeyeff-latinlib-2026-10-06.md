# Every window of a larger Latin library, 6 October 2026

Not a reading. No letter string is stored.

Latin fits the cells' letter counts best of the languages screened ([screen](dagapeyeff-screen-2026-10-06.md)), with one Thomistic window needing 4 errors. Pelling proposed in 2021 matching sorted letter counts against a large library ([Cipher Mysteries, 1 May 2021](https://ciphermysteries.com/2021/05/01/dagapeyeff-cipher-how-about-a-sorted-frequency-distribution-search-of-project-gutenberg)). Under a one-to-one letter key and any transposition, a window whose sorted counts equal the cells' would be a possible source text. A window needing 0, 1 or 2 errors would be a concrete lead.

`engine.dagapeyeff_latinlib` takes every window, one letter apart, of six Universal Dependencies Latin treebanks (ITTB, Perseus, PROIEL with the Vulgate and Caesar, UDante, LLCT charters, CIRCSE) and fifteen Latin books from Project Gutenberg (Virgil, Cicero, Augustine, Descartes, Caesar, Plautus, Newton's Principia, Vitruvius, Sallust, Apicius, Boethius). Several Gutenberg editions carry English notes or facing translations, so only paragraphs led by Latin function words are kept. That is 8,944,241 letters and 8,940,146 windows.

| Source | Letters | Fewest errors | Median | Within 4 | Within 8 |
| --- | --- | --- | --- | --- | --- |
| Thomas Aquinas (ITTB) | 2,204,065 | 4 | 22 | 7 | 2,584 |
| Newton, Principia (Gutenberg 28233) | 611,782 | 4 | 22 | 1 | 899 |
| PROIEL (Vulgate, Caesar, Cicero) | 1,102,590 | 5 | 25 | 0 | 211 |
| Augustine, Confessiones (33849) | 675,578 | 5 | 24 | 0 | 189 |
| Vitruvius (51812) | 833,673 | 5 | 23 | 0 | 251 |
| Apicius (16439) | 133,705 | 5 | 24 | 0 | 67 |
| Classical poetry and prose (Perseus, Virgil, Cicero, Sallust, Caesar, Plautus) | | 6 to 10 | 22 to 25 | 0 | |
| All 21 sources | 8,944,241 | 4 | | 8 | |

No window comes within 2 errors. The closest needs 4, in Aquinas (two windows) and in Newton. Scholastic and technical Latin, with its flat spread of common letters, fits better than classical Latin.

So no Latin text here can be the source under a one-to-one key and a transposition unless at least 4 cells are wrong. The book's own exercise has about that many slips, so this does not exclude Latin; it rules out a clean Latin source in this library, and it leaves Latin with a few errors under an order-destroying system as the case to search. The source and offset of the twelve closest windows are in the frozen file; the letters are not.

Not a reading. No letter string is stored.
