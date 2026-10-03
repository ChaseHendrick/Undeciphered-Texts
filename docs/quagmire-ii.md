# Quagmire II

`engine/solvers/quagmire_ii.py` encrypts and decrypts classical Quagmire II when the ciphertext keyword, indicator, and indicator column are supplied. `solve_quagmire_ii` wraps that decryption in a `SolveResult`. It does not search for unknown keys.

The [American Cryptogram Association Quagmire II sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireII.pdf) defines its K2 keyword plan: the plaintext alphabet is straight A-Z and the ciphertext alphabet is keyed. Drop repeated keyword letters, then append unused A-Z letters in alphabetical order. The indicator specifies the period. Rotate each ciphertext row so its indicator letter appears beneath the chosen plaintext letter, and use those rows in sequence. The implementation uses the existing Quagmire IV transformation with a straight plaintext alphabet.

The PDF was fetched and visually checked on 2026-10-03. Its SHA-256 was `9a732261fe24ef967df09f8eda892e10c7f340383f542958cf33189f53e51fbc`.

## Published example

The sheet prints the keyword as `SPRINGFEV(ER)`. E and R repeat earlier letters, giving ciphertext alphabet `SPRINGFEVABCDHJKLMOQTUWXYZ`. The indicator is `FLOWER` under plaintext `A`, period 6.

The printed plaintext is:

```text
In the Quag Two a straight plain alphabet is run against a keyed cipher alphabet.
```

The printed ciphertext is:

```text
JICIC OSLYK ILFVC HEBDX CCORJ IOEWA FMWKK TXBGW HRJIB KEDBJ WZABU
XWHEH UXOXC U.
```

The certificate stores each as an uppercase A-Z stream. Spaces, grouping, and the final full stops are omitted. The plaintext has 66 letters. Its SHA-256 is `becf36055e08f7d2235b822c7747b00db755c3314592c32e57cd1222a9122c24`.

## Use and validation

```python
from engine.solvers.quagmire_ii import ACA_CIPHER, solve_quagmire_ii

result = solve_quagmire_ii(
    ACA_CIPHER,
    ciphertext_keyword="SPRINGFEVER",
    indicator="FLOWER",
    indicator_under="A",
)
print(result.plaintext)
```

Inputs accept lowercase A-Z and ignore non-letter separators. Non-ASCII letters and empty letter streams raise an error. The indicator keeps repeated letters, and any A-Z plaintext column is supported. A final short period group receives no padding.

`tests/test_quagmire_ii.py` compares decryption and encryption with the independent printed vector, checks the recovered plaintext against `engine/data/quagmire_ii_certificate.json` and its SHA-256, and covers another keyword, repeated indicator letters, another column, a short final group, and invalid input. The test file failed with a missing-module import before the solver was added. Run the focused checks with Python 3.10 or newer:

```bash
python3 -m unittest tests.test_quagmire_ii -v
```

The helper requires keys, so it is not in the keyless `SOLVERS` dispatch. This certificate is a published classical worked example. It is not a reading of an unknown script or a solution for Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
