# The switch-walk suite: the twentieth measurement's declared
# artifact against its frozen predecessors. Hand constants pin the
# declared switch bands the finer-resolution walk instrument located,
# the window masses at the standing first boundary and the seed-kind
# registry's unchanged tail; the artifact pins are read from the
# frozen run of 30 October 2026 with the bridge gate verified at 408
# fields (81 per ZL or IT cell and 42 per GC cell, times six cells)
# and the direction tables recorded for every span beside every
# finer head.
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/"
    "voynich-homophonic-switch-walk.json"
).resolve()
FROZEN_REAL = Path(
    "docs/research-notes/"
    "voynich-homophonic-real-at-basis-ladder.json"
).resolve()
FROZEN_FINE = Path(
    "docs/research-notes/"
    "voynich-homophonic-finer-walk.json"
).resolve()

SCALAR_KEYS = [
    "empty_type_count", "self_pair_share", "top_1_share",
    "top_10_share", "top_50_share", "pair_entropy",
]

# code -> (kept pairs, window mass, the declared bands j / 10000 in
# lower-upper pairs, and each band's (first head, last head)), the
# window mass exactly the standing first boundary's span size and the
# walk's endpoints exactly the frozen finer-walk instrument's stored
# heads at each band's two boundary thousandth steps, every head at
# an int(step x the anchor basis) position with the anchor basis the
# kept pair total + 1.
SWITCH_SHAPES = {
    "ZL": (
        218415, 54604, ((4700, 4710), (4790, 4800)),
        (102655, 102873), (104621, 104839),
    ),
    "GC": (183199, 45800, ((4370, 4380),), (80058, 80241)),
    "IT": (
        220531, 55133, ((4820, 4830), (4890, 4900)),
        (106296, 106516), (107840, 108060),
    ),
}

# The declared answer, read off the stored direction tables: code ->
# (band lower, side, summary) -> the head intervals the tracked
# flip's label changes across, in order.
TURN_PINS = {
    "ZL": {
        (4700, "left", "top_50_share"): [(4709, 4710)],
        (4790, "left", "self_pair_share"): [(4791, 4792)],
        (4790, "right", "top_1_share"): [(4790, 4791)],
    },
    "GC": {(4370, "left", "self_pair_share"): [(4370, 4371)]},
    "IT": {
        (4820, "left", "self_pair_share"): [
            (4825, 4826), (4827, 4828), (4829, 4830),
        ],
        (4820, "left", "top_50_share"): [(4822, 4823)],
        (4890, "right", "top_1_share"): [(4895, 4896)],
    },
}

# the declared spot heads for the scalar pins: the first, the middle
# and the last of each band's 11, indexes into the band's stored head
# rows.
SPOT_HEADS = (0, 5, 10)

# code -> the fresh whole profile's six scalars, read
# from the frozen switch-walk run of 30 October 2026.
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
    # (code, language, switch index, head index, side)
    # -> the span profile's six scalars at the declared
    # spot heads
    ("ZL", "english", 0, 0, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067744,
        "top_1_share": 0.08748,
        "top_10_share": 0.437639,
        "top_50_share": 0.893832,
        "pair_entropy": 3.991647,
    },
    ("ZL", "english", 0, 0, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055391,
        "top_1_share": 0.071656,
        "top_10_share": 0.38946,
        "top_50_share": 0.883967,
        "pair_entropy": 4.080312,
    },
    ("ZL", "english", 0, 5, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067537,
        "top_1_share": 0.087569,
        "top_10_share": 0.437794,
        "top_50_share": 0.893794,
        "pair_entropy": 3.991431,
    },
    ("ZL", "english", 0, 5, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055547,
        "top_1_share": 0.071567,
        "top_10_share": 0.389365,
        "top_50_share": 0.883737,
        "pair_entropy": 4.080818,
    },
    ("ZL", "english", 0, 10, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067641,
        "top_1_share": 0.087618,
        "top_10_share": 0.437663,
        "top_50_share": 0.893639,
        "pair_entropy": 3.991904,
    },
    ("ZL", "english", 0, 10, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055547,
        "top_1_share": 0.071432,
        "top_10_share": 0.389445,
        "top_50_share": 0.883791,
        "pair_entropy": 4.08028,
    },
    ("ZL", "english", 1, 0, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.065864,
        "top_1_share": 0.0891,
        "top_10_share": 0.440394,
        "top_50_share": 0.893494,
        "pair_entropy": 3.990789,
    },
    ("ZL", "english", 1, 0, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.056443,
        "top_1_share": 0.070487,
        "top_10_share": 0.390153,
        "top_50_share": 0.883804,
        "pair_entropy": 4.077394,
    },
    ("ZL", "english", 1, 5, "left"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.065782,
        "top_1_share": 0.089258,
        "top_10_share": 0.440275,
        "top_50_share": 0.893255,
        "pair_entropy": 3.991479,
    },
    ("ZL", "english", 1, 5, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.056473,
        "top_1_share": 0.070383,
        "top_10_share": 0.390121,
        "top_50_share": 0.883959,
        "pair_entropy": 4.076734,
    },
    ("ZL", "english", 1, 10, "left"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.065626,
        "top_1_share": 0.089319,
        "top_10_share": 0.440176,
        "top_50_share": 0.893005,
        "pair_entropy": 3.992262,
    },
    ("ZL", "english", 1, 10, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.05652,
        "top_1_share": 0.070293,
        "top_10_share": 0.390122,
        "top_50_share": 0.883948,
        "pair_entropy": 4.076501,
    },
    ("ZL", "latin", 0, 0, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067744,
        "top_1_share": 0.08748,
        "top_10_share": 0.437639,
        "top_50_share": 0.893832,
        "pair_entropy": 3.991647,
    },
    ("ZL", "latin", 0, 0, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055391,
        "top_1_share": 0.071656,
        "top_10_share": 0.38946,
        "top_50_share": 0.883967,
        "pair_entropy": 4.080312,
    },
    ("ZL", "latin", 0, 5, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067537,
        "top_1_share": 0.087569,
        "top_10_share": 0.437794,
        "top_50_share": 0.893794,
        "pair_entropy": 3.991431,
    },
    ("ZL", "latin", 0, 5, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055547,
        "top_1_share": 0.071567,
        "top_10_share": 0.389365,
        "top_50_share": 0.883737,
        "pair_entropy": 4.080818,
    },
    ("ZL", "latin", 0, 10, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.067641,
        "top_1_share": 0.087618,
        "top_10_share": 0.437663,
        "top_50_share": 0.893639,
        "pair_entropy": 3.991904,
    },
    ("ZL", "latin", 0, 10, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.055547,
        "top_1_share": 0.071432,
        "top_10_share": 0.389445,
        "top_50_share": 0.883791,
        "pair_entropy": 4.08028,
    },
    ("ZL", "latin", 1, 0, "left"): {
        "empty_type_count": 1015,
        "self_pair_share": 0.065864,
        "top_1_share": 0.0891,
        "top_10_share": 0.440394,
        "top_50_share": 0.893494,
        "pair_entropy": 3.990789,
    },
    ("ZL", "latin", 1, 0, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.056443,
        "top_1_share": 0.070487,
        "top_10_share": 0.390153,
        "top_50_share": 0.883804,
        "pair_entropy": 4.077394,
    },
    ("ZL", "latin", 1, 5, "left"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.065782,
        "top_1_share": 0.089258,
        "top_10_share": 0.440275,
        "top_50_share": 0.893255,
        "pair_entropy": 3.991479,
    },
    ("ZL", "latin", 1, 5, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.056473,
        "top_1_share": 0.070383,
        "top_10_share": 0.390121,
        "top_50_share": 0.883959,
        "pair_entropy": 4.076734,
    },
    ("ZL", "latin", 1, 10, "left"): {
        "empty_type_count": 1016,
        "self_pair_share": 0.065626,
        "top_1_share": 0.089319,
        "top_10_share": 0.440176,
        "top_50_share": 0.893005,
        "pair_entropy": 3.992262,
    },
    ("ZL", "latin", 1, 10, "right"): {
        "empty_type_count": 1004,
        "self_pair_share": 0.05652,
        "top_1_share": 0.070293,
        "top_10_share": 0.390122,
        "top_50_share": 0.883948,
        "pair_entropy": 4.076501,
    },
    ("GC", "english", 0, 0, "left"): {
        "empty_type_count": 818,
        "self_pair_share": 0.015943,
        "top_1_share": 0.045917,
        "top_10_share": 0.375487,
        "top_50_share": 0.803383,
        "pair_entropy": 4.431143,
    },
    ("GC", "english", 0, 0, "right"): {
        "empty_type_count": 810,
        "self_pair_share": 0.014715,
        "top_1_share": 0.047287,
        "top_10_share": 0.35712,
        "top_50_share": 0.801171,
        "pair_entropy": 4.462909,
    },
    ("GC", "english", 0, 5, "left"): {
        "empty_type_count": 818,
        "self_pair_share": 0.015872,
        "top_1_share": 0.04585,
        "top_10_share": 0.3756,
        "top_50_share": 0.803326,
        "pair_entropy": 4.431362,
    },
    ("GC", "english", 0, 5, "right"): {
        "empty_type_count": 810,
        "self_pair_share": 0.014714,
        "top_1_share": 0.047463,
        "top_10_share": 0.357309,
        "top_50_share": 0.801079,
        "pair_entropy": 4.463281,
    },
    ("GC", "english", 0, 10, "left"): {
        "empty_type_count": 817,
        "self_pair_share": 0.015732,
        "top_1_share": 0.045897,
        "top_10_share": 0.375695,
        "top_50_share": 0.803024,
        "pair_entropy": 4.432483,
    },
    ("GC", "english", 0, 10, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014713,
        "top_1_share": 0.047566,
        "top_10_share": 0.357533,
        "top_50_share": 0.801343,
        "pair_entropy": 4.462085,
    },
    ("GC", "latin", 0, 0, "left"): {
        "empty_type_count": 818,
        "self_pair_share": 0.015943,
        "top_1_share": 0.045917,
        "top_10_share": 0.375487,
        "top_50_share": 0.803383,
        "pair_entropy": 4.431143,
    },
    ("GC", "latin", 0, 0, "right"): {
        "empty_type_count": 810,
        "self_pair_share": 0.014715,
        "top_1_share": 0.047287,
        "top_10_share": 0.35712,
        "top_50_share": 0.801171,
        "pair_entropy": 4.462909,
    },
    ("GC", "latin", 0, 5, "left"): {
        "empty_type_count": 818,
        "self_pair_share": 0.015872,
        "top_1_share": 0.04585,
        "top_10_share": 0.3756,
        "top_50_share": 0.803326,
        "pair_entropy": 4.431362,
    },
    ("GC", "latin", 0, 5, "right"): {
        "empty_type_count": 810,
        "self_pair_share": 0.014714,
        "top_1_share": 0.047463,
        "top_10_share": 0.357309,
        "top_50_share": 0.801079,
        "pair_entropy": 4.463281,
    },
    ("GC", "latin", 0, 10, "left"): {
        "empty_type_count": 817,
        "self_pair_share": 0.015732,
        "top_1_share": 0.045897,
        "top_10_share": 0.375695,
        "top_50_share": 0.803024,
        "pair_entropy": 4.432483,
    },
    ("GC", "latin", 0, 10, "right"): {
        "empty_type_count": 811,
        "self_pair_share": 0.014713,
        "top_1_share": 0.047566,
        "top_10_share": 0.357533,
        "top_50_share": 0.801343,
        "pair_entropy": 4.462085,
    },
    ("IT", "english", 0, 0, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.066156,
        "top_1_share": 0.090662,
        "top_10_share": 0.444127,
        "top_50_share": 0.898742,
        "pair_entropy": 3.962718,
    },
    ("IT", "english", 0, 0, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054706,
        "top_1_share": 0.072193,
        "top_10_share": 0.393914,
        "top_50_share": 0.885362,
        "pair_entropy": 4.066207,
    },
    ("IT", "english", 0, 5, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.065884,
        "top_1_share": 0.090798,
        "top_10_share": 0.4441,
        "top_50_share": 0.898525,
        "pair_entropy": 3.963632,
    },
    ("IT", "english", 0, 5, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054788,
        "top_1_share": 0.072083,
        "top_10_share": 0.394023,
        "top_50_share": 0.885717,
        "pair_entropy": 4.065258,
    },
    ("IT", "english", 0, 10, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.065748,
        "top_1_share": 0.090907,
        "top_10_share": 0.444426,
        "top_50_share": 0.898633,
        "pair_entropy": 3.963182,
    },
    ("IT", "english", 0, 10, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054837,
        "top_1_share": 0.072021,
        "top_10_share": 0.394172,
        "top_50_share": 0.885703,
        "pair_entropy": 4.064918,
    },
    ("IT", "english", 1, 0, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.064999,
        "top_1_share": 0.090173,
        "top_10_share": 0.443115,
        "top_50_share": 0.898111,
        "pair_entropy": 3.967737,
    },
    ("IT", "english", 1, 0, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056095,
        "top_1_share": 0.071868,
        "top_10_share": 0.395561,
        "top_50_share": 0.886881,
        "pair_entropy": 4.055477,
    },
    ("IT", "english", 1, 5, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.06492,
        "top_1_share": 0.090121,
        "top_10_share": 0.442937,
        "top_50_share": 0.898026,
        "pair_entropy": 3.96844,
    },
    ("IT", "english", 1, 5, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056333,
        "top_1_share": 0.071694,
        "top_10_share": 0.395752,
        "top_50_share": 0.886979,
        "pair_entropy": 4.054616,
    },
    ("IT", "english", 1, 10, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.064867,
        "top_1_share": 0.090096,
        "top_10_share": 0.442677,
        "top_50_share": 0.897915,
        "pair_entropy": 3.96872,
    },
    ("IT", "english", 1, 10, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056492,
        "top_1_share": 0.071606,
        "top_10_share": 0.395747,
        "top_50_share": 0.886988,
        "pair_entropy": 4.054086,
    },
    ("IT", "latin", 0, 0, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.066156,
        "top_1_share": 0.090662,
        "top_10_share": 0.444127,
        "top_50_share": 0.898742,
        "pair_entropy": 3.962718,
    },
    ("IT", "latin", 0, 0, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054706,
        "top_1_share": 0.072193,
        "top_10_share": 0.393914,
        "top_50_share": 0.885362,
        "pair_entropy": 4.066207,
    },
    ("IT", "latin", 0, 5, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.065884,
        "top_1_share": 0.090798,
        "top_10_share": 0.4441,
        "top_50_share": 0.898525,
        "pair_entropy": 3.963632,
    },
    ("IT", "latin", 0, 5, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054788,
        "top_1_share": 0.072083,
        "top_10_share": 0.394023,
        "top_50_share": 0.885717,
        "pair_entropy": 4.065258,
    },
    ("IT", "latin", 0, 10, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.065748,
        "top_1_share": 0.090907,
        "top_10_share": 0.444426,
        "top_50_share": 0.898633,
        "pair_entropy": 3.963182,
    },
    ("IT", "latin", 0, 10, "right"): {
        "empty_type_count": 1031,
        "self_pair_share": 0.054837,
        "top_1_share": 0.072021,
        "top_10_share": 0.394172,
        "top_50_share": 0.885703,
        "pair_entropy": 4.064918,
    },
    ("IT", "latin", 1, 0, "left"): {
        "empty_type_count": 1050,
        "self_pair_share": 0.064999,
        "top_1_share": 0.090173,
        "top_10_share": 0.443115,
        "top_50_share": 0.898111,
        "pair_entropy": 3.967737,
    },
    ("IT", "latin", 1, 0, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056095,
        "top_1_share": 0.071868,
        "top_10_share": 0.395561,
        "top_50_share": 0.886881,
        "pair_entropy": 4.055477,
    },
    ("IT", "latin", 1, 5, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.06492,
        "top_1_share": 0.090121,
        "top_10_share": 0.442937,
        "top_50_share": 0.898026,
        "pair_entropy": 3.96844,
    },
    ("IT", "latin", 1, 5, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056333,
        "top_1_share": 0.071694,
        "top_10_share": 0.395752,
        "top_50_share": 0.886979,
        "pair_entropy": 4.054616,
    },
    ("IT", "latin", 1, 10, "left"): {
        "empty_type_count": 1049,
        "self_pair_share": 0.064867,
        "top_1_share": 0.090096,
        "top_10_share": 0.442677,
        "top_50_share": 0.897915,
        "pair_entropy": 3.96872,
    },
    ("IT", "latin", 1, 10, "right"): {
        "empty_type_count": 1032,
        "self_pair_share": 0.056492,
        "top_1_share": 0.071606,
        "top_10_share": 0.395747,
        "top_50_share": 0.886988,
        "pair_entropy": 4.054086,
    },
}

HEAD_DIRECTIONS = {
    # (code, language, switch index, head index, side)
    # -> the span's direction record against the whole
    # profile
    ("ZL", "english", 0, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 0, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 0, 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 0, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 2, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 1, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 1, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 6, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 7, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 0, 10, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 0, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 2, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 1, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 1, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 1, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 2, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 0, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 1, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 2, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 0, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 0, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 0, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 0, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 0, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 0, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 0, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 1, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 2, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 1, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 1, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 0, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 0, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 1, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 0, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 2, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 0, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 3, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 4, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 5, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 8, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 9, "left"): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 0, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 0, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 0, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 0, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 1, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 1, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 2, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 2, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 3, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 3, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 4, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 4, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 5, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 5, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 6, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 6, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 7, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 7, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 8, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 8, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 9, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 9, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 1, 10, "left"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 1, 10, "right"): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
}

TRACKED = {
    # code -> the mechanical tracked-flip list read from
    # the frozen switch-walk run (also the rule's replay
    # against the frozen finer-walk cell, in order)
    "ZL": [{"side": 'left', "summary": 'top_50_share', "at_lower": 'above', "at_upper": 'below', "lower": 4700, "upper": 4710, "lower_position": 102655, "upper_position": 102873}, {"side": 'left', "summary": 'self_pair_share', "at_lower": 'above', "at_upper": 'below', "lower": 4790, "upper": 4800, "lower_position": 104621, "upper_position": 104839}, {"side": 'right', "summary": 'top_1_share', "at_lower": 'above', "at_upper": 'below', "lower": 4790, "upper": 4800, "lower_position": 104621, "upper_position": 104839}],
    "GC": [{"side": 'left', "summary": 'self_pair_share', "at_lower": 'above', "at_upper": 'below', "lower": 4370, "upper": 4380, "lower_position": 80058, "upper_position": 80241}],
    "IT": [{"side": 'left', "summary": 'self_pair_share', "at_lower": 'above', "at_upper": 'below', "lower": 4820, "upper": 4830, "lower_position": 106296, "upper_position": 106516}, {"side": 'left', "summary": 'top_50_share', "at_lower": 'above', "at_upper": 'below', "lower": 4820, "upper": 4830, "lower_position": 106296, "upper_position": 106516}, {"side": 'right', "summary": 'top_1_share', "at_lower": 'above', "at_upper": 'below', "lower": 4890, "upper": 4900, "lower_position": 107840, "upper_position": 108060}],
}

class SwitchWalkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_real = json.loads(FROZEN_REAL.read_text())
        self.frozen_fine = json.loads(FROZEN_FINE.read_text())

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.SWITCH_WALK_STEP_DENOM, 10000)
        self.assertEqual(
            homo.SWITCH_WALK_SWITCH_STEPS,
            {
                "ZL": ((4700, 4710), (4790, 4800)),
                "GC": ((4370, 4380),),
                "IT": ((4820, 4830), (4890, 4900)),
            },
        )
        self.assertEqual(
            homo.SWITCH_WALK_ARTIFACT_PATH.name,
            "voynich-homophonic-switch-walk.json",
        )
        self.assertEqual(max(homo.KIND_ID.values()), 30)
        self.assertEqual(
            homo.KIND_ID["homo_cut_geom"], 30,
            "the seed-kind registry ends at the cut-geometry kind; "
            "the switch-walk instrument draws no seed at all",
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
        problems, fields = homo._compare_switch_walk_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 408)
        self.assertEqual(
            self.artifact["bridge_gate"],
            {
                "status": "verified", "fields_compared": 408,
                "per_cell_fields": {"ZL": 81, "GC": 42, "IT": 81},
            },
        )

    def test_the_declared_shapes(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            kept, mass, bands, *band_ends = SWITCH_SHAPES[code]
            self.assertEqual(cell["kept_pairs"], kept, code)
            self.assertEqual(cell["window_pairs"], mass, code)
            self.assertEqual(
                tuple(
                    (band["lower"], band["upper"])
                    for band in cell["switches"]
                ),
                bands, code,
            )
            anchor = kept + 1
            for band_index, (lower, upper) in enumerate(bands):
                heads = cell["switches"][band_index]["heads"]
                self.assertEqual(len(heads), 11, (code, band_index))
                steps = tuple(
                    j / 10000 for j in range(lower, upper + 1)
                )
                for index, row in enumerate(heads):
                    self.assertEqual(
                        row["head_j"], lower + index,
                        (code, band_index, index),
                    )
                    self.assertEqual(
                        row["step"], steps[index],
                        (code, band_index, index),
                    )
                    self.assertEqual(
                        row["head_position"],
                        int(steps[index] * anchor),
                        (code, band_index, index),
                    )
                self.assertEqual(
                    heads[0]["head_position"],
                    band_ends[band_index][0],
                    (code, band_index),
                )
                self.assertEqual(
                    heads[-1]["head_position"],
                    band_ends[band_index][1],
                    (code, band_index),
                )

    def test_the_whole_gate(self) -> None:
        for code in FILES:
            for language in LANGS:
                fresh = homo._switch_walk_cell(
                    code, self.frozen_fine["files"][code][language],
                )
                stored = self.artifact["files"][code][language]
                self.assertEqual(fresh, stored, (code, language))
                frozen = self.frozen_real["files"][code][language][
                    "rungs"
                ][0]["real_rung_profile"]
                self.assertEqual(
                    stored["whole_profile"], frozen, (code, language),
                )

    def test_the_switch_walk_rebuild(self) -> None:
        for code in FILES:
            first, second = homo._real_pair_sequence(code)
            real = homo._homo_real_stream(code)
            mark = len(real["mapped_chars"]) - 1
            kept, mass, bands, *_ = SWITCH_SHAPES[code]
            anchor = kept + 1
            stored = self.artifact["files"][code]["english"]
            whole = stored["whole_profile"]
            self.assertEqual(stored["window_pairs"], mass, code)
            for band_index, (lower, upper) in enumerate(bands):
                heads = stored["switches"][band_index]["heads"]
                steps = tuple(
                    j / 10000 for j in range(lower, upper + 1)
                )
                for index, row in enumerate(heads):
                    head = row["head_position"]
                    self.assertEqual(
                        head, int(steps[index] * anchor),
                        (code, band_index, index),
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
                        carried = homo._boundary_carried_pairs(
                            matrix, mark
                        )
                        span = row[side]
                        self.assertEqual(
                            profile, span["profile"],
                            (code, band_index, index, side),
                        )
                        self.assertEqual(
                            carried, span["boundary_carried_pairs"],
                            (code, band_index, index, side),
                        )
                        self.assertEqual(
                            span["profile"]["total_pairs"],
                            span["pairs"] - carried,
                            (code, band_index, index, side),
                        )
                        self.assertEqual(
                            span["first_position"], start,
                            (code, band_index, index, side),
                        )
                        self.assertEqual(
                            span["end_position"], start + mass,
                            (code, band_index, index, side),
                        )
                        fresh = homo._direction_vs_whole(
                            profile, whole,
                        )
                        self.assertEqual(
                            fresh, span["direction"],
                            (code, band_index, index, side),
                        )
                        pinned = HEAD_DIRECTIONS[
                            (code, "english", band_index, index, side)
                        ]
                        self.assertEqual(
                            span["direction"], pinned,
                            (code, band_index, index, side),
                        )

    def test_the_direction_table(self) -> None:
        for code in FILES:
            for language in LANGS:
                stored = self.artifact["files"][code][language]
                whole = stored["whole_profile"]
                for band_index, band in enumerate(stored["switches"]):
                    for index, row in enumerate(band["heads"]):
                        for side in ("left", "right"):
                            fresh = homo._direction_vs_whole(
                                row[side]["profile"], whole,
                            )
                            self.assertEqual(
                                fresh, row[side]["direction"],
                                (code, language, band_index, index,
                                 side),
                            )
                            pinned = HEAD_DIRECTIONS[
                                (code, language, band_index, index,
                                 side)
                            ]
                            self.assertEqual(
                                row[side]["direction"], pinned,
                                (code, language, band_index, index,
                                 side),
                            )

    def test_confluence_with_the_finer_walk_records(self) -> None:
        for code in FILES:
            fine_cell = self.frozen_fine["files"][code]["english"]
            cell = self.artifact["files"][code]["english"]
            positions = {
                row["head_position"]: row
                for row in fine_cell["heads"]
            }
            for band_index, band in enumerate(cell["switches"]):
                heads = band["heads"]
                self.assertIn(
                    heads[0]["head_position"], positions, code,
                )
                self.assertIn(
                    heads[-1]["head_position"], positions, code,
                )
                lower_row = positions[heads[0]["head_position"]]
                upper_row = positions[heads[-1]["head_position"]]
                self.assertEqual(
                    heads[0]["head_position"],
                    lower_row["head_position"],
                    (code, band_index),
                )
                self.assertEqual(
                    heads[-1]["head_position"],
                    upper_row["head_position"],
                    (code, band_index),
                )
                marks = (
                    heads[0]["left"]["profile"]
                    == lower_row["left"]["profile"],
                    heads[0]["right"]["profile"]
                    == lower_row["right"]["profile"],
                    heads[-1]["left"]["profile"]
                    == upper_row["left"]["profile"],
                    heads[-1]["right"]["profile"]
                    == upper_row["right"]["profile"],
                )
                self.assertEqual(
                    marks, (True, True, True, True),
                    (code, band_index),
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
                for band_index in range(len(cell["switches"])):
                    for index in SPOT_HEADS:
                        for side in ("left", "right"):
                            pinned = SPAN_SCALARS[
                                (code, language, band_index, index,
                                 side)
                            ]
                            for key in SCALAR_KEYS:
                                self.assertEqual(
                                    cell["switches"][band_index][
                                        "heads"
                                    ][index][side]["profile"][key],
                                    pinned[key],
                                    (code, language, band_index,
                                     index, side, key),
                                )

    def test_tracked_flips_pins(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            mechanical = []
            fine_cell = self.frozen_fine["files"][code]["english"]
            for lower, upper in homo.SWITCH_WALK_SWITCH_STEPS[code]:
                mechanical.extend(
                    homo._switch_walk_flips(fine_cell, lower, upper)
                )
            self.assertEqual(
                cell["tracked_flips"], mechanical, code,
            )
            self.assertEqual(
                cell["tracked_flips"], TRACKED[code], code,
            )

    def test_the_tracked_turns(self) -> None:
        singles = 0
        splits = 0
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            for band in cell["switches"]:
                lower, upper = band["lower"], band["upper"]
                for flip in cell["tracked_flips"]:
                    if flip["lower"] != lower:
                        continue
                    values = [
                        row[flip["side"]]["direction"][
                            flip["summary"]
                        ]
                        for row in band["heads"]
                    ]
                    self.assertEqual(
                        values[0], flip["at_lower"],
                        (code, lower, flip["side"]),
                    )
                    self.assertEqual(
                        values[-1], flip["at_upper"],
                        (code, lower, flip["side"]),
                    )
                    change_js = [
                        (lower + i, lower + i + 1)
                        for i in range(len(values) - 1)
                        if values[i] != values[i + 1]
                    ]
                    self.assertEqual(
                        change_js,
                        TURN_PINS[code][
                            (lower, flip["side"], flip["summary"])
                        ],
                        (code, lower, flip["side"],
                         flip["summary"]),
                    )
                    if len(change_js) == 1:
                        singles += 1
                    else:
                        splits += 1
        self.assertEqual((singles, splits), (6, 1))

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
            "Twentieth declared measurement, the switch walk "
            "instrument, declared after the finer-resolution walk "
            "instrument walked the eleven declared thousandth heads",
            "not one of its 792 direction entries records equal, "
            "and every tracked turn landed between two consecutive "
            "declared thousandth heads",
            "so each flip's location is only as fine as a "
            "thousandth of the stream",
            "whether the shared bands' paired flips stay together "
            "or separate",
            "ZL j 4700 to 4710 inclusive and j 4790 to 4800 "
            "inclusive, GC j 4370 to 4380 inclusive, IT j 4820 to "
            "4830 inclusive and j 4890 to 4900 inclusive, 11 heads "
            "per switch band, the first and last heads of each "
            "band exactly the finer-resolution walk instrument's "
            "stored heads at that band's two boundary thousandth "
            "steps",
            "matched by head position and verified in the gate "
            "against that instrument's frozen stored head records, "
            "no float step equality asserted anywhere",
            "computed mechanically from the frozen stored "
            "directions and listed in the artifact band by band, "
            "no hand selection performed over them",
            "no band is loaded, no envelope is formed, no verdict "
            "and no scalar margin is produced anywhere in this "
            "artifact: the declared question is answered by "
            "direction",
            "whether its value sits above, below or equal to the "
            "whole sequence's value at the stored 6-decimal "
            "rounding",
            "the four endpoint span profiles verified field for "
            "field against the frozen finer-walk instrument's "
            "stored profiles at the band's two boundary steps",
            "81 fields per ZL or IT cell (two switch bands), 42 "
            "fields per GC cell (one switch band), 408 fields all "
            "told",
            "0 problems, 408 fields compared, the declared 81 per "
            "ZL or IT cell and 42 per GC cell, no divergence in "
            "any of them",
            "ZL band j 4700 to 4710, window 54,604, 11 heads, "
            "first 102,655, last 102,873; ZL band j 4790 to 4800, "
            "window 54,604, 11 heads, first 104,621, last 104,839",
            "GC band j 4370 to 4380, window 45,800, 11 heads, "
            "first 80,058, last 80,241",
            "IT band j 4820 to 4830, window 55,133, 11 heads, "
            "first 106,296, last 106,516; IT band j 4890 to 4900, "
            "window 55,133, 11 heads, first 107,840, last 108,060",
            "ZL band j 4700 to 4710, 1 tracked flip: left top_50 "
            "above to below; ZL band j 4790 to 4800, 2 tracked "
            "flips: left self above to below and right top_1 "
            "above to below; GC band j 4370 to 4380, 1 tracked "
            "flip: left self above to below; IT band j 4820 to "
            "4830, 2 tracked flips: left self above to below and "
            "left top_50 above to below; IT band j 4890 to 4900, "
            "1 tracked flip: right top_1 above to below",
            "the six fresh cells' direction records total 1,320 "
            "entries, none equal",
            "the ZL whole row anchors them (kept 218,415 pairs, "
            "68,616 whole boundary-carried pairs, 928 empty types, "
            "self 0.065848, top_1 0.070481, top_10 0.424435, top_50 "
            "0.893671, entropy 4.010179)",
            "In the first band (j 4700 to 4710, heads 102,655 to "
            "102,873) the left span's top_50 runs above at the "
            "band's first ten heads (0.893832 at 102,655 through "
            "0.893692 at 102,852) and below at the last (0.893639 "
            "at 102,873), so its tracked flip turns once, between "
            "j 4709 and j 4710, at the band's closing step",
            "In the second band (j 4790 to 4800, heads 104,621 to "
            "104,839) the two tracked flips separate: the right "
            "span's top_1 turns first, above only at the band's "
            "first head (0.070487 at 104,621) and below at the "
            "remaining heads (0.070460 at 104,643 through 0.070293 "
            "at 104,839), so it turns between j 4790 and j 4791",
            "the left span's self holds above two heads (0.065864 "
            "at 104,621 and 0.065886 at 104,643) and turns between "
            "j 4791 and j 4792, below from 0.065811 at 104,664 "
            "down to 0.065626 at 104,839",
            "No equal entry appears anywhere in the ZL switch "
            "walk's direction records: the gap's three tracked "
            "flips each turn once at the finer steps, none "
            "splitting and none drifting, and the two flips that "
            "shared the second band at the finer walk's thousandth "
            "steps separate, the right top_1 turning one declared "
            "ten-thousandth step before the left self",
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
            "finer steps j / 10000 across the five switch bands "
            "the finer-resolution walk instrument located (ZL j "
            "4700 to 4710 and j 4790 to 4800, GC j 4370 to 4380, "
            "IT j 4820 to 4830 and j 4890 to 4900),", what,
        )
        self.assertIn(
            "the two window-mass spans beside the head priced "
            "fresh at every finer position, the direction tables "
            "recorded at every finer position, no rung bands and "
            "no envelopes", what,
        )
        self.assertIn(
            "at which declared ten-thousandth position each "
            "tracked direction flip turns - the tracked flips "
            "exactly the frozen finer-walk direction records that "
            "change across each switch band's two boundary heads, "
            "computed mechanically - and whether each turns once "
            "or splits into more than one turn, whether the "
            "shared bands' paired flips stay together or separate, "
            "or whether any of them drifts smoothly inside its "
            "band", what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading.",
            what,
        )
        tracked_rule = self.artifact["declared"]["tracked_rule"]
        self.assertIn(
            "the tracked flips are exactly the side and summary "
            "direction records the frozen finer-walk artifact "
            "records as changing across each switch band's two "
            "boundary heads", tracked_rule,
        )
        self.assertIn(
            "computed mechanically from the frozen stored "
            "directions and listed in the artifact band by band, "
            "no hand selection performed over them", tracked_rule,
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
        confluence_rule = self.artifact["declared"][
            "confluence_rule"
        ]
        self.assertIn(
            "matched by head position, no float step equality "
            "asserted anywhere", confluence_rule,
        )
        self.assertIn(
            "each band's first head is that instrument's stored "
            "head at the band's lower boundary thousandth step",
            confluence_rule,
        )
        machinery_rule = self.artifact["declared"]["machinery_rule"]
        self.assertIn("no seed of any kind", machinery_rule)

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
