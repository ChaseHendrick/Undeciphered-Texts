"""K4 in-place substitution with unknown keyed alphabets: exact SMT checks.

Every model here keeps each letter in its place and enciphers it with a
shift on keyed alphabets that are left completely unknown. Nothing is
assumed about the keyword, and no language model is used: the only
evidence is the two published clues, EASTNORTHEAST at 21 and BERLINCLOCK
at 63. A result therefore holds whatever language the rest of K4 is in.

Ranks are positions of letters in an unknown alphabet. The families are

- periodic Quagmire III, Vigenere sense: rank(c) = rank(p) + K[i mod n]
  (straight Vigenere and the K1/K2 keyed Vigenere with any keyword)
- periodic Quagmire III, Beaufort sense: rank(c) = K[i mod n] - rank(p)
- periodic Quagmire I: c = prank(p) + K[i mod n]
- periodic Quagmire II: crank(c) = p + K[i mod n]
- periodic Quagmire IV: crank(c) = prank(p) + K[i mod n]
- progressive Quagmire III: the period's key gains s each cycle
- ciphertext autokey with lag L on one keyed alphabet: the shift at i is
  row(c[i - L]) for an arbitrary map row from key letter to shift, which
  covers every way of reading a tableau row from a key letter
- the same with a plain and a cipher alphabet that differ (Quagmire IV)
- plaintext autokey with lag L, on one or two keyed alphabets; it binds
  only where the key letter falls inside a clue

Unsatisfiable means no alphabet, keyword, key or primer of that family
places both clues. Satisfiable means the clues do not rule it out; the
held-back check then counts how many letters of one clue the other clue
forces. A forced letter is one that a second query cannot make different.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import random

from engine.k4_gromark_obstruction import CRIB_SPANS, crib_pairs
from engine.solvers.k4_attempt import K4_CIPHERTEXT

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PERIODIC = ("q3-vigenere", "q3-beaufort", "q1", "q2", "q4")
PROGRESSIVE = ("q3-progressive",)
AUTOKEY = ("q3-ct-autokey", "q4-ct-autokey", "q3-pt-autokey", "q4-pt-autokey")
FAMILIES = PERIODIC + PROGRESSIVE + AUTOKEY


def _z3():
    try:
        import z3
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("k4_alphabet_csp needs the optional z3-solver (requirements-synthesis.txt)") from exc
    return z3


def _mod26(z3, expression):
    """expression is 0 mod 26, for an expression bounded by -77..77."""
    return z3.Or([expression == value for value in (-78, -52, -26, 0, 26, 52, 78)])


def _ranks(z3, solver, name):
    ranks = [z3.Int(f"{name}_{letter}") for letter in LETTERS]
    solver.add([z3.And(r >= 0, r < 26) for r in ranks])
    solver.add(z3.Distinct(ranks))
    return ranks


def _shifts(z3, solver, name, count):
    shifts = [z3.Int(f"{name}_{index}") for index in range(count)]
    solver.add([z3.And(s >= 0, s < 26) for s in shifts])
    return shifts


def _build(family: str, parameter: int, ciphertext: str, pairs, step: int = 0):
    """Solver plus a function giving the plaintext letter expression at a position.

    parameter is the period for periodic families and the lag for autokey.
    """
    z3 = _z3()
    solver = z3.Solver()
    solver.set(random_seed=0)
    rank = _ranks(z3, solver, "rank")
    other = _ranks(z3, solver, "crank") if family.startswith("q4") else rank
    solver.add(rank[0] == 0)  # one alphabet rotation is a free gauge in every family here

    if family in PERIODIC or family in PROGRESSIVE:
        key = _shifts(z3, solver, "key", parameter)
        # A progressive key adds step times the cycle number. The step is
        # fixed per instance (see _steps) so every relation stays mod 26.

        def relation(i, c, p):
            k = key[i % parameter] + (step * (i // parameter)) % 26
            if family == "q3-beaufort":
                return _mod26(z3, rank[c] + rank[p] - k)
            if family == "q1":
                return _mod26(z3, c - rank[p] - k)
            if family == "q2":
                return _mod26(z3, rank[c] - p - k)
            if family == "q4":
                return _mod26(z3, other[c] - rank[p] - k)
            return _mod26(z3, rank[c] - rank[p] - k)
    else:
        row = _shifts(z3, solver, "row", 26)
        known = {i: p_letter for i, _c, p_letter in pairs}

        def relation(i, c, p):
            if i < parameter:
                return z3.BoolVal(True)  # the primer is unknown
            if "-pt-" in family:
                if i - parameter not in known:
                    return z3.BoolVal(True)  # the key letter is unknown plaintext
                k = row[LETTERS.index(known[i - parameter])]
            else:
                k = row[LETTERS.index(ciphertext[i - parameter])]
            return _mod26(z3, other[c] - rank[p] - k)

    for i, c_letter, p_letter in pairs:
        solver.add(relation(i, LETTERS.index(c_letter), LETTERS.index(p_letter)))
    return z3, solver, relation


def check(family: str, parameter: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> str:
    """'sat' or 'unsat' for both clues jointly. 'unknown' never counts as either."""
    pairs = crib_pairs(ciphertext, spans)
    results = set()
    for step in _steps(family):
        _z3_module, solver, _ = _build(family, parameter, ciphertext, pairs, step)
        result = str(solver.check())
        if result == "sat":
            return "sat"
        results.add(result)
    return "unknown" if "unknown" in results else "unsat"


def _steps(family: str) -> range:
    """Progressive steps 1..25 (step 0 is the periodic family); one pass otherwise."""
    return range(1, 26) if family in PROGRESSIVE else range(0, 1)


def held_back(family: str, parameter: int, ciphertext: str = K4_CIPHERTEXT,
              fit=CRIB_SPANS[0], reserve=CRIB_SPANS[1]) -> dict:
    """Fit one clue, then ask which reserved letters that fit forces.

    A reserved letter is forced right when the fit cannot be completed with
    any other plaintext letter there, and forced wrong when it cannot be
    completed with the clue letter. Otherwise it is free.
    """
    start, word = reserve
    clue_ok = [False] * len(word)
    other_ok = [False] * len(word)
    fitted = False
    for step in _steps(family):
        z3, solver, relation = _build(family, parameter, ciphertext, crib_pairs(ciphertext, (fit,)), step)
        if str(solver.check()) != "sat":
            continue
        fitted = True
        for offset, letter in enumerate(word):
            i = start + offset
            c = LETTERS.index(ciphertext[i])
            target = LETTERS.index(letter)
            solver.push()
            solver.add(relation(i, c, target))
            clue_ok[offset] |= str(solver.check()) == "sat"
            solver.pop()
            solver.push()
            # The plaintext letter is free when some other letter also fits.
            solver.add(z3.Or([relation(i, c, v) for v in range(26) if v != target]))
            other_ok[offset] |= str(solver.check()) == "sat"
            solver.pop()
    if not fitted:
        return {"fit": "unsat", "right": 0, "wrong": 0, "free": len(word)}
    right = sum(1 for a, b in zip(clue_ok, other_ok) if a and not b)
    wrong = sum(1 for a, b in zip(clue_ok, other_ok) if b and not a)
    return {"fit": "sat", "right": right, "wrong": wrong, "free": len(word) - right - wrong}


def planted(family: str, parameter: int, seed: int, spans=CRIB_SPANS) -> str:
    """A 97-letter ciphertext with both clues planted under a random key of the family."""
    rng = random.Random(seed)
    plain = [rng.choice(LETTERS) for _ in range(97)]
    for start, word in spans:
        plain[start : start + len(word)] = word
    p = [LETTERS.index(ch) for ch in plain]
    alphabet = rng.sample(range(26), 26)  # letter -> rank
    second = rng.sample(range(26), 26) if family.startswith("q4") else alphabet
    inverse = {r: letter for letter, r in enumerate(second)}
    out: list[int] = []
    if family in PERIODIC or family in PROGRESSIVE:
        key = [rng.randrange(26) for _ in range(parameter)]
        step = rng.randrange(1, 26) if family in PROGRESSIVE else 0
        for i, letter in enumerate(p):
            k = key[i % parameter] + step * (i // parameter)
            if family == "q3-beaufort":
                out.append(inverse[(k - alphabet[letter]) % 26])
            elif family == "q1":
                out.append((alphabet[letter] + k) % 26)
            elif family == "q2":
                out.append({r: l for l, r in enumerate(alphabet)}[(letter + k) % 26])
            else:
                out.append(inverse[(alphabet[letter] + k) % 26])
    else:
        row = [rng.randrange(26) for _ in range(26)]
        for i, letter in enumerate(p):
            source = p if "-pt-" in family else out
            k = rng.randrange(26) if i < parameter else row[source[i - parameter]]
            out.append(inverse[(alphabet[letter] + k) % 26])
    return "".join(LETTERS[v] for v in out)


def _check_job(job):
    family, parameter, ciphertext = job
    return family, parameter, check(family, parameter, ciphertext)


def scan(families=FAMILIES, max_parameter: int = 96, ciphertext: str = K4_CIPHERTEXT, workers: int = 1) -> dict:
    """Joint satisfiability for every family and period or lag 1..max_parameter."""
    jobs = [(family, parameter, ciphertext) for family in families for parameter in range(1, max_parameter + 1)]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            results = list(pool.map(_check_job, jobs))
    else:
        results = [_check_job(job) for job in jobs]
    table = {family: {"sat": [], "unsat": [], "unknown": []} for family in families}
    for family, parameter, result in results:
        table[family][result].append(parameter)
    return {
        "model": "in-place substitution on unknown keyed alphabets, clues only, no language model",
        "families": table,
        "solved": False,
        "claimed_plaintext": None,
    }


if __name__ == "__main__":
    import json
    import sys

    top = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    print(json.dumps(scan(max_parameter=top, workers=workers)["families"], indent=1))
