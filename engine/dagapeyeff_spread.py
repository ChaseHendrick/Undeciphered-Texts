"""The most uneven row of the square. Not a reading.

Unevenness is five times the sum of squared deviations, an integer. A
re-pairing keeps both digit totals. Columns use the same rule. The solved
exercise is scored on its own letters. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_ROWS = "67890"
_COLUMNS = "12345"


def _grid(rows: list[str], columns: list[str], row_keys: str, column_keys: str) -> list[list[int]]:
    joint = Counter(zip(rows, columns))
    return [[joint.get((row, column), 0) for column in column_keys] for row in row_keys]


def _spread(line: list[int]) -> int:
    total = sum(line)
    squares = sum(value * value for value in line)
    return 5 * squares - total * total


def _most(grid: list[list[int]], across: bool) -> tuple[int, list[int]]:
    if across:
        lines = grid
    else:
        lines = [[grid[row][column] for row in range(len(grid))] for column in range(len(grid[0]))]
    best = max(lines, key=_spread)
    return _spread(best), best


def _as_uneven(rows: list[str], columns: list[str], row_keys: str, column_keys: str, row_mark: int, column_mark: int) -> tuple[int, int, int]:
    drawn = random.Random(_SEED)
    row_hits = 0
    column_hits = 0
    either_hits = 0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        grid = _grid(rows, shuffled, row_keys, column_keys)
        row_hit = _most(grid, True)[0] >= row_mark
        column_hit = _most(grid, False)[0] >= column_mark
        row_hits += row_hit
        column_hits += column_hit
        either_hits += row_hit or column_hit
    return row_hits, column_hits, either_hits


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("spread")
def spread_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    grid = _grid(rows, columns, _ROWS, _COLUMNS)
    row_spread, row_line = _most(grid, True)
    column_spread, column_line = _most(grid, False)
    row_hits, column_hits, either_hits = _as_uneven(rows, columns, _ROWS, _COLUMNS, row_spread, column_spread)
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_rows = [pair[0] for pair in control]
    control_columns = [pair[1] for pair in control]
    control_grid = _grid(control_rows, control_columns, alphabet, alphabet)
    control_spread, control_line = _most(control_grid, True)
    control_column_spread, control_column_line = _most(control_grid, False)
    control_hits, control_column_hits, control_either = _as_uneven(
        control_rows, control_columns, alphabet, alphabet, control_spread, control_column_spread
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "row_line": row_line,
        "row_spread": row_spread,
        "column_line": column_line,
        "column_spread": column_spread,
        "draws": _DRAWS,
        "rows_as_uneven": row_hits,
        "columns_as_uneven": column_hits,
        "either_as_uneven": either_hits,
        "control_line": control_line,
        "control_spread": control_spread,
        "control_column_line": control_column_line,
        "control_column_spread": control_column_spread,
        "control_rows_as_uneven": control_hits,
        "control_columns_as_uneven": control_column_hits,
        "control_either_as_uneven": control_either,
        "scope": (
            "An uneven row is not a reading. "
            "No letter string is stored."
        ),
    }
