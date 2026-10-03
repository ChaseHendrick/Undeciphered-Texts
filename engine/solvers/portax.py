"""Portax (digraphic Porta) known-key solver.

The American Cryptogram Association sheet describes a two-alphabet slide.
A1 is A-M over a sliding N-Z. A2 is the alphabet written in columns of two
(ACE... over BDF...). The keyword letter under A sets the slide. A and B
share one setting, C and D the next, through Y and Z. Plaintext is written
in rows under the keyword. Vertical pairs are enciphered as the other
corners of the rectangle on that slide, top letter first. A pair already
in one column takes the other two letters of that column. Ciphertext is
read by rows. The map is an involution, so the same step decrypts.

  https://www.cryptogram.org/downloads/aca.info/ciphers/Portax.pdf

This module encrypts and decrypts only when the keyword is supplied.
It is a known classical-cipher helper for that published example. It does
not read an unknown script and it does not claim Kryptos K4, Zodiac,
Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.result import SolveResult

# ACA Portax sheet (fetched 2026-10-03). Keyword EASY.
# Printed plaintext: "the early bird gets the worm"
# The sheet pads the last cell with x. Printed ciphertext:
# NIJAM PBGQC WKHQJ EUIKY MPAT.
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Portax.pdf"
ACA_KEY = "EASY"
ACA_MESSAGE = "the early bird gets the worm"
ACA_PLAIN = "THEEARLYBIRDGETSTHEWORMX"
ACA_CIPHER = "NIJAMPBGQCWKHQJEUIKYMPAT"
ACA_PRINTED_CIPHER = "NIJAM PBGQC WKHQJ EUIKY MPAT"

_SCOPE = (
    "Known classical Portax cipher solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."
)

_A2_TOP = [chr(65 + 2 * j) for j in range(13)]
_A2_BOT = [chr(66 + 2 * j) for j in range(13)]


def portax_key(key: str) -> str:
    """A-Z keyword. Non-letters are dropped. At least one letter is required."""
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("Portax key must contain at least one letter")
    return cleaned


def portax_key_index(key_letter: str) -> int:
    """Slide index 0..12. A and B share 0; Y and Z share 12."""
    letter = letters_only(key_letter)
    if len(letter) != 1:
        raise ValueError("Portax slide selector must be one letter")
    return (ord(letter) - 65) // 2


def _slide(key_index: int) -> tuple[dict[str, tuple[int, int]], dict[str, tuple[int, int]], list[list[str]], list[list[str]]]:
    """Upper (A1) and lower (A2) grids for one keyword letter, 13 columns."""
    upper_at: dict[str, tuple[int, int]] = {}
    lower_at: dict[str, tuple[int, int]] = {}
    upper = [[""] * 13 for _ in range(2)]
    lower = [[""] * 13 for _ in range(2)]
    for col in range(13):
        upper[0][col] = chr(65 + col)
        upper[1][col] = chr(ord("N") + (col + key_index) % 13)
        lower[0][col] = _A2_TOP[(key_index + col) % 13]
        lower[1][col] = _A2_BOT[(key_index + col) % 13]
        upper_at[upper[0][col]] = (0, col)
        upper_at[upper[1][col]] = (1, col)
        lower_at[lower[0][col]] = (0, col)
        lower_at[lower[1][col]] = (1, col)
    return upper_at, lower_at, upper, lower


def portax_pair(top: str, bottom: str, key_letter: str) -> str:
    """Encipher one vertical pair. The same call deciphers it.

    Top is read in A1, bottom in A2. Different columns swap columns and
    keep the sub-row. The same column takes the other two letters, upper
    letter first.
    """
    pair = letters_only(top + bottom)
    if len(pair) != 2:
        raise ValueError("Portax pair expects two letters")
    upper_at, lower_at, upper, lower = _slide(portax_key_index(key_letter))
    top_row, top_col = upper_at[pair[0]]
    bot_row, bot_col = lower_at[pair[1]]
    if top_col == bot_col:
        cipher_top = upper[1 - top_row][top_col]
        cipher_bot = lower[1 - bot_row][bot_col]
    else:
        cipher_top = upper[top_row][bot_col]
        cipher_bot = lower[bot_row][top_col]
    return cipher_top + cipher_bot


def _rows(letters: str, period: int) -> list[list[str]]:
    if len(letters) % period != 0:
        raise ValueError("Portax letter count must fill the keyword width")
    row_count = len(letters) // period
    if row_count % 2 != 0:
        raise ValueError("Portax needs an even number of rows for vertical pairs")
    return [
        list(letters[row * period : (row + 1) * period])
        for row in range(row_count)
    ]


def _apply_rows(grid: list[list[str]], keyword: str) -> str:
    period = len(keyword)
    for row in range(0, len(grid), 2):
        for col in range(period):
            paired = portax_pair(grid[row][col], grid[row + 1][col], keyword[col])
            grid[row][col] = paired[0]
            grid[row + 1][col] = paired[1]
    return "".join("".join(line) for line in grid)


def portax_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Portax keyword.

    Non-letters are dropped. A final incomplete block is filled with X so
    the width is the keyword and the row count is even, matching the x
    on the ACA sheet.
    """
    keyword = portax_key(key)
    period = len(keyword)
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    block = 2 * period
    pad = (-len(letters)) % block
    letters += "X" * pad
    return _apply_rows(_rows(letters, period), keyword)


def portax_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Portax keyword.

    The sheet's map is its own inverse. Ciphertext must already be a
    complete block (keyword width, even row count). No pad is added.
    """
    keyword = portax_key(key)
    period = len(keyword)
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    if len(letters) % (2 * period) != 0:
        raise ValueError("Portax ciphertext must fill an even number of keyword rows")
    return _apply_rows(_rows(letters, period), keyword)


def solve_portax(text: str, *, key: str) -> SolveResult:
    """Recover Portax plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army
    message Nr. 86.
    """
    keyword = portax_key(key)
    plain_letters = portax_decrypt(text, keyword)
    return SolveResult(
        method="portax",
        plaintext=plain_letters,
        key=keyword,
        score=float(len(plain_letters)),
        details={
            "key": keyword,
            "period": len(keyword),
            "letters": len(letters_only(text)),
            "mode": "known_keyword",
            "scope": _SCOPE,
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_KEY",
    "ACA_MESSAGE",
    "ACA_PLAIN",
    "ACA_PRINTED_CIPHER",
    "ACA_URL",
    "portax_decrypt",
    "portax_encrypt",
    "portax_key",
    "portax_key_index",
    "portax_pair",
    "solve_portax",
]
