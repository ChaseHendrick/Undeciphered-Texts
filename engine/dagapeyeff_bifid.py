"""Undo a bifid on the coordinate stream. Not a reading.

Each cell is already a row digit and a column digit. A bifid of period p
reads those digits in blocks, takes the first half of a block as rows and
the second half as columns, and pairs them again. Every period from 1 to
196 is scored with the solver's quadgram model after the frequency labeling.
The best period is kept only as a number. The cells are not.
"""

from __future__ import annotations

import random
from engine.dagapeyeff_cache import frozen

from engine.dagapeyeff_life import _assign
from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_swarm import challenge_pairs
from engine.language import get_model

_DRAWS = 2000
_SEED = 20261004
_ROW = "67890"
_COL = "12345"


def _digits(pairs: list[str]) -> list[int]:
    out: list[int] = []
    for pair in pairs:
        out.append(_ROW.index(pair[0]))
        out.append(_COL.index(pair[1]))
    return out


def undo_bifid(pairs: list[str], period: int) -> list[str]:
    digits = _digits(pairs)
    out: list[str] = []
    count = len(pairs)
    for start in range(0, count, period):
        block = min(period, count - start)
        chunk = digits[2 * start : 2 * start + 2 * block]
        for row, column in zip(chunk[:block], chunk[block:]):
            out.append(_ROW[row] + _COL[column])
    return out


def _quad(pairs: list[str], logp: list[float]) -> float:
    letters = _assign(tuple(pairs))
    a = ord(letters[0]) - 65
    b = ord(letters[1]) - 65
    c = ord(letters[2]) - 65
    total = 0.0
    for char in letters[3:]:
        d = ord(char) - 65
        total += logp[((a * 26 + b) * 26 + c) * 26 + d]
        a, b, c = b, c, d
    return total / (len(letters) - 3)


def _best(pairs: list[str], logp: list[float]) -> tuple[float, int]:
    best_score = None
    best_period = 1
    for period in range(1, len(pairs) + 1):
        score = _quad(undo_bifid(pairs, period), logp)
        if best_score is None or score > best_score:
            best_score = score
            best_period = period
    return best_score, best_period


@frozen("bifid")
def bifid_report() -> dict:
    model = get_model()
    logp = model.logp
    pairs = list(challenge_pairs())
    identity = _quad(undo_bifid(pairs, 1), logp)
    best_score, best_period = _best(pairs, logp)
    english_letters = _prose("english.txt", len(pairs))
    seq = [ord(char) - 65 for char in english_letters]
    total = 0.0
    a, b, c = seq[0], seq[1], seq[2]
    for d in seq[3:]:
        total += logp[((a * 26 + b) * 26 + c) * 26 + d]
        a, b, c = b, c, d
    english = total / (len(seq) - 3)
    drawn = random.Random(_SEED)
    sample = pairs[:]
    as_high = 0
    for _ in range(_DRAWS):
        drawn.shuffle(sample)
        if _best(sample, logp)[0] >= best_score:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "periods": len(pairs),
        "draws": _DRAWS,
        "period_scores": len(pairs) * _DRAWS,
        "identity_quad": round(identity, 4),
        "best_quad": round(best_score, 4),
        "best_period": best_period,
        "english_quad": round(english, 4),
        "reaches_english": best_score >= english,
        "shuffles_as_high": as_high,
        "scope": (
            "The best period is a number, not a text. "
            "A shuffle whose best period scores as high is not a reading. "
            "No letter string is stored."
        ),
    }
