# Reverse-engineering check, 2026-10-03

Engine result inside declared bounds. No plaintext claimed.

The new `engine/reverse_engineer.py` was run on the unchanged ciphertext and aligned cribs imported from `engine/solvers/k4_attempt.py`. That module records the source of the transcription. No ciphertext errors or shifted crib alignments were introduced.

- Ciphertext: 97 A-Z letters, SHA-256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.
- Known positions: 24, from EAST, NORTHEAST, BERLIN, and CLOCK at the recorded offsets.
- Tested families: Caesar/invertible affine (312 parameter pairs), one-to-one monoalphabetic substitution, Vigenere and Beaufort with periods 1 through 16.
- Compatible hypotheses: 0 in each tested family.
- `claimed_plaintext`: null.

The [reverse-engineering note](../reverse-engineering.md) explains the model constraints. This is an exact consistency check of these elementary models, not a test of all possible ciphers. It does not cover keyed alphabets, transpositions, compositions, ciphertext errors, or other alignments. It does not solve K4. The older [K4 search](../k4-attempt.md) and [error-model search](../k4-error-model.md) retain their own bounds and results. Nr. 86 was not searched.
