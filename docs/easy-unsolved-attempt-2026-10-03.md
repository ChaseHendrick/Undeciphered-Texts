# Dorabella bounded open-target attempt, 3 October 2026

**No verified reading was recovered.** A frequency baseline and two stochastic substitution models were actually run on Dorabella's 87-symbol research transcription. The seven target runs returned conflicting candidates. Both long known-answer controls succeeded, but neither matched-length 87-character control recovered completely. Shortness did not make this a reliable or uniquely solvable case.

The [complete JSON record](easy-unsolved-attempt-2026-10-03.json) preserves exact source hashes, ciphertext, parameters, observed work counts, all seven candidate witnesses, forward comparisons, control references and limitations. `claimed_plaintext` remains null and `new_verified_plaintext` is false. Reproduce with `.venv/bin/python tools/easy_unsolved_attempt.py` on macOS or Linux; the script uses existing engine methods and a POSIX signal for its 120-second search deadline. A rerun writes a fresh JSON record, so preserve the dated record if comparing runs.

## Source and input

The live [Decipher challenge](https://decipher.nu/challenges/elgars-dorabella-cipher/workbench) states that no systematic decipherment has been accepted. This is a current first-party community challenge observation, not proof about every unpublished proposal. Hauer and colleagues' [primary experimental paper](https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf) distinguishes uncertain glyph orientations from experimental symbol labels and does not establish a reading.

The authors deposited [Code and Data, HistoCrypt 2021](https://doi.org/10.5281/zenodo.4819086), published 27 May 2021. The [official API](https://zenodo.org/api/records/4819086) was fetched with normal TLS verification. Its metadata declares CC BY 4.0 for the deposited data and a separate GPL3 code notice. No third-party source code, corpus or model was imported into the repository.

The archive member `dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt` was read directly from a streamed archive response. Its exact 87 ASCII bytes are:

```text
abcdefgdhijklmknkkfbbkmoiopjqgkgfodhrdckkcfplgkjkfsqlmohhojqcqfsqcmstpqckfslqpdbpqfdmod
```

Raw SHA-256: `36d5211d9beb72c0fe99fad1fa1c268c7519d2cb82f294d53237cff4eded6730`. Uppercase engine-input SHA-256: `ed1b7d3391cbe06bc52d023643860a0795624836cb7efe155d0af59e269d5a50`. There are 20 distinct labels. They are glyph identifiers, not authentic Latin ciphertext letters or phonetic values.

The streamed inspection stopped after 31.857 seconds; the full archive MD5 was not recomputed. The live workbench displays the same character sequence. An [older participant transcription](https://raw.githubusercontent.com/doranchak/zodiac-killer-ciphers/master/src/main/java/com/zodiackillerciphers/ciphers/Ciphers.java) has repeated-symbol assignment disagreements at zero-based positions 33 and 77 after canonical relabeling. It was not searched or selected according to English fitness. No original-autograph transcription adjudication is claimed. The author's flattened input was preserved, without guessed word boundaries, punctuation, omissions or reordered positions.

## Declared attacks

The deterministic baseline assigns glyph-frequency ranks to English unigram ranks; its quadgram score is computed afterward. The bijective model uses existing cooled annealing with one-to-one glyph/letter mapping. The relaxed homophonic model uses existing fixed-temperature annealing, allowing different glyphs to decode to the same letter. Its larger mapping freedom does not constitute stronger evidence. Both optimizers use the same existing English quadgram corpus; neither fits new weights or uses target cribs.

Seeds were fixed at 1729, 2718 and 3141 for each optimizer. Bijective runs used five restarts of 3,000 iterations, temperature 30 and cooling 0.997, followed by four 1,500-iteration shakes and at most 16 polish passes per polish call. Homophonic runs used 10,000 iterations, temperature 2.0 and at most 30 polish passes. The unused post-search neural opinion was disabled, preventing incidental neural-model fitting. No expected target text, artist-name dictionary or tuning from target output entered the search.

| Target procedure | Runs | Measured objective operations | Distinct candidate texts |
| --- | ---: | ---: | ---: |
| Frequency baseline | 1 | 1 full score | 1 |
| Bijective annealing | 3 | 71,339 full scores | 3 |
| Relaxed homophonic annealing | 3 | 95,563 incremental updates plus 9 full scores | 3 |

The total target count was 166,912 operations. Controls used another 169,350, for 336,262 overall, below the 1,000,000-operation cap. The complete search/control phase took 7.278 seconds and finished every declared run. Source retrieval is separate from that timing. A full score call and an incremental assignment update have different costs; repeated states and rollback updates are counted, so these are not distinct keys or a fraction of key-space coverage.

## Controls and ambiguity

Independent known-key encoders generated control ciphertexts and exactly replayed their references. No key was supplied to the optimizer. Long controls use existing original repository prose; the two short controls share a new fixed 87-character courier sentence.

| Control | Length | Correct recovered positions | Exact recovery |
| --- | ---: | ---: | --- |
| Long bijective | 496 | 496 | Yes |
| Matched-length bijective | 87 | 80 | No |
| Long homophonic | 470 | 470 | Yes |
| Matched-length homophonic | 87 | 34 | No |

The JSON records recovered and expected SHA-256 values. Longer controls have different budgets, so they establish implementation health rather than a matched performance guarantee. One short control per model is not an accuracy benchmark. Their failures prevent interpreting the target's failure as an exclusion of English or either entire cipher family.

The three bijective target outputs disagree at 41, 73 and 82 positions pairwise. The three relaxed outputs disagree at 5, 77 and 77 positions. The highest-scoring relaxed candidate merges ten cipher-symbol distinctions and contains frequent English fragments without establishing a coherent, sourced message. Its favorable score reflects a permissive fit, not verification. All witnesses remain unspaced in the JSON; no sentence, name or reading has been invented from them.

Bijective candidates independently re-encrypt to the entire normalized ciphertext. This verifies their transform consistency only. Homophonic decoders match every position, but exact forward replay needs explicitly recorded, ciphertext-derived homophone selectors. None matches the canonical round-robin encoder without those selectors. Such permissive replay is weaker than an independently established historical encoding rule.

No independent historical plaintext or key was acquired, so heldout historical accuracy is unavailable. A guessed phrase was not substituted for a reference. The unconstrained observed-map spaces are `26!/6!` for bijective substitution and `26^20` for the relaxed model; no exhaustive search or finite-keyspace exclusion is claimed. The result is a bounded failed recovery with visible ambiguity, not a solved cipher. Nr. 86 was excluded.

The next useful work is improving recovery and calibration on independently constructed short controls, plus acquiring separately checked glyph and Elgar evidence. Merely treating a higher English score as the answer would not resolve the missing verification.
