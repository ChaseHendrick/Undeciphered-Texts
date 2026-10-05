"""The aligned runs still touch the rare cells when those cells stay put.

Cells that appear at most three times keep their seats. The other cells are
shuffled. Among the shuffles that already have two runs in one starting
column, the score is how often both runs sit next to a rare cell. The
meeting of the common cell with a different run is scored on the same
draws, and it is kept only if it still clears once a vertical run is
required. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_contact import _band, _rare
from engine.dagapeyeff_meeting import _meetings
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14
_RUN = 3


def _vertical_runs(seq: list[str], mode: str) -> int:
    found = 0
    for column in range(_WIDTH):
        start = 0
        while start < _WIDTH:
            end = start
            while end + 1 < _WIDTH and seq[(end + 1) * _WIDTH + column] == seq[start * _WIDTH + column]:
                end += 1
            if end - start + 1 >= _RUN and seq[start * _WIDTH + column] == mode:
                found += 1
            start = end + 1
    return found


@frozen("seats")
def seats_report() -> dict:
    pairs = list(challenge_pairs())
    rare = _rare(pairs)
    shared, touched, _runs = _band(pairs, rare)
    mode = Counter(pairs).most_common(1)[0][0]
    low = sorted(rare)
    pinned = {index for index, cell in enumerate(pairs) if cell in rare}
    free = [index for index in range(len(pairs)) if index not in pinned]
    seen = random.Random(_SEED)
    aligned = 0
    contact = 0
    vertical = 0
    meeting = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        bag = [shuffled[index] for index in free]
        seen.shuffle(bag)
        for index, cell in zip(free, bag):
            shuffled[index] = cell
        shuffle_shared, shuffle_touched, _ignored = _band(shuffled, rare)
        if shuffle_shared >= shared:
            aligned += 1
            if shuffle_touched >= touched:
                contact += 1
        if _vertical_runs(shuffled, mode) >= 1:
            vertical += 1
            if _meetings(shuffled)[0] >= 1:
                meeting += 1
    contact_rate = contact / aligned if aligned else 1.0
    meeting_rate = meeting / vertical if vertical else 1.0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pinned": len(pinned),
        "low": low,
        "draws": _DRAWS,
        "aligned": aligned,
        "contact": contact,
        "vertical_runs": vertical,
        "meeting_given_vertical": meeting,
        "allowed": aligned > 0 and contact_rate < 0.05 and meeting_rate >= 0.05,
        "scope": "Contact with the rare seats is not a reading. No letter string is stored.",
    }
