"""Whether a row of the square steps steadily. Not a reading.

The five counts in a row are the five column digits. A line is strict when
each step changes, all in one direction. Ties do not count. The comparison
keeps both digit totals and re-pairs them. Columns are scored too. No letter
string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 100000
_ROWS = "67890"
_COLUMNS = "12345"


def _strict(counts: list[int]) -> bool:
    diffs = [right - left for left, right in zip(counts, counts[1:])]
    return all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs)


def _lines(rows: list[str], columns: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    joint = Counter(zip(rows, columns))
    by_row = [[joint.get((row, column), 0) for column in _COLUMNS] for row in _ROWS]
    by_column = [[joint.get((row, column), 0) for row in _ROWS] for column in _COLUMNS]
    return by_row, by_column


@frozen("monotone")
def monotone_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    by_row, by_column = _lines(rows, columns)
    strict_rows = [counts for counts in by_row if _strict(counts)]
    if len(strict_rows) != 1:
        raise ValueError("expected one strict row")
    drawn = random.Random(_SEED)
    rows_hit = 0
    columns_hit = 0
    either_hit = 0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        trial_rows, trial_columns = _lines(rows, shuffled)
        row_hit = any(_strict(counts) for counts in trial_rows)
        column_hit = any(_strict(counts) for counts in trial_columns)
        rows_hit += row_hit
        columns_hit += column_hit
        either_hit += row_hit or column_hit
    return {
        "solved": False,
        "claimed_plaintext": None,
        "strict_row": strict_rows[0],
        "strict_rows": len(strict_rows),
        "strict_columns": sum(_strict(counts) for counts in by_column),
        "draws": _DRAWS,
        "rows_with_one": rows_hit,
        "columns_with_one": columns_hit,
        "either_with_one": either_hit,
        "scope": (
            "A staircase in one direction is not a reading. "
            "A line chosen from either direction is not a rarer line. "
            "No letter string is stored."
        ),
    }
