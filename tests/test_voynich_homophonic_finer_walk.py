# The finer-walk suite: the nineteenth measurement's declared
# artifact against its frozen predecessors. Hand constants pin the
# declared finer steps, the gap steps the boundary-walk instrument
# located, the window masses at the standing first boundary and the
# seed-kind registry's unchanged tail; the artifact pins are read
# from the frozen run of 29 October 2026 with the bridge gate
# verified at 252 fields (42 per cell times six cells) and the
# direction tables recorded for every span beside every finer head.
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/"
    "voynich-homophonic-finer-walk.json"
).resolve()
FROZEN_REAL = Path(
    "docs/research-notes/"
    "voynich-homophonic-real-at-basis-ladder.json"
).resolve()
FROZEN_WALK = Path(
    "docs/research-notes/"
    "voynich-homophonic-boundary-walk.json"
).resolve()

SCALAR_KEYS = [
    "empty_type_count", "self_pair_share", "top_1_share",
    "top_10_share", "top_50_share", "pair_entropy",
]

# code -> (kept pairs, window mass, lower step, upper step, first
# head, last head), the window mass exactly the standing first
# boundary's span size and the walk's endpoints exactly the frozen
# boundary-walk instrument's heads at the gap's two hundredth steps,
# every head at an int(step x the anchor basis) position with the
# anchor basis the kept pair total + 1.
GAP_SHAPES = {
    "ZL": (218415, 54604, 470, 480, 102655, 104839),
    "GC": (183199, 45800, 430, 440, 78776, 80608),
    "IT": (220531, 55133, 480, 490, 105855, 108060),
}

# the frozen boundary-walk head-row indexes at each gap's two
# hundredth steps, its steps running j / 100 with j 25 to 50 so its
# row index i sits at the step (25 + i) / 100.
WALK_ROWS = {"ZL": (22, 23), "GC": (18, 19), "IT": (23, 24)}

# the declared spot heads for the scalar pins: the first, the
# middle and the last of the 11, indexes into the stored head rows.
SPOT_HEADS = (0, 5, 10)

# code -> the fresh whole profile's six scalars, read
# from the frozen finer-walk run of 29 October 2026.
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
        "empty_type_count": 1015,
        "self_pair_share": 0.067744,
        "top_1_share": 0.08748,
        "top_10_share": 0.437639,
        "top_50_share": 0.893832,
        "pair_entropy": 3.991647,
    },
    ("ZL", "english", 0, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055391,
        "top_1_share": 0.071656,
        "top_10_share": 0.38946,
        "top_50_share": 0.883967,
        "pair_entropy": 4.080312,
    },
    ("ZL", "english", 5, "left"): {
        "empty_type_count": 1014,
        "self_pair_share": 0.067325,
        "top_1_share": 0.088022,
        "top_10_share": 0.43799,
        "top_50_share": 0.893536,
        "pair_entropy": 3.992424,
    },
    ("ZL", "english", 5, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.056064,
        "top_1_share": 0.071036,
        "top_10_share": 0.390322,
        "top_50_share": 0.883886,
        "pair_entropy": 4.078153,
    },
    ("ZL", "english", 10, "left"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.065626,
        "top_1_share": 0.089319,
        "top_10_share": 0.440176,
        "top_50_share": 0.893005,
        "pair_entropy": 3.992262,
    },
    ("ZL", "english", 10, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.05652,
        "top_1_share": 0.070293,
        "top_10_share": 0.390122,
        "top_50_share": 0.883948,
        "pair_entropy": 4.076501,
    },
    ("ZL", "latin", 0, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067744,
        "top_1_share": 0.08748,
        "top_10_share": 0.437639,
        "top_50_share": 0.893832,
        "pair_entropy": 3.991647,
    },
    ("ZL", "latin", 0, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055391,
        "top_1_share": 0.071656,
        "top_10_share": 0.38946,
        "top_50_share": 0.883967,
        "pair_entropy": 4.080312,
    },
    ("ZL", "latin", 5, "left"): {
        "empty_type_count": 1014,
        "self_pair_share": 0.067325,
        "top_1_share": 0.088022,
        "top_10_share": 0.43799,
        "top_50_share": 0.893536,
        "pair_entropy": 3.992424,
    },
    ("ZL", "latin", 5, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.056064,
        "top_1_share": 0.071036,
        "top_10_share": 0.390322,
        "top_50_share": 0.883886,
        "pair_entropy": 4.078153,
    },
    ("ZL", "latin", 10, "left"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.065626,
        "top_1_share": 0.089319,
        "top_10_share": 0.440176,
        "top_50_share": 0.893005,
        "pair_entropy": 3.992262,
    },
    ("ZL", "latin", 10, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.05652,
        "top_1_share": 0.070293,
        "top_10_share": 0.390122,
        "top_50_share": 0.883948,
        "pair_entropy": 4.076501,
    },
    ("GC", "english", 0, "left"): {
        "empty_type_count": 820,
        "self_pair_share": 0.016324,
        "top_1_share": 0.045946,
        "top_10_share": 0.375315,
        "top_50_share": 0.804577,
        "pair_entropy": 4.427614,
    },
    ("GC", "english", 0, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014868,
        "top_1_share": 0.045926,
        "top_10_share": 0.358756,
        "top_50_share": 0.800536,
        "pair_entropy": 4.463737,
    },
    ("GC", "english", 5, "left"): {
        "empty_type_count": 819,
        "self_pair_share": 0.016188,
        "top_1_share": 0.045789,
        "top_10_share": 0.374459,
        "top_50_share": 0.803829,
        "pair_entropy": 4.431209,
    },
    ("GC", "english", 5, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014787,
        "top_1_share": 0.047039,
        "top_10_share": 0.356811,
        "top_50_share": 0.800664,
        "pair_entropy": 4.463484,
    },
    ("GC", "english", 10, "left"): {
        "empty_type_count": 819,
        "self_pair_share": 0.015417,
        "top_1_share": 0.045711,
        "top_10_share": 0.376192,
        "top_50_share": 0.803185,
        "pair_entropy": 4.431261,
    },
    ("GC", "english", 10, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014844,
        "top_1_share": 0.04803,
        "top_10_share": 0.357979,
        "top_50_share": 0.801599,
        "pair_entropy": 4.461091,
    },
    ("GC", "latin", 0, "left"): {
        "empty_type_count": 820,
        "self_pair_share": 0.016324,
        "top_1_share": 0.045946,
        "top_10_share": 0.375315,
        "top_50_share": 0.804577,
        "pair_entropy": 4.427614,
    },
    ("GC", "latin", 0, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014868,
        "top_1_share": 0.045926,
        "top_10_share": 0.358756,
        "top_50_share": 0.800536,
        "pair_entropy": 4.463737,
    },
    ("GC", "latin", 5, "left"): {
        "empty_type_count": 819,
        "self_pair_share": 0.016188,
        "top_1_share": 0.045789,
        "top_10_share": 0.374459,
        "top_50_share": 0.803829,
        "pair_entropy": 4.431209,
    },
    ("GC", "latin", 5, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014787,
        "top_1_share": 0.047039,
        "top_10_share": 0.356811,
        "top_50_share": 0.800664,
        "pair_entropy": 4.463484,
    },
    ("GC", "latin", 10, "left"): {
        "empty_type_count": 819,
        "self_pair_share": 0.015417,
        "top_1_share": 0.045711,
        "top_10_share": 0.376192,
        "top_50_share": 0.803185,
        "pair_entropy": 4.431261,
    },
    ("GC", "latin", 10, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014844,
        "top_1_share": 0.04803,
        "top_10_share": 0.357979,
        "top_50_share": 0.801599,
        "pair_entropy": 4.461091,
    },
    ("IT", "english", 0, "left"): {
        "empty_type_count": 1051,
        "self_pair_share": 0.066813,
        "top_1_share": 0.090677,
        "top_10_share": 0.444915,
        "top_50_share": 0.899495,
        "pair_entropy": 3.958425,
    },
    ("IT", "english", 0, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054488,
        "top_1_share": 0.072222,
        "top_10_share": 0.393322,
        "top_50_share": 0.885194,
        "pair_entropy": 4.068135,
    },
    ("IT", "english", 5, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.065304,
        "top_1_share": 0.090632,
        "top_10_share": 0.443759,
        "top_50_share": 0.898225,
        "pair_entropy": 3.966696,
    },
    ("IT", "english", 5, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.055499,
        "top_1_share": 0.071993,
        "top_10_share": 0.39454,
        "top_50_share": 0.886458,
        "pair_entropy": 4.060181,
    },
    ("IT", "english", 10, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.064867,
        "top_1_share": 0.090096,
        "top_10_share": 0.442677,
        "top_50_share": 0.897915,
        "pair_entropy": 3.96872,
    },
    ("IT", "english", 10, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056492,
        "top_1_share": 0.071606,
        "top_10_share": 0.395747,
        "top_50_share": 0.886988,
        "pair_entropy": 4.054086,
    },
    ("IT", "latin", 0, "left"): {
        "empty_type_count": 1051,
        "self_pair_share": 0.066813,
        "top_1_share": 0.090677,
        "top_10_share": 0.444915,
        "top_50_share": 0.899495,
        "pair_entropy": 3.958425,
    },
    ("IT", "latin", 0, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054488,
        "top_1_share": 0.072222,
        "top_10_share": 0.393322,
        "top_50_share": 0.885194,
        "pair_entropy": 4.068135,
    },
    ("IT", "latin", 5, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.065304,
        "top_1_share": 0.090632,
        "top_10_share": 0.443759,
        "top_50_share": 0.898225,
        "pair_entropy": 3.966696,
    },
    ("IT", "latin", 5, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.055499,
        "top_1_share": 0.071993,
        "top_10_share": 0.39454,
        "top_50_share": 0.886458,
        "pair_entropy": 4.060181,
    },
    ("IT", "latin", 10, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.064867,
        "top_1_share": 0.090096,
        "top_10_share": 0.442677,
        "top_50_share": 0.897915,
        "pair_entropy": 3.96872,
    },
    ("IT", "latin", 10, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056492,
        "top_1_share": 0.071606,
        "top_10_share": 0.395747,
        "top_50_share": 0.886988,
        "pair_entropy": 4.054086,
    },
}

HEAD_DIRECTIONS = {
    # (code, language, head index, side) -> the span's
    # direction record against the whole profile
    ("ZL", "english", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
}

TRACKED = {
    # code -> the mechanical tracked-flip list read from
    # the frozen finer-walk run (also the rule's replay
    # against the frozen boundary-walk cell, in order)
    "ZL": [{"side": "left", "summary": "self_pair_share", "at_lower": "above", "at_upper": "below"}, {"side": "left", "summary": "top_50_share", "at_lower": "above", "at_upper": "below"}, {"side": "right", "summary": "top_1_share", "at_lower": "above", "at_upper": "below"}],
    "GC": [{"side": "left", "summary": "self_pair_share", "at_lower": "above", "at_upper": "below"}],
    "IT": [{"side": "left", "summary": "self_pair_share", "at_lower": "above", "at_upper": "below"}, {"side": "left", "summary": "top_50_share", "at_lower": "above", "at_upper": "below"}, {"side": "right", "summary": "top_1_share", "at_lower": "above", "at_upper": "below"}],
}
class FinerWalkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_real = json.loads(FROZEN_REAL.read_text())
        self.frozen_walk = json.loads(FROZEN_WALK.read_text())

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.FINE_WALK_STEP_DENOM, 1000)
        self.assertEqual(
            homo.FINE_WALK_GAP_STEPS,
            {"ZL": (470, 480), "GC": (430, 440), "IT": (480, 490)},
        )
        self.assertEqual(
            homo.FINE_WALK_ARTIFACT_PATH.name,
            "voynich-homophonic-finer-walk.json",
        )
        self.assertEqual(max(homo.KIND_ID.values()), 30)
        self.assertEqual(
            homo.KIND_ID["homo_cut_geom"], 30,
            "the seed-kind registry ends at the cut-geometry kind; "
            "the finer-resolution walk instrument draws no seed at "
            "all",
        )
        self.assertEqual(
            sorted(self.artifact["declared"]),
            [
                "base_seed", "boundary_rule", "closure_rule",
                "confluence_rule", "direction_rule", "exclusion_rule",
                "gate_rule", "machinery_rule", "mapped",
                "models_rule", "no_band_rule", "record_rule",
                "roster_rule", "split_rule", "state_note",
                "summary_rule", "tracked_rule", "walk_rule",
            ],
        )
        self.assertEqual(
            self.artifact["declared"]["base_seed"], homo.BASE_SEED,
        )
        self.assertEqual(
            self.artifact["declared"]["mapped"], homo.MAPPED_HOMO,
        )

    def test_gate_replay(self) -> None:
        problems, fields = homo._compare_finer_walk_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 252)
        self.assertEqual(
            self.artifact["bridge_gate"],
            {
                "status": "verified", "fields_compared": 252,
                "per_cell_fields": 42,
            },
        )

    def test_the_declared_shapes(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            kept, mass, lower, upper, first_head, last_head = (
                GAP_SHAPES[code]
            )
            self.assertEqual(cell["kept_pairs"], kept, code)
            self.assertEqual(cell["window_pairs"], mass, code)
            self.assertEqual(
                cell["gap_steps"], {"lower": lower, "upper": upper},
                code,
            )
            heads = cell["heads"]
            self.assertEqual(len(heads), 11, code)
            self.assertEqual(
                heads[0]["head_position"], first_head, code,
            )
            self.assertEqual(
                heads[-1]["head_position"], last_head, code,
            )
            anchor = kept + 1
            steps = tuple(j / 1000 for j in range(lower, upper + 1))
            for index, row in enumerate(heads):
                self.assertEqual(row["step"], steps[index], (code, index))
                self.assertEqual(
                    row["head_position"],
                    int(steps[index] * anchor), (code, index),
                )
            walk_cell = self.frozen_walk["files"][code]["english"]
            spot, tail = WALK_ROWS[code]
            self.assertEqual(
                heads[0]["head_position"],
                walk_cell["heads"][spot]["head_position"], code,
            )
            self.assertEqual(
                heads[-1]["head_position"],
                walk_cell["heads"][tail]["head_position"], code,
            )

    def test_the_whole_gate(self) -> None:
        for code in FILES:
            for language in LANGS:
                fresh = homo._fine_walk_cell(
                    code, self.frozen_walk["files"][code][language],
                )
                stored = self.artifact["files"][code][language]
                self.assertEqual(fresh, stored, (code, language))
                frozen = self.frozen_real["files"][code][language][
                    "rungs"
                ][0]["real_rung_profile"]
                self.assertEqual(
                    stored["whole_profile"], frozen, (code, language),
                )

    def test_the_fine_walk_rebuild(self) -> None:
        for code in FILES:
            first, second = homo._real_pair_sequence(code)
            real = homo._homo_real_stream(code)
            mark = len(real["mapped_chars"]) - 1
            kept, mass, _, _, _, _ = GAP_SHAPES[code]
            anchor = kept + 1
            lower, upper = homo.FINE_WALK_GAP_STEPS[code]
            steps = tuple(j / 1000 for j in range(lower, upper + 1))
            stored = self.artifact["files"][code]["english"]
            whole = stored["whole_profile"]
            self.assertEqual(stored["window_pairs"], mass, code)
            for index, row in enumerate(stored["heads"]):
                head = row["head_position"]
                self.assertEqual(
                    head,
                    int(steps[index] * anchor), (code, index),
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

    def test_confluence_with_the_boundary_walk_records(self) -> None:
        for code in FILES:
            walk_cell = self.frozen_walk["files"][code]["english"]
            cell = self.artifact["files"][code]["english"]
            spot, tail = WALK_ROWS[code]
            lower_row = walk_cell["heads"][spot]
            upper_row = walk_cell["heads"][tail]
            marks = (
                cell["heads"][0]["left"]["profile"]
                == lower_row["left"]["profile"],
                cell["heads"][0]["right"]["profile"]
                == lower_row["right"]["profile"],
                cell["heads"][-1]["left"]["profile"]
                == upper_row["left"]["profile"],
                cell["heads"][-1]["right"]["profile"]
                == upper_row["right"]["profile"],
            )
            self.assertEqual(
                marks, (True, True, True, True), code,
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

    def test_tracked_flips_pins(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            lower, upper = homo.FINE_WALK_GAP_STEPS[code]
            walk_cell = self.frozen_walk["files"][code]["english"]
            mechanical = homo._tracked_flips(walk_cell, lower, upper)
            self.assertEqual(
                cell["tracked_flips"], mechanical, code,
            )
            self.assertEqual(
                cell["tracked_flips"], TRACKED[code], code,
            )

    def test_the_turns_are_single(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            for flip in cell["tracked_flips"]:
                values = [
                    row[flip["side"]]["direction"][flip["summary"]]
                    for row in cell["heads"]
                ]
                n_after = values.count(flip["at_upper"])
                self.assertEqual(values[0], flip["at_lower"], code)
                self.assertEqual(values[-1], flip["at_upper"], code)
                self.assertGreaterEqual(n_after, 1, code)
                self.assertEqual(
                    values,
                    [flip["at_lower"]] * (11 - n_after)
                    + [flip["at_upper"]] * n_after,
                    (code, flip["side"], flip["summary"]),
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
            "Nineteenth declared measurement, the finer-resolution "
            "walk instrument, declared after the boundary-walk "
            "instrument located the direction flips in gaps between "
            "consecutive declared hundredth heads",
            "the walk prices nothing between two consecutive "
            "hundredth heads, so each flip's location is only as "
            "fine as a hundredth of the stream",
            "at which finer position it turns, whether it turns "
            "once or splits into more than one turn, or whether any "
            "of them drifts smoothly across the gap",
            "the window mass is fixed at the standing basis "
            "arithmetic's first boundary",
            "so the window mass is ZL 54,604, GC 45,800 and IT "
            "55,133 kept-adjacent pairs",
            "and the head is walked at int(step x the anchor basis) "
            "positions for the declared steps j / 1000 with j "
            "running over the three declared gaps exactly as the "
            "boundary-walk instrument located them: ZL j 470 to 480 "
            "inclusive, GC j 430 to 440 inclusive, IT j 480 to 490 "
            "inclusive, 11 heads per file, the first and last heads "
            "of each gap exactly the boundary-walk instrument's "
            "recorded heads at that gap's two hundredth steps",
            "The tracked flips are the side and summary direction "
            "records the frozen boundary-walk artifact records as "
            "changing across each gap's two hundredth steps, "
            "computed mechanically from the frozen stored "
            "directions and listed in the artifact, no hand "
            "selection performed over them",
            "the two spans beside the head are the window-mass "
            "span ending at the head and the window-mass span "
            "starting at the head, each priced fresh",
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
            "the four endpoint span profiles verified field for "
            "field against the frozen boundary-walk instrument's "
            "stored profiles at the gap's two hundredth steps",
            "42 fields per cell, 252 fields all told",
            "0 problems, 252 fields compared, the declared 42 per "
            "cell, no divergence in any of them",
            "ZL gap j 470 to 480, window 54,604, 11 heads, first "
            "102,655, last 104,839",
            "GC gap j 430 to 440, window 45,800, 11 heads, first "
            "78,776, last 80,608",
            "IT gap j 480 to 490, window 55,133, 11 heads, first "
            "105,855, last 108,060",
            "ZL 3 tracked flips: left self above to below, left "
            "top_50 above to below, right top_1 above to below; GC "
            "1 tracked flip: left self above to below; IT 3 tracked "
            "flips: left self above to below, left top_50 above to "
            "below, right top_1 above to below",
            "all four endpoint marks true in every file, ZL "
            "True/True/True/True, GC True/True/True/True, IT "
            "True/True/True/True",
            "the ZL whole row anchors them (kept 218,415 pairs, "
            "68,616 whole boundary-carried pairs, 928 empty types, "
            "self 0.065848, top_1 0.070481, top_10 0.424435, top_50 "
            "0.893671, entropy 4.010179)",
            "The left span's self runs above for the first ten "
            "heads (0.067744 at the first head 102,655 down to "
            "0.065864 at 104,621) and below at the last head "
            "(0.065626 at 104,839), so the tracked flip turns at "
            "the gap's last switch, between 104,621 and 104,839, "
            "rather than drifting across the gap",
            "The left span's top_50 runs above at the first head "
            "(0.893832) and below at the remaining ten (0.893639 at "
            "102,873 through 0.893005 at 104,839), so its tracked "
            "flip turns at the gap's first switch, between 102,655 "
            "and 102,873",
            "The right span's top_1 runs above for the first ten "
            "heads (0.071656 at 102,655 through 0.070487 at 104,621) "
            "and below at the last head (0.070293 at 104,839), so "
            "its tracked flip lands between the same two heads that "
            "close the left self's run",
            "The left span's top_1 runs above at all 11 heads "
            "(0.087480 at 102,655 and 0.089319 at 104,839), its "
            "top_10 above at all 11 and its entropy below at "
            "all 11",
            "the right span's self runs below at all 11 heads, its "
            "top_10 below at all 11, its top_50 below at all 11 and "
            "its entropy above at all 11",
            "No equal entry appears anywhere in the ZL fine walk's "
            "direction records, and the gap's three tracked flips "
            "turn at exactly two declared finer switches, the first "
            "switch and the last switch, none splitting and none "
            "drifting",
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
            "walked by one declared boundary head at the declared "
            "finer steps j / 1000 inside the three gaps the "
            "boundary-walk instrument located its flips in", what,
        )
        self.assertIn(
            "the two window-mass spans beside the head priced "
            "fresh at every finer position, the direction tables "
            "recorded at every finer position, no bands and no "
            "envelopes", what,
        )
        self.assertIn(
            "at which finer declared position each tracked "
            "direction flip turns - the tracked flips exactly the "
            "frozen boundary-walk direction records that change "
            "across each gap, computed mechanically - or whether "
            "any of them splits into more than one turn or drifts "
            "smoothly inside its gap", what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading.",
            what,
        )
        tracked_rule = self.artifact["declared"]["tracked_rule"]
        self.assertIn(
            "the tracked flips are exactly the side and summary "
            "direction records the frozen boundary-walk artifact "
            "records as changing across each gap's two hundredth "
            "steps", tracked_rule,
        )
        self.assertIn(
            "computed mechanically from the frozen stored "
            "directions and listed in the artifact, no hand "
            "selection performed over them", tracked_rule,
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
