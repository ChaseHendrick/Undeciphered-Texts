"""Which measurements can see structure in the 1939 challenge. Not a reading.

Each method gets the same seed and thousands of null trials. A method works
when the challenge lands where that null almost never lands, and when the
book's solved example is accepted by the same measurement. Letters are not kept.
"""

from __future__ import annotations

import random
import statistics
from collections import Counter
from math import exp, lgamma

from engine.dagapeyeff_swarm import (
    CONTROL,
    ENGLISH_25,
    _pairs,
    best_chi_square,
    challenge_pairs,
    digram_excess,
)

_SEED = 20261004
_WIDTHS = range(2, 29)
_BIG = 10000
_HALF = 5000
_GAP = 2000
_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
_TAIL: dict[tuple[int, int, int, int], float] = {}


def _log_comb(total: int, choose: int) -> float:
    if choose < 0 or choose > total:
        return float("-inf")
    return lgamma(total + 1) - lgamma(choose + 1) - lgamma(total - choose + 1)


def _tail(population: int, marked: int, draw: int, observed: int) -> float:
    key = (population, marked, draw, observed)
    cached = _TAIL.get(key)
    if cached is not None:
        return cached
    if observed <= 0:
        _TAIL[key] = 1.0
        return 1.0
    log_denom = _log_comb(population, draw)
    total = 0.0
    for count in range(observed, min(marked, draw) + 1):
        total += exp(_log_comb(marked, count) + _log_comb(population - marked, draw - count) - log_denom)
    _TAIL[key] = total
    return total


def _rarest_p(seq: list[str], marked_symbols: set[str]) -> tuple[float, int, int]:
    """Smallest column probability over widths 2..28. Returns p, width, column."""
    marked = sum(symbol in marked_symbols for symbol in seq)
    best = 1.0
    where = (0, 0)
    length = len(seq)
    for width in _WIDTHS:
        hits = [0] * width
        draws = [0] * width
        for index, symbol in enumerate(seq):
            column = index % width
            draws[column] += 1
            if symbol in marked_symbols:
                hits[column] += 1
        for column in range(width):
            score = _tail(length, marked, draws[column], hits[column])
            if score < best:
                best = score
                where = (width, column)
    return best, where[0], where[1]


def _gap_cv(seq: list[str], symbol: str) -> float:
    indexes = [index for index, item in enumerate(seq) if item == symbol]
    gaps = [indexes[index + 1] - indexes[index] for index in range(len(indexes) - 1)]
    return statistics.pstdev(gaps) / (sum(gaps) / len(gaps))


def method_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    rare = {symbol for symbol, count in counts.items() if count <= 2}
    observed_p, width, column = _rarest_p(pairs, rare)
    drawn = random.Random(_SEED)
    width_hits = 0
    for _ in range(_BIG):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        score, _, _ = _rarest_p(shuffled, rare)
        if score <= observed_p * (1 + 1e-9):
            width_hits += 1

    printed = digram_excess(tuple(pairs))
    drawn = random.Random(_SEED)
    digram_at_least = 0
    for _ in range(_BIG):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if digram_excess(tuple(shuffled)) >= printed:
            digram_at_least += 1

    whole = best_chi_square(tuple(pairs))
    drawn = random.Random(_SEED)
    english_max = 0.0
    english_as_flat = 0
    for _ in range(_BIG):
        letters = tuple(drawn.choices(_ALPHABET, weights=ENGLISH_25, k=len(pairs)))
        score = best_chi_square(letters)
        if score > english_max:
            english_max = score
        if score >= whole:
            english_as_flat += 1

    first = best_chi_square(tuple(pairs[:98]))
    second = best_chi_square(tuple(pairs[98:]))
    drawn = random.Random(_SEED)
    first_as_flat = 0
    second_as_flat = 0
    for _ in range(_HALF):
        letters = tuple(drawn.choices(_ALPHABET, weights=ENGLISH_25, k=98))
        score = best_chi_square(letters)
        if score >= first:
            first_as_flat += 1
        if score >= second:
            second_as_flat += 1

    regular = min(
        (symbol for symbol, count in counts.items() if count >= 4),
        key=lambda symbol: _gap_cv(pairs, symbol),
    )
    regular_cv = _gap_cv(pairs, regular)
    drawn = random.Random(_SEED)
    as_regular = 0
    for _ in range(_GAP):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _gap_cv(shuffled, regular) <= regular_cv:
            as_regular += 1

    control = best_chi_square(_pairs(CONTROL, "ABCDE"))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _BIG + _BIG + _BIG + _HALF + _GAP,
        "column_width": width,
        "column_index": column,
        "column_draws": _BIG,
        "column_as_extreme": width_hits,
        "digram_excess": printed,
        "digram_draws": _BIG,
        "digram_shuffle_at_least": digram_at_least,
        "challenge_chi": round(whole, 2),
        "english_draws": _BIG,
        "english_max_chi": round(english_max, 2),
        "english_as_flat": english_as_flat,
        "control_chi": round(control, 2),
        "first_half_chi": round(first, 2),
        "second_half_chi": round(second, 2),
        "half_draws": _HALF,
        "first_half_as_flat": first_as_flat,
        "second_half_as_flat": second_as_flat,
        "regular_symbol": regular,
        "gap_draws": _GAP,
        "gap_as_regular": as_regular,
        "works": ("rare-column search", "full-length letter counts"),
        "does_not_work": ("printed-order digrams", "either half alone", "symbol spacing"),
        "scope": (
            "A method works only if its own null almost never matches the challenge. "
            "The solved example is the check that letter counts still accept real English. "
            "No letter string is stored."
        ),
    }
