"""K4 under the surviving letter-chain shapes: enumerate every key, then read.

For each chain shape the elimination left open, EVERY surviving primer is a
complete key: the stream is fixed for all 97 positions and the alphabet is
fixed on the 14 crib letters, leaving 12 free letters against 12 free
positions. That is an anchored substitution puzzle. If K4 is one of these
shapes, annealing under the repository quadgram model recovers the message;
otherwise the best candidates are language evidence, not exclusions.

Validated end to end on a planted English target before touching K4.
Not committed: scratch for the letter-chain language pass.
"""

from __future__ import annotations

import itertools
import json
import random
import sys

import numpy as np

from engine.k4_letter_chain import (
    ALPHABET_INDEX,
    CRIB_SPANS,
    _reduce,
    coefficients,
)
from engine.k4_gromark_obstruction import crib_pairs
from engine.language import ENGLISH_ORDER, get_model
from engine.solvers.k4_attempt import K4_CIPHERTEXT

FULL = 97
IDX = ALPHABET_INDEX
CAP = 12_000_000  # largest assignment space swept

PAIRS = crib_pairs(K4_CIPHERTEXT, CRIB_SPANS)
LETTERS = sorted({c for _, c, _ in PAIRS})
COL = {c: j for j, c in enumerate(LETTERS)}
CIPHER = np.array([ord(K4_CIPHERTEXT[i]) - 65 for i in range(FULL)])
CIPHER_POS = np.array([p for p, _, _ in PAIRS], dtype=np.int64)
PLAIN_IDX = np.array([IDX[pl] for _, _, pl in PAIRS], dtype=np.int64)
LET_COL = np.array([COL[c] for _, c, _ in PAIRS], dtype=np.int64)
N_LET = len(LETTERS)
NLT = [ord(ch) - 65 for ch in LETTERS]


def congruences(m, a, b, rec, ap):
    """The same-letter congruence system for one shape."""
    rows_c = coefficients(m, a, b, rec, FULL)
    by_letter = {}
    for (pos, c, pl) in PAIRS:
        by_letter.setdefault(c, []).append((pos, IDX[pl]))
    eq_rows, eq_rhs = [], []
    for uses in by_letter.values():
        for (pi, pli), (pj, plj) in itertools.combinations(uses, 2):
            eq_rows.append([(rows_c[pi][t] - rows_c[pj][t]) % 26 for t in range(m)])
            eq_rhs.append((ap * (plj - pli)) % 26)
    return rows_c, eq_rows, eq_rhs


def survivors(m, a, b, rec, ap):
    """Every (primer, apply) for this shape that is consistent and distinct.

    Returns (list of (primer, stream97, apply), count_of_space). None when the
    space exceeds the sweep cap.
    """
    rows_c, eq_rows, eq_rhs = congruences(m, a, b, rec, ap)
    pivot_cols, reduced, rank = _reduce(eq_rows, eq_rhs, m)
    # zero rows with a nonzero right-hand side: the system itself is inconsistent
    for row in reduced[rank:]:
        if all(x % 26 == 0 for x in row[:m]) and row[m] % 26 != 0:
            return [], 0
    free = [c for c in range(m) if c not in pivot_cols]
    total = 26 ** len(free)
    if total > CAP:
        return None, total
    W = np.array(rows_c, dtype=np.int64)          # (97, m)
    Wc = W[CIPHER_POS]                             # (npairs, m)
    pivot_rhs = np.array([reduced[i][m] % 26 for i in range(rank)], dtype=np.int64)
    free_mat = (np.array([[reduced[i][c] % 26 for c in free] for i in range(rank)],
                         dtype=np.int64) if rank else
                np.zeros((0, len(free)), dtype=np.int64))
    survivors_out = []
    # every candidate must satisfy ALL reduced rows: _reduce pivots only on
    # unit coefficients, so leftover rows can still veto a candidate
    row_mat = np.array([[row[t] % 26 for t in range(m)] for row in reduced],
                       dtype=np.int64)
    row_rhs = np.array([row[m] % 26 for row in reduced], dtype=np.int64)
    if not free:
        prim = np.zeros((1, m), dtype=np.int64)
        if rank:
            prim[:, pivot_cols] = pivot_rhs
        if ((prim @ row_mat.T) % 26 != row_rhs[None, :]).any():
            return [], 0
        stream = (prim @ W.T) % 26
        t14 = (PLAIN_IDX[None, :] + ap * stream[0, CIPHER_POS]) % 26
        t_val = np.array([0] * N_LET, dtype=np.int64)
        for k, j in enumerate(LET_COL):
            t_val[k] = t14[0, k]
        if len(set(t_val.tolist())) == N_LET:
            survivors_out.append((tuple(prim[0].tolist()), tuple(stream[0].tolist()), ap))
        return survivors_out, total
    # vectorized mesh over free vars, chunked by the first free dimension
    rest = list(itertools.product(range(26), repeat=len(free) - 1)) if len(free) > 1 else [()]
    rest_mat = np.array(rest, dtype=np.int64)      # (26^(f-1), f-1)
    for v0 in range(26):
        k = rest_mat.shape[0]
        assign = np.empty((k, len(free)), dtype=np.int64)
        assign[:, 0] = v0
        if len(free) > 1:
            assign[:, 1:] = rest_mat
        prim = np.empty((k, m), dtype=np.int32)
        prim[:, pivot_cols] = (pivot_rhs[None, :] - assign @ free_mat.T) % 26
        prim[:, free] = assign
        prim64 = prim.astype(np.int64)
        solved_rows = (prim64 @ row_mat.T) % 26 == row_rhs[None, :]
        tcrib = (PLAIN_IDX[None, :] + ap * ((prim64 @ Wc.T) % 26)) % 26
        T14 = np.empty((k, N_LET), dtype=np.int32)
        T14[:] = -1
        for j, col in enumerate(LET_COL):
            T14[:, col] = tcrib[:, j]
        order = np.sort(T14, axis=1)
        okmask = np.all(np.diff(order, axis=1) > 0, axis=1) & solved_rows.all(axis=1)
        if okmask.any():
            good = np.nonzero(okmask)[0]
            full_stream = (prim[good].astype(np.int64) @ W.T) % 26
            for i in range(good.shape[0]):
                survivors_out.append((tuple(int(x) for x in prim[good[i]]),
                                      tuple(int(x) for x in full_stream[i]), ap))
    return survivors_out, total


def climb(stream, ap, seed: int, restarts: int = 6):
    """Anchored anneal over the free alphabet letters under the quadgram model."""
    model = get_model()
    logp = model.logp
    T = [-1] * 26
    fixed = [False] * 26
    for (pos, c, pl) in PAIRS:
        val = (IDX[pl] + ap * stream[pos]) % 26
        ci = ord(c) - 65
        if fixed[ci]:
            assert T[ci] == val
        else:
            T[ci], fixed[ci] = val, True
    letters_used = [ord(K4_CIPHERTEXT[i]) - 65 for i in range(FULL)]
    free_letters = [i for i in range(26) if not fixed[i]]
    seated = {T[i] for i in range(26) if fixed[i]}
    free_pos = [v for v in range(26) if v not in seated]
    counts = {i: letters_used.count(i) for i in free_letters}

    def plaintext():
        S = stream
        a = ap
        return [(T[CIPHER[i]] - a * S[i]) % 26 for i in range(FULL)]

    def score_of(p):
        lp = logp
        s = 0.0
        a, b, c = p[0], p[1], p[2]
        for i in range(3, FULL):
            d = p[i]
            s += lp[((a * 26 + b) * 26 + c) * 26 + d]
            a, b, c = b, c, d
        return s

    rng = random.Random(seed)
    best_score, best_text, best_T = float("-inf"), None, None
    ranked = sorted(free_letters, key=lambda i: -counts[i])
    for r in range(restarts):
        # init: map the most frequent free cipher letter to the alphabet
        # position of the most frequent English letter, and so on down
        pos_order = sorted(free_pos, key=lambda v: ENGLISH_ORDER.index(chr(65 + v)))
        for lt, v in zip(ranked, pos_order):
            T[lt] = v
        if r:
            vals = [T[i] for i in free_letters]
            rng.shuffle(vals)
            for i, v in zip(free_letters, vals):
                T[i] = v
        # greedy polish: retarget one free letter at a time
        moves = [(lt, v) for lt in free_letters for v in free_pos]
        improved = True
        while improved:
            improved = False
            base = score_of(plaintext())
            best_gain, best_move = 0.0, None
            for (lt, v) in moves:
                cur = T[lt]
                if v == cur:
                    continue
                T[lt] = v
                gain = score_of(plaintext()) - base
                T[lt] = cur
                if gain > best_gain + 1e-9:
                    best_gain, best_move = gain, (lt, v)
            if best_move:
                T[best_move[0]] = best_move[1]
                improved = True
        s = score_of(plaintext())
        if s > best_score:
            best_score, best_text, best_T = s, plaintext(), T[:]
    text = "".join(chr(65 + v) for v in best_text)
    for start, word in CRIB_SPANS:
        assert text[start:start + len(word)] == word, "crib lost in decode"
    return best_score, text


def planted_english_target(seed: int, m: int, a: int, b: int, rec: int, ap: int):
    """A REAL English K4-shaped target: prose from the training file with both
    cribs planted, encrypted under a random primer and a random alphabet."""
    prose_path = "engine/data/neural_train_public.txt"
    text_lines = open(prose_path, encoding="utf-8").read().split()
    rng = random.Random(seed)
    prose = rng.choice(text_lines) + " " + rng.choice(text_lines) + " " + rng.choice(text_lines)
    letters = [ch for ch in prose.upper() if "A" <= ch <= "Z"]
    while len(letters) < FULL:
        letters += [ch for ch in rng.choice(text_lines).upper() if "A" <= ch <= "Z"]
    plain = letters[:FULL]
    for start, word in CRIB_SPANS:
        plain[start:start + len(word)] = list(word)
    rows_c = coefficients(m, a, b, rec, FULL)
    primer = [rng.randrange(26) for _ in range(m)]
    stream = [sum(rows_c[i][t] * primer[t] for t in range(m)) % 26 for i in range(FULL)]
    alphabet = random.Random(9).sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 26)
    cipher = [alphabet[(IDX[plain[i]] + ap * stream[i]) % 26] for i in range(FULL)]
    return "".join(cipher), primer, "".join(plain)


def hunt(ciphertext, quiet: bool = False, shapes=None):
    """Run the whole attack on one ciphertext with the given crib spans."""
    global PAIRS, CIPHER, CIPHER_POS, PLAIN_IDX, LET_COL, LETTERS, COL, N_LET, NLT
    PAIRS = crib_pairs(ciphertext, CRIB_SPANS)
    LETTERS = sorted({c for _, c, _ in PAIRS})
    COL = {c: j for j, c in enumerate(LETTERS)}
    N_LET = len(LETTERS)
    CIPHER = np.array([ord(ciphertext[i]) - 65 for i in range(FULL)])
    CIPHER_POS = np.array([p for p, _, _ in PAIRS], dtype=np.int64)
    PLAIN_IDX = np.array([IDX[pl] for _, _, pl in PAIRS], dtype=np.int64)
    LET_COL = np.array([COL[c] for _, c, _ in PAIRS], dtype=np.int64)
    shapes = shapes or default_shapes()
    streams: dict[str, dict] = {}
    shape_report = []
    for (m, a, b, rec, ap) in shapes:
        sur, total = survivors(m, a, b, rec, ap)
        if sur is None:
            shape_report.append({"m": m, "a": a, "b": b, "rec": rec, "ap": ap,
                                 "answer": "skipped", "space": total})
            if not quiet:
                print(f"m={m} lag=({a},{b}) rec={rec:+d} ap={ap:+d}: space {total} > cap, skipped", flush=True)
            continue
        for primer, stream, ap_ in sur:
            if ap_ == 1:
                canon_primer, canon_stream = primer, stream
            else:
                canon_primer = tuple((-p) % 26 for p in primer)
                canon_stream = tuple((-v) % 26 for v in stream)
            key = str(canon_stream)
            if key not in streams:
                streams[key] = {"primer": canon_primer, "stream": canon_stream,
                                "m": m, "a": a, "b": b, "rec": rec}
        shape_report.append({"m": m, "a": a, "b": b, "rec": rec, "ap": ap,
                             "answer": "fits", "primers": len(sur), "space": total,
                             "solved": False, "claimed_plaintext": None})
        if not quiet:
            print(f"m={m} lag=({a},{b}) rec={rec:+d} ap={ap:+d}: {len(sur)} primers", flush=True)
    results = []
    for j, (_, item) in enumerate(sorted(streams.items())):
        score, text = climb(item["stream"], 1, seed=77)
        results.append({**item, "score": round(score, 2),
                        "per_letter": round(score / (FULL - 3), 3), "text": text})
        if not quiet and j % 100 == 0:
            print(f"  climbed {j}/{len(streams)}", flush=True)
    results.sort(key=lambda r: -r["score"])
    return results, shape_report, len(streams)


def default_shapes():
    shapes = []
    for m in (11, 12, 13, 14):
        for rec in (1, -1):
            for ap in (1, -1):
                shapes.append((m, m, m - 1, rec, ap))
    shapes += [(10, 8, 10, 1, 1), (10, 8, 10, 1, -1),
               (10, 8, 10, -1, 1), (10, 8, 10, -1, -1),
               (10, 2, 10, -1, 1), (10, 2, 10, -1, -1)]
    return shapes


def self_test():
    """The attack must recover a planted ENGLISH target end to end."""
    cipher, primer, truth = planted_english_target(7, 12, 12, 11, 1, 1)
    results, shapes, n = hunt(cipher, quiet=True)
    best = results[0]
    match = sum(1 for a, b in zip(best["text"], truth) if a == b)
    print(f"self-test: shapes={len(shapes)} streams={n} "
          f"best per_letter={best['per_letter']} letters matching truth: {match}/97")
    print("   truth:", truth[:40], "...")
    print("   found:", best["text"][:40], "...")
    return match


def main():
    self_test()
    results, shape_report, n = hunt(K4_CIPHERTEXT)
    with open("work/k4_chain_hunt.json", "w") as fh:
        json.dump({"shapes": shape_report, "top": results[:200]}, fh, indent=1)
    print(f"\n== K4: {n} canonical streams climbed; top by quadgram ==")
    for r in results[:10]:
        print(f"m={r['m']} lag=({r['a']},{r['b']}) rec={r['rec']:+d} per_letter={r['per_letter']}")
        print("   ", r["text"])


if __name__ == "__main__":
    main()
