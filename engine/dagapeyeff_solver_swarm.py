"""The repo's own solvers, as a swarm, on the 196 cells. Not a reading.

Caesar, Vigenere, and substitution each see the cells as letters A through Y.
Each solver is also run on shuffled cells. Only the scores are kept. The
plaintext a solver prints is discarded.
"""

from __future__ import annotations

import random
from functools import lru_cache

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _PROSE, _cells
from engine.solvers.caesar import solve_caesar
from engine.solvers.substitution import solve_substitution
from engine.solvers.vigenere import solve_vigenere

_SEED = 20261004
_CAESAR_DRAWS = 40
_VIGENERE_DRAWS = 20
_SUBSTITUTION_DRAWS = 8
_VIGENERE_PERIOD = 8
_SUBSTITUTION_STEPS = 400


def _letters(cells: list[int]) -> str:
    return "".join(chr(65 + cell) for cell in cells)


def _per_letter(score: float, count: int) -> float:
    return score / count


@lru_cache(maxsize=1)
def solver_swarm_report() -> dict:
    cells = _cells()
    text = _letters(cells)
    prose = letters_only(_PROSE)
    caesar = solve_caesar(text)
    vigenere = solve_vigenere(text, max_period=_VIGENERE_PERIOD)
    substitution = solve_substitution(text, restarts=1, steps=_SUBSTITUTION_STEPS, seed=_SEED)
    caesar_prose = solve_caesar(prose)
    vigenere_prose = solve_vigenere(prose, max_period=_VIGENERE_PERIOD)
    substitution_prose = solve_substitution(prose, restarts=1, steps=_SUBSTITUTION_STEPS, seed=_SEED)
    drawn = random.Random(_SEED)
    caesar_as_high = 0
    for _ in range(_CAESAR_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score = solve_caesar(_letters(shuffled)).score
        if score >= caesar.score:
            caesar_as_high += 1
    vigenere_as_high = 0
    for _ in range(_VIGENERE_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score = solve_vigenere(_letters(shuffled), max_period=_VIGENERE_PERIOD).score
        if score >= vigenere.score:
            vigenere_as_high += 1
    substitution_as_high = 0
    for _ in range(_SUBSTITUTION_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score = solve_substitution(
            _letters(shuffled), restarts=1, steps=_SUBSTITUTION_STEPS, seed=_SEED
        ).score
        if score >= substitution.score:
            substitution_as_high += 1
    letters = len(text)
    prose_letters = len(prose)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "letters": letters,
        "caesar_per_letter": round(_per_letter(caesar.score, letters), 4),
        "caesar_prose_per_letter": round(_per_letter(caesar_prose.score, prose_letters), 4),
        "caesar_draws": _CAESAR_DRAWS,
        "caesar_shuffles_as_high": caesar_as_high,
        "vigenere_max_period": _VIGENERE_PERIOD,
        "vigenere_period": vigenere.details["period"],
        "vigenere_per_letter": round(_per_letter(vigenere.score, letters), 4),
        "vigenere_prose_per_letter": round(_per_letter(vigenere_prose.score, prose_letters), 4),
        "vigenere_draws": _VIGENERE_DRAWS,
        "vigenere_shuffles_as_high": vigenere_as_high,
        "substitution_steps": _SUBSTITUTION_STEPS,
        "substitution_per_letter": round(_per_letter(substitution.score, letters), 4),
        "substitution_prose_per_letter": round(_per_letter(substitution_prose.score, prose_letters), 4),
        "substitution_reading": substitution.details["reading"],
        "substitution_draws": _SUBSTITUTION_DRAWS,
        "substitution_shuffles_as_high": substitution_as_high,
        "scope": "A solver score is not a reading. The plaintext is discarded.",
    }
