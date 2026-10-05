"""How far the bounded Enigma trial separates Enigma from Bob's other families.

Eight ciphertexts per family are drawn from the training slice of the Austen
prose, with the training generator, at the router's three lengths. Each gets
the trial in engine.neural_enigma_features. The number kept is how many
standard deviations the best setting stands above all tried settings. No
held-out prose is used, and no setting or plaintext is kept.
"""

from __future__ import annotations

import random

import numpy as np

from engine.dagapeyeff_cache import frozen
from engine.neural_enigma_features import enigma_trial
from engine.neural_features import feature_tables
from engine.neural_grade import FAMILIES, _english_unigram, letters_az, load_training_prose
from engine.neural_router_v2 import _encrypt

_SEED = 20261013
_PER_FAMILY = 8
_EXTRA = ("rail-fence", "affine", "autokey")


@frozen("bob-enigma")
def bob_enigma_report() -> dict:
    full = letters_az(load_training_prose())
    training = full[: int(len(full) * 0.6)]
    english = _english_unigram(training)
    tables = feature_tables(training, english)
    logenglish = np.log(np.maximum(np.asarray(tables["english"], dtype=np.float64), 1e-300))
    drawn = random.Random(_SEED)
    rows = {}
    for family in (*FAMILIES, *_EXTRA):
        scores = []
        for _ in range(_PER_FAMILY):
            length = drawn.choice((120, 180, 240))
            start = drawn.randrange(len(training) - length)
            cipher = _encrypt(family, training[start:start + length], drawn)
            values = np.array([ord(ch) - 65 for ch in cipher if "A" <= ch <= "Z"], dtype=np.int64)
            scores.append(round(float(enigma_trial(values, tables["logdig"], logenglish)["pair_z"]), 2))
        rows[family] = scores
    others = [score for family, scores in rows.items() if family != "enigma" for score in scores]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "per_family": _PER_FAMILY,
        "families": len(rows),
        "enigma_lowest_z": min(rows["enigma"]),
        "others_highest_z": max(others),
        "separated": min(rows["enigma"]) > max(others),
        "z_by_family": rows,
        "scope": (
            "A bounded trial assuming reflector B, rotors I to III and no plugboard, the training "
            "generator's settings. It ranks families. It does not break an intercept."
        ),
    }
