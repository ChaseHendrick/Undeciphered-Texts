# Nihilist cipher (known-key solver)

`engine/solvers/nihilist.py` decrypts a **known** square keyword and additive keyword. `tests/test_nihilist.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Wikipedia: Nihilist cipher](https://en.wikipedia.org/wiki/Nihilist_cipher) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Square keyword | `ZEBRAS` |
| Additive keyword | `RUSSIAN` |
| Key | `ZEBRAS RUSSIAN` |
| Plaintext | `DYNAMITEWINTERPALACE` |
| Ciphertext | `37 106 62 36 67 47 86 26 104 53 62 77 27 55 57 66 55 36 54 27` |

The page writes "DYNAMITE WINTER PALACE". Spaces are not part of the ciphertext. The letter stream above is what the published coordinates encode.

The page's square (rows and columns numbered 1 to 5, J omitted):

```
  1 2 3 4 5
1 Z E B R A
2 S C D F G
3 H I K L M
4 N O P Q T
5 U V W X Y
```

Plaintext coordinates and the repeating RUSSIAN coordinates are added as ordinary decimal numbers, not digit by digit:

```
PT:  23  55   41  15  35  32  45  12  53   32  41  45  12  14  43  15  34  15  22  12
KEY: 14  51   21  21  32  15  41  14  51   21  21  32  15  41  14  51  21  21  32  15
CT:  37  106  62  36  67  47  86  26  104  53  62  77  27  55  57  66  55  36  54  27
```

## What the engine does

- Drop non-letters. Fold J into I, matching a 25-cell square that has I and no J.
- The key is two keywords: the square keyword, then the additive keyword, separated by a space (a slash also works).
- Encryption turns both streams into 1-5 coordinates and adds each pair as a normal integer. Cipher numbers stay separated by spaces, because sums such as 106 are three digits.
- Decryption subtracts the repeating additive coordinates and reads the square.
- `solve_nihilist(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters.
- No blind keyword search is registered. Supply the key.

## Verification certificate

`engine/data/nihilist_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `NihilistCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown square keyword or additive keyword.
- Implement the later straddling-checkerboard or VIC variants. This is the basic Nihilist addition cipher only.
