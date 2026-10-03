# Nr. 86 German-scored two-square climb, 2026-10-02 (EDT)

Not a decipherment. Funkspruch Nr. 86 was not solved. No plaintext is claimed.

Run at 2026-10-02 23:31 EDT from `main` at `eb0792d`. The climber is not part of this commit. Scoring and the decrypt check use the repo.

## What was searched

Ciphertext, 46 letters, designator included: `FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ`.

Source of the ciphertext, still with no printed plaintext: https://cryptocellar.org/bgac/g-army-ts-messages.html (page “Messages That We Have Failed to Break”, updated 27 July 2026). The 30 September 2026 list at https://cryptocellar.org/bgac/1941-msg-list.html says Nr. 86 was broken and does not print the reading. This note does not treat that credit as a text.

Encipherment is the single-stage Truppenschlüssel two-square in `engine.ciphers` (Ostwald & Weierud, https://cryptocellar.org/pubs/mcts.pdf): two 5×5 squares, J omitted, rectangle or same-row right-neighbour, ciphertext letter from the right square first.

Objective: `engine.german` quadgram log-likelihood (`GermanModel.quadgram_score` / `engine.solvers.two_square.german_trigram_score`), the Grimm excerpt model. Higher (closer to zero) means more like that fairy tale. It is not a military-German model. Mean is the total divided by `n - 3`.

Neighborhood: best-improvement on every pairwise letter swap inside each square, plus every row swap and every column swap, then the same kick schedule as `climb_two_square` (perturb 1..10 random cell swaps and climb again). Restarts shuffle both squares. Cribs `ANGRIFF`, `FEIND`, `STELLUNG`, `MELDUNG` were added only as a flat bonus on the objective (`weight` times how many of those strings occur). Acceptance below uses the pure German score, with the crib bonus removed.

## German baseline already in the repo

From `docs/logs/two-square-2026-10-02.md`, rescored here with the same function:

| text | letters | quadgram | mean | role |
| --- | ---: | ---: | ---: | --- |
| raw Nr. 86 ciphertext | 46 | −176.3662 | −4.1015 | documented raw score, about −4.102 |
| earlier English-trigram climb preview `UTGSANDTHEREODCLISATTVDENTHAORETIDNVPXGANDTHEW` | 46 | −149.9250 | −3.4866 | documented climb, about −3.487 |
| unit-test probe `DERWOLFUNDDIESIEBENJUNGENGEISZLEINWARENALLEHUNGRIG` | 50 | −112.4926 | −2.3935 | held-out-style German; the log’s other probe was about −2.325 |
| booklet sentence in that log, `FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENABGEWEHRT` | 54 | −145.2287 | −2.8476 | published example, not Nr. 86 |
| first 46 letters of that booklet sentence | 46 | −125.1609 | −2.9107 | known-plaintext control, not Nr. 86 |
| message 64 raw plaintext `SQARFXPLACHXPLACHXISTZURUEQB` | 28 | −83.9534 | −3.3581 | published, Fig. 6 squares |

A candidate has to be clearly better than that German baseline and read as German. Beating the number alone is not enough: this model scores short Grimm-like strings above real Truppenschlüssel prose.

## Commands

Log-probabilities were the `engine.german` quadgram table. The climb binary implemented the neighborhood above. Each line is `ciphertext restarts kicks seed crib_weight [cribs...]`.

Pure German score, no crib bonus:

```
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 300 12 20261002 0
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 200 12 7 0
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 200 12 86 0
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 300 12 20261003 0
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 300 12 99 0
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 300 12 123456 0
```

Crib bonus only as a search hint (1,600 pure restarts above, plus these):

```
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 80 8 86101 8 ANGRIFF
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 60 8 86111 25 ANGRIFF
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 80 8 86102 8 FEIND
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 60 8 86112 25 FEIND
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 200 12 86112 25 FEIND
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 80 8 86103 8 STELLUNG
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 60 8 86113 25 STELLUNG
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 80 8 86104 8 MELDUNG
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 60 8 86114 25 MELDUNG
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 100 8 86105 8 ANGRIFF FEIND STELLUNG MELDUNG
FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ 80 8 86115 25 ANGRIFF FEIND STELLUNG MELDUNG
```

Wall time for the whole set was a few seconds per batch, not hours. `python3 -m unittest tests.test_two_square` was not re-run as the claim; message 64 was checked inside the same decrypt used for the control.

## Best candidate (rejected)

Best pure score seen, from the 60-restart `FEIND` hint at weight 25, seed 86112. The crib is not in the string. Python `two_square_decrypt` / `two_square_encrypt` round-trips it, and `german_trigram_score` matches.

- Plain: `EBPHICHENHATTEWEINDENEKRHDESIEGOLDEMWARNTRDASS`
- Quadgram: **−77.7089**. Mean: **−1.8072**.
- Squares: `GLIXQANTMZCUPOFYWEBSKHRDV` / `HNXQSRITVYOGACWEKBFUMZLPD`
- Against the documented baseline: mean −1.807 is higher than the ciphertext (−4.102), the earlier climb (−3.487), the held-out probe (−2.393 here, about −2.325 in the earlier log), and the booklet sentence (−2.848).
- It is not clearly a German reading. The only whole words in it are scraps the Grimm model likes (`HATTE`, `WEIN`, `GOLD`, `DASS`). It has none of `ANGRIFF`, `FEIND`, `STELLUNG`, `MELDUNG`.
- It is not unique. Other seeds land in the same band on different strings, including pure climbs with no crib: seed 99, 300 restarts, −80.6781 (`OCFRDCHEISTDIEINEGOLDENEKLESRNUNDDELSTEONABMEN`, mean −1.876); seed 86, −82.8075; seed 20261002, −83.4638. Those strings also paste fairy-tale fragments (`DIEINEGOLDENE`, `KUGEL`, `KOENIG`) and are not the same plaintext.

## Why the higher score is not accepted

Known-plaintext controls, same climber, same German score:

- Booklet fragment `FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENA` (46 letters) under random squares `EFXWTUMQVHGBIOPDNKRCYLSAZ` / `IVBFTHWSALDRPXGOMUEYKZNQC` encrypts to `FNPSYUXSVGQZPBXXFMAECXEVNAFUMNEWCXOWSXIUNRQKEM`. True score −125.1609 (mean −2.911). A 200-restart, 12-kick climb (seed 20261002) returned `VLREBENWODUNTENGOLDENDSATSCHRLEINDICHDIEKTENLI`, score −84.4302 (mean −1.963), which is not the plaintext. The impostor beats the true text.
- Message 64 ciphertext `FFZNSBQTHNCIQTHNCIXPOLAQTQNZ` decrypts with the Fig. 6 squares to `SQARFXPLACHXPLACHXISTZURUEQB`, score −83.9534 (mean −3.358). A 100-restart climb returned `XABERICHTESICHTESINEKLENEKUG`, score −35.8928 (mean −1.436), not the published plaintext.

So a 46-letter climb that scores near −1.8 is what this fairy-tale model does when it is wrong. The Nr. 86 best sits in that band. It is better than the old documented climb and better than the held-out probe number, and it is still rejected.

Crib hits that did stick are worse and still not German. Examples: `FEIND` inside `HRTEINENFNDUBMWASSERBNUFEINDHASDEXOSPINERBRUNT` at −93.0615 (mean −2.164); `MELDUNG` inside `MTGERFOSMELDUNGDATSCPASWAGELDUOLWILLEFDENSCHEI` at −99.9501 (mean −2.324). `ANGRIFF` and `STELLUNG` did not occur in any saved local optimum under the budgets above. Mean −2.16 is only a small step past the probe and is worse than the unconstrained impostors.

## Result

**Failed.** Nr. 86 stays unsolved in this repo. The best candidate is not obviously German, it is not a published plaintext, and the same search outscores known Truppenschlüssel plaintext without finding it.
