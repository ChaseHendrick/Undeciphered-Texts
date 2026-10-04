"""The largest hole in the cell frequencies, and the 2026 period-7 claim. Not a reading.

The hole is the unique largest jump between occupied frequencies. The cells
on the low side of that jump are then counted in column 14, the column named
in 2014, not a column this search picked. The period-7 claim is the pair
repeat rate at lag 7, scored against pair shuffles. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter
from math import comb, gcd

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 2000
_WIDTH = 14
_NAMED = 13


def _reduced(numerator: int, denominator: int) -> tuple[int, int]:
    scale = gcd(numerator, denominator)
    return numerator // scale, denominator // scale


def _occupied(pairs: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(sorted(set(Counter(pairs).values())))


def _largest_gap(occupied: tuple[int, ...]) -> tuple[int, int, int]:
    gaps = [right - left for left, right in zip(occupied, occupied[1:])]
    if not gaps or gaps.count(max(gaps)) != 1:
        raise ValueError("the largest frequency gap must exist and be unique")
    index = gaps.index(max(gaps))
    return occupied[index], occupied[index + 1], gaps[index]


def _kappa(pairs: list[str], lag: int) -> float:
    return sum(left == right for left, right in zip(pairs, pairs[lag:])) / (len(pairs) - lag)


@frozen("hole")
def hole_report() -> dict:
    pairs = challenge_pairs()
    counts = Counter(pairs)
    occupied = _occupied(pairs)
    low_max, high_min, gap = _largest_gap(occupied)
    low = [index for index, pair in enumerate(pairs) if counts[pair] <= low_max]
    high = [index for index, pair in enumerate(pairs) if counts[pair] == high_min]
    already = [index for index, pair in enumerate(pairs) if counts[pair] <= 2]
    fresh = [index for index, pair in enumerate(pairs) if counts[pair] == low_max and low_max > 2]
    if any(index % _WIDTH != _NAMED for index in low):
        in_named = sum(index % _WIDTH == _NAMED for index in low)
    else:
        in_named = len(low)
    full_num, full_den = _reduced(comb(_WIDTH, len(low)), comb(len(pairs), len(low)))
    seats = _WIDTH - len(already)
    rest = len(pairs) - len(already)
    step_num, step_den = _reduced(comb(seats, len(fresh)), comb(rest, len(fresh)))
    high_in_named = sum(index % _WIDTH == _NAMED for index in high)
    observed = _kappa(list(pairs), 7)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = list(pairs)
        drawn.shuffle(shuffled)
        if _kappa(shuffled, 7) >= observed - 1e-15:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "occupied": occupied,
        "low_max": low_max,
        "high_min": high_min,
        "gap": gap,
        "low_cells": len(low),
        "low_in_named_column": in_named,
        "full_numerator": full_num,
        "full_denominator": full_den,
        "already_recorded_cells": len(already),
        "new_cells": len(fresh),
        "step_numerator": step_num,
        "step_denominator": step_den,
        "high_cells": len(high),
        "high_in_named_column": high_in_named,
        "period7_draws": _DRAWS,
        "period7_as_high": as_high,
        "scope": (
            "Column 14 was named in 2014. The low side is the unique largest frequency gap, "
            "not a cutoff slid until the count looked rare. "
            "The period-7 pair rate is a published claim, not a lag chosen here. "
            "No letter string is stored."
        ),
    }
