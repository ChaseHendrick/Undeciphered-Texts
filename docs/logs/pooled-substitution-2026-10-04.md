# Pooled substitution, 4 October 2026

Not solved. No plaintext is stored.

The research note for Bob cited a substitution model that pools every copy of a symbol and then forces a one-to-one key. `engine/pooled_substitution.py` is that constraint and nothing else. It is not a Transformer, and it is not part of Bob. Eighty was too small a polish, so each key gets 200 random swaps. A swap is kept only when the quadgram score rises. The bijective swap exchanges two letters. The colliding swap is allowed to point two ciphertext letters at one plaintext letter.

On a 240-letter English passage under a random permutation, the bijective key stays a permutation, re-encrypts to the ciphertext, and matches more than a quarter of the letters. The colliding key uses fewer than 26 images. It can look more accurate only by pointing several ciphertext letters at E. That is not a substitution key.

The same polish was run on IASRZ Nr. 129 and on K4, in English and in the Grimm letter model. The control is the same polish on a shuffle of that ciphertext. Scores are quadgram sums. Higher is closer to the sample. None of these is a reading.

| Text | Model | Bijective | Colliding | Shuffled control | Bijective beats the shuffle |
| --- | --- | ---: | ---: | ---: | --- |
| IASRZ 129 | English | -279.57 | -230.38 | -281.94 | yes |
| IASRZ 129 | Grimm | -274.61 | -230.13 | -282.24 | yes |
| K4 | English | -309.35 | -280.05 | -310.45 | yes |
| K4 | Grimm | -313.26 | -252.16 | -312.49 | no |

On every row the colliding key scores higher than the legal one-to-one key. The small gains over a shuffle are the same kind of gain a collapsed alphabet gets for free. K4 under the Grimm model does not beat its shuffle at all. Simple substitution is not supported for either text.

`solved` stays false and `claimed_plaintext` stays null.
