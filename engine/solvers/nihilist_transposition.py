"""Nihilist transposition known-key solver.

The American Cryptogram Association cipher sheet (fetched 2026-10-03)
describes Nihilist transposition:

  https://www.cryptogram.org/downloads/aca.info/ciphers/NihilistTransposition.pdf

The same numeric key is applied to rows and to columns. Plaintext is
written into an n-by-n square by rows (n at most 10). Columns are
reordered into numerical key order, then rows are reordered the same
way. Ciphertext is taken off by columns or by rows from that square,
printed in groups of five.

That sheet uses the taking-out key (LEDGE, Novice Notes). Elcy's
writing-in key is the inverse permutation; for some keys, including
2134, writing-in and taking-out are identical, and both sheet paths
print the same squares.

On that sheet the key is 2134 and the plaintext is "square needed
here". Spaces and case are not enciphered, so the 16 letters are
SQUARENEEDEDHERE. Taken off by columns the grouped ciphertext is
EQDER SEHNU EREAD E. Taken off by rows it is ERNEQ SUADE EDEHR E.
Each printed line ends with a period. That period is not a letter.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the numeric key is supplied.
It is **not** an unknown-script reading. It does **not** claim
Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick
cipher, the Voynich manuscript, or army message Nr. 86. It does not
implement the Nihilist substitution (Polybius addition) cipher.
"""

from __future__ import annotations

import math

from engine.result import SolveResult

# ACA Nihilist Transposition sheet (fetched 2026-10-03).
ACA_NIHILIST_TRANSPOSITION_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/NihilistTransposition.pdf"
)
ACA_NIHILIST_TRANSPOSITION_KEY = "2134"
ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN = "square needed here"
ACA_NIHILIST_TRANSPOSITION_PLAIN = "SQUARENEEDEDHERE"
# C1 on the sheet: taken off by columns. The trailing period is not a letter.
ACA_NIHILIST_TRANSPOSITION_CIPHER = "EQDER SEHNU EREAD E"
ACA_NIHILIST_TRANSPOSITION_CIPHER_ROWS = "ERNEQ SUADE EDEHR E"

_MAX_SIDE = 10
_GROUP = 5

_SCOPE = (
    "Known classical Nihilist transposition solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "the Zodiac ciphers, the Beale ciphers, the McCormick cipher, "
    "the Voynich manuscript, or army message Nr. 86."
)


def _letters(text: str) -> str:
    """Uppercase A-Z letters, in order. Spaces and punctuation are dropped."""
    if not isinstance(text, str):
        raise ValueError("nihilist transposition text must be a string")
    return "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())


def normalize_key(key: str) -> str:
    """Numeric key as a permutation of 1..n, one digit per row and column.

    "2134" means four rows and four columns. Taking-out order is the
    column (or row) whose digit is 1, then 2, then 3, then 4. The sheet
    allows at most 10 by 10, so n is 2 to 10.
    """
    if not isinstance(key, str):
        raise ValueError("nihilist transposition key must be a string of digits")
    digits = "".join(ch for ch in key.strip() if not ch.isspace())
    if not digits.isdigit() or len(digits) < 2 or len(digits) > _MAX_SIDE:
        raise ValueError(
            "nihilist transposition key must be 2 to 10 digits (10x10 maximum)"
        )
    if len(set(digits)) != len(digits):
        raise ValueError("nihilist transposition key digits must be unique")
    expected = "".join(str(i) for i in range(1, len(digits) + 1))
    if "".join(sorted(digits)) != expected:
        raise ValueError("nihilist transposition key must be a permutation of 1..n")
    return digits


def normalize_takeoff(takeoff: str) -> str:
    """Return "columns" or "rows"."""
    if not isinstance(takeoff, str):
        raise ValueError("nihilist transposition takeoff must be 'columns' or 'rows'")
    name = takeoff.strip().lower()
    if name in {"columns", "column", "cols", "col", "c", "vertical"}:
        return "columns"
    if name in {"rows", "row", "r", "horizontal"}:
        return "rows"
    raise ValueError("nihilist transposition takeoff must be 'columns' or 'rows'")


def _order(key: str) -> list[int]:
    """Indexes in taking-out order: digit 1 first, then 2, and so on."""
    return sorted(range(len(key)), key=lambda index: int(key[index]))


def _side_from_letters(count: int) -> int:
    if count < 1:
        raise ValueError("nihilist transposition text must contain at least one letter")
    side = int(math.isqrt(count))
    if side * side != count:
        raise ValueError(
            "nihilist transposition plaintext length must be a perfect square"
        )
    if side < 2 or side > _MAX_SIDE:
        raise ValueError(
            "nihilist transposition square must be from 2 by 2 through 10 by 10"
        )
    return side


def _group(letters: str) -> str:
    """ACA groups of five. A short final group is kept."""
    return " ".join(
        letters[index : index + _GROUP] for index in range(0, len(letters), _GROUP)
    )


def _grid_from_rows(letters: str, side: int) -> list[list[str]]:
    return [list(letters[row * side : (row + 1) * side]) for row in range(side)]


def _read_rows(grid: list[list[str]]) -> str:
    return "".join("".join(row) for row in grid)


def _read_columns(grid: list[list[str]]) -> str:
    side = len(grid)
    return "".join(grid[row][col] for col in range(side) for row in range(side))


def _write_columns(letters: str, side: int) -> list[list[str]]:
    grid = [[""] * side for _ in range(side)]
    cursor = 0
    for col in range(side):
        for row in range(side):
            grid[row][col] = letters[cursor]
            cursor += 1
    return grid


def _permute_columns(grid: list[list[str]], order: list[int]) -> list[list[str]]:
    return [[row[index] for index in order] for row in grid]


def _permute_rows(grid: list[list[str]], order: list[int]) -> list[list[str]]:
    return [grid[index] for index in order]


def nihilist_transposition_encrypt(
    text: str,
    key: str,
    *,
    takeoff: str = "columns",
) -> str:
    """Encrypt with a known Nihilist transposition numeric key.

    Letters fill an n-by-n square by rows. Columns then rows are reordered
    into numerical key order (taking-out). The result is read by columns
    or by rows and grouped in fives. Spaces and punctuation are not
    enciphered.
    """
    letters = _letters(text)
    digits = normalize_key(key)
    mode = normalize_takeoff(takeoff)
    side = _side_from_letters(len(letters))
    if side != len(digits):
        raise ValueError(
            "nihilist transposition key length must equal the square side"
        )
    order = _order(digits)
    grid = _grid_from_rows(letters, side)
    grid = _permute_columns(grid, order)
    grid = _permute_rows(grid, order)
    stream = _read_columns(grid) if mode == "columns" else _read_rows(grid)
    return _group(stream)


def nihilist_transposition_decrypt(
    text: str,
    key: str,
    *,
    takeoff: str = "columns",
) -> str:
    """Decrypt with a known Nihilist transposition numeric key.

    Ciphertext refills the square by columns or by rows, then rows and
    columns are restored from numerical key order. Plaintext is the
    square read by rows. Group spaces and a trailing period are ignored.
    """
    letters = _letters(text)
    digits = normalize_key(key)
    mode = normalize_takeoff(takeoff)
    side = _side_from_letters(len(letters))
    if side != len(digits):
        raise ValueError(
            "nihilist transposition key length must equal the square side"
        )
    # Encrypt did new[j] = old[order[j]]. Restore with inv[order[j]] = j.
    order = _order(digits)
    inv = [0] * side
    for new_index, old_index in enumerate(order):
        inv[old_index] = new_index
    if mode == "columns":
        grid = _write_columns(letters, side)
    else:
        grid = _grid_from_rows(letters, side)
    grid = _permute_rows(grid, inv)
    grid = _permute_columns(grid, inv)
    return _read_rows(grid)


def solve_nihilist_transposition(
    text: str,
    *,
    key: str,
    takeoff: str = "columns",
) -> SolveResult:
    """Recover Nihilist transposition plaintext when the key is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or Nr. 86.
    """
    digits = normalize_key(key)
    mode = normalize_takeoff(takeoff)
    plain = nihilist_transposition_decrypt(text, digits, takeoff=mode)
    return SolveResult(
        method="nihilist_transposition",
        plaintext=plain,
        key=digits,
        score=float(len(plain)),
        details={
            "key": digits,
            "numeric_key": digits,
            "side": len(digits),
            "letters": len(plain),
            "takeoff": mode,
            "mode": "known_nihilist_transposition",
            "variant": "aca_taking_out",
            "scope": _SCOPE,
            "source_url": ACA_NIHILIST_TRANSPOSITION_URL,
        },
    )


__all__ = [
    "ACA_NIHILIST_TRANSPOSITION_CIPHER",
    "ACA_NIHILIST_TRANSPOSITION_CIPHER_ROWS",
    "ACA_NIHILIST_TRANSPOSITION_KEY",
    "ACA_NIHILIST_TRANSPOSITION_PLAIN",
    "ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN",
    "ACA_NIHILIST_TRANSPOSITION_URL",
    "nihilist_transposition_decrypt",
    "nihilist_transposition_encrypt",
    "normalize_key",
    "normalize_takeoff",
    "solve_nihilist_transposition",
]
