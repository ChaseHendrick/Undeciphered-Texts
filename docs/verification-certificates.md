# Verification certificates

Short note on the JSON certificates under `engine/data/*_certificate.json`.

## What they check

Each certificate records a **cipher or tool name**, the **known plaintext or gloss**, the **input** (ciphertext, sign, or phrase), an optional **source URL**, optional **keys**, and the **SHA-256** of the known text. The matching unit test loads that file, recomputes the hash, and decrypts or looks up the input so the recovered text matches.

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

## Lookups and readers with a cited known text

elder-futhark, ogham, Gardiner A1, Maya T544, ancient Greek ἄνθρωπος, cuneiform AN, Coptic ⲣⲱⲙⲉ, Egyptian jmn, Latin Gallia…, known-language-reader (Latin phrase), glyph-reader (planted labels), OCR (synthetic line).

`docs/assets/readme-hero.jpg` is not part of this change.
