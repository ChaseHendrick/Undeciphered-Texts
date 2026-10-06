"""Digit ciphers other than Polybius pairs: excluded by the cells' digit alternation. Not a reading.

Without the final 000 the challenge's 392 digits alternate perfectly between
two classes: every even place holds one of 6, 7, 8, 9, 0 and every odd place
one of 1, 2, 3, 4, 5. No key can change that fact, so it is a test for digit
ciphers whose codes are not all pairs from two fixed classes:

- a straddling checkerboard (eight letters get one digit, the rest two digits
  behind one of two prefix digits), with a random layout;
- Nihilist substitution: a keyed 5 by 5 square's coordinates (11 to 55) plus a
  repeating keyword's coordinates, written as decimal numbers, so that sums run
  from 22 to 110; and the same with coordinates numbered 0 to 4.

For planted held-out English under random keys, the statistic is the best
share of the first 392 digits that alternate between any two classes of five
digits. The cells score 1.

No letter string is stored.
"""

from __future__ import annotations

import itertools
import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261021
_DIGITS = 392
_DRAWS = 300
_CLASSES = [set(c) for c in itertools.combinations("0123456789", 5)]


def alternation(digits: str) -> float:
    """Best share of places whose digit is in class A at even places and in its complement at odd places."""
    best = 0
    for first in _CLASSES:
        hits = sum((ch in first) == (i % 2 == 0) for i, ch in enumerate(digits))
        best = max(best, hits)
    return best / len(digits)


def checkerboard(text: str, rng: random.Random) -> str:
    digits = list("0123456789")
    rng.shuffle(digits)
    prefixes, singles = digits[:2], digits[2:]
    letters = list(PLAIN)
    rng.shuffle(letters)
    code = {}
    for k, ch in enumerate(letters[:8]):
        code[ch] = singles[k]
    for k, ch in enumerate(letters[8:]):
        code[ch] = prefixes[k // 10] + str(k % 10)
    return "".join(code[ch] for ch in text)


def nihilist(text: str, rng: random.Random, base: int) -> str:
    square = list(PLAIN)
    rng.shuffle(square)
    where = {ch: divmod(i, 5) for i, ch in enumerate(square)}
    period = rng.randrange(2, 15)
    key = [rng.choice(PLAIN) for _ in range(period)]
    out = []
    for i, ch in enumerate(text):
        r, c = where[ch]
        kr, kc = where[key[i % period]]
        out.append(str((r + base) * 10 + (c + base) + (kr + base) * 10 + (kc + base)))
    return "".join(out)


@frozen("dagapeyeff-digitcodes")
def digitcodes_report() -> dict:
    rng = random.Random(_SEED)
    printed = "".join(challenge_pairs())[:_DIGITS]
    systems = {
        "straddling checkerboard": lambda t: checkerboard(t, rng),
        "Nihilist, coordinates 1 to 5": lambda t: nihilist(t, rng, 1),
        "Nihilist, coordinates 0 to 4": lambda t: nihilist(t, rng, 0),
    }
    rows = {}
    for name, encode in systems.items():
        scores = []
        for k in range(_DRAWS):
            prose = _held(_HELD[k % len(_HELD)])
            start = rng.randrange(len(prose) - 400)
            digits = encode(prose[start:start + 400])[:_DIGITS]
            scores.append(alternation(digits))
        rows[name] = {"draws": _DRAWS, "best": round(max(scores), 4), "reaching_cells": sum(s >= 1.0 for s in scores)}
    return {"solved": False, "claimed_plaintext": None, "cells": alternation(printed), "systems": rows}
