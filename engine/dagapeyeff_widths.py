"""Every column width of the 392 digits. Not a reading.

An earlier pass stopped at width 28 and found that width 3 stays on the
square. This pass finishes the widths. A width that stays legal is then
scored against random re-pairings, and against the book's solved exercise.
No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CHALLENGE, CONTROL, _digits, _pairs, best_chi_square

_SEED = 20261004
_DRAWS = 2000
_ROW = set("67890")
_COLUMN = set("12345")


def _column_read(text: str, width: int) -> str:
    rows = [text[index:index + width] for index in range(0, len(text), width)]
    out = []
    for column in range(width):
        for row in rows:
            if column < len(row):
                out.append(row[column])
    return "".join(out)


def _legal(stream: str) -> int:
    return sum(
        stream[index] in _ROW and stream[index + 1] in _COLUMN
        for index in range(0, len(stream), 2)
    )


def _digits_body() -> str:
    digits = _digits(CHALLENGE)
    if not digits.endswith("000") or len(digits) != 395:
        raise ValueError("the printed challenge is expected to be 395 digits ending in 000")
    return digits[:-3]


def _control_letters() -> str:
    letters = "".join(char for char in CONTROL if char.isalpha())
    if len(letters) != 178 or len(letters) % 2:
        raise ValueError("the solved exercise is expected to be 178 letters")
    return letters


@frozen("widths")
def widths_report() -> dict:
    digits = _digits_body()
    legal_widths = [width for width in range(1, len(digits) + 1) if _legal(_column_read(digits, width)) == 196]
    if legal_widths != [1, 3, 131, 392]:
        raise ValueError("the fully legal widths changed")
    width_131 = _column_read(digits, 131)
    pairs_131 = _pairs(width_131, "0123456789")
    chi_131 = round(best_chi_square(pairs_131), 2)
    rows = [digits[index] for index in range(0, len(digits), 2)]
    columns = [digits[index] for index in range(1, len(digits), 2)]
    drawn = random.Random(_SEED)
    as_flat = 0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        repaired = tuple(row + column for row, column in zip(rows, shuffled))
        if best_chi_square(repaired) <= chi_131 + 1e-9:
            as_flat += 1
    letters = _control_letters()
    control_printed = round(best_chi_square(_pairs(letters, "ABCDE")), 2)
    control_width_3 = round(best_chi_square(_pairs(_column_read(letters, 3), "ABCDE")), 2)
    control_width_131 = round(best_chi_square(_pairs(_column_read(letters, 131), "ABCDE")), 2)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "widths": len(digits),
        "fully_legal": legal_widths,
        "width_131_chi": chi_131,
        "re_pairings_as_flat": as_flat,
        "draws": _DRAWS,
        "control_printed_chi": control_printed,
        "control_width_3_chi": control_width_3,
        "control_width_131_chi": control_width_131,
        "scope": "A column width that stays on the square is not a reading. No letter string is stored.",
    }
