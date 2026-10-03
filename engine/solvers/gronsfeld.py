"""Gronsfeld known-key solver: Vigenère shifts restricted to digits 0–9.

With A=0 … Z=25 and a repeating numeric key,

    C = (P + digit) mod 26
    P = (C - digit) mod 26

The worked example used here is the one on CaesarCipher.org (fetched
2026-10-02):

  https://caesarcipher.org/learn/gronsfeld-cipher-numeric-key-vigenere-variant-guide

The page encrypts the message "ATTACK AT DAWN" with key 3 1 4 1 5. After
spaces are removed, the letter stream is ATTACKATDAWN and the ciphertext
letter stream is DUXBHNBXEFZO (also printed there as "DUXBH NBXEF ZO").

This module is a **known classical-cipher** solver. It recovers plaintext
only when the numeric key is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# CaesarCipher.org worked example (fetched 2026-10-02).
# https://caesarcipher.org/learn/gronsfeld-cipher-numeric-key-vigenere-variant-guide
CAESARCIPHER_ORG_URL = (
    "https://caesarcipher.org/learn/gronsfeld-cipher-numeric-key-vigenere-variant-guide"
)
CAESARCIPHER_ORG_KEY = "31415"
CAESARCIPHER_ORG_PLAIN = "ATTACKATDAWN"
CAESARCIPHER_ORG_CIPHER = "DUXBHNBXEFZO"

_SCOPE = (
    "Known classical Gronsfeld cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def gronsfeld_key(key: str) -> tuple[int, ...]:
    """Digits 0–9. Spaces and other separators are ignored. At least one digit is required.

    Letters are rejected so a Vigenère keyword is not silently treated as a Gronsfeld key.
    """
    if any(ch.isalpha() for ch in key):
        raise ValueError("Gronsfeld key must be digits 0-9, not letters")
    digits = tuple(int(ch) for ch in key if ch.isdigit())
    if not digits:
        raise ValueError("Gronsfeld key must contain at least one digit")
    return digits


def gronsfeld_substitute(letter: str, digit: int, *, decrypt: bool = False) -> str:
    """Shift one A–Z letter by a digit 0–9. Decrypt subtracts; encrypt adds."""
    plain = letters_only(letter)
    if len(plain) != 1:
        raise ValueError("Gronsfeld substitute expects one A-Z letter")
    if not isinstance(digit, int) or isinstance(digit, bool) or not 0 <= digit <= 9:
        raise ValueError("Gronsfeld digit must be an int from 0 to 9")
    shift = -digit if decrypt else digit
    return chr(65 + (ord(plain) - 65 + shift) % 26)


def _apply(text: str, key: str, *, decrypt: bool) -> str:
    digits = gronsfeld_key(key)
    stream = letters_only(text)
    if not stream:
        raise ValueError("text has no letters")
    out = [
        gronsfeld_substitute(ch, digits[i % len(digits)], decrypt=decrypt)
        for i, ch in enumerate(stream)
    ]
    return "".join(out)


def gronsfeld_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Gronsfeld numeric key. Non-letters are dropped."""
    return _apply(text, key, decrypt=False)


def gronsfeld_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Gronsfeld numeric key. Non-letters are dropped."""
    return _apply(text, key, decrypt=True)


def solve_gronsfeld(text: str, *, key: str) -> SolveResult:
    """Recover Gronsfeld plaintext when the numeric key is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    digits = gronsfeld_key(key)
    plain_letters = gronsfeld_decrypt(text, key)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    key_text = "".join(str(d) for d in digits)
    return SolveResult(
        method="gronsfeld",
        plaintext=rendered,
        key=key_text,
        score=float(len(plain_letters)),
        details={
            "key": key_text,
            "letters": len(letters_only(text)),
            "mode": "known_numeric_key",
            "scope": _SCOPE,
            "source_url": CAESARCIPHER_ORG_URL,
        },
    )


__all__ = [
    "CAESARCIPHER_ORG_CIPHER",
    "CAESARCIPHER_ORG_KEY",
    "CAESARCIPHER_ORG_PLAIN",
    "CAESARCIPHER_ORG_URL",
    "gronsfeld_decrypt",
    "gronsfeld_encrypt",
    "gronsfeld_key",
    "gronsfeld_substitute",
    "solve_gronsfeld",
]
