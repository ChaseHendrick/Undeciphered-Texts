# Sourced solver expansion, 3 October 2026

This continuation adds thirteen ACA classical helpers and one public-parameter RSA attack, then connects bounded searches through an explicit tool registry and investigation ledger. Published definitions, supplied-key decoding, conditional unknown-key inference and synthetic neural family classification are separate claims. No new historical plaintext is verified by this work.

## Sources and implementations

The thirteen ACA additions are Baconian, Condi, Progressive Key, Periodic Gromark, Monome-Dinome, Morbit, Pollux, Numbered Key, Redefence, Sequence Transposition, Checkerboard, Homophonic and Interrupted Key. Each has a module under `engine/solvers`, a focused test file, a JSON certificate and an individual note. The independent printed diagrams and ciphertexts were fetched and visually inspected on 2026-10-03. Sources and representation details are indexed in [verification-certificates.md](../verification-certificates.md).

Important source boundaries:

- Progressive Key's sheet supplies only 30 aligned plaintext letters despite printing 40 ciphertext letters. Its certificate covers that prefix only.
- Baconian's second textual carrier supplies eleven printed plaintext letters. Its continuation is not invented; the explicit 26-letter variant has synthetic controls rather than attribution to that ACA example.
- Morbit and Pollux recover spaces encoded in the Morse stream. A terminal display period does not become plaintext punctuation when no period code was printed.
- Periodic Gromark supports keywords with 2 through 9 distinct letters. Its primer and last-digit checks detect some framing errors, not authentication.
- Monome-Dinome and Baconian disclose merged letters and lost word spaces. Numbered Key retains repeated keyword letters because they create different valid homophones.
- RSA Wiener uses [the original paper's Section V weak key](https://www.jannaud.fr/static/download/Travail/wiener.pdf#page=4). The two-byte message `00 41` and ciphertext 1511 are constructed controls with that key. Public parameters enter recovery; factors and the private exponent do not. The certificate hashes actual recovered bytes.

## Unknown-key and composed tools

Condi inference searches a caller-supplied keyword list, alphabet shifts and initial offsets under a check cap. Progressive Key inference fits periods, progressions and key slots to aligned cribs, leaving unresolved slots explicit. Their unknown-key controls are constructed independent fixtures and are separate from the published supplied-key certificates.

Homophonic tests the 25 possible key shifts in each of four independent numeric rows. Five aligned letters in the printed control determine GOLF and predict seventeen further letters; three aligned letters leave `GO??` and 625 compatible keys. Interrupted Key infers ORANGE from six aligned letters with a supplied reset pattern and predicts 34 other letters. Both are conditional unknown-key controls, not unknown-family or arbitrary-pattern decipherment.

The additional plaintext-autokey inference tool tests bounded primer lengths, propagates aligned plaintext equations exactly and retains one unigram-selected example per compatible length for quadgram ranking. A blind 423-letter synthetic control recovers its literal paragraph without a supplied primer; a separate primary university vector tests exact propagation from one crib letter. Exact compatible seed counts and consensus cover all seeds within the tested lengths; displayed score-ranked examples do not constitute exhaustive quadgram search. Its feature API receives only ciphertext and caller training tables and is independently checked in both NumPy and standard-library implementations.

The Morse constraint tool enumerates Morbit and Pollux maps fairly under a shared map/time budget, with strict parsing and caller-supplied lexicon or aligned decoded-text evidence. It reports map ambiguity separately from plaintext ambiguity, retaining null conclusions when incomplete. The published Morbit control uses a deliberately strong four-word lexicon, no supplied key, and full `9!` map enumeration. Morse coordinates count recovered spaces and punctuation.

The transposition portfolio alternates rail-fence, the existing route, limited right-to-left columnar settings and Redefence hypotheses. Each tested inverse is checked against its forward transform. Candidates deduplicate by plaintext while retaining bounded equivalent-key examples. Completion is relative to requested models; scores and reencryption do not identify the actual family or verify a historical answer.

The registry exposes allowlisted helpers with modes, required parameters, JSON validation, typed cribs and binary encodings. The investigation ledger combines bounded hypotheses, transform checks, contradictions, advisory neural rankings and concrete next actions. Unknown correctness remains unknown. Simulated control states and reward metrics describe program behavior, not emotion or consciousness.

## Neural training and evaluation

The saved format 5 residual router has 20 output families, 142 features and three 96-unit networks. Its training uses supervised label smoothing, a curriculum based on training errors and paired-dropout consistency. Disjoint Austen slices provide fitting, checkpoint selection and calibration. Doyle is excluded from gradient updates, but reused Doyle scores are now development comparisons. Recursive certificate-text exclusion covers nested complete expected/predicted text as well as plaintext and known-text fields.

| Evaluation | Correct | Scope |
| --- | --- | --- |
| Fixed 20-family top one | 428/480, 89.17% | 24 generated cases per family |
| Fixed 20-family top three | 477/480, 99.38% | Three family suggestions, not plaintexts |
| Exact earlier 17-family benchmark | 193/204 | Same original ciphertexts; original checkpoint scored 158/204 |
| Format 5 Wells audit top one | 429/480, 89.38% | Previously unused prose and fresh synthetic keys after the earlier selection stage |
| Format 5 Wells audit top three | 476/480, 99.17% | Same hashed format 5 artifact, no refitting or recalibration for that audit |

The accepted format 5 run used 250 epochs and 256 training examples per family and took 101.965 local seconds. An independent direct-matrix replay confirms all three fixed counts. The original neural weights are preserved.

Larger candidates were rejected. Format 6 tied 428/480 but regressed to 189/204; the original gate only compared the earlier benchmark against the initial baseline and allowed that regression. The gate was corrected to replay and protect the incumbent on both fixed comparisons, its regression test was added, and format 5 was restored. A validation-selected five-network blend scored 434/480 but 192/204 and was rejected. Format 7 added six conditional M209 measurements and scored 431/480 but 187/204; it was also rejected. A prior expanded 23-class trial regressed on the identical earlier 480 cases and was rejected. No rejected candidate is the shipped model.

The Wells audit is source-hashed and replayable in `engine/data/neural_router_v2_audit.json` with corpus and provenance beside it. It followed the earlier selection stage and remains specific to format 5 SHA `d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825`. All 48-letter overlap windows against Austen and Doyle and complete certificate text were checked. Later authorized training stages excluded Wells from fitting and selection, so this is not a globally untouched final audit claim. Its scope is the disclosed synthetic generators, with Enigma and M209 the weakest classes. Neither accuracy nor family confidence verifies a historical decipherment. The requested 480/480 remains unmet, with 52 fixed top-one errors in the saved model.

Source format 8 uses the exact format 5 prefix of 142 features plus six conditional M209 values, for 148 features. Formats 2 through 8 remain loadable. The first warm trial used rate 0.01, 256 cases per family, 250 epochs and three 96-unit members. It scored 433/480 top one, 477/480 top three and 191/204 legacy in 101.727 local seconds. Checkpoints were 55,45,0. The promotion gate rejected the two added legacy errors, leaving the shipped format 5 SHA unchanged. Its rejected candidate serialization was 1,598,673 bytes with SHA `e16275216d982d3dc2d74b5089d2b8599943d58da72fc071ffdaf9b204f62be3`. `--warm-start` and `--learning-rate` now expose compatible initialization and a bounded schedule rate; checkpoint 0 protects against worse Austen validation choices, while both reused Doyle gates still decide promotion.

A later authorized conservative warm trial used the same sample count, epochs and architecture with rate 0.0003. It scored 432/480 top one, 476/480 top three and 191/204 legacy in 91.310 local seconds, with checkpoints 75,95,15. It was rejected without retuning; neither warm trial evaluated Wells. Its 1,611,059-byte candidate SHA was `fd35a67bf2702cbc3631fb84a447c1986a81181a34e128db3fb04bad702f44b0`. The shipped model remains format 5 with the previously recorded SHA and benchmark counts.

Serialization is bounded to 4 MiB before replacement and preserves a loadable incumbent. Custom artifact paths use distinct metrics siblings. Invalid floating-point values and malformed parameter dimensions are rejected. Independent central finite differences checked 460 objective/network derivatives with maximum absolute error `1.91e-10`. See [neural-upgrades.md](../neural-upgrades.md) for feature versions, every experimental count, the independent audit and reproducibility commands.

## Executed checks

Focused commands are in [TESTING.md](../TESTING.md). New module tests first failed on missing imports before implementation. The Periodic Gromark large-frame regression failed before separate raw-frame and normalized-body limits fixed the mismatch. The two-view objective regression failed at the old 10,000-row limit before raising only that limit to 20,000; cell and pair caps remain 1,000,000 and 10,000.

- Baconian, Condi, Progressive Key and Periodic Gromark: 28 focused tests passed after the frame fix.
- Neural objective utilities: 9 focused tests passed in 0.054 seconds after the row-limit fix.
- Checkerboard and Homophonic: 16 focused tests passed in 0.008 seconds after their missing-import failures.
- Independent modular controls matched 100 random fixtures each for Condi, Progressive Key and Periodic Gromark, plus 100 sparse Progressive Key inference cases and all 50 valid Baconian codes across the two variants.
- Independent coordinate-path and cyclic-table oracles matched 100 random Checkerboard controls and 100 random Homophonic encryption/decryption/inference controls, including sparse key-row evidence.
- A peer audit independently checked both source diagrams and PDF hashes, 150 random Checkerboard homophone controls, 150 Homophonic controls with exact row options/counts/predictions, and 150 short-budget reports. Printed five-character Checkerboard display groups also decoded correctly; no actionable issue was found.

The integrated local discovery run passed 943 tests with no skips in 34.131 seconds on Python 3.12.14 before the final custom-artifact regression was added. The final stable run and remote CI are recorded separately below. Focused passes above do not substitute for full discovery.

The final stable local discovery passed 1,061 tests with no skips in 41.843 seconds using `.venv/bin/python` and `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`. A separate temporary demo recovered all three fixture plaintexts exactly in 4.309 seconds with no failures. These runs cover the current source, including V8 warm-start and learning-rate controls; they do not rerun the Wells audit or establish a new historical decipherment. Four changed source/test files also passed Python 3.10 grammar parsing. The broader repository grammar, JSON and diff checks passed separately. These are local results, not a CI result for the commit being published.

The [Bob research plan](../bob-research-2026-10-03.md) records primary-source ideas for broader generators and constrained decipherment. It is a proposed next stage, not another model trial or promoted artifact.

The README hero JPEG is outside this change. No model result, candidate rank or certificate here claims an unknown script, Kryptos K4, army message Nr. 86, general RSA or production cryptography has been solved.
