"""One digit place from each printed group, then a new pairing. Not a reading.

The last group is left out, because it holds the filler. Each of the five
places is paired on its own. A place that would put a column digit first is
turned over so the row digit leads. Shuffled groups of the same parity get
the same five places. No letter string is stored.
"""

from __future__ import annotations

import random
from functools import lru_cache

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_swarm import CHALLENGE
from engine.language import ENGLISH_ORDER, get_legacy_model

_SEED = 20261004
_NULL = 80
_ROW = "67890"
_COLUMN = "12345"


def _quad(plain_cells: list[int], logp: list[float], english: list[int]) -> float:
    if len(plain_cells) < 4:
        return float("-inf")
    counts = [0] * 25
    for cell in plain_cells:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in plain_cells]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _body() -> list[str]:
    groups = CHALLENGE.split()
    if len(groups) != 79 or any(len(group) != 5 for group in groups):
        raise ValueError("the challenge is expected to be 79 groups of five")
    return groups[:-1]


def _cells(digits: str) -> list[int] | None:
    if len(digits) % 2:
        return None
    cells = []
    for index in range(0, len(digits), 2):
        left, right = digits[index], digits[index + 1]
        if left in _COLUMN and right in _ROW:
            left, right = right, left
        if left not in _ROW or right not in _COLUMN:
            return None
        cells.append(_ROW.index(left) * 5 + _COLUMN.index(right))
    return cells


def _best(groups: list[str], logp: list[float], english: list[int]) -> tuple[float, int, int]:
    best = float("-inf")
    best_place = -1
    kept = 0
    for place in range(5):
        digits = "".join(group[place] for group in groups)
        cells = _cells(digits)
        if cells is None:
            continue
        kept += 1
        score = _quad(cells, logp, english)
        if score > best:
            best = score
            best_place = place
    return best, best_place, kept


@lru_cache(maxsize=1)
def place_report() -> dict:
    logp = get_legacy_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    groups = _body()
    best, place, kept = _best(groups, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_legacy_model().score(prose) / (len(prose) - 3)
    even = groups[0::2]
    odd = groups[1::2]
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled_even = even[:]
        shuffled_odd = odd[:]
        drawn.shuffle(shuffled_even)
        drawn.shuffle(shuffled_odd)
        mixed = []
        for left, right in zip(shuffled_even, shuffled_odd):
            mixed.append(left)
            mixed.append(right)
        score, _place, _kept = _best(mixed, logp, english)
        if score >= best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "groups": len(groups),
        "places": 5,
        "places_on_square": kept,
        "best_place": place,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "scope": "One digit place is not a reading. No letter string is stored.",
    }
