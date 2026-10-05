"""Four counts in a row that differ by one. Not a reading.

A straight is successive counts whose steps are all +1 or all -1. The
comparison keeps both digit totals and re-pairs them. Columns get the same
rule. The solved exercise is scored on its own letters. No letter string
is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 100000
_ROWS = "67890"
_COLUMNS = "12345"


def _straight(counts: list[int]) -> int:
    best = 1
    index = 0
    last = len(counts) - 1
    while index < last:
        step = counts[index + 1] - counts[index]
        if abs(step) != 1:
            index += 1
            continue
        end = index + 1
        while end < last and counts[end + 1] - counts[end] == step:
            end += 1
        best = max(best, end - index + 1)
        index = end
    return best


def _grid(rows: list[str], columns: list[str], row_keys: str, column_keys: str) -> list[list[int]]:
    joint = Counter(zip(rows, columns))
    return [[joint.get((row, column), 0) for column in column_keys] for row in row_keys]


def _longest(grid: list[list[int]], across: bool) -> int:
    if across:
        lines = grid
    else:
        lines = [[grid[row][column] for row in range(len(grid))] for column in range(len(grid[0]))]
    return max(_straight(line) for line in lines)


def _as_long(rows: list[str], columns: list[str], row_keys: str, column_keys: str, observed: int) -> tuple[int, int, int]:
    drawn = random.Random(_SEED)
    row_hits = 0
    column_hits = 0
    either_hits = 0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        grid = _grid(rows, shuffled, row_keys, column_keys)
        row_hit = _longest(grid, True) >= observed
        column_hit = _longest(grid, False) >= observed
        row_hits += row_hit
        column_hits += column_hit
        either_hits += row_hit or column_hit
    return row_hits, column_hits, either_hits


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("straight")
def straight_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    grid = _grid(rows, columns, _ROWS, _COLUMNS)
    row_length = _longest(grid, True)
    column_length = _longest(grid, False)
    row_hits, column_hits, either_hits = _as_long(rows, columns, _ROWS, _COLUMNS, row_length)
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_rows = [pair[0] for pair in control]
    control_columns = [pair[1] for pair in control]
    control_grid = _grid(control_rows, control_columns, alphabet, alphabet)
    control_length = _longest(control_grid, True)
    control_hits, _, _ = _as_long(control_rows, control_columns, alphabet, alphabet, control_length)
    strict_row = next(line for line in grid if _straight(line) == row_length)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "row_length": row_length,
        "column_length": column_length,
        "strict_row": strict_row,
        "draws": _DRAWS,
        "rows_as_long": row_hits,
        "columns_as_long": column_hits,
        "either_as_long": either_hits,
        "control_row_length": control_length,
        "control_rows_as_long": control_hits,
        "scope": (
            "A run of counts that differ by one is not a reading. "
            "No letter string is stored."
        ),
    }
