"""Encrypt and decrypt the classical ciphers this package solves.

These are the forward maps used to build known tests. Solvers do not call
them with the secret; tests and the demo do, then throw the key away.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only


def _is_key_alpha(key: str) -> str:
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("key must contain at least one letter")
    return cleaned


def caesar_encrypt(text: str, shift: int) -> str:
    shift %= 26
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            out.append(ch)
            continue
        base = ord("A") if ch.isupper() else ord("a")
        out.append(chr(base + (ord(ch) - base + shift) % 26))
    return "".join(out)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


def vigenere_encrypt(text: str, key: str) -> str:
    keyword = _is_key_alpha(key)
    out: list[str] = []
    j = 0
    for ch in text:
        if not ch.isalpha():
            out.append(ch)
            continue
        shift = ord(keyword[j % len(keyword)]) - 65
        base = ord("A") if ch.isupper() else ord("a")
        out.append(chr(base + (ord(ch) - base + shift) % 26))
        j += 1
    return "".join(out)


def vigenere_decrypt(text: str, key: str) -> str:
    keyword = _is_key_alpha(key)
    # Decrypt is encrypt under the complementary shifts.
    complement = "".join(chr(65 + (26 - (ord(ch) - 65)) % 26) for ch in keyword)
    return vigenere_encrypt(text, complement)


def substitution_encrypt(text: str, key: str) -> str:
    """key[i] is the ciphertext letter that replaces plaintext letter i (A=0)."""
    cipher_alpha = _is_key_alpha(key)
    if len(cipher_alpha) != 26 or len(set(cipher_alpha)) != 26:
        raise ValueError("substitution key must be a permutation of A-Z")
    table = {ALPHABET[i]: cipher_alpha[i] for i in range(26)}
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            out.append(ch)
            continue
        mapped = table[ch.upper()]
        out.append(mapped.lower() if ch.islower() else mapped)
    return "".join(out)


def substitution_decrypt(text: str, key: str) -> str:
    cipher_alpha = _is_key_alpha(key)
    if len(cipher_alpha) != 26 or len(set(cipher_alpha)) != 26:
        raise ValueError("substitution key must be a permutation of A-Z")
    inverse = ["?"] * 26
    for plain_i, cipher_ch in enumerate(cipher_alpha):
        inverse[ord(cipher_ch) - 65] = ALPHABET[plain_i]
    return substitution_encrypt(text, "".join(inverse))
