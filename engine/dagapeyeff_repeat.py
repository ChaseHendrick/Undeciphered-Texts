"""A long run with a second run of the same cell. Not a reading.

The count is lines, rows or columns, that hold a run of at least three
and another disjoint run of at least two of that same cell. The raw count
sits just under 5 percent. Every such line already contains a long run, so
the count is also taken on shuffles that already have one. That widened
rate is not under 5 percent. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import defaultdict

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def _runs(line: list[str]) -> list[tuple[str, int]]:
    found = []
    index = 0
    while index < _WIDTH:
        end = index
        while end + 1 < _WIDTH and line[end + 1] == line[index]:
            end += 1
        found.append((line[index], end - index + 1))
        index = end + 1
    return found


def _lines(seq: list[str], axis: str) -> list[list[str]]:
    if axis == "row":
        return [seq[row * _WIDTH:(row + 1) * _WIDTH] for row in range(_WIDTH)]
    return [[seq[row * _WIDTH + column] for row in range(_WIDTH)] for column in range(_WIDTH)]


def _hits(seq: list[str]) -> list[dict]:
    found = []
    for axis in ("row", "column"):
        for index, line in enumerate(_lines(seq, axis)):
            grouped: dict[str, list[int]] = defaultdict(list)
            for cell, length in _runs(line):
                grouped[cell].append(length)
            for cell, lengths in grouped.items():
                long = sum(length >= 3 for length in lengths)
                second = sum(length >= 2 for length in lengths)
                if long >= 1 and second >= 2:
                    found.append({
                        "axis": axis,
                        "index": index,
                        "cell": cell,
                        "lengths": lengths,
                    })
    return found


def _has_long(seq: list[str], axis: str) -> bool:
    for line in _lines(seq, axis):
        for _cell, length in _runs(line):
            if length >= 3:
                return True
    return False


@frozen("repeat")
def repeat_report() -> dict:
    pairs = list(challenge_pairs())
    hits = _hits(pairs)
    seen = random.Random(_SEED)
    as_high = 0
    vertical_runs = 0
    vertical_and_feature = 0
    any_long = 0
    any_and_feature = 0
    observed = len(hits)
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        found = len(_hits(shuffled)) >= observed
        if found:
            as_high += 1
        vertical = _has_long(shuffled, "column")
        either = vertical or _has_long(shuffled, "row")
        if vertical:
            vertical_runs += 1
            if found:
                vertical_and_feature += 1
        if either:
            any_long += 1
            if found:
                any_and_feature += 1
    raw = as_high / _DRAWS
    widened = vertical_and_feature / vertical_runs if vertical_runs else 1.0
    either_rate = any_and_feature / any_long if any_long else 1.0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "lines": observed,
        "hits": hits,
        "draws": _DRAWS,
        "as_high": as_high,
        "vertical_runs": vertical_runs,
        "vertical_and_feature": vertical_and_feature,
        "any_long": any_long,
        "any_and_feature": any_and_feature,
        "allowed": raw < 0.05 and widened < 0.05 and either_rate < 0.05,
        "scope": "A second run beside a long run is not a reading. No letter string is stored.",
    }
