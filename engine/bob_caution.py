"""Bob names a family, then a shuffle is asked the same question.

If the shuffle gets the same name, the call is the alphabet, not the order.
The shipped weights are not replaced. No letter string is stored.
"""

from __future__ import annotations

import hashlib
import random
from pathlib import Path

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen
from engine.neural_router_v2 import route_probabilities

_SEED = 20261004
_DRAWS = 40
_WEIGHTS = Path(__file__).resolve().parent / "data" / "neural_router_v2_weights.json"
_SHIPPED = "d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825"


def _letters(cells: list[int]) -> str:
    return "".join(chr(65 + cell) for cell in cells)


def _caesar(text: str, shift: int) -> str:
    return "".join(chr(65 + (ord(char) - 65 + shift) % 26) for char in text)


def _ask(text: str, drawn: random.Random) -> dict:
    ranked = route_probabilities(text)
    top = ranked["candidates"][0]
    symbols = [ord(char) - 65 for char in text]
    same = 0
    as_confident = 0
    for _ in range(_DRAWS):
        shuffled = symbols[:]
        drawn.shuffle(shuffled)
        other = route_probabilities(_letters(shuffled))["candidates"][0]
        if other["family"] == top["family"]:
            same += 1
        if other["probability"] >= top["probability"]:
            as_confident += 1
    return {
        "family": top["family"],
        "probability": round(top["probability"], 4),
        "uncertain": ranked["uncertain"],
        "shuffles_same_family": same,
        "shuffles_as_confident": as_confident,
        "uses_order": same * 2 < _DRAWS,
    }


@frozen("bob-caution")
def bob_caution_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    challenge = _ask(_letters(_cells()), random.Random(_SEED))
    control_text = _caesar(letters_only(_PROSE), 7)
    control = _ask(control_text, random.Random(_SEED + 1))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "draws": _DRAWS,
        "challenge_family": challenge["family"],
        "challenge_probability": challenge["probability"],
        "challenge_uncertain": challenge["uncertain"],
        "challenge_shuffles_same_family": challenge["shuffles_same_family"],
        "challenge_shuffles_as_confident": challenge["shuffles_as_confident"],
        "challenge_uses_order": challenge["uses_order"],
        "control_family": control["family"],
        "control_probability": control["probability"],
        "control_shuffles_same_family": control["shuffles_same_family"],
        "control_uses_order": control["uses_order"],
        "scope": "A family name is not a reading. The weights were not replaced.",
    }
