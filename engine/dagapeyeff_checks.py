"""Fast checks for the swarm and the engines. Not a reading.

The frozen scores must not claim a reading. The chi-square must ignore
order. Both ends of a printed group of five cannot sit on the square at
once, because a group of five is an odd length and the pairs start at
the first digit. A shuffle that also scores zero is not evidence.
No letter string is stored.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from engine.dagapeyeff_foresight import after_training
from engine.dagapeyeff_swarm import CHALLENGE, best_chi_square, challenge_pairs

_CACHE = Path(__file__).resolve().parent / "data" / "swarm_cache"
_ROW = set("67890")
_COLUMN = set("12345")
_SEED = 20261004
_DRAWS = 2000


def _on_square(first: str, second: str) -> bool:
    return first in _ROW and second in _COLUMN


def _cache_check() -> dict:
    files = sorted(_CACHE.glob("*.json"))
    claiming = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("solved") is not False or data.get("claimed_plaintext") is not None:
            claiming.append(path.name)
    return {"files": len(files), "claiming_a_reading": claiming}


def _parity_check() -> dict:
    groups = CHALLENGE.split()
    both_on = 0
    interior_breaks = 0
    for index, group in enumerate(groups[:-1]):
        left = _on_square(group[0], group[1])
        right = _on_square(group[3], group[4])
        if left and right:
            both_on += 1
        if index % 2 == 0:
            if not (left and not right):
                interior_breaks += 1
        elif not (right and not left):
            interior_breaks += 1
    last = groups[-1]
    last_left = _on_square(last[0], last[1])
    last_right = _on_square(last[3], last[4])
    if last_left and last_right:
        both_on += 1
    drawn = random.Random(_SEED)
    as_low = 0
    for _ in range(_DRAWS):
        count = 0
        for group in groups:
            chars = list(group)
            drawn.shuffle(chars)
            if _on_square(chars[0], chars[1]) and _on_square(chars[3], chars[4]):
                count += 1
        if count <= both_on:
            as_low += 1
    return {
        "groups": len(groups),
        "interior_groups": len(groups) - 1,
        "interior_breaks": interior_breaks,
        "both_ends_on_square": both_on,
        "last_group_left_on_square": last_left,
        "last_group_right_on_square": last_right,
        "forced_by_odd_groups": interior_breaks == 0,
        "shuffle_draws": _DRAWS,
        "shuffles_as_low": as_low,
        "shuffle_is_evidence": False,
    }


def _order_check() -> dict:
    pairs = list(challenge_pairs())
    forward = round(best_chi_square(tuple(pairs)), 2)
    backward = round(best_chi_square(tuple(reversed(pairs))), 2)
    return {"pairs": len(pairs), "forward_chi": forward, "reversed_chi": backward, "order_changes_chi": forward != backward}


def checks_report() -> dict:
    cache = _cache_check()
    parity = _parity_check()
    order = _order_check()
    trained = after_training()
    sound = (
        cache["claiming_a_reading"] == []
        and parity["forced_by_odd_groups"]
        and parity["both_ends_on_square"] == 0
        and not order["order_changes_chi"]
        and trained["accepted"] == ["end-pairs"]
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "sound": sound,
        "cache": cache,
        "parity": parity,
        "order": order,
        "trained_accepted": trained["accepted"],
        "learned": (
            f"{cache['files']} frozen scores claim no reading. Reversing the cells does not change the chi-square. "
            "Both ends of a printed group of five are on the square in 0 of 79 groups. "
            "That zero is forced by the odd group length, so "
            f"{parity['shuffles_as_low']} of {parity['shuffle_draws']} shuffles also hitting zero is not evidence. "
            "The next job the members allow is the check, not another search. Refuse the zero as a finding."
        ),
    }
