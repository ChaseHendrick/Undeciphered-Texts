"""Nicodemus known-key solver: columnar transposition, then Vigenere, then a 5-letter takeoff.

The American Cryptogram Association describes Nicodemus in three steps
(the sheet fetched 2026-10-02):

  https://www.cryptogram.org/downloads/aca.info/ciphers/Nicodemus.pdf

1. Column transposition. The keyword sets the width. Plaintext is written
   in rows. Columns are reordered by the alphabetical rank of the keyword.
   Repeated keyword letters keep left-to-right order (the earlier letter
   gets the smaller rank).
2. Vigenere encipherment with the same key. After the columns move, each
   column is shifted by the keyword letter now at its head. That is a
   Vigenere pass whose key is the keyword in the new column order.
3. Take off 5 letters at a time from each column in that order. If the
   last block is shorter than 5, the remaining letters are taken from
   each column in the same order.

Worked example on that sheet:

  plaintext sentence: the early bird gets the worm
  key: CAT
  ciphertext: HAYRE VGNKI XKUWM TWMUG TAH.

Key CAT ranks as C=2, A=1, T=3, so the columns move to order A, C, T and
the Vigenere key for those columns is ACT. The letter stream of the
sentence is THEEARLYBIRDGETSTHEWORM and the letter stream of the
ciphertext is HAYREVGNKIXKUWMTWMUGTAH.

A second published walk-through (CryptoCrack, fetched 2026-10-02) uses
key MONEY and the sentence "Money can't buy happiness. But it sure makes
misery easier to live with." This module reproduces that ciphertext as
well. It is not the certificate example.

  https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/nicodemus

This module is a **known classical-cipher** solver. It recovers plaintext
only when the keyword is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# ACA Nicodemus sheet (fetched 2026-10-02).
ACA_NICODEMUS_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/Nicodemus.pdf"
)
ACA_NICODEMUS_KEY = "CAT"
ACA_NICODEMUS_PLAIN = "THEEARLYBIRDGETSTHEWORM"
ACA_NICODEMUS_CIPHER = "HAYREVGNKIXKUWMTWMUGTAH"
ACA_NICODEMUS_CIPHER_GROUPED = "HAYRE VGNKI XKUWM TWMUG TAH."

# CryptoCrack user guide (fetched 2026-10-02). Not the certificate example.
CRYPTOCRACK_NICODEMUS_URL = (
    "https://sites.google.com/site/cryptocrackprogram/user-guide/"
    "cipher-types/substitution/nicodemus"
)
CRYPTOCRACK_NICODEMUS_KEY = "MONEY"
CRYPTOCRACK_NICODEMUS_PLAIN = (
    "MONEYCANTBUYHAPPINESSBUTITSUREMAKESMISERYEASIERTOLIVEWITH"
)
CRYPTOCRACK_NICODEMUS_CIPHER = (
    "IXEIXYOGBEAAUAHCOMWPWZNQGVIIWSFYYKQHXFNGGOWSFCQPGJAUFRJVG"
)

_SCOPE = (
    "Known classical Nicodemus cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)

_TAKEOFF = 5


def nicodemus_key(key: str) -> str:
    """A-Z keyword. At least one letter is required. Repeats are kept."""
    cleaned = "".join(ch for ch in letters_only(key) if "A" <= ch <= "Z")
    if not cleaned:
        raise ValueError("Nicodemus keyword must contain at least one letter")
    return cleaned


def nicodemus_letters(text: str) -> str:
    """A-Z letters only. Other characters are dropped."""
    return "".join(ch for ch in letters_only(text) if "A" <= ch <= "Z")


def column_order(key: str) -> tuple[int, ...]:
    """Original column indexes in alphabetical rank order.

    Ties break left to right, so the earlier copy of a repeated letter
    is read first.
    """
    cleaned = nicodemus_key(key)
    return tuple(sorted(range(len(cleaned)), key=lambda i: (cleaned[i], i)))


def _column_heights(n: int, width: int, order: tuple[int, ...]) -> list[int]:
    """Height of each transposed column.

    The incomplete last row, if any, fills original columns from the left
    before the columns are reordered.
    """
    base, extra = divmod(n, width)
    original = [base + (1 if index < extra else 0) for index in range(width)]
    return [original[index] for index in order]


def _write_rows(letters: str, width: int) -> list[str]:
    columns: list[list[str]] = [[] for _ in range(width)]
    for index, ch in enumerate(letters):
        columns[index % width].append(ch)
    return ["".join(column) for column in columns]


def _read_rows(columns: list[str]) -> str:
    height = max((len(column) for column in columns), default=0)
    out: list[str] = []
    for row in range(height):
        for column in columns:
            if row < len(column):
                out.append(column[row])
    return "".join(out)


def _shift_column(column: str, key_letter: str, sign: int) -> str:
    shift = (ord(key_letter) - ord("A")) * sign
    return "".join(
        chr((ord(ch) - ord("A") + shift) % 26 + ord("A")) for ch in column
    )


def _takeoff(columns: list[str]) -> str:
    """Read 5 letters from each column in order, then the next 5, and so on."""
    heights = [len(column) for column in columns]
    remaining = heights[:]
    parts: list[str] = []
    while sum(remaining):
        for index, column in enumerate(columns):
            take = min(_TAKEOFF, remaining[index])
            if take:
                start = heights[index] - remaining[index]
                parts.append(column[start : start + take])
            remaining[index] -= take
    return "".join(parts)


def _untakeoff(cipher: str, heights: list[int]) -> list[str]:
    """Inverse of the 5-letter column takeoff."""
    columns = [""] * len(heights)
    remaining = heights[:]
    pos = 0
    while sum(remaining):
        for index, left in enumerate(remaining):
            take = min(_TAKEOFF, left)
            columns[index] += cipher[pos : pos + take]
            pos += take
            remaining[index] -= take
    if pos != len(cipher) or sum(len(column) for column in columns) != len(cipher):
        raise ValueError("ciphertext length does not match the Nicodemus key")
    return columns


def nicodemus_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Nicodemus keyword. Non-letters are dropped.

    Columns are transposed, each column is Vigenere-shifted by the keyword
    letter at its new head, then ciphertext is read 5 letters per column.
    """
    letters = nicodemus_letters(text)
    if not letters:
        raise ValueError("text has no letters")
    cleaned = nicodemus_key(key)
    order = column_order(cleaned)
    original = _write_rows(letters, len(cleaned))
    transposed = [original[index] for index in order]
    reordered = "".join(cleaned[index] for index in order)
    shifted = [
        _shift_column(column, key_letter, 1)
        for column, key_letter in zip(transposed, reordered)
    ]
    return _takeoff(shifted)


def nicodemus_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Nicodemus keyword.

    Undo the 5-letter takeoff, undo the column Vigenere shifts, restore
    the original column order, and read the rows.
    """
    letters = nicodemus_letters(text)
    if not letters:
        raise ValueError("text has no letters")
    cleaned = nicodemus_key(key)
    order = column_order(cleaned)
    heights = _column_heights(len(letters), len(cleaned), order)
    transposed = _untakeoff(letters, heights)
    reordered = "".join(cleaned[index] for index in order)
    plain_transposed = [
        _shift_column(column, key_letter, -1)
        for column, key_letter in zip(transposed, reordered)
    ]
    original = [""] * len(cleaned)
    for column, index in zip(plain_transposed, order):
        original[index] = column
    return _read_rows(original)


def solve_nicodemus(text: str, *, key: str) -> SolveResult:
    """Recover Nicodemus plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    cleaned = nicodemus_key(key)
    plain_letters = nicodemus_decrypt(text, cleaned)
    rendered = (
        reinject(text, plain_letters)
        if any(not ch.isalpha() for ch in text)
        else plain_letters
    )
    order = column_order(cleaned)
    return SolveResult(
        method="nicodemus",
        plaintext=rendered,
        key=cleaned,
        score=float(len(plain_letters)),
        details={
            "key": cleaned,
            "reordered_key": "".join(cleaned[index] for index in order),
            "letters": len(nicodemus_letters(text)),
            "mode": "known_nicodemus",
            "variant": "column_transpose_vigenere_takeoff_5",
            "scope": _SCOPE,
            "source_url": ACA_NICODEMUS_URL,
        },
    )


__all__ = [
    "ACA_NICODEMUS_CIPHER",
    "ACA_NICODEMUS_CIPHER_GROUPED",
    "ACA_NICODEMUS_KEY",
    "ACA_NICODEMUS_PLAIN",
    "ACA_NICODEMUS_URL",
    "CRYPTOCRACK_NICODEMUS_CIPHER",
    "CRYPTOCRACK_NICODEMUS_KEY",
    "CRYPTOCRACK_NICODEMUS_PLAIN",
    "CRYPTOCRACK_NICODEMUS_URL",
    "column_order",
    "nicodemus_decrypt",
    "nicodemus_encrypt",
    "nicodemus_key",
    "nicodemus_letters",
    "solve_nicodemus",
]
