"""AES single-block encryption and supplied-key decryption.

Implements AES-128, AES-192, and AES-256 using the Python standard library.
Each input is exactly sixteen bytes. FIPS 197 defines the transformation:
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf

The independent known-answer vectors are printed in Appendix C of NIST's
archived original FIPS 197:
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
NIST states that its 2023 update made no technical algorithm changes.

The solve_aes wrapper requires the key and returns hexadecimal bytes. It
does not search for an unknown key. This educational implementation has
no mode of operation, authentication, padding, or constant-time guarantee.
It is not a production cryptographic library or a claim about Kryptos K4,
Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib

from engine.result import SolveResult


FIPS197_URL = "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf"
FIPS197_CURRENT_URL = "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf"
FIPS197_PDF_SHA256 = "251dfe0b5dc283abaf364adf586f7ec6dc4e495335d48dd5ee0fee6c5961da8a"
BLOCK_BYTES = 16

# FIPS 197 S-box, indexed by the byte value. The inverse table is derived.
_SBOX = bytes.fromhex(
    "637c777bf26b6fc53001672bfed7ab76"
    "ca82c97dfa5947f0add4a2af9ca472c0"
    "b7fd9326363ff7cc34a5e5f171d83115"
    "04c723c31896059a071280e2eb27b275"
    "09832c1a1b6e5aa0523bd6b329e32f84"
    "53d100ed20fcb15b6acbbe394a4c58cf"
    "d0efaafb434d338545f9027f503c9fa8"
    "51a3408f929d38f5bcb6da2110fff3d2"
    "cd0c13ec5f974417c4a77e3d645d1973"
    "60814fdc222a908846eeb814de5e0bdb"
    "e0323a0a4906245cc2d3ac629195e479"
    "e7c8376d8dd54ea96c56f4ea657aae08"
    "ba78252e1ca6b4c6e8dd741f4bbd8b8a"
    "703eb5664803f60e613557b986c11d9e"
    "e1f8981169d98e949b1e87e9ce5528df"
    "8ca1890dbfe6426841992d0fb054bb16"
)
_INVERSE_SBOX = bytes(_SBOX.index(value) for value in range(256))

_MIX_MATRIX = (
    (2, 3, 1, 1),
    (1, 2, 3, 1),
    (1, 1, 2, 3),
    (3, 1, 1, 2),
)
_INVERSE_MIX_MATRIX = (
    (14, 11, 13, 9),
    (9, 14, 11, 13),
    (13, 9, 14, 11),
    (11, 13, 9, 14),
)


def _validate_block(block: bytes) -> None:
    if not isinstance(block, bytes):
        raise TypeError("AES block must be bytes")
    if len(block) != BLOCK_BYTES:
        raise ValueError("AES block must contain exactly 16 bytes")


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes):
        raise TypeError("AES key must be bytes")
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must contain 16, 24, or 32 bytes")


def _multiply(left: int, right: int) -> int:
    """Multiply bytes in GF(2**8), modulo x**8 + x**4 + x**3 + x + 1."""
    result = 0
    while right:
        if right & 1:
            result ^= left
        left = (left << 1) ^ (0x11B if left & 0x80 else 0)
        right >>= 1
    return result


def aes_expand_key(key: bytes) -> tuple[bytes, ...]:
    """Return all sixteen-byte round keys, including the initial round key."""
    _validate_key(key)
    word_count = len(key) // 4
    rounds = word_count + 6
    words = [list(key[offset : offset + 4]) for offset in range(0, len(key), 4)]
    round_constant = 1
    for index in range(word_count, 4 * (rounds + 1)):
        temporary = words[index - 1][:]
        if index % word_count == 0:
            temporary = [_SBOX[value] for value in temporary[1:] + temporary[:1]]
            temporary[0] ^= round_constant
            round_constant = _multiply(round_constant, 2)
        elif word_count == 8 and index % word_count == 4:
            temporary = [_SBOX[value] for value in temporary]
        words.append(
            [words[index - word_count][offset] ^ temporary[offset] for offset in range(4)]
        )
    return tuple(
        bytes(value for word in words[index : index + 4] for value in word)
        for index in range(0, len(words), 4)
    )


def _add_round_key(state: list[int], key: bytes) -> list[int]:
    return [value ^ key[index] for index, value in enumerate(state)]


def _shift_rows(state: list[int], *, inverse: bool = False) -> list[int]:
    """The flat state uses the FIPS 197 column-major byte order."""
    direction = -1 if inverse else 1
    return [
        state[4 * ((column + direction * row) % 4) + row]
        for column in range(4)
        for row in range(4)
    ]


def _mix_columns(state: list[int], *, inverse: bool = False) -> list[int]:
    matrix = _INVERSE_MIX_MATRIX if inverse else _MIX_MATRIX
    result = []
    for column in range(4):
        values = state[4 * column : 4 * column + 4]
        for coefficients in matrix:
            value = 0
            for coefficient, byte in zip(coefficients, values):
                value ^= _multiply(byte, coefficient)
            result.append(value)
    return result


def aes_encrypt_block(block: bytes, key: bytes) -> bytes:
    """Encrypt exactly one sixteen-byte block, with no padding or mode."""
    _validate_block(block)
    round_keys = aes_expand_key(key)
    state = _add_round_key(list(block), round_keys[0])
    for round_key in round_keys[1:-1]:
        state = [_SBOX[value] for value in state]
        state = _shift_rows(state)
        state = _mix_columns(state)
        state = _add_round_key(state, round_key)
    state = [_SBOX[value] for value in state]
    state = _shift_rows(state)
    return bytes(_add_round_key(state, round_keys[-1]))


def aes_decrypt_block(block: bytes, key: bytes) -> bytes:
    """Decrypt exactly one sixteen-byte block with its supplied AES key."""
    _validate_block(block)
    round_keys = aes_expand_key(key)
    state = _add_round_key(list(block), round_keys[-1])
    for round_key in reversed(round_keys[1:-1]):
        state = _shift_rows(state, inverse=True)
        state = [_INVERSE_SBOX[value] for value in state]
        state = _add_round_key(state, round_key)
        state = _mix_columns(state, inverse=True)
    state = _shift_rows(state, inverse=True)
    state = [_INVERSE_SBOX[value] for value in state]
    return bytes(_add_round_key(state, round_keys[0]))


def solve_aes(ciphertext: bytes, *, key: bytes) -> SolveResult:
    """Decrypt one block with the required key, returning lowercase hex.

    No unknown-key search is attempted. The hash covers the recovered raw
    bytes, rather than the hexadecimal text used by SolveResult.plaintext.
    """
    plaintext = aes_decrypt_block(ciphertext, key)
    key_bits = 8 * len(key)
    return SolveResult(
        method="aes",
        plaintext=plaintext.hex(),
        key=key.hex(),
        score=float(len(plaintext)),
        details={
            "algorithm": f"AES-{key_bits}",
            "key_bits": key_bits,
            "rounds": len(key) // 4 + 6,
            "block_bytes": BLOCK_BYTES,
            "encoding": "hex",
            "plaintext_hex": plaintext.hex(),
            "ciphertext_hex": ciphertext.hex(),
            "plaintext_sha256": hashlib.sha256(plaintext).hexdigest(),
            "hash_encoding": "raw_bytes",
            "mode": "known_key",
            "scope": (
                "Supplied-key AES single-block decryption only. No unknown-key cracking, "
                "authentication, padding, or mode of operation. Educational implementation "
                "without a constant-time guarantee; not a production cryptographic library."
            ),
            "source_url": FIPS197_URL,
            "algorithm_source_url": FIPS197_CURRENT_URL,
        },
    )


__all__ = [
    "BLOCK_BYTES",
    "FIPS197_CURRENT_URL",
    "FIPS197_PDF_SHA256",
    "FIPS197_URL",
    "aes_decrypt_block",
    "aes_encrypt_block",
    "aes_expand_key",
    "solve_aes",
]
