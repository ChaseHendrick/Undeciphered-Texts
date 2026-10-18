"""K4 as a transposition composed with an in-place periodic substitution: clue-only bounds.

The model is a transposition T (T[j] is the ciphertext position of
plaintext position j) and a periodic substitution of period p with any
alphabet in each column, in either order:

- transpose then substitute: C[i] = sub_{i mod p}(Pt[i]) with Pt[T[j]] = P[j],
  so clue letter P[j] shows at ciphertext position T[j] under column T[j] mod p;
- substitute then transpose: S[j] = sub_{j mod p}(P[j]) and C[T[j]] = S[j],
  so clue letter P[j] uses column j mod p and shows at T[j].

The only evidence is the two published clues, EASTNORTHEAST at 21 and
BERLINCLOCK at 63 (zero based). Each hypothesis gives 24 (column,
plaintext letter, ciphertext letter) triples. The bijection bound of
engine.k4_periodic_bijection then excludes it when one column needs a
plaintext letter to go to two ciphertext letters or two plaintext letters
to go to one. That holds for every alphabet, so no language is assumed.

Survivors meet a stronger filter: straight Vigenere or Beaufort on A-Z or
on the KRYPTOS keyed alphabet, one shift per column. A strong survivor
whose key is complete (every column has a clue letter) can be decrypted;
it is reported only as an unverified candidate with its English quadgram
score and index of coincidence.

Two text lengths are run. 97 is K4 as carved. 98 puts the "?" that ends
K3 on the sculpture in front of K4 as an extra ciphertext symbol; the clue
positions then move up by one. A clue letter cannot be enciphered to "?"
under the strong filter; the bijection bound treats "?" as a 27th symbol.

Families (construction reasons in docs/k4-focus/transposition-substitution-2026-10-18.md):

a. columnar, incomplete last row, every column order, widths 2 to 10,
   both read directions (compiled kernel engine/k4_transposition_sub.c);
b. K3-style double rotation on irregular grids, checked against K3;
c. route transpositions on every rectangle with a short last row;
d. keyed columnar and Myszkowski with a frozen keyword list.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import ctypes
import random
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

import numpy as np

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.solvers.k4_attempt import K4_CIPHERTEXT

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRYPTOS_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
QUESTION = 26
MAX_PERIOD = 26
LENGTHS = (97, 98)
COMPOSITIONS = ("transpose-then-substitute", "substitute-then-transpose")
VARIANTS = ("vigenere-AZ", "beaufort-AZ", "vigenere-KRYPTOS", "beaufort-KRYPTOS")
COLUMNAR_WIDTHS = tuple(range(2, 11))
FAMILIES = ("a-columnar", "b-rotation", "c-route", "d-keyword")
THREADS = 2

# Frozen keyword list from the task, then extras with a sourced reason.
KEYWORDS = (
    "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "BERLINCLOCK", "EASTNORTHEAST",
    "SANBORN", "SCHEIDT", "LANGLEY", "SHADOW", "IQLUSION", "UNDERGRUUND", "LAYERTWO",
)
EXTRA_KEYWORDS = {
    # K2 as first published ended "ID BY ROWS"; Sanborn corrected it to "X LAYER TWO" in 2006.
    "IDBYROWS": "https://en.wikipedia.org/wiki/Kryptos",
    # K3 paraphrases Howard Carter's account of opening Tutankhamun's tomb.
    "CARTER": "https://en.wikipedia.org/wiki/Kryptos",
}
ALL_KEYWORDS = KEYWORDS + tuple(EXTRA_KEYWORDS)

_SOURCE = Path(__file__).resolve().parent / "k4_transposition_sub.c"
_NSTAT = 12
_CANDW = 32
_CAP = 4096


# ---------------------------------------------------------------- setup


def setup(length: int = 97, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    """Ciphertext symbols (0..25, 26 for '?'), clue plaintext positions and letters."""
    letters = [ord(ch) - 65 for ch in ciphertext if ch.isalpha()]
    if length == len(letters) + 1:
        symbols, shift = [QUESTION] + letters, 1
    elif length == len(letters):
        symbols, shift = letters, 0
    else:
        raise ValueError("length must be the letter count or one more")
    cpos, cpl = [], []
    for start, word in spans:
        for offset, ch in enumerate(word):
            cpos.append(start + offset + shift)
            cpl.append(ord(ch) - 65)
    return {"n": length, "ct": symbols, "cpos": cpos, "cpl": cpl}


def _ranks() -> list[list[int]]:
    return [[LETTERS.index(ch) for ch in LETTERS], [KRYPTOS_ALPHABET.index(ch) for ch in LETTERS]]


# ------------------------------------------------- pure Python reference


def columns(perm, cpos, comp: int, p: int) -> list[int]:
    return [(perm[j] if comp == 0 else j) % p for j in cpos]


def bijection_ok(perm, s: dict, comp: int, p: int) -> bool:
    plain_to, cipher_to = {}, {}
    for col, j, pl in zip(columns(perm, s["cpos"], comp, p), s["cpos"], s["cpl"]):
        cl = s["ct"][perm[j]]
        if plain_to.setdefault((col, pl), cl) != cl or cipher_to.setdefault((col, cl), pl) != pl:
            return False
    return True


def strong_key(perm, s: dict, comp: int, p: int, variant: int):
    """Shift per column (None where no clue) or None on a contradiction."""
    rank = _ranks()[variant >> 1]
    key = [None] * p
    for col, j, pl in zip(columns(perm, s["cpos"], comp, p), s["cpos"], s["cpl"]):
        cl = s["ct"][perm[j]]
        if cl == QUESTION:
            return None
        shift = (rank[cl] + rank[pl]) % 26 if variant & 1 else (rank[cl] - rank[pl]) % 26
        if key[col] is None:
            key[col] = shift
        elif key[col] != shift:
            return None
    return key


def decrypt(perm, s: dict, comp: int, p: int, variant: int, key) -> str:
    """Full decryption under a complete strong key. '?' stays '?'."""
    rank = _ranks()[variant >> 1]
    alphabet = LETTERS if variant >> 1 == 0 else KRYPTOS_ALPHABET
    ct, n = s["ct"], s["n"]

    def unsub(symbol: int, col: int) -> str:
        if symbol == QUESTION:
            return "?"
        r = (key[col] - rank[symbol]) % 26 if variant & 1 else (rank[symbol] - key[col]) % 26
        return alphabet[r]

    if comp == 0:
        return "".join(unsub(ct[perm[j]], perm[j] % p) for j in range(n))
    return "".join(unsub(ct[perm[j]], j % p) for j in range(n))


def encipher(plain: list[int], perm, comp: int, alphabets: list[list[int]]) -> list[int]:
    """Planted-control encipherment with one arbitrary alphabet per column."""
    n, p = len(plain), len(alphabets)
    out = [0] * n
    if comp == 0:
        moved = [0] * n
        for j in range(n):
            moved[perm[j]] = plain[j]
        for i in range(n):
            out[i] = alphabets[i % p][moved[i]]
    else:
        for j in range(n):
            out[perm[j]] = alphabets[j % p][plain[j]]
    return out


def shift_alphabets(variant: int, key: list[int]) -> list[list[int]]:
    """Per-column plain-to-cipher maps for a Vigenere or Beaufort key."""
    rank = _ranks()[variant >> 1]
    alphabet = LETTERS if variant >> 1 == 0 else KRYPTOS_ALPHABET
    out = []
    for k in key:
        if variant & 1:
            out.append([LETTERS.index(alphabet[(k - rank[x]) % 26]) for x in range(26)])
        else:
            out.append([LETTERS.index(alphabet[(rank[x] + k) % 26]) for x in range(26)])
    return out


def inverse(perm) -> list[int]:
    out = [0] * len(perm)
    for j, t in enumerate(perm):
        out[t] = j
    return out


def apply(perm, text):
    """Text moved by perm: out[perm[j]] = text[j]."""
    out = [None] * len(perm)
    for j, t in enumerate(perm):
        out[t] = text[j]
    return out


# ------------------------------------------------------ transpositions


def columnar_perm(n: int, order, direction: int) -> list[int]:
    """Write rows of len(order), read columns order[0], order[1], ...; direction 1 is the inverse."""
    w = len(order)
    rows, full = -(-n // w), n % w
    length = [rows if (full == 0 or c < full) else rows - 1 for c in range(w)]
    start, cum = [0] * w, 0
    for c in order:
        start[c] = cum
        cum += length[c]
    perm = [start[j % w] + j // w for j in range(n)]
    return perm if direction == 0 else inverse(perm)


def _from_reading(n: int, reading) -> list[int]:
    perm = [0] * n
    for i, src in enumerate(reading):
        perm[src] = i
    return perm


def rotation_step(n: int, w: int, clockwise: bool, align: str) -> list[int]:
    """Write n letters in rows of w, rotate the grid a quarter turn, read rows.

    The last row is short when w does not divide n. align 'left' puts its
    letters in the leftmost cells, 'right' in the rightmost. Rotating
    clockwise and reading rows reads the columns left to right, each from
    the bottom up; anticlockwise reads them right to left, each top down.
    Empty cells are skipped. On a full rectangle this is exactly the turn
    in Sanborn's K3 coding chart.
    """
    rows = -(-n // w)
    last = n - (rows - 1) * w
    index, k = {}, 0
    for r in range(rows):
        for c in range(w):
            if r < rows - 1 or (c < last if align == "left" else c >= w - last):
                index[(r, c)] = k
                k += 1
    if clockwise:
        coords = [(r, c) for c in range(w) for r in range(rows - 1, -1, -1)]
    else:
        coords = [(r, c) for c in range(w - 1, -1, -1) for r in range(rows)]
    return _from_reading(n, [index[rc] for rc in coords if rc in index])


def rotation_perm(n: int, w1: int, w2: int, rot1: bool, rot2: bool, align1: str = "left",
                  align2: str = "left") -> list[int]:
    s1 = rotation_step(n, w1, rot1, align1)
    s2 = rotation_step(n, w2, rot2, align2)
    return [s2[s1[j]] for j in range(n)]


def k3_reproduced() -> dict:
    """The rotation family with Sanborn's K3 grids, against the repo's K3 constants."""
    from engine.solvers.columnar import KRYPTOS_K3_CIPHERTEXT, KRYPTOS_K3_PLAINTEXT

    perm = rotation_perm(336, 42, 14, True, True)
    enc = "".join(apply(perm, KRYPTOS_K3_PLAINTEXT))
    dec = "".join(KRYPTOS_K3_CIPHERTEXT[perm[j]] for j in range(336))
    return {"encrypt_matches": enc == KRYPTOS_K3_CIPHERTEXT, "decrypt_matches": dec == KRYPTOS_K3_PLAINTEXT,
            "grids": "8 rows of 42, quarter turn clockwise, rows of 14, quarter turn clockwise"}


def _base_routes(rows: int, w: int) -> dict:
    routes = {
        "rows": [(r, c) for r in range(rows) for c in range(w)],
        "rows-boustrophedon": [(r, c if r % 2 == 0 else w - 1 - c) for r in range(rows) for c in range(w)],
        "columns": [(r, c) for c in range(w) for r in range(rows)],
        "columns-boustrophedon": [(r if c % 2 == 0 else rows - 1 - r, c) for c in range(w) for r in range(rows)],
    }
    for name, first in (("spiral-clockwise", (0, 1)), ("spiral-anticlockwise", (1, 0))):
        seen, out = set(), []
        r, c, (dr, dc) = 0, 0, first
        for _ in range(rows * w):
            out.append((r, c))
            seen.add((r, c))
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < w) or (nr, nc) in seen:
                if name == "spiral-clockwise":
                    dr, dc = dc, -dr
                else:
                    dr, dc = -dc, dr
                nr, nc = r + dr, c + dc
            r, c = nr, nc
        routes[name] = out
    for name, key in (("diagonal", lambda r, c: r + c), ("antidiagonal", lambda r, c: c - r)):
        groups: dict[int, list] = {}
        for r in range(rows):
            for c in range(w):
                groups.setdefault(key(r, c), []).append((r, c))
        ordered = [groups[d] for d in sorted(groups)]
        routes[name + "-down"] = [rc for g in ordered for rc in g]
        routes[name + "-up"] = [rc for g in ordered for rc in reversed(g)]
        routes[name + "-zigzag"] = [rc for i, g in enumerate(ordered) for rc in (g if i % 2 else reversed(g))]
    return routes


def route_perms(n: int):
    """(label, perm) for every route on every width 2..n-1 with a short last row.

    Letters fill the rectangle by rows; the empty cells are the right end of
    the last row. Each base route is taken from all four corners (the four
    reflections), forwards and backwards, and both as the reading route
    (write rows, read route) and as the writing route (the inverse).
    """
    for w in range(2, n):
        rows = -(-n // w)
        idx = {(r, c): r * w + c for r in range(rows) for c in range(w) if r * w + c < n}
        for name, coords in _base_routes(rows, w).items():
            for flip in range(4):
                fr = (lambda r: rows - 1 - r) if flip & 2 else (lambda r: r)
                fc = (lambda c: w - 1 - c) if flip & 1 else (lambda c: c)
                reading = [idx[(fr(r), fc(c))] for r, c in coords if (fr(r), fc(c)) in idx]
                for reverse in (False, True):
                    order = reading[::-1] if reverse else reading
                    perm = _from_reading(n, order)
                    label = f"w{w} {name} corner{flip} {'reversed' if reverse else 'forward'}"
                    yield label + " read", perm
                    yield label + " written", inverse(perm)


def keyed_order(keyword: str) -> list[int]:
    """Columns in reading order: alphabetical, ties left to right."""
    return sorted(range(len(keyword)), key=lambda i: (keyword[i], i))


def myszkowski_perm(n: int, keyword: str) -> list[int]:
    """Write rows under the keyword; tied columns are read row by row together."""
    w = len(keyword)
    numbers = sorted(set(keyword))
    reading = []
    rows = -(-n // w)
    for letter in numbers:
        cols = [c for c in range(w) if keyword[c] == letter]
        for r in range(rows):
            for c in cols:
                if r * w + c < n:
                    reading.append(r * w + c)
    return _from_reading(n, reading)


def keyword_perms(n: int):
    for word in ALL_KEYWORDS:
        order = keyed_order(word)
        conv = inverse(order)
        for label, o in (("keyed", order), ("keyed-inverse-convention", conv)):
            for d in (0, 1):
                yield f"{word} {label} dir{d}", columnar_perm(n, o, d)
        m = myszkowski_perm(n, word)
        yield f"{word} myszkowski dir0", m
        yield f"{word} myszkowski dir1", inverse(m)


def rotation_perms(n: int):
    """(label, perm) for every width pair, turn pair and short-row alignment pair."""
    steps = {}
    for w in range(1, n + 1):
        for rot in (True, False):
            for align in (("left",) if n % w == 0 else ("left", "right")):
                steps[(w, rot, align)] = np.array(rotation_step(n, w, rot, align), dtype=np.int32)
    keys = list(steps)
    for k1 in keys:
        s1 = steps[k1]
        for k2 in keys:
            yield (k1, k2), steps[k2][s1]


def distinct(perms) -> tuple[list[str], np.ndarray, int]:
    """Drop repeated permutations; keep the first label of each."""
    seen, labels, rows, raw = set(), [], [], 0
    for label, perm in perms:
        raw += 1
        arr = np.asarray(perm, dtype=np.int32)
        key = arr.astype(np.uint8).tobytes()
        if key in seen:
            continue
        seen.add(key)
        labels.append(label)
        rows.append(arr)
    return labels, np.vstack(rows), raw


@lru_cache(maxsize=None)
def family_perms(family: str, n: int) -> tuple[list, np.ndarray, int]:
    if family == "b-rotation":
        return distinct(rotation_perms(n))
    if family == "c-route":
        return distinct(route_perms(n))
    if family == "d-keyword":
        return distinct(keyword_perms(n))
    raise ValueError(family)


# ------------------------------------------------------- compiled kernel


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed for engine.k4_transposition_sub")
    built = Path(tempfile.mkdtemp(prefix="k4-transposition-sub-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE)], check=True)
    lib = ctypes.CDLL(str(built))
    lib.ts_columnar.restype = ctypes.c_longlong
    lib.ts_perms.restype = None
    return lib


class _Job:
    def __init__(self, s: dict, maxp: int):
        self.maxp = maxp
        self.ct = (ctypes.c_int * s["n"])(*s["ct"])
        self.ncl = len(s["cpos"])
        self.cpos = (ctypes.c_int * self.ncl)(*s["cpos"])
        self.cpl = (ctypes.c_int * self.ncl)(*s["cpl"])
        self.rank = (ctypes.c_int * 52)(*(_ranks()[0] + _ranks()[1]))
        self.stats = (ctypes.c_longlong * (2 * (maxp + 1) * _NSTAT))()
        self.cands = (ctypes.c_int * (_CAP * _CANDW))()
        self.ncand = ctypes.c_int(0)

    def result(self):
        stats = np.array(self.stats, dtype=np.int64).reshape(2, self.maxp + 1, _NSTAT)
        kept = min(self.ncand.value, _CAP)
        raw = np.array(self.cands[: kept * _CANDW], dtype=np.int64).reshape(kept, _CANDW)
        cands = [(int(r[0]), int(r[1]), int(r[2]), tuple(int(v) for v in r[4 : 4 + r[3]])) for r in raw]
        return stats, cands, self.ncand.value


def run_columnar(s: dict, widths=COLUMNAR_WIDTHS, maxp: int = MAX_PERIOD, threads: int = THREADS) -> dict:
    lib = _kernel()
    tasks = [(w, f) for w in widths for f in range(w)]

    def one(task):
        w, first = task
        job = _Job(s, maxp)
        orders = lib.ts_columnar(s["n"], job.ct, job.ncl, job.cpos, job.cpl, job.rank, maxp, w, first,
                                 job.stats, job.cands, _CAP, ctypes.byref(job.ncand))
        return (w, orders) + job.result()

    stats = np.zeros((2, maxp + 1, _NSTAT), dtype=np.int64)
    by_width = {w: np.zeros((2, maxp + 1, _NSTAT), dtype=np.int64) for w in widths}
    cands, total_cands, orders = [], 0, {w: 0 for w in widths}
    with ThreadPoolExecutor(max_workers=threads) as pool:
        for w, n_orders, st, cs, nc in pool.map(one, tasks):
            stats += st
            by_width[w] += st
            orders[w] += n_orders
            total_cands += nc
            cands.extend(cs)
    return {"stats": stats, "by_width": by_width, "orders": orders, "cands": cands, "complete_total": total_cands}


def run_perms(s: dict, perms: np.ndarray, maxp: int = MAX_PERIOD, threads: int = THREADS) -> dict:
    lib = _kernel()
    perms = np.ascontiguousarray(perms, dtype=np.int32)
    count = perms.shape[0]
    chunks = [(i, min(count, i + 4096)) for i in range(0, count, 4096)]

    def one(chunk):
        lo, hi = chunk
        job = _Job(s, maxp)
        block = perms[lo:hi]
        ptr = block.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        lib.ts_perms(s["n"], job.ct, job.ncl, job.cpos, job.cpl, job.rank, maxp, ptr, hi - lo, lo,
                     job.stats, job.cands, _CAP, ctypes.byref(job.ncand))
        return job.result()

    stats = np.zeros((2, maxp + 1, _NSTAT), dtype=np.int64)
    cands, total = [], 0
    with ThreadPoolExecutor(max_workers=threads) as pool:
        for st, cs, nc in pool.map(one, chunks):
            stats += st
            total += nc
            cands.extend(cs)
    return {"stats": stats, "cands": cands, "complete_total": total}


# ------------------------------------------------------------- reporting


def _ic(text: str) -> float:
    letters = [ch for ch in text if ch.isalpha()]
    n = len(letters)
    counts = [letters.count(ch) for ch in LETTERS]
    return sum(c * (c - 1) for c in counts) / (n * (n - 1)) if n > 1 else 0.0


def score_text(text: str) -> float:
    from engine.language import get_model

    seq = [ord(ch) - 65 for ch in text if ch.isalpha()]
    return get_model().score(seq) / (len(seq) - 3)


def candidate_record(family: str, s: dict, cand, labels=None, perms=None) -> dict:
    comp, p, variant, ident = cand
    if family == "a-columnar":
        w, direction, order = ident[0], ident[1], ident[2 : 2 + ident[0]]
        perm = columnar_perm(s["n"], order, direction)
        label = f"width {w} order {list(order)} dir{direction}"
    else:
        perm = [int(v) for v in perms[ident[0]]]
        label = labels[ident[0]] if not isinstance(labels[ident[0]], tuple) else str(labels[ident[0]])
    key = strong_key(perm, s, comp, p, variant)
    assert key is not None and None not in key, "kernel and reference disagree"
    plain = decrypt(perm, s, comp, p, variant, key)
    for j, pl in zip(s["cpos"], s["cpl"]):
        assert plain[j] == LETTERS[pl]
    return {"family": family, "n": s["n"], "transposition": label, "composition": COMPOSITIONS[comp],
            "period": p, "clue_checks": len(s["cpos"]) - p, "variant": VARIANTS[variant],
            "key": "".join(LETTERS[k] for k in key),
            "plaintext_unverified": plain, "quadgram_per_letter": round(score_text(plain), 3),
            "ic": round(_ic(plain), 4)}


def summarize(stats: np.ndarray, maxp: int = MAX_PERIOD) -> dict:
    out = {}
    for comp in (0, 1):
        rows = stats[comp, 1 : maxp + 1]
        out[COMPOSITIONS[comp]] = {
            "checked": int(rows[:, 0].sum()),
            "bijection_excluded": int(rows[:, 0].sum() - rows[:, 1].sum()),
            "bijection_survivors": int(rows[:, 1].sum()),
            "strong_survivors": {VARIANTS[v]: int(rows[:, 2 + v].sum()) for v in range(4)},
            "complete_key_survivors": {VARIANTS[v]: int(rows[:, 6 + v].sum()) for v in range(4)},
            "strong_any": int(rows[:, 10].sum()),
            "complete_any": int(rows[:, 11].sum()),
            "strong_any_by_period": [int(x) for x in rows[:, 10]],
            "bijection_survivors_by_period": [int(x) for x in rows[:, 1]],
            "checked_by_period": [int(x) for x in rows[:, 0]],
        }
    return out


def run_family(family: str, n: int, ciphertext: str = K4_CIPHERTEXT, widths=COLUMNAR_WIDTHS) -> dict:
    s = setup(n, ciphertext)
    t0 = time.time()
    if family == "a-columnar":
        res = run_columnar(s, widths)
        labels = perms = None
        info = {"orders_per_width": res["orders"], "transpositions": 2 * sum(res["orders"].values())}
    else:
        labels, perms, raw = family_perms(family, n)
        res = run_perms(s, perms)
        info = {"raw_transpositions": raw, "transpositions": int(perms.shape[0])}
    elapsed = time.time() - t0
    records = [candidate_record(family, s, c, labels, perms) for c in res["cands"]]
    records.sort(key=lambda r: -r["quadgram_per_letter"])
    return {"family": family, "n": n, **info, "seconds": round(elapsed, 2), "summary": summarize(res["stats"]),
            "complete_key_total": res["complete_total"], "candidates": records,
            "by_width": {w: summarize(st) for w, st in res.get("by_width", {}).items()},
            "solved": False, "claimed_plaintext": None}


# ---------------------------------------------------------- controls


def random_family_perm(family: str, n: int, rng: random.Random):
    if family == "a-columnar":
        w = rng.choice(COLUMNAR_WIDTHS)
        order = rng.sample(range(w), w)
        return columnar_perm(n, order, rng.randrange(2))
    if family == "b-rotation":
        w1, w2 = rng.randrange(1, n + 1), rng.randrange(1, n + 1)
        a1, a2 = rng.choice(("left", "right")), rng.choice(("left", "right"))
        return rotation_perm(n, w1, w2, rng.random() < 0.5, rng.random() < 0.5, a1, a2)
    labels, perms, _ = family_perms(family, n)
    return [int(v) for v in perms[rng.randrange(perms.shape[0])]]


def planted(family: str, n: int, rng: random.Random, strong_variant: int | None = None):
    """Random letters with both clues planted, enciphered under a random hypothesis."""
    s = setup(n)
    plain = [rng.randrange(26) for _ in range(n)]
    for j, pl in zip(s["cpos"], s["cpl"]):
        plain[j] = pl
    perm = random_family_perm(family, n, rng)
    comp, p = rng.randrange(2), rng.randint(1, MAX_PERIOD)
    if strong_variant is None:
        alphabets = [rng.sample(range(26), 26) for _ in range(p)]
    else:
        alphabets = shift_alphabets(strong_variant, [rng.randrange(26) for _ in range(p)])
    ct = encipher(plain, perm, comp, alphabets)
    s = dict(s, ct=ct)
    return s, perm, comp, p, "".join(LETTERS[x] for x in plain)


def planted_controls(trials: int = 200, seed: int = 20261018) -> dict:
    """True hypotheses under random alphabets must never be excluded (reference and kernel)."""
    rng = random.Random(seed)
    out = {}
    for family in ("a-columnar", "b-rotation", "c-route", "d-keyword"):
        excluded, strong_missed, recovered, complete = 0, 0, 0, 0
        for t in range(trials):
            n = LENGTHS[t % 2]
            s, perm, comp, p, _plain = planted(family, n, rng)
            st = run_perms(s, np.array([perm]), threads=1)["stats"]
            if not bijection_ok(perm, s, comp, p) or st[comp, p, 1] != 1:
                excluded += 1
            v = rng.randrange(4)
            s, perm, comp, p, plain = planted(family, n, rng, strong_variant=v)
            key = strong_key(perm, s, comp, p, v)
            if key is None:
                strong_missed += 1
            elif None not in key:
                complete += 1
                recovered += decrypt(perm, s, comp, p, v, key) == plain
        out[family] = {"trials": trials, "true_excluded": excluded, "strong_true_excluded": strong_missed,
                       "strong_complete_keys": complete, "strong_complete_recovered": recovered}
    return out


def power(samples: int = 400, texts: int = 10, seed: int = 7) -> dict:
    """Fraction of random wrong hypotheses from the family excluded on planted texts."""
    rng = random.Random(seed)
    out = {}
    for family in ("a-columnar", "b-rotation", "c-route", "d-keyword"):
        stats = np.zeros((2, MAX_PERIOD + 1, _NSTAT), dtype=np.int64)
        for t in range(texts):
            n = LENGTHS[t % 2]
            s, true_perm, comp, p, _ = planted(family, n, rng)
            wrong = [random_family_perm(family, n, rng) for _ in range(samples)]
            wrong = [w for w in wrong if w != true_perm]
            stats += run_perms(s, np.array(wrong))["stats"]
        rec = {}
        for comp in (0, 1):
            chk, surv = stats[comp, 1:, 0], stats[comp, 1:, 1]
            rec[COMPOSITIONS[comp]] = {
                "excluded_fraction_by_period": [round(1 - int(b) / int(a), 4) for a, b in zip(chk, surv)],
                "excluded_fraction_all": round(1 - int(surv.sum()) / int(chk.sum()), 4),
            }
        out[family] = rec
    return out


def null_texts(count: int = 3, seed: int = 97) -> list[str]:
    """K4's own letters shuffled: same letter counts, no clue structure."""
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        letters = list(K4_CIPHERTEXT)
        rng.shuffle(letters)
        out.append("".join(letters))
    return out


def k4_report(families=FAMILIES, widths=COLUMNAR_WIDTHS, ciphertext: str = K4_CIPHERTEXT) -> dict:
    runs = [run_family(f, n, ciphertext, widths=widths) for f in families for n in LENGTHS]
    return {"runs": runs, "solved": False, "claimed_plaintext": None}


def candidate_summary(run: dict) -> dict:
    by_period: dict[int, int] = {}
    for rec in run["candidates"]:
        by_period[rec["period"]] = by_period.get(rec["period"], 0) + 1
    best = run["candidates"][0] if run["candidates"] else None
    return {"complete_key_total": run["complete_key_total"], "by_period": dict(sorted(by_period.items())),
            "best_quadgram_per_letter": best["quadgram_per_letter"] if best else None,
            "best": best}


def null_report(count: int = 3, families=FAMILIES, widths=COLUMNAR_WIDTHS) -> list[dict]:
    """The same enumeration on shuffled K4 letters, to show what chance gives."""
    out = []
    for text in null_texts(count):
        rep = k4_report(families, widths, text)
        out.append({"ciphertext": text, "runs": [
            {"family": r["family"], "n": r["n"], "summary": r["summary"], "candidates": candidate_summary(r)}
            for r in rep["runs"]]})
    return out


def _print_summary(run: dict) -> None:
    print(f"\n== {run['family']} n={run['n']} transpositions={run['transpositions']} seconds={run['seconds']}")
    for comp, rec in run["summary"].items():
        print(f"  {comp}: checked {rec['checked']} excluded {rec['bijection_excluded']} "
              f"survivors {rec['bijection_survivors']}")
        print(f"    strong {rec['strong_survivors']}")
        print(f"    complete {rec['complete_key_survivors']}")
        print(f"    survivors by period {rec['bijection_survivors_by_period']}")
        print(f"    strong any {rec['strong_any']} complete any {rec['complete_any']}")
        print(f"    strong any by period {rec['strong_any_by_period']}")
    summ = candidate_summary(run)
    print(f"  complete-key total {summ['complete_key_total']}, by period {summ['by_period']}")
    for rec in run["candidates"][:3]:
        print("   ", {k: rec[k] for k in ("transposition", "composition", "period", "clue_checks", "variant",
                                         "key", "quadgram_per_letter", "ic")})
        print("    unverified:", rec["plaintext_unverified"])


def main(argv: list[str]) -> None:
    """python3 -m engine.k4_transposition_sub [max_width] [null_count]"""
    widths = tuple(range(2, int(argv[0]) + 1)) if argv else COLUMNAR_WIDTHS
    nulls = int(argv[1]) if len(argv) > 1 else 0
    print("K3 reproduction:", k3_reproduced())
    print("planted controls:", planted_controls())
    for family, rec in power().items():
        for comp, x in rec.items():
            print(f"power {family} {comp}: all {x['excluded_fraction_all']}")
            print(f"  by period {x['excluded_fraction_by_period']}")
    report = k4_report(widths=widths)
    for run in report["runs"]:
        _print_summary(run)
        for w, summ in run["by_width"].items():
            print(f"   width {w}: " + "; ".join(
                f"{c[:5]} chk {r['checked']} surv {r['bijection_survivors']} "
                f"strong-any {r['strong_any']} complete-any {r['complete_any']}"
                for c, r in summ.items()))
    for i, null in enumerate(null_report(nulls, widths=widths) if nulls else []):
        print(f"\n## null {i}: {null['ciphertext']}")
        for r in null["runs"]:
            line = "; ".join(f"{c[:5]} surv {x['bijection_survivors']} strong-any {x['strong_any']} "
                             f"complete-any {x['complete_any']}" for c, x in r["summary"].items())
            print(f"  {r['family']} n={r['n']}: {line}; best {r['candidates']['best_quadgram_per_letter']} "
                  f"by period {r['candidates']['by_period']}")
    print("solved:", report["solved"], "claimed_plaintext:", report["claimed_plaintext"])


if __name__ == "__main__":
    main(sys.argv[1:])
