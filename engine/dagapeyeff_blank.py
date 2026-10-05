"""Seven cells of the square are empty. Not a reading.

The digit that appears once leaves four cells of its row empty in every
re-pairing. That margin is not the result. Three further cells are empty.
A re-pairing may shuffle the column digits or the row digits. The solved
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


def _zeros(row_keys: str, column_keys: str, row_seq: list[str], column_seq: list[str]) -> int:
    joint = Counter(zip(row_seq, column_seq))
    return sum(1 for row in row_keys for column in column_keys if joint.get((row, column), 0) == 0)


def _tail(row_keys: str, column_keys: str, row_seq: list[str], column_seq: list[str], observed: int, shuffle_rows: bool) -> tuple[int, int, int]:
    drawn = random.Random(_SEED)
    as_many = 0
    furthest = 0
    at_furthest = 0
    for _ in range(_DRAWS):
        if shuffle_rows:
            bag = row_seq[:]
            drawn.shuffle(bag)
            count = _zeros(row_keys, column_keys, bag, column_seq)
        else:
            bag = column_seq[:]
            drawn.shuffle(bag)
            count = _zeros(row_keys, column_keys, row_seq, bag)
        if count > furthest:
            furthest = count
            at_furthest = 0
        if count == furthest:
            at_furthest += 1
        if count >= observed:
            as_many += 1
    return as_many, furthest, at_furthest


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("blank")
def blank_report() -> dict:
    pairs = list(challenge_pairs())
    row_seq = [pair[0] for pair in pairs]
    column_seq = [pair[1] for pair in pairs]
    joint = Counter(zip(row_seq, column_seq))
    empty = [row + column for row in _ROWS for column in _COLUMNS if joint.get((row, column), 0) == 0]
    once = min(_ROWS, key=row_seq.count)
    further = [cell for cell in empty if cell[0] != once]
    column_as_many, column_furthest, column_at_furthest = _tail(
        _ROWS, _COLUMNS, row_seq, column_seq, len(empty), False
    )
    row_as_many, row_furthest, row_at_furthest = _tail(
        _ROWS, _COLUMNS, row_seq, column_seq, len(empty), True
    )
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_rows = [pair[0] for pair in control]
    control_columns = [pair[1] for pair in control]
    control_empty = _zeros(alphabet, alphabet, control_rows, control_columns)
    control_column_as_many, _, _ = _tail(
        alphabet, alphabet, control_rows, control_columns, control_empty, False
    )
    control_row_as_many, _, _ = _tail(
        alphabet, alphabet, control_rows, control_columns, control_empty, True
    )
    allowed = column_as_many * 20 < _DRAWS and row_as_many * 20 < _DRAWS
    return {
        "solved": False,
        "claimed_plaintext": None,
        "empty": len(empty),
        "once_digit": once,
        "once_empty": len(empty) - len(further),
        "further": further,
        "draws": _DRAWS,
        "column_as_many": column_as_many,
        "column_furthest": column_furthest,
        "column_at_furthest": column_at_furthest,
        "row_as_many": row_as_many,
        "row_furthest": row_furthest,
        "row_at_furthest": row_at_furthest,
        "exercise_empty": control_empty,
        "exercise_column_as_many": control_column_as_many,
        "exercise_row_as_many": control_row_as_many,
        "allowed": allowed,
        "scope": "Seven empty cells are not a reading. No letter string is stored.",
    }
