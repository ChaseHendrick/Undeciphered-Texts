"""Ciphers that mix letters spread text over more symbols than the cells use. Not a reading.

The cells use 18 of the 25 symbols, 13 of them nearly equally. A cipher whose
output symbol depends on more than one plaintext letter, or on a key that
changes along the text, spreads ordinary text over more symbols. For each of
these families, held-out English windows of 196 letters are enciphered under
random keys and the number of different symbols is counted:

- 2 by 2 Hill over a keyed square (a random invertible matrix modulo 25);
- bifid over a keyed square, periods 2 to 14 and the whole text;
- autokey on the square: each cell's coordinates plus the previous plaintext
  letter's, modulo 5;
- a running key: the coordinates of a second English text added, modulo 5;
- Vigenere modulo 25 on a keyed alphabet, periods 2 to 14.

The statement holds for keys drawn at random. A degenerate key (a diagonal
Hill matrix, a constant shift) reduces to a plain square, which the corpus
count covers. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held

_SEED = 20261022
_LETTERS = 196
_STRIDE = 97
_DRAWS = 3


def hill(x: list[int], rng: random.Random) -> list[int]:
    while True:
        a, b, c, d = (rng.randrange(25) for _ in range(4))
        if (a * d - b * c) % 5:
            break
    out = []
    for k in range(0, len(x) - 1, 2):
        out += [(a * x[k] + b * x[k + 1]) % 25, (c * x[k] + d * x[k + 1]) % 25]
    return out


def bifid(x: list[int], period: int) -> list[int]:
    out = []
    for start in range(0, len(x), period):
        block = x[start:start + period]
        stream = [v // 5 for v in block] + [v % 5 for v in block]
        out += [stream[2 * i] * 5 + stream[2 * i + 1] for i in range(len(block))]
    return out


def autokey(x: list[int], rng: random.Random) -> list[int]:
    prev = rng.randrange(25)
    out = []
    for v in x:
        out.append(((v // 5 + prev // 5) % 5) * 5 + (v % 5 + prev % 5) % 5)
        prev = v
    return out


def running(x: list[int], key: list[int]) -> list[int]:
    return [((v // 5 + k // 5) % 5) * 5 + (v % 5 + k % 5) % 5 for v, k in zip(x, key)]


def vigenere25(x: list[int], period: int, rng: random.Random) -> list[int]:
    key = [rng.randrange(25) for _ in range(period)]
    return [(v + key[i % period]) % 25 for i, v in enumerate(x)]


@frozen("dagapeyeff-mixing")
def mixing_report() -> dict:
    rng = random.Random(_SEED)
    windows = [prose[s:s + _LETTERS] for prose in map(_held, _HELD) for s in range(0, len(prose) - _LETTERS, _STRIDE)]
    keytext = "".join(_held(name) for name in _HELD)
    cases = {"hill 2x2": lambda x: hill(x, rng), "autokey": lambda x: autokey(x, rng)}
    for period in (2, 3, 4, 5, 7, 14, _LETTERS):
        cases[f"bifid {period}"] = (lambda p: lambda x: bifid(x, p))(period)
    for period in (2, 3, 4, 5, 7, 14):
        cases[f"vigenere25 {period}"] = (lambda p: lambda x: vigenere25(x, p, rng))(period)

    def running_case(x):
        start = rng.randrange(len(keytext) - _LETTERS)
        return running(x, [PLAIN.index(ch) for ch in keytext[start:start + _LETTERS]])

    cases["running key"] = running_case
    cells = _cells()
    rows = {}
    for name, encode in cases.items():
        counts = []
        for window in windows:
            for _ in range(_DRAWS):
                label = rng.sample(range(25), 25)
                counts.append(len(set(encode([label[PLAIN.index(ch)] for ch in window]))))
        rows[name] = {"draws": len(counts), "fewest_distinct": min(counts),
                      "reaching_cells": sum(c <= len(set(cells)) for c in counts)}
    return {"solved": False, "claimed_plaintext": None, "cells_distinct": len(set(cells)), "cases": rows}
