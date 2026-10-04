"""The best word score over every period-4 shift. Not a reading.

The earlier search kept the key with the friendliest counts and only then
asked for a word score. This one scores every key with the quadgram model
and keeps the best. Shuffled cells get the same search. No letter string
is stored.
"""

from __future__ import annotations

import random
from functools import lru_cache

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells, _phases
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004
_NULL = 8
_KEYS = 25 ** 4


def _best_quad(seq: list[int], logp: list[float], english: list[int]) -> float:
    count = len(seq)
    decrypted = [[0] * count for _ in range(25)]
    for shift in range(25):
        shift_row, shift_column = divmod(shift, 5)
        landed = decrypted[shift]
        for index, cell in enumerate(seq):
            row, column = divmod(cell, 5)
            landed[index] = ((row - shift_row) % 5) * 5 + (column - shift_column) % 5
    first_set, second_set, third_set, fourth_set = _phases(seq, 4)
    best = float("-inf")
    mapping = [0] * 25
    plain = [0] * count
    for i, first in enumerate(first_set):
        for j, second in enumerate(second_set):
            partial = [first[bin_] + second[bin_] for bin_ in range(25)]
            for k, third in enumerate(third_set):
                partial_three = [partial[bin_] + third[bin_] for bin_ in range(25)]
                stream_i = decrypted[i]
                stream_j = decrypted[j]
                stream_k = decrypted[k]
                for n, fourth in enumerate(fourth_set):
                    counts = [partial_three[bin_] + fourth[bin_] for bin_ in range(25)]
                    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
                    rank = 0
                    for cell in order:
                        if counts[cell] == 0:
                            continue
                        mapping[cell] = english[rank]
                        rank += 1
                    stream_n = decrypted[n]
                    for index in range(count):
                        which = index & 3
                        if which == 0:
                            plain[index] = mapping[stream_i[index]]
                        elif which == 1:
                            plain[index] = mapping[stream_j[index]]
                        elif which == 2:
                            plain[index] = mapping[stream_k[index]]
                        else:
                            plain[index] = mapping[stream_n[index]]
                    left, mid, right = plain[0], plain[1], plain[2]
                    total = 0.0
                    for index in range(3, count):
                        nxt = plain[index]
                        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
                        left, mid, right = mid, right, nxt
                    score = total / (count - 3)
                    if score > best:
                        best = score
    return best


@lru_cache(maxsize=1)
def word_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    best = _best_quad(cells, logp, english)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        if _best_quad(shuffled, logp, english) >= best:
            as_high += 1
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "keys": _KEYS,
        "null_texts": _NULL,
        "trials": _KEYS * (1 + _NULL),
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "shuffles_as_high": as_high,
        "scope": (
            "The best word score over every period-4 shift is still a score. "
            "Shuffled cells get the same search. No letter string is stored."
        ),
    }
