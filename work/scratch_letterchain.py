"""Scratch 3: lagged-Fibonacci letter keys (mod 26) in place on K4. Not for the repo.

Model: one cipher alphabet; each plaintext index i is enciphered at alphabet
position (plain index + R[i]) mod 26, where the key stream R satisfies a linear
recurrence over Z26 with an m-letter primer: R[i] = s*(R[i-a] + s2*R[i-b]) ... 
kept to R[i] = (R[i-a] +/- R[i-b]) mod 26 with a, b <= m, primer R[0..m-1].
Every R[i] is then a known linear combination of primer letters, so the
same-crib-letter equations idx(p_i) + R[i] == idx(p_j) + R[j] (mod 26) become
linear congruences in the primer. Solve over Z26, enumerate the affine
solution space, and for each primer check the per-letter alphabet placement.
"""
import itertools
import sys
from fractions import Fraction

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.solvers.k4_attempt import K4_CIPHERTEXT

LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
IDX = {ch: i for i, ch in enumerate(LET)}
N = 97


def coefficients(m, a, b, sign, length):
    """Rows: coefficient vectors in (Z26)^m for R[i], i < length."""
    rows = []
    for i in range(length):
        if i < m:
            vec = [0] * m
            vec[i] = 1
            rows.append(vec)
        else:
            u = list(rows[i - a])
            v = rows[i - b]
            for t in range(m):
                u[t] = (u[t] + sign * v[t]) % 26
            rows.append(u)
    return rows


def spike(matrix, col, n_rows, mod):
    """Gaussian elimination mod arbitrary modulus (26 here). Keep pivots odd units via unit search."""
    # 26 = 2 * 13. Units are odd numbers not divisible by 13: 1,3,5,7,9,11,15,17,19,21,23,25.
    pivots = []
    r0 = 0
    for c in range(n_rows and len(matrix[0]) or 0):
        pass
    return pivots


def solve_affine(rows, rhs, m, mod=26):
    """All solutions of rows . x == rhs over Z_mod, m unknowns.

    Returns (basis_count, solutions_iter) -- we enumerate exhaustively when
    the free-variable count is small; otherwise returns None to signal 'too many'.
    """
    # build augmented matrix and row-reduce with unit pivots
    A = [list(r) + [rhs[i] % mod] for i, r in enumerate(rows)]
    n = len(A)
    width = m
    pivot_cols = []
    r = 0
    for c in range(width):
        # find a unit coefficient in this column at or below row r
        pr = None
        for i in range(r, n):
            if A[i][c] % mod != 0 and _is_unit(A[i][c], mod):
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = _inverse(A[r][c], mod)
        A[r] = [(x * inv) % mod for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] % mod != 0:
                f = A[i][c]
                A[i] = [(A[i][t] - f * A[r][t]) % mod for t in range(width + 1)]
        pivot_cols.append(c)
        r += 1
        if r == n:
            break
    # consistency
    for i in range(r, n):
        if all(x % mod == 0 for x in A[i][:width]) and A[i][width] % mod != 0:
            return 0, None
    free = [c for c in range(width) if c not in pivot_cols]
    count = mod ** len(free)
    if count > 200_000:
        return count, None

    def solutions():
        for assign in itertools.product(range(mod), repeat=len(free)):
            x = [0] * width
            for pc, row in zip(pivot_cols, A[: r]):
                x[pc] = row[width] % mod
            f = dict(zip(free, assign))
            for c in free:
                x[c] = f[c]
            ok = True
            for row in A:
                s = sum(row[t] * x[t] for t in range(width)) % mod
                if s != row[width] % mod:
                    ok = False
                    break
            if ok:
                yield x
    return count, solutions()


UNITS = [u for u in range(1, 26) if u % 2 != 0 and u % 13 != 0]


def _is_unit(x, mod):
    x %= mod
    return x in UNITS


def _inverse(x, mod=26):
    x %= mod
    for y in range(mod):
        if (x * y) % mod == 1:
            return y
    raise ValueError(f"{x} not a unit mod {mod}")


def crib_pairs_of():
    out = []
    for start, word in CRIB_SPANS:
        for o, ch in enumerate(word):
            out.append((start + o, K4_CIPHERTEXT[start + o], ch))
    return out


def probe(m, a, b, sign, pairs, planted_plain=None):
    """Return 'fits' / 'excluded' / counts for one recurrence and primer length."""
    need = max(p for p, _, _ in pairs) + 1
    rows_c = coefficients(m, a, b, sign, need)
    eqs = []
    rhs = []
    # same-crib-letter equations
    by_letter = {}
    for p, c, pl in pairs:
        by_letter.setdefault(c, []).append((p, pl))
    for c, uses in sorted(by_letter.items()):
        (p1, pl1), (p2, pl2) = uses[0], uses[-1]
        for (pi, pli), (pj, plj) in itertools.combinations(uses, 2):
            if pi == pj:
                # same position? cannot happen across distinct uses here
                continue
            row = [(rows_c[pi][t] - rows_c[pj][t]) % 26 for t in range(m)]
            eqs.append(row)
            rhs.append((IDX[plj] - IDX[pli]) % 26)
    count, sols = solve_affine(eqs, rhs, m)
    if count == 0:
        return {"m": m, "a": a, "b": b, "sign": sign, "answer": "excluded", "primers": 0}
    if sols is None:
        return {"m": m, "a": a, "b": b, "sign": sign, "answer": "too-many", "primers": count}
    survivors = 0
    for primer in sols:
        # full stream, t per letter, consistency and distinctness
        stream = []
        for i in range(need):
            stream.append(sum(rows_c[i][t] * primer[t] for t in range(m)) % 26)
        t_of = {}
        ok = True
        for p, c, pl in pairs:
            t = (IDX[pl] + stream[p]) % 26
            if c in t_of:
                if t_of[c] != t:
                    ok = False
                    break
            else:
                t_of[c] = t
        if not ok or len(set(t_of.values())) != len(t_of):
            continue
        survivors += 1
    return {"m": m, "a": a, "b": b, "sign": sign,
            "answer": "fits" if survivors else "excluded", "primers": survivors}


def planted_plain_of(rng):
    plain = [rng.choice(LET) for _ in range(N)]
    for start, word in CRIB_SPANS:
        plain[start:start + len(word)] = list(word)
    return "".join(plain)


def planted_probe(m, a, b, sign, seed):
    """Control: a random primer must always fit."""
    from engine.solvers.gromark import gromark_encrypt  # stream shape differs; encrypt manually
    rng = __import__("random").Random(seed)
    primer = [rng.randrange(26) for _ in range(m)]
    rows_c = coefficients(m, a, b, sign, N)
    stream = []
    for i in range(N):
        stream.append(sum(rows_c[i][t] * primer[t] for t in range(m)) % 26)
    # encrypt: one alphabet = identity here (t_c = plain index); letters planted
    pt = planted_plain_of(rng)
    ct = []
    for i, ch in enumerate(pt):
        ct.append(LET[(IDX[ch] + stream[i]) % 26])
    cipher = "".join(ct)
    pairs = []
    for start, word in CRIB_SPANS:
        for o, ch in enumerate(word):
            pairs.append((start + o, cipher[start + o], ch))
    # run the same probe but with the identity alphabet
    need = N
    eqs, rhs = [], []
    by_letter = {}
    for p, c, pl in pairs:
        by_letter.setdefault(c, []).append((p, pl))
    for c, uses in sorted(by_letter.items()):
        for (pi, pli), (pj, plj) in itertools.combinations(uses, 2):
            row = [(rows_c[pi][t] - rows_c[pj][t]) % 26 for t in range(m)]
            eqs.append(row)
            rhs.append((IDX[plj] - IDX[pli]) % 26)
    count, sols = solve_affine(eqs, rhs, m)
    if count == 0:
        return {"seed": seed, "m": m, "answer": "BLOCKED (bug)"}
    if sols is None:
        return {"seed": seed, "m": m, "answer": "too-many(control-expected)", "primers": count}
    survivors = 0
    for cand in sols:
        stream2 = [sum(rows_c[i][t] * cand[t] for t in range(m)) % 26 for i in range(need)]
        t_of = {}
        ok = True
        for p, c, pl in pairs:
            t = (IDX[pl] + stream2[p]) % 26
            if c in t_of and t_of[c] != t or c not in t_of and t in t_of.values():
                ok = False
                break
            t_of[c] = t
        if ok:
            survivors += 1
    return {"seed": seed, "m": m, "answer": "fits" if survivors else "excluded(bug)", "primers": survivors}


if __name__ == "__main__":
    pairs = crib_pairs_of()
    print("crib letters distinct:", len({c for _, c, _ in pairs}))
    print("canonical lag (m, m-1), add and subtract:")
    for sign, tag in ((1, "add"), (-1, "subtract")):
        for m in range(2, 41):
            r = probe(m, m, m - 1, sign, pairs)
            if r["answer"] in ("excluded", "fits") or m < 30:
                print(f"  {tag} m={m:2d}: {r['answer']}  primers={r['primers']}")
            if r["answer"] == "fits":
                break
    print("generic lag pairs, add, m up to 8:")
    for m in range(2, 9):
        for a, b in itertools.combinations(range(1, m + 1), 2):
            r = probe(m, a, b, 1, pairs)
            if r["answer"] == "fits":
                print(f"  m={m} lag=({a},{b}): {r}")
        worst = min((probe(m, a, b, 1, pairs)["primers"], a, b)
                    for a, b in itertools.combinations(range(1, m + 1), 2))
        print(f"  m={m}: max survivors {worst[0] if isinstance(worst[0], int) else '?'} ...")
