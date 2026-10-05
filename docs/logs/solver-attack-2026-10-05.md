# Solver pentest, 5 October 2026

Training prose only. No plaintext is stored. Nothing here is promoted as a higher score.

Caesar search is exact on 8 of 8. Lower case, one deleted letter, and one inserted letter all keep the shift. Reversal keeps the shift too, because Caesar changes each letter on its own. That is not evidence the solver undid an attack.

Vigenere search is exact on 6 of 6, including lower case. Deleting one letter keeps the keyword 0 of 6 times. A rule that required the keyword to survive that deletion would also drop the true keywords, so the rule stays off. Caesar search on a Vigenere text is exact 0 of 4 times.

Beaufort with the supplied key is exact on 6 of 6. Affine with the supplied key is exact on 4 of 4, and the published 5, 8 example still round-trips. A wrong key is exact 0 times on both. The wrong key still re-encrypts, because decrypting and encrypting with one key rebuilds the ciphertext. The judge cannot see a wrong key that way.

Substitution search on two windows of 240 letters is consistent on 2 of 2 and exact on 0 of 2. The order flag was open on both misses. The flag is not a recovery. Empty input, digits, and a four-letter Vigenere probe are rejected, 3 of 3.

A forward match is not a historical decipherment.
