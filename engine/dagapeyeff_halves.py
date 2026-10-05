"""Even and odd positions use different symbol counts. Not a reading.

The raw gap looks rare. The five extra symbols on the odd side are the
five symbols that never leave the last column, and that column is an odd
index in every row. Leave those symbols out and the gap is ordinary.
A period of 7 is scored the same way. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def _private(seq: list[str]) -> list[str]:
    found = []
    for cell in sorted(set(seq)):
        seats = [index for index, item in enumerate(seq) if item == cell]
        if seats and all(index % _WIDTH == _WIDTH - 1 for index in seats):
            found.append(cell)
    return found


def _gap(seq: list[str], period: int, skip: set[str]) -> int:
    supports = []
    length = len(seq)
    for residue in range(period):
        supports.append(len({seq[index] for index in range(residue, length, period) if seq[index] not in skip}))
    return max(supports) - min(supports)


def _supports(seq: list[str], period: int) -> list[int]:
    length = len(seq)
    return [len({seq[index] for index in range(residue, length, period)}) for residue in range(period)]


def _as_high(seq: list[str], skip: set[str], gap2: int, gap7: int, seen: random.Random) -> tuple[int, int]:
    high2 = 0
    high7 = 0
    for _ in range(_DRAWS):
        shuffled = seq[:]
        seen.shuffle(shuffled)
        if _gap(shuffled, 2, skip) >= gap2:
            high2 += 1
        if _gap(shuffled, 7, skip) >= gap7:
            high7 += 1
    return high2, high7


@frozen("halves")
def halves_report() -> dict:
    pairs = list(challenge_pairs())
    private = _private(pairs)
    even, odd = _supports(pairs, 2)
    gap2 = _gap(pairs, 2, set())
    gap7 = _gap(pairs, 7, set())
    residual2 = _gap(pairs, 2, set(private))
    residual7 = _gap(pairs, 7, set(private))
    raw2, raw7 = _as_high(pairs, set(), gap2, gap7, random.Random(_SEED))
    left2, left7 = _as_high(pairs, set(private), residual2, residual7, random.Random(_SEED))
    raw_rate = raw2 / _DRAWS
    left_rate = left2 / _DRAWS
    return {
        "solved": False,
        "claimed_plaintext": None,
        "even_support": even,
        "odd_support": odd,
        "gap": gap2,
        "draws": _DRAWS,
        "as_high": raw2,
        "private": private,
        "residual_gap": residual2,
        "residual_as_high": left2,
        "period7_gap": gap7,
        "period7_as_high": raw7,
        "period7_residual_gap": residual7,
        "period7_residual_as_high": left7,
        "allowed": raw_rate < 0.05 and left_rate < 0.05,
        "scope": "A split of even and odd positions is not a reading. No letter string is stored.",
    }
