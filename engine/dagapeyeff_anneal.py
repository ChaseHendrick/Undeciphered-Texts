"""A longer solver swarm on the 196 cells. Not a reading.

The frozen solver swarm used 400 substitution steps and one restart. This
one uses 2000 steps and four restarts, the same budget on the cells, on
ordinary prose, and on shuffled cells. Caesar and Vigenere run in the same
swarm. Bob's reader is asked after the ranking and does not keep letters.
A higher score than a shuffle is still not a plaintext.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only
from engine.bob_read import try_read
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen
from engine.solvers.caesar import solve_caesar
from engine.solvers.substitution import solve_substitution
from engine.solvers.vigenere import solve_vigenere

_SEED = 20261009
_STEPS = 2000
_RESTARTS = 4
_DRAWS = 6
_VIGENERE_PERIOD = 8


def _letters(cells: list[int]) -> str:
    return "".join(chr(65 + cell) for cell in cells)


def _per_letter(score: float, count: int) -> float:
    return score / count


def _substitution(text: str, seed: int):
    return solve_substitution(text, restarts=_RESTARTS, steps=_STEPS, seed=seed)


@frozen("dagapeyeff-anneal")
def anneal_swarm_report() -> dict:
    cells = _cells()
    text = _letters(cells)
    prose = letters_only(_PROSE)
    reading = try_read(text)
    caesar = solve_caesar(text)
    vigenere = solve_vigenere(text, max_period=_VIGENERE_PERIOD)
    substitution = _substitution(text, _SEED)
    caesar_prose = solve_caesar(prose)
    vigenere_prose = solve_vigenere(prose, max_period=_VIGENERE_PERIOD)
    substitution_prose = _substitution(prose, _SEED)
    drawn = random.Random(_SEED)
    caesar_as_high = vigenere_as_high = substitution_as_high = 0
    for draw in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        sample = _letters(shuffled)
        if solve_caesar(sample).score >= caesar.score:
            caesar_as_high += 1
        if solve_vigenere(sample, max_period=_VIGENERE_PERIOD).score >= vigenere.score:
            vigenere_as_high += 1
        if _substitution(sample, _SEED + draw).score >= substitution.score:
            substitution_as_high += 1
    letters = len(text)
    prose_letters = len(prose)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "letters": letters,
        "reader_family": reading["family"],
        "reader_withheld": bool(reading["withheld"]),
        "reader_consistent": bool(reading["consistent"]),
        "caesar_per_letter": round(_per_letter(caesar.score, letters), 4),
        "caesar_prose_per_letter": round(_per_letter(caesar_prose.score, prose_letters), 4),
        "caesar_shuffles_as_high": caesar_as_high,
        "vigenere_max_period": _VIGENERE_PERIOD,
        "vigenere_per_letter": round(_per_letter(vigenere.score, letters), 4),
        "vigenere_prose_per_letter": round(_per_letter(vigenere_prose.score, prose_letters), 4),
        "vigenere_shuffles_as_high": vigenere_as_high,
        "substitution_steps": _STEPS,
        "substitution_restarts": _RESTARTS,
        "substitution_per_letter": round(_per_letter(substitution.score, letters), 4),
        "substitution_prose_per_letter": round(_per_letter(substitution_prose.score, prose_letters), 4),
        "substitution_reading": bool(substitution.details["reading"]),
        "substitution_shuffles_as_high": substitution_as_high,
        "draws": _DRAWS,
        "promoted": False,
        "scope": (
            "A longer search on the cells is still a score against shuffles. "
            "The reader does not keep the letters. Not a reading."
        ),
    }
