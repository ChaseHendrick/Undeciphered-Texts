# Quagmire I with known keys

`engine/solvers/quagmire_i.py` encrypts and decrypts Quagmire I when its plaintext keyword, indicator, and indicator column are supplied. It shares the alphabet rotation with Quagmire IV. Quagmire I uses a keyed plaintext alphabet and a straight ciphertext alphabet.

Source: [American Cryptogram Association Quagmire I sheet, page 71](https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf), fetched and visually checked on 2026-10-03. The fetched PDF has SHA-256 `d210a34ebd3cb614cb16861c15218ead70fbe44b6b4658cbf990c0662628eb70`.

| Field | Printed example |
| --- | --- |
| Plaintext keyword | `SPRINGFEV(ER)`; the repeated E and R do not enter the alphabet twice |
| Plaintext alphabet | `SPRINGFEVABCDHJKLMOQTUWXYZ` |
| Ciphertext alphabet | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` |
| Indicator | `FLOWER`, period 6 |
| Indicator column | Under plaintext `A`, column 10 in the mixed alphabet |

The indicator rotates each ciphertext row so its letter sits under plaintext A. The first plaintext letter T uses the FLOWER row for F and becomes Q. The next letter H uses the row for L and becomes P. This repeats after six letters.

The sheet's sentence is:

```text
The Quag One is a periodic cipher with a keyed plain alphabet
run against a straight cipher alphabet.
```

Its printed ciphertext is:

```text
QPMGQ RBUJU YIFDM PYAIF QYYJJ JHJYC JLUUT PIDVW YMFSG AESDW HIZRB
LIRVC FCZPE LBPZY YJJJH WLJJL PUP.
```

Spaces and punctuation are dropped. The stored plaintext contains 83 uppercase letters. The incomplete final period is left short, with no filler.

```python
from engine.solvers.quagmire_i import solve_quagmire_i

result = solve_quagmire_i(
    ciphertext,
    plaintext_keyword="SPRINGFEVER",
    indicator="FLOWER",
    indicator_under="A",
)
print(result.plaintext)
```

`quagmire_i_encrypt` and `quagmire_i_decrypt` take the same key arguments. Letter inputs use A-Z; letters outside that alphabet raise `ValueError`. Repeated keyword letters are removed when building the alphabet, while repeated indicator letters are retained in its period.

`tests/test_quagmire_i.py` checks both directions against the printed example. It loads `engine/data/quagmire_i_certificate.json`, decrypts the recorded ciphertext, and compares the recovered plaintext's SHA-256 with the certificate. It also checks other indicator columns, incomplete periods, invalid inputs, and an independent Vigenere vector when both alphabets are straight. See [verification-certificates.md](verification-certificates.md).

This is a known-key classical cipher helper. It does not search for unknown keys, and it is not registered in the text-only `SOLVERS` CLI. It makes no claim about an unknown script, Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
