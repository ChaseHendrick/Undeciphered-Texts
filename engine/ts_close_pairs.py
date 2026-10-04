"""Measure the three closest Truppenschlüssel pairs. Do not decipher them.

The letters are the public groups on the CryptoCellar failure page, updated
27 July 2026. The designator is included in the full string and removed for
the body. A dash is an unknown slot, not a guessed letter. solved stays false.
"""

from __future__ import annotations

import random

SOURCE = "https://cryptocellar.org/bgac/g-army-ts-messages.html"
# Cipher alphabet omits J, matching the two-square solver.
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# 8 July 1941, Nr. 129 and Nr. 130, same station and same designator.
IASRZ_129 = (
    "IASRZEDSTBYQSXIAMMTPMNDEYTZNFGETXFMCAMTGZLZNLGZLZQQLIACLTDMM"
    "OFCZSLOFCPSLIAHWAUESMNNGYASSRN"
)
IASRZ_130 = "IASRZEDSTBUYPXVCWFPRMZRPMZNORUOZMNOMXYRANXNYNNBGWFIS"

# 4 July 1941, Nr. 96 and Nr. 97, both headed 1735. Nr. 97 prints RQMX-.
DSZPZ = "DSZPZRQMYQFWMTQMTHYQZWMTQMTUYRZGZHVLPZUCXYZWLVAAQIFIPFYRZOZHVL"
DEZPS_KNOWN = "DEZPSRQMXQSWMTQYTUYZWMTOTUYRZOZHVLAAQIZWPFPZUCFYMFLGZOZHVL"
DEZPS_GAP_AT = 9  # zero-based index of the printed dash, in the full string

# 6 July 1941, Nr. 109 and Nr. 110, same station, sixteen minutes apart.
SSKFV = "SSKFVEGDOKGDSPGDZNFDCTTRRAKWTTGVKDBVDSLQXBYEXBTRFZRYLMOTIYIZ"
HOHOX = "HOHOXWSWGGMSHYLHNOANGTVVTPNZPFZKEROQNXRROQMXSRGLMOTIYIZ"


def common_prefix(left: str, right: str) -> str:
    count = 0
    while count < len(left) and count < len(right) and left[count] == right[count]:
        count += 1
    return left[:count]


def common_suffix(left: str, right: str) -> str:
    count = 0
    while count < len(left) and count < len(right) and left[-1 - count] == right[-1 - count]:
        count += 1
    return left[-count:] if count else ""


def alignment_matches(left: str, right: str) -> int:
    """How many letters a Needleman-Wunsch alignment keeps equal.

    Match 2, mismatch -1, gap -2. The score is not a plaintext score.
    """
    n, m = len(left), len(right)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = -2 * i
        move[i][0] = 1
    for j in range(1, m + 1):
        score[0][j] = -2 * j
        move[0][j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            step = 2 if left[i - 1] == right[j - 1] else -1
            options = (
                (score[i - 1][j - 1] + step, 0),
                (score[i - 1][j] - 2, 1),
                (score[i][j - 1] - 2, 2),
            )
            score[i][j], move[i][j] = max(options)
    i, j = n, m
    hits = 0
    while i or j:
        step = move[i][j]
        if step == 0:
            if left[i - 1] == right[j - 1]:
                hits += 1
            i -= 1
            j -= 1
        elif step == 1:
            i -= 1
        else:
            j -= 1
    return hits


def _body(text: str, designator: str) -> str:
    if not text.startswith(designator):
        raise ValueError("designator is not the start of the printed groups")
    return text[len(designator):]


def null_alignment_max(text: str, length: int, *, draws: int, seed: int) -> int:
    """Best alignment score of `text` against random J-free strings."""
    rng = random.Random(seed)
    best = 0
    for _ in range(draws):
        fake = "".join(rng.choice(ALPHABET) for _ in range(length))
        best = max(best, alignment_matches(text, fake))
    return best


def search_ts_close_pairs() -> dict:
    """Report the three pair measurements. No square is searched."""
    iasrz_body_129 = _body(IASRZ_129, "IASRZ")
    iasrz_body_130 = _body(IASRZ_130, "IASRZ")
    dszpz_body = _body(DSZPZ, "DSZPZ")
    dezps_body = _body(DEZPS_KNOWN, "DEZPS")
    real_hits = alignment_matches(dszpz_body, dezps_body)
    overlap = min(len(dszpz_body), len(dezps_body))
    exact = sum(a == b for a, b in zip(dszpz_body, dezps_body))
    null_hits = null_alignment_max(dszpz_body, len(dezps_body), draws=20, seed=20261004)
    return {
        "claimed_plaintext": None,
        "solved": False,
        "source": SOURCE,
        "iasrz": {
            "full_lengths": (len(IASRZ_129), len(IASRZ_130)),
            "shared_prefix": common_prefix(IASRZ_129, IASRZ_130),
            "body_lengths": (len(iasrz_body_129), len(iasrz_body_130)),
            "body_prefix": common_prefix(iasrz_body_129, iasrz_body_130),
            "bodies_even": len(iasrz_body_129) % 2 == 0 and len(iasrz_body_130) % 2 == 0,
        },
        "same_time": {
            "known_body_lengths": (len(dszpz_body), len(dezps_body)),
            "dash_index_in_full_string": DEZPS_GAP_AT,
            "ungapped_matches": exact,
            "ungapped_compared": overlap,
            "alignment_matches": real_hits,
            "null_max_matches": null_hits,
            "above_null": real_hits > null_hits,
        },
        "shared_ending": {
            "printed_lengths": (len(SSKFV), len(HOHOX)),
            "form_lengths": (60, 50),
            "shared_suffix": common_suffix(SSKFV, HOHOX),
        },
        "scope": "Letter agreement only. No two-square key was tried and no plaintext is claimed. Odd bodies are not padded.",
    }
