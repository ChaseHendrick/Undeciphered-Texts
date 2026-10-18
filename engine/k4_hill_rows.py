"""K4 in-place Hill ciphers of size 2 to 4: every decryption row, exhaustively.

A Hill cipher deciphers each block of n letters as p = M c mod 26. Row j
of M must send every ciphertext block whose plaintext is known to that
block's j-th plaintext letter. With 26^n candidate rows the check is
exhaustive, so no key is sampled. Blocks may start at any of the n
alignments, and letters may be numbered A-Z or by the KRYPTOS, PALIMPSEST
or ABSCISSA keyed alphabets. Only the two published clues are used; there
is no language model, so the result holds whatever language K4 is in.

A size and alignment is excluded when some row has no candidate, or when
no choice of rows gives a matrix invertible mod 26. Otherwise the fit
fold fits one clue and counts reserved letters forced right or wrong.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.solvers.k4_attempt import K4_CIPHERTEXT

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SIZES = (2, 3, 4)
MAX_COMBINATIONS = 200000


def keyed(keyword: str) -> str:
    seen = []
    for letter in keyword + LETTERS:
        if letter not in seen:
            seen.append(letter)
    return "".join(seen)


NUMBERINGS = {
    "A-Z": LETTERS,
    "KRYPTOS": keyed("KRYPTOS"),
    "PALIMPSEST": keyed("PALIMPSEST"),
    "ABSCISSA": keyed("ABSCISSA"),
}

_ROWS: dict[int, np.ndarray] = {}


def _all_rows(n: int) -> np.ndarray:
    if n not in _ROWS:
        grids = np.indices((26,) * n, dtype=np.int16).reshape(n, -1).T
        _ROWS[n] = grids
    return _ROWS[n]


def known_blocks(n: int, alignment: int, spans, ciphertext: str, alphabet: str):
    """(block start, cipher vector, plain vector) for blocks wholly inside a clue."""
    blocks = []
    for start, word in spans:
        end = start + len(word)
        first = start + ((alignment - start) % n)
        for b in range(first, end - n + 1, n):
            c = [alphabet.index(ch) for ch in ciphertext[b : b + n]]
            p = [alphabet.index(word[b - start + k]) for k in range(n)]
            blocks.append((b, np.array(c, dtype=np.int64), p))
    return blocks


def row_candidates(n: int, blocks) -> list[np.ndarray]:
    """For each row j, every vector r with r . c = p[j] mod 26 on all blocks."""
    rows = _all_rows(n).astype(np.int64)
    keep = [np.ones(len(rows), dtype=bool) for _ in range(n)]
    for _b, c, p in blocks:
        values = (rows @ c) % 26
        for j in range(n):
            keep[j] &= values == p[j]
    return [rows[mask] for mask in keep]


def _invertible(matrix: np.ndarray) -> bool:
    det = round(np.linalg.det(matrix.astype(float))) % 26
    return math.gcd(int(det), 26) == 1


def _some_invertible(candidates) -> bool | None:
    """True if a choice of rows is invertible mod 26; None if too many to try."""
    total = math.prod(len(c) for c in candidates)
    if total == 0:
        return False
    if total > MAX_COMBINATIONS:
        # Too many to list: a sampled invertible choice still proves "sat".
        rng = random.Random(0)
        for _ in range(MAX_COMBINATIONS):
            choice = [c[rng.randrange(len(c))] for c in candidates]
            if _invertible(np.array(choice)):
                return True
        return None
    for choice in itertools.product(*candidates):
        if _invertible(np.array(choice)):
            return True
    return False


def check(n: int, alignment: int, numbering: str = "A-Z", ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS) -> dict:
    alphabet = NUMBERINGS[numbering]
    blocks = known_blocks(n, alignment, spans, ciphertext, alphabet)
    candidates = row_candidates(n, blocks)
    counts = [len(c) for c in candidates]
    invertible = _some_invertible(candidates)
    status = "unsat" if invertible is False else ("sat" if invertible else "unknown")
    return {"size": n, "alignment": alignment, "numbering": numbering, "blocks": len(blocks),
            "row_counts": counts, "status": status}


def held_back(n: int, alignment: int, numbering: str = "A-Z", ciphertext: str = K4_CIPHERTEXT,
              fit=CRIB_SPANS[0], reserve=CRIB_SPANS[1]) -> dict:
    """Fit rows on one clue; a reserved letter is forced when every fitted row agrees on it."""
    alphabet = NUMBERINGS[numbering]
    candidates = row_candidates(n, known_blocks(n, alignment, (fit,), ciphertext, alphabet))
    right = wrong = 0
    start, word = reserve
    end = start + len(word)
    for i in range(start, end):
        block = i - ((i - alignment) % n)
        if block < 0 or block + n > len(ciphertext) or not len(candidates[i - block]):
            continue
        c = np.array([alphabet.index(ch) for ch in ciphertext[block : block + n]], dtype=np.int64)
        predicted = set(((candidates[i - block] @ c) % 26).tolist())
        if len(predicted) == 1:
            if alphabet[predicted.pop()] == word[i - start]:
                right += 1
            else:
                wrong += 1
    return {"fit_rows": [len(c) for c in candidates], "right": right, "wrong": wrong,
            "free": len(word) - right - wrong}


def planted(n: int, alignment: int, seed: int, numbering: str = "A-Z", spans=CRIB_SPANS) -> str:
    """Both clues planted in random text under a random invertible Hill key."""
    rng = random.Random(seed)
    alphabet = NUMBERINGS[numbering]
    plain = [rng.choice(LETTERS) for _ in range(97)]
    for start, word in spans:
        plain[start : start + len(word)] = word
    while True:
        m = np.array([[rng.randrange(26) for _ in range(n)] for _ in range(n)])
        if _invertible(m):
            break
    out = list(plain)
    # Encryption is the inverse of p = M c; solve each block by trying rows is
    # wasteful, so invert M mod 26 through the adjugate.
    det = int(round(np.linalg.det(m.astype(float)))) % 26
    adj = np.round(np.linalg.inv(m.astype(float)) * np.linalg.det(m.astype(float))).astype(np.int64)
    inverse = (pow(det, -1, 26) * adj) % 26
    for b in range(alignment, 97 - n + 1, n):
        p = np.array([alphabet.index(ch) for ch in plain[b : b + n]], dtype=np.int64)
        c = (inverse @ p) % 26
        out[b : b + n] = [alphabet[v] for v in c]
    return "".join(out)


def scan(ciphertext: str = K4_CIPHERTEXT) -> dict:
    rows = []
    for numbering in NUMBERINGS:
        for n in SIZES:
            for alignment in range(n):
                result = check(n, alignment, numbering, ciphertext)
                if result["status"] != "unsat":
                    result["fold_east"] = held_back(n, alignment, numbering, ciphertext, CRIB_SPANS[0], CRIB_SPANS[1])
                    result["fold_berlin"] = held_back(n, alignment, numbering, ciphertext, CRIB_SPANS[1], CRIB_SPANS[0])
                rows.append(result)
    return {
        "model": "in-place Hill, sizes 2 to 4, every alignment, four letter numberings, clues only",
        "rows": rows,
        "solved": False,
        "claimed_plaintext": None,
    }


if __name__ == "__main__":
    for row in scan()["rows"]:
        print(row)
