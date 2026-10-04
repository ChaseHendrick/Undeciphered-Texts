"""Which column the order actually depends on. Not a reading.

Each column is deleted in turn and the remaining cells are scored by how
well one predicts the next. The same fourteen deletions are tried on
shuffled grids. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_swarm import challenge_pairs
from engine.stats import successive_information

_SEED = 20261004
_DRAWS = 10000
_WIDTH = 14


def _drop(seq: list[str], column: int) -> list[str]:
    return [symbol for index, symbol in enumerate(seq) if index % _WIDTH != column]


def _scores(seq: list[str]) -> list[float]:
    return [successive_information(_drop(seq, column)) for column in range(_WIDTH)]


def bearing_report() -> dict:
    pairs = list(challenge_pairs())
    scores = _scores(pairs)
    lowest = min(range(_WIDTH), key=lambda column: scores[column])
    gap = max(scores) - min(scores)
    drawn = random.Random(_SEED)
    as_low = 0
    gap_as_wide = 0
    target = scores[13]
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        trial = _scores(shuffled)
        if min(trial) <= target + 1e-15:
            as_low += 1
        if max(trial) - min(trial) >= gap - 1e-15:
            gap_as_wide += 1
    kept = len(pairs) - len(pairs) // _WIDTH
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _DRAWS * _WIDTH,
        "scores": tuple(round(score, 4) for score in scores),
        "lowest_column": lowest,
        "lowest_mi": round(scores[lowest], 4),
        "next_lowest_mi": round(sorted(scores)[1], 4),
        "highest_column": max(range(_WIDTH), key=lambda column: scores[column]),
        "highest_mi": round(max(scores), 4),
        "full_mi": round(successive_information(pairs), 4),
        "english_mi": round(successive_information(_prose("english.txt", kept)), 4),
        "as_low": as_low,
        "gap_as_wide": gap_as_wide,
        "draws": _DRAWS,
        "scope": (
            "A column the order depends on is not a reading. "
            "Same-length English is still the yardstick. No letter string is stored."
        ),
    }
