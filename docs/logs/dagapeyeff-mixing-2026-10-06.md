# Ciphers that mix letters, 6 October 2026

Not a reading. No letter string is stored.

The cells use 18 of the 25 symbols, 13 of them nearly equally. A cipher whose output symbol depends on more than one plaintext letter, or on a key that changes along the text, spreads ordinary text over more symbols than that. `engine.dagapeyeff_mixing` enciphers 370 windows of 196 letters of held-out Austen, Doyle and Wells under random keys, three draws each (1,110 a case), and counts the different symbols.

| Family | Fewest symbols | Draws with 18 or fewer |
| --- | --- | --- |
| 2 by 2 Hill over a keyed square | 23 | 0 |
| Autokey on the square (previous plaintext letter's coordinates added) | 23 | 0 |
| Bifid, periods 2, 3, 4, 5, 7, 14 and the whole text | 22 to 23 | 0 |
| Vigenere modulo 25 on a keyed alphabet, periods 2 to 14 | 20 to 24 | 0 |
| Running key: another English text's coordinates added | 24 | 0 |

None comes near the cells' 18. Earlier probes of bifid, autokey, running keys and the book's exercise as a key found nothing but showed no power ([bifid](dagapeyeff-bifid-2026-10-04.md), [autokey](dagapeyeff-autokey-2026-10-04.md), [running](dagapeyeff-running-2026-10-04.md), [book key](dagapeyeff-bookkey-2026-10-04.md)); this count excludes them for ordinary English without a search. The statement is for keys drawn at random. A degenerate key, such as a diagonal Hill matrix or a constant shift, is a plain square, which the [corpus count](dagapeyeff-corpus-2026-10-05.md) covers.

Not a reading. No letter string is stored.
