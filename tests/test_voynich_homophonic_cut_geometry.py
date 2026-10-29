# The cut-geometry attribution suite: the sixteenth measurement's
# declared artifact against its frozen predecessors. Hand constants
# pin the rung bases, the seed kind, the geometry order and the
# real record; the artifact pins are read from the frozen run of
# 28 October 2026 with the bridge gate verified at 813 fields (the
# real-at-basis ladder's 693 anchors plus the 120 prefix-rung replay
# checks) and every geometry rung-cell verdict priced over all 144.
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/"
    "voynich-homophonic-cut-geometry-attribution.json"
).resolve()
FROZEN_REAL = Path(
    "docs/research-notes/"
    "voynich-homophonic-real-at-basis-ladder.json"
).resolve()
FROZEN_LADDER = Path(
    "docs/research-notes/"
    "voynich-homophonic-matched-basis-ladder.json"
).resolve()
FROZEN_MATCHED = Path(
    "docs/research-notes/"
    "voynich-homophonic-matched-truncation.json"
).resolve()

# The declared rungs, anchor first.
RUNGS = (1.0, 0.75, 0.5, 0.25)

# The declared geometry rows per rung record, the suffix cut first,
# then the four random seeds in declared order; each rung's fresh
# rows live on its rung record's geometries list in this order, and
# the prefix row is the real-at-basis ladder's own rung record.
GEOM_NAMES = ("suffix", "seed0", "seed1", "seed2", "seed3")
GEOMS = ("suffix", "random", "random", "random", "random")
SEEDS = (None, 0, 1, 2, 3)

OUTSIDE_ALL = [
    "symbol_shares", "pair_shares", "empty_type_count",
    "self_pair_share", "top_1_share", "top_10_share",
    "top_50_share", "pair_entropy",
]
SCALAR_KEYS = [
    "empty_type_count", "self_pair_share", "top_1_share",
    "top_10_share", "top_50_share", "pair_entropy",
]

# code -> (anchor basis, then the 75, 50 and 25 percent rung bases),
# each descended rung floor(p x the anchor basis) tokens.
RUNG_BASES = {
    "ZL": (218416, 163812, 109208, 54604),
    "GC": (183200, 137400, 91600, 45800),
    "IT": (220532, 165399, 110266, 55133),
}

# code -> the record triple (stream_events, unmapped_events,
# kept_pairs, standing plant length) and the anchor basis = kept + 1.
REAL = {
    "ZL": (218663, 126, 218415, 218663, 218416),
    "GC": (186708, 1769, 183199, 186708, 183200),
    "IT": (220532, 0, 220531, 220532, 220532),
}

# code -> the anchor rung's boundary-carried pairs (the whole
# sequence's mark-carried pairs, every geometry's own at the anchor
# by the degenerate identity).
CARRIED_ANCHOR = {"ZL": 68616, "GC": 71384, "IT": 72880}

# the ZL english suffix row's carried pairs at the anchor, 75, 50
# and 25 percent rungs, pinned from the probes.
SUFFIX_CARRIED_ZL = (68616, 52045, 34516, 17176)
# The per-cell per-geometry scalar pins, read from the
# frozen cut-geometry run of 28 October 2026: each pin
# is a (real, band_low, band_high) triple from the row's
# declared envelope, the geometry row's re-priced six
# scalars beside the frozen matched-basis ladder's band
# at its rung width.
GEOM_PIN = {
    ("ZL", "english"): {
        1.0: {
            "suffix": {
                "empty_type_count": (928, 323, 454),
                "self_pair_share": (0.065848, 0.018692, 0.026719),
                "top_1_share": (0.070481, 0.018187, 0.035877),
                "top_10_share": (0.424435, 0.106088, 0.148334),
                "top_50_share": (0.893671, 0.305696, 0.355757),
                "pair_entropy": (4.010179, 5.928491, 6.102985),
            },
            "seed0": {
                "empty_type_count": (928, 323, 454),
                "self_pair_share": (0.065848, 0.018692, 0.026719),
                "top_1_share": (0.070481, 0.018187, 0.035877),
                "top_10_share": (0.424435, 0.106088, 0.148334),
                "top_50_share": (0.893671, 0.305696, 0.355757),
                "pair_entropy": (4.010179, 5.928491, 6.102985),
            },
            "seed1": {
                "empty_type_count": (928, 323, 454),
                "self_pair_share": (0.065848, 0.018692, 0.026719),
                "top_1_share": (0.070481, 0.018187, 0.035877),
                "top_10_share": (0.424435, 0.106088, 0.148334),
                "top_50_share": (0.893671, 0.305696, 0.355757),
                "pair_entropy": (4.010179, 5.928491, 6.102985),
            },
            "seed2": {
                "empty_type_count": (928, 323, 454),
                "self_pair_share": (0.065848, 0.018692, 0.026719),
                "top_1_share": (0.070481, 0.018187, 0.035877),
                "top_10_share": (0.424435, 0.106088, 0.148334),
                "top_50_share": (0.893671, 0.305696, 0.355757),
                "pair_entropy": (4.010179, 5.928491, 6.102985),
            },
            "seed3": {
                "empty_type_count": (928, 323, 454),
                "self_pair_share": (0.065848, 0.018692, 0.026719),
                "top_1_share": (0.070481, 0.018187, 0.035877),
                "top_10_share": (0.424435, 0.106088, 0.148334),
                "top_50_share": (0.893671, 0.305696, 0.355757),
                "pair_entropy": (4.010179, 5.928491, 6.102985),
            },
        },
        0.75: {
            "suffix": {
                "empty_type_count": (942, 318, 464),
                "self_pair_share": (0.060009, 0.01884, 0.027095),
                "top_1_share": (0.072428, 0.018173, 0.035196),
                "top_10_share": (0.415296, 0.106088, 0.157183),
                "top_50_share": (0.888714, 0.305696, 0.368859),
                "pair_entropy": (4.031522, 5.92046, 6.115742),
            },
            "seed0": {
                "empty_type_count": (950, 318, 464),
                "self_pair_share": (0.065902, 0.01884, 0.027095),
                "top_1_share": (0.070356, 0.018173, 0.035196),
                "top_10_share": (0.42441, 0.106088, 0.157183),
                "top_50_share": (0.893071, 0.305696, 0.368859),
                "pair_entropy": (4.009743, 5.92046, 6.115742),
            },
            "seed1": {
                "empty_type_count": (949, 318, 464),
                "self_pair_share": (0.066109, 0.01884, 0.027095),
                "top_1_share": (0.069977, 0.018173, 0.035196),
                "top_10_share": (0.424484, 0.106088, 0.157183),
                "top_50_share": (0.893915, 0.305696, 0.368859),
                "pair_entropy": (4.009488, 5.92046, 6.115742),
            },
            "seed2": {
                "empty_type_count": (947, 318, 464),
                "self_pair_share": (0.065567, 0.01884, 0.027095),
                "top_1_share": (0.070383, 0.018173, 0.035196),
                "top_10_share": (0.425183, 0.106088, 0.157183),
                "top_50_share": (0.893971, 0.305696, 0.368859),
                "pair_entropy": (4.00809, 5.92046, 6.115742),
            },
            "seed3": {
                "empty_type_count": (946, 318, 464),
                "self_pair_share": (0.066341, 0.01884, 0.027095),
                "top_1_share": (0.070957, 0.018173, 0.035196),
                "top_10_share": (0.424841, 0.106088, 0.157183),
                "top_50_share": (0.893934, 0.305696, 0.368859),
                "pair_entropy": (4.007986, 5.92046, 6.115742),
            },
        },
        0.5: {
            "suffix": {
                "empty_type_count": (963, 341, 495),
                "self_pair_share": (0.058642, 0.01878, 0.027796),
                "top_1_share": (0.064586, 0.015177, 0.034405),
                "top_10_share": (0.419354, 0.100396, 0.157691),
                "top_50_share": (0.890629, 0.305696, 0.370604),
                "pair_entropy": (4.024671, 5.90532, 6.108939),
            },
            "seed0": {
                "empty_type_count": (975, 341, 495),
                "self_pair_share": (0.065835, 0.01878, 0.027796),
                "top_1_share": (0.0707, 0.015177, 0.034405),
                "top_10_share": (0.425658, 0.100396, 0.157691),
                "top_50_share": (0.892854, 0.305696, 0.370604),
                "pair_entropy": (4.009556, 5.90532, 6.108939),
            },
            "seed1": {
                "empty_type_count": (971, 341, 495),
                "self_pair_share": (0.066166, 0.01878, 0.027796),
                "top_1_share": (0.070272, 0.015177, 0.034405),
                "top_10_share": (0.423537, 0.100396, 0.157691),
                "top_50_share": (0.894099, 0.305696, 0.370604),
                "pair_entropy": (4.008461, 5.90532, 6.108939),
            },
            "seed2": {
                "empty_type_count": (979, 341, 495),
                "self_pair_share": (0.066272, 0.01878, 0.027796),
                "top_1_share": (0.07024, 0.015177, 0.034405),
                "top_10_share": (0.424783, 0.100396, 0.157691),
                "top_50_share": (0.894713, 0.305696, 0.370604),
                "pair_entropy": (4.005017, 5.90532, 6.108939),
            },
            "seed3": {
                "empty_type_count": (975, 341, 495),
                "self_pair_share": (0.065841, 0.01878, 0.027796),
                "top_1_share": (0.070757, 0.015177, 0.034405),
                "top_10_share": (0.425516, 0.100396, 0.157691),
                "top_50_share": (0.893845, 0.305696, 0.370604),
                "pair_entropy": (4.005973, 5.90532, 6.108939),
            },
        },
        0.25: {
            "suffix": {
                "empty_type_count": (1020, 376, 505),
                "self_pair_share": (0.058701, 0.018805, 0.027025),
                "top_1_share": (0.060117, 0.014518, 0.03463),
                "top_10_share": (0.448099, 0.100414, 0.160534),
                "top_50_share": (0.900713, 0.309486, 0.372217),
                "pair_entropy": (3.97606, 5.883769, 6.098317),
            },
            "seed0": {
                "empty_type_count": (1010, 376, 505),
                "self_pair_share": (0.065726, 0.018805, 0.027025),
                "top_1_share": (0.071136, 0.014518, 0.03463),
                "top_10_share": (0.424298, 0.100414, 0.160534),
                "top_50_share": (0.892841, 0.309486, 0.372217),
                "pair_entropy": (4.009569, 5.883769, 6.098317),
            },
            "seed1": {
                "empty_type_count": (1013, 376, 505),
                "self_pair_share": (0.067041, 0.018805, 0.027025),
                "top_1_share": (0.071055, 0.014518, 0.03463),
                "top_10_share": (0.425955, 0.100414, 0.160534),
                "top_50_share": (0.894601, 0.309486, 0.372217),
                "pair_entropy": (3.998056, 5.883769, 6.098317),
            },
            "seed2": {
                "empty_type_count": (1009, 376, 505),
                "self_pair_share": (0.067815, 0.018805, 0.027025),
                "top_1_share": (0.071633, 0.014518, 0.03463),
                "top_10_share": (0.428514, 0.100414, 0.160534),
                "top_50_share": (0.8943, 0.309486, 0.372217),
                "pair_entropy": (4.001034, 5.883769, 6.098317),
            },
            "seed3": {
                "empty_type_count": (1005, 376, 505),
                "self_pair_share": (0.065402, 0.018805, 0.027025),
                "top_1_share": (0.071013, 0.014518, 0.03463),
                "top_10_share": (0.428373, 0.100414, 0.160534),
                "top_50_share": (0.892359, 0.309486, 0.372217),
                "pair_entropy": (4.009035, 5.883769, 6.098317),
            },
        },
    },
    ("ZL", "latin"): {
        1.0: {
            "suffix": {
                "empty_type_count": (928, 240, 503),
                "self_pair_share": (0.065848, 0.011829, 0.023974),
                "top_1_share": (0.070481, 0.013486, 0.02536),
                "top_10_share": (0.424435, 0.09782, 0.132009),
                "top_50_share": (0.893671, 0.268516, 0.336674),
                "pair_entropy": (4.010179, 5.980168, 6.252),
            },
            "seed0": {
                "empty_type_count": (928, 240, 503),
                "self_pair_share": (0.065848, 0.011829, 0.023974),
                "top_1_share": (0.070481, 0.013486, 0.02536),
                "top_10_share": (0.424435, 0.09782, 0.132009),
                "top_50_share": (0.893671, 0.268516, 0.336674),
                "pair_entropy": (4.010179, 5.980168, 6.252),
            },
            "seed1": {
                "empty_type_count": (928, 240, 503),
                "self_pair_share": (0.065848, 0.011829, 0.023974),
                "top_1_share": (0.070481, 0.013486, 0.02536),
                "top_10_share": (0.424435, 0.09782, 0.132009),
                "top_50_share": (0.893671, 0.268516, 0.336674),
                "pair_entropy": (4.010179, 5.980168, 6.252),
            },
            "seed2": {
                "empty_type_count": (928, 240, 503),
                "self_pair_share": (0.065848, 0.011829, 0.023974),
                "top_1_share": (0.070481, 0.013486, 0.02536),
                "top_10_share": (0.424435, 0.09782, 0.132009),
                "top_50_share": (0.893671, 0.268516, 0.336674),
                "pair_entropy": (4.010179, 5.980168, 6.252),
            },
            "seed3": {
                "empty_type_count": (928, 240, 503),
                "self_pair_share": (0.065848, 0.011829, 0.023974),
                "top_1_share": (0.070481, 0.013486, 0.02536),
                "top_10_share": (0.424435, 0.09782, 0.132009),
                "top_50_share": (0.893671, 0.268516, 0.336674),
                "pair_entropy": (4.010179, 5.980168, 6.252),
            },
        },
        0.75: {
            "suffix": {
                "empty_type_count": (942, 283, 503),
                "self_pair_share": (0.060009, 0.012506, 0.023974),
                "top_1_share": (0.072428, 0.01335, 0.02536),
                "top_10_share": (0.415296, 0.097045, 0.134341),
                "top_50_share": (0.888714, 0.268516, 0.339127),
                "pair_entropy": (4.031522, 5.980168, 6.254451),
            },
            "seed0": {
                "empty_type_count": (950, 283, 503),
                "self_pair_share": (0.065902, 0.012506, 0.023974),
                "top_1_share": (0.070356, 0.01335, 0.02536),
                "top_10_share": (0.42441, 0.097045, 0.134341),
                "top_50_share": (0.893071, 0.268516, 0.339127),
                "pair_entropy": (4.009743, 5.980168, 6.254451),
            },
            "seed1": {
                "empty_type_count": (949, 283, 503),
                "self_pair_share": (0.066109, 0.012506, 0.023974),
                "top_1_share": (0.069977, 0.01335, 0.02536),
                "top_10_share": (0.424484, 0.097045, 0.134341),
                "top_50_share": (0.893915, 0.268516, 0.339127),
                "pair_entropy": (4.009488, 5.980168, 6.254451),
            },
            "seed2": {
                "empty_type_count": (947, 283, 503),
                "self_pair_share": (0.065567, 0.012506, 0.023974),
                "top_1_share": (0.070383, 0.01335, 0.02536),
                "top_10_share": (0.425183, 0.097045, 0.134341),
                "top_50_share": (0.893971, 0.268516, 0.339127),
                "pair_entropy": (4.00809, 5.980168, 6.254451),
            },
            "seed3": {
                "empty_type_count": (946, 283, 503),
                "self_pair_share": (0.066341, 0.012506, 0.023974),
                "top_1_share": (0.070957, 0.01335, 0.02536),
                "top_10_share": (0.424841, 0.097045, 0.134341),
                "top_50_share": (0.893934, 0.268516, 0.339127),
                "pair_entropy": (4.007986, 5.980168, 6.254451),
            },
        },
        0.5: {
            "suffix": {
                "empty_type_count": (963, 360, 503),
                "self_pair_share": (0.058642, 0.013366, 0.024518),
                "top_1_share": (0.064586, 0.013618, 0.025917),
                "top_10_share": (0.419354, 0.09782, 0.132131),
                "top_50_share": (0.890629, 0.268516, 0.335977),
                "pair_entropy": (4.024671, 5.980168, 6.250767),
            },
            "seed0": {
                "empty_type_count": (975, 360, 503),
                "self_pair_share": (0.065835, 0.013366, 0.024518),
                "top_1_share": (0.0707, 0.013618, 0.025917),
                "top_10_share": (0.425658, 0.09782, 0.132131),
                "top_50_share": (0.892854, 0.268516, 0.335977),
                "pair_entropy": (4.009556, 5.980168, 6.250767),
            },
            "seed1": {
                "empty_type_count": (971, 360, 503),
                "self_pair_share": (0.066166, 0.013366, 0.024518),
                "top_1_share": (0.070272, 0.013618, 0.025917),
                "top_10_share": (0.423537, 0.09782, 0.132131),
                "top_50_share": (0.894099, 0.268516, 0.335977),
                "pair_entropy": (4.008461, 5.980168, 6.250767),
            },
            "seed2": {
                "empty_type_count": (979, 360, 503),
                "self_pair_share": (0.066272, 0.013366, 0.024518),
                "top_1_share": (0.07024, 0.013618, 0.025917),
                "top_10_share": (0.424783, 0.09782, 0.132131),
                "top_50_share": (0.894713, 0.268516, 0.335977),
                "pair_entropy": (4.005017, 5.980168, 6.250767),
            },
            "seed3": {
                "empty_type_count": (975, 360, 503),
                "self_pair_share": (0.065841, 0.013366, 0.024518),
                "top_1_share": (0.070757, 0.013618, 0.025917),
                "top_10_share": (0.425516, 0.09782, 0.132131),
                "top_50_share": (0.893845, 0.268516, 0.335977),
                "pair_entropy": (4.005973, 5.980168, 6.250767),
            },
        },
        0.25: {
            "suffix": {
                "empty_type_count": (1020, 399, 537),
                "self_pair_share": (0.058701, 0.013527, 0.021909),
                "top_1_share": (0.060117, 0.013764, 0.025031),
                "top_10_share": (0.448099, 0.098316, 0.138755),
                "top_50_share": (0.900713, 0.272333, 0.348076),
                "pair_entropy": (3.97606, 5.951767, 6.248471),
            },
            "seed0": {
                "empty_type_count": (1010, 399, 537),
                "self_pair_share": (0.065726, 0.013527, 0.021909),
                "top_1_share": (0.071136, 0.013764, 0.025031),
                "top_10_share": (0.424298, 0.098316, 0.138755),
                "top_50_share": (0.892841, 0.272333, 0.348076),
                "pair_entropy": (4.009569, 5.951767, 6.248471),
            },
            "seed1": {
                "empty_type_count": (1013, 399, 537),
                "self_pair_share": (0.067041, 0.013527, 0.021909),
                "top_1_share": (0.071055, 0.013764, 0.025031),
                "top_10_share": (0.425955, 0.098316, 0.138755),
                "top_50_share": (0.894601, 0.272333, 0.348076),
                "pair_entropy": (3.998056, 5.951767, 6.248471),
            },
            "seed2": {
                "empty_type_count": (1009, 399, 537),
                "self_pair_share": (0.067815, 0.013527, 0.021909),
                "top_1_share": (0.071633, 0.013764, 0.025031),
                "top_10_share": (0.428514, 0.098316, 0.138755),
                "top_50_share": (0.8943, 0.272333, 0.348076),
                "pair_entropy": (4.001034, 5.951767, 6.248471),
            },
            "seed3": {
                "empty_type_count": (1005, 399, 537),
                "self_pair_share": (0.065402, 0.013527, 0.021909),
                "top_1_share": (0.071013, 0.013764, 0.025031),
                "top_10_share": (0.428373, 0.098316, 0.138755),
                "top_50_share": (0.892359, 0.272333, 0.348076),
                "pair_entropy": (4.009035, 5.951767, 6.248471),
            },
        },
    },
    ("GC", "english"): {
        1.0: {
            "suffix": {
                "empty_type_count": (642, 318, 453),
                "self_pair_share": (0.015928, 0.018513, 0.027183),
                "top_1_share": (0.051049, 0.018386, 0.035403),
                "top_10_share": (0.373572, 0.106088, 0.15809),
                "top_50_share": (0.8066, 0.305406, 0.370289),
                "pair_entropy": (4.422831, 5.919417, 6.116692),
            },
            "seed0": {
                "empty_type_count": (642, 318, 453),
                "self_pair_share": (0.015928, 0.018513, 0.027183),
                "top_1_share": (0.051049, 0.018386, 0.035403),
                "top_10_share": (0.373572, 0.106088, 0.15809),
                "top_50_share": (0.8066, 0.305406, 0.370289),
                "pair_entropy": (4.422831, 5.919417, 6.116692),
            },
            "seed1": {
                "empty_type_count": (642, 318, 453),
                "self_pair_share": (0.015928, 0.018513, 0.027183),
                "top_1_share": (0.051049, 0.018386, 0.035403),
                "top_10_share": (0.373572, 0.106088, 0.15809),
                "top_50_share": (0.8066, 0.305406, 0.370289),
                "pair_entropy": (4.422831, 5.919417, 6.116692),
            },
            "seed2": {
                "empty_type_count": (642, 318, 453),
                "self_pair_share": (0.015928, 0.018513, 0.027183),
                "top_1_share": (0.051049, 0.018386, 0.035403),
                "top_10_share": (0.373572, 0.106088, 0.15809),
                "top_50_share": (0.8066, 0.305406, 0.370289),
                "pair_entropy": (4.422831, 5.919417, 6.116692),
            },
            "seed3": {
                "empty_type_count": (642, 318, 453),
                "self_pair_share": (0.015928, 0.018513, 0.027183),
                "top_1_share": (0.051049, 0.018386, 0.035403),
                "top_10_share": (0.373572, 0.106088, 0.15809),
                "top_50_share": (0.8066, 0.305406, 0.370289),
                "pair_entropy": (4.422831, 5.919417, 6.116692),
            },
        },
        0.75: {
            "suffix": {
                "empty_type_count": (674, 335, 473),
                "self_pair_share": (0.014007, 0.018404, 0.027769),
                "top_1_share": (0.051058, 0.015821, 0.034743),
                "top_10_share": (0.373617, 0.103071, 0.157186),
                "top_50_share": (0.804829, 0.305406, 0.368975),
                "pair_entropy": (4.43086, 5.916585, 6.10912),
            },
            "seed0": {
                "empty_type_count": (691, 335, 473),
                "self_pair_share": (0.016119, 0.018404, 0.027769),
                "top_1_share": (0.051456, 0.015821, 0.034743),
                "top_10_share": (0.375462, 0.103071, 0.157186),
                "top_50_share": (0.806564, 0.305406, 0.368975),
                "pair_entropy": (4.419684, 5.916585, 6.10912),
            },
            "seed1": {
                "empty_type_count": (690, 335, 473),
                "self_pair_share": (0.015895, 0.018404, 0.027769),
                "top_1_share": (0.050857, 0.015821, 0.034743),
                "top_10_share": (0.373292, 0.103071, 0.157186),
                "top_50_share": (0.80611, 0.305406, 0.368975),
                "pair_entropy": (4.423522, 5.916585, 6.10912),
            },
            "seed2": {
                "empty_type_count": (680, 335, 473),
                "self_pair_share": (0.016116, 0.018404, 0.027769),
                "top_1_share": (0.050553, 0.015821, 0.034743),
                "top_10_share": (0.37307, 0.103071, 0.157186),
                "top_50_share": (0.80577, 0.305406, 0.368975),
                "pair_entropy": (4.424432, 5.916585, 6.10912),
            },
            "seed3": {
                "empty_type_count": (680, 335, 473),
                "self_pair_share": (0.016192, 0.018404, 0.027769),
                "top_1_share": (0.05033, 0.015821, 0.034743),
                "top_10_share": (0.372571, 0.103071, 0.157186),
                "top_50_share": (0.806656, 0.305406, 0.368975),
                "pair_entropy": (4.421759, 5.916585, 6.10912),
            },
        },
        0.5: {
            "suffix": {
                "empty_type_count": (726, 359, 502),
                "self_pair_share": (0.015234, 0.018849, 0.027852),
                "top_1_share": (0.053523, 0.017005, 0.034804),
                "top_10_share": (0.378619, 0.106112, 0.158851),
                "top_50_share": (0.810512, 0.305386, 0.372036),
                "pair_entropy": (4.403008, 5.899352, 6.109574),
            },
            "seed0": {
                "empty_type_count": (739, 359, 502),
                "self_pair_share": (0.016111, 0.018849, 0.027852),
                "top_1_share": (0.051549, 0.017005, 0.034804),
                "top_10_share": (0.375344, 0.106112, 0.158851),
                "top_50_share": (0.806648, 0.305386, 0.372036),
                "pair_entropy": (4.41993, 5.899352, 6.109574),
            },
            "seed1": {
                "empty_type_count": (746, 359, 502),
                "self_pair_share": (0.015971, 0.018849, 0.027852),
                "top_1_share": (0.050439, 0.017005, 0.034804),
                "top_10_share": (0.373597, 0.106112, 0.158851),
                "top_50_share": (0.809554, 0.305386, 0.372036),
                "pair_entropy": (4.413231, 5.899352, 6.109574),
            },
            "seed2": {
                "empty_type_count": (735, 359, 502),
                "self_pair_share": (0.015499, 0.018849, 0.027852),
                "top_1_share": (0.050823, 0.017005, 0.034804),
                "top_10_share": (0.372978, 0.106112, 0.158851),
                "top_50_share": (0.805324, 0.305386, 0.372036),
                "pair_entropy": (4.425515, 5.899352, 6.109574),
            },
            "seed3": {
                "empty_type_count": (735, 359, 502),
                "self_pair_share": (0.015961, 0.018849, 0.027852),
                "top_1_share": (0.050387, 0.017005, 0.034804),
                "top_10_share": (0.372716, 0.106112, 0.158851),
                "top_50_share": (0.807325, 0.305386, 0.372036),
                "pair_entropy": (4.417694, 5.899352, 6.109574),
            },
        },
        0.25: {
            "suffix": {
                "empty_type_count": (837, 399, 520),
                "self_pair_share": (0.013229, 0.018382, 0.025854),
                "top_1_share": (0.062981, 0.01885, 0.033087),
                "top_10_share": (0.395967, 0.109712, 0.164276),
                "top_50_share": (0.819398, 0.307336, 0.377631),
                "pair_entropy": (4.341177, 5.863478, 6.087147),
            },
            "seed0": {
                "empty_type_count": (819, 399, 520),
                "self_pair_share": (0.017168, 0.018382, 0.025854),
                "top_1_share": (0.051969, 0.01885, 0.033087),
                "top_10_share": (0.377195, 0.109712, 0.164276),
                "top_50_share": (0.807683, 0.307336, 0.377631),
                "pair_entropy": (4.410373, 5.863478, 6.087147),
            },
            "seed1": {
                "empty_type_count": (819, 399, 520),
                "self_pair_share": (0.015422, 0.018382, 0.025854),
                "top_1_share": (0.048705, 0.01885, 0.033087),
                "top_10_share": (0.375081, 0.109712, 0.164276),
                "top_50_share": (0.809232, 0.307336, 0.377631),
                "pair_entropy": (4.406237, 5.863478, 6.087147),
            },
            "seed2": {
                "empty_type_count": (818, 399, 520),
                "self_pair_share": (0.014914, 0.018382, 0.025854),
                "top_1_share": (0.051109, 0.01885, 0.033087),
                "top_10_share": (0.372568, 0.109712, 0.164276),
                "top_50_share": (0.803433, 0.307336, 0.377631),
                "pair_entropy": (4.425403, 5.863478, 6.087147),
            },
            "seed3": {
                "empty_type_count": (809, 399, 520),
                "self_pair_share": (0.01633, 0.018382, 0.025854),
                "top_1_share": (0.049957, 0.01885, 0.033087),
                "top_10_share": (0.37355, 0.109712, 0.164276),
                "top_50_share": (0.807549, 0.307336, 0.377631),
                "pair_entropy": (4.415826, 5.863478, 6.087147),
            },
        },
    },
    ("GC", "latin"): {
        1.0: {
            "suffix": {
                "empty_type_count": (642, 262, 500),
                "self_pair_share": (0.015928, 0.011979, 0.023941),
                "top_1_share": (0.051049, 0.013384, 0.02536),
                "top_10_share": (0.373572, 0.097128, 0.133145),
                "top_50_share": (0.8066, 0.26876, 0.338741),
                "pair_entropy": (4.422831, 5.98016, 6.254936),
            },
            "seed0": {
                "empty_type_count": (642, 262, 500),
                "self_pair_share": (0.015928, 0.011979, 0.023941),
                "top_1_share": (0.051049, 0.013384, 0.02536),
                "top_10_share": (0.373572, 0.097128, 0.133145),
                "top_50_share": (0.8066, 0.26876, 0.338741),
                "pair_entropy": (4.422831, 5.98016, 6.254936),
            },
            "seed1": {
                "empty_type_count": (642, 262, 500),
                "self_pair_share": (0.015928, 0.011979, 0.023941),
                "top_1_share": (0.051049, 0.013384, 0.02536),
                "top_10_share": (0.373572, 0.097128, 0.133145),
                "top_50_share": (0.8066, 0.26876, 0.338741),
                "pair_entropy": (4.422831, 5.98016, 6.254936),
            },
            "seed2": {
                "empty_type_count": (642, 262, 500),
                "self_pair_share": (0.015928, 0.011979, 0.023941),
                "top_1_share": (0.051049, 0.013384, 0.02536),
                "top_10_share": (0.373572, 0.097128, 0.133145),
                "top_50_share": (0.8066, 0.26876, 0.338741),
                "pair_entropy": (4.422831, 5.98016, 6.254936),
            },
            "seed3": {
                "empty_type_count": (642, 262, 500),
                "self_pair_share": (0.015928, 0.011979, 0.023941),
                "top_1_share": (0.051049, 0.013384, 0.02536),
                "top_10_share": (0.373572, 0.097128, 0.133145),
                "top_50_share": (0.8066, 0.26876, 0.338741),
                "pair_entropy": (4.422831, 5.98016, 6.254936),
            },
        },
        0.75: {
            "suffix": {
                "empty_type_count": (674, 307, 500),
                "self_pair_share": (0.014007, 0.012489, 0.023941),
                "top_1_share": (0.051058, 0.013366, 0.02536),
                "top_10_share": (0.373617, 0.097737, 0.136046),
                "top_50_share": (0.804829, 0.26876, 0.341342),
                "pair_entropy": (4.43086, 5.98016, 6.253207),
            },
            "seed0": {
                "empty_type_count": (691, 307, 500),
                "self_pair_share": (0.016119, 0.012489, 0.023941),
                "top_1_share": (0.051456, 0.013366, 0.02536),
                "top_10_share": (0.375462, 0.097737, 0.136046),
                "top_50_share": (0.806564, 0.26876, 0.341342),
                "pair_entropy": (4.419684, 5.98016, 6.253207),
            },
            "seed1": {
                "empty_type_count": (690, 307, 500),
                "self_pair_share": (0.015895, 0.012489, 0.023941),
                "top_1_share": (0.050857, 0.013366, 0.02536),
                "top_10_share": (0.373292, 0.097737, 0.136046),
                "top_50_share": (0.80611, 0.26876, 0.341342),
                "pair_entropy": (4.423522, 5.98016, 6.253207),
            },
            "seed2": {
                "empty_type_count": (680, 307, 500),
                "self_pair_share": (0.016116, 0.012489, 0.023941),
                "top_1_share": (0.050553, 0.013366, 0.02536),
                "top_10_share": (0.37307, 0.097737, 0.136046),
                "top_50_share": (0.80577, 0.26876, 0.341342),
                "pair_entropy": (4.424432, 5.98016, 6.253207),
            },
            "seed3": {
                "empty_type_count": (680, 307, 500),
                "self_pair_share": (0.016192, 0.012489, 0.023941),
                "top_1_share": (0.05033, 0.013366, 0.02536),
                "top_10_share": (0.372571, 0.097737, 0.136046),
                "top_50_share": (0.806656, 0.26876, 0.341342),
                "pair_entropy": (4.421759, 5.98016, 6.253207),
            },
        },
        0.5: {
            "suffix": {
                "empty_type_count": (726, 376, 500),
                "self_pair_share": (0.015234, 0.013329, 0.023837),
                "top_1_share": (0.053523, 0.013609, 0.025776),
                "top_10_share": (0.378619, 0.098063, 0.134714),
                "top_50_share": (0.810512, 0.26876, 0.338778),
                "pair_entropy": (4.403008, 5.978656, 6.250384),
            },
            "seed0": {
                "empty_type_count": (739, 376, 500),
                "self_pair_share": (0.016111, 0.013329, 0.023837),
                "top_1_share": (0.051549, 0.013609, 0.025776),
                "top_10_share": (0.375344, 0.098063, 0.134714),
                "top_50_share": (0.806648, 0.26876, 0.338778),
                "pair_entropy": (4.41993, 5.978656, 6.250384),
            },
            "seed1": {
                "empty_type_count": (746, 376, 500),
                "self_pair_share": (0.015971, 0.013329, 0.023837),
                "top_1_share": (0.050439, 0.013609, 0.025776),
                "top_10_share": (0.373597, 0.098063, 0.134714),
                "top_50_share": (0.809554, 0.26876, 0.338778),
                "pair_entropy": (4.413231, 5.978656, 6.250384),
            },
            "seed2": {
                "empty_type_count": (735, 376, 500),
                "self_pair_share": (0.015499, 0.013329, 0.023837),
                "top_1_share": (0.050823, 0.013609, 0.025776),
                "top_10_share": (0.372978, 0.098063, 0.134714),
                "top_50_share": (0.805324, 0.26876, 0.338778),
                "pair_entropy": (4.425515, 5.978656, 6.250384),
            },
            "seed3": {
                "empty_type_count": (735, 376, 500),
                "self_pair_share": (0.015961, 0.013329, 0.023837),
                "top_1_share": (0.050387, 0.013609, 0.025776),
                "top_10_share": (0.372716, 0.098063, 0.134714),
                "top_50_share": (0.807325, 0.26876, 0.338778),
                "pair_entropy": (4.417694, 5.978656, 6.250384),
            },
        },
        0.25: {
            "suffix": {
                "empty_type_count": (837, 414, 547),
                "self_pair_share": (0.013229, 0.01295, 0.021521),
                "top_1_share": (0.062981, 0.014424, 0.024548),
                "top_10_share": (0.395967, 0.099777, 0.140588),
                "top_50_share": (0.819398, 0.269632, 0.347807),
                "pair_entropy": (4.341177, 5.943103, 6.233837),
            },
            "seed0": {
                "empty_type_count": (819, 414, 547),
                "self_pair_share": (0.017168, 0.01295, 0.021521),
                "top_1_share": (0.051969, 0.014424, 0.024548),
                "top_10_share": (0.377195, 0.099777, 0.140588),
                "top_50_share": (0.807683, 0.269632, 0.347807),
                "pair_entropy": (4.410373, 5.943103, 6.233837),
            },
            "seed1": {
                "empty_type_count": (819, 414, 547),
                "self_pair_share": (0.015422, 0.01295, 0.021521),
                "top_1_share": (0.048705, 0.014424, 0.024548),
                "top_10_share": (0.375081, 0.099777, 0.140588),
                "top_50_share": (0.809232, 0.269632, 0.347807),
                "pair_entropy": (4.406237, 5.943103, 6.233837),
            },
            "seed2": {
                "empty_type_count": (818, 414, 547),
                "self_pair_share": (0.014914, 0.01295, 0.021521),
                "top_1_share": (0.051109, 0.014424, 0.024548),
                "top_10_share": (0.372568, 0.099777, 0.140588),
                "top_50_share": (0.803433, 0.269632, 0.347807),
                "pair_entropy": (4.425403, 5.943103, 6.233837),
            },
            "seed3": {
                "empty_type_count": (809, 414, 547),
                "self_pair_share": (0.01633, 0.01295, 0.021521),
                "top_1_share": (0.049957, 0.014424, 0.024548),
                "top_10_share": (0.37355, 0.099777, 0.140588),
                "top_50_share": (0.807549, 0.269632, 0.347807),
                "pair_entropy": (4.415826, 5.943103, 6.233837),
            },
        },
    },
    ("IT", "english"): {
        1.0: {
            "suffix": {
                "empty_type_count": (984, 325, 449),
                "self_pair_share": (0.065777, 0.018701, 0.027087),
                "top_1_share": (0.071689, 0.018068, 0.035914),
                "top_10_share": (0.429316, 0.106088, 0.148471),
                "top_50_share": (0.89868, 0.30546, 0.35595),
                "pair_entropy": (3.980621, 5.927877, 6.102609),
            },
            "seed0": {
                "empty_type_count": (984, 325, 449),
                "self_pair_share": (0.065777, 0.018701, 0.027087),
                "top_1_share": (0.071689, 0.018068, 0.035914),
                "top_10_share": (0.429316, 0.106088, 0.148471),
                "top_50_share": (0.89868, 0.30546, 0.35595),
                "pair_entropy": (3.980621, 5.927877, 6.102609),
            },
            "seed1": {
                "empty_type_count": (984, 325, 449),
                "self_pair_share": (0.065777, 0.018701, 0.027087),
                "top_1_share": (0.071689, 0.018068, 0.035914),
                "top_10_share": (0.429316, 0.106088, 0.148471),
                "top_50_share": (0.89868, 0.30546, 0.35595),
                "pair_entropy": (3.980621, 5.927877, 6.102609),
            },
            "seed2": {
                "empty_type_count": (984, 325, 449),
                "self_pair_share": (0.065777, 0.018701, 0.027087),
                "top_1_share": (0.071689, 0.018068, 0.035914),
                "top_10_share": (0.429316, 0.106088, 0.148471),
                "top_50_share": (0.89868, 0.30546, 0.35595),
                "pair_entropy": (3.980621, 5.927877, 6.102609),
            },
            "seed3": {
                "empty_type_count": (984, 325, 449),
                "self_pair_share": (0.065777, 0.018701, 0.027087),
                "top_1_share": (0.071689, 0.018068, 0.035914),
                "top_10_share": (0.429316, 0.106088, 0.148471),
                "top_50_share": (0.89868, 0.30546, 0.35595),
                "pair_entropy": (3.980621, 5.927877, 6.102609),
            },
        },
        0.75: {
            "suffix": {
                "empty_type_count": (998, 318, 462),
                "self_pair_share": (0.059721, 0.018887, 0.027333),
                "top_1_share": (0.07376, 0.018112, 0.035253),
                "top_10_share": (0.420792, 0.106088, 0.157263),
                "top_50_share": (0.89337, 0.30546, 0.369102),
                "pair_entropy": (4.002811, 5.920093, 6.116071),
            },
            "seed0": {
                "empty_type_count": (997, 318, 462),
                "self_pair_share": (0.065887, 0.018887, 0.027333),
                "top_1_share": (0.071951, 0.018112, 0.035253),
                "top_10_share": (0.428722, 0.106088, 0.157263),
                "top_50_share": (0.898635, 0.30546, 0.369102),
                "pair_entropy": (3.981489, 5.920093, 6.116071),
            },
            "seed1": {
                "empty_type_count": (997, 318, 462),
                "self_pair_share": (0.065786, 0.018887, 0.027333),
                "top_1_share": (0.071376, 0.018112, 0.035253),
                "top_10_share": (0.428255, 0.106088, 0.157263),
                "top_50_share": (0.8989, 0.30546, 0.369102),
                "pair_entropy": (3.980381, 5.920093, 6.116071),
            },
            "seed2": {
                "empty_type_count": (999, 318, 462),
                "self_pair_share": (0.066752, 0.018887, 0.027333),
                "top_1_share": (0.071554, 0.018112, 0.035253),
                "top_10_share": (0.430324, 0.106088, 0.157263),
                "top_50_share": (0.899281, 0.30546, 0.369102),
                "pair_entropy": (3.978272, 5.920093, 6.116071),
            },
            "seed3": {
                "empty_type_count": (994, 318, 462),
                "self_pair_share": (0.065454, 0.018887, 0.027333),
                "top_1_share": (0.072124, 0.018112, 0.035253),
                "top_10_share": (0.428075, 0.106088, 0.157263),
                "top_50_share": (0.898778, 0.30546, 0.369102),
                "pair_entropy": (3.980017, 5.920093, 6.116071),
            },
        },
        0.5: {
            "suffix": {
                "empty_type_count": (1009, 338, 491),
                "self_pair_share": (0.057784, 0.018939, 0.027767),
                "top_1_share": (0.065897, 0.015138, 0.034458),
                "top_10_share": (0.425561, 0.100656, 0.157543),
                "top_50_share": (0.893634, 0.30546, 0.369888),
                "pair_entropy": (3.999146, 5.906326, 6.11015),
            },
            "seed0": {
                "empty_type_count": (1013, 338, 491),
                "self_pair_share": (0.064822, 0.018939, 0.027767),
                "top_1_share": (0.071678, 0.015138, 0.034458),
                "top_10_share": (0.427929, 0.100656, 0.157543),
                "top_50_share": (0.897279, 0.30546, 0.369888),
                "pair_entropy": (3.985835, 5.906326, 6.11015),
            },
            "seed1": {
                "empty_type_count": (1013, 338, 491),
                "self_pair_share": (0.065271, 0.018939, 0.027767),
                "top_1_share": (0.070642, 0.015138, 0.034458),
                "top_10_share": (0.427874, 0.100656, 0.157543),
                "top_50_share": (0.899077, 0.30546, 0.369888),
                "pair_entropy": (3.979607, 5.906326, 6.11015),
            },
            "seed2": {
                "empty_type_count": (1017, 338, 491),
                "self_pair_share": (0.067221, 0.018939, 0.027767),
                "top_1_share": (0.071199, 0.015138, 0.034458),
                "top_10_share": (0.43081, 0.100656, 0.157543),
                "top_50_share": (0.900123, 0.30546, 0.369888),
                "pair_entropy": (3.973913, 5.906326, 6.11015),
            },
            "seed3": {
                "empty_type_count": (1010, 338, 491),
                "self_pair_share": (0.065803, 0.018939, 0.027767),
                "top_1_share": (0.072917, 0.015138, 0.034458),
                "top_10_share": (0.428023, 0.100656, 0.157543),
                "top_50_share": (0.899287, 0.30546, 0.369888),
                "pair_entropy": (3.978825, 5.906326, 6.11015),
            },
        },
        0.25: {
            "suffix": {
                "empty_type_count": (1064, 383, 507),
                "self_pair_share": (0.058704, 0.018882, 0.026675),
                "top_1_share": (0.060903, 0.014318, 0.034724),
                "top_10_share": (0.455375, 0.098647, 0.160437),
                "top_50_share": (0.905808, 0.309421, 0.372346),
                "pair_entropy": (3.935649, 5.885832, 6.098799),
            },
            "seed0": {
                "empty_type_count": (1049, 383, 507),
                "self_pair_share": (0.065023, 0.018882, 0.026675),
                "top_1_share": (0.071303, 0.014318, 0.034724),
                "top_10_share": (0.429523, 0.098647, 0.160437),
                "top_50_share": (0.899407, 0.309421, 0.372346),
                "pair_entropy": (3.980643, 5.885832, 6.098799),
            },
            "seed1": {
                "empty_type_count": (1049, 383, 507),
                "self_pair_share": (0.065786, 0.018882, 0.026675),
                "top_1_share": (0.071272, 0.014318, 0.034724),
                "top_10_share": (0.427903, 0.098647, 0.160437),
                "top_50_share": (0.89843, 0.309421, 0.372346),
                "pair_entropy": (3.982639, 5.885832, 6.098799),
            },
            "seed2": {
                "empty_type_count": (1055, 383, 507),
                "self_pair_share": (0.066598, 0.018882, 0.026675),
                "top_1_share": (0.072314, 0.014318, 0.034724),
                "top_10_share": (0.433806, 0.098647, 0.160437),
                "top_50_share": (0.900992, 0.309421, 0.372346),
                "pair_entropy": (3.965077, 5.885832, 6.098799),
            },
            "seed3": {
                "empty_type_count": (1041, 383, 507),
                "self_pair_share": (0.064097, 0.018882, 0.026675),
                "top_1_share": (0.073258, 0.014318, 0.034724),
                "top_10_share": (0.428273, 0.098647, 0.160437),
                "top_50_share": (0.900669, 0.309421, 0.372346),
                "pair_entropy": (3.977512, 5.885832, 6.098799),
            },
        },
    },
    ("IT", "latin"): {
        1.0: {
            "suffix": {
                "empty_type_count": (984, 241, 500),
                "self_pair_share": (0.065777, 0.013217, 0.024029),
                "top_1_share": (0.071689, 0.013525, 0.02536),
                "top_10_share": (0.429316, 0.098044, 0.131821),
                "top_50_share": (0.89868, 0.268841, 0.336358),
                "pair_entropy": (3.980621, 5.980406, 6.252202),
            },
            "seed0": {
                "empty_type_count": (984, 241, 500),
                "self_pair_share": (0.065777, 0.013217, 0.024029),
                "top_1_share": (0.071689, 0.013525, 0.02536),
                "top_10_share": (0.429316, 0.098044, 0.131821),
                "top_50_share": (0.89868, 0.268841, 0.336358),
                "pair_entropy": (3.980621, 5.980406, 6.252202),
            },
            "seed1": {
                "empty_type_count": (984, 241, 500),
                "self_pair_share": (0.065777, 0.013217, 0.024029),
                "top_1_share": (0.071689, 0.013525, 0.02536),
                "top_10_share": (0.429316, 0.098044, 0.131821),
                "top_50_share": (0.89868, 0.268841, 0.336358),
                "pair_entropy": (3.980621, 5.980406, 6.252202),
            },
            "seed2": {
                "empty_type_count": (984, 241, 500),
                "self_pair_share": (0.065777, 0.013217, 0.024029),
                "top_1_share": (0.071689, 0.013525, 0.02536),
                "top_10_share": (0.429316, 0.098044, 0.131821),
                "top_50_share": (0.89868, 0.268841, 0.336358),
                "pair_entropy": (3.980621, 5.980406, 6.252202),
            },
            "seed3": {
                "empty_type_count": (984, 241, 500),
                "self_pair_share": (0.065777, 0.013217, 0.024029),
                "top_1_share": (0.071689, 0.013525, 0.02536),
                "top_10_share": (0.429316, 0.098044, 0.131821),
                "top_50_share": (0.89868, 0.268841, 0.336358),
                "pair_entropy": (3.980621, 5.980406, 6.252202),
            },
        },
        0.75: {
            "suffix": {
                "empty_type_count": (998, 280, 500),
                "self_pair_share": (0.059721, 0.012518, 0.024029),
                "top_1_share": (0.07376, 0.013365, 0.02536),
                "top_10_share": (0.420792, 0.097707, 0.134148),
                "top_50_share": (0.89337, 0.268841, 0.338867),
                "pair_entropy": (4.002811, 5.980406, 6.254241),
            },
            "seed0": {
                "empty_type_count": (997, 280, 500),
                "self_pair_share": (0.065887, 0.012518, 0.024029),
                "top_1_share": (0.071951, 0.013365, 0.02536),
                "top_10_share": (0.428722, 0.097707, 0.134148),
                "top_50_share": (0.898635, 0.268841, 0.338867),
                "pair_entropy": (3.981489, 5.980406, 6.254241),
            },
            "seed1": {
                "empty_type_count": (997, 280, 500),
                "self_pair_share": (0.065786, 0.012518, 0.024029),
                "top_1_share": (0.071376, 0.013365, 0.02536),
                "top_10_share": (0.428255, 0.097707, 0.134148),
                "top_50_share": (0.8989, 0.268841, 0.338867),
                "pair_entropy": (3.980381, 5.980406, 6.254241),
            },
            "seed2": {
                "empty_type_count": (999, 280, 500),
                "self_pair_share": (0.066752, 0.012518, 0.024029),
                "top_1_share": (0.071554, 0.013365, 0.02536),
                "top_10_share": (0.430324, 0.097707, 0.134148),
                "top_50_share": (0.899281, 0.268841, 0.338867),
                "pair_entropy": (3.978272, 5.980406, 6.254241),
            },
            "seed3": {
                "empty_type_count": (994, 280, 500),
                "self_pair_share": (0.065454, 0.012518, 0.024029),
                "top_1_share": (0.072124, 0.013365, 0.02536),
                "top_10_share": (0.428075, 0.097707, 0.134148),
                "top_50_share": (0.898778, 0.268841, 0.338867),
                "pair_entropy": (3.980017, 5.980406, 6.254241),
            },
        },
        0.5: {
            "suffix": {
                "empty_type_count": (1009, 353, 500),
                "self_pair_share": (0.057784, 0.013268, 0.024498),
                "top_1_share": (0.065897, 0.013587, 0.025896),
                "top_10_share": (0.425561, 0.098177, 0.131964),
                "top_50_share": (0.893634, 0.268841, 0.336261),
                "pair_entropy": (3.999146, 5.980406, 6.250893),
            },
            "seed0": {
                "empty_type_count": (1013, 353, 500),
                "self_pair_share": (0.064822, 0.013268, 0.024498),
                "top_1_share": (0.071678, 0.013587, 0.025896),
                "top_10_share": (0.427929, 0.098177, 0.131964),
                "top_50_share": (0.897279, 0.268841, 0.336261),
                "pair_entropy": (3.985835, 5.980406, 6.250893),
            },
            "seed1": {
                "empty_type_count": (1013, 353, 500),
                "self_pair_share": (0.065271, 0.013268, 0.024498),
                "top_1_share": (0.070642, 0.013587, 0.025896),
                "top_10_share": (0.427874, 0.098177, 0.131964),
                "top_50_share": (0.899077, 0.268841, 0.336261),
                "pair_entropy": (3.979607, 5.980406, 6.250893),
            },
            "seed2": {
                "empty_type_count": (1017, 353, 500),
                "self_pair_share": (0.067221, 0.013268, 0.024498),
                "top_1_share": (0.071199, 0.013587, 0.025896),
                "top_10_share": (0.43081, 0.098177, 0.131964),
                "top_50_share": (0.900123, 0.268841, 0.336261),
                "pair_entropy": (3.973913, 5.980406, 6.250893),
            },
            "seed3": {
                "empty_type_count": (1010, 353, 500),
                "self_pair_share": (0.065803, 0.013268, 0.024498),
                "top_1_share": (0.072917, 0.013587, 0.025896),
                "top_10_share": (0.428023, 0.098177, 0.131964),
                "top_50_share": (0.899287, 0.268841, 0.336261),
                "pair_entropy": (3.978825, 5.980406, 6.250893),
            },
        },
        0.25: {
            "suffix": {
                "empty_type_count": (1064, 404, 535),
                "self_pair_share": (0.058704, 0.013499, 0.022046),
                "top_1_share": (0.060903, 0.013812, 0.025113),
                "top_10_share": (0.455375, 0.098242, 0.138286),
                "top_50_share": (0.905808, 0.27285, 0.34743),
                "pair_entropy": (3.935649, 5.951559, 6.248481),
            },
            "seed0": {
                "empty_type_count": (1049, 404, 535),
                "self_pair_share": (0.065023, 0.013499, 0.022046),
                "top_1_share": (0.071303, 0.013812, 0.025113),
                "top_10_share": (0.429523, 0.098242, 0.138286),
                "top_50_share": (0.899407, 0.27285, 0.34743),
                "pair_entropy": (3.980643, 5.951559, 6.248481),
            },
            "seed1": {
                "empty_type_count": (1049, 404, 535),
                "self_pair_share": (0.065786, 0.013499, 0.022046),
                "top_1_share": (0.071272, 0.013812, 0.025113),
                "top_10_share": (0.427903, 0.098242, 0.138286),
                "top_50_share": (0.89843, 0.27285, 0.34743),
                "pair_entropy": (3.982639, 5.951559, 6.248481),
            },
            "seed2": {
                "empty_type_count": (1055, 404, 535),
                "self_pair_share": (0.066598, 0.013499, 0.022046),
                "top_1_share": (0.072314, 0.013812, 0.025113),
                "top_10_share": (0.433806, 0.098242, 0.138286),
                "top_50_share": (0.900992, 0.27285, 0.34743),
                "pair_entropy": (3.965077, 5.951559, 6.248481),
            },
            "seed3": {
                "empty_type_count": (1041, 404, 535),
                "self_pair_share": (0.064097, 0.013499, 0.022046),
                "top_1_share": (0.073258, 0.013812, 0.025113),
                "top_10_share": (0.428273, 0.098242, 0.138286),
                "top_50_share": (0.900669, 0.27285, 0.34743),
                "pair_entropy": (3.977512, 5.951559, 6.248481),
            },
        },
    },
}

# The per-cell per-geometry vector outside counts (symbol
# positions out of 36, pair positions out of 1296), from
# the same run.
VECTOR_GEOM = {
    ("ZL", "english"): {
        1.0: {
            "suffix": (35, 834),
            "seed0": (35, 834),
            "seed1": (35, 834),
            "seed2": (35, 834),
            "seed3": (35, 834),
        },
        0.75: {
            "suffix": (35, 822),
            "seed0": (36, 824),
            "seed1": (36, 824),
            "seed2": (36, 823),
            "seed3": (36, 823),
        },
        0.5: {
            "suffix": (36, 794),
            "seed0": (36, 793),
            "seed1": (34, 793),
            "seed2": (36, 793),
            "seed3": (36, 791),
        },
        0.25: {
            "suffix": (36, 788),
            "seed0": (36, 786),
            "seed1": (34, 790),
            "seed2": (36, 782),
            "seed3": (36, 785),
        },
    },
    ("ZL", "latin"): {
        1.0: {
            "suffix": (36, 780),
            "seed0": (36, 780),
            "seed1": (36, 780),
            "seed2": (36, 780),
            "seed3": (36, 780),
        },
        0.75: {
            "suffix": (35, 781),
            "seed0": (35, 778),
            "seed1": (35, 778),
            "seed2": (35, 781),
            "seed3": (35, 781),
        },
        0.5: {
            "suffix": (35, 780),
            "seed0": (35, 779),
            "seed1": (34, 778),
            "seed2": (35, 781),
            "seed3": (35, 781),
        },
        0.25: {
            "suffix": (35, 750),
            "seed0": (35, 746),
            "seed1": (35, 747),
            "seed2": (35, 745),
            "seed3": (35, 749),
        },
    },
    ("GC", "english"): {
        1.0: {
            "suffix": (36, 829),
            "seed0": (36, 829),
            "seed1": (36, 829),
            "seed2": (36, 829),
            "seed3": (36, 829),
        },
        0.75: {
            "suffix": (36, 816),
            "seed0": (36, 809),
            "seed1": (36, 814),
            "seed2": (36, 809),
            "seed3": (36, 810),
        },
        0.5: {
            "suffix": (36, 787),
            "seed0": (36, 779),
            "seed1": (36, 780),
            "seed2": (36, 781),
            "seed3": (36, 785),
        },
        0.25: {
            "suffix": (35, 769),
            "seed0": (36, 762),
            "seed1": (36, 769),
            "seed2": (36, 766),
            "seed3": (36, 766),
        },
    },
    ("GC", "latin"): {
        1.0: {
            "suffix": (33, 781),
            "seed0": (33, 781),
            "seed1": (33, 781),
            "seed2": (33, 781),
            "seed3": (33, 781),
        },
        0.75: {
            "suffix": (32, 784),
            "seed0": (32, 781),
            "seed1": (32, 781),
            "seed2": (32, 781),
            "seed3": (32, 780),
        },
        0.5: {
            "suffix": (33, 782),
            "seed0": (33, 780),
            "seed1": (33, 780),
            "seed2": (33, 780),
            "seed3": (33, 779),
        },
        0.25: {
            "suffix": (32, 732),
            "seed0": (33, 731),
            "seed1": (34, 733),
            "seed2": (33, 733),
            "seed3": (33, 733),
        },
    },
    ("IT", "english"): {
        1.0: {
            "suffix": (35, 839),
            "seed0": (35, 839),
            "seed1": (35, 839),
            "seed2": (35, 839),
            "seed3": (35, 839),
        },
        0.75: {
            "suffix": (34, 818),
            "seed0": (35, 825),
            "seed1": (35, 824),
            "seed2": (35, 825),
            "seed3": (35, 826),
        },
        0.5: {
            "suffix": (35, 789),
            "seed0": (35, 799),
            "seed1": (35, 800),
            "seed2": (35, 799),
            "seed3": (35, 800),
        },
        0.25: {
            "suffix": (35, 782),
            "seed0": (35, 782),
            "seed1": (35, 784),
            "seed2": (35, 785),
            "seed3": (36, 785),
        },
    },
    ("IT", "latin"): {
        1.0: {
            "suffix": (35, 785),
            "seed0": (35, 785),
            "seed1": (35, 785),
            "seed2": (35, 785),
            "seed3": (35, 785),
        },
        0.75: {
            "suffix": (34, 780),
            "seed0": (34, 785),
            "seed1": (34, 784),
            "seed2": (34, 784),
            "seed3": (34, 785),
        },
        0.5: {
            "suffix": (35, 779),
            "seed0": (34, 782),
            "seed1": (34, 784),
            "seed2": (34, 784),
            "seed3": (34, 785),
        },
        0.25: {
            "suffix": (35, 746),
            "seed0": (34, 749),
            "seed1": (35, 748),
            "seed2": (34, 747),
            "seed3": (34, 750),
        },
    },
}

# The verdict distribution over all 144 geometry
# rung-cell verdicts (24 rung-cells times the six
# geometries, the rung record's prefix verdict included).
VERDICT_COUNTS = {
    "shape-outside-analogues": 144,
}


class CutGeometryAttributionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_real = json.loads(FROZEN_REAL.read_text())
        self.frozen_ladder = json.loads(FROZEN_LADDER.read_text())
        self.frozen_matched = json.loads(FROZEN_MATCHED.read_text())
        self.declared = self.artifact["declared"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.KIND_ID["homo_cut_geom"], 30)
        self.assertEqual(homo.N_CUT_SEEDS, 4)
        self.assertEqual(homo.CUT_GEOM_RUNG_KEYS, (
            "real_rung_kept_pairs",
            "real_rung_boundary_carried_pairs",
            "real_rung_profile",
            "invariants",
            "verdict",
        ))
        self.assertTrue(
            str(homo.CUT_GEOM_ARTIFACT_PATH).endswith(
                "voynich-homophonic-cut-geometry-attribution.json"
            )
        )
        self.assertEqual(self.declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(self.declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(
            sorted(self.declared),
            [
                "band_reference_rule", "base_seed", "boundary_rule",
                "bridge_gate_rule", "closure_rule",
                "cut_geometry_rule", "exclusion_rule", "invariants",
                "machinery_rule", "mapped", "mass_rule",
                "models_rule", "record_rule", "roster_rule",
                "seed_kinds", "split_rule", "state_note",
                "verdict_rule",
            ],
        )
        self.assertEqual(
            sorted(self.declared["invariants"]),
            [
                "empty_type_count", "pair_entropy",
                "self_pair_share", "sorted_pair_multiset",
                "sorted_symbol_marginals", "top_k_shares",
            ],
        )
        self.assertEqual(
            sorted(self.artifact),
            ["bridge_gate", "declared", "files", "what"],
        )
        self.assertEqual(
            self.artifact["bridge_gate"],
            {
                "status": "verified",
                "fields_compared": 813,
                "ladder_gate_fields": 693,
                "geometry_replay_checks": 120,
            },
        )

    def test_the_cut_geometry_declaration(self) -> None:
        rule = self.declared["cut_geometry_rule"]
        self.assertIn(
            "the prefix cut prices the sequence's first mass "
            "positions (the real-at-basis ladder's own row, "
            "verified against that artifact in the gate), the "
            "suffix cut prices the sequence's last mass positions",
            rule,
        )
        self.assertIn(
            "so one seed's rung submasses are nested subsets; the "
            "real's cut under any geometry can move its own "
            "profile both ways, every direction is open per "
            "geometry and per rung, and every row is recorded with "
            "no selection performed", rule,
        )
        mass = self.declared["mass_rule"]
        self.assertIn(
            "every geometry row prices its rung's mass exactly "
            "(the rung's basis - 1 pairs, the exact full-width "
            "mass every one of the frozen rung's cut rows prices), "
            "the mass-match identity enforced in code on every row "
            "before any envelope is formed", mass,
        )
        self.assertIn(
            "its expected profile is the whole sequence's profile "
            "and not the prefix cut's, and this is the declared "
            "attribution arithmetic the row verdicts are read "
            "against", mass,
        )
        seeds = self.declared["seed_kinds"]
        self.assertIn(
            "the declared new seed kind homo_cut_geom (id 30), "
            "positions 0 to 3, per file with the language slot "
            "fixed at 0 because the real's side is identical for "
            "both languages of a file", seeds,
        )
        self.assertIn(
            "so one seed's rung submasses are nested subsets and "
            "no selection is performed over seeds", seeds,
        )
        verdict = self.declared["verdict_rule"]
        self.assertIn(
            "a geometry rung-cell is "
            "shape-consistent-with-homophonic-encoding only when "
            "every declared invariant of that row's re-priced "
            "glyph-block profile sits inside the closed range of "
            "its rung's matched band's glyph-block profiles", verdict,
        )
        self.assertIn(
            "the declared question is asked over all 144 geometry "
            "rung-cell verdicts together (24 rung-cells times the "
            "six geometries, the anchor rung's 24 the declared "
            "degenerate identity cases)", verdict,
        )
        gate = self.declared["bridge_gate_rule"]
        self.assertIn(
            "813 fields all told", gate,
        )
        self.assertIn(
            "the suffix and random rows carry no frozen "
            "counterpart and ride on the declared geometry rule, "
            "whose mass-match and degenerate anchor identities "
            "abort on any divergence", gate,
        )
        self.assertIn(
            "this instrument contains no assignment search anywhere",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "no split applies", self.declared["split_rule"],
        )
        self.assertIn(
            "no score table is built or used",
            self.declared["models_rule"],
        )
        self.assertIn(
            "no scalar margin is formed",
            self.declared["closure_rule"],
        )
        self.assertIn(
            "the family's declared exclusion format is not "
            "re-scoped by this artifact",
            self.declared["exclusion_rule"],
        )
        self.assertIn(
            "the rung bands are the frozen matched-basis ladder's "
            "rung member profiles taken by reference, the same "
            "bands the real-at-basis ladder priced",
            self.declared["band_reference_rule"],
        )
        self.assertIn(
            "no encoding is re-run on the band side anywhere",
            self.declared["roster_rule"],
        )
        self.assertIn(
            "the standing alphabet-width disclosure carries "
            "unchanged",
            self.declared["boundary_rule"],
        )
        self.assertIn(
            "126 unmapped events inside ZL's 218,663, 1,769 inside "
            "GC's 186,708, none inside IT's 220,532",
            self.declared["state_note"],
        )
        record = self.declared["record_rule"]
        self.assertIn(
            "per cell the artifact records the real-at-basis "
            "ladder's cell record re-derived fresh (verified "
            "against the frozen real-at-basis ladder artifact in "
            "the gate) and the four declared rungs in order", record,
        )

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "Sixteenth declared measurement, the cut-geometry "
            "attribution instrument",
            "do they re-price the real the same way, so the "
            "deepening is mass alone, or do they disagree, so the "
            "real's own ordering carries it",
            "the declared new seed kind homo_cut_geom (id 30), "
            "positions 0 to 3, per file with the language slot "
            "fixed at 0",
            "so one seed's rung submasses are nested subsets across "
            "the rungs and no selection is performed over seeds",
            "the rung-cell verdicts asked over all 144 geometry "
            "rung-cells together (24 rung-cells times the six "
            "geometries, the anchor rung's 24 the declared "
            "degenerate identity cases)",
            "813 fields all told",
            "the gate ran at 0 problems, 813 fields compared",
            "anchor degenerate identity for all six geometries True "
            "per file",
            "seed 0's rung submasses nested subsets True per file",
            "at the anchor rung every geometry's row is the "
            "degenerate identity (68,616 carried, 928 empties, "
            "self 0.065848, top_1 0.070481, top_10 0.424435, "
            "top_50 0.893671, entropy 4.010179, every row verdict "
            "shape-outside-analogues with all eight tests outside)",
            "the suffix row carries 52,045 pairs and prices 942 "
            "empties, self 0.060009, top_1 0.072428, top_10 "
            "0.415296, top_50 0.888714 and entropy 4.031522",
            "every probed row verdict shape-outside-analogues with "
            "all eight tests outside",
            "the random rows' scalars stay at the anchor's "
            "neighborhood down the whole ladder (self near 0.066, "
            "entropy near 4.0 nats)",
            "the prefix row's self rises 0.065848, 0.068229, "
            "0.073015 and 0.083007 down the rungs with entropy "
            "4.010179, 4.014465, 3.982947 and 3.904198",
            "same-mass cuts already disagreeing in both directions "
            "away from the mass-only expectation at this cell",
            "nothing here is a reading or a language claim",
        ):
            self.assertIn(phrase, doc)
        self.assertEqual(
            " ".join(doc.split()).count(
                "nothing here is a reading or a language claim"
            ),
            15,
        )

    def test_the_truthful_question(self) -> None:
        what = self.artifact["what"]
        self.assertIn(
            "the real's own kept-adjacent pair sequence cut at each "
            "rung's mass under six declared geometries", what,
        )
        self.assertIn(
            "the standing prefix cut the real-at-basis ladder "
            "priced, a suffix cut of the same mass, and four "
            "declared seeded random submasses of the same mass", what,
        )
        self.assertIn(
            "do same-mass cuts that differ only in geometry "
            "re-price the real the same way, so the real's "
            "deepening concentration is a function of mass alone, "
            "or do they disagree, so the real's own ordering "
            "carries it", what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading",
            what,
        )

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_cut_geometry_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 813)
        self.assertEqual(
            self.artifact["bridge_gate"]["fields_compared"], fields
        )

    def test_prefix_records_match_frozen(self) -> None:
        for code in FILES:
            events, unmapped, kept, standing, anchor = REAL[code]
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen_real["files"][code][language]
                self.assertEqual(cell["stream_events"], events)
                self.assertEqual(cell["unmapped_events"], unmapped)
                self.assertEqual(cell["kept_pairs"], kept)
                self.assertEqual(
                    cell["standing_plant_length"], standing
                )
                for key in homo.MATCHED_REAL_RECORD_KEYS:
                    self.assertEqual(cell[key], frozen[key], key)
                rungs = cell["rungs"]
                self.assertEqual(len(rungs), len(RUNGS))
                for i, rung in enumerate(RUNGS):
                    self.assertEqual(rung, rungs[i]["run"])
                    expected = (
                        anchor if rung == 1.0
                        else int(rung * anchor)
                    )
                    self.assertEqual(
                        expected, RUNG_BASES[code][i]
                    )
                    for key in homo.CUT_GEOM_RUNG_KEYS:
                        self.assertEqual(
                            rungs[i][key], frozen["rungs"][i][key],
                            (code, language, rung, key),
                        )

    def test_mass_match_identity(self) -> None:
        for code in FILES:
            for language in LANGS:
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    mass = RUNG_BASES[code][i] - 1
                    self.assertEqual(
                        rungs[i]["match_basis_events"], mass + 1
                    )
                    self.assertEqual(
                        rungs[i]["real_rung_kept_pairs"], mass
                    )
                    self.assertEqual(
                        rungs[i]["real_rung_boundary_carried_pairs"]
                        + rungs[i]["real_rung_profile"]["total_pairs"],
                        mass,
                    )
                    for name, geom, seed in zip(
                        GEOM_NAMES, GEOMS, SEEDS
                    ):
                        row = rungs[i]["geometries"][GEOM_NAMES.index(
                            name
                        )]
                        self.assertEqual(row["geometry"], geom)
                        if seed is None:
                            self.assertNotIn("seed_index", row)
                        else:
                            self.assertEqual(row["seed_index"], seed)
                        self.assertEqual(row["run"], rung)
                        self.assertEqual(row["cut_mass_pairs"], mass)
                        self.assertEqual(
                            row["boundary_carried_pairs"]
                            + row["profile"]["total_pairs"],
                            mass,
                        )

    def test_degenerate_anchor_identity(self) -> None:
        for code in FILES:
            for language in LANGS:
                rung = self.artifact["files"][code][language]["rungs"][0]
                matched = self.frozen_matched["files"][code][language]
                self.assertEqual(
                    rung["real_rung_profile"],
                    matched["real_profile"],
                )
                self.assertEqual(
                    rung["real_rung_boundary_carried_pairs"],
                    CARRIED_ANCHOR[code],
                )
                for name, row in zip(
                    GEOM_NAMES, rung["geometries"]
                ):
                    self.assertEqual(
                        row["profile"],
                        matched["real_profile"],
                        (code, language, name),
                    )
                    self.assertEqual(
                        row["boundary_carried_pairs"],
                        CARRIED_ANCHOR[code],
                        (code, language, name),
                    )

    def test_nesting(self) -> None:
        for code in FILES:
            first, second = homo._real_pair_sequence(code)
            total = len(first)
            self.assertEqual(total, REAL[code][2])
            for seed_index in range(homo.N_CUT_SEEDS):
                seed = homo._seed(
                    homo.CELL_ID[code],
                    homo.KIND_ID["homo_cut_geom"], 0, seed_index,
                )
                perm = np.random.default_rng(seed).permutation(total)
                takes = []
                for i, rung in enumerate(RUNGS):
                    mass = RUNG_BASES[code][i] - 1
                    takes.append(set(perm[:mass].tolist()))
                self.assertTrue(
                    takes[3] <= takes[2] <= takes[1] <= takes[0],
                    (code, seed_index),
                )

    def test_scalar_pins(self) -> None:
        for (code, language), table in GEOM_PIN.items():
            rungs = self.artifact["files"][code][language]["rungs"]
            for i, rung in enumerate(RUNGS):
                for name, row_pin in table[rung].items():
                    row = rungs[i]["geometries"][
                        GEOM_NAMES.index(name)
                    ]
                    tests = row["invariants"]
                    for key, triple in row_pin.items():
                        self.assertEqual(
                            triple[0], row["profile"][key],
                            (code, language, rung, name, key),
                        )
                        self.assertEqual(
                            (triple[1], triple[2]),
                            (
                                tests[key]["band_low"],
                                tests[key]["band_high"],
                            ),
                            (code, language, rung, name, key),
                        )
        # the ZL english suffix descent, pinned from the probes
        rungs = self.artifact["files"]["ZL"]["english"]["rungs"]
        suffix_self = (0.065848, 0.060009, 0.058642, 0.058701)
        suffix_ent = (
            4.010179, 4.031522, 4.024671, 3.97606,
        )
        for i, rung in enumerate(RUNGS):
            profile = rungs[i]["geometries"][0]["profile"]
            self.assertEqual(
                profile["self_pair_share"], suffix_self[i], rung
            )
            self.assertEqual(
                profile["pair_entropy"], suffix_ent[i], rung
            )
            self.assertEqual(
                rungs[i]["geometries"][0]["boundary_carried_pairs"],
                SUFFIX_CARRIED_ZL[i], rung,
            )

    def test_vector_outside_counts(self) -> None:
        for (code, language), table in VECTOR_GEOM.items():
            rungs = self.artifact["files"][code][language]["rungs"]
            for i, rung in enumerate(RUNGS):
                for name, counts in table[rung].items():
                    row = rungs[i]["geometries"][
                        GEOM_NAMES.index(name)
                    ]
                    share_out = row["invariants"][
                        "symbol_shares"
                    ]["outside"]
                    pair_out = row["invariants"][
                        "pair_shares"
                    ]["outside"]
                    self.assertEqual(
                        len(share_out), counts[0],
                        (code, language, rung, name),
                    )
                    self.assertEqual(
                        len(pair_out), counts[1],
                        (code, language, rung, name),
                    )
                    for entry in share_out:
                        self.assertLess(entry["position"], 36)
                    for entry in pair_out:
                        self.assertLess(entry["position"], 1296)

    def test_verdict_table(self) -> None:
        counted = {}
        rows_total = 0
        for code in FILES:
            for language in LANGS:
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    verdicts = [rungs[i]["verdict"]] + [
                        row["verdict"]
                        for row in rungs[i]["geometries"]
                    ]
                    for verdict in verdicts:
                        counted[verdict] = counted.get(verdict, 0) + 1
                        rows_total += 1
        self.assertEqual(rows_total, 144)
        self.assertEqual(counted, VERDICT_COUNTS)

    def test_envelope_rederivation(self) -> None:
        for code in FILES:
            for language in LANGS:
                frozen_cell = self.frozen_ladder["files"][code][
                    language
                ]
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    band = [
                        {"profile": row["matched_profile"]}
                        for row in
                        frozen_cell["rungs"][i]["members_profiles"]
                    ]
                    for name, row in zip(
                        GEOM_NAMES, rungs[i]["geometries"]
                    ):
                        fresh = homo._search_free_envelope(
                            row["profile"], band
                        )
                        self.assertEqual(
                            fresh, row["invariants"],
                            (code, language, rung, name),
                        )
                        outside = [
                            key for key, test in fresh.items()
                            if not test["inside"]
                        ]
                        self.assertEqual(
                            outside, row["outside_invariants"]
                        )
                        verdict = (
                            "shape-consistent-with-"
                            "homophonic-encoding"
                            if not outside
                            else "shape-outside-analogues"
                        )
                        self.assertEqual(verdict, row["verdict"])

    def test_one_geometry_row_recompute(self) -> None:
        fresh = homo._real_geometry_row(
            "ZL", "english", 0.5, "suffix", None,
            self.frozen_real, self.frozen_ladder,
        )
        stored = self.artifact["files"]["ZL"]["english"]["rungs"][2][
            "geometries"
        ][0]
        self.assertEqual(fresh, stored)
        fresh_seed = homo._real_geometry_row(
            "ZL", "english", 0.25, "random", 2,
            self.frozen_real, self.frozen_ladder,
        )
        stored_seed = self.artifact["files"]["ZL"]["english"][
            "rungs"
        ][3]["geometries"][3]
        self.assertEqual(fresh_seed, stored_seed)

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
