"""The fullest line that still has an empty cell. Not a reading.

A re-pairing keeps both digit totals. The chance a line of that size still
has an empty cell is an exact count, not a sample. Rows and columns use the
same rule. The solved exercise is scored on its own letters. No letter
string is stored.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import comb, gcd

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_ROWS = "67890"
_COLUMNS = "12345"


def _grid(rows: list[str], columns: list[str], row_keys: str, column_keys: str) -> list[list[int]]:
    joint = Counter(zip(rows, columns))
    return [[joint.get((row, column), 0) for column in column_keys] for row in row_keys]


def _fullest(grid: list[list[int]], across: bool) -> tuple[int, int]:
    lines = grid if across else [[grid[row][column] for row in range(len(grid))] for column in range(len(grid[0]))]
    holed = [sum(line) for line in lines if 0 in line]
    open_lines = [sum(line) for line in lines if 0 not in line]
    if not holed or not open_lines:
        raise ValueError("expected both an empty cell and a full line")
    return max(holed), max(open_lines)


def _hole_fraction(seats: int, sizes: list[int], total: int) -> tuple[int, int]:
    denominator = comb(total, seats)
    numerator = 0
    for width in range(1, len(sizes) + 1):
        sign = 1 if width % 2 else -1
        for indexes in combinations(range(len(sizes)), width):
            rest = total - sum(sizes[index] for index in indexes)
            if rest >= seats:
                numerator += sign * comb(rest, seats)
    if numerator <= 0:
        raise ValueError("the empty-cell count must be positive")
    divisor = gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("heavy")
def heavy_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    grid = _grid(rows, columns, _ROWS, _COLUMNS)
    row_full, row_open = _fullest(grid, True)
    column_full, _column_open = _fullest(grid, False)
    row_sizes = [sum(line) for line in grid]
    column_sizes = [sum(grid[row][column] for row in range(5)) for column in range(5)]
    row_num, row_den = _hole_fraction(row_full, column_sizes, len(pairs))
    open_num, open_den = _hole_fraction(row_open, column_sizes, len(pairs))
    column_num, column_den = _hole_fraction(column_full, row_sizes, len(pairs))
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_grid = _grid([pair[0] for pair in control], [pair[1] for pair in control], alphabet, alphabet)
    control_full, _control_open = _fullest(control_grid, True)
    control_columns = [sum(control_grid[row][column] for row in range(5)) for column in range(5)]
    control_num, control_den = _hole_fraction(control_full, control_columns, len(control))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "row_full": row_full,
        "row_open": row_open,
        "row_numerator": row_num,
        "row_denominator": row_den,
        "open_numerator": open_num,
        "open_denominator": open_den,
        "column_full": column_full,
        "column_numerator": column_num,
        "column_denominator": column_den,
        "control_row_full": control_full,
        "control_numerator": control_num,
        "control_denominator": control_den,
        "scope": (
            "A full row with an empty cell is not a reading. "
            "No letter string is stored."
        ),
    }
