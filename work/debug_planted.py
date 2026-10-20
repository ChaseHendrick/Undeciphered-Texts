"""Debug 2: build stages. Not for the repo."""
import itertools
import random

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from engine.k4_gromark_obstruction import CRIB_SPANS, crib_pairs
from engine.solvers.k4_attempt import K4_CIPHERTEXT
from engine.solvers.periodic_gromark import (
    periodic_gromark_alphabet,
    periodic_gromark_encrypt,
    periodic_gromark_primer,
    periodic_gromark_running_key,
)
from engine.solvers.gromark import gromark_keyword

CT = K4_CIPHERTEXT
N = len(CT)
PAIRS = crib_pairs(CT)
SPEC = [(p, c, pl) for p, c, pl in PAIRS]
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
        assert max(abs(x) for x in lits) <= self.top, (max(abs(x) for x in lits), self.top)
        enc = CardEnc.equals(lits=list(lits), bound=1, top_id=self.top,
                             encoding=EncType.seqcounter)
        assert enc.nv >= max(abs(x) for x in lits), (enc.nv, lits)
        self.top = max(self.top, enc.nv)
        self.cls.extend(enc.clauses)


def build(k, fits=(0, 1), stages=None):
    """Stages: S_distinct, rho_perm, chain, t, eq."""
    st = stages or {"S_distinct": True, "rho_perm": True, "chain": True, "t": True, "eq": True}
    f = Cnf()
    S = [[f.var() for _ in range(26)] for _ in range(k)]
    for g in range(k):
        f.exactly_one(S[g])
    if st["S_distinct"]:
        for g, h in itertools.combinations(range(k), 2):
            for v in range(26):
                f.cls.append([-S[g][v], -S[h][v]])
    rho = [[f.var() for _ in range(1, k + 1)] for _ in range(k)]
    for g in range(k):
        f.exactly_one(rho[g])
    if st["rho_perm"]:
        for j in range(1, k + 1):
            f.exactly_one([rho[g][j - 1] for g in range(k)])
    r = []
    for i in range(N):
        vals = [f.var() for _ in range(10)]
        f.exactly_one(vals)
        if i < k:
            f.cls.append([-vals[0]])
            for j in range(k + 1, 10):
                f.cls.append([-vals[j]])
            for j in range(1, k + 1):
                f.cls.append([-rho[i][j - 1], vals[j]])
                f.cls.append([rho[i][j - 1], -vals[j]])
        elif st["chain"]:
            for a in range(10):
                for b in range(10):
                    s = (a + b) % 10
                    for d in range(10):
                        if d == s:
                            f.cls.append([-r[i - k][a], -r[i - k + 1][b], vals[d]])
                        else:
                            f.cls.append([-r[i - k][a], -r[i - k + 1][b], -vals[d]])
        r.append(vals)
    letters = sorted({c for _, c, _ in SPEC})
    t = {ch: [f.var() for _ in range(26)] for ch in letters}
    for ch in letters:
        f.exactly_one(t[ch])

    fitted = {}
    reserved = {}
    for which in (0, 1):
        start, word = CRIB_SPANS[which]
        d = fitted if which in fits else reserved
        for o, ch in enumerate(word):
            d[start + o] = ch

    def add_eq(guard, pos, pch, force=True):
        g = (pos // k) % k
        base = IDX[pch]
        for s in range(26):
            for d in range(10):
                v = (base + s + d) % 26
                if st["eq"] is False:
                    return
                if force:
                    f.cls.append([-guard, -S[g][s], -r[pos][d], t[cch][v]])
                else:
                    f.cls.append([-guard, -S[g][s], -r[pos][d], -t[cch][v]])

    t_on, t_off = {}, {}
    for pos in sorted({p for p, _, _ in SPEC}):
        cch = CT[pos]
        t_on[pos] = f.var()
        t_off[pos] = f.var()
        if pos in fitted:
            add_eq(t_on[pos], pos, fitted[pos], force=True)
            f.cls.append([t_on[pos]])
            f.cls.append([-t_off[pos]])
    return f, S, r, t, t_on, t_off, fitted, reserved


if __name__ == "__main__":
    rng = random.Random(7)
    klen = 3
    head = "".join(rng.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", klen))
    plain = [rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(97)]
    plain[21:34] = list("EASTNORTHEAST")
    plain[63:74] = list("BERLINCLOCK")
    pt = "".join(plain)
    ct = periodic_gromark_encrypt(pt, keyword=head)
    kwm = gromark_keyword(head)
    A = periodic_gromark_alphabet(kwm)
    S_true = [A.index(ch) for ch in kwm]
    R_true = [int(c) for c in periodic_gromark_running_key(kwm, 97)]
    t_true = {}
    for pos, cch, _pl in SPEC:
        t_true[cch] = A.index(ct[pos])

    combos = [
        ("all", {"S_distinct": True, "rho_perm": True, "chain": True, "t": True, "eq": True}),
        ("no S-distinct", {"S_distinct": False, "rho_perm": True, "chain": True, "t": True, "eq": True}),
        ("no rho-perm", {"S_distinct": True, "rho_perm": False, "chain": True, "t": True, "eq": True}),
        ("no chain", {"S_distinct": True, "rho_perm": True, "chain": False, "t": True, "eq": True}),
        ("no t", {"S_distinct": True, "rho_perm": True, "chain": True, "t": False, "eq": False}),
        ("S-only", {"S_distinct": False, "rho_perm": False, "chain": False, "t": False, "eq": False}),
    ]
    pins = lambda f, S, r, t: (
        [S[g][S_true[g]] for g in range(klen)]
        + [r[i][R_true[i]] for i in range(97)]
        + [t[ch][val] for ch, val in t_true.items()]
    )
    for nm, st in combos:
        f, S, r, t, ton, toff, fitted, reserved = build(klen, fits=(0, 1), stages=st)
        p = pins(f, S, r, t)
        if nm == "S-only":
            p = [S[g][S_true[g]] for g in range(klen)]
        if nm == "no t":
            p = [x for x in p if x < 0 or True]
        if nm == "no t":
            # t vars excluded from pinning: filter by membership
            tvars = {v for ch in t for v in t[ch]}
            p = [x for x in p if x not in tvars] if nm == "no t" and False else p
        with Solver(name="cadical153", bootstrap_with=f.cls) as s:
            ok = s.solve(assumptions=[x for x in p])
        print(f"{nm:14s} -> {'SAT' if ok else 'UNSAT'}  (pins {len(p)}, cls {len(f.cls)})")
