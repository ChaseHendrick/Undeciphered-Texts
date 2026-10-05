"""The sharpest cell in the square. Not a reading.

The score of a cell is how far its count sits from the product of the two
digit totals. The recorded cell is the sharpest of the 25, and the
re-pairings are allowed the same choice. The solved exercise is scored on
its own letters. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter
from math import gcd

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_ROWS = "67890"
_COLUMNS = "12345"


def _sharpest(rows: list[str], columns: list[str], row_keys: str, column_keys: str) -> tuple[int, int, str, int]:
    joint = Counter(zip(rows, columns))
    row_totals = Counter(rows)
    column_totals = Counter(columns)
    total = len(rows)
    best = (0, 1)
    where = ""
    observed = 0
    chi = 0.0
    for row in row_keys:
        for column in column_keys:
            expect = row_totals[row] * column_totals[column]
            if expect == 0:
                continue
            count = joint.get((row, column), 0)
            numerator = (total * count - expect) ** 2
            denominator = total * expect
            chi += numerator / denominator
            if numerator * best[1] > best[0] * denominator:
                best = (numerator, denominator)
                where = row + column
                observed = count
    return best[0], best[1], where, observed, chi


def _reduce(numerator: int, denominator: int) -> tuple[int, int]:
    divisor = gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def _as_sharp(rows: list[str], columns: list[str], row_keys: str, column_keys: str, mark: tuple[int, int]) -> tuple[int, int, int, float]:
    drawn = random.Random(_SEED)
    hits = 0
    peak = (0, 1)
    sum_x = 0.0
    sum_y = 0.0
    sum_xx = 0.0
    sum_yy = 0.0
    sum_xy = 0.0
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        numerator, denominator, _, _, chi = _sharpest(rows, shuffled, row_keys, column_keys)
        residual = (numerator / denominator) ** 0.5
        if numerator * mark[1] >= mark[0] * denominator:
            hits += 1
        if numerator * peak[1] > peak[0] * denominator:
            peak = (numerator, denominator)
        sum_x += residual
        sum_y += chi
        sum_xx += residual * residual
        sum_yy += chi * chi
        sum_xy += residual * chi
    mean_x = sum_x / _DRAWS
    mean_y = sum_y / _DRAWS
    cov = sum_xy / _DRAWS - mean_x * mean_y
    var_x = sum_xx / _DRAWS - mean_x * mean_x
    var_y = sum_yy / _DRAWS - mean_y * mean_y
    correlation = cov / (var_x * var_y) ** 0.5
    return hits, peak[0], peak[1], correlation


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("sharp")
def sharp_report() -> dict:
    pairs = list(challenge_pairs())
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    numerator, denominator, where, observed, chi = _sharpest(rows, columns, _ROWS, _COLUMNS)
    numerator, denominator = _reduce(numerator, denominator)
    hits, peak_num, peak_den, correlation = _as_sharp(rows, columns, _ROWS, _COLUMNS, (numerator, denominator))
    peak_num, peak_den = _reduce(peak_num, peak_den)
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_rows = [pair[0] for pair in control]
    control_columns = [pair[1] for pair in control]
    control_num, control_den, control_where, control_observed, _ = _sharpest(
        control_rows, control_columns, alphabet, alphabet
    )
    control_num, control_den = _reduce(control_num, control_den)
    control_hits, _, _, _ = _as_sharp(
        control_rows, control_columns, alphabet, alphabet, (control_num, control_den)
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cell": where,
        "observed": observed,
        "numerator": numerator,
        "denominator": denominator,
        "chi": round(chi, 2),
        "draws": _DRAWS,
        "as_sharp": hits,
        "peak_numerator": peak_num,
        "peak_denominator": peak_den,
        "correlation": round(correlation, 3),
        "control_cell": control_where,
        "control_observed": control_observed,
        "control_as_sharp": control_hits,
        "scope": (
            "The sharpest cell is not a reading. "
            "No letter string is stored."
        ),
    }
