"""The 1939 counts scored as some other language. Not a reading.

The square has 25 cells, so I and J share a cell for every language that uses
the Latin alphabet. That is the grid, not a preference for English. Each
language is then judged against text drawn from its own letter rates.
Esperanto is separate: the sourced table has 28 letters, and the six hatted
letters are folded into the plain ones. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_more import _PERCENT
from engine.dagapeyeff_swarm import challenge_pairs
from engine.language import UNIGRAM

_SEED = 20261004
_DRAWS = 2000
_LATIN = (
    "english",
    "french",
    "german",
    "spanish",
    "italian",
    "portuguese",
    "dutch",
)
# Ottó Haszpra, as printed on the Esperanto Wikipedia "Literofteco" page.
# Six hatted letters are folded into c, g, h, j, s, and u.
_ESPERANTO = {
    "a": 12.59, "b": 1.15, "c": 0.85 + 0.67, "d": 3.04, "e": 8.99, "f": 1.09,
    "g": 1.28 + 0.69, "h": 0.50 + 0.01, "i": 9.36, "j": 2.71 + 0.15, "k": 4.22,
    "l": 6.24, "m": 3.06, "n": 7.79, "o": 8.80, "p": 2.82, "r": 5.97,
    "s": 5.91 + 0.35, "t": 5.50, "u": 3.36 + 0.51, "v": 1.87, "z": 0.52,
}


def _raw(language: str) -> tuple[float, ...]:
    if language == "english":
        return UNIGRAM
    return tuple(value / 100 for value in _PERCENT[language])


def _square_rates(raw: tuple[float, ...]) -> tuple[float, ...]:
    merged = []
    for index, rate in enumerate(raw):
        if index == 9:
            continue
        if index == 8:
            merged.append(rate + raw[9])
        else:
            merged.append(rate)
    scale = sum(merged)
    return tuple(value / scale for value in merged)


def _chi(counts: list[int], rates: tuple[float, ...]) -> float:
    ordered = sorted(counts, reverse=True)
    if len(ordered) > len(rates):
        raise ValueError("more symbols than the language model")
    ordered = ordered + [0] * (len(rates) - len(ordered))
    total = sum(ordered)
    score = 0.0
    for count, rate in zip(ordered, sorted(rates, reverse=True)):
        expected = total * rate
        score += (count - expected) ** 2 / expected
    return score


def _fold_ij(counts26: list[int]) -> list[int]:
    folded = []
    for index, count in enumerate(counts26):
        if index == 9:
            continue
        if index == 8:
            folded.append(count + counts26[9])
        else:
            folded.append(count)
    return folded


def _draw_latin(language: str, length: int, drawn: random.Random) -> list[int]:
    raw = _raw(language)
    counts = [0] * 26
    for letter in drawn.choices(range(26), weights=raw, k=length):
        counts[letter] += 1
    return _fold_ij(counts)


def _language_row(language: str, observed: list[int], prose: list[int]) -> dict:
    rates = _square_rates(_raw(language))
    cipher = _chi(observed, rates)
    prose_score = _chi(prose, rates)
    drawn = random.Random(_SEED)
    cipher_as_flat = 0
    prose_as_flat = 0
    cipher_draw = []
    for _ in range(_DRAWS):
        score = _chi(_draw_latin(language, 196, drawn), rates)
        cipher_draw.append(score)
        if score >= cipher - 1e-9:
            cipher_as_flat += 1
    for _ in range(_DRAWS):
        score = _chi(_draw_latin(language, sum(prose), drawn), rates)
        if score >= prose_score - 1e-9:
            prose_as_flat += 1
    cipher_draw.sort()
    return {
        "chi": round(cipher, 2),
        "median": round(cipher_draw[_DRAWS // 2], 2),
        "as_flat": cipher_as_flat,
        "prose_chi": round(prose_score, 2),
        "prose_as_flat": prose_as_flat,
    }


def _esperanto_rates() -> tuple[float, ...]:
    order = "abcdefghijklmnoprstuvz"
    raw = [_ESPERANTO[letter] for letter in order]
    scale = sum(raw)
    return tuple(value / scale for value in raw)


def _esperanto_row(observed: list[int]) -> dict:
    rates = _esperanto_rates()
    cipher = _chi(observed, rates)
    drawn = random.Random(_SEED)
    as_flat = 0
    scores = []
    width = len(rates)
    for _ in range(_DRAWS):
        counts = [0] * width
        for index in drawn.choices(range(width), weights=rates, k=196):
            counts[index] += 1
        score = _chi(counts, rates)
        scores.append(score)
        if score >= cipher - 1e-9:
            as_flat += 1
    scores.sort()
    return {
        "letters": width,
        "chi": round(cipher, 2),
        "median": round(scores[_DRAWS // 2], 2),
        "as_flat": as_flat,
    }


def language_report() -> dict:
    observed = list(Counter(challenge_pairs()).values())
    prose_letters = letters_only(_PROSE)
    prose = [0] * 26
    for char in prose_letters:
        prose[ord(char) - 65] += 1
    prose = _fold_ij(prose)
    rows = {language: _language_row(language, observed, prose) for language in _LATIN}
    esperanto = _esperanto_row(observed)
    closest = min(rows, key=lambda language: rows[language]["chi"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "draws": _DRAWS,
        "trials": _DRAWS * (len(rows) * 2 + 1),
        "languages": rows,
        "closest": closest,
        "closest_chi": rows[closest]["chi"],
        "esperanto": esperanto,
        "english_prose_inside": rows["english"]["prose_as_flat"] > _DRAWS // 10,
        "scope": (
            "A language fits only if text drawn from that language is as flat as the cipher. "
            "The solved English exercise is the check that real English still fits English. "
            "No letter string is stored."
        ),
    }
