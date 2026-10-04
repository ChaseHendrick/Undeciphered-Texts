"""Whether the two digits in each 1939 cell are glued. Not a reading.

The row digits are one stream and the column digits are another. Each stream
is checked for order of its own. The pairs are checked against the product
of those two margins. Small expected counts make a textbook tail the wrong
tool, so the comparison is a shuffle that keeps the margins. No letter
string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter

from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_LAGS = range(1, 41)
_LAG_DRAWS = 5000


def _streams() -> tuple[list[str], list[str]]:
    pairs = challenge_pairs()
    return [pair[0] for pair in pairs], [pair[1] for pair in pairs]


def _mi(seq: list[str]) -> float:
    count = len(seq) - 1
    joint = Counter(zip(seq, seq[1:]))
    left = Counter(seq[:-1])
    right = Counter(seq[1:])
    score = 0.0
    for (first, second), seen in joint.items():
        share = seen / count
        score += share * math.log(share / ((left[first] / count) * (right[second] / count)))
    return score


def _association(rows: list[str], columns: list[str]) -> float:
    count = len(rows)
    row_counts = Counter(rows)
    column_counts = Counter(columns)
    joint = Counter(zip(rows, columns))
    score = 0.0
    for row, row_count in row_counts.items():
        for column, column_count in column_counts.items():
            expected = row_count * column_count / count
            seen = joint.get((row, column), 0)
            score += (seen - expected) ** 2 / expected
    return score


def _best_lag(seq: list[str]) -> float:
    best = 0.0
    length = len(seq)
    for lag in _LAGS:
        hits = sum(seq[index] == seq[index + lag] for index in range(length - lag))
        best = max(best, hits / (length - lag))
    return best


def glue_report() -> dict:
    rows, columns = _streams()
    joint = Counter(row + column for row, column in zip(rows, columns))
    row_mi = _mi(rows)
    column_mi = _mi(columns)
    association = _association(rows, columns)
    row_lag = _best_lag(rows)
    column_lag = _best_lag(columns)
    drawn = random.Random(_SEED)
    row_as_high = 0
    column_as_high = 0
    association_as_high = 0
    for _ in range(_DRAWS):
        shuffled_rows = rows[:]
        shuffled_columns = columns[:]
        drawn.shuffle(shuffled_rows)
        drawn.shuffle(shuffled_columns)
        if _mi(shuffled_rows) >= row_mi - 1e-15:
            row_as_high += 1
        if _mi(shuffled_columns) >= column_mi - 1e-15:
            column_as_high += 1
        if _association(rows, shuffled_columns) >= association - 1e-9:
            association_as_high += 1
    drawn = random.Random(_SEED + 1)
    row_lag_as_high = 0
    column_lag_as_high = 0
    for _ in range(_LAG_DRAWS):
        shuffled_rows = rows[:]
        shuffled_columns = columns[:]
        drawn.shuffle(shuffled_rows)
        drawn.shuffle(shuffled_columns)
        if _best_lag(shuffled_rows) >= row_lag - 1e-15:
            row_lag_as_high += 1
        if _best_lag(shuffled_columns) >= column_lag - 1e-15:
            column_lag_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(rows),
        "trials": _DRAWS * 3 + _LAG_DRAWS * 2,
        "association": round(association, 2),
        "association_as_high": association_as_high,
        "draws": _DRAWS,
        "pair_91": joint["91"],
        "pair_61": joint["61"],
        "row_mi": round(row_mi, 4),
        "column_mi": round(column_mi, 4),
        "row_as_high": row_as_high,
        "column_as_high": column_as_high,
        "row_best_lag": round(row_lag, 4),
        "column_best_lag": round(column_lag, 4),
        "row_lag_as_high": row_lag_as_high,
        "column_lag_as_high": column_lag_as_high,
        "lag_draws": _LAG_DRAWS,
        "scope": (
            "The glue is the pairing, not the order of either digit. "
            "A textbook tail is not used, because some expected counts are below one. "
            "No letter string is stored."
        ),
    }
