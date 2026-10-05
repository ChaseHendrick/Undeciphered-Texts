"""Empty cells on the two diagonals of the square. Not a reading.

The main diagonal uses the digit order as printed. The other diagonal runs
the opposite way. A re-pairing keeps both digit totals. The sum of a
diagonal was scored and does not survive both directions. The empty cells
do. The solved exercise is scored on its own letters. No letter string
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


def _grid(rows: list[str], columns: list[str], row_keys: str, column_keys: str) -> list[list[int]]:
    joint = Counter(zip(rows, columns))
    return [[joint.get((row, column), 0) for column in column_keys] for row in row_keys]


def _measure(grid: list[list[int]]) -> tuple[int, int, int, int, int]:
    main_sum = sum(grid[index][index] for index in range(5))
    anti_sum = sum(grid[index][4 - index] for index in range(5))
    main_zeros = sum(grid[index][index] == 0 for index in range(5))
    anti_zeros = sum(grid[index][4 - index] == 0 for index in range(5))
    holes = main_zeros
    for index in range(5):
        if index != 4 - index and grid[index][4 - index] == 0:
            holes += 1
    return main_sum, anti_sum, main_zeros, anti_zeros, holes


def _null(rows: list[str], columns: list[str], row_keys: str, column_keys: str, observed: tuple[int, int, int, int, int]) -> dict[str, int]:
    drawn = random.Random(_SEED)
    main_sum_as_low = 0
    sum_either = 0
    main_zeros_as_many = 0
    either_zeros_as_many = 0
    holes_as_many = 0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        main_sum, anti_sum, main_zeros, anti_zeros, holes = _measure(_grid(rows, shuffled, row_keys, column_keys))
        main_sum_as_low += main_sum <= observed[0]
        sum_either += main_sum <= observed[0] or anti_sum >= observed[1]
        main_zeros_as_many += main_zeros >= observed[2]
        either_zeros_as_many += max(main_zeros, anti_zeros) >= max(observed[2], observed[3])
        holes_as_many += holes >= observed[4]
    return {
        "main_sum_as_low": main_sum_as_low,
        "sum_either": sum_either,
        "main_zeros_as_many": main_zeros_as_many,
        "either_zeros_as_many": either_zeros_as_many,
        "holes_as_many": holes_as_many,
    }


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("diagonal")
def diagonal_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    observed = _measure(_grid(rows, columns, _ROWS, _COLUMNS))
    counts = _null(rows, columns, _ROWS, _COLUMNS, observed)
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_rows = [pair[0] for pair in control]
    control_columns = [pair[1] for pair in control]
    control_observed = _measure(_grid(control_rows, control_columns, alphabet, alphabet))
    control_counts = _null(control_rows, control_columns, alphabet, alphabet, control_observed)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "main_sum": observed[0],
        "anti_sum": observed[1],
        "main_zeros": observed[2],
        "anti_zeros": observed[3],
        "holes": observed[4],
        "draws": _DRAWS,
        **counts,
        "control_main_zeros": control_observed[2],
        "control_anti_zeros": control_observed[3],
        "control_either_zeros_as_many": control_counts["either_zeros_as_many"],
        "scope": (
            "Empty cells on a diagonal are not a reading. "
            "No letter string is stored."
        ),
    }
