"""The order score, counted once, by the column a pair starts in. Not a reading.

The earlier column shares counted a boundary pair twice. Here each pair is
counted for the column it starts in, so the fourteen numbers add up to the
whole score. No letter string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter

from engine.dagapeyeff_private import private_columns
from engine.dagapeyeff_swarm import challenge_pairs
from engine.stats import successive_information

_SEED = 20261004
_DRAWS = 10000
_WIDTH = 14


def _outgoing(seq: list[str]) -> list[float]:
    count = len(seq) - 1
    joint = Counter(zip(seq, seq[1:]))
    left = Counter(seq[:-1])
    right = Counter(seq[1:])
    shares = [0.0] * _WIDTH
    for index in range(count):
        first = seq[index]
        second = seq[index + 1]
        seen = joint[(first, second)]
        share = seen / count
        piece = share * math.log(share / ((left[first] / count) * (right[second] / count)))
        shares[index % _WIDTH] += piece / seen
    return shares


def _private_outgoing(seq: list[str], banned: set[str]) -> list[float]:
    count = len(seq) - 1
    joint = Counter(zip(seq, seq[1:]))
    left = Counter(seq[:-1])
    right = Counter(seq[1:])
    shares = [0.0] * _WIDTH
    for index in range(count):
        first = seq[index]
        second = seq[index + 1]
        if first not in banned and second not in banned:
            continue
        seen = joint[(first, second)]
        share = seen / count
        piece = share * math.log(share / ((left[first] / count) * (right[second] / count)))
        shares[index % _WIDTH] += piece / seen
    return shares


def outgoing_report() -> dict:
    pairs = list(challenge_pairs())
    shares = _outgoing(pairs)
    banned = {symbol for symbol, _column, _count in private_columns(pairs)}
    private = _private_outgoing(pairs, banned)
    ranked = sorted(range(_WIDTH), key=lambda column: shares[column], reverse=True)
    drawn = random.Random(_SEED)
    target = max(shares)
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if max(_outgoing(shuffled)) >= target - 1e-12:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _DRAWS * _WIDTH,
        "full_mi": round(successive_information(pairs), 4),
        "outgoing": tuple(round(share, 4) for share in shares),
        "outgoing_sum": round(sum(shares), 4),
        "highest_column": ranked[0],
        "highest": round(shares[ranked[0]], 4),
        "second_column": ranked[1],
        "second": round(shares[ranked[1]], 4),
        "private_from_12": round(private[12], 4),
        "private_from_13": round(private[13], 4),
        "as_high": as_high,
        "draws": _DRAWS,
        "scope": (
            "Counting each pair once shows the seam score is the private symbols, "
            "not a second pattern in the ordinary cells. It is not a reading. "
            "No letter string is stored."
        ),
    }
