"""K4 in-place models on unknown alphabets as pure SAT, with MaxSAT error counts.

The same families and the same clue-only evidence as `engine.k4_alphabet_csp`,
encoded with one boolean per (letter, rank) and per (column, shift) and solved
with CaDiCaL through PySAT. Modular shifts become implications between those
booleans, so no arithmetic reaches the solver. The answers must agree with the
Z3 module; `tests/test_k4_sat.py` checks that on the K4 scan.

`min_drops` asks RC2, a MaxSAT solver, for the fewest clue letters that must
be dropped for a family to fit. A dropped letter stands for a misspelled
plaintext letter or a wrong ciphertext letter. Sanborn left deliberate
misspellings in K1 to K3, so a model that fits with one or two dropped letters
is worth knowing about, but only against the same count on random ciphertexts:
dropping letters makes every model easier to fit.

Families: q3-vigenere, q3-beaufort, q1, q2, q4 (periodic), q3-progressive (step
1 to 25 per cycle), q3-ct-autokey and q4-ct-autokey (shift = row(c[i - L]) for
an arbitrary row map). For autokey a ciphertext error would also move a later
shift, so its drop counts are a lower bound.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import random

from engine.k4_gromark_obstruction import CRIB_SPANS, crib_pairs
from engine.solvers.k4_attempt import K4_CIPHERTEXT

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PERIODIC = ("q3-vigenere", "q3-beaufort", "q1", "q2", "q4")
PROGRESSIVE = ("q3-progressive",)
AUTOKEY = ("q3-ct-autokey", "q4-ct-autokey")
FAMILIES = PERIODIC + PROGRESSIVE + AUTOKEY


def _pysat():
    try:
        from pysat.card import CardEnc, EncType
        from pysat.examples.rc2 import RC2
        from pysat.formula import WCNF
        from pysat.solvers import Solver
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("k4_sat needs the optional python-sat package (requirements-synthesis.txt)") from exc
    return CardEnc, EncType, RC2, WCNF, Solver


class _Formula:
    def __init__(self) -> None:
        self.top = 0
        self.hard: list[list[int]] = []

    def var(self) -> int:
        self.top += 1
        return self.top

    def grid(self, rows: int, cols: int) -> list[list[int]]:
        return [[self.var() for _ in range(cols)] for _ in range(rows)]

    def exactly_one(self, literals) -> None:
        CardEnc, EncType, *_ = _pysat()
        encoded = CardEnc.equals(lits=list(literals), bound=1, top_id=self.top, encoding=EncType.seqcounter)
        self.top = max(self.top, encoded.nv)
        self.hard.extend(encoded.clauses)

    def permutation(self) -> list[list[int]]:
        grid = self.grid(26, 26)  # grid[letter][rank]
        for letter in range(26):
            self.exactly_one(grid[letter])
        for rank in range(26):
            self.exactly_one([grid[letter][rank] for letter in range(26)])
        return grid

    def shifts(self, count: int) -> list[list[int]]:
        grid = self.grid(count, 26)
        for row in grid:
            self.exactly_one(row)
        return grid


def _encode(family: str, parameter: int, ciphertext: str, pairs, step: int):
    """Hard clauses plus one guarded clause group per clue letter.

    Returns (formula, guards): guards[i] is a fresh variable that switches
    clue letter i on; it appears negated in every clause of that letter.
    """
    f = _Formula()
    plain = f.permutation()
    second = f.permutation() if family.startswith("q4") else plain
    f.hard.append([plain[0][0]])  # one alphabet rotation is a free gauge in every family here
    if family in AUTOKEY:
        row = f.shifts(26)
    else:
        key = f.shifts(parameter)
    guards = {}
    for i, c_letter, p_letter in pairs:
        c, p = LETTERS.index(c_letter), LETTERS.index(p_letter)
        g = f.var()
        guards[i] = g
        if family in AUTOKEY:
            if i < parameter:
                continue  # the primer is unknown
            shift = row[LETTERS.index(ciphertext[i - parameter])]
            offset = 0
        else:
            shift = key[i % parameter]
            offset = (step * (i // parameter)) % 26
        for k in range(26):
            total = (k + offset) % 26
            if family == "q1":
                # c = rank(p) + k: rank(p) must be c - k.
                f.hard.append([-g, -shift[k], plain[p][(c - total) % 26]])
            elif family == "q2":
                # crank(c) = p + k.
                f.hard.append([-g, -shift[k], plain[c][(p + total) % 26]])
            else:
                for v in range(26):
                    if family == "q3-beaufort":
                        target = (total - v) % 26
                    else:
                        target = (v + total) % 26
                    f.hard.append([-g, -plain[p][v], -shift[k], second[c][target]])
    return f, guards


def _steps(family: str) -> range:
    return range(1, 26) if family in PROGRESSIVE else range(0, 1)


def check(family: str, parameter: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> str:
    """'sat' or 'unsat' for both clues jointly."""
    *_, Solver = _pysat()
    pairs = crib_pairs(ciphertext, spans)
    for step in _steps(family):
        f, guards = _encode(family, parameter, ciphertext, pairs, step)
        with Solver(name="cadical153", bootstrap_with=f.hard) as solver:
            if solver.solve(assumptions=list(guards.values())):
                return "sat"
    return "unsat"


def min_drops(family: str, parameter: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    """Fewest clue letters to drop so the family fits, with one witness set."""
    _CardEnc, _EncType, RC2, WCNF, _Solver = _pysat()
    pairs = crib_pairs(ciphertext, spans)
    best = None
    for step in _steps(family):
        f, guards = _encode(family, parameter, ciphertext, pairs, step)
        wcnf = WCNF()
        for clause in f.hard:
            wcnf.append(clause)
        for g in guards.values():
            wcnf.append([g], weight=1)
        with RC2(wcnf) as rc2:
            model = rc2.compute()
            cost = rc2.cost
        if model is None:
            continue
        chosen = set(model)
        dropped = tuple(i for i, g in guards.items() if g not in chosen)
        if best is None or cost < best[0]:
            best = (cost, dropped)
        if best[0] == 0:
            break
    if best is None:
        return {"drops": None, "dropped": None}
    return {"drops": best[0], "dropped": best[1]}


def random_ciphertext(seed: int) -> str:
    rng = random.Random(seed)
    return "".join(rng.choice(LETTERS) for _ in range(97))


def _drops_job(job):
    family, parameter, text = job
    return min_drops(family, parameter, text)["drops"]


def drop_scan(families=FAMILIES, periods=range(1, 27), controls: int = 20, workers: int = 1,
              ciphertext: str = K4_CIPHERTEXT) -> dict:
    """Minimum drops on K4 and on random ciphertexts for each family and period."""
    jobs = []
    for family in families:
        for period in periods:
            jobs.append((family, period, ciphertext))
            jobs.extend((family, period, random_ciphertext(7919 * period + 31 * s + len(family))) for s in range(controls))
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            results = list(pool.map(_drops_job, jobs, chunksize=4))
    else:
        results = [_drops_job(job) for job in jobs]
    table: dict = {}
    for (family, period, text), drops in zip(jobs, results):
        row = table.setdefault(family, {}).setdefault(str(period), {"k4": None, "random": []})
        if text == ciphertext:
            row["k4"] = drops
        else:
            row["random"].append(drops)
    return {"model": "in-place, unknown alphabets, fewest clue letters dropped (MaxSAT)",
            "families": table, "solved": False, "claimed_plaintext": None}


def check_two_keys(first: int, second: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS,
                   beaufort: bool = False) -> str:
    """Two repeating keys added together on one unknown keyed alphabet.

    The shift at i is a[i mod first] + b[i mod second]. It is a special case
    of one key with period lcm(first, second), with far fewer free shifts, so
    the clues can test it where lcm exceeds what the one-key check can reach.
    """
    *_, Solver = _pysat()
    f = _Formula()
    rank = f.permutation()
    f.hard.append([rank[0][0]])
    a = f.shifts(first)
    b = f.shifts(second)
    f.hard.append([a[0][0]])  # (a + t, b - t) is the same cipher
    for i, c_letter, p_letter in crib_pairs(ciphertext, spans):
        c, p = LETTERS.index(c_letter), LETTERS.index(p_letter)
        shift = f.shifts(1)[0]
        for u in range(26):
            for w in range(26):
                f.hard.append([-a[i % first][u], -b[i % second][w], shift[(u + w) % 26]])
        for k in range(26):
            for v in range(26):
                target = (k - v) % 26 if beaufort else (v + k) % 26
                f.hard.append([-rank[p][v], -shift[k], rank[c][target]])
    with Solver(name="cadical153", bootstrap_with=f.hard) as solver:
        return "sat" if solver.solve() else "unsat"


def planted_two_keys(first: int, second: int, seed: int, spans=CRIB_SPANS, beaufort: bool = False) -> str:
    rng = random.Random(seed)
    plain = [rng.randrange(26) for _ in range(97)]
    for start, word in spans:
        plain[start : start + len(word)] = [LETTERS.index(ch) for ch in word]
    alphabet = rng.sample(range(26), 26)
    inverse = {r: letter for letter, r in enumerate(alphabet)}
    a = [rng.randrange(26) for _ in range(first)]
    b = [rng.randrange(26) for _ in range(second)]
    out = []
    for i, letter in enumerate(plain):
        k = a[i % first] + b[i % second]
        rank = (k - alphabet[letter]) % 26 if beaufort else (alphabet[letter] + k) % 26
        out.append(LETTERS[inverse[rank]])
    return "".join(out)


def _two_key_job(job):
    first, second, beaufort, text = job
    return check_two_keys(first, second, text, beaufort=beaufort)


def two_key_scan(top: int = 26, workers: int = 1, ciphertext: str = K4_CIPHERTEXT) -> dict:
    """Every pair 2 <= first < second <= top, Vigenere and Beaufort sense."""
    jobs = [(m, n, beaufort, ciphertext) for beaufort in (False, True)
            for m in range(2, top + 1) for n in range(m + 1, top + 1)]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            results = list(pool.map(_two_key_job, jobs, chunksize=4))
    else:
        results = [_two_key_job(job) for job in jobs]
    table = {"vigenere": {"sat": [], "unsat": []}, "beaufort": {"sat": [], "unsat": []}}
    for (m, n, beaufort, _text), result in zip(jobs, results):
        table["beaufort" if beaufort else "vigenere"][result].append([m, n])
    return {"model": "two added repeating keys on one unknown keyed alphabet, clues only",
            "senses": table, "solved": False, "claimed_plaintext": None}


if __name__ == "__main__":
    import json
    import sys

    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    controls = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    print(json.dumps(drop_scan(workers=workers, controls=controls)["families"], indent=1))
