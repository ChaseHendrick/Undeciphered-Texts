# The stream-position suite: the seventeenth measurement's declared
# artifact against its frozen predecessors. Hand constants pin the
# declared boundaries, the twelve segment sizes, the seed-kind
# registry's unchanged tail and the whole sequence's identity; the
# artifact pins are read from the frozen run of 29 October 2026 with
# the bridge gate verified at 102 fields (17 per cell times six
# cells) and the direction tables recorded for every segment.
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/"
    "voynich-homophonic-stream-positions.json"
).resolve()
FROZEN_REAL = Path(
    "docs/research-notes/"
    "voynich-homophonic-real-at-basis-ladder.json"
).resolve()

SCALAR_KEYS = [
    "empty_type_count", "self_pair_share", "top_1_share",
    "top_10_share", "top_50_share", "pair_entropy",
]

# code -> (kept pairs, the four declared end positions), the first
# three boundaries at int(quarter x the anchor basis) positions and
# the last boundary the sequence's end; every kept pair total is
# three over a multiple of four.
STREAM_SHAPES = {
    "ZL": (218415, [54604, 109208, 163812, 218415]),
    "GC": (183199, [45800, 91600, 137400, 183199]),
    "IT": (220531, [55133, 110266, 165399, 220531]),
}

# code -> the twelve implied segment sizes, the first three equal
# and the remainder landing on the last segment per file.
SEGMENT_PAIRS = {
    "ZL": [54604, 54604, 54604, 54603],
    "GC": [45800, 45800, 45800, 45799],
    "IT": [55133, 55133, 55133, 55132],
}
# The stream-position pins, read from the frozen
# stream-position run of 29 October 2026: each
# per-file whole profile's six scalars and each
# segment's six scalars beside its direction record,
# every entry recorded, no margin formed.
WHOLE_SCALARS = {
    "ZL": {
        "empty_type_count": 928,
        "self_pair_share": 0.065848,
        "top_1_share": 0.070481,
        "top_10_share": 0.424435,
        "top_50_share": 0.893671,
        "pair_entropy": 4.010179,
    },
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
    "IT": {
        "empty_type_count": 984,
        "self_pair_share": 0.065777,
        "top_1_share": 0.071689,
        "top_10_share": 0.429316,
        "top_50_share": 0.89868,
        "pair_entropy": 3.980621,
    },
}

SEG_SCALARS = {
    # (code, segment) -> the segment profile's six scalars
    ("ZL", "english", 0): {
        "empty_type_count": 1028,
        "self_pair_share": 0.083007,
        "top_1_share": 0.06476,
        "top_10_share": 0.463045,
        "top_50_share": 0.914338,
        "pair_entropy": 3.904198,
    },
    ("ZL", "english", 1): {
        "empty_type_count": 1015,
        "self_pair_share": 0.062765,
        "top_1_share": 0.088227,
        "top_10_share": 0.437141,
        "top_50_share": 0.891247,
        "pair_entropy": 4.005492,
    },
    ("ZL", "english", 2): {
        "empty_type_count": 1007,
        "self_pair_share": 0.058582,
        "top_1_share": 0.069075,
        "top_10_share": 0.397112,
        "top_50_share": 0.88721,
        "pair_entropy": 4.051398,
    },
    ("ZL", "english", 3): {
        "empty_type_count": 1020,
        "self_pair_share": 0.058701,
        "top_1_share": 0.060117,
        "top_10_share": 0.448099,
        "top_50_share": 0.900713,
        "pair_entropy": 3.97606,
    },
    ("ZL", "latin", 0): {
        "empty_type_count": 1028,
        "self_pair_share": 0.083007,
        "top_1_share": 0.06476,
        "top_10_share": 0.463045,
        "top_50_share": 0.914338,
        "pair_entropy": 3.904198,
    },
    ("ZL", "latin", 1): {
        "empty_type_count": 1015,
        "self_pair_share": 0.062765,
        "top_1_share": 0.088227,
        "top_10_share": 0.437141,
        "top_50_share": 0.891247,
        "pair_entropy": 4.005492,
    },
    ("ZL", "latin", 2): {
        "empty_type_count": 1007,
        "self_pair_share": 0.058582,
        "top_1_share": 0.069075,
        "top_10_share": 0.397112,
        "top_50_share": 0.88721,
        "pair_entropy": 4.051398,
    },
    ("ZL", "latin", 3): {
        "empty_type_count": 1020,
        "self_pair_share": 0.058701,
        "top_1_share": 0.060117,
        "top_10_share": 0.448099,
        "top_50_share": 0.900713,
        "pair_entropy": 3.97606,
    },
    ("GC", "english", 0): {
        "empty_type_count": 840,
        "self_pair_share": 0.021603,
        "top_1_share": 0.057632,
        "top_10_share": 0.383269,
        "top_50_share": 0.8276,
        "pair_entropy": 4.337008,
    },
    ("GC", "english", 1): {
        "empty_type_count": 831,
        "self_pair_share": 0.011493,
        "top_1_share": 0.04601,
        "top_10_share": 0.386106,
        "top_50_share": 0.802313,
        "pair_entropy": 4.431385,
    },
    ("GC", "english", 2): {
        "empty_type_count": 814,
        "self_pair_share": 0.017204,
        "top_1_share": 0.05186,
        "top_10_share": 0.371746,
        "top_50_share": 0.806232,
        "pair_entropy": 4.428392,
    },
    ("GC", "english", 3): {
        "empty_type_count": 837,
        "self_pair_share": 0.013229,
        "top_1_share": 0.062981,
        "top_10_share": 0.395967,
        "top_50_share": 0.819398,
        "pair_entropy": 4.341177,
    },
    ("GC", "latin", 0): {
        "empty_type_count": 840,
        "self_pair_share": 0.021603,
        "top_1_share": 0.057632,
        "top_10_share": 0.383269,
        "top_50_share": 0.8276,
        "pair_entropy": 4.337008,
    },
    ("GC", "latin", 1): {
        "empty_type_count": 831,
        "self_pair_share": 0.011493,
        "top_1_share": 0.04601,
        "top_10_share": 0.386106,
        "top_50_share": 0.802313,
        "pair_entropy": 4.431385,
    },
    ("GC", "latin", 2): {
        "empty_type_count": 814,
        "self_pair_share": 0.017204,
        "top_1_share": 0.05186,
        "top_10_share": 0.371746,
        "top_50_share": 0.806232,
        "pair_entropy": 4.428392,
    },
    ("GC", "latin", 3): {
        "empty_type_count": 837,
        "self_pair_share": 0.013229,
        "top_1_share": 0.062981,
        "top_10_share": 0.395967,
        "top_50_share": 0.819398,
        "pair_entropy": 4.341177,
    },
    ("IT", "english", 0): {
        "empty_type_count": 1051,
        "self_pair_share": 0.083549,
        "top_1_share": 0.065613,
        "top_10_share": 0.469072,
        "top_50_share": 0.918903,
        "pair_entropy": 3.871494,
    },
    ("IT", "english", 1): {
        "empty_type_count": 1052,
        "self_pair_share": 0.063603,
        "top_1_share": 0.089513,
        "top_10_share": 0.441593,
        "top_50_share": 0.897695,
        "pair_entropy": 3.972243,
    },
    ("IT", "english", 2): {
        "empty_type_count": 1032,
        "self_pair_share": 0.05686,
        "top_1_share": 0.070918,
        "top_10_share": 0.398919,
        "top_50_share": 0.888273,
        "pair_entropy": 4.041147,
    },
    ("IT", "english", 3): {
        "empty_type_count": 1064,
        "self_pair_share": 0.058704,
        "top_1_share": 0.060903,
        "top_10_share": 0.455375,
        "top_50_share": 0.905808,
        "pair_entropy": 3.935649,
    },
    ("IT", "latin", 0): {
        "empty_type_count": 1051,
        "self_pair_share": 0.083549,
        "top_1_share": 0.065613,
        "top_10_share": 0.469072,
        "top_50_share": 0.918903,
        "pair_entropy": 3.871494,
    },
    ("IT", "latin", 1): {
        "empty_type_count": 1052,
        "self_pair_share": 0.063603,
        "top_1_share": 0.089513,
        "top_10_share": 0.441593,
        "top_50_share": 0.897695,
        "pair_entropy": 3.972243,
    },
    ("IT", "latin", 2): {
        "empty_type_count": 1032,
        "self_pair_share": 0.05686,
        "top_1_share": 0.070918,
        "top_10_share": 0.398919,
        "top_50_share": 0.888273,
        "pair_entropy": 4.041147,
    },
    ("IT", "latin", 3): {
        "empty_type_count": 1064,
        "self_pair_share": 0.058704,
        "top_1_share": 0.060903,
        "top_10_share": 0.455375,
        "top_50_share": 0.905808,
        "pair_entropy": 3.935649,
    },
}

SEG_DIRECTIONS = {
    # (code, segment) -> the direction record vs the whole
    ("ZL", "english", 0): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "english", 1): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "english", 2): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "english", 3): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 0): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("ZL", "latin", 1): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("ZL", "latin", 2): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("ZL", "latin", 3): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 0): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "english", 1): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 2): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "english", 3): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 0): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("GC", "latin", 1): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 2): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "above", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("GC", "latin", 3): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 0): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "english", 1): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "english", 2): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "english", 3): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 0): {"empty_type_count": "above", "self_pair_share": "above", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
    ("IT", "latin", 1): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "above", "top_10_share": "above", "top_50_share": "below", "pair_entropy": "below"},
    ("IT", "latin", 2): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "below", "top_50_share": "below", "pair_entropy": "above"},
    ("IT", "latin", 3): {"empty_type_count": "above", "self_pair_share": "below", "top_1_share": "below", "top_10_share": "above", "top_50_share": "above", "pair_entropy": "below"},
}
class StreamPositionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_real = json.loads(FROZEN_REAL.read_text())

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.STREAM_QUARTERS, (0.25, 0.5, 0.75, 1.0))
        self.assertEqual(
            homo.STREAM_SCALARS,
            (
                "empty_type_count", "self_pair_share",
                "top_1_share", "top_10_share", "top_50_share",
                "pair_entropy",
            ),
        )
        self.assertEqual(
            homo.STREAM_POS_ARTIFACT_PATH.name,
            "voynich-homophonic-stream-positions.json",
        )
        self.assertEqual(max(homo.KIND_ID.values()), 30)
        self.assertEqual(
            homo.KIND_ID["homo_cut_geom"], 30,
            "the seed-kind registry ends at the cut-geometry kind; "
            "the stream-position instrument draws no seed at all",
        )
        self.assertEqual(
            sorted(self.artifact["declared"]),
            [
                "base_seed", "boundary_rule", "closure_rule",
                "direction_rule", "exclusion_rule", "gate_rule",
                "machinery_rule", "mapped", "models_rule",
                "no_band_rule", "partition_rule", "record_rule",
                "roster_rule", "split_rule", "state_note",
                "summary_rule",
            ],
        )
        self.assertEqual(
            self.artifact["declared"]["base_seed"],
            homo.BASE_SEED,
        )
        self.assertEqual(
            self.artifact["declared"]["mapped"], homo.MAPPED_HOMO,
        )

    def test_gate_replay(self) -> None:
        problems, fields = homo._compare_stream_positions_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 102)
        self.assertEqual(
            self.artifact["bridge_gate"],
            {
                "status": "verified", "fields_compared": 102,
                "per_cell_fields": 17,
            },
        )

    def test_the_declared_sizes(self) -> None:
        for code in FILES:
            cell = self.artifact["files"][code]["english"]
            kept, bounds = STREAM_SHAPES[code]
            self.assertEqual(cell["kept_pairs"], kept, code)
            self.assertEqual(cell["boundaries"], bounds, code)
            self.assertEqual(
                [segment["pairs"] for segment in cell["segments"]],
                SEGMENT_PAIRS[code], code,
            )
            self.assertEqual(
                sum(segment["pairs"] for segment in cell["segments"]),
                kept, code,
            )

    def test_the_whole_gate(self) -> None:
        for code in FILES:
            for language in LANGS:
                fresh = homo._stream_position_profiles(code)
                stored = self.artifact["files"][code][language]
                self.assertEqual(
                    fresh["whole_profile"], stored["whole_profile"],
                    (code, language),
                )
                frozen = self.frozen_real["files"][code][language][
                    "rungs"
                ][0]["real_rung_profile"]
                self.assertEqual(
                    stored["whole_profile"], frozen, (code, language),
                )
                self.assertEqual(
                    stored["whole_boundary_carried_pairs"],
                    fresh["whole_boundary_carried_pairs"],
                    (code, language),
                )

    def test_the_partition_rebuild(self) -> None:
        first, second = homo._real_pair_sequence("ZL")
        real = homo._homo_real_stream("ZL")
        mark = len(real["mapped_chars"]) - 1
        for code in FILES:
            first, second = homo._real_pair_sequence(code)
            real = homo._homo_real_stream(code)
            mark = len(real["mapped_chars"]) - 1
            stored = self.artifact["files"][code]["english"]
            previous = 0
            for index, bound in enumerate(stored["boundaries"]):
                matrix = np.zeros((37, 37))
                np.add.at(
                    matrix,
                    (first[previous:bound],
                     second[previous:bound]),
                    1.0,
                )
                profile = homo._profile_facts(
                    homo._glyph_block_matrix(matrix, mark)
                )
                carried = homo._boundary_carried_pairs(matrix, mark)
                segment = stored["segments"][index]
                self.assertEqual(
                    profile, segment["profile"],
                    (code, index),
                )
                self.assertEqual(
                    carried, segment["boundary_carried_pairs"],
                    (code, index),
                )
                self.assertEqual(
                    segment["profile"]["total_pairs"],
                    segment["pairs"] - carried,
                    (code, index),
                )
                self.assertEqual(
                    segment["first_position"], previous,
                    (code, index),
                )
                self.assertEqual(
                    segment["end_position"], bound, (code, index),
                )
                previous = bound
            total_sum = sum(
                segment["profile"]["total_pairs"]
                for segment in stored["segments"]
            )
            self.assertEqual(
                total_sum, stored["whole_profile"]["total_pairs"],
                code,
            )
            carried_sum = sum(
                segment["boundary_carried_pairs"]
                for segment in stored["segments"]
            )
            self.assertEqual(
                carried_sum, stored["whole_boundary_carried_pairs"],
                code,
            )

    def test_the_direction_table(self) -> None:
        for code in FILES:
            for language in LANGS:
                stored = self.artifact["files"][code][language]
                whole = stored["whole_profile"]
                for segment in stored["segments"]:
                    fresh = homo._direction_vs_whole(
                        segment["profile"], whole,
                    )
                    self.assertEqual(
                        fresh, segment["direction"],
                        (code, language, segment["segment"]),
                    )
                    pinned = SEG_DIRECTIONS[
                        (code, language, segment["segment"])
                    ]
                    self.assertEqual(
                        segment["direction"], pinned,
                        (code, language, segment["segment"]),
                    )
                    pinned_scalars = SEG_SCALARS[
                        (code, language, segment["segment"])
                    ]
                    for key in SCALAR_KEYS:
                        self.assertEqual(
                            segment["profile"][key],
                            pinned_scalars[key],
                            (code, language, segment["segment"], key),
                        )

    def test_scalar_pins(self) -> None:
        for code in FILES:
            whole = self.artifact["files"][code]["english"][
                "whole_profile"
            ]
            pinned = WHOLE_SCALARS[code]
            for key in SCALAR_KEYS:
                self.assertEqual(whole[key], pinned[key], (code, key))

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

    def test_module_docstring_declaration(self) -> None:
        doc = Path(homo.__file__).read_text()
        phrases = (
            "Seventeenth declared measurement, the stream-position "
            "instrument",
            "declared after the cut-geometry attribution instrument "
            "attributed the real-at-basis ladder's deepening to the "
            "real's own ordering and located the ordering effect in "
            "the stream's opening pairs",
            "is the real's concentration a smooth function of "
            "stream position, or do particular spans of the stream "
            "carry it?",
            "the real's own ordered kept-adjacent pair sequence "
            "divided into four declared equal-count consecutive "
            "segments",
            "the first three boundaries sit at int(quarter x the "
            "anchor basis) positions with the anchor basis the kept "
            "pair total + 1, at the quarters 0.25, 0.5 and 0.75, and "
            "the last boundary is the sequence's end",
            "every file's kept pair total is three over a multiple "
            "of four, so each file's first three segments are the "
            "same size and the remainder lands on the last segment",
            "for ZL, 54,604, 54,604, 54,604 and 54,603 kept-adjacent "
            "pairs, for GC 45,800, 45,800, 45,800 and 45,799, and "
            "for IT 55,133, 55,133, 55,133 and 55,132",
            "each segment prices every kept-adjacent pair of its "
            "own consecutive interval, no pair dropped, no pair "
            "synthesized, so the four segments partition the whole "
            "sequence exactly",
            "no band is loaded, no envelope is formed, no rung band "
            "side, no verdict and no scalar margin is produced "
            "anywhere",
            "whether its value sits above, below or equal to the "
            "whole sequence's value at the stored 6-decimal "
            "rounding",
            "the bridge gate first, per cell",
            "17 fields per cell, 102 fields all told",
            "the gate ran at 0 problems, 102 fields compared",
            "ZL's end positions 54,604, 109,208, 163,812 and "
            "218,415 give the four sizes 54,604, 54,604, 54,604 and "
            "54,603",
            "IT's 55,133, 110,266, 165,399 and 220,531 give 55,133, "
            "55,133, 55,133 and 55,132",
            "the four segments' kept pairs sum to the whole's "
            "(218,415, 183,199 and 220,531), their block totals sum "
            "to the whole's (149,799, 111,815 and 147,651) and "
            "their boundary-carried counts sum to the whole's "
            "(68,616, 71,384 and 72,880)",
            "the opening segment (54,604 pairs, 16,571 carried) "
            "prices empties 1,028, self 0.083007, top_1 0.06476, "
            "top_10 0.463045, top_50 0.914338 and entropy 3.904198",
            "the second segment (54,604 pairs, 17,529 carried) "
            "prices empties 1,015, self 0.062765, top_1 0.088227, "
            "top_10 0.437141, top_50 0.891247 and entropy 4.005492",
            "the third segment (54,604 pairs, 17,340 carried) "
            "prices empties 1,007, self 0.058582, top_1 0.069075, "
            "top_10 0.397112, top_50 0.88721 and entropy 4.051398",
            "the closing segment (54,603 pairs, 17,176 carried) "
            "prices empties 1,020, self 0.058701, top_1 0.060117, "
            "top_10 0.448099, top_50 0.900713 and entropy 3.97606",
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
            "the real's own kept-adjacent pair sequence divided "
            "into four declared equal-count consecutive segments",
            what,
        )
        self.assertIn(
            "the four segment profiles recorded beside each other "
            "and beside the whole-sequence profile, no bands and no "
            "envelopes", what,
        )
        self.assertIn(
            "is the real's concentration a smooth function of "
            "stream position, or do particular spans of the stream "
            "carry it", what,
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
