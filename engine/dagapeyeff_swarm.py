"""Bounded checks on the 1939 D'Agapeyeff challenge. Not a reading.

The digits are the challenge on the last page of the first edition of
Codes and Ciphers. The letter block is the Polybius exercise earlier in
the same book, whose plaintext the publisher of the transcription already
prints. Transposition cannot repair a letter-count mismatch, so the
frequency test is the whole of the English question this swarm can settle.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.language import UNIGRAM

# Wikipedia, D'Agapeyeff cipher, the block printed from the 1939 book.
# https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher
CHALLENGE = """
75628 28591 62916 48164 91748 58464 74748 28483 81638 18174
74826 26475 83828 49175 74658 37575 75936 36565 81638 17585
75756 46282 92857 46382 75748 38165 81848 56485 64858 56382
72628 36281 81728 16463 75828 16483 63828 58163 63630 47481
91918 46385 84656 48565 62946 26285 91859 17491 72756 46575
71658 36264 74818 28462 82649 18193 65626 48484 91838 57491
81657 27483 83858 28364 62726 26562 83759 27263 82827 27283
82858 47582 81837 28462 82837 58164 75748 58162 92000
"""

# Same page: the book's own worked Polybius example, letters rather than digits.
CONTROL = """
CDDBC ECBCE BBEBD ABCCB BDBAB CCDCD BCDDE CAECB DDDAA CABCE
AABDE BCEDC BCCDA EBDCB AAEAB ECDDB DCCEC EEABD ADEAD CAADE
ACABD CBDCB AABDC ACEDC BABCD DCDBD DCBEB CDCBE BCAAB DACCD
DBBBC EAACD BDCDD BCEDC AECAC EDC
"""

_ROW = set("67890")
_COLUMN = set("12345")
_SHUFFLES = 200
_SEED = 20261004

# 25-letter English: published A-Z rates with I and J added together, then scaled.
_MERGED = []
for index, rate in enumerate(UNIGRAM):
    if index == 9:
        continue
    if index == 8:
        _MERGED.append(rate + UNIGRAM[9])
    else:
        _MERGED.append(rate)
_SCALE = sum(_MERGED)
ENGLISH_25 = tuple(rate / _SCALE for rate in _MERGED)


def _digits(text: str) -> str:
    return "".join(char for char in text if char.isdigit())


def _pairs(text: str, alphabet: str) -> tuple[str, ...]:
    stream = "".join(char for char in text.upper() if char in alphabet)
    if len(stream) % 2:
        raise ValueError("pair stream must be even")
    return tuple(stream[index:index + 2] for index in range(0, len(stream), 2))


def challenge_pairs() -> tuple[str, ...]:
    """Drop the printed terminal 000. Every remaining pair is one Polybius cell."""
    digits = _digits(CHALLENGE)
    if not digits.endswith("000"):
        raise ValueError("the printed challenge is expected to end in the filler 000")
    digits = digits[:-3]
    pairs = _pairs(digits, "0123456789")
    for pair in pairs:
        if pair[0] not in _ROW or pair[1] not in _COLUMN:
            raise ValueError(f"pair {pair} is outside the 5 by 5 digit square")
    return pairs


def best_chi_square(pairs: tuple[str, ...]) -> float:
    """Chi-square after the cell counts are matched to English as well as counts allow.

    Sorting both lists is optimal because the score depends on the counts
    only through sum of count-squared over probability. A transposition
    does not change those counts, so it cannot improve this number.
    """
    counts = sorted(Counter(pairs).values(), reverse=True)
    width = len(ENGLISH_25)
    if len(counts) > width:
        raise ValueError("more cells than a 5 by 5 square")
    counts = counts + [0] * (width - len(counts))
    rates = sorted(ENGLISH_25, reverse=True)
    total = sum(counts)
    score = 0.0
    for count, rate in zip(counts, rates):
        expected = total * rate
        score += (count - expected) ** 2 / expected
    return score


def digram_excess(pairs: tuple[str, ...]) -> int:
    """How many adjacent cell pairs are copies of an earlier one."""
    if len(pairs) < 2:
        return 0
    counts = Counter(pairs[index] + pairs[index + 1] for index in range(len(pairs) - 1))
    return sum(count - 1 for count in counts.values())


def search_dagapeyeff() -> dict:
    """Compare the challenge with the book's own example. Claim no plaintext."""
    challenge = challenge_pairs()
    control = _pairs(CONTROL, "ABCDE")
    challenge_chi = best_chi_square(challenge)
    control_chi = best_chi_square(control)
    observed = digram_excess(challenge)
    drawn = random.Random(_SEED)
    shuffle_excess = []
    symbols = list(challenge)
    for _ in range(_SHUFFLES):
        drawn.shuffle(symbols)
        shuffle_excess.append(digram_excess(tuple(symbols)))
    mean = sum(shuffle_excess) / len(shuffle_excess)
    variance = sum((item - mean) ** 2 for item in shuffle_excess) / len(shuffle_excess)
    z_score = 0.0 if variance == 0 else (observed - mean) / variance ** 0.5
    return {
        "claimed_plaintext": None,
        "solved": False,
        "challenge_pairs": len(challenge),
        "distinct_cells": len(set(challenge)),
        "grid": f"{int(len(challenge) ** 0.5)} by {int(len(challenge) ** 0.5)}"
        if int(len(challenge) ** 0.5) ** 2 == len(challenge) else "not a square grid",
        "challenge_chi_square": round(challenge_chi, 2),
        "control_chi_square": round(control_chi, 2),
        "challenge_closer_to_english": challenge_chi < control_chi,
        "digram_excess": observed,
        "shuffle_mean_excess": round(mean, 2),
        "digram_z": round(z_score, 2),
        "shuffles": _SHUFFLES,
        "scope": (
            "No letter assignment and no transposition of these cells matches "
            "English as well as the book's own example. A second cipher, or an "
            "error in the encipherment, is not ruled out. No plaintext is claimed."
        ),
    }
