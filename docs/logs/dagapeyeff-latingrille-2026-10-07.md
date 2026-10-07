# Latin under a turning grille: how right the key must be, 7 October 2026

Not a reading. No letter string is stored. The cells were not searched.

The [compiled grille search](dagapeyeff-grillec-2026-10-06.md) finds planted grilles with the letter key given and none with grille and key both unknown. `engine.dagapeyeff_latingrille` repeats the question under the Latin quadgram model on four planted held-out Thomistic windows. It asks how right the key must be, and whether re-solving the key at every grille move helps.

**Key held fixed.** The grille is annealed alone (4 restarts of 2,000,000 steps), the key held at the true key or at a key with some symbols' letters rotated.

| Key | Cells right under the key | Grilles recovered (49 of 49 holes) | Holes right otherwise |
| --- | --- | --- | --- |
| True | 100 percent | 4 of 4 | |
| About 15 percent spoiled | 77 to 82 percent | 1 of 4 | 18 to 24 |
| About 30 percent spoiled | 65 to 69 percent | 0 of 4 | 16 to 22 |

**Key re-solved at every move.** Each grille move is scored by a greedy key climb under the quadgram model (`engine/dagapeyeff_latingrille.c`), 2 restarts of 60,000 moves, then grille and key are polished together (2,000,000 steps). It recovers 0 of 4, ending at 15 to 18 of 49 holes and -2.81 to -3.05 a letter against -1.37 to -1.78 for the true texts. Climbing the key on a letter-pair model instead also recovers 0 of 4 (14 to 19 holes). Under pairs a wrong grille with its best key scores as well as the true one, so the pair score cannot guide the search.

Scratch runs, not frozen, agree. 80 independent joint restarts of 1,000,000 steps found neither of two planted grilles (at most 22 holes). Starting the joint search from the true key with the key free to move drifts away to about -2.5 a letter.

The grille needs a key with roughly 80 percent or more of cells right before the grille can be found. Key-only methods reach at most 59 percent ([seeded key](dagapeyeff-grillec-2026-10-06.md)). A Latin message under a turning grille is therefore neither found nor excluded.

Not a reading. No letter string is stored.
