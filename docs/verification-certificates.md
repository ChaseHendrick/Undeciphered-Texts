# Verification certificates

Short note on the JSON certificates under `engine/data/*_certificate.json`.

## What they check

Each certificate records a **cipher or tool name**, the **known plaintext or gloss**, the **input** (ciphertext, sign, or phrase), an optional **source URL**, optional **keys**, and the **SHA-256** of the known text. The matching unit test loads that file, recomputes the hash, and decrypts or looks up the input so the recovered text matches.

These certificates check a **published worked example**, a **cited dictionary gloss**, or a **repository fixture**. They do **not** claim a reading of an unknown script. They do **not** claim a solution for Linear A, the Indus script, the Voynich manuscript, rongorongo, Kryptos K4, or army message Nr. 86.

## Existing original-method certificates

- `lumen_braid_certificate.json`, original lumen-braid method
- `prism_latch_certificate.json`, original prism-latch method

## Classical solvers with published or fixture examples

bifid, digrafid (ACA fractionation example), playfair, adfgvx, columnar (Kryptos K3), keyed Vigenère (Kryptos K1 and K2), caesar, vigenère, substitution, crib, beam-search, two-square (synthetic English only), ragbaby (ACA sheet, keyword GROSBEAK), grandpre (ACA sheet, first column LACQUERS), cadenus (ACA sheet, keyword EASY), trifid (Practical Cryptography cube, period 5; spaces are not in the hashed plaintext), turning grille (ACA sheet, stencil 1 8 10 12), fbi-letter-shift (FBI published one-letter right shift, Meet me at the park at noon), slidefair (ACA sheet, keyword DIGRAPH, Vigenere table), amsco (ACA sheet, key 41325, first cell a digraph; spaces are not in the hashed plaintext), myszkowski (ACA sheet, keyword BANANA), portax (ACA sheet, keyword EASY), cm bifid (ACA sheet, plaintext square EXTRAORDINARY clockwise spiral, ciphertext square NOVELTY alternating verticals, period 7; spaces are not in the hashed plaintext), seriated playfair (ACA sheet, keyword LOGARITHM, period 6; the vertical null X is in the hashed plaintext), rsa_broadcast (Boneh/Hastad e=3 broadcast, synthetic textbook-weak instance printed in the certificate).

## Lookups and readers with a cited known text

elder-futhark, ogham, Gardiner A1, Maya T544, ancient Greek ἄνθρωπος, cuneiform AN, Coptic ⲣⲱⲙⲉ, Egyptian jmn, Latin Gallia…, known-language-reader (Latin phrase), glyph-reader (planted labels), OCR (synthetic line).

`docs/assets/readme-hero.jpg` is not part of this change.
