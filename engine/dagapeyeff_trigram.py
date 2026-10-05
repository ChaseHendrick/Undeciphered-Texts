"""Three cells in a row, in the challenge and in the solved exercise. Not a reading.

The count is how many different three-cell sequences occur more than once.
Four cells in a row are scored as well, because that was the next length.
Shuffles of the same cells get the same counts. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 10000


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


def _repeated(seq: list[str], length: int) -> int:
    grams = Counter(tuple(seq[index:index + length]) for index in range(len(seq) - length + 1))
    return sum(value > 1 for value in grams.values())


def _as_high(seq: list[str], length: int, observed: int) -> int:
    drawn = random.Random(_SEED)
    hits = 0
    for _ in range(_DRAWS):
        shuffled = seq[:]
        drawn.shuffle(shuffled)
        if _repeated(shuffled, length) >= observed:
            hits += 1
    return hits


def _as_few(seq: list[str], length: int, observed: int) -> int:
    drawn = random.Random(_SEED)
    hits = 0
    for _ in range(_DRAWS):
        shuffled = seq[:]
        drawn.shuffle(shuffled)
        if _repeated(shuffled, length) <= observed:
            hits += 1
    return hits


@frozen("trigram")
def trigram_report() -> dict:
    pairs = list(challenge_pairs())
    control = _control_pairs()
    repeated = _repeated(pairs, 3)
    control_repeated = _repeated(control, 3)
    four = _repeated(pairs, 4)
    control_four = _repeated(control, 4)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(pairs),
        "repeated_trigrams": repeated,
        "trigrams_as_high": _as_high(pairs, 3, repeated),
        "repeated_tetragrams": four,
        "tetragrams_as_few": _as_few(pairs, 4, four),
        "control_cells": len(control),
        "control_repeated_trigrams": control_repeated,
        "control_trigrams_as_high": _as_high(control, 3, control_repeated),
        "control_repeated_tetragrams": control_four,
        "control_tetragrams_as_few": _as_few(control, 4, control_four),
        "draws": _DRAWS,
        "lengths_scored": 2,
        "scope": (
            "A three-cell habit in the solved exercise is not a reading of the challenge. "
            "No letter string is stored."
        ),
    }
