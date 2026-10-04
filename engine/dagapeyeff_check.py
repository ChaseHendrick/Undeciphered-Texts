"""Is the rare column a check digit of the other cells in its row? Not a reading.

The predictors are fixed: copy another column, add a neighboring pair, add
every other column, take the majority, or guess a constant. Each is scored
by how many of the 14 rows it gets right. The same search on a shuffled
target column is the control. A planted sum is detected. No letter string
is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_TARGET = 13
_ROW = "67890"
_COLUMN = "12345"


def _matrix(pairs: list[str], alphabet: str, digit: int) -> list[list[int]]:
    return [
        [alphabet.index(pairs[row * 14 + column][digit]) for column in range(14)]
        for row in range(14)
    ]


def best_match(matrix: list[list[int]], column: int = _TARGET) -> tuple[int, int]:
    """Best row-hits among the fixed predictors, and how many predictors ran."""
    size = len(matrix)
    others = [index for index in range(len(matrix[0])) if index != column]
    target = [matrix[row][column] for row in range(size)]
    best = 0
    used = 0

    def consider(predicted: list[int]) -> None:
        nonlocal best, used
        used += 1
        hits = 0
        for row in range(size):
            if predicted[row] == target[row]:
                hits += 1
        if hits > best:
            best = hits

    for source in others:
        consider([matrix[row][source] for row in range(size)])
    consider([sum(matrix[row][source] for source in others) % 5 for row in range(size)])
    consider([
        sum(matrix[row][source] if source % 2 == 0 else -matrix[row][source] for source in others) % 5
        for row in range(size)
    ])
    majority = []
    for row in range(size):
        majority.append(Counter(matrix[row][source] for source in others).most_common(1)[0][0])
    consider(majority)
    for left, right in zip(others, others[1:]):
        consider([(matrix[row][left] + matrix[row][right]) % 5 for row in range(size)])
    for guess in range(5):
        consider([guess] * size)
    return best, used


def _tail(matrix: list[list[int]], draws: int, seed: int) -> tuple[int, int, int]:
    observed, used = best_match(matrix)
    target = [matrix[row][_TARGET] for row in range(14)]
    drawn = random.Random(seed)
    as_high = 0
    for _ in range(draws):
        shuffled = target[:]
        drawn.shuffle(shuffled)
        trial = [row[:] for row in matrix]
        for row in range(14):
            trial[row][_TARGET] = shuffled[row]
        if best_match(trial)[0] >= observed:
            as_high += 1
    return observed, as_high, used


def check_report() -> dict:
    pairs = list(challenge_pairs())
    row_best, row_as_high, used = _tail(_matrix(pairs, _ROW, 0), _DRAWS, _SEED)
    column_best, column_as_high, used_again = _tail(_matrix(pairs, _COLUMN, 1), _DRAWS, _SEED + 1)
    if used != used_again:
        raise RuntimeError("the two digit streams did not use the same predictors")
    return {
        "solved": False,
        "claimed_plaintext": None,
        "predictors": used,
        "draws": _DRAWS,
        "trials": used * _DRAWS * 2,
        "row_best": row_best,
        "row_as_high": row_as_high,
        "column_best": column_best,
        "column_as_high": column_as_high,
        "scope": (
            "Matching the rare column from the rest of its row is not a reading. "
            "The predictors are fixed, and a shuffled column gets the same search. "
            "No letter string is stored."
        ),
    }
