"""Running-key known-key solver: a non-repeating text keystream.

The running-key cipher uses the same tabula recta as Vigenere. A short
keyword is not repeated. The key is a passage at least as long as the
plaintext (often taken from a book). With A=0 ... Z=25,

    C = (P + K) mod 26
    P = (C - K) mod 26

The worked example used here is the one on Practical Cryptography
(fetched 2026-10-02):

  http://practicalcryptography.com/ciphers/classical-era/running-key/

Key text: "How does the duck know that? said Victor"
Plaintext: DEFENDTHEEASTWALLOFTHECASTLE
Ciphertext: KSBHBHLALIDMVGKYZKYAHXUAAWGM

This module is a **known classical-cipher** solver. It recovers plaintext
only when the running key is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Practical Cryptography worked example (fetched 2026-10-02).
# http://practicalcryptography.com/ciphers/classical-era/running-key/
PRACTICAL_CRYPTOGRAPHY_URL = (
    "http://practicalcryptography.com/ciphers/classical-era/running-key/"
)
PRACTICAL_CRYPTOGRAPHY_KEY = "HOWDOESTHEDUCKKNOWTHATSAIDVI"
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE"
PRACTICAL_CRYPTOGRAPHY_CIPHER = "KSBHBHLALIDMVGKYZKYAHXUAAWGM"

_SCOPE = (
    "Known classical running-key cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def running_key_key(key: str) -> str:
    """A-Z running key. Non-letters are dropped. At least one letter is required."""
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("Running key must contain at least one letter")
    return cleaned


def _keystream(key: str, n: int) -> str:
    """Use the running key as written. Do not repeat a short key."""
    cleaned = running_key_key(key)
    if len(cleaned) < n:
        raise ValueError(
            "Running key is shorter than the text; it is not repeated"
        )
    return cleaned[:n]


def running_key_encrypt(text: str, key: str) -> str:
    """Encrypt with a known running key. Non-letters are dropped.

    Each letter is (plaintext + keystream) mod 26. The key is not repeated.
    Extra key letters past the plaintext length are ignored.
    """
    plain = letters_only(text)
    if not plain:
        raise ValueError("text has no letters")
    keystream = _keystream(key, len(plain))
    out = [
        chr(65 + (ord(p) + ord(k) - 130) % 26)
        for p, k in zip(plain, keystream)
    ]
    return "".join(out)


def running_key_decrypt(text: str, key: str) -> str:
    """Decrypt with a known running key.

    Each letter is (ciphertext - keystream) mod 26. The key is not repeated.
    """
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    keystream = _keystream(key, len(cipher))
    out = [
        chr(65 + (ord(c) - ord(k)) % 26)
        for c, k in zip(cipher, keystream)
    ]
    return "".join(out)


def solve_running_key(text: str, *, key: str) -> SolveResult:
    """Recover running-key plaintext when the key passage is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    cleaned = running_key_key(key)
    plain_letters = running_key_decrypt(text, cleaned)
    rendered = (
        reinject(text, plain_letters)
        if any(not ch.isalpha() for ch in text)
        else plain_letters
    )
    return SolveResult(
        method="running_key",
        plaintext=rendered,
        key=cleaned,
        score=float(len(plain_letters)),
        details={
            "key": cleaned,
            "letters": len(letters_only(text)),
            "mode": "known_running_key",
            "variant": "vigenere_nonrepeating_text_key",
            "scope": _SCOPE,
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
        },
    )


__all__ = [
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_KEY",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "running_key_decrypt",
    "running_key_encrypt",
    "running_key_key",
    "solve_running_key",
]
