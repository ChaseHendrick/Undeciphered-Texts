"""ACA Numbered Key: a repeated-letter key extended to cover the alphabet.

Source: https://www.cryptogram.org/downloads/aca.info/ciphers/NumberedKey.pdf
Duplicate phrase letters are separate homophones. Supplied-key decryption only.
"""
from __future__ import annotations

from collections.abc import Sequence
from engine.result import SolveResult

ACA_NUMBERED_KEY_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/NumberedKey.pdf"
ACA_NUMBERED_KEY_KEY = "I like ciphers."
ACA_NUMBERED_KEY_START = 18
ACA_NUMBERED_KEY_PLAIN = "THEROADTOSUCCESSISALWAYSUNDERCONSTRUCTION"
ACA_NUMBERED_KEY_CIPHER = "04 19 20 21 02 23 25 04 02 22 05 16 16 15 22 22 11 22 23 12 07 23 09 22 05 01 25 20 21 16 02 01 22 04 21 05 16 04 17 02 01"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_LETTERS = 4096


def _letters(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text/key must be a string")
    if len(text) > 16384 or any(ch.isalpha() and not ch.isascii() for ch in text):
        raise ValueError("text/key must use ASCII letters within the input size bound")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not 1 <= len(letters) <= MAX_LETTERS:
        raise ValueError(f"text/key must contain 1..{MAX_LETTERS} letters")
    return letters


def numbered_key_alphabet(key: str, *, start: int = 0) -> str:
    """Append missing A-Z letters and rotate to index start before numbering."""
    head = _letters(key)
    extended = head + "".join(ch for ch in ALPHABET if ch not in head)
    if len(extended) > 100:
        raise ValueError("extended key must fit two-digit codes 00..99")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an integer rotation index")
    if not 0 <= start < len(extended):
        raise ValueError("start must identify a position within the extended key")
    return extended[start:] + extended[:start]


def numbered_key_encrypt(text: str, key: str, *, start: int = 0,
                         homophone_indices: Sequence[int] | None = None) -> str:
    plain = _letters(text)
    table = numbered_key_alphabet(key, start=start)
    if homophone_indices is None:
        choices = (0,) * len(plain)
    elif isinstance(homophone_indices, Sequence) and not isinstance(homophone_indices, (str, bytes, bytearray)):
        if len(homophone_indices) != len(plain):
            raise ValueError("one homophone selection is required per plaintext letter")
        choices = tuple(homophone_indices)
    else:
        raise TypeError("homophone selections must be a finite integer sequence")
    out = []
    for ch, choice in zip(plain, choices):
        codes = [i for i, letter in enumerate(table) if letter == ch]
        if not isinstance(choice, int) or isinstance(choice, bool):
            raise TypeError("homophone selections must be integers")
        if not 0 <= choice < len(codes):
            raise ValueError(f"homophone selection exceeds the alternatives for {ch}")
        out.append(f"{codes[choice]:02d}")
    return " ".join(out)


def _codes(text: str | Sequence[int]) -> tuple[int, ...]:
    if isinstance(text, str):
        if len(text) > 16384:
            raise ValueError("ciphertext exceeds the input size bound")
        body = text.strip()
        if body.endswith("."):
            body = body[:-1].rstrip()
        tokens = body.split()
        if not tokens or len(tokens) > MAX_LETTERS or any(len(x) != 2 or any(ch not in "0123456789" for ch in x) for x in tokens):
            raise ValueError("ciphertext must contain 1..4096 space-separated two-digit ASCII codes")
        return tuple(map(int, tokens))
    if isinstance(text, Sequence) and not isinstance(text, (bytes, bytearray)):
        if not 1 <= len(text) <= MAX_LETTERS:
            raise ValueError("ciphertext must contain 1..4096 code integers")
        if any(not isinstance(code, int) or isinstance(code, bool) for code in text):
            raise TypeError("ciphertext code values must be integers")
        return tuple(text)
    raise TypeError("ciphertext must be a code string or finite integer sequence")


def numbered_key_decrypt(text: str | Sequence[int], key: str, *, start: int = 0) -> str:
    table = numbered_key_alphabet(key, start=start)
    codes = _codes(text)
    if any(code < 0 or code >= len(table) for code in codes):
        raise ValueError("ciphertext code is outside the numbered key")
    return "".join(table[code] for code in codes)


def solve_numbered_key(text: str | Sequence[int], *, key: str, start: int = 0) -> SolveResult:
    plain = numbered_key_decrypt(text, key, start=start)
    table = numbered_key_alphabet(key, start=start)
    return SolveResult("numbered_key", plain, f"{_letters(key)}; start {start}", float(len(plain)),
                       {"mode": "supplied_key", "start": start, "numbered_alphabet": table,
                        "source_url": ACA_NUMBERED_KEY_URL, "scope": "Supplied-key homophonic substitution only."})
