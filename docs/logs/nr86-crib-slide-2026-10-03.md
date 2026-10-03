# Nr. 86 crib slide, 2026-10-03 (EDT)

Not a decipherment. Funkspruch Nr. 86 was not solved. No plaintext is claimed.

Finished 2026-10-03 00:22 EDT. Synced onto `origin/main` at `aa41926` before this commit. The two-square code under test is the same as at `115871b`. This note is the only file added. No quadgram hill climb was run.

## What was tested

Ciphertext, 46 letters, designator included: `FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ`.

Encipherment is the single-stage Truppenschlüssel two-square in `engine.ciphers` (Ostwald and Weierud, https://cryptocellar.org/pubs/mcts.pdf): two 5x5 squares, J omitted, first plaintext letter in the left square, second in the right, rectangle or same-row right neighbour, ciphertext letter from the right square first.

Cribs, J already absent: `FEIND`, `ANGRIFF`, `STELLUNG`, `MELDUNG`, `ABEND`, `MORGEN`. Each crib was tried at every letter offset that fits in 46.

A placement is impossible when a known plaintext letter is the same letter as the ciphertext letter that would have to be a different cell of the same square:

- even offset: plaintext letter equals the second ciphertext letter of that digraph
- odd offset: plaintext letter equals the first ciphertext letter of that digraph

Both the rectangle and the same-row rule need those two to be different cells. If neither single-letter ban fires, every touched digraph is still tried both ways. The assignment is kept only when the row equalities, row inequalities, and mod-5 column steps fit in two squares with no two letters on one cell. Letters outside the crib are reported only when every legal assignment decrypts the same letter there. A crib letter is not evidence: the crib was inserted.

The same checker accepts the true squares of the booklet fragment and of message 64. On the booklet sentence, `FEIND` at offset 0 and `ANGRIFF` at offset 10 together force the true `I` at offset 6 (`FEINDLIQER`) and no false letter. Flipping the mode of the first digraph of that true key is rejected. A one-letter bridge can be real. It is not, by itself, a reading.

## Single cribs

244 placements. 60 fail the one-letter ban. 2 more fail when the digraphs are combined. 182 fit at least one mode assignment. 180 of those force no letter outside the crib. Two force one outside letter, and that letter is not a German word.

| crib | offsets tried | one-letter ban | combined-digraph failure | geometry allows |
| --- | ---: | ---: | ---: | ---: |
| FEIND | 42 | 10 | 0 | 32 |
| ANGRIFF | 40 | 9 | 0 | 31 |
| STELLUNG | 39 | 8 | 1 | 30 |
| MELDUNG | 40 | 11 | 0 | 29 |
| ABEND | 42 | 8 | 0 | 34 |
| MORGEN | 41 | 14 | 1 | 26 |

One-letter bans, offsets only:

- FEIND: 0, 1, 7, 11, 13, 24, 27, 34, 36, 39
- ANGRIFF: 6, 9, 10, 18, 21, 22, 31, 34, 37
- STELLUNG: 4, 5, 10, 12, 22, 26, 31, 33
- MELDUNG: 5, 6, 7, 11, 13, 19, 23, 25, 27, 32, 34
- ABEND: 7, 10, 12, 17, 22, 26, 33, 36
- MORGEN: 2, 5, 7, 8, 10, 11, 19, 22, 23, 24, 25, 31, 32, 40

Combined-digraph failures, both with all 16 mode assignments unsatisfiable:

- `STELLUNG` at 6. Digraphs `ST/MW`, `EL/RL`, `LU/VN`, `NG/RE`. Left-square `L` is both the second ciphertext letter of `EL` and the first plaintext letter of `LU`. Left-square `N` links `LU` to `NG`. Left-square `E` links `EL` to `NG`. A rectangle assignment puts `E` and `N` on the same left-square cell. The other 15 assignments fail the same way.
- `MORGEN` at 9. Digraphs `?/M` over `RL`, `OR/VN`, `GE/RE`, `N/?` over `KE`. No single letter equals its own ciphertext partner. Every combined assignment still collides.

Best single square fragment, rejected: `STELLUNG` at 8 is the only placement with exactly one surviving mode pattern, `SRRR` (same-row, then three rectangles), on digraphs `ST/RL`, `EL/VN`, `LU/RE`, `NG/KE`. It fixes 11 left/right column-offset pairs and 6 same-row pairs. It forces no plaintext letter outside `STELLUNG`. The crib was assumed, so the fragment is not German evidence.

Best single outside letter, rejected: `ANGRIFF` at 24 forces `I` at offset 12, and all 16 of its mode patterns are legal. `MELDUNG` at 21 forces `M` at offset 13 (10 of 16 patterns legal). Each extra letter stands alone. Neither continues the crib. Neither is a word.

## Adjacent pairs

Pairs of non-overlapping cribs that share a square letter and have at most three letters between them: 2,537. Result: 1,213 legal with no outside letter, 849 impossible, 425 with at least one outside letter, 50 stopped at a 25 second cap with no decision. Pairs farther apart were not finished. Disjoint letter sets were not rechecked; they cannot force a bridge letter.

The longest span that is exactly a German compound, with the new letter inside the word, is `FEINDEMELDUNG` at offsets 8 through 20. It comes from assuming `FEIND` at 8 and `MELDUNG` at 14. Those two cribs leave a one-letter gap at offset 13. All 27 legal mode assignments put `E` there. The same count, 27 of 128 mode patterns, is returned by a second, separate row-and-column checker. Grimm quadgram of those 13 letters: -22.084, mean -2.208. That number is a measurement. It was not used to search.

Why it is not kept:

- The only new letter is `E`. `FEIND` and `MELDUNG` were put in by the search.
- The same test forces other one-letter bridges that are not German, including `NANGRIFF`, `EFEINDSTELLUNG`, and `MMELDUNGMELDUNG`. A German-looking bridge is not unique.
- Other legal pairs force a different letter on an overlapping offset. `FEIND` at 4 plus `STELLUNG` at 11 (24 legal) forces `FEINDE` at offsets 4 through 9, so offset 8 is `D`. `FEINDEMELDUNG` needs offset 8 to be `F`. `STELLUNG` at 13 plus `ABEND` at 5 forces `STELLUNGS` at offsets 13 through 21, which is not `MELDUNG`.
- Offsets 0 through 7 and 21 through 45 stay blank. A 13-letter fragment is not the message.
- No published plaintext of Nr. 86 was used. The 30 September 2026 status list says the message was broken and does not print the reading. This note does not treat that credit as a text.

Shorter spans that happen to be German inflections, also rejected, same reason: `FEINDE` (offsets 4 through 9), `ANGRIFFE` (offsets 2 through 9), `STELLUNGS` (offsets 13 through 21). Each is one added letter on an assumed crib, and they disagree with each other.

## Result

**Failed.** Nr. 86 stays unsolved in this repo. The crib slide does not produce one consistent German fragment. The best candidate, `FEINDEMELDUNG`, is one forced `E` between two assumed cribs, and other legal placements contradict it.
