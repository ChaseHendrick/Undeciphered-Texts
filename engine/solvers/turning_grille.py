"""Turning grille (Fleissner) known-stencil solver.

The American Cryptogram Association cipher sheet (fetched 2026-10-03)
describes the turning grille:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Grille.pdf

The sheet allows a square of at most 12 by 12. Openings (perforations)
are cut so that four clockwise quarter-turns cover each cell once.
The first quarter of the message is written through the openings,
left to right and top to bottom ("across"). The grille is turned 90
degrees clockwise for the second quarter, 180 degrees for the third,
and 270 degrees for the fourth. The ciphertext is the filled square
read by rows, printed in groups of five.

On that sheet the 4 by 4 stencil is reported as "1 8 10 12" (cells
numbered by rows from 1). The plaintext is "the turning grille".
Spaces and case are not written into the square, so the 16 letters
are THETURNINGGRILLE. The filled square is

  T I L U
  N R G H
  G E L T
  E N I R

and the grouped ciphertext is TILUN RGHGE LTENI R. The printed line
ends with a period. That period is not a cell.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the stencil is supplied.
It is **not** an unknown-script reading and **not** a claim about
army message Nr. 86.
"""

from __future__ import annotations

import math
import re

from engine.result import SolveResult

# ACA Grille sheet (fetched 2026-10-03).
ACA_GRILLE_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Grille.pdf"
ACA_GRILLE_STENCIL = "1 8 10 12"
ACA_GRILLE_PLAIN = "THETURNINGGRILLE"
ACA_GRILLE_SHEET_PLAIN = "the turning grille"
ACA_GRILLE_CIPHER = "TILUN RGHGE LTENI R"

# The sheet says "12x12 square maximum".
_MAX_SIDE = 12
_GROUP = 5

_SCOPE = (
    "Known classical turning-grille cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def _letters(text: str) -> str:
    """Uppercase A-Z letters, in order. Spaces and punctuation are dropped."""
    return "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())


def _rotate_cw(index: int, side: int, turns: int) -> int:
    """1-based row-major cell after `turns` clockwise quarter-turns."""
    row, col = divmod(index - 1, side)
    for _ in range(turns % 4):
        row, col = col, side - 1 - row
    return row * side + col + 1


def parse_stencil(key: str) -> tuple[int, tuple[int, ...]]:
    """Parse a stencil such as "1 8 10 12" into side length and cell numbers.

    Cells are numbered from 1, left to right and top to bottom. The four
    clockwise turns of the openings must be disjoint and must cover the
    square. The side is even, at least 2, and at most 12.
    """
    if not isinstance(key, str) or not key.strip():
        raise ValueError("turning grille stencil must list cell numbers")
    if re.search(r"[^\d\s,;]", key):
        raise ValueError("turning grille stencil must list cell numbers")
    numbers = [int(part) for part in re.findall(r"\d+", key)]
    if not numbers:
        raise ValueError("turning grille stencil must list cell numbers")
    cell_count = 4 * len(numbers)
    side = int(math.isqrt(cell_count))
    if side * side != cell_count or side < 2 or side > _MAX_SIDE or side % 2:
        raise ValueError(
            "turning grille stencil must fill an even square from 2 by 2 "
            "through 12 by 12"
        )
    if any(number < 1 or number > cell_count for number in numbers):
        raise ValueError("stencil cell is outside the square")
    if len(set(numbers)) != len(numbers):
        raise ValueError("stencil lists the same cell twice")
    seen: set[int] = set()
    for turns in range(4):
        for number in numbers:
            cell = _rotate_cw(number, side, turns)
            if cell in seen:
                raise ValueError("stencil openings overlap when the grille is turned")
            seen.add(cell)
    if len(seen) != cell_count:
        raise ValueError("stencil does not cover the square")
    return side, tuple(sorted(numbers))


def stencil_key(key: str) -> str:
    """Canonical sols form: cell numbers in ascending order, separated by spaces."""
    _side, numbers = parse_stencil(key)
    return " ".join(str(number) for number in numbers)


def _openings(numbers: tuple[int, ...], side: int, turns: int) -> list[int]:
    """1-based cells open on this turn, in across (row-major) order."""
    return sorted(_rotate_cw(number, side, turns) for number in numbers)


def _group(letters: str) -> str:
    """ACA groups of five. A short final group is kept."""
    return " ".join(letters[index : index + _GROUP] for index in range(0, len(letters), _GROUP))


def turning_grille_encrypt(text: str, key: str) -> str:
    """Encrypt with a known turning-grille stencil.

    Letters are written through the openings, across, for each clockwise
    quarter-turn. The square is then read by rows and grouped in fives.
    Spaces and punctuation in the plaintext are not enciphered.
    """
    side, numbers = parse_stencil(key)
    letters = _letters(text)
    if len(letters) != side * side:
        raise ValueError(
            f"turning grille needs {side * side} letters for a {side} by {side} square"
        )
    grid = [""] * (side * side)
    cursor = 0
    for turns in range(4):
        for cell in _openings(numbers, side, turns):
            grid[cell - 1] = letters[cursor]
            cursor += 1
    return _group("".join(grid))


def turning_grille_decrypt(text: str, key: str) -> str:
    """Decrypt with a known turning-grille stencil.

    Ciphertext letters fill the square by rows. Plaintext is read through
    the openings, across, for each clockwise quarter-turn. A trailing
    period and the spaces between groups of five are ignored.
    """
    side, numbers = parse_stencil(key)
    letters = _letters(text)
    if len(letters) != side * side:
        raise ValueError(
            f"turning grille needs {side * side} letters for a {side} by {side} square"
        )
    plain: list[str] = []
    for turns in range(4):
        for cell in _openings(numbers, side, turns):
            plain.append(letters[cell - 1])
    return "".join(plain)


def solve_turning_grille(text: str, *, key: str) -> SolveResult:
    """Recover turning-grille plaintext when the stencil is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    stencil = stencil_key(key)
    side, _numbers = parse_stencil(stencil)
    plain = turning_grille_decrypt(text, stencil)
    return SolveResult(
        method="turning_grille",
        plaintext=plain,
        key=stencil,
        score=float(len(plain)),
        details={
            "key": stencil,
            "stencil": stencil,
            "side": side,
            "turns": 4,
            "direction": "clockwise",
            "letters": len(plain),
            "mode": "known_turning_grille",
            "variant": "aca_fleissner",
            "scope": _SCOPE,
            "source_url": ACA_GRILLE_URL,
        },
    )


__all__ = [
    "ACA_GRILLE_CIPHER",
    "ACA_GRILLE_PLAIN",
    "ACA_GRILLE_SHEET_PLAIN",
    "ACA_GRILLE_STENCIL",
    "ACA_GRILLE_URL",
    "parse_stencil",
    "solve_turning_grille",
    "stencil_key",
    "turning_grille_decrypt",
    "turning_grille_encrypt",
]
