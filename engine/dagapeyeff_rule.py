"""Did the 1939 challenge follow the book's dummy rule? Not a reading.

The earlier swarm deleted every third, fourth, or fifth cell and scored what
remained. That imposes the rule. This one asks whether the digits contain it.

A worker states the prediction before it measures. The book's rule predicts
that one residue is a single filler symbol. The rival is that he did not do
that, so the 196 cells are the whole cipher. The solved example in the book
is the control: it was not written with dummies, so a real filler test must
not fire on it either. Letters are not kept.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_swarm import CONTROL, _pairs, challenge_pairs

_BOOK = (3, 4, 5)
_SEED = 20261004
_DRAWS = 400

CARD = {
    "hypothesis": "Every third, fourth, or fifth cell is one dummy symbol.",
    "prediction": "That residue uses one symbol, or a share no shuffle of these cells reaches.",
    "rival": "He did not use the rule. The 196 cells are the cipher.",
    "control": "The solved Polybius example earlier in the book.",
    "claimed_plaintext": None,
}


def book_residues() -> tuple[tuple[int, int], ...]:
    return tuple((period, phase) for period in _BOOK for phase in range(period))


def _class(seq: tuple[str, ...] | list[str], period: int, phase: int) -> list[str]:
    return [seq[index] for index in range(phase, len(seq), period)]


def _narrowest(seq: tuple[str, ...] | list[str]) -> tuple[int, int, int, int]:
    """Return period, phase, length, distinct symbols. Ties keep the earlier residue."""
    chosen = None
    for period, phase in book_residues():
        got = _class(seq, period, phase)
        distinct = len(set(got))
        row = (period, phase, len(got), distinct)
        if chosen is None or distinct < chosen[3]:
            chosen = row
    return chosen


def _peakiest(seq: tuple[str, ...] | list[str]) -> tuple[int, int, int, float]:
    chosen = None
    for period, phase in book_residues():
        got = _class(seq, period, phase)
        share = max(Counter(got).values()) / len(got)
        row = (period, phase, len(got), share)
        if chosen is None or share > chosen[3]:
            chosen = row
    return chosen


def worker_report(worker: int) -> dict:
    """One book-rule residue. Filler only if the class is a single symbol."""
    menu = book_residues()
    if worker < 0 or worker >= len(menu):
        raise IndexError(worker)
    period, phase = menu[worker]
    got = _class(challenge_pairs(), period, phase)
    distinct = len(set(got))
    report = dict(CARD)
    report.update({
        "worker": worker,
        "period": period,
        "phase": phase,
        "kept_out": len(challenge_pairs()) - len(got),
        "residue_length": len(got),
        "distinct": distinct,
        "top_share": round(max(Counter(got).values()) / len(got), 4),
        "looks_like_filler": distinct == 1,
    })
    return report


def search_rule() -> dict:
    """Close the card. A deletion score is not consulted, because the rule is not there."""
    pairs = challenge_pairs()
    control = _pairs(CONTROL, "ABCDE")
    narrow = _narrowest(pairs)
    peak = _peakiest(pairs)
    control_narrow = _narrowest(control)
    drawn = random.Random(_SEED)
    as_narrow = 0
    for _ in range(_DRAWS):
        shuffled = list(pairs)
        drawn.shuffle(shuffled)
        if _narrowest(shuffled)[3] <= narrow[3]:
            as_narrow += 1
    drawn = random.Random(_SEED)
    as_peaked = 0
    for _ in range(_DRAWS):
        shuffled = list(pairs)
        drawn.shuffle(shuffled)
        if _peakiest(shuffled)[3] >= peak[3] - 1e-12:
            as_peaked += 1
    filler = any(worker_report(index)["looks_like_filler"] for index in range(len(book_residues())))
    report = dict(CARD)
    report.update({
        "solved": False,
        "residues": len(book_residues()),
        "narrow_period": narrow[0],
        "narrow_phase": narrow[1],
        "narrow_length": narrow[2],
        "narrow_distinct": narrow[3],
        "shuffle_draws": _DRAWS,
        "shuffle_as_narrow": as_narrow,
        "peak_period": peak[0],
        "peak_phase": peak[1],
        "peak_share": round(peak[3], 4),
        "shuffle_as_peaked": as_peaked,
        "any_filler": filler,
        "control_narrow_distinct": control_narrow[3],
        "confirms_hypothesis": filler and as_narrow == 0,
        "rival_stands": (not filler) and as_narrow > _DRAWS // 4,
        "scope": (
            "The prediction is measured on the residue itself. "
            "Deleting it and rescoring the rest is a later question, already lost. "
            "No letter string is stored."
        ),
    })
    return report
