"""A longer substitution search, scored on fresh training windows.

The default search is 4000 steps and 10 restarts. This drill also runs 8000
steps and 16 restarts. The windows are not the pentest windows. The known
substitution certificate is the regression: both searches have to recover it.
The default arguments of the solver are not changed. No plaintext is stored.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.alphabet import letters_only
from engine.dagapeyeff_cache import frozen
from engine.neural_grade import letters_az, load_training_prose
from engine.solvers.substitution import solve_substitution

_STARTS = (1000, 2500, 4000, 5500, 7000, 10500)
_WIDTH = 200
_SEED = 20261008
_PERMUTATION = "QWERTYUIOPASDFGHJKLZXCVBNM"
_LONG_STEPS = 8000
_LONG_RESTARTS = 16
_CERTIFICATE = Path(__file__).resolve().parent / "data" / "substitution_certificate.json"


def _exact(result, original: str) -> bool:
    return letters_only(result.plaintext) == letters_only(original)


def _window(prose: str, start: int) -> str:
    piece = prose[start : start + _WIDTH]
    if len(piece) < _WIDTH:
        raise RuntimeError("training prose is shorter than the solver drill")
    return piece


@frozen("solver-train")
def solver_train_report() -> dict:
    from engine.ciphers import substitution_encrypt

    prose = letters_az(load_training_prose())
    default_exact = long_exact = 0
    for start in _STARTS:
        original = _window(prose, start)
        cipher = substitution_encrypt(original, _PERMUTATION)
        default_exact += _exact(solve_substitution(cipher), original)
        long_exact += _exact(
            solve_substitution(cipher, restarts=_LONG_RESTARTS, steps=_LONG_STEPS, seed=_SEED),
            original,
        )
    certificate = json.loads(_CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("cipher_name") != "substitution":
        raise RuntimeError("the substitution certificate is not the expected file")
    cipher = certificate["ciphertext"]
    original = certificate["plaintext"]
    default_certificate = _exact(solve_substitution(cipher), original)
    long_certificate = _exact(
        solve_substitution(cipher, restarts=_LONG_RESTARTS, steps=_LONG_STEPS, seed=_SEED),
        original,
    )
    promoted = long_exact > default_exact and long_certificate and default_certificate
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_replaced": False,
        "default_changed": False,
        "windows": len(_STARTS),
        "width": _WIDTH,
        "default_exact": default_exact,
        "long_steps": _LONG_STEPS,
        "long_restarts": _LONG_RESTARTS,
        "long_exact": long_exact,
        "certificate_default_exact": default_certificate,
        "certificate_long_exact": long_certificate,
        "promoted": bool(promoted),
        "scope": (
            "A longer substitution search is a drill on known training text. "
            "It does not change the solver, and it is not a reading."
        ),
    }
