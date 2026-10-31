# The boundary-walk suite: the eighteenth measurement's declared
# artifact against its frozen predecessors. Hand constants pin the
# declared steps, the window masses at the standing first boundary,
# the head endpoints at the standing first and second boundaries and
# the seed-kind registry's unchanged tail; the artifact pins are read
# from the frozen run of 29 October 2026 with the bridge gate
# verified at 516 fields (86 per cell times six cells) and the
# direction tables recorded for every span beside every head.
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/"
    "voynich-homophonic-boundary-walk.json"
).resolve()
FROZEN_REAL = Path(
    "docs/research-notes/"
    "voynich-homophonic-real-at-basis-ladder.json"
).resolve()
FROZEN_STREAM = Path(
    "docs/research-notes/"
    "voynich-homophonic-stream-positions.json"
).resolve()

SCALAR_KEYS = [
    "empty_type_count", "self_pair_share", "top_1_share",
    "top_10_share", "top_50_share", "pair_entropy",
]

# code -> (kept pairs, window mass, first head, last head), the
# window mass exactly the standing first boundary's span size and
# the walk's endpoints exactly the standing first and second
# boundaries, every head at an int(step x the anchor basis)
# position with the anchor basis the kept pair total + 1.
WALK_SHAPES = {
    "ZL": (218415, 54604, 54604, 109208),
    "GC": (183199, 45800, 45800, 91600),
    "IT": (220531, 55133, 55133, 110266),
}

# the declared spot heads for the scalar pins: the first, a middle
# and the last of the 26, indexes into the stored head rows.
SPOT_HEADS = (0, 12, 25)

# code -> the fresh whole profile's six scalars, read
# from the frozen boundary-walk run of 29 October 2026.
WHOLE_SCALARS = {
    "ZL": {
        "empty_type_count": 928,
        "self_pair_share": 0.065848,
        "top_1_share": 0.070481,
        "top_10_share": 0.424435,
        "top_50_share": 0.893671,
        "pair_entropy": 4.010179,
    },
    "GC": {
        "empty_type_count": 642,
        "self_pair_share": 0.015928,
        "top_1_share": 0.051049,
        "top_10_share": 0.373572,
        "top_50_share": 0.8066,
        "pair_entropy": 4.422831,
    },
    "IT": {
        "empty_type_count": 984,
        "self_pair_share": 0.065777,
        "top_1_share": 0.071689,
        "top_10_share": 0.429316,
        "top_50_share": 0.89868,
        "pair_entropy": 3.980621,
    },
}

SPAN_SCALARS = {
    # (code, language, head index, side) -> the span
    # profile's six scalars at the declared spot heads
    ("ZL", "english", 0, "left"): {
        "empty_type_count": 1028,
        "self_pair_share": 0.083007,
        "top_1_share": 0.06476,
        "top_10_share": 0.463045,
        "top_50_share": 0.914338,
        "pair_entropy": 3.904198,
    },
    ("ZL", "english", 0, "right"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.062765,
        "top_1_share": 0.088227,
        "top_10_share": 0.437141,
        "top_50_share": 0.891247,
        "pair_entropy": 4.005492,
    },
    ("ZL", "english", 12, "left"): {
        "empty_type_count": 1029,
        "self_pair_share": 0.075825,
        "top_1_share": 0.074873,
        "top_10_share": 0.458703,
        "top_50_share": 0.910956,
        "pair_entropy": 3.926608,
    },
    ("ZL", "english", 12, "right"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.057164,
        "top_1_share": 0.085488,
        "top_10_share": 0.425209,
        "top_50_share": 0.886868,
        "pair_entropy": 4.045388,
    },
    ("ZL", "english", 25, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.062765,
        "top_1_share": 0.088227,
        "top_10_share": 0.437141,
        "top_50_share": 0.891247,
        "pair_entropy": 4.005492,
    },
    ("ZL", "english", 25, "right"): {
        "empty_type_count": 1007,
        "self_pair_share": 0.058582,
        "top_1_share": 0.069075,
        "top_10_share": 0.397112,
        "top_50_share": 0.88721,
        "pair_entropy": 4.051398,
    },
    ("ZL", "latin", 0, "left"): {
        "empty_type_count": 1028,
        "self_pair_share": 0.083007,
        "top_1_share": 0.06476,
        "top_10_share": 0.463045,
        "top_50_share": 0.914338,
        "pair_entropy": 3.904198,
    },
    ("ZL", "latin", 0, "right"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.062765,
        "top_1_share": 0.088227,
        "top_10_share": 0.437141,
        "top_50_share": 0.891247,
        "pair_entropy": 4.005492,
    },
    ("ZL", "latin", 12, "left"): {
        "empty_type_count": 1029,
        "self_pair_share": 0.075825,
        "top_1_share": 0.074873,
        "top_10_share": 0.458703,
        "top_50_share": 0.910956,
        "pair_entropy": 3.926608,
    },
    ("ZL", "latin", 12, "right"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.057164,
        "top_1_share": 0.085488,
        "top_10_share": 0.425209,
        "top_50_share": 0.886868,
        "pair_entropy": 4.045388,
    },
    ("ZL", "latin", 25, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.062765,
        "top_1_share": 0.088227,
        "top_10_share": 0.437141,
        "top_50_share": 0.891247,
        "pair_entropy": 4.005492,
    },
    ("ZL", "latin", 25, "right"): {
        "empty_type_count": 1007,
        "self_pair_share": 0.058582,
        "top_1_share": 0.069075,
        "top_10_share": 0.397112,
        "top_50_share": 0.88721,
        "pair_entropy": 4.051398,
    },
    ("GC", "english", 0, "left"): {
        "empty_type_count": 840,
        "self_pair_share": 0.021603,
        "top_1_share": 0.057632,
        "top_10_share": 0.383269,
        "top_50_share": 0.8276,
        "pair_entropy": 4.337008,
    },
    ("GC", "english", 0, "right"): {
        "empty_type_count": 831,
        "self_pair_share": 0.011493,
        "top_1_share": 0.04601,
        "top_10_share": 0.386106,
        "top_50_share": 0.802313,
        "pair_entropy": 4.431385,
    },
    ("GC", "english", 12, "left"): {
        "empty_type_count": 847,
        "self_pair_share": 0.018227,
        "top_1_share": 0.05358,
        "top_10_share": 0.381027,
        "top_50_share": 0.826186,
        "pair_entropy": 4.350886,
    },
    ("GC", "english", 12, "right"): {
        "empty_type_count": 817,
        "self_pair_share": 0.012244,
        "top_1_share": 0.048648,
        "top_10_share": 0.364405,
        "top_50_share": 0.801873,
        "pair_entropy": 4.448769,
    },
    ("GC", "english", 25, "left"): {
        "empty_type_count": 831,
        "self_pair_share": 0.011493,
        "top_1_share": 0.04601,
        "top_10_share": 0.386106,
        "top_50_share": 0.802313,
        "pair_entropy": 4.431385,
    },
    ("GC", "english", 25, "right"): {
        "empty_type_count": 814,
        "self_pair_share": 0.017204,
        "top_1_share": 0.05186,
        "top_10_share": 0.371746,
        "top_50_share": 0.806232,
        "pair_entropy": 4.428392,
    },
    ("GC", "latin", 0, "left"): {
        "empty_type_count": 840,
        "self_pair_share": 0.021603,
        "top_1_share": 0.057632,
        "top_10_share": 0.383269,
        "top_50_share": 0.8276,
        "pair_entropy": 4.337008,
    },
    ("GC", "latin", 0, "right"): {
        "empty_type_count": 831,
        "self_pair_share": 0.011493,
        "top_1_share": 0.04601,
        "top_10_share": 0.386106,
        "top_50_share": 0.802313,
        "pair_entropy": 4.431385,
    },
    ("GC", "latin", 12, "left"): {
        "empty_type_count": 847,
        "self_pair_share": 0.018227,
        "top_1_share": 0.05358,
        "top_10_share": 0.381027,
        "top_50_share": 0.826186,
        "pair_entropy": 4.350886,
    },
    ("GC", "latin", 12, "right"): {
        "empty_type_count": 817,
        "self_pair_share": 0.012244,
        "top_1_share": 0.048648,
        "top_10_share": 0.364405,
        "top_50_share": 0.801873,
        "pair_entropy": 4.448769,
    },
    ("GC", "latin", 25, "left"): {
        "empty_type_count": 831,
        "self_pair_share": 0.011493,
        "top_1_share": 0.04601,
        "top_10_share": 0.386106,
        "top_50_share": 0.802313,
        "pair_entropy": 4.431385,
    },
    ("GC", "latin", 25, "right"): {
        "empty_type_count": 814,
        "self_pair_share": 0.017204,
        "top_1_share": 0.05186,
        "top_10_share": 0.371746,
        "top_50_share": 0.806232,
        "pair_entropy": 4.428392,
    },
    ("IT", "english", 0, "left"): {
        "empty_type_count": 1051,
        "self_pair_share": 0.083549,
        "top_1_share": 0.065613,
        "top_10_share": 0.469072,
        "top_50_share": 0.918903,
        "pair_entropy": 3.871494,
    },
    ("IT", "english", 0, "right"): {
        "empty_type_count": 1052,
        "self_pair_share": 0.063603,
        "top_1_share": 0.089513,
        "top_10_share": 0.441593,
        "top_50_share": 0.897695,
        "pair_entropy": 3.972243,
    },
    ("IT", "english", 12, "left"): {
        "empty_type_count": 1063,
        "self_pair_share": 0.076727,
        "top_1_share": 0.075898,
        "top_10_share": 0.464648,
        "top_50_share": 0.917088,
        "pair_entropy": 3.890578,
    },
    ("IT", "english", 12, "right"): {
        "empty_type_count": 1036,
        "self_pair_share": 0.057037,
        "top_1_share": 0.08711,
        "top_10_share": 0.430128,
        "top_50_share": 0.892833,
        "pair_entropy": 4.021784,
    },
    ("IT", "english", 25, "left"): {
        "empty_type_count": 1052,
        "self_pair_share": 0.063603,
        "top_1_share": 0.089513,
        "top_10_share": 0.441593,
        "top_50_share": 0.897695,
        "pair_entropy": 3.972243,
    },
    ("IT", "english", 25, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.05686,
        "top_1_share": 0.070918,
        "top_10_share": 0.398919,
        "top_50_share": 0.888273,
        "pair_entropy": 4.041147,
    },
    ("IT", "latin", 0, "left"): {
        "empty_type_count": 1051,
        "self_pair_share": 0.083549,
        "top_1_share": 0.065613,
        "top_10_share": 0.469072,
        "top_50_share": 0.918903,
        "pair_entropy": 3.871494,
    },
    ("IT", "latin", 0, "right"): {
        "empty_type_count": 1052,
        "self_pair_share": 0.063603,
        "top_1_share": 0.089513,
        "top_10_share": 0.441593,
        "top_50_share": 0.897695,
        "pair_entropy": 3.972243,
    },
    ("IT", "latin", 12, "left"): {
        "empty_type_count": 1063,
        "self_pair_share": 0.076727,
        "top_1_share": 0.075898,
        "top_10_share": 0.464648,
        "top_50_share": 0.917088,
        "pair_entropy": 3.890578,
    },
    ("IT", "latin", 12, "right"): {
        "empty_type_count": 1036,
        "self_pair_share": 0.057037,
        "top_1_share": 0.08711,
        "top_10_share": 0.430128,
        "top_50_share": 0.892833,
        "pair_entropy": 4.021784,
    },
    ("IT", "latin", 25, "left"): {
        "empty_type_count": 1052,
        "self_pair_share": 0.063603,
        "top_1_share": 0.089513,
        "top_10_share": 0.441593,
        "top_50_share": 0.897695,
        "pair_entropy": 3.972243,
    },
    ("IT", "latin", 25, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.05686,
        "top_1_share": 0.070918,
        "top_10_share": 0.398919,
        "top_50_share": 0.888273,
        "pair_entropy": 4.041147,
    },
}

HEAD_DIRECTIONS = {
    # (code, language, head index, side) -> the span's
    # direction record against the whole profile
    ("ZL", "english", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 11, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 11, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 12, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 12, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 13, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 13, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 14, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 14, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 15, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 15, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 16, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 16, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 17, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 17, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 18, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 18, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 19, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 19, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 20, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 20, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 21, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 21, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 22, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 22, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 23, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 23, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 24, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 24, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 25, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 25, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 11, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 11, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 12, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 12, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 13, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 13, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 14, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 14, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 15, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 15, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 16, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 16, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 17, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 17, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 18, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 18, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 19, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 19, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 20, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 20, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 21, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 21, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 22, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 22, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 23, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 23, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 24, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 24, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 25, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 25, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "english", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "english", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "english", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "english", 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 11, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 11, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 12, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 12, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 13, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 13, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 14, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 14, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 15, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 15, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 16, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 16, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 17, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 17, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 18, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 18, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 19, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 19, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 20, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 20, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 21, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 21, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 22, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 22, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 23, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 23, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 24, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 24, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 25, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 25, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "latin", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "latin", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "latin", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("GC", "latin", 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 11, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 11, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 12, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 12, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 13, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 13, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 14, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 14, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 15, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 15, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 16, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 16, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 17, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 17, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 18, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 18, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 19, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 19, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 20, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 20, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 21, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 21, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 22, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 22, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 23, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 23, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 24, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 24, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 25, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 25, "right"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 11, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 11, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 12, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 12, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 13, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 13, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 14, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 14, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 15, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 15, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 16, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 16, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 17, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 17, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 18, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 18, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 19, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 19, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 20, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 20, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 21, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 21, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 22, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 22, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 23, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 23, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 24, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 24, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 25, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 25, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 11, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 11, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 12, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 12, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 13, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 13, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 14, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 14, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 15, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 15, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 16, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 16, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 17, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 17, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 18, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 18, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 19, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 19, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 20, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 20, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 21, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 21, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 22, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 22, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 23, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 23, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 24, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 24, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 25, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 25, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
}


class BoundaryWalkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_real = json.loads(FROZEN_REAL.read_text())
        self.frozen_stream = json.loads(FROZEN_STREAM.read_text())

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.STREAM_WALK_STEP_DENOM, 100)
        self.assertEqual(
            homo.STREAM_WALK_HEAD_STEPS,
            tuple(j / 100 for j in range(25, 51)),
        )
        self.assertEqual(homo.STREAM_WALK_FIRST_STEP, 25)
        self.assertEqual(homo.STREAM_WALK_LAST_STEP, 50)
        self.assertEqual(
            homo.STREAM_WALK_ARTIFACT_PATH.name,
            "voynich-homophonic-boundary-walk.json",
        )
        self.assertEqual(max(homo.KIND_ID.values()), 30)
        self.assertEqual(
            homo.KIND_ID["homo_cut_geom"], 30,
            "the seed-kind registry ends at the cut-geometry kind; "
            "the boundary-walk instrument draws no seed at all",
        )
        self.assertEqual(
            sorted(self.artifact["declared"]),
            [
                "base_seed", "boundary_rule", "closure_rule",
                "confluence_rule", "direction_rule", "exclusion_rule",
                "gate_rule", "machinery_rule", "mapped",
                "models_rule", "no_band_rule", "record_rule",
                "roster_rule", "split_rule", "state_note",
                "summary_rule", "walk_rule",
            ],
        )
        self.assertEqual(
            self.artifact["declared"]["base_seed"], homo.BASE_SEED,
        )
        self.assertEqual(
            self.artifact["declared"]["mapped"], homo.MAPPED_HOMO,
        )

    def test_gate_replay(self) -> None:
        problems, fields = homo._compare_boundary_walk_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 516)
        self.assertEqual(
            self.artifact["bridge_gate"],
            {
                "status": "verified", "fields_compared": 516,
                "per_cell_fields": 86,
            },
        )

    def test_the_declared_shapes(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            kept, mass, first_head, last_head = WALK_SHAPES[code]
            self.assertEqual(cell["kept_pairs"], kept, code)
            self.assertEqual(cell["window_pairs"], mass, code)
            heads = cell["heads"]
            self.assertEqual(len(heads), 26, code)
            self.assertEqual(
                heads[0]["head_position"], first_head, code,
            )
            self.assertEqual(
                heads[-1]["head_position"], last_head, code,
            )
            anchor = kept + 1
            for index, row in enumerate(heads):
                self.assertEqual(
                    row["step"],
                    homo.STREAM_WALK_HEAD_STEPS[index], (code, index),
                )
                self.assertEqual(
                    row["head_position"],
                    int(homo.STREAM_WALK_HEAD_STEPS[index] * anchor),
                    (code, index),
                )
            stream_cell = self.frozen_stream["files"][code]["english"]
            self.assertEqual(
                heads[0]["head_position"],
                stream_cell["boundaries"][0], code,
            )
            self.assertEqual(
                heads[-1]["head_position"],
                stream_cell["boundaries"][1], code,
            )
            self.assertEqual(
                cell["stream_position_boundaries"],
                stream_cell["boundaries"], code,
            )

    def test_the_whole_gate(self) -> None:
        for code in FILES:
            for language in LANGS:
                fresh = homo._walk_cell(
                    code, self.frozen_stream["files"][code][language],
                )
                stored = self.artifact["files"][code][language]
                self.assertEqual(fresh, stored, (code, language))
                frozen = self.frozen_real["files"][code][language][
                    "rungs"
                ][0]["real_rung_profile"]
                self.assertEqual(
                    stored["whole_profile"], frozen, (code, language),
                )

    def test_the_walk_rebuild(self) -> None:
        for code in FILES:
            first, second = homo._real_pair_sequence(code)
            real = homo._homo_real_stream(code)
            mark = len(real["mapped_chars"]) - 1
            kept, mass, _, _ = WALK_SHAPES[code]
            anchor = kept + 1
            stored = self.artifact["files"][code]["english"]
            whole = stored["whole_profile"]
            self.assertEqual(stored["window_pairs"], mass, code)
            for index, row in enumerate(stored["heads"]):
                head = row["head_position"]
                self.assertEqual(
                    head,
                    int(homo.STREAM_WALK_HEAD_STEPS[index] * anchor),
                    (code, index),
                )
                for side, start in (
                    ("left", head - mass), ("right", head),
                ):
                    matrix = np.zeros((37, 37))
                    np.add.at(
                        matrix,
                        (first[start:start + mass],
                         second[start:start + mass]),
                        1.0,
                    )
                    profile = homo._profile_facts(
                        homo._glyph_block_matrix(matrix, mark)
                    )
                    carried = homo._boundary_carried_pairs(matrix, mark)
                    span = row[side]
                    self.assertEqual(
                        profile, span["profile"], (code, index, side),
                    )
                    self.assertEqual(
                        carried, span["boundary_carried_pairs"],
                        (code, index, side),
                    )
                    self.assertEqual(
                        span["profile"]["total_pairs"],
                        span["pairs"] - carried,
                        (code, index, side),
                    )
                    self.assertEqual(
                        span["first_position"], start,
                        (code, index, side),
                    )
                    self.assertEqual(
                        span["end_position"], start + mass,
                        (code, index, side),
                    )
                    fresh = homo._direction_vs_whole(profile, whole)
                    self.assertEqual(
                        fresh, span["direction"],
                        (code, index, side),
                    )
                    pinned = HEAD_DIRECTIONS[
                        (code, "english", index, side)
                    ]
                    self.assertEqual(
                        span["direction"], pinned,
                        (code, index, side),
                    )

    def test_the_direction_table(self) -> None:
        for code in FILES:
            for language in LANGS:
                stored = self.artifact["files"][code][language]
                whole = stored["whole_profile"]
                for index, row in enumerate(stored["heads"]):
                    for side in ("left", "right"):
                        fresh = homo._direction_vs_whole(
                            row[side]["profile"], whole,
                        )
                        self.assertEqual(
                            fresh, row[side]["direction"],
                            (code, language, index, side),
                        )
                        pinned = HEAD_DIRECTIONS[
                            (code, language, index, side)
                        ]
                        self.assertEqual(
                            row[side]["direction"], pinned,
                            (code, language, index, side),
                        )

    def test_confluence_with_the_stream_position_records(self) -> None:
        for code in FILES:
            frozen_cell = self.frozen_stream["files"][code]["english"]
            cell = self.artifact["files"][code]["english"]
            marks = (
                cell["heads"][0]["left"]["profile"]
                == frozen_cell["segments"][0]["profile"],
                cell["heads"][0]["right"]["profile"]
                == frozen_cell["segments"][1]["profile"],
                cell["heads"][-1]["left"]["profile"]
                == frozen_cell["segments"][1]["profile"],
                cell["heads"][-1]["right"]["profile"]
                == frozen_cell["segments"][2]["profile"],
            )
            self.assertEqual(
                marks, (True, True, True, True), code,
            )
            self.assertEqual(
                cell["heads"][0]["left"]["profile"],
                frozen_cell["segments"][0]["profile"], code,
            )
            self.assertEqual(
                cell["heads"][-1]["right"]["profile"]
                ["total_pairs"],
                frozen_cell["segments"][2]["profile"]["total_pairs"],
                code,
            )

    def test_scalar_pins(self) -> None:
        for code in FILES:
            whole = self.artifact["files"][code]["english"][
                "whole_profile"
            ]
            pinned = WHOLE_SCALARS[code]
            for key in SCALAR_KEYS:
                self.assertEqual(whole[key], pinned[key], (code, key))

    def test_span_scalar_pins(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                for index in SPOT_HEADS:
                    for side in ("left", "right"):
                        pinned = SPAN_SCALARS[
                            (code, language, index, side)
                        ]
                        for key in SCALAR_KEYS:
                            self.assertEqual(
                                cell["heads"][index][side]["profile"]
                                [key],
                                pinned[key],
                                (code, language, index, side, key),
                            )

    def test_language_cells_agree(self) -> None:
        for code in FILES:
            self.assertEqual(
                self.artifact["files"][code]["english"],
                self.artifact["files"][code]["latin"], code,
            )

    def test_no_bands_anywhere(self) -> None:
        text = ARTIFACT.read_text()
        for banned in (
            '"verdict"', '"invariants"', '"members_profiles"',
            '"outside"', '"band_low"', '"band_high"',
        ):
            self.assertNotIn(banned, text)
        self.assertIn(
            "no rung band is loaded",
            self.artifact["declared"]["no_band_rule"],
        )
        self.assertIn(
            "no verdict and no scalar margin is produced anywhere",
            self.artifact["declared"]["no_band_rule"],
        )

    def test_module_docstring_declaration(self) -> None:
        doc = Path(homo.__file__).read_text()
        phrases = (
            "Eighteenth declared measurement, the boundary-walk "
            "instrument",
            "the direction tables flip sign at declared boundaries "
            "instead of drifting, so the concentration turns on and "
            "off between spans",
            "move one declared boundary head along declared "
            "positions between the stream's first and second "
            "declared boundaries, price the two spans beside the "
            "head fresh at every position",
            "where the second span's top_1 spike begins and ends "
            "along the stream, and whether the opening span's "
            "above-whole concentration turns off at a declared "
            "location or drifts smoothly across positions",
            "the window mass is fixed at the standing basis "
            "arithmetic's first boundary",
            "so the window mass is ZL 54,604, GC 45,800 and IT "
            "55,133 kept-adjacent pairs",
            "and the head is walked at int(step x the anchor basis) "
            "positions for the declared steps j / 100 with j running "
            "25 to 50 inclusive, 26 heads per file (ZL heads 54,604 "
            "to 109,208, GC 45,800 to 91,600, IT 55,133 to 110,266)",
            "the first head's two spans are exactly the "
            "stream-position instrument's first and second segments "
            "and the last head's two spans exactly its second and "
            "third segments (the declared confluence, verified in "
            "the gate against that instrument's frozen stored "
            "profiles)",
            "no band is loaded, no envelope is formed, no verdict "
            "and no scalar margin is produced anywhere in this "
            "artifact: the declared question is answered by "
            "direction",
            "whether its value sits above, below or equal to the "
            "whole sequence's value at the stored 6-decimal "
            "rounding",
            "the fresh whole-sequence profile verified field for "
            "field against the frozen real-at-basis ladder's anchor "
            "profile",
            "86 fields per cell, 516 fields all told",
            "0 problems, 516 fields compared, the declared 86 per "
            "cell, no divergence in any of them",
            "ZL window 54,604, 26 heads, first 54,604, last 109,208",
            "GC window 45,800, 26 heads, first 45,800, last 91,600",
            "IT window 55,133, 26 heads, first 55,133, last 110,266",
            "all four marks true in every file, ZL "
            "True/True/True/True, GC True/True/True/True, IT "
            "True/True/True/True",
            "the ZL whole row anchors them (kept 218,415 pairs, "
            "68,616 whole boundary-carried pairs, 928 empty types, "
            "self 0.065848, top_1 0.070481, top_10 0.424435, top_50 "
            "0.893671, entropy 4.010179)",
            "and the 26 heads tell this story. The left span's "
            "self runs above for 23 heads (0.083007 at the first "
            "head 54,604, peaking 0.085542 at 63,340) and below at "
            "the last three (0.065626 at 104,839 down to 0.062765 "
            "at 109,208)",
            "it turns off between two declared heads rather than "
            "drifting across them",
            "The left span's top_1 runs below at the first six "
            "heads, above at the seventh and eighth (0.071009 at "
            "67,708 and 0.071104 at 69,893), below at the ninth "
            "(0.069494 at 72,077), and above for the remaining "
            "seventeen (0.070542 at 74,261 rising to 0.089319 at "
            "104,839, 0.088887 at 107,023 and 0.088227 at 109,208)",
            "its top_10 above at all 26 heads, its top_50 above for "
            "23 heads then below for 3, and its entropy below at "
            "all 26 heads",
            "The right span's self runs below at all 26 heads, its "
            "top_1 above for 23 heads (peaking 0.092363 at 61,156) "
            "then below at the last three (0.070293 at 104,839)",
            "its top_10 above for the first 13 heads then below for "
            "the last 13, its top_50 below at all 26 heads, and its "
            "entropy below at the first five heads, above at "
            "65,524, below again at 67,708, and above for the "
            "remaining nineteen",
            "No equal entry appears anywhere in the walk's "
            "direction records, matching the standing expectation, "
            "and the left self's flip and the right top_1's flip "
            "sit between the same two declared heads, 102,655 and "
            "104,839",
        )
        for phrase in phrases:
            self.assertIn(phrase, " ".join(doc.split()), phrase)
        self.assertEqual(
            " ".join(doc.split()).count(
                "nothing here is a reading or a language claim"
            ),
            19,
        )

    def test_the_truthful_question(self) -> None:
        what = self.artifact["what"]
        self.assertIn(
            "with the real's own kept-adjacent pair sequence "
            "walked by one declared boundary head across declared "
            "step positions between the stream's first and second "
            "declared boundaries", what,
        )
        self.assertIn(
            "the two window-mass spans beside the head priced "
            "fresh at every position, the direction tables "
            "recorded at every position, no bands and no "
            "envelopes", what,
        )
        self.assertIn(
            "where the second span's top_1 spike begins and ends "
            "along the stream, and whether the opening span's "
            "above-whole concentration turns off at a declared "
            "location or drifts smoothly across positions", what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading.",
            what,
        )
        state_note = self.artifact["declared"]["state_note"]
        self.assertIn("126 unmapped events inside ZL's 218,663",
                      state_note)
        self.assertIn("1,769 inside GC's 186,708", state_note)
        self.assertIn("none inside IT's 220,532", state_note)
        self.assertIn(
            "the real's side is identical for both languages of a "
            "file", state_note,
        )
        self.assertIn(
            "the whole-sequence profile is anchored to the frozen "
            "real-at-basis ladder's anchor profile in the gate",
            state_note,
        )

    def test_dash_bans(self) -> None:
        for source in (
            ARTIFACT.read_text(),
            Path(homo.__file__).read_text(),
            Path(__file__).read_text(),
        ):
            self.assertNotIn(chr(0x2011), source)
            self.assertNotIn(chr(0x2013), source)
            self.assertNotIn(chr(0x2014), source)


if __name__ == "__main__":
    unittest.main()
