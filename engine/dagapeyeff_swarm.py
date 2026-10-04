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
_DRAWS = 2000
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


def english_calibration(draws: int = _DRAWS) -> dict:
    """Same-length English. Chi-square grows with length, so 89 cells are not the control."""
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    if len(alphabet) != len(ENGLISH_25):
        raise RuntimeError("25-letter alphabet and rates disagree")
    drawn = random.Random(_SEED)
    chis = []
    distincts = []
    challenge_chi = best_chi_square(challenge_pairs())
    challenge_distinct = len(set(challenge_pairs()))
    for _ in range(draws):
        sample = tuple(drawn.choices(alphabet, weights=ENGLISH_25, k=196))
        chis.append(best_chi_square(sample))
        distincts.append(len(set(sample)))
    ordered = sorted(chis)
    return {
        "draws": draws,
        "chi_median": round(ordered[draws // 2], 2),
        "chi_max": round(ordered[-1], 2),
        "flatter_than_challenge": sum(1 for score in chis if score >= challenge_chi),
        "min_distinct": min(distincts),
        "as_narrow_as_challenge": sum(1 for count in distincts if count <= challenge_distinct),
    }


def edits_to_look_english(calibration: dict) -> dict:
    """Greedy cell changes until the counts sit inside the same-length English range.

    The forged cells are not returned. A frequency repair is not a plaintext.
    """
    cells = [row + column for row in "67890" for column in "12345"]
    current = list(challenge_pairs())
    ceiling = calibration["chi_max"]
    median = calibration["chi_median"]
    reached = {"inside_sample_max": None, "at_or_below_median": None, "one_edit_chi_square": None}
    for step in range(1, len(current) + 1):
        best = None
        for index, old in enumerate(current):
            for cell in cells:
                if cell == old:
                    continue
                current[index] = cell
                score = best_chi_square(tuple(current))
                if best is None or score < best[0]:
                    best = (score, index, cell)
            current[index] = old
        score, index, cell = best
        current[index] = cell
        if step == 1:
            reached["one_edit_chi_square"] = round(score, 2)
        if reached["inside_sample_max"] is None and score <= ceiling:
            reached["inside_sample_max"] = step
        if reached["at_or_below_median"] is None and score <= median:
            reached["at_or_below_median"] = step
            break
    return reached


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
    calibration = english_calibration()
    repairs = edits_to_look_english(calibration)
    return {
        "claimed_plaintext": None,
        "solved": False,
        "challenge_pairs": len(challenge),
        "control_pairs": len(control),
        "distinct_cells": len(set(challenge)),
        "grid": f"{int(len(challenge) ** 0.5)} by {int(len(challenge) ** 0.5)}"
        if int(len(challenge) ** 0.5) ** 2 == len(challenge) else "not a square grid",
        "challenge_chi_square": round(challenge_chi, 2),
        "control_chi_square": round(control_chi, 2),
        "challenge_closer_to_english": challenge_chi < control_chi,
        "english_draws": calibration["draws"],
        "english_chi_median": calibration["chi_median"],
        "english_chi_max": calibration["chi_max"],
        "flatter_than_challenge": calibration["flatter_than_challenge"],
        "english_min_distinct": calibration["min_distinct"],
        "as_narrow_as_challenge": calibration["as_narrow_as_challenge"],
        "one_edit_chi_square": repairs["one_edit_chi_square"],
        "edits_to_enter_sample": repairs["inside_sample_max"],
        "edits_to_median": repairs["at_or_below_median"],
        "digram_excess": observed,
        "shuffle_mean_excess": round(mean, 2),
        "digram_z": round(z_score, 2),
        "shuffles": _SHUFFLES,
        "scope": (
            "Same-length English is the control that counts. The book's example "
            "is shorter, so its chi-square is only a direction. Changing a cell "
            "to improve the count is not a reading. No plaintext is claimed."
        ),
    }
