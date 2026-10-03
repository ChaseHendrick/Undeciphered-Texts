"""Vigenère autokey known-key solver: primer, then plaintext, as the keystream.

Blaise de Vigenère's autokey (1586) starts with a short primer keyword and
then continues the keystream with the plaintext itself. With A=0 … Z=25,

    keystream = primer + plaintext
    C = (P + K) mod 26
    P = (C - K) mod 26

Decryption uses only the primer at first. Each recovered plaintext letter is
appended to the keystream and used for the next letter.

The worked example used here is the one on Practical Cryptography
(fetched 2026-10-02):

  http://practicalcryptography.com/ciphers/autokey-cipher/

This module is a **known classical-cipher** solver. It recovers plaintext
only when the primer keyword is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Practical Cryptography worked example (fetched 2026-10-02).
# http://practicalcryptography.com/ciphers/autokey-cipher/
PRACTICAL_CRYPTOGRAPHY_URL = "http://practicalcryptography.com/ciphers/autokey-cipher/"
PRACTICAL_CRYPTOGRAPHY_KEY = "FORTIFICATION"
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE"
PRACTICAL_CRYPTOGRAPHY_CIPHER = "ISWXVIBJEXIGGZEQPBIMOIGAKMHE"

_SCOPE = (
    "Known classical Vigenère autokey cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def autokey_key(key: str) -> str:
    """A-Z primer keyword. Non-letters are dropped. At least one letter is required."""
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("Autokey primer must contain at least one letter")
    return cleaned


def autokey_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Vigenère-autokey primer. Non-letters are dropped.

    The keystream is the primer followed by the plaintext, truncated to the
    plaintext length. Each letter is (plaintext + keystream) mod 26.
    """
    primer = autokey_key(key)
    plain = letters_only(text)
    if not plain:
        raise ValueError("text has no letters")
    keystream = (primer + plain)[: len(plain)]
    out = [
        chr(65 + (ord(p) + ord(k) - 130) % 26)
        for p, k in zip(plain, keystream)
    ]
    return "".join(out)


def autokey_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Vigenère-autokey primer.

    The primer decrypts the first letters. Each recovered plaintext letter
    is then used as the next keystream letter.
    """
    primer = autokey_key(key)
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    keystream = list(primer)
    plain: list[str] = []
    for index, ch in enumerate(cipher):
        if index >= len(keystream):
            raise ValueError("Autokey primer was exhausted before the ciphertext ended")
        letter = chr(65 + (ord(ch) - ord(keystream[index])) % 26)
        plain.append(letter)
        keystream.append(letter)
    return "".join(plain)


def solve_autokey(text: str, *, key: str) -> SolveResult:
    """Recover Vigenère-autokey plaintext when the primer keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    primer = autokey_key(key)
    plain_letters = autokey_decrypt(text, primer)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    return SolveResult(
        method="autokey",
        plaintext=rendered,
        key=primer,
        score=float(len(plain_letters)),
        details={
            "key": primer,
            "letters": len(letters_only(text)),
            "mode": "known_primer",
            "variant": "vigenere_plaintext_autokey",
            "scope": _SCOPE,
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
        },
    )


__all__ = [
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_KEY",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "autokey_decrypt",
    "autokey_encrypt",
    "autokey_key",
    "solve_autokey",
]
