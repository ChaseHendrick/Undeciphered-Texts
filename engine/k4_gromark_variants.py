"""K4 under Gromark variants: the digit bound generalized, and Periodic Gromark as SAT.

The committed obstruction `engine.k4_gromark_obstruction` rules out in-place ACA
Gromark for any keyword because ciphertext letters F, K and P cannot share one
alphabet index with both public cribs while every shift lies in digits 0 to 9.
That argument never used the chain addition, the primer length or the keyword
alphabet; this module states it in its general form and machine-checks it.

- Any in-place cipher with one cipher alphabet and a per-letter shift equal to a
  digit 0 to 9 from any digit stream, added or subtracted (the two Gronsfeld
  senses), is excluded for any keyword, primer, recurrence and lag. The same
  three letters carry the contradiction under both senses.
- In-place ACA Periodic Gromark with the keyword left free is excluded at every
  head length 2 to 9. The SAT model (`check`) is written in a relaxed space that
  is a superset of every real keyword: any distinct alphabet positions for the
  head letters, any rank permutation as the primer, and cipher indexes free per
  crib letter. A head length that cannot place both clues there cannot place
  them under any keyword either. Head lengths 2 and 3 are cross-checked against
  exhaustive enumeration of the relaxed space; planted texts under random
  keywords are never blocked (`tests/test_k4_gromark_variants.py`).

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import itertools
import random

from engine.k4_gromark_obstruction import CRIB_SPANS, crib_pairs
from engine.solvers.gromark import (ACA_GROMARK_CIPHER, ACA_GROMARK_KEY,
                                    ACA_GROMARK_PLAIN, gromark_decrypt,
                                    gromark_encrypt)
from engine.solvers.k4_attempt import K4_CIPHERTEXT
from engine.solvers.periodic_gromark import periodic_gromark_encrypt

HEAD_LENGTHS = range(2, 10)
LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_INDEX = {ch: i for i, ch in enumerate(LET)}


def digit_bound(ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS, sense: str = "add",
                digits=range(10)) -> dict:
    """Cipher letters with no allowed alphabet index under every crib use.

    For one cipher alphabet and shifts by digits only, the same ciphertext
    letter at two crib letters forces one alphabet index to satisfy both.
    Sense 'add' is the ACA Gromark sense (index = plain index + digit) and
    'subtract' its Beaufort sense (index = plain index - digit). The bounds
    depend on no alphabet, no primer length and no recurrence, so a digit
    stream of any construction is covered either way it is applied.
    """
    if sense not in ("add", "subtract"):
        raise ValueError("sense must be 'add' or 'subtract'")
    by_letter: dict[str, set[int]] = {}
    for _position, cipher_letter, plain_letter in crib_pairs(ciphertext, spans):
        plain_index = ALPHABET_INDEX[plain_letter]
        if sense == "add":
            allowed = {(plain_index + digit) % 26 for digit in digits}
        else:
            allowed = {(plain_index - digit) % 26 for digit in digits}
        if cipher_letter not in by_letter:
            by_letter[cipher_letter] = allowed
        else:
            by_letter[cipher_letter] &= allowed
    blocked = sorted(letter for letter, allowed in by_letter.items() if not allowed)
    return {"sense": sense, "blocked_letters": blocked, "blocked": bool(blocked),
            "solved": False, "claimed_plaintext": None}


def controls_digit_bound(trials: int = 20, seed: int = 331) -> dict:
    """Planted Gromark texts (sheet fixtures and random keys) never block.

    The ACA sheet example is first recovered as a known-plaintext check, then
    97-letter windows with both clues planted are enciphered under random
    keywords and primers. Neither sense may produce an empty domain there.
    """
    assert gromark_decrypt(ACA_GROMARK_CIPHER, ACA_GROMARK_KEY) == ACA_GROMARK_PLAIN
    rng = random.Random(seed)
    for _ in range(trials):
        keyword = "".join(rng.sample(LET, 5))
        primer = "".join(rng.choice("0123456789") for _ in range(5))
        window = "".join(rng.choice(LET) for _ in range(97))
        window = (window[:21] + "EASTNORTHEAST" + window[34:63]
                  + "BERLINCLOCK" + window[74:])
        cipher = gromark_encrypt(window, f"{keyword} {primer}")
        for sense in ("add", "subtract"):
            report = digit_bound(cipher, sense=sense)
            if report["blocked"]:
                raise AssertionError(f"planted Gromark text blocked under {sense}: "
                                     f"{report['blocked_letters']}")
    return {"windows": trials, "blocked": 0,
            "solved": False, "claimed_plaintext": None}


def _pysat():
    try:
        from pysat.card import CardEnc, EncType
        from pysat.solvers import Solver
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("k4_gromark_variants needs the optional python-sat package") from exc
    return CardEnc, EncType, Solver


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


def spec_of(ciphertext: str, spans=CRIB_SPANS) -> tuple[tuple[int, str, str], ...]:
    """(position, ciphertext letter, plaintext letter) for each clue letter."""
    return crib_pairs(ciphertext, spans)


def relaxed_cnf(k: int, ciphertext: str, spec, fits=(0, 1)) -> dict:
    """CNF for in-place Periodic Gromark with the head length k left free.

    Relaxed space, a superset of every real head of length k:
    - s[g] is the alphabet position of head letter g, any distinct 0..25;
    - rho[g] is its rank, any permutation of 1..k, so the primer is rho[0..k-1];
    - the rank-digit chain extends by (r[i-k] + r[i-k+1]) % 10, as in
      `engine.solvers.periodic_gromark.periodic_gromark_running_key`;
    - t[c] is the alphabet position of cipher letter c, free per crib letter.
    Equations: t[c] = index(plain) + s[(i//k)%k] + r[i] (mod 26) at fitted clues.
    """
    CardEnc, _, _ = _pysat()
    n = len(ciphertext)
    f = _Cnf()
    s_g = [[f.var() for _ in range(26)] for _ in range(k)]
    for g in range(k):
        f.exactly_one(s_g[g])
    for g, h in itertools.combinations(range(k), 2):
        for v in range(26):
            f.clauses.append([-s_g[g][v], -s_g[h][v]])
    rho = [[f.var() for _ in range(1, k + 1)] for _ in range(k)]
    for g in range(k):
        f.exactly_one(rho[g])
    for j in range(1, k + 1):
        f.exactly_one([rho[g][j - 1] for g in range(k)])
    r = []
    for i in range(n):
        vals = [f.var() for _ in range(10)]
        f.exactly_one(vals)
        if i < k:
            # the chain-added primer starts as the rank digits 1..k of the head
            f.clauses.append([-vals[0]])
            for j in range(k + 1, 10):
                f.clauses.append([-vals[j]])
            for j in range(1, k + 1):
                f.clauses.append([-rho[i][j - 1], vals[j]])
                f.clauses.append([rho[i][j - 1], -vals[j]])
        else:
            for a in range(10):
                for b in range(10):
                    q = (a + b) % 10
                    for d in range(10):
                        if d == q:
                            f.clauses.append([-r[i - k][a], -r[i - k + 1][b], vals[d]])
                        else:
                            f.clauses.append([-r[i - k][a], -r[i - k + 1][b], -vals[d]])
        r.append(vals)
    letters = sorted({c for _, c, _ in spec})
    t = {ch: [f.var() for _ in range(26)] for ch in letters}
    for ch in letters:
        f.exactly_one(t[ch])
    fitted, reserved = {}, {}
    for which in (0, 1):
        start, word = CRIB_SPANS[which]
        target = fitted if which in fits else reserved
        for offset, ch in enumerate(word):
            target[start + offset] = ch
    t_on, t_off = {}, {}

    def add_eq(guard: int, pos: int, plain_letter: str, force: bool) -> None:
        """(guard => cipher letter index satisfies/misses the plain letter)."""
        group = (pos // k) % k
        base = ALPHABET_INDEX[plain_letter]
        for s in range(26):
            for d in range(10):
                v = (base + s + d) % 26
                lit = t[ciphertext[pos]][v]
                sign = lit if force else -lit
                f.clauses.append([-guard, -s_g[group][s], -r[pos][d], sign])

    pos_seen = sorted({p for p, _, _ in spec})
    for pos in pos_seen:
        t_on[pos] = f.var()
        t_off[pos] = f.var()
        if pos in fitted:
            add_eq(t_on[pos], pos, fitted[pos], True)
            f.clauses.append([t_on[pos]])
            f.clauses.append([-t_off[pos]])
    return {"f": f, "s": s_g, "r": r, "t": t, "t_on": t_on, "t_off": t_off,
            "fitted": fitted, "reserved": reserved, "pos_seen": pos_seen}


def check(k: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS, fits=(0, 1)) -> str:
    """'sat' or 'unsat' for the clues at one head length in the relaxed space."""
    *_, Solver = _pysat()
    cnf = relaxed_cnf(k, ciphertext, spec_of(ciphertext, spans), fits)
    with Solver(name="cadical153", bootstrap_with=cnf["f"].clauses) as solver:
        return "sat" if solver.solve() else "unsat"


def fit_fold(k: int, fit: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    """Fit one clue, then count reserved letters forced right, wrong or free."""
    *_, Solver = _pysat()
    cnf = relaxed_cnf(k, ciphertext, spec_of(ciphertext, spans), fits=(fit,))
    out = {"k": k, "fit": fit, "fit_sat": True, "right": 0, "wrong": 0, "free": 0}
    with Solver(name="cadical153", bootstrap_with=cnf["f"].clauses) as solver:
        if not solver.solve():
            out["fit_sat"] = False
            return out
        for pos in cnf["reserved"]:
            plain_letter = cnf["reserved"][pos]
            cipher_letter = ciphertext[pos]
            group = (pos // k) % k
            base = ALPHABET_INDEX[plain_letter]
            for s in range(26):
                for d in range(10):
                    v = (base + s + d) % 26
                    solver.add_clause([-cnf["t_on"][pos], -cnf["s"][group][s], -cnf["r"][pos][d],
                                       cnf["t"][cipher_letter][v]])
                    solver.add_clause([-cnf["t_off"][pos], -cnf["s"][group][s], -cnf["r"][pos][d],
                                       -cnf["t"][cipher_letter][v]])
            can_be = solver.solve(assumptions=[cnf["t_on"][pos]])
            can_differ = solver.solve(assumptions=[cnf["t_off"][pos]])
            if can_be and not can_differ:
                out["right"] += 1
            elif can_differ and not can_be:
                out["wrong"] += 1
            else:
                out["free"] += 1
    out["reserved"] = out["right"] + out["wrong"] + out["free"]
    return out


def excavate(k: int, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    """Exhaustive count of relaxed configs that place both clues; small k only."""
    if not 2 <= k <= 5:
        raise ValueError("exhaustive relaxation is for head lengths 2 to 5")
    n_fit = 0
    positions = [(p, c, pl) for p, c, pl in crib_pairs(ciphertext, spans)]
    for s_vals in itertools.permutations(range(26), k):
        for rho in itertools.permutations(range(1, k + 1)):
            chain = list(rho)
            last = max(p for p, _, _ in positions)
            for i in range(k, last + 1):
                chain.append((chain[i - k] + chain[i - k + 1]) % 10)
            needed: dict[str, int] = {}
            fits = True
            for p, cipher, plain in positions:
                v = (ALPHABET_INDEX[plain] + s_vals[(p // k) % k] + chain[p]) % 26
                if cipher in needed and needed[cipher] != v:
                    fits = False
                    break
                needed[cipher] = v
            if fits:
                n_fit += 1
    return {"k": k, "fitting_configs": n_fit, "solved": False, "claimed_plaintext": None}


def planted_key(k: int, seed: int) -> str:
    """The head that planted(k, seed) encrypts under, for true-key controls."""
    rng = random.Random(seed)
    return "".join(rng.sample(LET, k))


def planted(k: int, seed: int, spans=CRIB_SPANS) -> str:
    """A ciphertext under a random head of length k with both clues planted."""
    rng = random.Random(seed)
    head = planted_key(k, seed)
    plain = [rng.choice(LET) for _ in range(97)]
    for start, word in spans:
        plain[start:start + len(word)] = word
    return periodic_gromark_encrypt("".join(plain), keyword=head)


def scan(workers: int = 1, head_lengths=HEAD_LENGTHS) -> dict:
    """The module result: digit bounds, periodic SAT, folds, controls.

    head_lengths reduces the periodic side for quick contract checks; the
    full scan covers head lengths 2 to 9.
    """
    bounds = {"add": digit_bound(sense="add"), "subtract": digit_bound(sense="subtract")}
    controls = controls_digit_bound()
    jobs = [(k, "both") for k in head_lengths]
    jobs += [(k, 0) for k in head_lengths] + [(k, 1) for k in head_lengths]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            rows = list(pool.map(_job, jobs))
    else:
        rows = [_job(job) for job in jobs]
    both = {str(j[0]): payload["answer"]
            for j, row in zip(jobs, rows) if j[1] == "both"
            for payload in [row[2]]}
    fold_e = {str(j[0]): row[2] for j, row in zip(jobs, rows) if j[1] == 0}
    fold_b = {str(j[0]): row[2] for j, row in zip(jobs, rows) if j[1] == 1}
    contradiction = []
    for k in head_lengths:
        sat = both[str(k)] == "unsat"
        folds = fold_e[str(k)], fold_b[str(k)]
        fits_nothing = any(not f["fit_sat"] for f in folds)
        forces_wrong = any(f["wrong"] > 0 for f in folds)
        if sat or fits_nothing or forces_wrong:
            contradiction.append(k)
    return {
        "model": ("in-place Gromark family: one cipher alphabet over a digit stream "
                  "(any primer, recurrence, lag), senses add and subtract; "
                  "in-place ACA Periodic Gromark with the keyword left free"),
        "digit_bounds": bounds,
        "gromark_controls": controls,
        "periodic_both_clues": both,
        "fold_east_northeast": {k: {kk: vv for kk, vv in fold_e[k].items()} for k in fold_e},
        "fold_berlinclock": {k: {kk: vv for kk, vv in fold_b[k].items()} for k in fold_b},
        "excluded_head_lengths": contradiction,
        "solved": False,
        "claimed_plaintext": None,
    }


def _job(job):
    k, kind = job
    ct = K4_CIPHERTEXT
    if kind == "both":
        return (k, kind, {"answer": check(k, ct)})
    return (k, kind, fit_fold(k, kind, ct))


if __name__ == "__main__":
    import json
    import sys

    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(json.dumps(scan(workers=workers)))
