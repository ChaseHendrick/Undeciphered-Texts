"""Bob is asked about the book's solved exercise, not only about prose.

The exercise pairs become cells in the same way as the challenge. A shuffle
that keeps the family means the call is the alphabet, not the order. The
shipped weights are not replaced. No letter string is stored.
"""

from __future__ import annotations

import hashlib
import random

from engine.bob_caution import _SHIPPED, _WEIGHTS, _ask, _letters
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL


def _exercise_cells() -> list[int]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    pairs = [letters[index:index + 2] for index in range(0, even, 2)]
    alphabet = "".join(sorted({letter for pair in pairs for letter in pair}))
    return [alphabet.index(pair[0]) * 5 + alphabet.index(pair[1]) for pair in pairs]


@frozen("bob-exercise")
def bob_exercise_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    exercise = _ask(_letters(_exercise_cells()), random.Random(20261004))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "draws": 40,
        "exercise_family": exercise["family"],
        "exercise_probability": exercise["probability"],
        "exercise_shuffles_same_family": exercise["shuffles_same_family"],
        "exercise_uses_order": exercise["uses_order"],
        "scope": "A family name for the exercise is not a reading of the challenge. The weights were not replaced.",
    }
