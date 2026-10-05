"""The introduction wait, with the rare cells held still. Not a reading.

Cells that appear at most three times keep their seats. The other cells are
shuffled. The wait is the longest gap between successive first appearances.
A second wait ignores the rare cells, so a gap that only ends on one of
them cannot count. The short wait is kept only if both versions clear.
No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_RUN = 3


def _drought(seq: list[str], skip: set[str]) -> int:
    seen: set[str] = set()
    previous = -1
    longest = 0
    for index, symbol in enumerate(seq):
        if symbol in skip or symbol in seen:
            continue
        longest = max(longest, index - previous)
        previous = index
        seen.add(symbol)
    return longest


@frozen("heldwait")
def heldwait_report() -> dict:
    pairs = list(challenge_pairs())
    low = sorted(cell for cell, count in Counter(pairs).items() if count <= _RUN)
    rare = set(low)
    pinned = {index for index, cell in enumerate(pairs) if cell in rare}
    free = [index for index in range(len(pairs)) if index not in pinned]
    observed = _drought(pairs, set())
    skipped = _drought(pairs, rare)
    seen = random.Random(_SEED)
    as_short = 0
    skip_as_short = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        bag = [shuffled[index] for index in free]
        seen.shuffle(bag)
        for index, cell in zip(free, bag):
            shuffled[index] = cell
        if _drought(shuffled, set()) <= observed:
            as_short += 1
        if _drought(shuffled, rare) <= skipped:
            skip_as_short += 1
    rate = as_short / _DRAWS
    skip_rate = skip_as_short / _DRAWS
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pinned": len(pinned),
        "low": low,
        "draws": _DRAWS,
        "wait": observed,
        "as_short": as_short,
        "skip_wait": skipped,
        "skip_as_short": skip_as_short,
        "allowed": rate < 0.05 and skip_rate < 0.05,
        "scope": "The introduction wait with the rare cells held still is not a reading. No letter string is stored.",
    }
