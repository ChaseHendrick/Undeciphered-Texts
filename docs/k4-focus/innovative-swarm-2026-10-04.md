# K4 innovative swarm, 4 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

Two lanes that the earlier K4 runs did not cover. The composition finish was repeating, autokey, and Beaufort. The keyword panel called ordinary Gromark without a primer, so it never entered this model.

## Lane 1: Gromark digit obstruction

`engine.k4_gromark_obstruction`. The model is the repo's ACA Gromark: one cipher alphabet, and a running digit in 0..9. Cribs stay at the published plaintext indexes, EASTNORTHEAST at 21 and BERLINCLOCK at 63.

A ciphertext letter has one alphabet index. That index has to be `(plaintext index + digit) mod 26`. Two uses of the same letter are impossible when those 10-index sets do not meet. On K4 that happens for F, K, and P. No keyword and no 5-digit primer can place both cribs in situ.

A control encrypts a 97-letter text that really does contain both cribs under `KRYPTOS 12345`. That ciphertext is not blocked. The test fails if the obstruction fires on every string.

Myszkowski under `KRYPTOS`, `PALIMPSEST`, and `ABSCISSA` does not escape it. Putting that transposition on either side of in-place Gromark yields the same crib pairs, so it is one check, not two. All three keywords stay blocked:

| Keyword | Blocked letters | Pure Myszkowski crib hit |
| --- | --- | --- |
| KRYPTOS | K, P, U | no |
| PALIMPSEST | C, K, Q | no |
| ABSCISSA | K, O | no |

Periodic Gromark is not this digit bound. The keyword also rotates the alphabet, and the primer is the rank digits of the keyword. The same three keywords decrypt K4 and place neither crib.

This does not rule out a different Gromark convention, a digit alphabet larger than 0..9, or a transposition outside these three keywords.

## Lane 2: Quagmire settings

`engine.k4_quagmire_panel`. Keywords are only `KRYPTOS`, `PALIMPSEST`, and `ABSCISSA`. Indicators are those keywords or one letter A-Z (29 indicators). The indicator column is every letter A-Z. Types I, II, and III use one keyword. Type IV uses the six ordered pairs of different keywords.

| Type | Decrypts | Rejected | Crib hits |
| --- | ---: | ---: | ---: |
| I | 2262 | 0 | 0 |
| II | 2262 | 0 | 0 |
| III | 2262 | 0 | 0 |
| IV | 4524 | 0 | 0 |
| all | 11310 | 0 | 0 |

The whole panel took under a second. No unverified plaintext was stored.

## What remains open

Other transpositions, a Gromark variant whose shift is not a single digit 0..9, and Quagmire indicators outside this keyword-or-letter set are not covered. A blocked model is not a reading of K4.
