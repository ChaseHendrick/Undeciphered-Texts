"""Why the substitution drill missed: the model, not the step count.

The solver drill of 5 October found the default search exact on 0 of 6
windows of 200 letters, and more steps did not help. Here every miss is
sorted. If the key the search returned scores at least as well as the true
text, the language model preferred a wrong key, and more steps cannot fix
that. If it scores lower, the search missed.

The windows are held-out Doyle prose, which the large corpus excludes. Each
window gets its own random permutation. The default is the small model with
10 restarts at temperature 30. The other arm is the 1.9M-letter model with
30 restarts at temperature 10. No plaintext is stored.
"""

from __future__ import annotations

import random
from pathlib import Path

from engine.ciphers import substitution_encrypt
from engine.dagapeyeff_cache import frozen
from engine.language import get_large_model, get_model
from engine.neural import load_training_prose
from engine.neural_grade import letters_az
from engine.solvers.substitution import solve_substitution

_DOYLE = Path(__file__).resolve().parent / "data" / "neural_heldout_doyle.txt"
_WIDTHS = (100, 200)
_WINDOWS = 8
_SEED = 20261010
_ARMS = (
    ("small", 10, 30.0),
    ("large", 30, 10.0),
)


def _windows(width: int) -> list[str]:
    prose = letters_az(load_training_prose(_DOYLE))
    stride = (len(prose) - width) // _WINDOWS
    return [prose[index * stride : index * stride + width] for index in range(_WINDOWS)]


def _permutation(draw: int) -> str:
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.Random(_SEED + draw).shuffle(letters)
    return "".join(letters)


def _arm(name: str, restarts: int, temperature: float, width: int) -> dict:
    model = get_large_model() if name == "large" else get_model()
    exact = good = model_misses = search_misses = 0
    correct = 0
    for draw, original in enumerate(_windows(width)):
        cipher = substitution_encrypt(original, _permutation(draw))
        result = solve_substitution(cipher, restarts=restarts, temperature=temperature, model=model)
        found = "".join(char for char in result.plaintext if char.isalpha()).upper()
        hits = sum(left == right for left, right in zip(found, original))
        correct += hits
        exact += found == original
        if hits * 10 >= 9 * width:
            good += 1
            continue
        truth = model.score([ord(char) - 65 for char in original])
        if result.score >= truth - 1e-9:
            model_misses += 1
        else:
            search_misses += 1
    return {
        "model": name,
        "model_letters": model.sample_letters,
        "restarts": restarts,
        "temperature": temperature,
        "width": width,
        "windows": _WINDOWS,
        "exact": exact,
        "nine_tenths_right": good,
        "letters_right": round(correct / (width * _WINDOWS), 4),
        "misses_the_model_prefers": model_misses,
        "misses_the_search_left": search_misses,
    }


@frozen("solver-model")
def solver_model_report() -> dict:
    arms = [_arm(name, restarts, temperature, width) for width in _WIDTHS for name, restarts, temperature in _ARMS]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "default_changed": False,
        "arms": arms,
        "scope": (
            "A drill on held-out English with known keys. A higher score than the true text means the model, "
            "not the search, chose the wrong key. Not a reading."
        ),
    }
