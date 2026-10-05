"""The sandwich, with the rare cells held still. Not a reading.

Cells that appear at most three times keep their seats. The other cells are
shuffled. A sandwich is the common cell on both sides of a cell that also
has a run of three. A plain gap is the common cell on both sides of any
other cell. The plain gap is the wider score. The overlap with two aligned
runs is counted so the sandwich is not mistaken for that alignment. No
letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_sandwich import _gaps
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14
_RUN = 3


def _plain(seq: list[str], mode: str) -> int:
    found = 0
    for row in range(_WIDTH):
        for column in range(1, _WIDTH - 1):
            middle = seq[row * _WIDTH + column]
            if (
                seq[row * _WIDTH + column - 1] == mode
                and seq[row * _WIDTH + column + 1] == mode
                and middle != mode
            ):
                found += 1
    for column in range(_WIDTH):
        for row in range(1, _WIDTH - 1):
            middle = seq[row * _WIDTH + column]
            if (
                seq[(row - 1) * _WIDTH + column] == mode
                and seq[(row + 1) * _WIDTH + column] == mode
                and middle != mode
            ):
                found += 1
    return found


def _aligned(seq: list[str]) -> int:
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
    if not starts:
        return 0
    return max(Counter(starts).values())


@frozen("heldsand")
def heldsand_report() -> dict:
    pairs = list(challenge_pairs())
    observed, mode, _middle, _found = _gaps(pairs)
    plain_observed = _plain(pairs, mode)
    low = sorted(cell for cell, count in Counter(pairs).items() if count <= _RUN)
    rare = set(low)
    pinned = {index for index, cell in enumerate(pairs) if cell in rare}
    free = [index for index in range(len(pairs)) if index not in pinned]
    seen = random.Random(_SEED)
    as_many = 0
    plain_as_many = 0
    also_aligned = 0
    aligned = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        bag = [shuffled[index] for index in free]
        seen.shuffle(bag)
        for index, cell in zip(free, bag):
            shuffled[index] = cell
        has_sandwich = _gaps(shuffled)[0] >= observed
        has_aligned = _aligned(shuffled) >= 2
        if has_sandwich:
            as_many += 1
            if has_aligned:
                also_aligned += 1
        if _plain(shuffled, mode) >= plain_observed:
            plain_as_many += 1
        if has_aligned:
            aligned += 1
    rate = as_many / _DRAWS
    plain_rate = plain_as_many / _DRAWS
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pinned": len(pinned),
        "low": low,
        "mode": mode,
        "gaps": observed,
        "plain_gaps": plain_observed,
        "draws": _DRAWS,
        "as_many": as_many,
        "plain_as_many": plain_as_many,
        "also_aligned": also_aligned,
        "aligned": aligned,
        "allowed": rate < 0.05 and plain_rate >= 0.05,
        "scope": "The sandwich with the rare cells held still is not a reading. No letter string is stored.",
    }
