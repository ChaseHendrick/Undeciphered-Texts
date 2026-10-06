# Periodic independent alphabets, 6 October 2026

Not a reading. No letter string is stored.

A periodic substitution with independent alphabets enciphers the letters at places i, i+p, i+2p and so on with one one-to-one key, and each of the p phases with its own key. The repeating shift ([additive](dagapeyeff-additive-2026-10-06.md)) is the special case in which the alphabets are shifts of one square. Each phase is then a one-to-one key on its own letters, so the error count of the [errors note](dagapeyeff-errors-2026-10-06.md) applies phase by phase: the fewest errors that turn a text into the cells, under any such keys, is the sum over the phases of half the distance between the sorted counts of the text's phase and the cells' phase. No key is searched.

`engine.dagapeyeff_phases` computes it for 1,558 windows of 196 letters of held-out Austen, Doyle and Wells at periods 2, 3, 4, 5, 6, 7 and 14. No window comes within 8 errors at any period; the fewest is 13 to 15 and the median 23 to 26. Five shuffles of the cells, used as targets instead of the cells, are reached with 9 to 18 errors, so the distance comes from the cells' overall letter counts (18 symbols, 13 of them nearly equal), not from their order.

Periodic independent alphabets over ordinary English, without a transposition before them and with errors at the book's rate, do not give the cells.

Not a reading. No letter string is stored.
