"""The mismatch that remains after the sharpest cell is set aside.

Each cell is scored by how far its count sits from the product of the two
digit totals. The sharpest cell is removed and the other cells are added.
A re-pairing may remove its own sharpest cell. The solved exercise is scored
on its own letters. No letter string is stored.
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


def _pieces(rows: list[str], columns: list[str], row_keys: str, column_keys: str) -> list[tuple[float, str]]:
    joint = Counter(zip(rows, columns))
    row_totals = Counter(rows)
    column_totals = Counter(columns)
    total = len(rows)
    pieces = []
    for row in row_keys:
        for column in column_keys:
            expect = row_totals[row] * column_totals[column]
            if expect == 0:
                continue
            count = joint.get((row, column), 0)
            piece = (total * count - expect) ** 2 / (total * expect)
            pieces.append((piece, row + column))
    pieces.sort(reverse=True)
    return pieces


def _as_large(rows: list[str], columns: list[str], row_keys: str, column_keys: str, mark: float) -> tuple[int, float]:
    drawn = random.Random(_SEED)
    hits = 0
    peak = 0.0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        pieces = _pieces(rows, shuffled, row_keys, column_keys)
        rest = sum(piece for piece, _name in pieces) - pieces[0][0]
        if rest >= mark:
            hits += 1
        if rest > peak:
            peak = rest
    return hits, peak


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("rest")
def rest_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    pieces = _pieces(rows, columns, _ROWS, _COLUMNS)
    chi = sum(piece for piece, _name in pieces)
    sharp = pieces[0][0]
    second = pieces[1][0]
    second_cell = pieces[1][1]
    rest = chi - sharp
    hits, peak = _as_large(rows, columns, _ROWS, _COLUMNS, rest)
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_rows = [pair[0] for pair in control]
    control_columns = [pair[1] for pair in control]
    control_pieces = _pieces(control_rows, control_columns, alphabet, alphabet)
    control_chi = sum(piece for piece, _name in control_pieces)
    control_sharp = control_pieces[0][0]
    control_rest = control_chi - control_sharp
    control_hits, control_peak = _as_large(
        control_rows, control_columns, alphabet, alphabet, control_rest
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "chi": round(chi, 2),
        "sharp": round(sharp, 2),
        "second_cell": second_cell,
        "second": round(second, 2),
        "rest": round(rest, 2),
        "draws": _DRAWS,
        "as_large": hits,
        "peak": round(peak, 2),
        "control_rest": round(control_rest, 2),
        "control_as_large": control_hits,
        "control_peak": round(control_peak, 2),
        "scope": (
            "A leftover mismatch is not a reading. "
            "No letter string is stored."
        ),
    }
