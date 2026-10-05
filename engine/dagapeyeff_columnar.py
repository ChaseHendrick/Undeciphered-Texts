"""Columnar transposition under a letter key, searched jointly, on the cells. Not a reading.

The plainest classical hypothesis for the challenge is a Polybius substitution
followed by a complete columnar transposition: plaintext written in rows of a
width that divides 196, columns copied out in key order. Earlier passes
scored random column keys by successive-symbol information, and ran the
substitution solver on the cells with a model that could not recover a known
200-letter substitution. This pass anneals the column order and the letter
key together under the default English model, which can.

Width 1 is plain substitution. Each width gets planted controls: training
prose with J folded into I, a random column order and a random letter key.
A control counts as recovered only when every letter comes back. The printed
cells, the one other legal regrouping, and shuffled cells get the same
search. No letter string is stored.
"""

from __future__ import annotations

import math
import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_regroup import regrouped_pairs
from engine.language import ENGLISH_ORDER, get_model
from engine.neural_grade import letters_az, load_training_prose
from engine.solvers.substitution import _score

WIDTHS = (1, 2, 4, 7, 14)
_SEED = 20261014
_PLANT_STARTS = (2000, 5000)
_SHUFFLES = 4
_RESTARTS = 4
_STEPS = 60000
_LETTERS = 196


def read_positions(width: int, order: list[int]) -> list[int]:
    """Ciphertext positions in plaintext order, for columns copied out in this order."""
    height = _LETTERS // width
    return [order[column] * height + row for row in range(height) for column in range(width)]


def columnar_encrypt(plain: list[int], width: int, key_order: list[int]) -> list[int]:
    height = _LETTERS // width
    return [plain[row * width + key_order[block]] for block in range(width) for row in range(height)]


def _frequency_key(cells: list[int]) -> list[int]:
    counts = [0] * 26
    for symbol in cells:
        counts[symbol] += 1
    ranked = sorted(range(26), key=lambda i: (-counts[i], i))
    key = [0] * 26
    for rank, symbol in enumerate(ranked):
        key[symbol] = ord(ENGLISH_ORDER[rank]) - 65
    return key


def anneal(cells: list[int], width: int, rng: random.Random, restarts: int = _RESTARTS,
           steps: int = _STEPS, start: float = 12.0, stop: float = 0.3) -> tuple[float, list[int], list[int]]:
    """Anneal the column order and the letter key together. Returns score, order and key."""
    logp = get_model().logp
    cooling = (stop / start) ** (1.0 / steps)
    best: tuple[float, list[int], list[int]] = (-math.inf, [], [])
    for _ in range(restarts):
        order = list(range(width))
        rng.shuffle(order)
        key = _frequency_key(cells)
        sequence = [cells[i] for i in read_positions(width, order)]
        current = _score(sequence, key, logp)
        temperature = start
        top = (current, order[:], key[:])
        for _ in range(steps):
            draw = rng.random()
            if width == 1 or draw < 0.6:
                i, j = rng.randrange(26), rng.randrange(26)
                if i != j:
                    key[i], key[j] = key[j], key[i]
                    score = _score(sequence, key, logp)
                    if score >= current or rng.random() < math.exp((score - current) / temperature):
                        current = score
                    else:
                        key[i], key[j] = key[j], key[i]
            else:
                trial = order[:]
                if draw < 0.8:
                    a, b = rng.randrange(width), rng.randrange(width)
                    trial[a], trial[b] = trial[b], trial[a]
                else:
                    column = trial.pop(rng.randrange(width))
                    trial.insert(rng.randrange(width), column)
                trial_sequence = [cells[i] for i in read_positions(width, trial)]
                score = _score(trial_sequence, key, logp)
                if score >= current or rng.random() < math.exp((score - current) / temperature):
                    current, order, sequence = score, trial, trial_sequence
            if current > top[0]:
                top = (current, order[:], key[:])
            temperature *= cooling
        if top[0] > best[0]:
            best = top
    return best


def _per_letter(score: float) -> float:
    return round(score / (_LETTERS - 3), 4)


def _regrouped_cells() -> list[int]:
    return ["67890".index(pair[0]) * 5 + "12345".index(pair[1]) for pair in regrouped_pairs()]


@frozen("dagapeyeff-columnar")
def columnar_report() -> dict:
    logp = get_model().logp
    prose = letters_az(load_training_prose()).replace("J", "I")
    cells = _cells()
    regrouped = _regrouped_cells()
    drawn = random.Random(_SEED)
    rows = []
    for width in WIDTHS:
        planted = []
        for start in _PLANT_STARTS:
            plain = [ord(ch) - 65 for ch in prose[start:start + _LETTERS]]
            order = list(range(width))
            drawn.shuffle(order)
            letters = list(range(26))
            drawn.shuffle(letters)
            cipher = [letters[x] for x in columnar_encrypt(plain, width, order)]
            score, found, key = anneal(cipher, width, random.Random(drawn.randrange(1 << 30)))
            recovered = [key[cipher[i]] for i in read_positions(width, found)]
            planted.append({
                "true_per_letter": _per_letter(_score(plain, list(range(26)), logp)),
                "found_per_letter": _per_letter(score),
                "wrong_letters": sum(a != b for a, b in zip(recovered, plain)),
            })
        cell_score = anneal(cells, width, random.Random(drawn.randrange(1 << 30)))[0]
        regroup_score = anneal(regrouped, width, random.Random(drawn.randrange(1 << 30)))[0]
        shuffles = []
        for _ in range(_SHUFFLES):
            shuffled = cells[:]
            drawn.shuffle(shuffled)
            shuffles.append(_per_letter(anneal(shuffled, width, random.Random(drawn.randrange(1 << 30)))[0]))
        cell_per_letter = _per_letter(cell_score)
        rows.append({
            "width": width,
            "planted": planted,
            "planted_recovered": sum(row["wrong_letters"] == 0 for row in planted),
            "cells_per_letter": cell_per_letter,
            "regrouped_per_letter": _per_letter(regroup_score),
            "shuffles_per_letter": shuffles,
            "shuffles_as_high": sum(score >= cell_per_letter for score in shuffles),
        })
    english = min(row["true_per_letter"] for width_row in rows for row in width_row["planted"])
    best_cells = max(max(row["cells_per_letter"], row["regrouped_per_letter"]) for row in rows)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "widths": list(WIDTHS),
        "restarts": _RESTARTS,
        "steps": _STEPS,
        "rows": rows,
        "lowest_planted_true_per_letter": english,
        "best_cells_per_letter": best_cells,
        "scope": (
            "A joint search over column order and letter key, with planted controls. The cells and "
            "the regrouping score where shuffled cells score, far under any planted English text. "
            "Not a reading. No letter string is stored."
        ),
    }
