"""A withhold gate in front of the lifted ranking. The weight file is not replaced.

A call is kept only when deleting the middle letter leaves the family alone,
and the mean probability is at least one half, unless the lifted Enigma
versus M-209 vote already applied. The one-half line is the router's existing
uncertainty cutoff. It was not chosen from this probe. Withholding is not a
higher score. No letter string is stored.
"""

from __future__ import annotations

import hashlib

import numpy as np

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.bob_lift import _bundle, _choose, lifted_family
from engine.dagapeyeff_cache import frozen
from engine.neural_router_v2 import _features, network_logits, route_probabilities

_PROBABILITY = 0.5


def drop_middle(text: str) -> str:
    """Drop the middle A-Z letter. The caller must leave at least 16 letters."""
    if not isinstance(text, str):
        raise TypeError("ciphertext must be text")
    seats = [index for index, char in enumerate(text) if "A" <= char.upper() <= "Z" and char.isascii()]
    if len(seats) < 17:
        raise ValueError("a deletion check needs 17 or more A-Z letters")
    cut = seats[len(seats) // 2]
    return text[:cut] + text[cut + 1:]


def accept_call(family: str, deleted_family: str, probability: float, lift_applied: bool) -> bool:
    """True when the ranking may be shown. False withholds it."""
    if not isinstance(family, str) or not isinstance(deleted_family, str):
        raise TypeError("families must be text")
    if isinstance(probability, bool) or not isinstance(probability, (int, float)):
        raise TypeError("probability must be a number")
    if not 0 <= float(probability) <= 1:
        raise ValueError("probability must lie between 0 and 1")
    if family != deleted_family:
        return False
    if lift_applied:
        return True
    return float(probability) >= _PROBABILITY


def route_hardened(text: str) -> dict:
    """Lifted ranking, withheld when the deletion check fails.

    Returned candidates keep the mean network's probabilities. No plaintext
    is added. The weight file is not read as a new model.
    """
    report = route_probabilities(text)
    family = lifted_family(text)
    deleted = lifted_family(drop_middle(text))
    top = report["candidates"][0]["probability"]
    folded = text.upper()
    saved, english, tables, weights, mean, scale, _train = _bundle()
    rows = [_features(folded, english, tables, version=saved["feature_version"])]
    each = np.stack([network_logits(rows, model) for model in saved["models"]], axis=0)
    base, chosen, _order = _choose([folded], each, tables, weights, mean, scale, saved["families"])
    lift_applied = int(chosen[0]) != int(base[0])
    accepted = accept_call(family, deleted, top, lift_applied)
    if accepted:
        return {
            **report,
            "accepted": True,
            "withheld": False,
            "family": family,
            "ordered_by": "lifted-vote",
            "weights_replaced": False,
        }
    return {
        **report,
        "accepted": False,
        "withheld": True,
        "family": None,
        "ordered_by": "withheld",
        "weights_replaced": False,
        "scope": report["scope"] + " This call was withheld because the middle-letter check failed or the probability was under one half.",
    }


@frozen("bob-harden")
def bob_harden_report() -> dict:
    """The gate's own rules. The probe that counts flips lives next to the attack."""
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "probability_cutoff": _PROBABILITY,
        "promoted_as_accuracy": False,
        "scope": "Withholding a fragile call is not a higher score and not a reading.",
    }
