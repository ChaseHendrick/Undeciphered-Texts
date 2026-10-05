"""The book's own exercise, used as a running key. Not a reading.

The two strings are the printed Polybius exercise, not a reading of the
challenge. One is what the pairs decode to. The other is the longer gloss.
Each is slid across the cells, and each is repeated to cover them. Shuffled
cells get the same slides. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.language import ENGLISH_ORDER, get_legacy_model

# Same two strings as tests/test_polybius_gronsfeld.py. The first is the
# faithful reading of the book's solved exercise. The second is its gloss.
_FAITHFUL = (
    "THENEWPLANOFATTACKINCLUDESOPERATIONSBYTHREEBOMBRSQUDRONS"
    "OVERFACTORYARYASOUTHWESTOTHERIVER"
)
_GLOSS = (
    "THENEWPLANOFATTACKINCLUDESOPERATIONSBYTHREEBOMBERSQUADRONS"
    "OVERFACTORYARYASOUTHWESTOFTHERIVER"
)
_SEED = 20261004
_NULL = 100


def _shifts(text: str) -> list[int]:
    out = []
    for char in text.upper():
        if not ("A" <= char <= "Z"):
            continue
        if char == "J":
            char = "I"
        value = ord(char) - 65
        if value > 8:
            value -= 1
        out.append(value)
    return out


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


def _best(cells: list[int], keys: list[list[int]], logp: list[float], english: list[int]) -> tuple[float, str]:
    best = float("-inf")
    best_name = ""
    count = len(cells)
    for name, key in zip(("faithful", "gloss"), keys):
        width = len(key)
        for direction in ("sub", "add"):
            for start in range(count - width + 1):
                window = cells[start : start + width]
                if direction == "sub":
                    plain = [(window[index] - key[index]) % 25 for index in range(width)]
                else:
                    plain = [(window[index] + key[index]) % 25 for index in range(width)]
                score = _quad(plain, logp, english)
                if score > best:
                    best = score
                    best_name = f"slide-{name}-{direction}"
            for direction_name, sign in (("tile-sub", -1), ("tile-add", 1)):
                plain = [(cells[index] + sign * key[index % width]) % 25 for index in range(count)]
                score = _quad(plain, logp, english)
                if score > best:
                    best = score
                    best_name = f"{direction_name}-{name}"
    return best, best_name


@frozen("bookkey")
def bookkey_report() -> dict:
    logp = get_legacy_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    keys = [_shifts(_FAITHFUL), _shifts(_GLOSS)]
    cells = _cells()
    best, name = _best(cells, keys, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_legacy_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score, _shuffle_name = _best(shuffled, keys, logp, english)
        if score >= best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "faithful_length": len(keys[0]),
        "gloss_length": len(keys[1]),
        "best_use": name,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "scope": "The book's exercise is not a reading of the challenge. No letter string is stored.",
    }
