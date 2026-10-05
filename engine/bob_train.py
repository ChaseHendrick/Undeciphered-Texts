"""One warm start of Bob. The weight file is not replaced.

Sixteen epochs, 32 samples per family, learning rate 0.0004, and a frozen
teacher at strength 0.25. The start is the shipped format 5 network. A
checkpoint may keep that start when validation does not improve. A tie on
both development bars is not a stronger router. The internal gate treats a
tie as allowed. This run does not use that permission, and it does not write
the file. The lifted ranking is unchanged.
"""

from __future__ import annotations

import hashlib

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.bob_lift import bob_lift_report
from engine.dagapeyeff_cache import frozen
from engine.neural_router_v2 import train_router

_EPOCHS = 16
_PER_CLASS = 32
_RATE = 0.0004
_STRENGTH = 0.25
_TEMPERATURE = 2.0


@frozen("bob-train")
def bob_train_report() -> dict:
    before = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    if before != _SHIPPED:
        raise RuntimeError("the shipped weight file is not the expected artifact")
    metrics = train_router(
        epochs=_EPOCHS,
        train_per_class=_PER_CLASS,
        write=False,
        warm_start=True,
        hidden=96,
        ensemble_size=3,
        learning_rate=_RATE,
        distillation_strength=_STRENGTH,
        distillation_temperature=_TEMPERATURE,
        feature_version="cipher_statistics_v5",
        expanded_families=False,
        more_prose=False,
        cost_sensitive=False,
    )
    after = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    if after != before:
        raise RuntimeError("training wrote the weight file")
    lift = bob_lift_report()
    predecessor = metrics["predecessor_comparison"]
    held_after = int(predecessor["correct_after"])
    held_before = int(predecessor["correct_before"])
    bench_after = int(predecessor["benchmark_correct_after"])
    bench_before = int(predecessor["benchmark_correct_before"])
    checkpoints = [int(epoch) for epoch in metrics["checkpoint_epochs"]]
    rose = held_after > held_before or bench_after > bench_before
    beat_lift = (
        held_after >= int(lift["held_after"])
        and bench_after >= int(lift["benchmark_after"])
        and (held_after > int(lift["held_after"]) or bench_after > int(lift["benchmark_after"]))
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": after,
        "weights_replaced": False,
        "weights_match_shipped": after == _SHIPPED,
        "epochs": _EPOCHS,
        "train_per_class": _PER_CLASS,
        "learning_rate": _RATE,
        "distillation_strength": _STRENGTH,
        "distillation_temperature": _TEMPERATURE,
        "hidden": 96,
        "ensemble_size": 3,
        "feature_version": "cipher_statistics_v5",
        "checkpoint_epochs": checkpoints,
        "held_before": held_before,
        "held_after": held_after,
        "held_total": int(predecessor["total"]),
        "held_top3": int(metrics["top3_correct"]),
        "benchmark_before": bench_before,
        "benchmark_after": bench_after,
        "benchmark_total": int(predecessor["benchmark_total"]),
        "internal_promoted": bool(metrics["promoted"]),
        "scores_rose": rose,
        "beat_lift": beat_lift,
        "lift_held": int(lift["held_after"]),
        "lift_benchmark": int(lift["benchmark_after"]),
        "promoted": False,
        "scope": (
            "A warm start that does not raise either development bar does not replace the weight file. "
            "A tie is not a stronger Bob. Not a reading."
        ),
    }
