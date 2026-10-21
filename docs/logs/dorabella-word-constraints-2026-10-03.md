# Dorabella word constraints, 2026-10-03

No historical plaintext was recovered or verified. This campaign tests a finite dictionary model of unspaced bijective substitution, separately from letter-score optimization. Both the unknown letter map and word boundaries are searched. No target plaintext, phrase template, key, crib, or personality word filter enters the search.

The frozen transcription comes from the [2021 experiment deposit](https://doi.org/10.5281/zenodo.4819086) by Bradley Hauer, Colin Choi, Anirudh S Sundar, Abram Hindle, Scott Smallwood, and Grzegorz Kondrak, member `dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt`. The [recorded first-party metadata check](../easy-unsolved-attempt-2026-10-03.md) identifies the data license as CC BY 4.0; no code from the deposit is imported. The [primary paper](https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf) discusses transcription and orientation uncertainty. These alphabetic labels are neutral glyph identifiers, not phonetic readings. This run uses the selected transcription in its recorded order; it does not adjudicate the autograph or other published transcriptions.

```text
abcdefgdhijklmknkkfbbkmoiopjqgkgfodhrdckkcfplgkjkfsqlmohhojqcqfsqcmstpqckfslqpdbpqfdmod
```

The input has 87 symbols and 20 distinct labels. SHA-256 of the exact lowercase ASCII input is `36d5211d9beb72c0fe99fad1fa1c268c7519d2cb82f294d53237cff4eded6730`. Uppercase normalized input hashes to `ed1b7d3391cbe06bc52d023643860a0795624836cb7efe155d0af59e269d5a50`.

Two vocabularies were frozen before the original four target runs:

- **Training prose:** the first 60% of ASCII letter positions in the dedicated Austen training excerpt, truncated to the last complete token, plus original `engine/data/english.txt`. Comment lines beginning `#` are omitted. The union has 1,153 word types and hashes to `373ba75e116b56f8bbd17758c51deecc8dbde774d082139d65bf6fe57e046fc0`.
- **Broader prose:** the bodies of [Pride and Prejudice, eBook 1342](https://www.gutenberg.org/ebooks/1342), and [Jane Eyre, eBook 1260](https://www.gutenberg.org/ebooks/1260), strictly between their Gutenberg START/END marker lines. Both first-party catalog pages identify the books as public domain in the USA. The union has 14,638 word types and hashes to `493c4b7bab8e48d702ba911b7c35e14fa1a1cd158bf0d3f81580027fc0ca0708`.

Token extraction uses ASCII letter runs with optional internal straight or curly apostrophes; apostrophes are removed. Hyphens split tokens. Word types are uppercase, sorted, and deduplicated, with a 64-letter entry limit. Proper names, foreign ASCII words, and initials receive the same treatment. These are corpus vocabularies, not curated dictionaries of ordinary English. Target text, control answers, Doyle, Wells, and neural development or final evaluations are not added to them. The original repository prose follows the repository MIT license. Full source-file and extracted-body hashes are in the [JSON record](dorabella-word-constraints-2026-10-03.json).

Each original target run declares at most 250,000 search nodes, 4,096 pending states, 20 retained witnesses, 20,000 lexicon entries, and a 30-second cooperative deadline. The ordinary finite model permits word lengths 1 through 32. The stricter finite model permits 2 through 16, explicitly excluding one-letter words and longer words; it is not a complete model of English.

| Vocabulary and word-length model | Nodes | Stop | Witnesses | Distinct plaintexts | Distinct boundary patterns |
| --- | ---: | --- | ---: | ---: | ---: |
| Training prose, 1 through 32 | 250,000 | Node limit | 0 | 0 | 0 |
| Training prose, 2 through 16 | 250,000 | Node limit | 0 | 0 | 0 |
| Broader prose, 1 through 32 | 772 | Candidate limit | 21 | 6 | 4 |
| Broader prose, 2 through 16 | 250,000 | Node limit | 0 | 0 | 0 |
| Broader prose, A/I singleton supplement, 1 through 32 | 249,228 | Node limit | 0 | 0 | 0 |

Every search is incomplete. Zero-candidate branches report `model_status: unknown`, not an exhaustive rejection. The broad 1-through-32 model has compatible witnesses but is incomplete. Its early witnesses consist mostly of isolated corpus initials and short fragments. They satisfy the stated constraints and exact forward replay, but do not provide credible historical readings. Only 20 of the 21 observed witnesses are retained because of the candidate cap. No forced plaintext or uniqueness is asserted.

After that initial vocabulary diagnostic, a separately authorized supplement retained every longer broad-vocabulary entry while permitting only `A` and `I` as one-letter words. Its 14,618-word vocabulary and unchanged 1-through-32 length interval are declared separately in the record. It consumed the remaining 249,228 nodes of the original one-million-node campaign budget. It reached the cap with no witness. This supplemental model removes isolated initials; it does not establish that the target lacks ordinary English words.

The control uses a separate, constructed 87-letter plaintext, independently enciphered before inference. The solver receives only the ciphertext and 28-word vocabulary containing the genuine words and unrelated distractors. It receives no key or word boundaries:

```text
THE COURIER SLOWLY CARRIED SEALED LETTERS THROUGH THE VILLAGE BEFORE SUNRISE AND RETURNED BY THE RIVER
```

The search exhausts in 883 nodes with one plaintext and one boundary pattern, recovering all 87 letters and the exact word boundaries. The recovered unspaced ASCII hash is `66bf40dbc849503f745921247db0c2c4f3a544bb9d4443711acfba2c00bb5fa5`. The [certificate](../../engine/data/unspaced_substitution_certificate.json) and regression verify the literal ciphertext, independent encoder, actual recovered output hash, and absence of key or boundary inputs. This is a covered-vocabulary control, not a target hypothesis or general language accuracy estimate.

The training vocabulary lacks the control words `COURIER`, `SEALED`, and `SUNRISE`; the broader vocabulary covers all its words. No missing word was added after this coverage audit. A separate short constructed English control deliberately omits `CONSISTENT` from its vocabulary: search exhausts in 43 nodes with no solution. These controls demonstrate why finite dictionary failure cannot exclude English, even without a node cap.

Independent review found and fixed a reporting error: different plaintexts sharing the same boundary tuple were previously counted as boundary ambiguity. For example, `ABBA` can fit both `NOON` and `DEED` with one boundary `(4,)`. A failing-then-passing regression now separates solution witnesses, plaintexts, and boundary patterns. The search order, models, candidate texts, node counts, and stop reasons did not change.

The original campaign used 1,000,000 target nodes. A separately recorded validation replay used another 1,000,000 nodes solely to verify the reporting fix with the same inputs, vocabularies, search order, and bounds. Cumulative actual target nodes are therefore **2,000,000**. Final replay target search time sums to 1.890 seconds; its full campaign and controls took 2.631 seconds on this local run. These timings are recorded observations, not a comparative speed benchmark.

The original report is superseded for boundary semantics and preserved in task work. Its SHA-256 is `ba9a3374082be4ded9e1e27a799343f5002152828cb482718ce28beea4b557e1`. The committed JSON records its original source hash and run summaries alongside the corrected replay. Final solver source hashes to `af20fc59ae3a9c5ff1d1085775b535026536cb5f59209994bda6af4c2f5b69b9`.

Reproduce the five declared models with the exact public-domain source snapshots whose hashes are recorded in JSON. The driver rejects an output directory containing existing files and caps each source file at 2 MB. It writes its protocol and lexicons before search, then complete result reports. If the original four runs consume the entire node budget, the supplement is explicitly not run.

```sh
.venv/bin/python tools/dorabella_word_campaign.py \
  --austen /path/to/pg1342.txt \
  --bronte /path/to/pg1260.txt \
  --ordinary-singletons \
  --output /private/tmp/dorabella-word-reproduction-new
```

The final ten standard-library tests cover blind recovery, the 87-letter certificate, global injection and repeat consistency, an independent exhaustive map-and-partition oracle, plaintext versus boundary ambiguity, exact node exhaustion, state and candidate limits, mocked timeout, bounded iterable consumption, and invalid input contracts. They validate these model controls and reports. The campaign supplies no Dorabella solution and no exclusion of English or substitution.
