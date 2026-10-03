"""Supplied-key ACA Sequence Transposition, including primer/check framing.

Source: https://www.cryptogram.org/downloads/aca.info/ciphers/SequenceTransposition.pdf
The final chain digit is the transmitted check digit, as in the ACA example.
"""
from __future__ import annotations

import re
from engine.result import SolveResult

ACA_SEQUENCE_TRANSPOSITION_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/SequenceTransposition.pdf"
ACA_SEQUENCE_TRANSPOSITION_KEYWORD = "GUMMYBEARS"
ACA_SEQUENCE_TRANSPOSITION_PRIMER = "69315"
ACA_SEQUENCE_TRANSPOSITION_PLAIN = "THEEARLYBIRDGETSTHEWORM"
ACA_SEQUENCE_TRANSPOSITION_CIPHER = "YHOMARTBDETHIGWLRESEERT"
MAX_LETTERS = 4096


def _letters(text: str, *, allow_digits: bool = False) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > 16384 or any(ch.isalpha() and not ch.isascii() for ch in text):
        raise ValueError("text must use ASCII letters within the input size bound")
    if not allow_digits and any(ch.isdigit() for ch in text):
        raise ValueError("letter text must not contain digits; use a complete framed message")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not 1 <= len(letters) <= MAX_LETTERS:
        raise ValueError(f"text must contain 1..{MAX_LETTERS} letters")
    return letters


def _primer(primer: str) -> str:
    if not isinstance(primer, str):
        raise TypeError("primer must be a five-digit string")
    if len(primer) != 5 or any(ch not in "0123456789" for ch in primer):
        raise ValueError("primer must contain exactly five ASCII digits")
    return primer


def sequence_digits(primer: str, length: int) -> str:
    _primer(primer)
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("sequence length must be an integer")
    if not 1 <= length <= MAX_LETTERS:
        raise ValueError(f"sequence length must be in 1..{MAX_LETTERS}")
    digits = [int(ch) for ch in primer]
    for index in range(max(0, length - 5)):
        digits.append((digits[index] + digits[index + 1]) % 10)
    return "".join(map(str, digits[:length]))


def sequence_key_ranks(keyword: str) -> tuple[int, ...]:
    letters = _letters(keyword)
    if len(letters) != 10:
        raise ValueError("keyword/phrase must contain exactly ten letters")
    ranks = [0] * 10
    for rank, position in enumerate(sorted(range(10), key=lambda i: (letters[i], i)), 1):
        ranks[position] = rank % 10
    return tuple(ranks)


def _positions(keyword: str, primer: str, length: int) -> list[int]:
    ranks = sequence_key_ranks(keyword)
    digits = sequence_digits(primer, length)
    buckets = [[] for _ in range(10)]
    for position, digit in enumerate(digits):
        buckets[int(digit)].append(position)
    return [position for rank in ranks for position in buckets[rank]]


def parse_sequence_frame(text: str) -> tuple[str, str, str]:
    if not isinstance(text, str):
        raise TypeError("frame must be a string")
    if len(text) > 16384:
        raise ValueError("frame exceeds the input size bound")
    match = re.fullmatch(r"\s*([0-9]{5})\s+([A-Za-z\s]+?)\s+([0-9])\.?\s*", text)
    if not match:
        raise ValueError("frame requires a five-digit primer, letter groups and one trailing check digit")
    primer, body, check = match.groups()
    return primer, _letters(body), check


def sequence_transposition_encrypt(text: str, keyword: str, primer: str, *, framed: bool = False) -> str:
    if not isinstance(framed, bool):
        raise TypeError("framed must be a boolean")
    plain = _letters(text)
    positions = _positions(keyword, primer, len(plain))
    cipher = "".join(plain[position] for position in positions)
    if framed:
        groups = " ".join(cipher[i:i + 5] for i in range(0, len(cipher), 5))
        return f"{primer} {groups} {sequence_digits(primer, len(plain))[-1]}"
    return cipher


def sequence_transposition_decrypt(text: str, keyword: str, primer: str | None = None,
                                   *, check_digit: str | None = None) -> str:
    if primer is None:
        if check_digit is not None:
            raise ValueError("a framed message supplies its own check digit")
        primer, cipher, check_digit = parse_sequence_frame(text)
    else:
        _primer(primer)
        cipher = _letters(text)
    sequence = sequence_digits(primer, len(cipher))
    if check_digit is not None:
        if not isinstance(check_digit, str):
            raise TypeError("check digit must be an ASCII digit string")
        if len(check_digit) != 1 or check_digit not in "0123456789" or check_digit != sequence[-1]:
            raise ValueError("transmitted check digit disagrees with the final sequence digit")
    plain = [""] * len(cipher)
    for ch, position in zip(cipher, _positions(keyword, primer, len(cipher))):
        plain[position] = ch
    return "".join(plain)


def solve_sequence_transposition(text: str, *, keyword: str, primer: str | None = None) -> SolveResult:
    plain = sequence_transposition_decrypt(text, keyword, primer)
    actual_primer = parse_sequence_frame(text)[0] if primer is None else primer
    key = _letters(keyword)
    return SolveResult("sequence_transposition", plain, f"{key} {actual_primer}", float(len(plain)),
                       {"mode": "supplied_key", "keyword": key, "primer": actual_primer,
                        "check_digit_verified": primer is None, "source_url": ACA_SEQUENCE_TRANSPOSITION_URL,
                        "scope": "Supplied-key classical transposition; check digit is not authentication."})
