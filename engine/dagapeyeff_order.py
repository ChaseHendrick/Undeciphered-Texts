"""Can any reordering of the 1939 cells behave like prose? Not a reading.

Mutual information of successive symbols is unchanged by relabeling them.
A substitution cipher cannot create dependence the order does not already
have. This swarm reorders the cells and compares that dependence with
same-length prose and with random orders. No letter string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from pathlib import Path

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_KEYS = 20000
_PERMS = 5000
_DATA = Path(__file__).resolve().parent / "data"


def _mi(seq: list[str] | str) -> float:
    count = len(seq) - 1
    joint = Counter(zip(seq, seq[1:]))
    left = Counter(seq[:-1])
    right = Counter(seq[1:])
    score = 0.0
    for (first, second), seen in joint.items():
        share = seen / count
        score += share * math.log(share / ((left[first] / count) * (right[second] / count)))
    return score


def _grid(pairs: list[str]) -> list[list[str]]:
    return [pairs[row * 14:(row + 1) * 14] for row in range(14)]


def _row_read(grid: list[list[str]], order: list[int]) -> list[str]:
    return [grid[row][column] for row in range(14) for column in order]


def _down_read(grid: list[list[str]], order: list[int]) -> list[str]:
    return [grid[row][column] for column in order for row in range(14)]


def _prose(name: str, length: int) -> str:
    text = letters_only((_DATA / name).read_text(encoding="utf-8"))
    return text[:length]


def order_report() -> dict:
    pairs = list(challenge_pairs())
    grid = _grid(pairs)
    identity = list(range(14))
    printed = _mi(pairs)
    down = _mi(_down_read(grid, identity))
    drawn = random.Random(_SEED)
    best_row = 0.0
    best_down = 0.0
    for _ in range(_KEYS):
        order = identity[:]
        drawn.shuffle(order)
        best_row = max(best_row, _mi(_row_read(grid, order)))
        best_down = max(best_down, _mi(_down_read(grid, order)))
    drawn = random.Random(_SEED)
    perm_max = 0.0
    perm_at_least = 0
    for _ in range(_PERMS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        score = _mi(shuffled)
        perm_max = max(perm_max, score)
        if score >= printed - 1e-15:
            perm_at_least += 1
    english = _prose("english.txt", len(pairs))
    german = _prose("german_excerpt.txt", len(pairs))
    relabeled = "".join(chr(65 + (ord(char) - 65 + 7) % 26) for char in english)
    book = letters_only(_PROSE)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _KEYS * 2 + _PERMS,
        "printed_mi": round(printed, 4),
        "down_mi": round(down, 4),
        "best_row_key_mi": round(best_row, 4),
        "best_down_key_mi": round(best_down, 4),
        "random_orders": _PERMS,
        "random_max_mi": round(perm_max, 4),
        "random_at_least_printed": perm_at_least,
        "english_mi": round(_mi(english), 4),
        "english_relabel_mi": round(_mi(relabeled), 4),
        "german_mi": round(_mi(german), 4),
        "book_letters": len(book),
        "book_mi": round(_mi(book), 4),
        "scope": (
            "Relabeling cannot raise this score. Same-length prose is the yardstick. "
            "The short solved exercise is reported apart because a short text inflates the score. "
            "No letter string is stored."
        ),
    }
