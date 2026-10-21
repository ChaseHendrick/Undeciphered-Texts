# Dorabella: heavier original-stream replica exchange, 3 October 2026

No verified reading was recovered. Ten frozen seeds made **10,016,740 target key-swap proposals** and evaluated **234,387,022 affected quadgram windows**. The checkpointed campaign, including three controls, finished in 65.139 seconds. All declared seed runs completed. This remains a sampled heuristic search, with no exclusion of the finite substitution keyspace.

The [machine-readable record](dorabella-tempering-2026-10-03.json) retains settings, exact counts, all stored plaintext/key witnesses, complete forward streams, source and code hashes, and the failed control. The [new solver](../../engine/solvers/substitution_parallel_tempering.py) uses exact sparse score deltas and logical replica exchange. The [reproduction script](../../tools/dorabella_tempering.py) does not train a model or submit an answer. Its frozen JSON `tool_name`, `substitution-parallel-tempering`, is an internal algorithm identifier; the public registry command is `substitution-tempering`.

## Frozen input and assumptions

This reuses the exact author-deposited [HistoCrypt 2021 data](https://doi.org/10.5281/zenodo.4819086), member `dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt`, acquired in the [earlier source audit](../easy-unsolved-attempt-2026-10-03.md). The [authors' paper](https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf) provides the research context. Source snapshots in this log are reused, not represented as a fresh live status audit.

The 87 neutral labels are:

```text
abcdefgdhijklmknkkfbbkmoiopjqgkgfodhrdckkcfplgkjkfsqlmohhojqcqfsqcmstpqckfslqpdbpqfdmod
```

Raw ASCII SHA-256: `36d5211d9beb72c0fe99fad1fa1c268c7519d2cb82f294d53237cff4eded6730`.

Uppercase normalized SHA-256: `ed1b7d3391cbe06bc52d023643860a0795624836cb7efe155d0af59e269d5a50`.

There are 20 distinct glyph labels. The labels have no claimed phonetic meaning. This campaign retains the flattened author stream: no row reversal, reordering, inserted spaces, transcription correction or invented letters. It tests one-to-one English substitution. Phonetic spelling, musical encodings, homophony and other models remain outside this campaign.

The objective is the unchanged quadgram table derived from `engine/data/english.txt`. No target phrase, artist name, dictionary, supposed solution, reference plaintext or neural fitting enters optimization. A full 26-letter permutation includes arbitrary mappings for six unobserved labels. Neither those mappings nor an English-fitness score provide independent historical evidence.

## Algorithm and declared coverage

Replica exchange is established prior work; see [Wang and Swendsen's account](https://arxiv.org/abs/cond-mat/0407273). This implementation independently combines it with exact sparse quadgram updates for substitution keys. It is a repository implementation, not a claim of algorithmic priority or a historical break.

For each ciphertext quadgram, the cached index is `17576*k[a] + 676*k[b] + 26*k[c] + k[d]`. Swapping key values at symbols `x,y` changes an affected index by `(k[y]-k[x])*(weight[x]-weight[y])`. Weights include every occurrence of a symbol in the window. The delta sums the new-minus-old table scores only at affected windows; the key remains a permutation. Retained candidates receive a fresh full score.

Eight logical replicas have temperatures `0.25, 0.5, 0.9, 1.5, 2.5, 4, 7, 12`. Each sweep proposes one key swap in each replica. Adjacent disjoint exchange pairs alternate every 25 sweeps. For maximizing score `S`, the exchange log acceptance ratio is `(1/T_i-1/T_j)*(S_j-S_i)`. States exchange between temperature slots; temperature values do not travel with states. These replicas execute in one Python process, not parallel worker threads.

Each seed runs five fresh ladders of 25,000 sweeps, with up to eight greedy polish passes per restart. Polish shares the proposal cap. Seeds are `1729, 2718, 3141, 5772, 8111, 104729, 130363, 20261003, 20261004, 20261005`. Per-seed caps are 1,020,000 proposals and 30 seconds; the main campaign cap is 11,000,000 proposals and 180 seconds, including controls. Timeout checks are cooperative and initialization/result-finalization can add overhead. No seed reached a time or proposal cap.

The ten target runs made 175,000 replica-exchange attempts, with 37,358 accepted exchanges, and 570 full-score calls. Actual target proposals include polish. Repeated states count again; these counts are not distinct keys. The maximum retained cached-versus-fresh score drift was `2.45e-12`.

The earlier original-stream bijective attack made 71,339 full-score evaluations. This new campaign made about 140.4 times that many swap proposals. A swap delta and a full-score call are different work units. The new target evaluated about 468.8 million old/new quadgram table entries through deltas; the previous target's full calls evaluated about 6.0 million windows. This is substantially heavier coverage, not a matched-budget speed or correctness benchmark.

## Independent controls before the main target runs

Control plaintext and key are used only by a separate encoder and post-search comparison. The optimizer receives ciphertext alone. The table is unchanged for every control and target.

| Control | Recovered positions | Exact? | Actual proposals | Reference fitness | Recovered fitness |
| --- | ---: | --- | ---: | ---: | ---: |
| Original 87-letter meeting-narrative prefix | 87/87 | Yes | 161,350 | -149.115340 | -149.115340 |
| Original 87-letter courier sentence | 79/87 | No | 161,824 | -194.438916 | -188.208661 |
| Original repository geology fixture | 496/496 | Yes | 56,650 | -1060.387547 | -1060.387547 |

The passing 87-letter prefix has 15 distinct plaintext letters, fewer than Dorabella's 20 glyph labels. It is a constructed prefix ending in `AND`, not a published historical solve, an accuracy benchmark, or a representative sample. Its recovered SHA-256 is `6f3038e1f2db4234fda1a0c215e63aa8e1a035d1ee2afa8f224d67853b632768`; the [certificate](../../engine/data/substitution_parallel_tempering_certificate.json) records the literal ciphertext, hidden-key search settings and exact independent forward replay. The long fixture recovered hash is `b10856fa44a5a6a5db837ef160844a00796b2227a484cba0db170f5d04e90ea6`.

The courier failure is material. The wrong output has **higher objective fitness than the independently known true text**. More exhaustive optimization of this score would not necessarily select the correct sentence. Exact re-encryption of that wrong candidate establishes transformation consistency only. The test suite preserves this negative control explicitly.

The first exact-recovery regression used the courier fixture and failed. Before freezing the main campaign, separate original controls were measured with the same unchanged objective: an 88-letter harbor sentence recovered 84 positions, a 146-letter courier extension recovered 138, and a 120-letter meeting narrative recovered exactly. Its separate 87-letter prefix also recovered exactly and became the passing regression. The JSON discloses this fixture selection; exact exploratory operation counts were not retained, and each such run had a 180,000-proposal cap. These exploratory controls are not included in the checkpointed main-campaign totals.

An earlier performance pilot also tested the original Dorabella stream before the final frozen campaign. It made 80,310 proposals in 0.640 seconds. Its full key and source byte hash were not retained, so it is explicitly separated from the forward-verified final witnesses. It did not change the objective or target transcription.

## Target results and independent verification limits

Best target fitness improved from the earlier `-223.139627` to `-218.493116`. Fifty distinct stored candidate plaintexts remain across the ten seed reports. Eight distinct seed-best readings have pairwise Hamming distances from zero to 73 of 87 positions. Some best-score ties differ at the first glyph; convergence on a common high-scoring basin does not make it historically correct.

One retained best-score witness is:

```text
JBRIDTFINSMOYWOCOOTBBOWASALMEFOFTAINGIROORTLYFOMOTHEYWANNAMERETHERWHPLEROTHYELIBLETIWAI
```

Its plaintext-to-cipher A-Z encryption key is `OBNEQGRSDAXPJHKTYCIFUWMZLV`. This is a gibberish fitness candidate containing English-looking fragments, not a proposed accepted message. The JSON preserves all stored alternatives and their own maps instead of silently filling or choosing letters.

Every stored candidate independently re-encrypts the **entire** original 87-symbol stream under its recorded bijection. Its forward SHA is the frozen normalized input SHA above. That is stronger than checking a fragment, but supplies no independent historical plaintext, key, encoding rule or heldout reference. No acquired independent historical verification exists; `claimed_plaintext` remains null. The keyspace is still `26!/6!` observed mappings, and no finite-keyspace exclusion follows from these sampled runs.

## Checks and reproduction

Before the module existed, the new focused test import failed with `ModuleNotFoundError`. The completed focused suite passes 14 tests, including the independent literal short recovery, original long recovery, full-score delta oracle for every swap pair, repeated-symbol windows, committed swaps, exchange sign, deterministic seeds, proposal/time bounds, supplied frozen table and the wrong-higher-fitness control. The final focused run completed in 4.322 seconds.

A separate agent also compared 1,200 committed swaps against independent random dense-table full scores and 100 exchange ratios against direct Boltzmann-weight algebra; maximum error was `2.28e-13`. This verifies the local objective mathematics, not Dorabella correctness. Solver, corpus and reproduction source hashes remained unchanged during the main campaign. Full-suite and public integration checks are reported separately by the parent task.

```sh
.venv/bin/python -m unittest discover -s tests -p test_substitution_parallel_tempering.py
.venv/bin/python tools/dorabella_tempering.py --output /tmp/dorabella-tempering-replay.json
```

Reproduction runs a new bounded search and records its own timings and current source hashes. The same seeds, corpus and implementation reproduce candidates and deterministic operation counts if wall limits do not interrupt them. This log establishes a stronger optimization attempt and a useful new solver. It does not establish a decipherment, unique reading, correctness probability or exclusion of other cipher families.
