"""RFC 8439 ChaCha20 encryption and decryption with a supplied key.

This educational standard-library implementation uses the RFC's 32-byte
key, 12-byte nonce, and 32-bit block counter. It is a stream cipher only:
it does not implement Poly1305, authenticated encryption, key discovery,
or an attack on modern cryptography. Results preserve arbitrary bytes.

Algorithm and independent vectors:
https://www.rfc-editor.org/rfc/rfc8439.html#section-2.3
https://www.rfc-editor.org/rfc/rfc8439.html#section-2.3.2
https://www.rfc-editor.org/rfc/rfc8439.html#section-2.4.2
"""

from __future__ import annotations

import hashlib
import struct

from engine.result import SolveResult


RFC_URL = "https://www.rfc-editor.org/rfc/rfc8439.html"
RFC_BLOCK_URL = RFC_URL + "#section-2.3.2"
RFC_CIPHER_URL = RFC_URL + "#section-2.4.2"
_MAX_COUNTER = (1 << 32) - 1
_CONSTANTS = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)
_ROUNDS = (
    (0, 4, 8, 12),
    (1, 5, 9, 13),
    (2, 6, 10, 14),
    (3, 7, 11, 15),
    (0, 5, 10, 15),
    (1, 6, 11, 12),
    (2, 7, 8, 13),
    (3, 4, 9, 14),
)


def _validate(key: bytes, nonce: bytes, counter: int) -> None:
    if not isinstance(key, bytes):
        raise TypeError("ChaCha20 key must be bytes")
    if len(key) != 32:
        raise ValueError("ChaCha20 key must contain exactly 32 bytes")
    if not isinstance(nonce, bytes):
        raise TypeError("ChaCha20 nonce must be bytes")
    if len(nonce) != 12:
        raise ValueError("ChaCha20 nonce must contain exactly 12 bytes")
    if not isinstance(counter, int) or isinstance(counter, bool):
        raise TypeError("ChaCha20 counter must be an integer")
    if not 0 <= counter <= _MAX_COUNTER:
        raise ValueError("ChaCha20 counter must be in 0..2^32-1")


def _rotate(word: int, bits: int) -> int:
    return ((word << bits) | (word >> (32 - bits))) & _MAX_COUNTER


def _quarter_round(state: list[int], a: int, b: int, c: int, d: int) -> None:
    state[a] = (state[a] + state[b]) & _MAX_COUNTER
    state[d] = _rotate(state[d] ^ state[a], 16)
    state[c] = (state[c] + state[d]) & _MAX_COUNTER
    state[b] = _rotate(state[b] ^ state[c], 12)
    state[a] = (state[a] + state[b]) & _MAX_COUNTER
    state[d] = _rotate(state[d] ^ state[a], 8)
    state[c] = (state[c] + state[d]) & _MAX_COUNTER
    state[b] = _rotate(state[b] ^ state[c], 7)


def chacha20_block(*, key: bytes, nonce: bytes, counter: int) -> bytes:
    """Return one 64-byte RFC 8439 keystream block using supplied parameters."""
    _validate(key, nonce, counter)
    initial = list(_CONSTANTS + struct.unpack("<8I", key) + (counter,) + struct.unpack("<3I", nonce))
    state = initial.copy()
    for _ in range(10):
        for a, b, c, d in _ROUNDS:
            _quarter_round(state, a, b, c, d)
    words = [(word + original) & _MAX_COUNTER for word, original in zip(state, initial)]
    return struct.pack("<16I", *words)


def chacha20_xor(data: bytes, *, key: bytes, nonce: bytes, counter: int = 1) -> bytes:
    """Encrypt or decrypt bytes; reject requests that would wrap the counter.

    Empty data is valid. A partial final block uses only the needed
    keystream bytes, and no padding is added.
    """
    _validate(key, nonce, counter)
    if not isinstance(data, bytes):
        raise TypeError("ChaCha20 data must be bytes")
    blocks = (len(data) + 63) // 64
    if blocks and counter + blocks - 1 > _MAX_COUNTER:
        raise ValueError("ChaCha20 counter would overflow 32 bits")
    out = bytearray()
    for block_index, offset in enumerate(range(0, len(data), 64)):
        stream = chacha20_block(key=key, nonce=nonce, counter=counter + block_index)
        out.extend(byte ^ mask for byte, mask in zip(data[offset:offset + 64], stream))
    return bytes(out)


def chacha20_encrypt(plaintext: bytes, *, key: bytes, nonce: bytes, counter: int = 1) -> bytes:
    """Encrypt with a supplied key, nonce, and initial counter."""
    return chacha20_xor(plaintext, key=key, nonce=nonce, counter=counter)


def chacha20_decrypt(ciphertext: bytes, *, key: bytes, nonce: bytes, counter: int = 1) -> bytes:
    """Decrypt with a supplied key, nonce, and initial counter."""
    return chacha20_xor(ciphertext, key=key, nonce=nonce, counter=counter)


def solve_chacha20(ciphertext: bytes, *, key: bytes, nonce: bytes, counter: int = 1) -> SolveResult:
    """Return recovered bytes as hex; this operation explicitly needs the key."""
    plain = chacha20_decrypt(ciphertext, key=key, nonce=nonce, counter=counter)
    return SolveResult(
        method="chacha20",
        plaintext=plain.hex(),
        key="supplied 256-bit key",
        score=0.0,
        details={
            "mode": "known_key",
            "input_encoding": "bytes",
            "plaintext_encoding": "hex",
            "plaintext_sha256": hashlib.sha256(plain).hexdigest(),
            "bytes": len(plain),
            "nonce_hex": nonce.hex(),
            "counter": counter,
            "authentication": "none",
            "source_url": RFC_URL,
            "scope": "Supplied-key RFC 8439 ChaCha20 only; no unknown-key recovery or authentication.",
        },
    )


__all__ = [
    "RFC_BLOCK_URL",
    "RFC_CIPHER_URL",
    "RFC_URL",
    "chacha20_block",
    "chacha20_decrypt",
    "chacha20_encrypt",
    "chacha20_xor",
    "solve_chacha20",
]
