# Compression language score

`engine/compression_score.py` ranks a string by how redundant it looks to zlib.

- `language_score` is raw UTF-8 bytes divided by compressed bytes. Higher means more repeated structure.
- `cross_entropy_bits_per_byte` is `8 * compressed_bytes / raw_bytes`. Lower means the same thing.
- `compare_to_shuffle` scores a string against one seeded character permutation of itself.

A real English or German passage should score above a shuffle of its own characters, because words and letter patterns compress and a permutation does not. The unit test is `tests/test_compression_score.py`. It uses the existing prose fixtures. It does not add a cipher solver.

## What this is not

**This tool does not decipher ancient scripts.** It does not read Linear A, the Voynich manuscript, Rongorongo, the Indus script, Phaistos, or any other undeciphered writing system. Beating a shuffle only shows that the original string had compressible order. It is not a translation, not a language identification, and not evidence that an unknown text has been solved.

Dieses Werkzeug entziffert keine antiken Schriften, nur ein Kompressionsmaß.

The idea that compressors notice language-like redundancy is old and public (see Benedetto, Caglioti, and Loreto, “Language Trees and Zipping,” *Physical Review Letters* 88, 048702, 2002, https://doi.org/10.1103/PhysRevLett.88.048702). That paper sorts known languages. It is not a method for reading an undeciphered script, and neither is this module.
