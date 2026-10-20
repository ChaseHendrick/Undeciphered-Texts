"""Scratch 2: unknown-keyword Periodic Gromark in place on K4 as SAT. Not for the repo.

Model per engine.solvers.periodic_gromark with the head left free:
  cipher[i] = alphabet[(ord(plain[i])-65 + starts[(i//k)%k] + R[i]) % 26]
  alphabet = K2M built from head; starts = alphabet positions of head letters;
  R = chain-added rank digits, R[i] = (R[i-k] + R[i-k+1]) % 10 for i >= k.
Relaxed space (a superset of every real keyword):
  s_g distinct values 0..25, rho a permutation of 1..k, t_c free per crib cipher letter
  (in a real keyword the s_g, rho and alphabet are coupled through the same head).
"""
import itertools
import random
import sys

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.solvers.k4_attempt import K4_CIPHERTEXT
from engine.solvers.periodic_gromark import (
    periodic_gromark_alphabet,
    periodic_gromark_encrypt,
    periodic_gromark_running_key,
)
from engine.solvers.gromark import gromark_keyword

LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
IDX = {ch: i for i, ch in enumerate(LET)}


class Cnf:
    def __init__(self):
        self.top = 0
        self.cls = []

    def var(self):
        self.top += 1
        return self.top

    def exactly_one(self, lits):
        enc = CardEnc.equals(lits=list(lits), bound=1, top_id=self.top,
                             encoding=EncType.seqcounter)
        self.top = max(self.top, enc.nv)
        self.cls.extend(enc.clauses)


def spec_of(ciphertext, spans):
    return [(start + o, ciphertext[start + o], ch)
            for start, word in spans
            for o, ch in enumerate(word)]


def build(k, ciphertext, spec, fits=(0, 1)):
    """CNF over the relaxed space. fits: clue indexes whose letters are constrained."""
    f = Cnf()
    s_g = [[f.var() for _ in range(26)] for _ in range(k)]
    for g in range(k):
        f.exactly_one(s_g[g])
    for g, h in itertools.combinations(range(k), 2):
        for v in range(26):
            f.cls.append([-s_g[g][v], -s_g[h][v]])
    rho = [[f.var() for _ in range(1, k + 1)] for _ in range(k)]
    for g in range(k):
        f.exactly_one(rho[g])
    for j in range(1, k + 1):
        f.exactly_one([rho[g][j - 1] for g in range(k)])
    n = len(ciphertext)
    r = []
    for i in range(n):
        vals = [f.var() for _ in range(10)]
        f.exactly_one(vals)
        if i < k:
            # primer digit = rank 1..k of the head letter at position i
            f.cls.append([-vals[0]])
            for j in range(k + 1, 10):
                f.cls.append([-vals[j]])
            for j in range(1, k + 1):
                f.cls.append([-rho[i][j - 1], vals[j]])
                f.cls.append([rho[i][j - 1], -vals[j]])
        else:
            for a in range(10):
                for b in range(10):
                    q = (a + b) % 10
                    for d in range(10):
                        if d == q:
                            f.cls.append([-r[i - k][a], -r[i - k + 1][b], vals[d]])
                        else:
                            f.cls.append([-r[i - k][a], -r[i - k + 1][b], -vals[d]])
        r.append(vals)
    letters = sorted({c for _, c, _ in spec})
    t = {ch: [f.var() for _ in range(26)] for ch in letters}
    for ch in letters:
        f.exactly_one(t[ch])

    fitted, reserved = {}, {}
    for which in (0, 1):
        start, word = CRIB_SPANS2[which] if False else spans[which]
        d = fitted if which in fits else reserved
        for o, ch in enumerate(word):
            d[start + o] = ch

    def add_eq(guard, pos, pch, force=True):
        grp = (pos // k) % k
        base = IDX[pch]
        for s in range(26):
            for d in range(10):
                v = (base + s + d) % 26
                if force:
                    f.cls.append([-guard, -s_g[grp][s], -r[pos][d], t[ciphertext[pos]][v]])
                else:
                    f.cls.append([-guard, -s_g[grp][s], -r[pos][d], -t[ciphertext[pos]][v]])

    t_on, t_off = {}, {}
    pos_seen = sorted({p for p, _, _ in spec})
    for pos in pos_seen:
        t_on[pos] = f.var()
        t_off[pos] = f.var()
        if pos in fitted:
            add_eq(t_on[pos], pos, fitted[pos], force=True)
            f.cls.append([t_on[pos]])
            f.cls.append([-t_off[pos]])
    return f, s_g, r, t, t_on, t_off, fitted, reserved, pos_seen


def fold(k, ciphertext, spec, fits=(0, 1), probes=True):
    """Whether the fitted clues hold; count forced right/wrong/free reserved letters."""
    f, s_g, r, t, t_on, t_off, fitted, reserved, pos_seen = build(k, ciphertext, spec, fits)
    out = {"k": k, "fit": "unknown", "right": 0, "wrong": 0, "free": 0}
    with Solver(name="cadical153", bootstrap_with=f.cls) as s:
        if not s.solve():
            out["fit"] = "unsat"
            return out
        out["fit"] = "sat"
        if not probes:
            return out
        for pos in reserved:
            pch = reserved[pos]
            cch = ciphertext[pos]
            grp = (pos // k) % k
            base = IDX[pch]
            for s0 in range(26):
                for d0 in range(10):
                    v = (base + s0 + d0) % 26
                    s.add_clause([-t_on[pos], -s_g[grp][s0], -r[pos][d0], t[cch][v]])
                    s.add_clause([-t_off[pos], -s_g[grp][s0], -r[pos][d0], -t[cch][v]])
            can_be = s.solve(assumptions=[t_on[pos]])
            can_differ = s.solve(assumptions=[t_off[pos]])
            if can_be and not can_differ:
                out["right"] += 1
            elif can_differ and not can_be:
                out["wrong"] += 1
            else:
                out["free"] += 1
    return out


spans = CRIB_SPANS
CRIB_SPANS2 = None


def planted(klen, rng):
    """A planted ciphertext of this head length with both clues at the public offsets."""
    head = "".join(rng.sample(LET, klen))
    plain = [rng.choice(LET) for _ in range(97)]
    plain[spans[0][0]:spans[0][0] + len(spans[0][1])] = list(spans[0][1])
    plain[spans[1][0]:spans[1][0] + len(spans[1][1])] = list(spans[1][1])
    pt = "".join(plain)
    ct = periodic_gromark_encrypt(pt, keyword=head)
    A = periodic_gromark_alphabet(gromark_keyword(head))
    return ct, A, head


def cross_check(k=3, seed=5):
    """SAT answer versus exhaustive search over the relaxed space (small k only)."""
    rng = random.Random(seed)
    ct, A, head = planted(k, rng)
    spec = spec_of(ct, spans)
    # true config check via the model equations, and SAT agreement
    res = fold(k, ct, spec)
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "k4"
    if mode == "k4":
        ct = K4_CIPHERTEXT
        spec = spec_of(ct, spans)
        for k in range(2, 10):
            res = fold(k, ct, spec, fits=(0, 1), probes=False)
            print(f"K4 k={k} both-clues: {res['fit']}")
    elif mode == "planted":
        rng = random.Random(11)
        bad = 0
        for trial in range(16):
            klen = 2 + trial % 8
            ct, A, head = planted(klen, rng)
            spec = spec_of(ct, spans)
            res = fold(klen, ct, spec, fits=(0, 1), probes=False)
            st = res["fit"]
            if st != "sat":
                bad += 1
                print(f"BAD k={klen} head={head}: {st}")
        print("planted sat:", 16 - bad, "blocked:", bad)
    elif mode == "folds":
        ct = K4_CIPHERTEXT
        spec = spec_of(ct, spans)
        for k in range(2, 10):
            a = fold(k, ct, spec, fits=(0,))
            b = fold(k, ct, spec, fits=(1,))
            print(f"K4 k={k} fit-E: {a}  fit-B: {b}")
