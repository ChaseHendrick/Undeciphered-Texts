"""The residual branch is doing work. The weights are not replaced.

Bob adds the first hidden layer back onto the second. This measures both
parts on the challenge and on a Caesar of known prose. A dead branch would
mean the second layer is unused. No letter string is stored.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from engine.alphabet import letters_only
from engine.bob_caution import _SHIPPED, _WEIGHTS, _caesar, _letters
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen


def _shares(text: str) -> list[float]:
    from engine.neural_features import feature_tables
    from engine.neural_router_v2 import _english_unigram, _features, load_router

    saved = load_router()
    english = _english_unigram(saved["training_letters"])
    tables = feature_tables(saved["training_letters"], english)
    row = np.asarray([_features(text.upper(), english, tables, version=saved["feature_version"])], dtype=np.float64)
    shares = []
    for model in saved["models"]:
        normalized = (row - np.asarray(model["mean"])) / np.asarray(model["scale"])
        parameters = {name: np.asarray(value, dtype=np.float64) for name, value in model["parameters"].items()}
        skip = np.tanh(normalized @ parameters["w0"] + parameters["b0"])
        branch = np.tanh(skip @ parameters["w1"] + parameters["b1"])
        branch_size = float(np.mean(np.abs(branch)))
        skip_size = float(np.mean(np.abs(skip)))
        shares.append(round(branch_size / (branch_size + skip_size), 4))
    return shares


@frozen("bob-branch")
def bob_branch_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    challenge = _shares(_letters(_cells()))
    control = _shares(_caesar(letters_only(_PROSE), 7))
    alive = all(0.4 <= share <= 0.6 for share in challenge + control)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "challenge_branch_share": challenge,
        "control_branch_share": control,
        "branch_alive": alive,
        "scope": "A live residual branch is not a reading. The weights were not replaced.",
    }
