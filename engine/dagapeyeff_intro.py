"""How long the text waits before it uses a new cell. Not a reading.

The wait is the longest gap between successive first appearances. Pair
shuffles of the same cells are the control. A second control keeps every
low-side cell, as the frequency hole defined that side, inside one column.
The book's solved exercise gets the same test. No letter string is stored.
"""

from __future__ import annotations

import random

from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_hole import hole_report
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 10000
_WIDTH = 14


def _drought(seq: list[str]) -> int:
    seen: set[str] = set()
    previous = -1
    longest = 0
    for index, symbol in enumerate(seq):
        if symbol in seen:
            continue
        longest = max(longest, index - previous)
        previous = index
        seen.add(symbol)
    return longest


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


def _given_the_hole(pairs: list[str], low_max: int, drawn: random.Random) -> list[str]:
    counts = Counter(pairs)
    low = [symbol for symbol in pairs if counts[symbol] <= low_max]
    rest = [symbol for symbol in pairs if counts[symbol] > low_max]
    grid = [""] * len(pairs)
    column = drawn.randrange(_WIDTH)
    seats = [row * _WIDTH + column for row in range(_WIDTH)]
    drawn.shuffle(seats)
    drawn.shuffle(low)
    for seat, symbol in zip(seats, low):
        grid[seat] = symbol
    empty = [index for index, symbol in enumerate(grid) if symbol == ""]
    drawn.shuffle(rest)
    for seat, symbol in zip(empty, rest):
        grid[seat] = symbol
    return grid


@frozen("intro")
def intro_report() -> dict:
    pairs = list(challenge_pairs())
    low_max = hole_report()["low_max"]
    observed = _drought(pairs)
    drawn = random.Random(_SEED)
    as_short = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _drought(shuffled) <= observed:
            as_short += 1
    drawn = random.Random(_SEED)
    hole_as_short = 0
    for _ in range(_DRAWS):
        if _drought(_given_the_hole(pairs, low_max, drawn)) <= observed:
            hole_as_short += 1
    control = _control_pairs()
    control_observed = _drought(control)
    drawn = random.Random(_SEED)
    control_as_short = 0
    for _ in range(_DRAWS):
        shuffled = control[:]
        drawn.shuffle(shuffled)
        if _drought(shuffled) <= control_observed:
            control_as_short += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(pairs),
        "distinct": len(set(pairs)),
        "longest_wait": observed,
        "draws": _DRAWS,
        "as_short": as_short,
        "low_max": low_max,
        "hole_as_short": hole_as_short,
        "control_cells": len(control),
        "control_distinct": len(set(control)),
        "control_longest_wait": control_observed,
        "control_as_short": control_as_short,
        "scope": (
            "A short wait for a new cell is not a reading. "
            "The solved exercise is the check that the wait is not special to the challenge. "
            "No letter string is stored."
        ),
    }
