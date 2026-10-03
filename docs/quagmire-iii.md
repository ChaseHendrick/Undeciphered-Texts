# Quagmire III

The [ACA Quagmire III sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIII.pdf) uses one keyed alphabet for both plaintext and ciphertext. A repeating indicator rotates the ciphertext rows under a selected plaintext letter. The implementation reuses the existing Quagmire IV mapping with equal plaintext and ciphertext keywords.

The sheet's example uses keyword `AUTOMOBILE`, indicator `HIGHWAY`, and indicator column `A`, with period 7. Its printed ciphertext is:

```text
KRSLW MITJD VIABM RGQMT MLLIV IFUIX RHTNY ONVRH HIIIR MCAOV EI
```

The recovered sentence is "The same keyed alphabet is used for plain and cipher alphabets." The certificate hashes its uppercase A-Z stream. Spaces and punctuation are dropped; no padding is added.

`engine/solvers/quagmire_iii.py` exposes encryption, decryption, and `solve_quagmire_iii` with supplied `keyword`, `indicator`, and `indicator_under` arguments. The helper accepts lowercase ASCII letters, drops keyword repeats, and retains indicator repeats. It rejects empty letter streams, non-ASCII letters, and an indicator column with multiple letters.

`tests/test_quagmire_iii.py` checks the printed rows, independent plaintext and ciphertext, general keys, and the recovered plaintext hash in `engine/data/quagmire_iii_certificate.json`. The PDF was downloaded and visually inspected on 2026-10-03; its SHA-256 is recorded in that certificate.

This is known-key classical cipher recovery. It does not search for unknown keys or claim a reading of an unknown script or a solution of Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
