"""Dictionary letter-patterns slid across the cells. Not a reading.

A word with a repeated letter has a shape. A window of cells matches that
shape, or it does not. Words with no repeated letter are skipped, because
they match too easily. The lexicon words are not kept. A shuffle of the
same cells is the control.
"""

from __future__ import annotations

import random
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_order import _down_read, _grid
from engine.dagapeyeff_regroup import regrouped_pairs
from engine.dagapeyeff_swarm import challenge_pairs

_LEXICON = Path(__file__).resolve().parent / "data" / "tridigital_lexicon.txt"
_SEED = 20261004
_LENGTHS = range(7, 12)
_DRAWS = {
    "printed": 100_000,
    "down": 50_000,
    "regrouped": 50_000,
}


def _pattern(seq: list[str] | str) -> tuple[int, ...]:
    seen: dict[str, int] = {}
    out = []
    for item in seq:
        index = seen.get(item)
        if index is None:
            index = len(seen)
            seen[item] = index
        out.append(index)
    return tuple(out)


def _shapes() -> set[tuple[int, tuple[int, ...]]]:
    found = set()
    for line in _LEXICON.read_text(encoding="utf-8").splitlines():
        word = line.strip().upper()
        if not word.isalpha() or len(word) not in _LENGTHS:
            continue
        if len(set(word)) == len(word):
            continue
        found.add((len(word), _pattern(word)))
    return found


def _hits(seq: list[str], shapes: set[tuple[int, tuple[int, ...]]]) -> int:
    hits = 0
    last = len(seq)
    for length in _LENGTHS:
        stop = last - length + 1
        for start in range(stop):
            if (length, _pattern(seq[start : start + length])) in shapes:
                hits += 1
    return hits


def _null(seq: list[str], shapes: set[tuple[int, tuple[int, ...]]], draws: int, seed: int, real: int) -> dict:
    drawn = random.Random(seed)
    sample = seq[:]
    as_high = 0
    below = 0
    for _ in range(draws):
        drawn.shuffle(sample)
        score = _hits(sample, shapes)
        if score >= real:
            as_high += 1
        if score < real:
            below += 1
    return {"draws": draws, "as_high": as_high, "below": below}


@lru_cache(maxsize=1)
def pattern_report() -> dict:
    shapes = _shapes()
    printed = list(challenge_pairs())
    down = _down_read(_grid(printed), list(range(14)))
    regrouped = regrouped_pairs()
    windows = sum(len(printed) - length + 1 for length in _LENGTHS)
    printed_hits = _hits(printed, shapes)
    down_hits = _hits(down, shapes)
    regrouped_hits = _hits(regrouped, shapes)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "shapes": len(shapes),
        "windows": windows,
        "printed_hits": printed_hits,
        "down_hits": down_hits,
        "regrouped_hits": regrouped_hits,
        "printed_null": _null(printed, shapes, _DRAWS["printed"], _SEED, printed_hits),
        "down_null": _null(printed, shapes, _DRAWS["down"], _SEED + 1, down_hits),
        "regrouped_null": _null(regrouped, shapes, _DRAWS["regrouped"], _SEED + 2, regrouped_hits),
        "scope": (
            "A window count is not a word, and a word is not a reading. "
            "No letter string is stored."
        ),
    }
