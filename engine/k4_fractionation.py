"""K4 under fractionating ciphers: a letter count for 5 by 5 squares, and trifid as SAT.

Any cipher whose output letters come from one 25-cell square (bifid, the
conjugated-matrix bifid, Playfair and its seriated form, two-square,
four-square, Phillips and other Polybius substitutions) can write at most 25
different letters. K4 uses all 26, so every such cipher is excluded outright,
whatever the key, period or language.

Trifid uses a 3 by 3 by 3 cube of 27 symbols. Inside each block of the period
it writes every symbol as three coordinates, reads them by rows (all layers,
then all rows, then all columns, the convention of `engine.solvers.trifid`)
and turns each new triple back into a symbol. The cube is left completely
unknown here: SAT variables place each of the 27 symbols in one cell, give
each plaintext position one symbol, and tie each ciphertext symbol to the
triple the block reads out. The clue letters fix their plaintext symbols.

Two lengths are run. With 97 letters the 27th symbol ('.') may appear in the
plaintext but never in the ciphertext. With 98 the question mark that ends
K3 on the sculpture is ciphertext position 0 and is the 27th symbol, and the
clue positions move up by one.

Only clue letters are used, so a blocked period is blocked whatever language
the rest of K4 is in. Planted texts with both clues under a random cube are
never blocked (`tests/test_k4_fractionation.py`).

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import random

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.solvers.k4_attempt import K4_CIPHERTEXT
from engine.solvers.trifid import TRIFID_ALPHABET, trifid_encrypt

SQUARE_CELLS = 25
SYMBOLS = TRIFID_ALPHABET  # 26 letters and '.'
CELLS = [(a, b, c) for a in range(3) for b in range(3) for c in range(3)]


def square_count_bound(ciphertext: str = K4_CIPHERTEXT) -> dict:
    """Distinct letters against the 25 a square can write."""
    distinct = len(set(ciphertext))
    return {"distinct_letters": distinct, "square_cells": SQUARE_CELLS,
            "excluded": distinct > SQUARE_CELLS, "solved": False, "claimed_plaintext": None}


def _pysat():
    try:
        from pysat.card import CardEnc, EncType
        from pysat.solvers import Solver
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("k4_fractionation needs the optional python-sat package") from exc
    return CardEnc, EncType, Solver


def setup(length: int = 97, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    """Ciphertext as trifid symbols and the clue letters at their positions."""
    if length == len(ciphertext) + 1:
        text, shift = "." + ciphertext, 1
    elif length == len(ciphertext):
        text, shift = ciphertext, 0
    else:
        raise ValueError("length must be the letter count or one more")
    known = {}
    for start, word in spans:
        for offset, ch in enumerate(word):
            known[start + offset + shift] = ch
    return {"n": length, "ct": text, "known": known}


class _Cnf:
    def __init__(self) -> None:
        self.top = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.top += 1
        return self.top

    def exactly_one(self, lits) -> None:
        CardEnc, EncType, _ = _pysat()
        enc = CardEnc.equals(lits=list(lits), bound=1, top_id=self.top, encoding=EncType.seqcounter)
        self.top = max(self.top, enc.nv)
        self.clauses.extend(enc.clauses)


def _encode(s: dict, period: int, known: dict):
    """CNF for one period. Returns the formula and the plaintext symbol variables."""
    n, ct = s["n"], s["ct"]
    f = _Cnf()
    # place[sym][cell]: symbol sym sits in cell.
    place = [[f.var() for _ in CELLS] for _ in SYMBOLS]
    for row in place:
        f.exactly_one(row)
    for cell in range(27):
        f.exactly_one([place[sym][cell] for sym in range(27)])
    touched = sorted({(i // period) * period for i in known})
    plain = {}
    for start in touched:
        block = list(range(start, min(start + period, n)))
        size = len(block)
        # digit[i][axis][v]: coordinate axis of plaintext position i is v.
        digit = {}
        for i in block:
            plain[i] = [f.var() for _ in SYMBOLS]
            f.exactly_one(plain[i])
            digit[i] = [[f.var() for _ in range(3)] for _ in range(3)]
            for axis in range(3):
                f.exactly_one(digit[i][axis])
            if i in known:
                f.clauses.append([plain[i][SYMBOLS.index(known[i])]])
            for sym in range(27):
                for cell, coords in enumerate(CELLS):
                    for axis in range(3):
                        f.clauses.append([-plain[i][sym], -place[sym][cell], digit[i][axis][coords[axis]]])
        # The block's coordinate stream: all layers, then rows, then columns.
        stream = [digit[i][axis] for axis in range(3) for i in block]
        for k in range(size):
            sym = SYMBOLS.index(ct[block[k]])
            triple = stream[3 * k : 3 * k + 3]
            for cell, coords in enumerate(CELLS):
                # The triple read out names the ciphertext symbol's cell, both ways.
                f.clauses.append([-triple[0][coords[0]], -triple[1][coords[1]], -triple[2][coords[2]],
                                  place[sym][cell]])
                for axis in range(3):
                    f.clauses.append([-place[sym][cell], triple[axis][coords[axis]]])
    return f, plain


def check(period: int, length: int = 97, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> str:
    """'sat' or 'unsat' for both clues at one period."""
    *_, Solver = _pysat()
    s = setup(length, ciphertext, spans)
    f, _ = _encode(s, period, s["known"])
    with Solver(name="cadical153", bootstrap_with=f.clauses) as solver:
        return "sat" if solver.solve() else "unsat"


def held_back(period: int, length: int = 97, fit: int = 0, ciphertext: str = K4_CIPHERTEXT,
              spans=CRIB_SPANS) -> dict:
    """Fit one clue (index fit), then count reserved letters forced right or wrong."""
    *_, Solver = _pysat()
    s = setup(length, ciphertext, spans)
    shift = 1 if length == len(ciphertext) + 1 else 0
    start, word = spans[fit]
    fitted = {start + k + shift: ch for k, ch in enumerate(word)}
    rstart, rword = spans[1 - fit]
    reserved = {rstart + k + shift: ch for k, ch in enumerate(rword)}
    # Only the fitted letters are fixed; reserved positions in the same blocks stay free.
    f, plain = _encode(s, period, fitted)
    right = wrong = 0
    with Solver(name="cadical153", bootstrap_with=f.clauses) as solver:
        if not solver.solve():
            return {"fit": "unsat", "right": 0, "wrong": 0, "free": len(reserved)}
        for i, ch in reserved.items():
            if i not in plain:
                continue  # its block holds no fitted letter, so nothing ties it
            lit = plain[i][SYMBOLS.index(ch)]
            can_be = solver.solve(assumptions=[lit])
            can_differ = solver.solve(assumptions=[-lit])
            right += can_be and not can_differ
            wrong += can_differ and not can_be
    return {"fit": "sat", "right": right, "wrong": wrong, "free": len(reserved) - right - wrong}


def planted(period: int, length: int, seed: int, spans=CRIB_SPANS) -> str:
    """A ciphertext with both clues planted under a random cube, letters only after position 0."""
    rng = random.Random(seed)
    while True:
        cube = "".join(rng.sample(SYMBOLS, 27))
        plain = [rng.choice(SYMBOLS[:26]) for _ in range(length)]
        shift = length - 97
        for start, word in spans:
            plain[start + shift : start + shift + len(word)] = word
        cipher = trifid_encrypt("".join(plain), cube, period)
        # 97 letters must not show the 27th symbol; 98 must show it only first.
        if length == 97 and "." not in cipher:
            return cipher
        if length == 98 and cipher[0] == "." and "." not in cipher[1:]:
            return cipher[1:]


def scan(periods=range(1, 99), lengths=(97, 98), workers: int = 1) -> dict:
    jobs = [(p, n) for n in lengths for p in periods if p <= n]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            results = list(pool.map(_job, jobs))
    else:
        results = [_job(job) for job in jobs]
    table = {str(n): {"sat": [], "unsat": []} for n in lengths}
    for (p, n), r in zip(jobs, results):
        table[str(n)][r].append(p)
    return {"model": "trifid, unknown cube, repo row-reading convention, clues only",
            "square_bound": square_count_bound(), "trifid": table,
            "solved": False, "claimed_plaintext": None}


def _job(job):
    p, n = job
    return check(p, n)


if __name__ == "__main__":
    import json
    import sys

    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(json.dumps(scan(workers=workers)))
