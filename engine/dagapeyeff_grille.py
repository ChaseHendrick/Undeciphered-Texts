"""A turning grille on the 14 by 14 square of cells. Not a reading.

196 is 14 squared, the size a Fleissner grille of 49 holes fills in four
turns. A grille is a transposition, so it cannot change the cell counts, and
the letter key is still unknown. Four searches, each with a planted control:

1. A climb on successive-symbol information, which a letter key cannot
   change. On a planted grille it overshoots the true text and finds chance
   agreement, so this score cannot choose a grille.
2. A grille search with the letter key given, on the default English model.
   This is the power check for the search itself.
3. A joint search over the grille and the letter key, on a planted text, on
   the cells, and on shuffled copies of each.
4. The unicity bound: how many letters this model needs before one key
   should stand out, against the 196 the cells have.

The plaintext is discarded. Agreement is counted up to the turn the grille
starts in, because starting one turn later reads the same quarters in another
order.
"""

from __future__ import annotations

import math
import random

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_order import _mi
from engine.language import ENGLISH_ORDER, get_model
from engine.neural_grade import letters_az, load_training_prose

SIDE = 14
HALF = 7
ORBITS = HALF * HALF
_SEED = 20261010
_PLANT_STARTS = (2000, 3500, 5000)


def _turn(row: int, column: int, turns: int) -> tuple[int, int]:
    for _ in range(turns):
        row, column = column, SIDE - 1 - row
    return row, column


_CELLS_OF = [
    [_turn(row, column, turns)[0] * SIDE + _turn(row, column, turns)[1] for turns in range(4)]
    for row in range(HALF)
    for column in range(HALF)
]


def grille_order(choice: list[int]) -> list[int]:
    """Square positions in plaintext order. choice[k] is the turn of orbit k's hole."""
    order: list[int] = []
    for turn in range(4):
        order.extend(sorted(_CELLS_OF[k][(choice[k] + turn) & 3] for k in range(ORBITS)))
    return order


def grille_encrypt(plain: list[int], choice: list[int]) -> list[int]:
    square = [0] * (SIDE * SIDE)
    for index, position in enumerate(grille_order(choice)):
        square[position] = plain[index]
    return square


def agreement(found: list[int], true: list[int]) -> int:
    return max(sum(((a + shift) & 3) == b for a, b in zip(found, true)) for shift in range(4))


def _quad(seq: list[int], logp: list[float]) -> float:
    a, b, c = seq[0], seq[1], seq[2]
    total = 0.0
    for d in seq[3:]:
        total += logp[((a * 26 + b) * 26 + c) * 26 + d]
        a, b, c = b, c, d
    return total


def _per_letter(score: float) -> float:
    return round(score / (SIDE * SIDE - 3), 4)


def _frequency_key(square: list[int]) -> list[int]:
    counts = [0] * 26
    for symbol in square:
        counts[symbol] += 1
    ranked = sorted(range(26), key=lambda i: (-counts[i], i))
    key = [0] * 26
    for rank, symbol in enumerate(ranked):
        key[symbol] = ord(ENGLISH_ORDER[rank]) - 65
    return key


def climb_information(square: list[int], rng: random.Random, restarts: int, steps: int) -> tuple[float, list[int]]:
    best = (-1.0, [])
    for _ in range(restarts):
        choice = [rng.randrange(4) for _ in range(ORBITS)]
        current = _mi([square[i] for i in grille_order(choice)])
        for _ in range(steps):
            k = rng.randrange(ORBITS)
            old = choice[k]
            choice[k] = (old + rng.randrange(1, 4)) & 3
            score = _mi([square[i] for i in grille_order(choice)])
            if score >= current:
                current = score
            else:
                choice[k] = old
        if current > best[0]:
            best = (current, choice[:])
    return best


def anneal_grille(square: list[int], key: list[int] | None, rng: random.Random, restarts: int, steps: int,
                  start: float = 10.0, stop: float = 0.2) -> tuple[float, list[int], list[int]]:
    """Anneal the grille, and the letter key too when key is None."""
    logp = get_model().logp
    cooling = (stop / start) ** (1.0 / steps)
    best: tuple[float, list[int], list[int]] = (-math.inf, [], [])
    for _ in range(restarts):
        choice = [rng.randrange(4) for _ in range(ORBITS)]
        letters = key[:] if key is not None else _frequency_key(square)
        order = grille_order(choice)
        current = _quad([letters[square[i]] for i in order], logp)
        temperature = start
        top = (current, choice[:], letters[:])
        for _ in range(steps):
            if key is not None or rng.random() < 0.5:
                k = rng.randrange(ORBITS)
                old = choice[k]
                choice[k] = (old + rng.randrange(1, 4)) & 3
                trial_order = grille_order(choice)
                score = _quad([letters[square[i]] for i in trial_order], logp)
                if score >= current or rng.random() < math.exp((score - current) / temperature):
                    current, order = score, trial_order
                else:
                    choice[k] = old
            else:
                i, j = rng.randrange(26), rng.randrange(26)
                if i != j:
                    letters[i], letters[j] = letters[j], letters[i]
                    score = _quad([letters[square[x]] for x in order], logp)
                    if score >= current or rng.random() < math.exp((score - current) / temperature):
                        current = score
                    else:
                        letters[i], letters[j] = letters[j], letters[i]
            if current > top[0]:
                top = (current, choice[:], letters[:])
            temperature *= cooling
        if top[0] > best[0]:
            best = top
    return best


def _planted(start: int, rng: random.Random, substitute: bool) -> tuple[list[int], list[int], list[int], list[int]]:
    prose = letters_az(load_training_prose()).replace("J", "I")
    plain = [ord(ch) - 65 for ch in prose[start:start + SIDE * SIDE]]
    choice = [rng.randrange(4) for _ in range(ORBITS)]
    key = list(range(26))
    if substitute:
        rng.shuffle(key)
    square = [key[x] for x in grille_encrypt(plain, choice)]
    return plain, choice, key, square


@frozen("dagapeyeff-grille")
def grille_report() -> dict:
    logp = get_model().logp
    drawn = random.Random(_SEED)

    # 1. Successive-symbol information on a planted grille.
    plain, choice, _key, square = _planted(_PLANT_STARTS[0], drawn, substitute=False)
    information, found = climb_information(square, random.Random(_SEED + 1), restarts=6, steps=3000)
    information_true = _mi(plain)
    information_agreement = agreement(found, choice)

    # 2. The letter key given.
    known_rows = []
    for index, start in enumerate(_PLANT_STARTS):
        plain, choice, _key, square = _planted(start, drawn, substitute=False)
        score, found, _letters = anneal_grille(square, list(range(26)), random.Random(_SEED + 10 + index), 4, 20000)
        known_rows.append({
            "true_per_letter": _per_letter(_quad(plain, logp)),
            "found_per_letter": _per_letter(score),
            "agreement": agreement(found, choice),
        })

    # 3. Grille and key both unknown.
    joint_rows = []
    for index, start in enumerate(_PLANT_STARTS[:2]):
        plain, choice, key, square = _planted(start, drawn, substitute=True)
        score, found, letters = anneal_grille(square, None, random.Random(_SEED + 20 + index), 4, 60000)
        shuffled = square[:]
        drawn.shuffle(shuffled)
        control, _f, _l = anneal_grille(shuffled, None, random.Random(_SEED + 30 + index), 4, 60000)
        joint_rows.append({
            "true_per_letter": _per_letter(_quad(plain, logp)),
            "found_per_letter": _per_letter(score),
            "shuffled_per_letter": _per_letter(control),
            "agreement": agreement(found, choice),
            "key_letters_right": sum(letters[key[x]] == x for x in set(plain)),
            "distinct_letters": len(set(plain)),
        })
    cells = _cells()
    cell_score, _f, _l = anneal_grille(cells, None, random.Random(_SEED + 40), 4, 60000)
    cell_shuffles = []
    for draw in range(4):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score, _f, _l = anneal_grille(shuffled, None, random.Random(_SEED + 50 + draw), 4, 60000)
        cell_shuffles.append(_per_letter(score))
    cell_per_letter = _per_letter(cell_score)

    # 4. Unicity: key bits over the bits per letter this model saves.
    prose = letters_az(load_training_prose()).replace("J", "I")
    sample = [ord(ch) - 65 for ch in prose[_PLANT_STARTS[0]:_PLANT_STARTS[0] + 2000]]
    nats = -_quad(sample, logp) / (len(sample) - 3)
    saved_bits = math.log2(26) - nats / math.log(2)
    symbols = len(set(cells))
    key_bits = 2 * ORBITS + math.log2(math.factorial(26) / math.factorial(26 - symbols))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(cells),
        "orbits": ORBITS,
        "information_found": round(information, 4),
        "information_true": round(information_true, 4),
        "information_agreement": information_agreement,
        "known_key": known_rows,
        "known_key_recovered": sum(row["agreement"] == ORBITS for row in known_rows),
        "joint": joint_rows,
        "joint_recovered": sum(row["agreement"] == ORBITS for row in joint_rows),
        "cell_per_letter": cell_per_letter,
        "cell_shuffles_per_letter": cell_shuffles,
        "cell_shuffles_as_high": sum(score >= cell_per_letter for score in cell_shuffles),
        "model_nats_per_letter": round(nats, 4),
        "saved_bits_per_letter": round(saved_bits, 4),
        "key_bits": round(key_bits, 2),
        "unicity_letters": round(key_bits / saved_bits, 1),
        "scope": (
            "A grille search under a known key is the power check. The joint search did not "
            "recover a planted grille, so the grille class is not closed. The cells do not beat "
            "shuffled cells under the same search. No letter string is stored."
        ),
    }
