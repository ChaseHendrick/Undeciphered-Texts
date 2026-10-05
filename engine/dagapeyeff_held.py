"""The aligned runs with the rare cells held still. Not a reading.

Cells that appear at most three times stay in their seats. The other cells
are shuffled. The score is the most runs of three that share a starting
column. A second score is the number of such runs, aligned or not. The
alignment is the claim only if it stays under 5 percent and the plain
count of runs does not. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14
_RUN = 3


def _starts(seq: list[str]) -> list[int]:
    starts = []
    index = 0
    length = len(seq)
    while index < length:
        end = index
        while end + 1 < length and seq[end + 1] == seq[index] and (end + 1) % _WIDTH != 0:
            end += 1
        if end // _WIDTH == index // _WIDTH and end - index + 1 >= _RUN:
            starts.append(index % _WIDTH)
        index = end + 1
    return starts


def _shared(seq: list[str]) -> int:
    starts = _starts(seq)
    if not starts:
        return 0
    return max(Counter(starts).values())


@frozen("held")
def held_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    low = sorted(cell for cell, count in counts.items() if count <= _RUN)
    pinned = {index for index, cell in enumerate(pairs) if cell in set(low)}
    free = [index for index in range(len(pairs)) if index not in pinned]
    observed_shared = _shared(pairs)
    observed_runs = len(_starts(pairs))
    seen = random.Random(_SEED)
    as_aligned = 0
    as_many_runs = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        bag = [shuffled[index] for index in free]
        seen.shuffle(bag)
        for index, cell in zip(free, bag):
            shuffled[index] = cell
        if _shared(shuffled) >= observed_shared:
            as_aligned += 1
        if len(_starts(shuffled)) >= observed_runs:
            as_many_runs += 1
    aligned_rate = as_aligned / _DRAWS
    run_rate = as_many_runs / _DRAWS
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pinned": len(pinned),
        "low": low,
        "shared_starts": observed_shared,
        "runs": observed_runs,
        "draws": _DRAWS,
        "as_aligned": as_aligned,
        "as_many_runs": as_many_runs,
        "allowed": aligned_rate < 0.05 and run_rate >= 0.05,
        "scope": "Aligned runs with the rare cells held still are not a reading. No letter string is stored.",
    }
