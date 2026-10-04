"""The one legal regrouping that flatters the counts. Not a reading.

Reversing the last three digits of every printed group stays on the square
and the chi-square falls near English. The same move hurts the book's solved
example. The order score of the regrouped cells is checked against shuffles
of those same cells. No letter string is stored.
"""

from __future__ import annotations

import random
from engine.dagapeyeff_cache import frozen

from engine.dagapeyeff_balls import information_ball
from engine.dagapeyeff_convert import _rate_balls, chi_ball
from engine.dagapeyeff_more import control_group_reorders
from engine.dagapeyeff_order import _down_read, _grid, _mi, _prose
from engine.dagapeyeff_swarm import CHALLENGE, challenge_pairs

_PERM = (0, 1, 4, 3, 2)
_DRAWS = 10000
_SEED = 20261004
_ENGLISH_LINE = 24.165


def regrouped_pairs() -> list[str]:
    groups = CHALLENGE.split()
    stream = "".join("".join(group[index] for index in _PERM) for group in groups)
    if not stream.endswith("000"):
        raise ValueError("the regrouped line should still end in the filler 000")
    stream = stream[:-3]
    pairs = [stream[index:index + 2] for index in range(0, len(stream), 2)]
    if len(pairs) != 196:
        raise ValueError("the regrouping should keep 196 cells")
    if any(pair[0] not in "67890" or pair[1] not in "12345" for pair in pairs):
        raise ValueError("the regrouping left the square")
    return pairs


@frozen("regroup")
def regroup_report() -> dict:
    pairs = regrouped_pairs()
    rates = _rate_balls()
    counts = chi_ball(pairs, rates)
    order = information_ball(pairs)
    printed = information_ball(list(challenge_pairs()))
    english = information_ball(list(_prose("english.txt", len(pairs))))
    grid = _grid(pairs)
    down = _mi(_down_read(grid, list(range(14))))
    row = _mi(pairs)
    drawn = random.Random(_SEED)
    sample = pairs[:]
    row_as_high = 0
    down_as_high = 0
    for _ in range(_DRAWS):
        drawn.shuffle(sample)
        score = _mi(sample)
        if score >= row:
            row_as_high += 1
        if score >= down:
            down_as_high += 1
    control = control_group_reorders()
    frequency_clears = float(counts.hi()) < _ENGLISH_LINE
    order_clears = order.hi() < english.lo()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "reorder": "01432",
        "chi_lo": round(float(counts.lo()), 6),
        "chi_hi": round(float(counts.hi()), 6),
        "frequency_clears_english_worst": frequency_clears,
        "order_mi": round(float(order.lo()), 4),
        "printed_mi": round(float(printed.lo()), 4),
        "english_mi": round(float(english.lo()), 4),
        "order_still_below_english": order_clears,
        "down_mi": round(down, 4),
        "draws": _DRAWS,
        "row_shuffles_as_high": row_as_high,
        "down_shuffles_as_high": down_as_high,
        "control_printed_chi": control["printed_chi"],
        "control_flipped_chi": control["flipped_chi"],
        "scope": (
            "A regrouping that flatters the counts and loses to a shuffle is not a reading. "
            "The changed cells are not kept. No letter string is stored."
        ),
    }
