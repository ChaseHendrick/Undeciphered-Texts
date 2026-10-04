"""Affine, Beaufort, and Porta, as a swarm. Not a reading.

These are not Caesar, Vigenere, or the substitution hill-climb. Each search
is also run on shuffled cells. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen
from engine.language import get_model, unigram_score
from engine.solvers.porta import porta_substitute

_SEED = 20261004
_DRAWS = 20
_BEAUFORT_DRAWS = 80
_COPRIMES = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
_PERIODS = range(2, 7)


def _inv(value: int) -> int:
    for candidate in range(26):
        if (value * candidate) % 26 == 1:
            return candidate
    raise ValueError("affine multiplier has no inverse")


def _quad(seq: list[int]) -> float:
    return get_model().score(seq) / (len(seq) - 3)


def _best_affine(seq: list[int]) -> tuple[float, int]:
    best = float("-inf")
    best_multiplier = 0
    for multiplier in _COPRIMES:
        inverse = _inv(multiplier)
        for shift in range(26):
            plain = [(inverse * (cell - shift)) % 26 for cell in seq]
            score = _quad(plain)
            if score > best:
                best = score
                best_multiplier = multiplier
    return best, best_multiplier


def _best_beaufort(seq: list[int]) -> tuple[float, int]:
    best = float("-inf")
    best_period = 0
    count = len(seq)
    for period in _PERIODS:
        plain = [0] * count
        for offset in range(period):
            column = seq[offset::period]
            best_column = column
            best_unigram = float("-inf")
            for shift in range(26):
                decoded = [(shift - cell) % 26 for cell in column]
                score = unigram_score(decoded)
                if score > best_unigram:
                    best_unigram = score
                    best_column = decoded
            for index, value in enumerate(best_column):
                plain[offset + index * period] = value
        score = _quad(plain)
        if score > best:
            best = score
            best_period = period
    return best, best_period


def _best_porta(seq: list[int]) -> tuple[float, int]:
    best = float("-inf")
    best_period = 0
    count = len(seq)
    rows = [chr(65 + row * 2) for row in range(13)]
    for period in _PERIODS:
        plain = [0] * count
        for offset in range(period):
            column = seq[offset::period]
            best_column = [0] * len(column)
            best_unigram = float("-inf")
            for row in rows:
                decoded = [ord(porta_substitute(chr(65 + cell), row)) - 65 for cell in column]
                score = unigram_score(decoded)
                if score > best_unigram:
                    best_unigram = score
                    best_column = decoded
            for index, value in enumerate(best_column):
                plain[offset + index * period] = value
        score = _quad(plain)
        if score > best:
            best = score
            best_period = period
    return best, best_period


def _as_high(seq: list[int], best: float, search, drawn: random.Random, draws: int) -> int:
    hits = 0
    for _ in range(draws):
        shuffled = seq[:]
        drawn.shuffle(shuffled)
        score, _detail = search(shuffled)
        if score >= best:
            hits += 1
    return hits


@frozen("classic-swarm")
def classic_swarm_report() -> dict:
    seq = _cells()
    prose = to_ints(letters_only(_PROSE))
    affine, multiplier = _best_affine(seq)
    beaufort, beaufort_period = _best_beaufort(seq)
    porta, porta_period = _best_porta(seq)
    affine_prose, _affine_multiplier = _best_affine(prose)
    prose_score = _quad(prose)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "letters": len(seq),
        "prose_per_quadgram": round(prose_score, 4),
        "affine_draws": _DRAWS,
        "affine_multiplier": multiplier,
        "affine_per_quadgram": round(affine, 4),
        "affine_on_prose": round(affine_prose, 4),
        "affine_shuffles_as_high": _as_high(seq, affine, _best_affine, random.Random(_SEED), _DRAWS),
        "beaufort_draws": _BEAUFORT_DRAWS,
        "beaufort_period": beaufort_period,
        "beaufort_per_quadgram": round(beaufort, 4),
        "beaufort_shuffles_as_high": _as_high(
            seq, beaufort, _best_beaufort, random.Random(_SEED), _BEAUFORT_DRAWS
        ),
        "porta_draws": _DRAWS,
        "porta_period": porta_period,
        "porta_per_quadgram": round(porta, 4),
        "porta_shuffles_as_high": _as_high(seq, porta, _best_porta, random.Random(_SEED), _DRAWS),
        "scope": "Affine, Beaufort, and Porta scores are not a reading. No letter string is stored.",
    }
