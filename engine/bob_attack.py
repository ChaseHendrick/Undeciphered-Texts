"""Pentest of the lifted ranking. The weight file is not replaced.

The attacks are predeclared: middle deletion, reversal, a duplicated middle
letter, case and spaces, English with no encryption, random letters, a short
string, and digits. Two texts per trained family are drawn from the training
prose, not from the development comparison. No letter string is stored.
"""

from __future__ import annotations

import hashlib
import random

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.bob_harden import accept_call, drop_middle
from engine.bob_lift import lifted_family
from engine.bob_pair import _texts
from engine.dagapeyeff_cache import frozen
from engine.neural_grade import letters_az, load_training_prose
from engine.neural_router_v2 import load_router, route_probabilities

_SEED = 20261006
_PER_CLASS = 2
_RANDOM = 8


def _family(text: str) -> str:
    return lifted_family(text)


def _top(text: str) -> tuple[str, float, bool]:
    report = route_probabilities(text)
    row = report["candidates"][0]
    return row["family"], float(row["probability"]), bool(report["uncertain"])


def _duplicate_middle(text: str) -> str:
    seats = [index for index, char in enumerate(text) if "A" <= char <= "Z"]
    cut = seats[len(seats) // 2]
    return text[:cut] + text[cut] + text[cut:]


@frozen("bob-attack")
def bob_attack_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    saved = load_router()
    names = saved["families"]
    training = letters_az(load_training_prose())
    texts, labels = _texts(training, _SEED, names, _PER_CLASS, False)
    clean = deletion_flips = reverse_flips = insertion_flips = 0
    case_mismatches = 0
    hardened_correct = hardened_withheld = hardened_wrong = 0
    for text, label in zip(texts, labels):
        truth = names[label]
        family = _family(text)
        if family == truth:
            clean += 1
        deleted = _family(drop_middle(text))
        if deleted != family:
            deletion_flips += 1
        if _family(text[::-1]) != family:
            reverse_flips += 1
        if _family(_duplicate_middle(text)) != family:
            insertion_flips += 1
        spaced = " ".join(text[index:index + 5] for index in range(0, len(text), 5)).lower()
        if _family(spaced) != family:
            case_mismatches += 1
        mean_family, probability, _uncertain = _top(text)
        lift_applied = family != mean_family
        kept = accept_call(family, deleted, probability, lift_applied)
        if not kept:
            hardened_withheld += 1
        elif family == truth:
            hardened_correct += 1
        else:
            hardened_wrong += 1
    drawn = random.Random(_SEED + 3)
    plain_certain = 0
    plain_peak = 0.0
    for _ in range(len(names)):
        start = drawn.randrange(len(training) - 160)
        window = training[start:start + 160]
        _family_name, probability, uncertain = _top(window)
        plain_peak = max(plain_peak, probability)
        if not uncertain:
            plain_certain += 1
    random_certain = 0
    random_peak = 0.0
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(_RANDOM):
        soup = "".join(drawn.choice(alphabet) for _ in range(160))
        _family_name, probability, uncertain = _top(soup)
        random_peak = max(random_peak, probability)
        if not uncertain:
            random_certain += 1
    short_rejected = False
    try:
        route_probabilities("A" * 15)
    except ValueError:
        short_rejected = True
    digit_rejected = False
    try:
        route_probabilities("1" * 40)
    except ValueError:
        digit_rejected = True
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "texts": len(texts),
        "clean_correct": clean,
        "deletion_flips": deletion_flips,
        "reverse_flips": reverse_flips,
        "insertion_flips": insertion_flips,
        "case_mismatches": case_mismatches,
        "hardened_correct": hardened_correct,
        "hardened_withheld": hardened_withheld,
        "hardened_wrong": hardened_wrong,
        "plain_draws": len(names),
        "plain_certain": plain_certain,
        "plain_peak": round(plain_peak, 4),
        "random_draws": _RANDOM,
        "random_certain": random_certain,
        "random_peak": round(random_peak, 4),
        "short_rejected": short_rejected,
        "digit_rejected": digit_rejected,
        "hardened_promoted_as_accuracy": False,
        "scope": (
            "An attack count is not a reading. Withholding fragile calls does not raise the development bars. "
            "The weight file was not replaced."
        ),
    }
