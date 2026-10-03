# Sign-mapping unicity bound

New files only: `engine/sign_mapping_bound.py`, `tests/test_sign_mapping_bound.py`, and this note. No solver, image, or other module is changed.

## What it does not do

This is a **bound, not a decipherment**. It does not read Linear A, the Indus script, the Voynich manuscript, Rongorongo, or any other ancient writing. It does not propose a sign list, a phonetic value, or a translation. A verdict of `possibly determined` is not a solution.

## What it computes

The named bound is Shannon's **unicity distance** for a random simple substitution (a uniformly random bijection on the alphabet):

```text
U = H(K) / D
H(K) = log2(alphabet_size!)
D = log2(alphabet_size) - entropy_bits_per_symbol
```

`entropy_bits_per_symbol` is a language-model entropy **you state**. The function does not estimate it from the text. `U` is a lower bound, in symbols, on the corpus length at which that model expects the key equivocation to fall away. The ratio is the one in C. E. Shannon, "Communication Theory of Secrecy Systems," *Bell System Technical Journal* 28(4): 656-715, 1949:

https://www.cs.virginia.edu/~evans/greatworks/shannon1949.pdf

Shannon's summary uses a decimal log: for English simple substitution he takes H(K) = log10(26!) as about 20 and D as about 0.7 decimal digits per letter, and concludes unicity at about 30 letters. This module uses bits. The quotient is the same in any base. If the stated entropy is at least log2(alphabet size), redundancy is not positive, U is infinite, and the verdict stays `underdetermined` (Shannon's ideal system: no finite corpus pins down a unique key).

Verdicts:

- `underdetermined` when the text is strictly shorter than U
- `possibly determined` when the text meets or exceeds U

`possibly determined` means only that the stated model no longer predicts a crowd of keys. It does not exhibit a mapping, and it does not say the mapping is the historically correct one.

## Tests

`tests/test_sign_mapping_bound.py` states an entropy of 1.0 bit per symbol.

- A text of 5 signs over an alphabet of 20 is `underdetermined`. Even with zero entropy the same alphabet still needs about 14 symbols, because log2(20!) / log2(20) is about 14, so 5 signs cannot uniquely fix a bijection.
- A long English-length text, 50,000 letters over 26 signs, at the same stated entropy, is `possibly determined`. Shannon's own English figure is on the order of 30 letters, so the pass is the length, not a claim that a script was read.

Passing the tests means the inequality matches that model. It does not mean Linear A or Indus was deciphered.
