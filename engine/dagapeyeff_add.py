"""Repeating addition on the 1939 5 by 5 square. Not a reading.

Rearranging the pairs cannot change letter counts. Subtracting a repeating
shift from each cell can. Every period-2 key and every period-3 key is
scored. The same search on shuffled copies is the control. A letter string
is not stored.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_swarm import ENGLISH_25, challenge_pairs
from engine.language import ENGLISH_ORDER, get_legacy_model

_SEED = 20261004
_NULL = 40
_ENGLISH = 200
_ROW = "67890"
_COLUMN = "12345"
# The book's own solved exercise, used only as a scale for real prose.
_PROSE = (
    "THE NEW PLAN OF ATTACK INCLUDES OPERATIONS BY THREE BOMBER "
    "SQUADRONS OVER FACTORY AREA SOUTHWEST OF THE RIVER"
)


def _cells() -> list[int]:
    pairs = challenge_pairs()
    return [_ROW.index(pair[0]) * 5 + _COLUMN.index(pair[1]) for pair in pairs]


def _chi(counts: list[int]) -> float:
    rates = sorted(ENGLISH_25, reverse=True)
    total = sum(counts)
    score = 0.0
    for count, rate in zip(sorted(counts, reverse=True), rates):
        expected = total * rate
        score += (count - expected) * (count - expected) / expected
    return score


def _rotations(hist: list[int]) -> list[list[int]]:
    rotated = []
    for shift_row in range(5):
        for shift_column in range(5):
            out = [0] * 25
            for row in range(5):
                for column in range(5):
                    landed = ((row - shift_row) % 5) * 5 + (column - shift_column) % 5
                    out[landed] += hist[row * 5 + column]
            rotated.append(out)
    return rotated


def _phases(seq: list[int], period: int) -> list[list[list[int]]]:
    hists = [[0] * 25 for _ in range(period)]
    for index, cell in enumerate(seq):
        hists[index % period][cell] += 1
    return [_rotations(hist) for hist in hists]


def _best(seq: list[int], period: int) -> tuple[float, tuple[int, ...], list[int]]:
    phases = _phases(seq, period)
    best = float("inf")
    best_key: tuple[int, ...] = ()
    best_counts: list[int] = []
    if period == 2:
        left, right = phases
        for i, first in enumerate(left):
            for j, second in enumerate(right):
                counts = [first[bin_] + second[bin_] for bin_ in range(25)]
                score = _chi(counts)
                if score < best:
                    best, best_key, best_counts = score, (i, j), counts
        return best, best_key, best_counts
    if period != 3:
        raise ValueError("period must be 2 or 3")
    first_set, second_set, third_set = phases
    for i, first in enumerate(first_set):
        for j, second in enumerate(second_set):
            partial = [first[bin_] + second[bin_] for bin_ in range(25)]
            for k, third in enumerate(third_set):
                counts = [partial[bin_] + third[bin_] for bin_ in range(25)]
                score = _chi(counts)
                if score < best:
                    best, best_key, best_counts = score, (i, j, k), counts
    return best, best_key, best_counts


def _mean_quadgram(seq: list[int], key: tuple[int, ...], counts: list[int]) -> float:
    period = len(key)
    plain_cells = []
    for index, cell in enumerate(seq):
        shift = key[index % period]
        shift_row, shift_column = divmod(shift, 5)
        row, column = divmod(cell, 5)
        plain_cells.append(((row - shift_row) % 5) * 5 + (column - shift_column) % 5)
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    mapping = {}
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in plain_cells]
    return get_legacy_model().score(plain) / (len(plain) - 3)


def add_report() -> dict:
    cells = _cells()
    period2, _, _ = _best(cells, 2)
    period3, key3, counts3 = _best(cells, 3)
    real_quad = _mean_quadgram(cells, key3, counts3)
    drawn = random.Random(_SEED)
    period2_as_low = 0
    period3_as_low = 0
    quad_as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score2, _, _ = _best(shuffled, 2)
        score3, key, counts = _best(shuffled, 3)
        if score2 <= period2 + 1e-9:
            period2_as_low += 1
        if score3 <= period3 + 1e-9:
            period3_as_low += 1
        if _mean_quadgram(shuffled, key, counts) >= real_quad - 1e-12:
            quad_as_high += 1
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    drawn = random.Random(_SEED)
    unigram_quads = []
    for _ in range(_ENGLISH):
        letters = [ord(char) - 65 for char in drawn.choices(alphabet, weights=ENGLISH_25, k=len(cells))]
        unigram_quads.append(get_legacy_model().score(letters) / (len(cells) - 3))
    unigram_quads.sort()
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_legacy_model().score(prose) / (len(prose) - 3)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "period2_keys": 625,
        "period3_keys": 15625,
        "null_texts": _NULL,
        "trials": (625 + 15625) * (1 + _NULL) + _ENGLISH,
        "period2_chi": round(period2, 2),
        "period2_null_as_low": period2_as_low,
        "period3_chi": round(period3, 2),
        "period3_null_as_low": period3_as_low,
        "period3_quadgram": round(real_quad, 4),
        "quadgram_null_as_high": quad_as_high,
        "unigram_quadgram_median": round(unigram_quads[_ENGLISH // 2], 4),
        "prose_quadgram": round(prose_quad, 4),
        "scope": (
            "The friendliest repeating shift makes the counts look English. "
            "Shuffled copies of the same cells do too, and the word score stays with the gibberish, not with prose. "
            "No letter string is stored."
        ),
    }
