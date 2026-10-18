"""K4 in-place Hill ciphers of size 5 to 10: exact row algebra, and 5 by 5 in full.

A Hill cipher deciphers each block of n letters as p = M c mod 26. Row j
of M must send every ciphertext block whose plaintext is known to that
block's j-th plaintext letter: r . c_b = p_b[j] mod 26. Sizes 2 to 4 are
closed by trying every row (engine.k4_hill_rows). From size 5 up the two
published clues give at most four known blocks, so a row is not pinned and
26^n rows are too many to list. Here each row's linear system is solved
exactly over GF(2) and GF(13) and the two answers are joined by the Chinese
remainder theorem, so the count of rows mod 26 is the count mod 2 times the
count mod 13.

A setting is excluded only when some row has no solution, or when no choice
of fitted rows is invertible mod 26. Over a field an invertible M with
M c_b = p_b for every known block exists exactly when the rows are
consistent and the known cipher blocks and plain blocks have the same rank,
so the second test is exact too. The held-back fold fits one clue and counts
letters of the other clue that every fitted row agrees on.

At 5 by 5 with four known blocks each row has 26 solutions, so there are
26^5 = 11,881,376 clue-consistent row choices. ``enumerate_keys`` lists all
of them, deciphers every full block and ranks the results by the repo's
English quadgram model and by index of coincidence. The quadgram score of a
key splits into five tables over four rows each, so the whole space is
scored without deciphering each key one by one. Planted controls put both
clues into held-out English, encipher with a random invertible key, and
check that the true key ranks first.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import math
import random
import time
from pathlib import Path

import numpy as np

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.k4_hill_rows import LETTERS, NUMBERINGS
from engine.solvers.k4_attempt import K4_CIPHERTEXT

SIZES = (5, 6, 7, 8, 9, 10)
PRIMES = (2, 13)
TOP = 20
POOL = 2000
MAX_KEYS = 52 ** 5
_DATA = Path(__file__).resolve().parent / "data"
# Held-out English: neither file is in the quadgram training file.
HELDOUT_FILES = ("neural_heldout_doyle.txt", "neural_audit_wells.txt")


# ---------------------------------------------------------------- algebra


def _rref(a: np.ndarray, p: int, columns: int) -> tuple[np.ndarray, list[int]]:
    """Row reduce mod p, choosing pivots only among the first ``columns`` columns."""
    a = a.copy() % p
    pivots: list[int] = []
    row = 0
    for col in range(columns):
        if row == a.shape[0]:
            break
        nz = np.nonzero(a[row:, col])[0]
        if not len(nz):
            continue
        swap = row + nz[0]
        a[[row, swap]] = a[[swap, row]]
        a[row] = (a[row] * pow(int(a[row, col]), -1, p)) % p
        for other in range(a.shape[0]):
            if other != row and a[other, col]:
                a[other] = (a[other] - a[other, col] * a[row]) % p
        pivots.append(col)
        row += 1
    return a, pivots


def rank_mod(a: np.ndarray, p: int) -> int:
    if a.size == 0:
        return 0
    return len(_rref(a, p, a.shape[1])[1])


def solve_rows(c: np.ndarray, plain: np.ndarray, p: int) -> dict:
    """Solve r . c_b = plain[b, j] mod p for every row j at once.

    Returns the rank of the block matrix, which rows are consistent, one
    particular solution per row (None if inconsistent) and a null-space basis
    shared by all rows.
    """
    k, n = c.shape
    if k == 0:
        basis = [np.eye(n, dtype=np.int64)[i] for i in range(n)]
        return {"rank": 0, "consistent": [True] * n, "particular": [np.zeros(n, dtype=np.int64)] * n,
                "basis": basis}
    reduced, pivots = _rref(np.hstack([c, plain]).astype(np.int64), p, n)
    rank = len(pivots)
    consistent, particular = [], []
    for j in range(n):
        rhs = reduced[:, n + j]
        ok = not np.any(rhs[rank:] % p)
        consistent.append(bool(ok))
        if ok:
            x = np.zeros(n, dtype=np.int64)
            for i, col in enumerate(pivots):
                x[col] = rhs[i]
            particular.append(x)
        else:
            particular.append(None)
    basis = []
    for free in (col for col in range(n) if col not in pivots):
        v = np.zeros(n, dtype=np.int64)
        v[free] = 1
        for i, col in enumerate(pivots):
            v[col] = (-reduced[i, free]) % p
        basis.append(v)
    return {"rank": rank, "consistent": consistent, "particular": particular, "basis": basis}


def crt(r2, r13):
    """The value mod 26 that is r2 mod 2 and r13 mod 13."""
    return (13 * np.asarray(r2) + 14 * np.asarray(r13)) % 26


def invertible(m: np.ndarray) -> bool:
    return all(rank_mod(np.asarray(m), p) == m.shape[0] for p in PRIMES)


def inverse_mod26(m: np.ndarray) -> np.ndarray:
    n = m.shape[0]
    parts = []
    for p in PRIMES:
        reduced, pivots = _rref(np.hstack([m % p, np.eye(n, dtype=np.int64)]), p, n)
        if len(pivots) < n:
            raise ValueError("matrix is not invertible mod 26")
        parts.append(reduced[:, n:])
    return crt(parts[0], parts[1]).astype(np.int64)


# ---------------------------------------------------------------- blocks


def known_blocks(n: int, alignment: int, spans, ciphertext: str, alphabet: str):
    """(block start, cipher vector, plain vector) for blocks wholly inside a clue."""
    blocks = []
    for start, word in spans:
        end = start + len(word)
        first = start + ((alignment - start) % n)
        for b in range(first, end - n + 1, n):
            c = [alphabet.index(ch) for ch in ciphertext[b : b + n]]
            p = [alphabet.index(word[b - start + k]) for k in range(n)]
            blocks.append((b, np.array(c, dtype=np.int64), np.array(p, dtype=np.int64)))
    return blocks


def _matrices(blocks, n):
    if not blocks:
        return np.zeros((0, n), dtype=np.int64), np.zeros((0, n), dtype=np.int64)
    return np.array([c for _b, c, _p in blocks]), np.array([p for _b, _c, p in blocks])


def row_system(n: int, blocks) -> dict:
    """Per-prime solution of every row, plus the exact invertibility test."""
    c, plain = _matrices(blocks, n)
    out = {}
    for p in PRIMES:
        sol = solve_rows(c, plain, p)
        sol["plain_rank"] = rank_mod(plain, p) if len(blocks) else 0
        out[p] = sol
    consistent = [all(out[p]["consistent"][j] for p in PRIMES) for j in range(n)]
    counts = []
    for j in range(n):
        if not consistent[j]:
            counts.append(0)
        else:
            counts.append(math.prod(p ** (n - out[p]["rank"]) for p in PRIMES))
    invertible_exists = all(consistent) and all(out[p]["rank"] == out[p]["plain_rank"] for p in PRIMES)
    return {"per_prime": out, "consistent": consistent, "row_counts": counts,
            "invertible_exists": invertible_exists}


def check(n: int, alignment: int, numbering: str = "A-Z", ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    alphabet = NUMBERINGS[numbering]
    blocks = known_blocks(n, alignment, spans, ciphertext, alphabet)
    system = row_system(n, blocks)
    excluded = not all(system["consistent"]) or not system["invertible_exists"]
    return {
        "size": n, "alignment": alignment, "numbering": numbering, "blocks": len(blocks),
        "rank_mod2": system["per_prime"][2]["rank"], "rank_mod13": system["per_prime"][13]["rank"],
        "plain_rank_mod2": system["per_prime"][2]["plain_rank"],
        "plain_rank_mod13": system["per_prime"][13]["plain_rank"],
        "consistent": all(system["consistent"]), "row_counts": system["row_counts"],
        "free_per_row": n - len(blocks) if blocks else n,
        "invertible_exists": system["invertible_exists"],
        "status": "excluded" if excluded else "open",
    }


def held_back(n: int, alignment: int, numbering: str = "A-Z", ciphertext: str = K4_CIPHERTEXT,
              fit=CRIB_SPANS[0], reserve=CRIB_SPANS[1]) -> dict:
    """Fit rows on one clue; a reserved letter is forced when every fitted row agrees on it."""
    alphabet = NUMBERINGS[numbering]
    system = row_system(n, known_blocks(n, alignment, (fit,), ciphertext, alphabet))
    right = wrong = 0
    start, word = reserve
    for i in range(start, start + len(word)):
        block = i - ((i - alignment) % n)
        j = i - block
        if block < 0 or block + n > len(ciphertext) or not system["consistent"][j]:
            continue
        c = np.array([alphabet.index(ch) for ch in ciphertext[block : block + n]], dtype=np.int64)
        values = []
        for p in PRIMES:
            sol = system["per_prime"][p]
            if any(int(v @ c) % p for v in sol["basis"]):
                break
            values.append(int(sol["particular"][j] @ c) % p)
        if len(values) < 2:
            continue
        if alphabet[int(crt(values[0], values[1]))] == word[i - start]:
            right += 1
        else:
            wrong += 1
    return {"fit_blocks": len(known_blocks(n, alignment, (fit,), ciphertext, alphabet)),
            "fit_rows": system["row_counts"], "right": right, "wrong": wrong,
            "free": len(word) - right - wrong}


def scan(ciphertext: str = K4_CIPHERTEXT, sizes=SIZES) -> dict:
    rows = []
    for numbering in NUMBERINGS:
        for n in sizes:
            for alignment in range(n):
                result = check(n, alignment, numbering, ciphertext)
                result["fold_east"] = held_back(n, alignment, numbering, ciphertext, CRIB_SPANS[0], CRIB_SPANS[1])
                result["fold_berlin"] = held_back(n, alignment, numbering, ciphertext, CRIB_SPANS[1], CRIB_SPANS[0])
                total = math.prod(result["row_counts"])
                result["row_choices"] = total
                rows.append(result)
    return {
        "model": "in-place Hill, sizes 5 to 10, every alignment, four letter numberings, clues only",
        "rows": rows,
        "solved": False,
        "claimed_plaintext": None,
    }


# ---------------------------------------------------------------- planting


def random_key(n: int, rng: random.Random) -> np.ndarray:
    while True:
        m = np.array([[rng.randrange(26) for _ in range(n)] for _ in range(n)], dtype=np.int64)
        if invertible(m):
            return m


def encipher(plain: str, key: np.ndarray, alignment: int, numbering: str = "A-Z") -> str:
    """Encipher full blocks so that p = key c mod 26; leftover letters stay as they are."""
    n = key.shape[0]
    alphabet = NUMBERINGS[numbering]
    inverse = inverse_mod26(key)
    out = list(plain)
    for b in range(alignment, len(plain) - n + 1, n):
        p = np.array([alphabet.index(ch) for ch in plain[b : b + n]], dtype=np.int64)
        out[b : b + n] = [alphabet[v] for v in (inverse @ p) % 26]
    return "".join(out)


def plant_clues(text: str, spans=CRIB_SPANS) -> str:
    letters = list(text)
    for start, word in spans:
        letters[start : start + len(word)] = word
    return "".join(letters)


def planted(n: int, alignment: int, seed: int, numbering: str = "A-Z", plain: str | None = None,
            spans=CRIB_SPANS) -> tuple[str, np.ndarray]:
    """Both clues planted (in random letters unless ``plain`` is given) under a random invertible key."""
    rng = random.Random(seed)
    if plain is None:
        plain = "".join(rng.choice(LETTERS) for _ in range(97))
    key = random_key(n, rng)
    return encipher(plant_clues(plain, spans), key, alignment, numbering), key


def english_windows(length: int = 97, files=HELDOUT_FILES) -> list[str]:
    """Non-overlapping windows of held-out English (not in the quadgram training file)."""
    windows = []
    for name in files:
        lines = (_DATA / name).read_text(encoding="utf-8").splitlines()
        body = " ".join(line for line in lines if not line.startswith("#"))
        text = "".join(ch for ch in body.upper() if ch in LETTERS)
        windows += [text[i : i + length] for i in range(0, len(text) - length + 1, length)]
    return windows


# ---------------------------------------------------------------- 5 by 5 enumeration


def row_solutions(system: dict, j: int) -> np.ndarray:
    """Every row j vector mod 26 that satisfies the known blocks."""
    parts = []
    for p in PRIMES:
        sol = system["per_prime"][p]
        x = sol["particular"][j]
        vectors = x[None, :]
        for v in sol["basis"]:
            vectors = (vectors[:, None, :] + np.arange(p)[None, :, None] * v[None, None, :]).reshape(-1, len(x)) % p
        parts.append(vectors)
    a, b = parts
    return crt(np.repeat(a, len(b), axis=0), np.tile(b, (len(a), 1))).astype(np.int64)


def _span(n: int, alignment: int, length: int = 97) -> tuple[int, int]:
    count = (length - alignment) // n
    return alignment, alignment + count * n


def _letter_stats(seq: list[int]) -> tuple[float, float]:
    counts = np.bincount(np.asarray(seq, dtype=np.int64), minlength=26).astype(float)
    total = counts.sum()
    ioc = float((counts * (counts - 1)).sum() / (total * (total - 1)))
    freq = counts[counts > 0] / total
    return ioc, float(-(freq * np.log2(freq)).sum())


def _outside_clues(start: int, end: int, spans=CRIB_SPANS) -> list[int]:
    inside = {i for s, w in spans for i in range(s, s + len(w))}
    return [i for i in range(start, end) if i not in inside]


def score_text(text: str, n: int, alignment: int, model=None) -> dict:
    """Quadgram score of the block span and letter statistics outside the clues."""
    if model is None:
        from engine.language import get_model
        model = get_model()
    start, end = _span(n, alignment, len(text))
    seq = [ord(ch) - 65 for ch in text[start:end]]
    total = model.score(seq)
    ioc, entropy = _letter_stats([ord(text[i]) - 65 for i in _outside_clues(start, end)])
    return {"quadgram": total, "per_quadgram": total / (len(seq) - 3), "ioc": ioc, "entropy": entropy}


def enumerate_keys(n: int, alignment: int, numbering: str = "A-Z", ciphertext: str = K4_CIPHERTEXT,
                   spans=CRIB_SPANS, top: int = TOP, true_key: np.ndarray | None = None,
                   max_keys: int = MAX_KEYS, model=None) -> dict:
    """Score every clue-consistent row choice by quadgrams and by index of coincidence.

    The quadgram total over the block span is the sum of n tables, table s
    holding the windows that start at row s. That needs every window to touch
    n - 1 or fewer rows, which holds at n = 5 (windows touch 4 rows).
    """
    if model is None:
        from engine.language import get_model
        model = get_model()
    if n != 5:
        raise ValueError("full enumeration is implemented for 5 by 5 only")
    started = time.time()
    alphabet = NUMBERINGS[numbering]
    to_std = np.array([ord(ch) - 65 for ch in alphabet], dtype=np.int64)
    blocks = known_blocks(n, alignment, spans, ciphertext, alphabet)
    system = row_system(n, blocks)
    report = {"size": n, "alignment": alignment, "numbering": numbering, "blocks": len(blocks),
              "row_counts": system["row_counts"], "solved": False, "claimed_plaintext": None}
    total_keys = math.prod(system["row_counts"])
    report["keys"] = total_keys
    if total_keys == 0 or not system["invertible_exists"]:
        report["status"] = "excluded"
        return report
    if total_keys > max_keys:
        report["status"] = "out of reach"
        return report

    start, end = _span(n, alignment, len(ciphertext))
    nblocks = (end - start) // n
    cipher = np.array([[alphabet.index(ch) for ch in ciphertext[b : b + n]]
                       for b in range(start, end, n)], dtype=np.int64)
    rows = [row_solutions(system, j) for j in range(n)]
    # letters[j][i, k]: standard index of the letter row j candidate i gives in block k.
    letters = [to_std[(r @ cipher.T) % 26] for r in rows]
    sizes = [len(r) for r in rows]

    logp = np.asarray(model.logp, dtype=np.float64)
    tables = []
    for s in range(n):
        shape = [sizes[(s + d) % n] for d in range(4)]
        table = np.zeros(shape, dtype=np.float64)
        for k in range(nblocks):
            idx = 0
            ok = True
            for d in range(4):
                row = (s + d) % n
                block = k + (s + d) // n
                if block >= nblocks:
                    ok = False
                    break
                view = [1, 1, 1, 1]
                view[d] = sizes[row]
                idx = idx * 26 + letters[row][:, block].reshape(view)
            if ok:
                table += logp[idx]
        tables.append(table)

    outside = np.array([i for i in _outside_clues(start, end)], dtype=np.int64)
    count_outside = len(outside)
    hist = []
    for j in range(n):
        ks = [(i - start) // n for i in outside if (i - start) % n == j]
        h = np.zeros((sizes[j], 26), dtype=np.float64)
        for k in ks:
            np.add.at(h, (np.arange(sizes[j]), letters[j][:, k]), 1.0)
        hist.append(h)
    pair = {(j, l): hist[j] @ hist[l].T for j in range(n) for l in range(j + 1, n)}
    single = [(h * h).sum(axis=1) for h in hist]

    def axis_view(j, values, i0):
        """Broadcast a per-row-j vector onto axes (i1, i2, i3, i4)."""
        shape = [1, 1, 1, 1]
        shape[j - 1] = sizes[j]
        return values.reshape(shape)

    def key_values(choice):
        q = sum(float(tables[s][tuple(choice[(s + d) % n] for d in range(4))]) for s in range(n))
        sq = sum(float(single[j][choice[j]]) for j in range(n))
        sq += 2 * sum(float(g[choice[j], choice[l]]) for (j, l), g in pair.items())
        return q, (sq - count_outside) / (count_outside * (count_outside - 1))

    true_index = None
    if true_key is not None:
        true_index = []
        for j in range(n):
            match = np.nonzero(np.all(rows[j] == true_key[j] % 26, axis=1))[0]
            true_index.append(int(match[0]) if len(match) else None)
        if None in true_index:
            true_index = None
    if true_index is not None:
        true_q, true_i = key_values(true_index)
    above_q = above_i = 0
    best_q: list[tuple[float, tuple]] = []
    best_i: list[tuple[float, tuple]] = []
    shape4 = sizes[1:]
    for i0 in range(sizes[0]):
        t0 = tables[0][i0][:, :, :, None]
        t1 = tables[1]
        t2 = tables[2][:, :, :, i0][None, :, :, :]
        t3 = np.transpose(tables[3][:, :, i0, :], (2, 0, 1))[:, None, :, :]
        t4 = np.transpose(tables[4][:, i0, :, :], (1, 2, 0))[:, :, None, :]
        q = t0 + t1 + t2 + t3 + t4
        sq = single[0][i0] + sum(axis_view(j, single[j], i0) for j in range(1, n))
        for (j, l), g in pair.items():
            if j == 0:
                sq = sq + 2 * axis_view(l, g[i0], i0)
            else:
                shape = [1, 1, 1, 1]
                shape[j - 1] = sizes[j]
                shape[l - 1] = sizes[l]
                sq = sq + 2 * g.reshape(shape)
        ioc = (sq - count_outside) / (count_outside * (count_outside - 1))
        flat_q = q.reshape(-1)
        flat_i = np.broadcast_to(ioc, q.shape).reshape(-1)
        if true_index is not None:
            above_q += int((flat_q > true_q + 1e-9).sum())
            above_i += int((flat_i > true_i + 1e-12).sum())
        for flat, best in ((flat_q, best_q), (flat_i, best_i)):
            keep = min(POOL, flat.size)
            part = np.argpartition(-flat, keep - 1)[:keep]
            best.extend((float(flat[pos]), (i0,) + tuple(int(x) for x in np.unravel_index(pos, shape4)))
                        for pos in part)
        best_q.sort(key=lambda item: -item[0])
        best_i.sort(key=lambda item: -item[0])
        del best_q[POOL:], best_i[POOL:]

    def decrypt(choice):
        key = np.array([rows[j][int(choice[j])] for j in range(n)])
        out = list(ciphertext.lower())
        for k, b in enumerate(range(start, end, n)):
            out[b : b + n] = [alphabet[v] for v in (key @ cipher[k]) % 26]
        return "".join(out), key

    def finish(best):
        kept = []
        for value, choice in best:
            text, key = decrypt(choice)
            if not invertible(key):
                continue
            stats = score_text(text.upper(), n, alignment, model)
            kept.append({"key": key.tolist(), "quadgram": stats["quadgram"], "per_quadgram": stats["per_quadgram"],
                         "ioc": stats["ioc"], "entropy": stats["entropy"], "text": text})
            if len(kept) == top:
                break
        return kept

    report["top_quadgram"] = finish(best_q)
    report["top_ioc"] = finish(best_i)
    report["status"] = "enumerated"
    if true_index is not None:
        report["true_quadgram"] = true_q
        report["true_rank_quadgram"] = above_q + 1
        report["true_ioc"] = true_i
        report["true_rank_ioc"] = above_i + 1
        if above_q < POOL:
            higher = [choice for value, choice in best_q if value > true_q + 1e-9]
            report["true_rank_quadgram_invertible"] = 1 + sum(invertible(decrypt(c)[1]) for c in higher)
        report["true_first_invertible"] = bool(report["top_quadgram"]) and \
            report["top_quadgram"][0]["key"] == (true_key % 26).tolist()
    report["seconds"] = round(time.time() - started, 2)
    return report


def english_baseline(n: int, alignment: int, model=None) -> list[dict]:
    """Held-out English windows with both clues planted, scored like a decrypt."""
    return [score_text(plant_clues(w), n, alignment, model) for w in english_windows()]


def planted_control(alignment: int, seed: int, numbering: str = "A-Z", model=None, n: int = 5,
                    english: bool = True) -> dict:
    """Plant both clues in held-out English, encipher with a random key, enumerate, rank the true key.

    With ``english`` false the rest of the plaintext is uniform random letters,
    which measures how well the best of 26^5 keys scores on text with no language.
    """
    windows = english_windows()
    rng = random.Random(seed)
    if english:
        plain = plant_clues(windows[rng.randrange(len(windows))])
    else:
        plain = plant_clues("".join(rng.choice(LETTERS) for _ in range(97)))
    key = random_key(n, rng)
    ciphertext = encipher(plain, key, alignment, numbering)
    report = enumerate_keys(n, alignment, numbering, ciphertext, true_key=key, model=model)
    report["seed"] = seed
    report["true_key"] = key.tolist()
    report.pop("top_ioc", None)
    top = report.get("top_quadgram", [])
    wrong = [c for c in top if c["key"] != report["true_key"]]
    report["best_wrong_quadgram"] = wrong[0]["quadgram"] if wrong else None
    report["best_wrong_per_quadgram"] = wrong[0]["per_quadgram"] if wrong else None
    report["top_quadgram"] = top[:3]
    return report


def run(control_seeds: int = 20, other_seeds: int = 10) -> dict:
    """Every 5 by 5 setting the algebra leaves open, English baseline, and planted controls."""
    from engine.language import get_model

    model = get_model()
    started = time.time()
    k4 = []
    for numbering in NUMBERINGS:
        for alignment in range(5):
            r = enumerate_keys(5, alignment, numbering, model=model)
            k4.append(r)
    baseline = {a: english_baseline(5, a, model) for a in range(5)}
    controls = []
    for numbering in NUMBERINGS:
        seeds = control_seeds if numbering == "A-Z" else other_seeds
        for alignment in (3, 4):
            for seed in range(seeds):
                controls.append(planted_control(alignment, 1000 * alignment + seed, numbering, model))
    nulls = [planted_control(alignment, 5000 + 1000 * alignment + seed, "A-Z", model, english=False)
             for alignment in (3, 4) for seed in range(control_seeds)]
    return {"k4": k4, "baseline": baseline, "controls": controls, "nulls": nulls,
            "seconds": round(time.time() - started, 1), "solved": False, "claimed_plaintext": None}

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "enumerate":
        import json

        result = run()
        print(json.dumps(result, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    else:
        for row in scan()["rows"]:
            print(row)
