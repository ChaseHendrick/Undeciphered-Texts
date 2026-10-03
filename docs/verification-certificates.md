# Verification certificates

Short note on the JSON certificates under `engine/data/*_certificate.json`.

## What they check

Certificates identify a **cipher or tool**, its **input and expected control**, optional **source URLs** and **keys**, and the **SHA-256** of the declared output. Schemas vary: some contain multiple vectors, binary values, conditional predictions or an expected chosen sentence. The matching test invokes the API and checks its actual output against the stored result and hash. Hash fields state their encoding and normalization; a hash alone does not establish independent provenance.

These certificates check a **published worked example**, a **cited dictionary gloss**, or a **repository fixture**. They do **not** claim a reading of an unknown script. They do **not** claim a solution for Linear A, the Indus script, the Voynich manuscript, rongorongo, Kryptos K4, or army message Nr. 86.

## Existing original-method certificates

- `lumen_braid_certificate.json`, original lumen-braid method
- `prism_latch_certificate.json`, original prism-latch method

## Classical solvers with published or fixture examples

bifid, digrafid (ACA fractionation example), playfair, adfgvx, columnar (Kryptos K3), keyed Vigenère (Kryptos K1 and K2), caesar, vigenère, substitution, crib, beam-search, two-square (synthetic English only), ragbaby (ACA sheet, keyword GROSBEAK), grandpre (ACA sheet, first column LACQUERS), cadenus (ACA sheet, keyword EASY), trifid (Practical Cryptography cube, period 5; spaces are not in the hashed plaintext), turning grille (ACA sheet, stencil 1 8 10 12), fbi-letter-shift (FBI published one-letter right shift, Meet me at the park at noon), slidefair (ACA sheet, keyword DIGRAPH, Vigenere table), amsco (ACA sheet, key 41325, first cell a digraph; spaces are not in the hashed plaintext), myszkowski (ACA sheet, keyword BANANA), portax (ACA sheet, keyword EASY), cm bifid (ACA sheet, plaintext square EXTRAORDINARY clockwise spiral, ciphertext square NOVELTY alternating verticals, period 7; spaces are not in the hashed plaintext), seriated playfair (ACA sheet, keyword LOGARITHM, period 6; the vertical null X is in the hashed plaintext), chaocipher (Programming Praxis 2010-07-06 known alphabets; left HXUCZVAMDSLKPEFJRIGTWOBNYQ, right PTLNBQDEOYSFAVZKGJRIHWXUMC; the published vector is the revealed algorithm, not Byrne's exhibits), quagmire IV (ACA sheet, plaintext keyword SENSORY, ciphertext keyword PERCEPTION, indicator EXTRA under plaintext S), nihilist transposition (ACA sheet, key 2134, column takeoff; spaces are not in the hashed plaintext), tri-square (ACA sheet, square 1 NOVELS vertical, square 2 READING horizontal, square 3 PASTIME clockwise spiral; the sheet prints the squares, not the keyword names; the final X is the even-length null on the sheet; spaces are not in the hashed plaintext), solitaire (Schneier Solitaire / Pontifex, passphrase CRYPTONOMICON, message SOLITAIRE with filler X included in the hashed plaintext SOLITAIREX), rsa_broadcast (Boneh/Hastad e=3 broadcast, synthetic textbook-weak instance printed in the certificate).

## Quagmire I, II, and III

The Quagmire family also includes these published examples, fetched and visually checked on 2026-10-03:

- `quagmire_i_certificate.json`: [ACA Quagmire I](https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf), plaintext keyword SPRINGFEVER, straight ciphertext alphabet, indicator FLOWER under plaintext A. See [quagmire-i.md](quagmire-i.md).
- `quagmire_ii_certificate.json`: [ACA Quagmire II](https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireII.pdf), straight plaintext alphabet, ciphertext keyword SPRINGFEVER, indicator FLOWER under plaintext A. See [quagmire-ii.md](quagmire-ii.md).
- `quagmire_iii_certificate.json`: [ACA Quagmire III](https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIII.pdf), keyword AUTOMOBILE for both alphabets, indicator HIGHWAY under plaintext A. See [quagmire-iii.md](quagmire-iii.md).

Each test decrypts the sheet's printed ciphertext with its published key and hashes the recovered uppercase plaintext. Spaces and punctuation are omitted. The source PDF hashes identify the sheets used. These are supplied-key checks, not unknown-key recovery.

## Modern and constraint examples

- `aes_certificate.json`: NIST FIPS 197 Appendix C vectors for all three AES key sizes. [aes.md](aes.md).
- `chacha20_certificate.json`: RFC 8439 block and stream vectors. [chacha20.md](chacha20.md).
- `rsa_fermat_certificate.json`: the Handbook of Applied Cryptography Example 8.4 plaintext integer, recovered from public parameters by bounded factoring. [rsa-fermat.md](rsa-fermat.md).
- `rsa_common_modulus_certificate.json`: a constructed same-message, shared-modulus fixture with coprime exponents. The cited source describes the weakness, not a historical solve. [rsa-common-modulus.md](rsa-common-modulus.md).
- `word_pattern_certificate.json`: the repository's substitution fixture and explicit lexicon with decoys, recovered without the key. [word-pattern.md](word-pattern.md).
- `reverse_engineer_certificate.json`: ACA Vigenere, using only a 28-letter crib to infer the model that predicts the remaining 19 letters. This is a tool certificate and is not a neural cipher-family class. [reverse-engineering.md](reverse-engineering.md).
- `cipher_synthesis_certificate.json`: a constructed reverse-layout plus affine fixture. SMT receives a short crib and must prove the remaining plaintext values, then hash that conditional prediction. The source describes the constraint engine, not a historical decipherment. [cipher-synthesis.md](cipher-synthesis.md).
- `puzzle_certificate.json`: two literal Sudoku grids and displayed answers from Peter Norvig's official article. Tests recover the completions, prove uniqueness within the search, check every clue and unit independently, and hash 81 solution digits. Puzzle fields are excluded from the language router. [puzzles.md](puzzles.md).

Binary certificates use `plaintext_hex` or `plaintext_integer` instead of language text. Their SHA-256 covers recovered raw bytes with the stated length and encoding, rather than the hexadecimal representation. They remain outside the language router's training exemplars.

## Sourced expansion on 2026-10-03

These thirteen classical helpers use independently printed ACA examples. Their certificates record the source sheet and hash recovered output; exact representation and losses are disclosed in each note.

| Certificate | Published evidence | Recovery mode |
| --- | --- | --- |
| `baconian_certificate.json` | [ACA Baconian](https://www.cryptogram.org/downloads/aca.info/ciphers/Baconian.pdf): word-initial carrier yields `SUCCESS`; letter carrier yields the printed eleven-letter `NOWISAGOODT` | Explicit extraction and 24-letter variant. Spaces are lost and I/J, U/V are merged. The 26-letter variant is a separate synthetic control. [Note](baconian.md). |
| `condi_certificate.json` | [ACA Condi](https://www.cryptogram.org/downloads/aca.info/ciphers/Condi.pdf): full 83-letter example, keyword STRANGE, alphabet shift 21 and initial offset 25 | Supplied key. A separate constructed fixture tests dictionary-and-crib inference without its keyword. [Note](condi.md). |
| `progressive_key_certificate.json` | [ACA Progressive Key](https://www.cryptogram.org/downloads/aca.info/ciphers/ProgressiveKey.pdf): GRAPEFRUIT and progression 1 | Supplied key for the 30-letter printed plaintext prefix. Ten further ciphertext letters have no printed aligned plaintext and are not certified. Separate synthetic cribs test unknown period, progression and key inference. [Note](progressive-key.md). |
| `periodic_gromark_certificate.json` | [ACA Periodic Gromark](https://www.cryptogram.org/downloads/aca.info/ciphers/PeriodicGromark.pdf): ENIGMA, derived primer 264351 and complete 64-letter example | Supplied keyword; primer and last digit are verified framing. [Note](periodic-gromark.md). |
| `monome_dinome_certificate.json` | [ACA Monome-Dinome](https://www.cryptogram.org/downloads/aca.info/ciphers/MonomeDinome.pdf): NOTARIES and digit order 6318927054 | Supplied box; hashes normalized letters with I/J and Y/Z merged. [Note](monome-dinome.md). |
| `morbit_certificate.json` | [ACA Morbit](https://www.cryptogram.org/downloads/aca.info/ciphers/Morbit.pdf): WISECRACK, ciphertext yielding `ONCE UPON A TIME` | Supplied ranked key. Hash includes recovered word spaces and excludes the unencoded prose period. [Note](morbit.md). |
| `pollux_certificate.json` | [ACA Pollux](https://www.cryptogram.org/downloads/aca.info/ciphers/Pollux.pdf): digit map yielding `LUCK HELPS` | Supplied map. Hash includes recovered word spaces; the printed terminal ciphertext period is framing. [Note](pollux.md). |
| `numbered_key_certificate.json` | [ACA Numbered Key](https://www.cryptogram.org/downloads/aca.info/ciphers/NumberedKey.pdf): phrase `I like ciphers.`, start 18 and literal homophonic codes | Supplied phrase and numbering rotation; repeated letters are retained. [Note](numbered-key.md). |
| `redefence_certificate.json` | [ACA Redefence](https://www.cryptogram.org/downloads/aca.info/ciphers/Redefence.pdf): row ranks 213, offset 0 and independently printed equivalent key | Supplied key for the published certificate; a different synthetic fixture tests blind bounded search. [Note](redefence.md). |
| `sequence_transposition_certificate.json` | [ACA Sequence Transposition](https://www.cryptogram.org/downloads/aca.info/ciphers/SequenceTransposition.pdf): GUMMYBEARS, primer 69315 and full frame ending in check 9 | Supplied keyword and primer; hashes recovered letters without inventing spaces. [Note](sequence-transposition.md). |
| `checkerboard_certificate.json` | [ACA Checkerboard](https://www.cryptogram.org/downloads/aca.info/ciphers/Checkerboard.pdf): simple and complex coordinates around the printed square | Supplied square and coordinate labels; both independently printed examples hash the same 33 recovered letters. [Note](checkerboard.md). |
| `homophonic_certificate.json` | [ACA Homophonic](https://www.cryptogram.org/downloads/aca.info/ciphers/Homophonic.pdf): GOLF and four cyclic numeric rows | Supplied keyword for the literal 22-code example. Separate inference receives only five aligned letters and predicts the other seventeen. Unobserved row keys remain unknown. [Note](homophonic.md). |
| `interrupted_key_certificate.json` | [ACA Interrupted Key](https://www.cryptogram.org/downloads/aca.info/ciphers/InterruptedKey.pdf): printed Vigenere key-stream diagram and ORANGE control | Certificate inference receives a supplied reset pattern, keyword length and six-letter crib, with no keyword. It predicts the remaining 34 letters and hashes those separately. No arbitrary reset-pattern search is claimed. [Note](interrupted-key.md). |

`rsa_wiener_certificate.json` is the fourteenth sourced cipher/attack addition in this batch. [Wiener's paper](https://www.jannaud.fr/static/download/Travail/wiener.pdf#page=4) publishes the weak key `n=8927`, `e=2621`, `d=5`, `p=79`, `q=113`. Message integer 65 and ciphertext 1511 are constructed controls using that key, not a published plaintext. Recovery receives public parameters only. The SHA-256 covers the recovered two bytes `00 41`, not their hexadecimal spelling. [Note](rsa-wiener.md).

The composed tools have separate evidence:

- `morse_constraints_certificate.json` tests the literal ACA Morbit ciphertext without its keyword or digit map, using an explicitly supplied four-word lexicon. Full enumeration establishes plaintext uniqueness within that strong lexicon and family assumption. It is not unrestricted English recovery. Its `tool_name` and tool-specific input fields prevent it from becoming another neural cipher-family label. [Note](morse-constraints.md).
- `transposition_ensemble_certificate.json` tests a constructed harbor-prose fixture without its key or plaintext. The published source describes Redefence; it does not publish this message. Hashing the recovered ranked candidate and matching its forward transform check the implementation, not historical correctness. Its `tool_name` keeps a portfolio separate from cipher-family classes. [Note](transposition-ensemble.md).
- `autokey_inference_certificate.json` freezes an original 423-letter constructed paragraph and ciphertext. Blind primer inference receives neither key nor plaintext and ranks the exact recovered control first. A separate primary university example tests exact crib propagation. Unigram-optimal column seeds and quadgram-ranked period examples do not exhaust all possible primers; conditional forced letters are distinguished from scored examples. Its tool fields keep it outside neural cipher-family labels. [Note](autokey-inference.md).
- `enigma_crib_search_certificate.json` recovers a three-letter start from a constructed independent rotor-table fixture with one missing cipher slot. Rotor order, rings, reflector, plugboard and eight crib letters are supplied; the start is withheld. Its recovered hash includes the preserved unknown slot. A separate existing published vector is also replayed. It is conditional starting-position recovery, not a general Enigma key break. [Note](enigma-crib-search.md).
- `hill_inference_certificate.json` recovers the 2 by 2 matrix for the printed `HELP -> HIAT` example in [Slinko's University of Auckland slides](https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf) from its full plaintext crib, without a supplied matrix. A separate original 28-letter vector receives seven aligned letters and predicts the other 21, retaining its terminal X. Completed enumeration determines conditional key and plaintext consensus; incomplete prefixes cannot do so. Its `tool_name` keeps matrix inference outside neural family-label discovery. [Note](hill-inference.md).
- `solver_reasoning_certificate.json` hashes the recovered top Caesar fixture from the bounded investigation ledger. This is a constructed control with no supplied shift, not a historical message. Its `tool_name` keeps investigative orchestration separate from cipher-family labels. [Note](solver-reasoning.md).

Condi and Progressive Key inference certificates similarly label their synthetic unknown-key fixtures separately from the published known-key examples. Search completion, candidate uniqueness under supplied assumptions, English scores and reencryption are different claims. An unresolved case requires independent heldout evidence or an independently cited exact plaintext before historical verification; workflow runs do not automatically mark it solved.

Neural weights and metrics are model artifacts, not plaintext certificates. Their known labels are generated cipher families. Evaluation reports the trained class list, prose splits, fixed benchmark comparisons and promotion gates, with no claim that all catalog tools have trained classes. The accepted format 5 Bob artifact reports 428/480 top one and 477/480 top three on reused Doyle development cases, and 193/204 on the exact earlier benchmark. These are family labels, not recovered messages, and do not describe an unfinished later training trial. A scalar correctness/speed reward cannot replace the gates or verify an unknown answer. See [neural-upgrades.md](neural-upgrades.md) and the [dated expansion log](logs/solver-expansion-2026-10-03.md).

## Ten persona solver controls

These certificates identify investigator APIs with `tool_name` fields. They
remain outside neural cipher-family discovery. Their expected keys and full
plaintexts are validation fields, not hidden investigator inputs. Explicit
cribs, dictionaries, keyword guesses and review references are disclosed.

| Certificate | Actual control and evidence scope |
| --- | --- |
| `persona_emperor_solver_certificate.json` | Literal constructed Caesar and rail-fence messages recovered without supplied keys or cribs; both recovered outputs are hashed. [Note](persona-emperor-solver.md). |
| `persona_inheritance_solver_certificate.json` | Constructed word-pattern, Vigenere, plaintext-autokey and Condi vectors with explicit lexicons, keyword lists or aligned cribs. Tests distinguish selected-key inference and predictions beyond cribs from unrestricted recovery. [Note](persona-inheritance-solver.md). |
| `persona_hallucinogens_solver_certificate.json` | Constructed affine-then-reversal ciphertext recovered without a key or crib; the recovered hash and inverse-composition replay are checked. This is repository composition, not a new historical method or solve. [Note](persona-hallucinogens-solver.md). |
| `persona_pacifist_solver_certificate.json` | Two independently printed affine examples recovered by enumerating 312 keys with sparse supplied cribs. Expected keys and independently recovered-output hashes check conditional inference. [Note](persona-pacifist-solver.md). |
| `persona_detective_solver_certificate.json` | Literal constructed Vigenere vector with an unplaced phrase; neither selected key nor phrase offset is supplied. The fitted phrase is not independent verification. [Note](persona-detective-solver.md). |
| `persona_cartographer_solver_certificate.json` | Constructed harbor-prose transposition control recovered without its key, using the existing bounded portfolio. Ranked recovery and forward replay do not authenticate unknown text. [Note](persona-cartographer-solver.md). |
| `persona_mechanic_solver_certificate.json` | Constructed Progressive Key, autokey and Hill controls with aligned cribs and no selected key, progression or matrix. Actual recovered full outputs are hashed. [Note](persona-mechanic-solver.md). |
| `persona_normal_man_solver_certificate.json` | Literal Caesar and rail-fence controls for the finite 32-trial baseline, with no selected key supplied. Plain-language narration changes neither evidence nor verification status. [Note](persona-normal-man-solver.md). |
| `persona_adversary_solver_certificate.json` | Constructed recovery and alternative witnesses under the same declared evidence. Competitor searches do not prove uniqueness across all ciphers. [Note](persona-adversary-solver.md). |
| `persona_skeptic_solver_certificate.json` | Constructed recovery followed by disjoint reserved-crib and declared-hash comparisons. Reserved references are excluded from generation, and matching them does not authenticate their provenance. [Note](persona-skeptic-solver.md). |

Council integration has separate tests for shared budgets, one common language
score, lazy selected loading and reserved-evidence separation. Repeated support
for a plaintext is not another independent certificate or a solved status.
The earlier persona preference certificates still check chosen sentences;
they are not retroactively upgraded into ciphertext recoveries.

## Lookups and readers with a cited known text

elder-futhark, ogham, Gardiner A1, Maya T544, ancient Greek ἄνθρωπος, cuneiform AN, Coptic ⲣⲱⲙⲉ, Egyptian jmn, Latin Gallia…, known-language-reader (Latin phrase), glyph-reader (planted labels), OCR (synthetic line).

`docs/assets/readme-hero.jpg` is not part of this change.
