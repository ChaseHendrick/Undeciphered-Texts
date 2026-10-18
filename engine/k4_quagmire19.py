"""K4 as in-place periodic Quagmire I, II or IV, searched against English, with a power test.

`engine.k4_sat` shows that Quagmire I, II and IV at period 19 can place both
K4 clues (EASTNORTHEAST at 21, BERLINCLOCK at 63). The clues alone cannot say
more. This module asks whether a language search can: simulated annealing over
the keyed alphabet(s) and the period's key shifts, scored by the English
quadgram model of `engine.language.get_model()`, run in C
(`engine/k4_quagmire19.c`, compiled on first use).

Families, letters 0 to 25, K = K[i mod period]:
  q1: c = rank_A(p) + K             (keyed plain alphabet, straight cipher)
  q2: rank_B(c) = p + K             (straight plain, keyed cipher alphabet)
  q4: rank_B(c) = rank_A(p) + K     (both keyed)

Clues: every column holding a clue letter takes its shift from the alphabets
(the shift most of its clue letters ask for). Clue letters still wrong cost
LAMBDA nats each (5 by default; a forced-fit pass uses 30), so clue agreement
is a penalty, not a hard rule. The reported "feasible" state is the best one
with every clue letter right.

Moves: swap two letters of one alphabet, change a free column's shift, and
shift a group of clue letters tied by shared columns along the alphabet with
their spacing kept. Restarts repeat the anneal from random alphabets. Variants
tried while tuning are kept as options: parallel tempering (method="tempering"),
heat-bath letter moves (pheat), move-then-refit large moves (plns), all shifts
free instead of derived (derive=False), and seeded starts (start=...). None of
them lifted Quagmire II or IV recovery; see docs/k4-focus/quagmire19-2026-10-18.md.

Before anything is said about K4 the same search, with the same budget, is
run blind on planted English (`power`), on random ciphertexts with the clues
at the same places, and on shuffles of K4 (`nulls`). A K4 score counts as a
lead only if it beats every null run and reaches the planted English range.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import ctypes
import math
import random
import shutil
import subprocess
import tempfile
import time
from functools import lru_cache
from pathlib import Path

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.language import get_model
from engine.solvers.k4_attempt import K4_CIPHERTEXT

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FAMILIES = {"q1": 1, "q2": 2, "q4": 4}
LAMBDA = 5.0
_SOURCE = Path(__file__).with_name("k4_quagmire19.c")
_DATA = Path(__file__).resolve().parent / "data"
DEFAULT = {"restarts": 6, "iters": 1_000_000, "t0": 6.0, "t1": 0.3}


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed for engine.k4_quagmire19")
    built = Path(tempfile.mkdtemp(prefix="k4-quagmire19-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.q_anneal.restype = None
    lib.q_tempering.restype = None
    lib.q_set_moves.restype = None
    lib.q_set_lns.restype = None
    lib.q_eval.restype = None
    return lib


@lru_cache(maxsize=1)
def _tables():
    model = get_model()
    one, two, three = model.prefix
    return (
        (ctypes.c_double * len(model.logp))(*model.logp),
        (ctypes.c_double * 26)(*one),
        (ctypes.c_double * 676)(*two),
        (ctypes.c_double * 17576)(*three),
    )


def _ints(text: str) -> list[int]:
    return [LETTERS.index(ch) for ch in text]


def _text(seq) -> str:
    return "".join(LETTERS[x] for x in seq)


def _clues(spans) -> tuple[list[int], list[int]]:
    pos, plain = [], []
    for start, word in spans:
        for offset, ch in enumerate(word):
            pos.append(start + offset)
            plain.append(LETTERS.index(ch))
    return pos, plain


def keyword_alphabet(word: str) -> str:
    """KRYPTOS-style mixed alphabet: keyword letters once, then the rest in order."""
    seen = []
    for ch in word.upper() + LETTERS:
        if ch in LETTERS and ch not in seen:
            seen.append(ch)
    return "".join(seen)


# Pure Python cipher, used to plant texts and to check the C kernel.
def encipher(family: str, plain: str, alpha_a: str, alpha_b: str, key: list[int]) -> str:
    """alpha_a, alpha_b are alphabets in rank order; q1 ignores alpha_b, q2 ignores alpha_a."""
    period = len(key)
    out = []
    for i, ch in enumerate(plain):
        k = key[i % period]
        if family == "q1":
            out.append(LETTERS[(alpha_a.index(ch) + k) % 26])
        elif family == "q2":
            out.append(alpha_b[(LETTERS.index(ch) + k) % 26])
        else:
            out.append(alpha_b[(alpha_a.index(ch) + k) % 26])
    return "".join(out)


def decipher(family: str, cipher: str, alpha_a: str, alpha_b: str, key: list[int]) -> str:
    period = len(key)
    out = []
    for i, ch in enumerate(cipher):
        k = key[i % period]
        if family == "q1":
            out.append(alpha_a[(LETTERS.index(ch) - k) % 26])
        elif family == "q2":
            out.append(LETTERS[(alpha_b.index(ch) - k) % 26])
        else:
            out.append(alpha_a[(alpha_b.index(ch) - k) % 26])
    return "".join(out)


def score_key(family: str, cipher: str, alpha_a: str, alpha_b: str, key: list[int], spans=CRIB_SPANS) -> dict:
    """Objective of one supplied key, computed by the C kernel."""
    lib = _kernel()
    q4, p1, p2, p3 = _tables()
    n, period = len(cipher), len(key)
    pos, plain = _clues(spans)
    ct = (ctypes.c_int * n)(*_ints(cipher))
    a = (ctypes.c_int * 26)(*_ints(alpha_a if family != "q2" else LETTERS))
    b_ranks = alpha_b if family != "q1" else LETTERS
    binv = (ctypes.c_int * 26)(*[b_ranks.index(ch) for ch in LETTERS])
    k = (ctypes.c_int * period)(*key)
    out_plain = (ctypes.c_int * n)()
    out = (ctypes.c_double * 3)()
    lib.q_eval(FAMILIES[family], n, ct, period, len(pos), (ctypes.c_int * len(pos))(*pos),
               (ctypes.c_int * len(pos))(*plain), q4, p1, p2, p3, ctypes.c_double(LAMBDA),
               a, binv, k, out_plain, out)
    return {"objective": out[0], "lang": out[1], "violations": int(out[2]), "plaintext": _text(out_plain)}


def _unpack(buf, period: int, n: int) -> dict:
    a = list(buf[0:26])
    binv = list(buf[26:52])
    b = [0] * 26
    for letter, rank in enumerate(binv):
        b[rank] = letter
    return {
        "alpha_a": _text(a),
        "alpha_b": _text(b),
        "key": list(buf[52:52 + period]),
        "plaintext": _text(buf[52 + period:52 + period + n]),
    }


def solve(cipher: str, family: str, period: int = 19, spans=CRIB_SPANS, restarts: int = DEFAULT["restarts"],
          iters: int = DEFAULT["iters"], t0: float = DEFAULT["t0"], t1: float = DEFAULT["t1"], seed: int = 1,
          derive: bool = True, lam: float = LAMBDA, start: tuple[str, str, list[int]] | None = None,
          key_only_start: bool = False, method: str = "anneal", replicas: int = 8, exch: int = 50, pshift: float = 0.1, pheat: float = 0.0, pkey: float = 0.15, plns: float = 0.0, inner: int = 200) -> dict:
    """Blind search. Returns the best-objective state and the best state with every clue letter right."""
    lib = _kernel()
    q4, p1, p2, p3 = _tables()
    n = len(cipher)
    pos, plain = _clues(spans)
    width = 52 + period + n
    best = (ctypes.c_int * width)()
    feas = (ctypes.c_int * width)()
    out = (ctypes.c_double * 6)()
    per = (ctypes.c_double * restarts)()
    if start is not None:
        sa, sb, sk = start
        a_seed = (ctypes.c_int * 26)(*_ints(sa))
        b_seed = (ctypes.c_int * 26)(*[sb.index(ch) for ch in LETTERS])
        k_seed = (ctypes.c_int * period)(*sk)
    else:
        a_seed = b_seed = (ctypes.c_int * 26)(*range(26))
        k_seed = (ctypes.c_int * period)()
    lib.q_set_moves(ctypes.c_double(pshift), ctypes.c_double(pheat), ctypes.c_double(pkey))
    lib.q_set_lns(ctypes.c_double(plns), inner)
    began = time.perf_counter()
    if method == "tempering":
        # iters is the total move budget per restart, shared by the replicas.
        lib.q_tempering(FAMILIES[family], n, (ctypes.c_int * n)(*_ints(cipher)), period, len(pos),
                        (ctypes.c_int * len(pos))(*pos), (ctypes.c_int * len(pos))(*plain), q4, p1, p2, p3,
                        ctypes.c_double(lam), restarts, replicas, ctypes.c_longlong(max(1, iters // replicas)),
                        ctypes.c_double(t0), ctypes.c_double(t1), exch, ctypes.c_ulonglong(seed),
                        best, feas, out, per)
    else:
        lib.q_anneal(FAMILIES[family], n, (ctypes.c_int * n)(*_ints(cipher)), period, len(pos),
                     (ctypes.c_int * len(pos))(*pos), (ctypes.c_int * len(pos))(*plain), q4, p1, p2, p3,
                     ctypes.c_double(lam), int(derive), restarts, ctypes.c_longlong(iters), ctypes.c_double(t0),
                     ctypes.c_double(t1), ctypes.c_ulonglong(seed),
                     0 if start is None else (2 if key_only_start else 1),
                     a_seed, b_seed, k_seed, best, feas, out, per)
    seconds = time.perf_counter() - began
    result = {
        "family": family,
        "period": period,
        "objective": out[0],
        "lang": out[1],
        "violations": int(out[2]),
        "feasible_lang": out[3] if out[3] > -1e299 else None,
        "evaluations": int(out[4]),
        "restarts_at_best": int(out[5]),
        "restarts": restarts,
        "iters": iters,
        "seconds": seconds,
        "method": method,
        "best": _unpack(best, period, n),
        "restart_best": list(per),
    }
    result["feasible"] = _unpack(feas, period, n) if result["feasible_lang"] is not None else None
    return result


def index_of_coincidence(text: str) -> float:
    n = len(text)
    counts = [text.count(ch) for ch in LETTERS]
    return sum(c * (c - 1) for c in counts) / (n * (n - 1)) if n > 1 else 0.0


# Planted texts.
def _heldout_letters() -> str:
    for name in ("neural_heldout_doyle.txt", "neural_audit_wells.txt"):
        path = _DATA / name
        if path.exists():
            body = "".join(line for line in path.read_text(encoding="utf-8").splitlines(True)
                           if not line.startswith("#"))
            yield name, "".join(ch for ch in body.upper() if ch in LETTERS), body


def plant_windows(count: int, n: int = 97, spans=CRIB_SPANS, seed: int = 0) -> list[str]:
    """Disjoint held-out English windows with both clues written in at their K4 positions."""
    windows = []
    for _name, letters, _body in _heldout_letters():
        for start in range(0, len(letters) - n + 1, n):
            windows.append(letters[start:start + n])
    rng = random.Random(seed)
    rng.shuffle(windows)
    out = []
    for w in windows[:count]:
        w = list(w)
        for start, word in spans:
            w[start:start + len(word)] = list(word)
        out.append("".join(w))
    return out


def _keyword_pool() -> list[str]:
    words = set()
    for _name, _letters, body in _heldout_letters():
        for token in body.upper().split():
            token = "".join(ch for ch in token if ch in LETTERS)
            if 6 <= len(token) <= 10:
                words.add(token)
    return sorted(words)


def random_alphabet(kind: str, rng: random.Random, pool: list[str]) -> tuple[str, str]:
    """('random' or 'keyword') alphabet and the keyword used ('' for random)."""
    if kind == "random":
        letters = list(LETTERS)
        rng.shuffle(letters)
        return "".join(letters), ""
    word = rng.choice(pool)
    return keyword_alphabet(word), word


def plant(family: str, plain: str, kind: str, period: int, rng: random.Random, pool: list[str]) -> dict:
    alpha_a, word_a = random_alphabet(kind, rng, pool) if family != "q2" else (LETTERS, "")
    alpha_b, word_b = random_alphabet(kind, rng, pool) if family != "q1" else (LETTERS, "")
    key = [rng.randrange(26) for _ in range(period)]
    cipher = encipher(family, plain, alpha_a, alpha_b, key)
    return {"plain": plain, "cipher": cipher, "alpha_a": alpha_a, "alpha_b": alpha_b, "key": key,
            "keywords": [w for w in (word_a, word_b) if w]}


def power(families=("q1", "q2", "q4"), kinds=("random", "keyword"), texts: int = 10, period: int = 19,
          seed: int = 7, **budget) -> list[dict]:
    """Blind recovery of planted English. One row per planted text."""
    pool = _keyword_pool()
    windows = plant_windows(texts, seed=seed)
    rows = []
    for family in families:
        for kind in kinds:
            rng = random.Random(f"{seed}-{family}-{kind}")
            for t, plain in enumerate(windows):
                p = plant(family, plain, kind, period, rng, pool)
                truth = score_key(family, p["cipher"], p["alpha_a"], p["alpha_b"], p["key"])
                assert truth["plaintext"] == plain and truth["violations"] == 0
                got = solve(p["cipher"], family, period, seed=1000 + t, **budget)
                best = got["feasible"] or got["best"]
                right = sum(a == b for a, b in zip(best["plaintext"], plain))
                rows.append({
                    "family": family, "kind": kind, "text": t, "keywords": p["keywords"],
                    "true_lang": truth["lang"], "found_lang": got["feasible_lang"], "found_objective": got["objective"],
                    "found_violations": got["violations"], "exact": best["plaintext"] == plain,
                    "letters_right": right / len(plain),
                    "beyond_clues_right": (right - 24) / (len(plain) - 24),
                    "restarts_at_best": got["restarts_at_best"], "seconds": got["seconds"],
                })
    return rows


def nulls(families=("q1", "q2", "q4"), count: int = 10, period: int = 19, seed: int = 11, **budget) -> list[dict]:
    """Random ciphertexts and K4 shuffles, clues told to the solver at the K4 positions."""
    rows = []
    for family in families:
        rng = random.Random(f"{seed}-{family}")
        for kind in ("random", "shuffle"):
            for t in range(count):
                if kind == "random":
                    cipher = "".join(rng.choice(LETTERS) for _ in range(len(K4_CIPHERTEXT)))
                else:
                    letters = list(K4_CIPHERTEXT)
                    rng.shuffle(letters)
                    cipher = "".join(letters)
                got = solve(cipher, family, period, seed=2000 + t, **budget)
                rows.append({"family": family, "kind": kind, "text": t, "objective": got["objective"],
                             "lang": got["lang"], "violations": got["violations"],
                             "feasible_lang": got["feasible_lang"], "seconds": got["seconds"],
                             "ioc": index_of_coincidence(got["best"]["plaintext"])})
    return rows


def k4(families=("q1", "q2", "q4"), period: int = 19, seed: int = 3000, **budget) -> dict:
    """K4 under each family. Candidates are unverified; nothing is claimed."""
    rows = []
    for family in families:
        got = solve(K4_CIPHERTEXT, family, period, seed=seed, **budget)
        best = got["feasible"] or got["best"]
        rows.append({
            "family": family, "objective": got["objective"], "lang": got["lang"], "violations": got["violations"],
            "feasible_lang": got["feasible_lang"], "candidate_unverified": best["plaintext"],
            "alpha_a": best["alpha_a"], "alpha_b": best["alpha_b"], "key": best["key"],
            "ioc": index_of_coincidence(best["plaintext"]), "restarts_at_best": got["restarts_at_best"],
            "seconds": got["seconds"],
        })
    return {"solved": False, "claimed_plaintext": None, "period": period, "rows": rows}


def lead_rule(k4_row: dict, null_rows: list[dict], power_rows: list[dict]) -> dict:
    """A K4 row is a lead only if it beats every null run and reaches the planted English range."""
    fam = k4_row["family"]
    k4_score = k4_row["feasible_lang"] if k4_row["feasible_lang"] is not None else -math.inf
    null_best = max(max(r["lang"], r["feasible_lang"] or -math.inf) for r in null_rows if r["family"] == fam)
    planted_low = min(r["true_lang"] for r in power_rows if r["family"] == fam)
    return {"family": fam, "k4": k4_score, "null_max": null_best, "planted_true_min": planted_low,
            "lead": bool(k4_score > null_best and k4_score >= planted_low)}


def main(argv=None) -> int:  # pragma: no cover - long experiment driver
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--texts", type=int, default=10)
    parser.add_argument("--nulls", type=int, default=10)
    parser.add_argument("--period", type=int, default=19)
    parser.add_argument("--restarts", type=int, default=DEFAULT["restarts"])
    parser.add_argument("--iters", type=int, default=DEFAULT["iters"])
    parser.add_argument("--lam", type=float, default=LAMBDA, help="nats per clue letter left wrong")
    parser.add_argument("--families", default="q1,q2,q4")
    parser.add_argument("--kinds", default="random,keyword")
    parser.add_argument("--skip", default="", help="comma list of power,nulls,k4 to skip")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    budget = {"restarts": args.restarts, "iters": args.iters, "lam": args.lam}
    fams = tuple(args.families.split(","))
    skip = set(filter(None, args.skip.split(",")))
    report: dict = {"budget": budget, "period": args.period}
    began = time.perf_counter()
    if "k4" not in skip:
        report["k4"] = k4(fams, args.period, **budget)
        print(json.dumps(report["k4"], indent=1), flush=True)
    if "power" not in skip:
        report["power"] = power(fams, tuple(args.kinds.split(",")), args.texts, args.period, **budget)
        for r in report["power"]:
            print(json.dumps(r), flush=True)
    if "nulls" not in skip:
        report["nulls"] = nulls(fams, args.nulls, args.period, **budget)
        for r in report["nulls"]:
            print(json.dumps(r), flush=True)
    if {"k4", "power", "nulls"} <= set(report):
        report["leads"] = [lead_rule(row, report["nulls"], report["power"]) for row in report["k4"]["rows"]]
    report["seconds"] = time.perf_counter() - began
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
