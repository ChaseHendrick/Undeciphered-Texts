"""Clerical checks on the printed groups, and the tallest line. Not a reading.

Seven check-digit rules are fixed before the shuffles. The tallest line is
the most times one symbol sits in one row or one column. A shuffle is
allowed the same seven rules and the same fourteen rows and columns.
No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CHALLENGE, _digits, challenge_pairs

_SEED = 20261004
_CHECK_DRAWS = 2000
_LINE_DRAWS = 10000
_WIDTH = 14


def _groups(pairs: list[str]) -> list[str]:
    stream = "".join(pairs) + "000"
    return [stream[index:index + 5] for index in range(0, len(stream), 5)]


def _rules(groups: list[str]) -> tuple[int, ...]:
    nums = [tuple(int(char) for char in group) for group in groups]
    middle = sum((a + b + d + e) % 10 == c for a, b, c, d, e in nums)
    last = sum((a + b + c + d) % 10 == e for a, b, c, d, e in nums)
    first = sum((b + c + d + e) % 10 == a for a, b, c, d, e in nums)
    mod9 = sum(sum(group) % 9 == 0 for group in nums)
    mod10 = sum(sum(group) % 10 == 0 for group in nums)
    linked = sum(left[4] == right[0] for left, right in zip(groups, groups[1:]))
    aligned = sum(left[0] == right[0] for left, right in zip(groups, groups[1:]))
    return (middle, last, first, mod9, mod10, linked, aligned)


def _line_modes(pairs: list[str]) -> tuple[int, int]:
    row_best = 1
    column_best = 1
    for row in range(_WIDTH):
        row_best = max(row_best, max(Counter(pairs[row * _WIDTH:(row + 1) * _WIDTH]).values()))
    for column in range(_WIDTH):
        cells = [pairs[row * _WIDTH + column] for row in range(_WIDTH)]
        column_best = max(column_best, max(Counter(cells).values()))
    return row_best, column_best


@frozen("clerical")
def clerical_report() -> dict:
    pairs = list(challenge_pairs())
    if "".join(pairs) + "000" != _digits(CHALLENGE):
        raise ValueError("the printed digits are the pairs plus the terminal 000")
    observed = _rules(_groups(pairs))
    best_rule = max(observed)
    row_mode, column_mode = _line_modes(pairs)
    line_mode = max(row_mode, column_mode)
    drawn = random.Random(_SEED)
    rule_as_high = 0
    family_as_high = 0
    for _ in range(_CHECK_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        trial = _rules(_groups(shuffled))
        if trial[2] >= observed[2]:
            rule_as_high += 1
        if max(trial) >= best_rule:
            family_as_high += 1
    drawn = random.Random(_SEED)
    row_as_high = 0
    column_as_high = 0
    line_as_high = 0
    for _ in range(_LINE_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        trial_row, trial_column = _line_modes(shuffled)
        if trial_row >= row_mode:
            row_as_high += 1
        if trial_column >= column_mode:
            column_as_high += 1
        if max(trial_row, trial_column) >= line_mode:
            line_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "groups": 79,
        "rules": len(observed),
        "rule_hits": list(observed),
        "best_rule_hits": best_rule,
        "first_digit_hits": observed[2],
        "check_draws": _CHECK_DRAWS,
        "first_digit_as_high": rule_as_high,
        "family_as_high": family_as_high,
        "row_mode": row_mode,
        "column_mode": column_mode,
        "line_draws": _LINE_DRAWS,
        "row_as_high": row_as_high,
        "column_as_high": column_as_high,
        "line_as_high": line_as_high,
        "scope": (
            "A check digit that a shuffle can reach is not a key. "
            "A line chosen after looking at rows and columns is not a rare column. "
            "No letter string is stored."
        ),
    }
