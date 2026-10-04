"""Habits and copying errors on the Truppenschlüssel residue.

The senders were clerks at a radio desk. This module records repeated
openings, a shared closing, the 1735 differences, and what happens if one
five-letter group is dropped from HOHOX. It does not search a square.
solved stays false.
"""

from __future__ import annotations

from engine.ts_bigram_phase import extra_repeats, random_at_least
from engine.ts_close_pairs import (
    DEZPS_KNOWN,
    DSZPZ,
    HOHOX,
    IASRZ_129,
    IASRZ_130,
    SSKFV,
)


def _columns(left: str, right: str) -> tuple[str, str]:
    """Needleman-Wunsch columns. Same penalties as the pair measurement."""
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
    out_left: list[str] = []
    out_right: list[str] = []
    while i or j:
        step = move[i][j]
        if step == 0:
            out_left.append(left[i - 1])
            out_right.append(right[j - 1])
            i -= 1
            j -= 1
        elif step == 1:
            out_left.append(left[i - 1])
            out_right.append("-")
            i -= 1
        else:
            out_left.append("-")
            out_right.append(right[j - 1])
            j -= 1
    return "".join(reversed(out_left)), "".join(reversed(out_right))


def hearing_tally() -> dict:
    """Classify the 1735 alignment. A second copy would be mostly matches."""
    left, right = _columns(DSZPZ[5:], DEZPS_KNOWN[5:])
    same = substituted = gaps = 0
    for a, b in zip(left, right):
        if a == "-" or b == "-":
            gaps += 1
        elif a == b:
            same += 1
        else:
            substituted += 1
    opening = sum(a == b for a, b in zip(DSZPZ[5:15], DEZPS_KNOWN[5:15]))
    return {
        "same": same,
        "substituted": substituted,
        "gaps": gaps,
        "opening_matches_in_10": opening,
    }


def hohox_drop_one_group() -> tuple[dict, ...]:
    """Drop each printed group. The form says 50 letters and the page shows 55."""
    if len(HOHOX) != 55:
        raise ValueError("HOHOX printed length is no longer 55")
    groups = [HOHOX[index : index + 5] for index in range(0, 55, 5)]
    rows = []
    for index, group in enumerate(groups):
        kept = "".join(groups[:index] + groups[index + 1 :])
        copies = extra_repeats(kept)
        rows.append({
            "index": index,
            "group": group,
            "length": len(kept),
            "extra_repeats": copies,
            "random_at_least": random_at_least(len(kept), copies),
        })
    return tuple(rows)


def search_ts_clerk() -> dict:
    """Record desk habits. No plaintext is produced."""
    drops = hohox_drop_one_group()
    hearing = hearing_tally()
    return {
        "claimed_plaintext": None,
        "solved": False,
        "iasrz_second_group": IASRZ_129[5:10],
        "iasrz_openings_match": IASRZ_129[5:10] == IASRZ_130[5:10],
        "f8y_second_groups": (SSKFV[5:10], HOHOX[5:10]),
        "f8y_shared_tail": SSKFV[-8:] if SSKFV[-8:] == HOHOX[-8:] else "",
        "hearing": hearing,
        "hohox_drops": drops,
        "hohox_max_extra_repeats": max(row["extra_repeats"] for row in drops),
        "scope": "Procedure and copying only. A shared opening is not the contents of the message.",
    }
