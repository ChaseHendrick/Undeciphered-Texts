"""Autokey on the 1939 square. Not a reading.

The key is the previous cell, not a short repeating shift and not one of
the five texts already tried. Four rules, twenty-five starting cells each.
Shuffled cells get the same four rules. No letter string is stored.
"""

from __future__ import annotations

import random
from functools import lru_cache

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004
_NULL = 40


def _quad(plain_cells: list[int], logp: list[float], english: list[int]) -> float:
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


def _decrypt(cells: list[int], seed: int, rule: str) -> list[int]:
    out = []
    previous = seed
    for cell in cells:
        if rule == "cipher-sub":
            plain = (cell - previous) % 25
            previous = cell
        elif rule == "cipher-add":
            plain = (cell + previous) % 25
            previous = cell
        elif rule == "plain-sub":
            plain = (cell - previous) % 25
            previous = plain
        else:
            plain = (cell + previous) % 25
            previous = plain
        out.append(plain)
    return out


def _best(cells: list[int], logp: list[float], english: list[int]) -> tuple[float, str]:
    best = float("-inf")
    best_rule = ""
    for rule in ("cipher-sub", "cipher-add", "plain-sub", "plain-add"):
        for seed in range(25):
            score = _quad(_decrypt(cells, seed, rule), logp, english)
            if score > best:
                best = score
                best_rule = rule
    return best, best_rule


@lru_cache(maxsize=1)
def autokey_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    best, rule = _best(cells, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score, _shuffle_rule = _best(shuffled, logp, english)
        if score >= best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "rules": 4,
        "seeds": 25,
        "best_rule": rule,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "scope": "An autokey score is not a reading. No letter string is stored.",
    }
