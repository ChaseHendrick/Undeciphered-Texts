"""What the 1939 digits do before any language is chosen. Not a reading.

No letter table is used. The only question is whether the digits already
separate into two groups, and whether one pair predicts the next. Both are
checked against shuffles of the same digits. No letter string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter

from engine.dagapeyeff_swarm import CHALLENGE, _digits

_SEED = 20261004
_DRAWS = 20000


def _stream() -> str:
    return _digits(CHALLENGE)


def _split(stream: str) -> tuple[set[str], set[str]]:
    return set(stream[0::2]), set(stream[1::2])


def _violations(stream: str, even: set[str], odd: set[str]) -> int:
    bad = 0
    for index, char in enumerate(stream):
        if index % 2 == 0 and char not in even:
            bad += 1
        elif index % 2 == 1 and char not in odd:
            bad += 1
    return bad


def _mutual(seq: list[str]) -> float:
    count = len(seq) - 1
    joint = Counter(zip(seq, seq[1:]))
    left = Counter(seq[:-1])
    right = Counter(seq[1:])
    score = 0.0
    for (first, second), seen in joint.items():
        share = seen / count
        score += share * math.log(share / ((left[first] / count) * (right[second] / count)))
    return score


def frame_report() -> dict:
    stream = _stream()
    even, odd = _split(stream)
    overlap = even & odd
    # The odd alphabet without the overlap is what the other phase would be
    # if that one digit were not sitting on the wrong side. Derived, not supplied.
    odd_only = odd - overlap
    bad_at = [
        index for index, char in enumerate(stream)
        if (index % 2 == 0 and char not in even) or (index % 2 == 1 and char not in odd_only)
    ]
    zeros = [index for index, char in enumerate(stream) if char == "0"]
    # A bad odd index is the second digit of a pair. Keep only the pairs before it.
    if len(bad_at) == 1 and bad_at[0] % 2 == 1:
        prefix = stream[:bad_at[0] - 1]
    else:
        prefix = stream[:len(stream) - (len(stream) % 2)]
    pairs = [prefix[index:index + 2] for index in range(0, len(prefix), 2)]
    observed_mi = _mutual(pairs)
    drawn = random.Random(_SEED)
    as_clean = 0
    for _ in range(_DRAWS):
        shuffled = list(stream)
        drawn.shuffle(shuffled)
        if _violations("".join(shuffled), even, odd_only) <= len(bad_at):
            as_clean += 1
    drawn = random.Random(_SEED)
    as_tied = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _mutual(shuffled) >= observed_mi - 1e-15:
            as_tied += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "digits": len(stream),
        "even_alphabet": "".join(sorted(even)),
        "odd_alphabet_without_overlap": "".join(sorted(odd_only)),
        "overlap": "".join(sorted(overlap)),
        "bad_indexes": tuple(bad_at),
        "zero_indexes": tuple(zeros),
        "legal_pairs": len(pairs),
        "draws": _DRAWS,
        "trials": _DRAWS * 2,
        "shuffles_as_clean": as_clean,
        "mutual_information": round(observed_mi, 4),
        "shuffles_as_predictable": as_tied,
        "scope": (
            "The two alphabets are whatever digits occupy the even and odd places. "
            "Nothing is called a letter, and the last zeros are not declared filler in advance. "
            "No letter string is stored."
        ),
    }
