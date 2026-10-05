"""The larger English model, drilled on fresh windows before it became the default.

The earlier drill found the substitution solver exact on 0 of 6 fresh
200-letter windows, with either search length. The search was not the
problem. The legacy model is fit on 10,923 characters, and its backoff lets a
key that scrambles every context score close to a right key. This drill runs
the same solver, same restarts and steps, on eight further training windows
at three lengths, once with each model. The certificate has to come back
under both. No plaintext is stored.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.alphabet import letters_only
from engine.dagapeyeff_cache import frozen
from engine.language import get_legacy_model, get_model
from engine.neural_grade import letters_az, load_training_prose
from engine.solvers.substitution import solve_substitution

_STARTS = (1000, 2500, 4000, 5500, 7000, 8200, 9300, 10500)
_WIDTHS = (200, 150, 100)
_PERMUTATION = "QWERTYUIOPASDFGHJKLZXCVBNM"
_CERTIFICATE = Path(__file__).resolve().parent / "data" / "substitution_certificate.json"


def _wrong(plaintext: str, original: str) -> int:
    found = letters_only(plaintext)
    return sum(a != b for a, b in zip(found, original)) + abs(len(found) - len(original))


@frozen("solver-strong")
def solver_strong_report() -> dict:
    from engine.ciphers import substitution_encrypt

    prose = letters_az(load_training_prose())
    rows = []
    for width in _WIDTHS:
        row = {"width": width, "windows": len(_STARTS)}
        for model in ("legacy", "default"):
            exact = wrong = 0
            for start in _STARTS:
                original = prose[start:start + width]
                if len(original) < width:
                    raise RuntimeError("training prose is shorter than the drill")
                cipher = substitution_encrypt(original, _PERMUTATION)
                errors = _wrong(solve_substitution(cipher, model=model).plaintext, original)
                exact += errors == 0
                wrong += errors
            row[f"{model}_exact"] = exact
            row[f"{model}_wrong_letters"] = wrong
        rows.append(row)
    certificate = json.loads(_CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("cipher_name") != "substitution":
        raise RuntimeError("the substitution certificate is not the expected file")
    certificate_exact = {
        model: _wrong(solve_substitution(certificate["ciphertext"], model=model).plaintext,
                      letters_only(certificate["plaintext"])) == 0
        for model in ("legacy", "default")
    }
    better = all(row["default_exact"] >= row["legacy_exact"] for row in rows) and any(
        row["default_exact"] > row["legacy_exact"] for row in rows
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "legacy_letters": get_legacy_model().sample_letters,
        "default_letters": get_model().sample_letters,
        "rows": rows,
        "certificate_legacy_exact": certificate_exact["legacy"],
        "certificate_default_exact": certificate_exact["default"],
        "promoted": bool(better and certificate_exact["default"]),
        "scope": (
            "A drill on known training text with a fresh key. It decides which "
            "English model the solvers use. It is not a reading."
        ),
    }
