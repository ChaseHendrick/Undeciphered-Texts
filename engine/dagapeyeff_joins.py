"""How much of the order sits on each column's joins. Not a reading.

Every adjacent pair contributes a piece of the score. A column's share is
the sum of the pieces that touch it. A pair between two columns is counted
for both, so the shares are not a partition. No letter string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter

from engine.dagapeyeff_swarm import challenge_pairs
from engine.stats import successive_information

_SEED = 20261004
_DRAWS = 10000
_WIDTH = 14


def _terms(seq: list[str]) -> list[float]:
    count = len(seq) - 1
    joint = Counter(zip(seq, seq[1:]))
    left = Counter(seq[:-1])
    right = Counter(seq[1:])
    terms = []
    for index in range(count):
        first = seq[index]
        second = seq[index + 1]
        seen = joint[(first, second)]
        share = seen / count
        piece = share * math.log(share / ((left[first] / count) * (right[second] / count)))
        terms.append(piece / seen)
    return terms


def _shares(seq: list[str]) -> list[float]:
    terms = _terms(seq)
    shares = []
    for column in range(_WIDTH):
        total = 0.0
        for index, piece in enumerate(terms):
            if index % _WIDTH == column or (index + 1) % _WIDTH == column:
                total += piece
        shares.append(total)
    return shares


def join_report() -> dict:
    pairs = list(challenge_pairs())
    shares = _shares(pairs)
    ranked = sorted(range(_WIDTH), key=lambda column: shares[column], reverse=True)
    drawn = random.Random(_SEED)
    target = shares[13]
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if max(_shares(shuffled)) >= target - 1e-12:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _DRAWS * _WIDTH,
        "full_mi": round(successive_information(pairs), 4),
        "shares": tuple(round(share, 4) for share in shares),
        "highest_column": ranked[0],
        "second_column": ranked[1],
        "third_column": ranked[2],
        "highest_share": round(shares[ranked[0]], 4),
        "second_share": round(shares[ranked[1]], 4),
        "third_share": round(shares[ranked[2]], 4),
        "as_high": as_high,
        "draws": _DRAWS,
        "scope": (
            "A column that carries more of the order than a shuffled grid allows "
            "is not a reading. The shares overlap wherever two columns meet. "
            "No letter string is stored."
        ),
    }
