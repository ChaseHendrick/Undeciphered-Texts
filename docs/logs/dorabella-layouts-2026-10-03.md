# Dorabella: physical layouts and two published transcriptions

Recorded 2026-10-03. This campaign produced no independently verified historical reading. It tested a finite set of physical reading orders with bijective substitution search, and preserved exact forward replay for every retained candidate. English fitness is an optimization score, not evidence that a candidate is Elgar's message.

## Primary inputs and physical evidence

The [Hauer et al. 2021 paper](https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf), page 2 Figure 1, was rendered directly from the downloaded PDF and inspected. The physical rows contain 29, 31 and 27 glyphs, with zero-based offsets 0, 29 and 60. A second reader independently counted the same rows. The paper describes ambiguous orientations and treats transcription letters as arbitrary symbol labels. Its author archive supplies the 87-character input with 20 distinct labels. [Author archive](https://doi.org/10.5281/zenodo.4819086)

The [Schmeh 2018 primary paper](https://ep.liu.se/ecp/149/026/ecp18149026.pdf) supplies another literal transcription on printed page 146. Its three printed lines were separately counted as 29, 31 and 27 characters, and its page 147 facsimile was inspected. This transcription has 21 distinct labels. The two inventories disagree on 43 pairwise symbol-equality relations. They were tested separately; English scores were not used to adjudicate disputed glyphs. [Publisher record](https://ep.liu.se/en/conference-article.aspx?Article_No=26&issue=149&series=ecp)

Both PDFs were fetched with normal TLS certificate verification. The publisher's `www.ep.liu.se` URL failed hostname verification; the same publisher's `ep.liu.se` URL succeeded without a certificate override. PDF hashes, exact transcription strings, raw author-member hash and inspected page numbers are in the companion JSON.

The source-backed geometry establishes rows, not reading direction. Neither checked paper provided a verified mapping from every neutral archive label to an indexed arc-count/orientation alphabet. No musical, numeric-orientation or invented Latin-label geometry search was performed.

## Frozen protocol and exact replay

Sixteen layouts combine top-to-bottom or bottom-to-top row order with each of the eight independent physical-row reversal masks. This includes whole reversal and both alternating row directions. No arbitrary row permutations, glyph substitutions chosen for English output, thematic cribs or historical plaintext guesses were added.

Every layout stores `ordered_to_original`: ordered position `j` reads original position `permutation[j]`. Restoring a plaintext candidate assigns it back to those original positions. An independent inverse implementation verified all 16 permutations. Each retained candidate is enciphered with its recovered key in the proposed reading order, then restored to the original stream. Both ordered and original ciphertext replay must match exactly. The JSON exports the original-position candidate and original ciphertext replay, so reading-order output is not confused with the physical inscription coordinates.

The baseline uses existing repository `solve_substitution`: five restarts, 6,000 annealing steps, initial temperature 30, cooling 0.997, greedy swap polish and four escape shakes. Three fixed seeds are run in breadth-first order over both inventories and all layouts: 96 target runs. The existing repository English quadgram model is frozen and read-only. No additional corpus or dictionary is supplied; finished-candidate neural scoring is disabled.

After baseline completion, a declared protocol extension used the new sparse parallel-tempering solver on all 31 remaining ordered streams, without fitness selection. Hauer identity was excluded because the independent main campaign owns original-stream tempering. One new seed, one restart, 5,000 sweeps, eight default temperatures, exchange interval 25, six polish passes and a 45,000-proposal per-stream cap were used. Full score recomputations, delta proposals and replica exchanges are reported separately. This extension does not create independent validation data.

The established total ceiling remained 180 seconds of measured search and 6,000,000 counted evaluations. The supplemental accounting sums full-score calls and delta proposals, which have different costs; it is not a count of distinct keys or a fraction of the factorial keyspace. Exchanges are separate. Actual values were:

| Measurement | Actual |
| --- | ---: |
| Completed baseline target searches | 96 |
| Completed supplemental target searches | 31 |
| Baseline full-score calls, including controls | 4,420,222 |
| Independent candidate and reference score checks | 112 |
| Supplemental full-score calls | 403 |
| Supplemental delta proposals | 1,252,175 |
| Combined counted evaluations | 5,672,912 |
| Supplemental exchange attempts | 21,700 |
| Total measured search seconds | 61.008 |

All configured baseline runs and all 31 supplemental inner searches completed. This is completion of the declared heuristic work, not an exhaustive key search or evidence against every substitution model. Supplemental maximum cached-score drift was about `1.23e-12`; retained candidates were fully rescored.

## Independent controls and outcome

Four new literal English plaintexts were normalized and truncated by the declared first-87-letter rule, enciphered independently, and tested with the key withheld from inference. Their exact plaintexts do not appear in the repository model corpus. Each was placed under two inverse layouts, producing eight layout fixtures. The ordered inference input repeats within each pair, so these are four distinct recovery controls, not eight independent cryptanalytic trials.

| Distinct control | Correct positions out of 87 | Recovered score | Reference score |
| --- | ---: | ---: | ---: |
| River and bridge | 86 | -133.629 | -134.180 |
| Doctor's letter | 86 | -157.755 | -162.049 |
| Farmer and horses | 87 | -155.180 | -155.180 |
| Train and travelers | 83 | -147.343 | -155.210 |

Only one of four distinct plaintexts was recovered exactly. In each imperfect control the wrong candidate scored above the reference, directly demonstrating a short-text objective limitation. Every inverse-layout fixture still passed independent forward replay.

The target produced 96 distinct baseline fitness candidates and 69 distinct supplemental witnesses. Their local English fragments do not make a coherent verified reading, and no source-backed heldout plaintext is available here. The highest baseline fitness was about -216.433; the highest supplemental fitness was about -220.087. These scores neither select the authentic transcription nor establish a decipherment. There is no estimated significance, empirical null calibration or correctness probability in this campaign. Broader corpus and original-stream searches are separate experiments.

## Replay and checks

The companion `dorabella-layouts-2026-10-03.json` preserves all target candidates, permutations, literal inputs, reference controls, hashes and counted bounds. The runner uses standard-library code and existing engine APIs:

The [archived baseline driver](artifacts/dorabella-layout-baseline-runner-2026-10-03.py)
preserves the exact source snapshot hashed when the baseline ran, SHA-256
`1637a7f7ecf6218a5de32e2e1b45dc510c0e950caaf72ec6fb130a41140db7f2`.
It is a source audit artifact; the current `tools/` driver is the executable
reproduction entry point and includes the later extension. The JSON separately
pins its final release hash. The cipher engine and scorer were unchanged.

```sh
.venv/bin/python tools/dorabella_layout_campaign.py --output /tmp/dorabella-layouts-replay.json
.venv/bin/python tools/dorabella_layout_campaign.py --output /tmp/dorabella-layouts-replay.json --extend-tempering
```

Existing experiment output is protected from accidental overwrite; a second extension is rejected. A separate one-call control stopped at exactly one objective call, emitted an incomplete result, retained the interrupted-run metadata and made no solve claim. Python 3.10 grammar parsing and all 16 independent inverse-layout controls passed. Read-only review of the new tempering solver additionally checked 1,200 randomized committed swaps against independent full scores and 100 exchange ratios against direct Boltzmann algebra; maximum absolute error was below `2.28e-13`. Five focused delta tests passed. No target reference, unverified historical text, archived GPL solver code, live submission or Nr86 input was used.

The next discriminating evidence would be a source-backed glyph-to-geometry table or an independently authenticated plaintext fragment. Repeating more seeds under the same scoring objective can improve optimization, but the observed control errors show why it cannot by itself authenticate a historical reading.
