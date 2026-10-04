"""Joint two-square climbs on the even Truppenschlüssel windows.

The scorer is a trigram count from the Grimm excerpt, not military German.
A score above a shuffled control is not a reading. solved stays false.
Odd bodies are not padded. A dropped endpoint is one letter, not a guess.
"""

from __future__ import annotations

import random
from collections import Counter
from functools import lru_cache

from engine.ciphers import TWO_SQUARE_ALPHABET
from engine.german import german_letters, load_training_prose
from engine.solvers.two_square import _hill_pass, _kick
from engine.ts_close_pairs import (
    DEZPS_KNOWN,
    DSZPZ,
    HOHOX,
    IASRZ_129,
    IASRZ_130,
    SSKFV,
)

RESTARTS = 4
KICKS = 6
SEED = 20261004


@lru_cache(maxsize=1)
def german_trigram_table() -> tuple[int, ...]:
    """Raw trigram counts from the folded Grimm excerpt. Index is base 26."""
    letters = german_letters(load_training_prose())
    counts: Counter[str] = Counter()
    for index in range(len(letters) - 2):
        counts[letters[index : index + 3]] += 1
    table = [0] * (26**3)
    for gram, count in counts.items():
        a, b, c = (ord(ch) - 65 for ch in gram)
        table[(a * 26 + b) * 26 + c] = count
    return tuple(table)


def _cells(text: str) -> list[int]:
    return [ord(ch) - 65 for ch in text]


def _climb(text: str, *, seed: int) -> int:
    if len(text) < 8 or len(text) % 2:
        raise ValueError("joint ciphertext must be even and at least 8 letters")
    table = german_trigram_table()
    ct = _cells(text)
    alphabet = [ord(ch) - 65 for ch in TWO_SQUARE_ALPHABET]
    rng = random.Random(seed)
    best = -1
    for _restart in range(RESTARTS):
        left = alphabet[:]
        right = alphabet[:]
        rng.shuffle(left)
        rng.shuffle(right)
        kick_n = 1
        local = -1
        for _kick_index in range(KICKS):
            score = _hill_pass(ct, left, right, table)
            if score > local:
                local = score
                kick_n = 1
            _kick(left, right, rng, kick_n)
            kick_n = min(10, kick_n + 1)
        if local > best:
            best = local
    return best


def _shuffle(text: str, seed: int) -> str:
    chars = list(text)
    random.Random(seed).shuffle(chars)
    return "".join(chars)


def _lane(name: str, left: str, right: str) -> dict:
    if len(left) % 2 or len(right) % 2:
        raise ValueError(f"{name} is not an even window")
    joint = left + right
    real = _climb(joint, seed=SEED)
    null = _climb(_shuffle(joint, SEED), seed=SEED)
    return {
        "name": name,
        "lengths": (len(left), len(right)),
        "real_score": real,
        "null_score": null,
        "beat_null": real > null,
    }


def search_ts_pair_climb() -> dict:
    """Climb the declared even windows. Return scores only, not plaintext."""
    iasrz_129 = IASRZ_129[5:]
    iasrz_130 = IASRZ_130[5:]
    dszpz = DSZPZ[5:]
    dezps = DEZPS_KNOWN[5:]
    lanes = (
        _lane("iasrz_designator_included", IASRZ_129, IASRZ_130),
        _lane("iasrz_drop_first", iasrz_129[1:], iasrz_130[1:]),
        _lane("iasrz_drop_last", iasrz_129[:-1], iasrz_130[:-1]),
        _lane("ending_drop_first", SSKFV, HOHOX[1:]),
        _lane("ending_drop_last", SSKFV, HOHOX[:-1]),
        _lane("time_1735_drop_first", dszpz[1:], dezps[1:]),
        _lane("time_1735_drop_last", dszpz[:-1], dezps[:-1]),
    )
    return {
        "claimed_plaintext": None,
        "solved": False,
        "restarts": RESTARTS,
        "kicks": KICKS,
        "seed": SEED,
        "scorer": "grimm_excerpt_trigram_counts",
        "lanes": lanes,
        "lanes_beating_null": sum(1 for lane in lanes if lane["beat_null"]),
        "scope": "Local climbs against one shuffled control. A higher score is not German plaintext and not a key.",
    }
