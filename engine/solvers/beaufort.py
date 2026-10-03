"""Beaufort known-key solver: reciprocal key-minus-plaintext subtraction.

Sir Francis Beaufort's cipher repeats a keyword. With A=0 … Z=25,

    C = (K - P) mod 26
    P = (K - C) mod 26

so the same operation encrypts and decrypts. The worked example used here
is the one on Practical Cryptography (fetched 2026-10-02):

  http://practicalcryptography.com/ciphers/beaufort-cipher/

This module is a **known classical-cipher** solver. It recovers plaintext
only when the keyword is supplied. It is **not** an unknown-script reading
and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Practical Cryptography worked example (fetched 2026-10-02).
# http://practicalcryptography.com/ciphers/beaufort-cipher/
PRACTICAL_CRYPTOGRAPHY_URL = "http://practicalcryptography.com/ciphers/beaufort-cipher/"
PRACTICAL_CRYPTOGRAPHY_KEY = "FORTIFICATION"
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE"
PRACTICAL_CRYPTOGRAPHY_CIPHER = "CKMPVCPVWPIWUJOGIUAPVWRIWUUK"

_SCOPE = (
    "Known classical Beaufort cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def beaufort_key(key: str) -> str:
    """A-Z keyword. Non-letters are dropped. At least one letter is required."""
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("Beaufort key must contain at least one letter")
    return cleaned


def beaufort_substitute(letter: str, key_letter: str) -> str:
    """Map one A-Z letter by (key - letter) mod 26. The map is an involution."""
    plain = letters_only(letter)
    key = letters_only(key_letter)
    if len(plain) != 1 or len(key) != 1:
        raise ValueError("Beaufort substitute expects one A-Z letter and one key letter")
    return chr(65 + (ord(key) - ord(plain)) % 26)


def _apply(text: str, key: str) -> str:
    keyword = beaufort_key(key)
    stream = letters_only(text)
    if not stream:
        raise ValueError("text has no letters")
    out = [
        beaufort_substitute(ch, keyword[i % len(keyword)])
        for i, ch in enumerate(stream)
    ]
    return "".join(out)


def beaufort_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Beaufort keyword. Non-letters are dropped."""
    return _apply(text, key)


def beaufort_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Beaufort keyword. The map is its own inverse."""
    return _apply(text, key)


def solve_beaufort(text: str, *, key: str) -> SolveResult:
    """Recover Beaufort plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    keyword = beaufort_key(key)
    plain_letters = beaufort_decrypt(text, keyword)
    # Keep spaces and punctuation from the ciphertext skeleton.
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    return SolveResult(
        method="beaufort",
        plaintext=rendered,
        key=keyword,
        score=float(len(plain_letters)),
        details={
            "key": keyword,
            "letters": len(letters_only(text)),
            "mode": "known_keyword",
            "scope": _SCOPE,
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
        },
    )


__all__ = [
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_KEY",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "beaufort_decrypt",
    "beaufort_encrypt",
    "beaufort_key",
    "beaufort_substitute",
    "solve_beaufort",
]
