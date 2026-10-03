# Nr. 86 three-score two-square climb - 2026-10-02 (EDT)

Not a decipherment. Funkspruch Nr. 86 was not solved. No plaintext is claimed.

Run at 2026-10-02 23:41 EDT from `main` at `087a436`. The climber is not part of this commit. Quadgram scores are `engine.german` (`GermanModel.quadgram_score`). Decrypt checks use `engine.ciphers.two_square_decrypt`.

## What was searched

Ciphertext, 46 letters, designator included: `FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ`.

The CryptoCellar page https://cryptocellar.org/bgac/g-army-ts-messages.html (fetched 2026-10-02, page updated 27 July 2026) still lists Nr. 86 with no "Broken on" note and no plaintext. The 30 September 2026 status list cited in `docs/logs/nr86-2026-10-02.md` says the message was broken and does not print the reading. This note does not treat that credit as a text.

Encipherment is the single-stage Truppenschlüssel two-square in `engine.ciphers` (Ostwald and Weierud, https://cryptocellar.org/pubs/mcts.pdf): two 5x5 squares, J omitted, rectangle or same-row right-neighbour, ciphertext letter from the right square first.

Neighborhood: best-improvement on every pairwise letter swap inside each square, plus every row swap and every column swap, then the same kick schedule as the 2026-10-02 German climb (perturb 1..10 random cell swaps and climb again). Restarts shuffle both squares. No crib bonus.

## Three scores

Every saved local optimum is scored three ways. A string that is the unique best on only one of them is rejected. Higher is better on each score.

1. German quadgram log-likelihood from `engine.german`, the Grimm excerpt model. Mean is the total divided by `n - 3`. This is the same score as commit `0b4464e`.
2. Word-break cover: letters covered by a non-overlapping segmentation into dictionary words of length at least 4. The dictionary is the 440 distinct words of that length in `engine/data/german_excerpt.txt` and `engine/data/neural_heldout_grimm_wolf.txt` (comment lines skipped, umlauts folded as in `engine.german`, J folded to I). It is fairy-tale German, not a military lexicon.
3. Repeat score: digram extras, the sum over the 26x26 digrams of `max(0, count - 1)`.

Search objectives, same neighborhood, 300 restarts, 8 kicks, seed 20261002:

| mode | objective | CPU seconds |
| --- | --- | ---: |
| 0 | quadgram only | 1.58 |
| 1 | word-break cover, quadgram as a tie break | 5.27 |
| 2 | repeat score, quadgram as a tie break | 2.92 |
| 3 | quadgram + 4 * cover + 2 * repeat | 9.97 |

The four runs saved 1,200 local optima. All 1,200 plaintexts were distinct.

## Best multi-score candidate (rejected)

Rank-sum across the 1,200 plaintexts (rank 1 is best on that score). The lowest sum is the compromise candidate. It is not the leader of any single score.

- Plain: `ZSSERDEKROBERENXEINSKEINENWELUSTOWERDESKOPFING`
- Quadgram: **-95.9954**. Mean: **-2.2325**.
- Word-break cover: **26** letters (`ERDE`, `EINS`, `KEINEN`, `LUST`, `ERDE`, `KOPF`).
- Repeat: **10** digram extras.
- Squares: `WIUNEOMYBXKAGQRFSVZLHCDTP` / `EUXKMVPICSRGYQNOHLZFBTADW`
- `two_square_decrypt` returns that string. It is not readable German. The pieces are Grimm words stuck together.

It beats the raw ciphertext on all three scores (ciphertext quadgram -176.3662, cover 0, repeat 1). Beating the ciphertext is not a reading. Inside the archive its ranks sum to 469, and three other strings each lead one score.

## Single-score leaders (each rejected)

| leads | plain | quadgram | mean | cover | repeat |
| --- | --- | ---: | ---: | ---: | ---: |
| quadgram only | `DNSCHOEHASGICHKENAUNDHINEGSTOTERDIELVHAEKUGESI` | -84.2658 | -1.9597 | 0 | 2 |
| cover only | `TMUTTEROMNACHUGUNTERRIEFBRMWARFIMMQUWALDURIHRE` | -112.9808 | -2.6275 | 31 | 4 |
| repeat only | `NLQVLDACZZICZICHDAHDAAHTZTTACSSSSNVNVLQACZTTTZ` | -144.4009 | -3.3582 | 0 | 19 |

No plaintext in the archive leads two scores. Each leader wins only one score and is rejected. The repeat leader is a stutter, not German. The cover leader is a chain of tale words (`MUTTER`, `NACH`, `UNTER`, `RIEF`, `WARF`, `WALD`, `IHRE`) and is not a message. The quadgram leader has cover 0.

The impostor from commit `0b4464e`, `EBPHICHENHATTEWEINDENEKRHDESIEGOLDEMWARNTRDASS`, still has a better quadgram than anything in this archive: -77.7089 (mean -1.8072), cover 9, repeat 3. It would lead only the quadgram column. It loses cover to 31 and repeat to 19. Same rejection as in that commit.

## Known controls of length 46

Same climber, same seed, same four objectives, 300 restarts and 8 kicks. Recovered means some hill-climb output was exactly the plaintext.

1. Published booklet fragment, not Nr. 86. Plain `FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENA` (first 46 letters of the Ostwald and Weierud booklet sentence). Squares `EFXWTUMQVHGBIOPDNKRCYLSAZ` / `IVBFTHWSALDRPXGOMUEYKZNQC`. Cipher `FNPSYUXSVGQZPBXXFMAECXEVNAFUMNEWCXOWSXIUNRQKEM`. True scores: quadgram -125.1609 (mean -2.9107), cover 8, repeat 7. **Not recovered** in any of the four 300-restart runs. A one-step neighbor audit (640 swaps: every pair, row, and column in either square) found 30 neighbors that are at least as good on cover and on repeat and strictly better on the quadgram. No positive weighting of these three scores makes the true key a local optimum. This hill climb cannot stop on that plaintext.

2. In-model control. First 46 letters of the folded Grimm excerpt, J folded to I: `INDENALTENZEITENWODASWUENSCHENNOCHGEHOLFENHATL`. Squares `GPODKIUSZMQLFYVAXERHWTBNC` / `NGRTKLAUBVYZXIFHODSWCPQEM`. Cipher `LGTNPZIPHOBNBGHOPAGZVEBTERCHHOPRCHTWDAYFHOOMCU`. True scores: quadgram -74.1644 (mean -1.7248), cover 32, repeat 7. The true key is a local optimum of the quadgram, of cover, and of the combined objective (no neighbor is strictly better). It is not a local optimum of the repeat score (100 neighbors repeat more). **Not recovered** at 300 restarts, and not recovered in a further 4,000 restarts on modes 0, 1, and 3 (seed 20261002, 8 kicks, 32,000 hills each). The mode-1 best in that longer run had cover 35, which is above the true cover of 32, so a high cover is not the plaintext.

3. Held-out control. First 46 letters of the wolf tale after J is folded to I: `DERWOLFUNDDIESIEBENIUNGENGEISZLEINWARENALLEHUN`. Same squares as the Grimm control. Cipher `TNHHNSXSQRTYWRBWMNEYLPTWPDSFAFITLGPISNPZYUORLP`. True scores: quadgram -98.9317, cover 24, repeat 9. The true key is a local optimum of cover only. **Not recovered** at 300 restarts on four modes, nor at 4,000 restarts on mode 1.

## Result

**Failed.** Nr. 86 stays unsolved in this repo. The three scores disagree: each leader wins only one score, and the rank-sum compromise is not readable German. The same method does not recover a known 46-letter control. On the published booklet fragment it cannot, because the true key is not a local optimum of any mix of these three scores. On the Grimm and wolf controls the true key is a local optimum of at least one score, and several thousand restarts still did not reach it.
