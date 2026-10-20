"""K4 under lagged-Fibonacci letter keys: linear algebra and exact SAT.

One cipher alphabet, in place: each plaintext index i is enciphered at
alphabet position (plain index + s * R[i]) mod 26, where the key stream R
over Z26 follows a lagged-Fibonacci letter chain with an m-letter primer,

    R[i] = (R[i-a] + rec_sign * R[i-b]) mod 26,   i >= m,  a, b <= m,

and s = +1 (Vigenere sense) or -1 (Beaufort sense) is how the stream is
applied. The digit Gromark is the same shape with R over digits 0 to 9 and
the period head dividing the positions; here the stream is letters.

Two exact methods, cross-checked:

- `linear_probe` writes the same-crib-letter equations as congruences in the
  primer: every R[i] is a known linear combination of R[0..m-1], and two uses
  of one ciphertext letter at positions i, j give
  (w_i - w_j) . primer = apply_sign * (plain_j - plain_i) (mod 26).
  Gaussian elimination over Z26 (units used as pivots) yields the affine
  solution space; each candidate is then checked for a consistent, distinct
  alphabet placement of the crib letters. Excluded means no primer survives.
- `check` is the exact SAT of the same model with the stream one-hot per
  position and the chain added by implication, covering the primer lengths
  where the affine space is too large to enumerate.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import itertools
import random

from engine.k4_gromark_obstruction import CRIB_SPANS, crib_pairs
from engine.k4_gromark_variants import _Cnf
from engine.solvers.k4_attempt import K4_CIPHERTEXT
from pysat.solvers import Solver

LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_INDEX = {ch: i for i, ch in enumerate(LET)}

# How many stream letters the longest crib needs.
MAX_POSITION = max(start + len(word) for start, word in CRIB_SPANS)


def coefficients(m: int, a: int, b: int, rec_sign: int, length: int) -> list[list[int]]:
    """R[i] as a linear combination of the primer R[0..m-1] over Z26."""
    if not 1 <= a <= m or not 1 <= b <= m:
        raise ValueError("lags a and b must both be at most the primer length m")
    rows = []
    for i in range(length):
        if i < m:
            vec = [0] * m
            vec[i] = 1
            rows.append(vec)
        else:
            base = list(rows[i - a])
            other = rows[i - b]
            for t in range(m):
                base[t] = (base[t] + rec_sign * other[t]) % 26
            rows.append(base)
    return rows


def _is_unit(x: int) -> bool:
    """Units of Z26: odd and not divisible by 13."""
    x %= 26
    return x != 0 and x % 2 != 0 and x % 13 != 0


def _inverse(x: int) -> int:
    x %= 26
    for y in range(1, 26):
        if (x * y) % 26 == 1:
            return y
    raise ValueError(f"{x} is not a unit mod 26")


def _reduce(rows: list[list[int]], rhs: list[int], m: int) -> tuple[list[int], list[list[int]], int]:
    """Row-reduce the congruence system; returns (pivot_cols, reduced_rows, rank)."""
    A = [list(r) + [rhs[i] % 26] for i, r in enumerate(rows)]
    pivot_cols: list[int] = []
    r = 0
    for c in range(m):
        pr = None
        for i in range(r, len(A)):
            if _is_unit(A[i][c]):
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = _inverse(A[r][c])
        A[r] = [(x * inv) % 26 for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % 26 != 0:
                factor = A[i][c]
                A[i] = [(A[i][t] - factor * A[r][t]) % 26 for t in range(m + 1)]
        pivot_cols.append(c)
        r += 1
        if r == len(A):
            break
    return pivot_cols, A, r


def linear_probe(m: int, a: int = None, b: int = None, rec_sign: int = 1, apply_sign: int = 1,
                 ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS,
                 limit: int = 200_000) -> dict:
    """Excluded / fits / too-many for one chain shape, from the primer congruences.

    Only validly zero-free rows are pivots; rows whose leading coefficient is
    a non-unit never pivot, so a reported exclusion still requires every
    remaining row to be checked against each candidate (done below), and a
    'too-many' answer means the affine space was not enumerated.
    """
    a = m if a is None else a
    b = m - 1 if b is None else b
    pairs = crib_pairs(ciphertext, spans)
    rows = coefficients(m, a, b, rec_sign, MAX_POSITION)
    by_letter: dict[str, list[tuple[int, str]]] = {}
    for position, cipher_letter, plain_letter in pairs:
        by_letter.setdefault(cipher_letter, []).append((position, plain_letter))
    eq_rows, eq_rhs = [], []
    for uses in by_letter.values():
        for (pi, pli), (pj, plj) in itertools.combinations(uses, 2):
            eq_rows.append([(rows[pi][t] - rows[pj][t]) % 26 for t in range(m)])
            eq_rhs.append((apply_sign * (ALPHABET_INDEX[plj] - ALPHABET_INDEX[pli])) % 26)
    pivot_cols, reduced, rank = _reduce(eq_rows, eq_rhs, m)
    for row in reduced[rank:]:
        if all(x % 26 == 0 for x in row[:m]) and row[m] % 26 != 0:
            return {"m": m, "a": a, "b": b, "rec_sign": rec_sign, "apply_sign": apply_sign,
                    "answer": "excluded", "primers": 0, "rank": rank,
                    "solved": False, "claimed_plaintext": None}
    free = [c for c in range(m) if c not in pivot_cols]
    count = 26 ** len(free)
    if count > limit:
        return {"m": m, "a": a, "b": b, "rec_sign": rec_sign, "apply_sign": apply_sign,
                "answer": "too-many", "primers": None, "rank": rank,
                "solved": False, "claimed_plaintext": None}
    consistent = 0
    distinct = 0
    for assign in itertools.product(range(26), repeat=len(free)):
        primer = [0] * m
        for c, value in zip(free, assign):
            primer[c] = value
        for pc, row in zip(pivot_cols, reduced[:rank]):
            primer[pc] = (row[m] - sum(row[c] * primer[c] for c in free)) % 26
        if any(sum(row[t] * primer[t] for t in range(m)) % 26 != row[m] % 26 for row in reduced):
            continue
        consistent += 1
        stream = [sum(rows[i][t] * primer[t] for t in range(m)) % 26 for i in range(MAX_POSITION)]
        placement: dict[str, int] = {}
        ok = True
        for position, cipher_letter, plain_letter in pairs:
            target = (ALPHABET_INDEX[plain_letter] + apply_sign * stream[position]) % 26
            if cipher_letter in placement:
                if placement[cipher_letter] != target:
                    ok = False
                    break
            elif target in placement.values():
                ok = False
                break
            else:
                placement[cipher_letter] = target
        if ok:
            distinct += 1
    return {"m": m, "a": a, "b": b, "rec_sign": rec_sign, "apply_sign": apply_sign,
            "answer": "fits" if distinct else "excluded", "primers": distinct,
            "consistent": consistent, "rank": rank,
            "solved": False, "claimed_plaintext": None}


def chain_cnf(m: int, a: int, b: int, rec_sign: int = 1, apply_sign: int = 1,
              ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    """Exact CNF: stream one-hot per position, chain by implication.

    Variables: R[i][v] for i < MAX_POSITION and v in 0..25; t[c][v] for each
    crib ciphertext letter c. The chain adds two stream letters per position;
    each crib equation is guarded on R[i] alone.
    """
    f = _Cnf()
    r = [[f.var() for _ in range(26)] for _ in range(MAX_POSITION)]
    for i in range(MAX_POSITION):
        f.exactly_one(r[i])
    for i in range(m, MAX_POSITION):
        for u in range(26):
            for v in range(26):
                # R[i] = R[i-a] + rec_sign * R[i-b]: the sign applies to the b term only
                q = (u + rec_sign * v) % 26
                left, right = r[i - a][u], r[i - b][v]
                f.clauses.append([-left, -right, r[i][q]])
                for other in range(26):
                    if other != q:
                        f.clauses.append([-left, -right, -r[i][other]])
    pairs = crib_pairs(ciphertext, spans)
    letters = sorted({c for _, c, _ in pairs})
    t = {c: [f.var() for _ in range(26)] for c in letters}
    for c in letters:
        f.exactly_one(t[c])
    for position, cipher_letter, plain_letter in pairs:
        base = ALPHABET_INDEX[plain_letter]
        for u in range(26):
            target = (base + apply_sign * u) % 26
            f.clauses.append([-r[position][u], t[cipher_letter][target]])
            for other in range(26):
                if other != target:
                    f.clauses.append([-r[position][u], -t[cipher_letter][other]])
    return {"f": f, "r": r, "t": t}


def check(m: int, a: int = None, b: int = None, rec_sign: int = 1, apply_sign: int = 1,
          ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> str:
    """'sat' or 'unsat' for one chain shape on the given ciphertext."""
    if a is None:
        a, b = m, m - 1
    cnf = chain_cnf(m, a, b, rec_sign, apply_sign, ciphertext, spans)
    with Solver(name="cadical153", bootstrap_with=cnf["f"].clauses) as solver:
        return "sat" if solver.solve() else "unsat"


def planted(m: int, seed: int, a: int = None, b: int = None, rec_sign: int = 1,
            apply_sign: int = 1, spans=CRIB_SPANS) -> dict:
    """A ciphertext of this model with both clues planted; returns it and the key."""
    a = m if a is None else a
    b = m - 1 if b is None else b
    rng = random.Random(seed)
    primer = [rng.randrange(26) for _ in range(m)]
    rows = coefficients(m, a, b, rec_sign, MAX_POSITION)
    stream = [sum(rows[i][t] * primer[t] for t in range(m)) % 26 for i in range(MAX_POSITION)]
    alphabet = list(LET)
    rng.shuffle(alphabet)
    plain = [rng.choice(LET) for _ in range(97)]
    for start, word in spans:
        plain[start:start + len(word)] = list(word)
    cipher = []
    for i, ch in enumerate(plain[:MAX_POSITION]):
        shift = apply_sign * stream[i]
        cipher.append(alphabet[(ALPHABET_INDEX[ch] + shift) % 26])
    cipher += plain[MAX_POSITION:]
    return {"ciphertext": "".join(cipher), "primer": primer, "alphabet": alphabet,
            "solved": False, "claimed_plaintext": None}


def stream_from_primer(m: int, a: int, b: int, rec_sign: int, primer: list[int]) -> list[int]:
    rows = coefficients(m, a, b, rec_sign, MAX_POSITION)
    return [sum(rows[i][t] * primer[t] for t in range(m)) % 26 for i in range(MAX_POSITION)]
