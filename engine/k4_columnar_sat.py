"""K4 columnar transposition with substitution as SAT, for wide columns.

The branch and bound in `engine.k4_columnar_bnb` counts surviving column
orders but slows down past width 14 when the key is long. Here the same
question, whether any column order fits, goes to a SAT solver (CaDiCaL via
PySAT), which does not list orders at all.

Variables: X[c][d] says column c is read in slot d (a permutation); S[d][s]
says slot d starts at text position s, which follows from the long or short
type of the slots before it; K[col][k] is the key shift of key column col.
Each clue letter then becomes clauses "X and S imply this key shift". The
model, conventions and variants are those of `engine.k4_transposition_sub`:
direction 0 writes rows and reads columns, direction 1 is the inverse;
comp 0 transposes then substitutes, comp 1 substitutes then transposes;
variants 0 to 3 are Vigenere or Beaufort on A-Z or the KRYPTOS alphabet.

A satisfying assignment is decoded into a column order and checked against
the plain-Python reference before it is reported. Only clue letters are
used, so an unsatisfiable setting is excluded whatever language K4 is in.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

from engine.k4_transposition_sub import QUESTION, _ranks, columnar_perm, setup, strong_key


def _pysat():
    try:
        from pysat.card import CardEnc, EncType
        from pysat.solvers import Solver
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("k4_columnar_sat needs the optional python-sat package") from exc
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


def _encode(s: dict, w: int, direction: int, comp: int, p: int, variant: int):
    n, ct, cpos, cpl = s["n"], s["ct"], s["cpos"], s["cpl"]
    rows, full = -(-n // w), n % w
    nlong = w if full == 0 else full
    length = [rows if c < nlong else rows - 1 for c in range(w)]
    rank = _ranks()[variant >> 1]
    f = _Cnf()
    X = [[f.var() for _ in range(w)] for _ in range(w)]
    for c in range(w):
        f.exactly_one(X[c])
    for d in range(w):
        f.exactly_one([X[c][d] for c in range(w)])
    # Slot d is long when a long column sits in it.
    long_slot = [f.var() for _ in range(w)]
    for d in range(w):
        for c in range(w):
            f.clauses.append([-X[c][d], long_slot[d] if c < nlong else -long_slot[d]])
    # S[d][s]: slot d starts at s.
    S = [dict() for _ in range(w + 1)]
    S[0][0] = f.var()
    f.clauses.append([S[0][0]])
    for d in range(w):
        for start, lit in S[d].items():
            for is_long, step in ((True, rows), (False, rows - 1)):
                nxt = start + step
                if nxt > n:
                    continue
                if nxt not in S[d + 1]:
                    S[d + 1][nxt] = f.var()
                f.clauses.append([-lit, -long_slot[d] if is_long else long_slot[d], S[d + 1][nxt]])
        f.exactly_one(S[d + 1].values())
    K = [[f.var() for _ in range(26)] for _ in range(p)]
    for row in K:
        f.exactly_one(row)

    def require(guard, t, j, pl):
        cl = ct[t]
        if cl == QUESTION:
            f.clauses.append([-g for g in guard])
            return
        col = (t if comp == 0 else j) % p
        shift = (rank[cl] + rank[pl]) % 26 if variant & 1 else (rank[cl] - rank[pl]) % 26
        f.clauses.append([-g for g in guard] + [K[col][shift]])

    for j, pl in zip(cpos, cpl):
        if direction == 0:
            c, r = j % w, j // w
            for d in range(w):
                for start, lit in S[d].items():
                    if start + r < n:
                        require((X[c][d], lit), start + r, j, pl)
        else:
            for d in range(w):
                for start, lit in S[d].items():
                    if not start <= j < start + rows:
                        continue
                    for c in range(w):
                        # Past a short column's end, j sits in the next slot instead.
                        if j < start + length[c]:
                            require((X[c][d], lit), (j - start) * w + c, j, pl)
    return f, X


def solve(s: dict, w: int, direction: int, comp: int, p: int, variant: int, limit: int = 0) -> dict:
    """Whether any column order fits; with limit > 0, up to limit verified orders."""
    *_, Solver = _pysat()
    f, X = _encode(s, w, direction, comp, p, variant)
    orders = []
    with Solver(name="cadical153", bootstrap_with=f.clauses) as solver:
        found = solver.solve()
        while found and len(orders) < max(limit, 1):
            model = set(lit for lit in solver.get_model() if lit > 0)
            order = [next(c for c in range(w) if X[c][d] in model) for d in range(w)]
            perm = columnar_perm(s["n"], order, direction)
            if strong_key(perm, s, comp, p, variant) is None:
                raise AssertionError("SAT model does not satisfy the reference check")
            orders.append(order)
            if limit <= 0:
                break
            solver.add_clause([-X[c][d] for d, c in enumerate(order)])
            found = solver.solve()
    return {"sat": bool(orders), "orders": orders}


def _job(args):
    n, w, direction, comp, p, variant = args
    r = solve(setup(n), w, direction, comp, p, variant)
    return {"n": n, "w": w, "dir": direction, "comp": comp, "p": p, "variant": variant,
            "sat": r["sat"], "order": r["orders"][0] if r["orders"] else None}


def scan(widths, periods=range(1, 21), variants=(0, 1, 2, 3), lengths=(97, 98), workers: int = 1) -> dict:
    jobs = [(n, w, d, comp, p, v) for n in lengths for w in widths for d in (0, 1)
            for comp in (0, 1) for p in periods for v in variants]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            rows = list(pool.map(_job, jobs, chunksize=2))
    else:
        rows = [_job(job) for job in jobs]
    return {"model": "columnar transposition with substitution as SAT, clues only",
            "rows": rows, "solved": False, "claimed_plaintext": None}


if __name__ == "__main__":
    import json
    import sys

    low, high = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    top = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    print(json.dumps(scan(range(low, high + 1), periods=range(1, top + 1), workers=workers)))
