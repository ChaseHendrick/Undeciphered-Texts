"""Porta (della Porta) known-key solver: 13 reciprocal alphabets.

Giambattista della Porta's cipher repeats a keyword. Each key letter
selects one of thirteen paired alphabets (A/B, C/D, …, Y/Z). The same
tableau encrypts and decrypts. The rows used here are the reciprocal
tableau in the published worked example:

  https://www.boxentriq.com/ciphers/porta-cipher

This module is a **known classical-cipher** solver. It recovers plaintext
only when the keyword is supplied. It is **not** an unknown-script reading
and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Boxentriq worked example (fetched 2026-10-02).
# https://www.boxentriq.com/ciphers/porta-cipher
BOXENTRIQ_URL = "https://www.boxentriq.com/ciphers/porta-cipher"
BOXENTRIQ_KEY = "FORTIFICATION"
BOXENTRIQ_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE"
BOXENTRIQ_CIPHER = "SYNNJSCVRNRLAHUTUKUCVRYRLANY"

_SCOPE = (
    "Known classical Porta cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def porta_key(key: str) -> str:
    """A–Z keyword. Non-letters are dropped. At least one letter is required."""
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("Porta key must contain at least one letter")
    return cleaned


def porta_row(key_letter: str) -> int:
    """Tableau row 0..12. A and B share row 0; Y and Z share row 12."""
    letter = letters_only(key_letter)
    if len(letter) != 1:
        raise ValueError("Porta row selector must be one letter")
    return (ord(letter) - 65) // 2


def porta_substitute(letter: str, key_letter: str) -> str:
    """Map one A–Z letter through the Porta row selected by key_letter.

    First half A–M goes to N–Z rotated by the row; second half is the inverse,
    so the map is an involution. Row 0 (A/B) is the familiar A↔N … M↔Z slide.
    """
    row = porta_row(key_letter)
    index = ord(letters_only(letter)) - 65
    if not 0 <= index <= 25 or len(letters_only(letter)) != 1:
        raise ValueError("Porta substitute expects one A-Z letter")
    if index < 13:
        return chr(65 + 13 + (index + row) % 13)
    return chr(65 + (index - 13 - row) % 13)


def _apply(text: str, key: str) -> str:
    keyword = porta_key(key)
    stream = letters_only(text)
    if not stream:
        raise ValueError("text has no letters")
    out = [
        porta_substitute(ch, keyword[i % len(keyword)])
        for i, ch in enumerate(stream)
    ]
    return "".join(out)


def porta_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Porta keyword. Non-letters are dropped."""
    return _apply(text, key)


def porta_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Porta keyword. The map is its own inverse."""
    return _apply(text, key)


def solve_porta(text: str, *, key: str) -> SolveResult:
    """Recover Porta plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    keyword = porta_key(key)
    plain_letters = porta_decrypt(text, keyword)
    # Keep spaces and punctuation from the ciphertext skeleton.
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    return SolveResult(
        method="porta",
        plaintext=rendered,
        key=keyword,
        score=float(len(plain_letters)),
        details={
            "key": keyword,
            "letters": len(letters_only(text)),
            "mode": "known_keyword",
            "scope": _SCOPE,
            "source_url": BOXENTRIQ_URL,
        },
    )


__all__ = [
    "BOXENTRIQ_CIPHER",
    "BOXENTRIQ_KEY",
    "BOXENTRIQ_PLAIN",
    "BOXENTRIQ_URL",
    "porta_decrypt",
    "porta_encrypt",
    "porta_key",
    "porta_row",
    "porta_substitute",
    "solve_porta",
]
