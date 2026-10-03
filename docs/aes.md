# AES single-block helper

`engine/solvers/aes.py` implements encryption and supplied-key decryption for one 16-byte AES block. It supports 16-, 24-, and 32-byte keys, corresponding to AES-128, AES-192, and AES-256. The runtime uses the Python standard library only.

The algorithm follows [NIST FIPS 197-upd1](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf): column-major state order, SubBytes, ShiftRows, MixColumns, AddRoundKey, the key expansion for all three key lengths, and inverse operations. NIST states that the 2023 editorial update did not change the AES algorithm. The independent published vectors below come from Appendix C of the [archived 2001 FIPS 197](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf).

## Published known answers

Each vector has plaintext bytes represented by hexadecimal `00112233445566778899aabbccddeeff`.

| Variant | Supplied key in hexadecimal | Published ciphertext in hexadecimal |
| --- | --- | --- |
| AES-128, Appendix C.1 | `000102030405060708090a0b0c0d0e0f` | `69c4e0d86a7b0430d8cdb78070b4c55a` |
| AES-192, Appendix C.2 | `000102030405060708090a0b0c0d0e0f1011121314151617` | `dda97ca4864cdfe06eaf70a0ec0d7191` |
| AES-256, Appendix C.3 | `000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f` | `8ea2b7ca516745bfeafc49904b496089` |

The original PDF was fetched on 2026-10-03, with SHA-256 `251dfe0b5dc283abaf364adf586f7ec6dc4e495335d48dd5ee0fee6c5961da8a`. The SHA-256 of the 16 recovered plaintext bytes is `a8faed6abbf35c12a4b26e40f6feb19d736d90045c83b9f9a31f638d323e6811`. This hashes the binary bytes, not their hexadecimal text representation.

## API

```python
from engine.solvers.aes import aes_decrypt_block, aes_encrypt_block, solve_aes

key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")
ciphertext = aes_encrypt_block(plaintext, key)
assert aes_decrypt_block(ciphertext, key) == plaintext

result = solve_aes(ciphertext, key=key)
assert result.plaintext == plaintext.hex()
assert result.details["mode"] == "known_key"
assert result.details["encoding"] == "hex"
```

`aes_encrypt_block` and `aes_decrypt_block` accept `bytes` and return `bytes`. Convert a string, bytearray, or other container explicitly before calling them. A block must have exactly 16 bytes, and a key must have exactly 16, 24, or 32 bytes. Invalid types raise `TypeError`; invalid lengths raise `ValueError`.

`aes_expand_key` returns a tuple of 11, 13, or 15 round keys, including the initial key. Each round key contains 16 bytes. `solve_aes` requires `key=` and returns a `SolveResult` whose plaintext is lowercase hexadecimal, with binary encoding and raw-byte hash metadata. Its score counts recovered bytes and does not estimate language quality.

## Validation and limits

`tests/test_aes.py` failed with a missing-module import before implementation. The ten focused tests then passed: all three published encryption and decryption vectors, published final round keys, raw-byte certificate hashes, arbitrary binary roundtrips, explicit-key metadata, and input errors. Run with Python 3.10 or newer:

```bash
python3 -m unittest tests.test_aes -v
```

An independent local check also matched encryption and decryption against the installed `cryptography` 50.0.1 library for 300 generated key/block pairs, 100 for each key size. That package is not imported by the solver or its committed tests.

`engine/data/aes_certificate.json` uses `plaintext_hex`, `ciphertext_hex`, `encoding: "hex"`, and `hash_encoding: "raw_bytes"`. It deliberately has no language plaintext/ciphertext fields, so the text-only neural router does not learn from binary vectors. The helper stays outside text-only `SOLVERS` dispatch.

This is supplied-key decryption. It does not recover an unknown AES key. The implementation has no authentication, padding, or mode of operation, and its Python table lookups and arithmetic have no constant-time guarantee. It is an educational primitive, not a production cryptographic library or a FIPS-validated implementation. No unresolved historical cipher or unknown script is claimed solved.
