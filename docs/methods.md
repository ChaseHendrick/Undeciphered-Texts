# Methods: how amateurs actually make progress

## 1. Transcription first
Garbage in, garbage out. Prefer high-resolution color scans. Record uncertain glyphs explicitly (do not silently guess). DECRYPT transcription guidelines exist for historical ciphers.

## 2. Cipher type triage
- **IC ≈ 0.066** (English-ish): monoalphabetic / plaintext-like.
- **IC ≈ 0.038–0.045**: polyalphabetic (e.g. Vigenère) or random/OTP-like.
- Repeating periods → Kasiski / IC-by-period → Vigenère family.
- Many homophones / number codes → nomenclator / homophonic (CrypTool, hill-climb).
- Flat random + 5-letter groups → codebook / OTP suspicion (pigeon case).

## 3. Frequency & n-grams
Match ciphertext symbol frequencies to language models (HistCorp for historical orthography). Bigrams/trigrams/quadgrams score candidate plaintexts during search.

## 4. Cribs & siblings
Known names, dates, places, military formula (“AN DIE…”, signatures), or a related broken message supply cribs. Crib-dragging recovers key stream fragments for Vigenère/Enigma-style systems.

## 5. Bilinguals & anchors (ancient scripts)
Names of rulers, toponyms, number systems, and true bilinguals are why Egyptian and later Maya yielded. Without them, computational search underdetermines readings.

## 6. Search algorithms (classical)
- Exhaustive (Caesar).
- IC + per-column Caesar (Vigenère).
- Simulated annealing / hill-climb / beam search (substitution, homophonic).
- Wordlists and language models re-score candidates.

## 7. Image catalogs & paleography
For undeciphered *scripts*, inventory signs, allographs, and ligatures before phonetics. SigLA / kohaumotu-style databases are the contribution layer.

## 8. Validation culture
Publish ciphertext, key, plaintext, method, and seed. Get specialist confirmation (archive owner, Weierud, DECRYPT peers, epigraphers). Viral posts are not peer review.

## 9. What this repo’s engine implements
See [`engine.md`](engine.md). Use it to practice classical attacks and to score Latin-script ciphertexts—not to “read” Linear A.
