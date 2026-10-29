# The real-at-basis ladder suite: the fifteenth measurement's
# declared artifact against its frozen predecessor. Hand constants
# pin the rung bases, the real record's masses and the rotating
# self-pair seam; the artifact pins are read from the frozen run of
# 27 October 2026 with the bridge gate verified at 693 fields (the
# matched-basis ladder's 657 anchors and the 36 real-record and
# anchor-rung replay checks) and all 24 rung-cell verdicts
# shape-outside-analogues.
import json
import unittest
from pathlib import Path

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
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

# Every rung-cell verdict is a shape-outside-analogue under the
# declared strict-all rule priced on the real's re-priced profile:
# 24 of 24. The inside scalar set moves with the real's own descent:
# GC latin's self_pair_share, the family's one standing inside
# invariant, is inside at its three upper rungs and outside at its
# 25 percent rung, while GC english's self_pair_share is outside
# below its band at its three upper rungs and inside at its 25
# percent rung - the first scalar entry under a mass-matched
# comparison.
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

# code -> the match-basis ladder's frozen members cut per rung and
# plants cut per rung, unchanged here: the bands are the frozen
# instrument's own facts taken by reference.
CUT_TABLE = {
    ("ZL", "english"): ((11, 11, 11, 12), (5, 5, 5, 5)),
    ("ZL", "latin"): ((5, 5, 7, 10), (5, 5, 5, 5)),
    ("GC", "english"): ((11, 11, 12, 12), (5, 5, 5, 5)),
    ("GC", "latin"): ((5, 6, 7, 10), (5, 5, 5, 5)),
    ("IT", "english"): ((0, 11, 11, 12), (0, 5, 5, 5)),
    ("IT", "latin"): ((0, 5, 7, 10), (0, 5, 5, 5)),
}

# code -> the record triple (stream_events, unmapped_events,
# kept_pairs, standing plant length) and the anchor basis = kept + 1.
REAL = {
    "ZL": (218663, 126, 218415, 218663, 218416),
    "GC": (186708, 1769, 183199, 186708, 183200),
    "IT": (220532, 0, 220531, 220532, 220532),
}

# code -> the anchor rung's boundary-carried pairs (the whole
# sequence's mark-carried pairs) and the ZL cell's carried quadruple
# at the anchor, 75, 50 and 25 percent rungs, pinned from the run.
CARRIED_ANCHOR = {"ZL": 68616, "GC": 71384, "IT": 72880}
CARRIED_ZL = (68616, 51440, 34099, 16570)

# GC english and GC latin's self_pair_share across the four rungs,
# the rotating seam: (real, band_low, band_high) per rung with the
# inside flag, pinned from the probes and verified from the artifact.
GC_SELF = {
    ("GC", "english"): (
        (0.015928, 0.018513, 0.027183),
        (0.016822, 0.018404, 0.027769),
        (0.016628, 0.018849, 0.027852),
        (0.021604, 0.018382, 0.025854),
    ),
    ("GC", "latin"): (
        (0.015928, 0.011979, 0.023941),
        (0.016822, 0.012489, 0.023941),
        (0.016628, 0.013329, 0.023837),
        (0.021604, 0.01295, 0.021521),
    ),
}
GC_INSIDE_SHAPE = {
    ("GC", "english"): (False, False, False, True),
    ("GC", "latin"): (True, True, True, False),
}
# The per-cell real-at-basis scalar pins, read from the
# frozen real-at-basis run of 27 October 2026: each pin is
# a (real, band_low, band_high) triple from the rung's
# declared envelope, the real's re-priced six scalars
# beside the frozen matched-basis ladder's band at its
# rung width.
REAL_PIN = {
    ("ZL", "english"): {
        1.0: {
            "empty_type_count": (928, 323, 454),
            "self_pair_share": (0.065848, 0.018692, 0.026719),
            "top_1_share": (0.070481, 0.018187, 0.035877),
            "top_10_share": (0.424435, 0.106088, 0.148334),
            "top_50_share": (0.893671, 0.305696, 0.355757),
            "pair_entropy": (4.010179, 5.928491, 6.102985),
        },
        0.75: {
            "empty_type_count": (950, 318, 464),
            "self_pair_share": (0.068229, 0.01884, 0.027095),
            "top_1_share": (0.073934, 0.018173, 0.035196),
            "top_10_share": (0.418115, 0.106088, 0.157183),
            "top_50_share": (0.892615, 0.305696, 0.368859),
            "pair_entropy": (4.014465, 5.92046, 6.115742),
        },
        0.5: {
            "empty_type_count": (980, 341, 495),
            "self_pair_share": (0.073015, 0.01878, 0.027796),
            "top_1_share": (0.076343, 0.015177, 0.034405),
            "top_10_share": (0.432937, 0.100396, 0.157691),
            "top_50_share": (0.899851, 0.305696, 0.370604),
            "pair_entropy": (3.982947, 5.90532, 6.108939),
        },
        0.25: {
            "empty_type_count": (1028, 376, 505),
            "self_pair_share": (0.083007, 0.018805, 0.027025),
            "top_1_share": (0.06476, 0.014518, 0.03463),
            "top_10_share": (0.463045, 0.100414, 0.160534),
            "top_50_share": (0.914338, 0.309486, 0.372217),
            "pair_entropy": (3.904198, 5.883769, 6.098317),
        },
    },
    ("ZL", "latin"): {
        1.0: {
            "empty_type_count": (928, 240, 503),
            "self_pair_share": (0.065848, 0.011829, 0.023974),
            "top_1_share": (0.070481, 0.013486, 0.02536),
            "top_10_share": (0.424435, 0.09782, 0.132009),
            "top_50_share": (0.893671, 0.268516, 0.336674),
            "pair_entropy": (4.010179, 5.980168, 6.252),
        },
        0.75: {
            "empty_type_count": (950, 283, 503),
            "self_pair_share": (0.068229, 0.012506, 0.023974),
            "top_1_share": (0.073934, 0.01335, 0.02536),
            "top_10_share": (0.418115, 0.097045, 0.134341),
            "top_50_share": (0.892615, 0.268516, 0.339127),
            "pair_entropy": (4.014465, 5.980168, 6.254451),
        },
        0.5: {
            "empty_type_count": (980, 360, 503),
            "self_pair_share": (0.073015, 0.013366, 0.024518),
            "top_1_share": (0.076343, 0.013618, 0.025917),
            "top_10_share": (0.432937, 0.09782, 0.132131),
            "top_50_share": (0.899851, 0.268516, 0.335977),
            "pair_entropy": (3.982947, 5.980168, 6.250767),
        },
        0.25: {
            "empty_type_count": (1028, 399, 537),
            "self_pair_share": (0.083007, 0.013527, 0.021909),
            "top_1_share": (0.06476, 0.013764, 0.025031),
            "top_10_share": (0.463045, 0.098316, 0.138755),
            "top_50_share": (0.914338, 0.272333, 0.348076),
            "pair_entropy": (3.904198, 5.951767, 6.248471),
        },
    },
    ("GC", "english"): {
        1.0: {
            "empty_type_count": (642, 318, 453),
            "self_pair_share": (0.015928, 0.018513, 0.027183),
            "top_1_share": (0.051049, 0.018386, 0.035403),
            "top_10_share": (0.373572, 0.106088, 0.15809),
            "top_50_share": (0.8066, 0.305406, 0.370289),
            "pair_entropy": (4.422831, 5.919417, 6.116692),
        },
        0.75: {
            "empty_type_count": (684, 335, 473),
            "self_pair_share": (0.016822, 0.018404, 0.027769),
            "top_1_share": (0.050598, 0.015821, 0.034743),
            "top_10_share": (0.368458, 0.103071, 0.157186),
            "top_50_share": (0.804229, 0.305406, 0.368975),
            "pair_entropy": (4.438165, 5.916585, 6.10912),
        },
        0.5: {
            "empty_type_count": (741, 359, 502),
            "self_pair_share": (0.016628, 0.018849, 0.027852),
            "top_1_share": (0.049955, 0.017005, 0.034804),
            "top_10_share": (0.371611, 0.106112, 0.158851),
            "top_50_share": (0.808924, 0.305386, 0.372036),
            "pair_entropy": (4.422221, 5.899352, 6.109574),
        },
        0.25: {
            "empty_type_count": (840, 399, 520),
            "self_pair_share": (0.021604, 0.018382, 0.025854),
            "top_1_share": (0.057634, 0.01885, 0.033087),
            "top_10_share": (0.383283, 0.109712, 0.164276),
            "top_50_share": (0.827594, 0.307336, 0.377631),
            "pair_entropy": (4.337033, 5.863478, 6.087147),
        },
    },
    ("GC", "latin"): {
        1.0: {
            "empty_type_count": (642, 262, 500),
            "self_pair_share": (0.015928, 0.011979, 0.023941),
            "top_1_share": (0.051049, 0.013384, 0.02536),
            "top_10_share": (0.373572, 0.097128, 0.133145),
            "top_50_share": (0.8066, 0.26876, 0.338741),
            "pair_entropy": (4.422831, 5.98016, 6.254936),
        },
        0.75: {
            "empty_type_count": (684, 307, 500),
            "self_pair_share": (0.016822, 0.012489, 0.023941),
            "top_1_share": (0.050598, 0.013366, 0.02536),
            "top_10_share": (0.368458, 0.097737, 0.136046),
            "top_50_share": (0.804229, 0.26876, 0.341342),
            "pair_entropy": (4.438165, 5.98016, 6.253207),
        },
        0.5: {
            "empty_type_count": (741, 376, 500),
            "self_pair_share": (0.016628, 0.013329, 0.023837),
            "top_1_share": (0.049955, 0.013609, 0.025776),
            "top_10_share": (0.371611, 0.098063, 0.134714),
            "top_50_share": (0.808924, 0.26876, 0.338778),
            "pair_entropy": (4.422221, 5.978656, 6.250384),
        },
        0.25: {
            "empty_type_count": (840, 414, 547),
            "self_pair_share": (0.021604, 0.01295, 0.021521),
            "top_1_share": (0.057634, 0.014424, 0.024548),
            "top_10_share": (0.383283, 0.099777, 0.140588),
            "top_50_share": (0.827594, 0.269632, 0.347807),
            "pair_entropy": (4.337033, 5.943103, 6.233837),
        },
    },
    ("IT", "english"): {
        1.0: {
            "empty_type_count": (984, 325, 449),
            "self_pair_share": (0.065777, 0.018701, 0.027087),
            "top_1_share": (0.071689, 0.018068, 0.035914),
            "top_10_share": (0.429316, 0.106088, 0.148471),
            "top_50_share": (0.89868, 0.30546, 0.35595),
            "pair_entropy": (3.980621, 5.927877, 6.102609),
        },
        0.75: {
            "empty_type_count": (990, 318, 462),
            "self_pair_share": (0.068127, 0.018887, 0.027333),
            "top_1_share": (0.075274, 0.018112, 0.035253),
            "top_10_share": (0.422317, 0.106088, 0.157263),
            "top_50_share": (0.897349, 0.30546, 0.369102),
            "pair_entropy": (3.988901, 5.920093, 6.116071),
        },
        0.5: {
            "empty_type_count": (1014, 338, 491),
            "self_pair_share": (0.073692, 0.018939, 0.027767),
            "top_1_share": (0.077426, 0.015138, 0.034458),
            "top_10_share": (0.437691, 0.100656, 0.157543),
            "top_50_share": (0.905603, 0.30546, 0.369888),
            "pair_entropy": (3.949893, 5.906326, 6.11015),
        },
        0.25: {
            "empty_type_count": (1051, 383, 507),
            "self_pair_share": (0.083551, 0.018882, 0.026675),
            "top_1_share": (0.065615, 0.014318, 0.034724),
            "top_10_share": (0.469085, 0.098647, 0.160437),
            "top_50_share": (0.918901, 0.309421, 0.372346),
            "pair_entropy": (3.871507, 5.885832, 6.098799),
        },
    },
    ("IT", "latin"): {
        1.0: {
            "empty_type_count": (984, 241, 500),
            "self_pair_share": (0.065777, 0.013217, 0.024029),
            "top_1_share": (0.071689, 0.013525, 0.02536),
            "top_10_share": (0.429316, 0.098044, 0.131821),
            "top_50_share": (0.89868, 0.268841, 0.336358),
            "pair_entropy": (3.980621, 5.980406, 6.252202),
        },
        0.75: {
            "empty_type_count": (990, 280, 500),
            "self_pair_share": (0.068127, 0.012518, 0.024029),
            "top_1_share": (0.075274, 0.013365, 0.02536),
            "top_10_share": (0.422317, 0.097707, 0.134148),
            "top_50_share": (0.897349, 0.268841, 0.338867),
            "pair_entropy": (3.988901, 5.980406, 6.254241),
        },
        0.5: {
            "empty_type_count": (1014, 353, 500),
            "self_pair_share": (0.073692, 0.013268, 0.024498),
            "top_1_share": (0.077426, 0.013587, 0.025896),
            "top_10_share": (0.437691, 0.098177, 0.131964),
            "top_50_share": (0.905603, 0.268841, 0.336261),
            "pair_entropy": (3.949893, 5.980406, 6.250893),
        },
        0.25: {
            "empty_type_count": (1051, 404, 535),
            "self_pair_share": (0.083551, 0.013499, 0.022046),
            "top_1_share": (0.065615, 0.013812, 0.025113),
            "top_10_share": (0.469085, 0.098242, 0.138286),
            "top_50_share": (0.918901, 0.27285, 0.34743),
            "pair_entropy": (3.871507, 5.951559, 6.248481),
        },
    },
}

# The per-rung vector outside counts (symbol positions out
# of 36, pair positions out of 1296), from the same run.
VECTOR_RUNGS = {
    ("ZL", "english"): {
        1.0: (35, 834),
        0.75: (33, 824),
        0.5: (33, 793),
        0.25: (36, 787),
    },
    ("ZL", "latin"): {
        1.0: (36, 780),
        0.75: (34, 779),
        0.5: (32, 782),
        0.25: (35, 746),
    },
    ("GC", "english"): {
        1.0: (36, 829),
        0.75: (36, 815),
        0.5: (35, 785),
        0.25: (35, 768),
    },
    ("GC", "latin"): {
        1.0: (33, 781),
        0.75: (32, 784),
        0.5: (33, 784),
        0.25: (33, 738),
    },
    ("IT", "english"): {
        1.0: (35, 839),
        0.75: (33, 827),
        0.5: (35, 802),
        0.25: (34, 785),
    },
    ("IT", "latin"): {
        1.0: (35, 785),
        0.75: (33, 782),
        0.5: (34, 785),
        0.25: (35, 752),
    },
}


class RealBasisLadderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen = json.loads(FROZEN_LADDER.read_text())
        self.frozen_matched = json.loads(FROZEN_MATCHED.read_text())
        self.declared = self.artifact["declared"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.REAL_LADDER_RUNG_KEYS, (
            "run", "match_basis_events", "real_rung_kept_pairs",
            "real_rung_boundary_carried_pairs", "real_rung_profile",
            "invariants", "outside_invariants", "verdict",
        ))
        self.assertTrue(
            str(homo.REAL_LADDER_ARTIFACT_PATH).endswith(
                "voynich-homophonic-real-at-basis-ladder.json"
            )
        )
        self.assertEqual(self.declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(self.declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(
            sorted(self.declared),
            [
                "band_reference_rule", "base_seed", "boundary_rule",
                "bridge_gate_rule", "closure_rule", "exclusion_rule",
                "invariants", "machinery_rule", "mapped", "mass_rule",
                "models_rule", "real_ladder_rule", "record_rule",
                "roster_rule", "seed_kinds", "split_rule",
                "state_note", "verdict_rule",
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
                "fields_compared": 693,
                "ladder_gate_fields": 657,
                "real_rung_replay_checks": 36,
            },
        )
        self.assertTrue(json.loads(FROZEN_LADDER.read_text())[
            "files"
        ] is not None)

    def test_the_real_ladder_declaration(self) -> None:
        rule = self.declared["real_ladder_rule"]
        self.assertIn(
            "the real's own kept-adjacent pair sequence re-priced "
            "at the matched-basis ladder's declared rungs", rule,
        )
        self.assertIn(
            "the anchor rung first at the cell's real counted pair "
            "total + 1 tokens (ZL 218,416, GC 183,200, IT 220,532)",
            rule,
        )
        self.assertIn(
            "then floor(p x the anchor basis) rungs at p 0.75, 0.50 "
            "and 0.25 (ZL 163,812, 109,208 and 54,604; GC 137,400, "
            "91,600 and 45,800; IT 165,399, 110,266 and 55,133)",
            rule,
        )
        self.assertIn(
            "at every rung the real prices its first basis - 1 "
            "kept-adjacent pairs through the same mark-excluded "
            "block and the same six summaries", rule,
        )
        self.assertIn(
            "the real's cut can move its own profile both ways", rule,
        )
        mass = self.declared["mass_rule"]
        self.assertIn(
            "the comparison at every rung is mass-matched on the "
            "paired side by the exact band arithmetic the "
            "matched-basis ladder priced", mass,
        )
        self.assertIn(
            "mass-matched on the real side by construction", mass,
        )
        self.assertIn(
            "the real's rung mass is its rung basis - 1 pairs and "
            "every one of the rung's cut rows prices its "
            "match_basis_events - 1 pairs full width", mass,
        )
        self.assertIn(
            "the mass-match identity verified against the frozen "
            "rung's rows before any envelope is formed", mass,
        )
        bands = self.declared["band_reference_rule"]
        self.assertIn(
            "the rung bands are the frozen matched-basis ladder's "
            "rung facts taken by reference", bands,
        )
        self.assertIn(
            "no encoding is re-run on the band side anywhere",
            self.declared["roster_rule"],
        )
        self.assertIn(
            "126 unmapped events inside ZL's 218,663, 1,769 inside "
            "GC's 186,708, none inside IT's 220,532",
            self.declared["state_note"],
        )
        self.assertIn(
            "contains no assignment search anywhere",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "no split applies", self.declared["split_rule"],
        )
        self.assertIn(
            "no seed is consumed anywhere in this instrument",
            self.declared["seed_kinds"],
        )
        record = self.declared["record_rule"]
        self.assertIn(
            "per cell the artifact records the real record once "
            "(verified against the frozen matched-basis ladder "
            "record) and the four declared rungs in order", record,
        )
        verdict = self.declared["verdict_rule"]
        self.assertIn(
            "priced per rung on the real's re-priced profile", verdict,
        )
        self.assertIn(
            "over all 24 rung-cell verdicts together", verdict,
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
        gate = self.declared["bridge_gate_rule"]
        self.assertIn(
            "the matched-basis ladder's gate exactly as that "
            "instrument declared it (the matched-truncation "
            "instrument's 540 anchor and replay fields plus the "
            "117 anchor-rung replay checks, 657 fields)", gate,
        )
        self.assertIn(
            "6 checks per cell, 36 checks total, 693 fields "
            "compared", gate,
        )
        self.assertIn(
            "no score table is built or used",
            self.declared["models_rule"],
        )
        self.assertIn(
            "the standing alphabet-width disclosure carries "
            "unchanged",
            self.declared["boundary_rule"],
        )

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "Fifteenth declared measurement, the real-at-basis "
            "ladder",
            "declared after the matched-basis ladder swept the "
            "truncation basis over the anchor rung and its 75, 50 "
            "and 25 percent rungs and read only the bands' "
            "movements at every descended rung",
            "its first basis - 1 kept-adjacent pairs",
            "the mass-match identity verified against the frozen "
            "rung's rows before any envelope is formed",
            "re-priced bands, so every rung's comparison is "
            "mass-matched on both sides for the first time in this "
            "family",
            "ZL's kept-adjacent pair sequence counts 218,415 "
            "ordered pairs, GC's 183,199 and IT's 220,531",
            "68,616 (ZL), 71,384 (GC) and 72,880 (IT) of those "
            "pairs carried by the boundary mark's row and column",
            "the gate ran at 657 fields compared, no problem",
            "the anchor rung's re-priced profile the frozen real "
            "profile exactly",
            "GC latin's self_pair_share, the family's one standing "
            "inside invariant, inside at its three upper rungs",
            "outside at its 25 percent rung (0.021604 against "
            "[0.01295, 0.021521])",
            "GC english's self_pair_share carries the counterpart "
            "motion, outside below its band at its three upper "
            "rungs",
            "and inside at its 25 percent rung",
            "every other cell's every rung stays all-eight-outside",
            "the real's own descents against the anchor scalars",
            "nothing here is a reading or a language claim",
        ):
            self.assertIn(phrase, doc)
        self.assertEqual(
            " ".join(doc.split()).count(
                "nothing here is a reading or a language claim"
            ),
             16,
        )

    def test_the_truthful_question(self) -> None:
        what = self.artifact["what"]
        self.assertIn(
            "the real's own kept-adjacent pair sequence re-priced "
            "at each rung beside them", what,
        )
        self.assertIn(
            "its first basis - 1 pairs, the exact full-width mass "
            "every one of the rung's cut rows prices", what,
        )
        self.assertIn(
            "every descended rung's comparison is mass-matched on "
            "both sides for the first time in this family", what,
        )
        self.assertIn(
            "does the real's own descending profile track the rung "
            "bands' descension or stay apart down the ladder in "
            "every (file, language) cell", what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading",
            what,
        )

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_real_ladder_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 693)
        self.assertEqual(
            self.artifact["bridge_gate"]["fields_compared"], fields
        )

    def test_real_record_and_bases(self) -> None:
        for code, row in REAL.items():
            events, unmapped, kept, standing, anchor = row
            real = homo._homo_real_stream(code)
            self.assertEqual(real["total_events"], events)
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen["files"][code][language]
                self.assertEqual(cell["stream_events"], events)
                self.assertEqual(cell["unmapped_events"], unmapped)
                self.assertEqual(cell["kept_pairs"], kept)
                self.assertEqual(
                    cell["real_full_width_total_pairs"], kept
                )
                self.assertEqual(
                    cell["standing_plant_length"], standing
                )
                self.assertTrue(cell["plants_at_source_identity"])
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
                        rungs[i]["match_basis_events"], expected
                    )
                    self.assertEqual(
                        expected, RUNG_BASES[code][i]
                    )
                    self.assertEqual(
                        rungs[i]["real_rung_kept_pairs"],
                        expected - 1,
                    )

    def test_carried_identities(self) -> None:
        for code in FILES:
            for language in LANGS:
                rungs = self.artifact["files"][code][language]["rungs"]
                self.assertEqual(
                    rungs[0]["real_rung_boundary_carried_pairs"],
                    CARRIED_ANCHOR[code],
                )
                for i, rung in enumerate(RUNGS):
                    mass = RUNG_BASES[code][i] - 1
                    carried = rungs[i][
                        "real_rung_boundary_carried_pairs"
                    ]
                    total = rungs[i]["real_rung_profile"][
                        "total_pairs"
                    ]
                    self.assertEqual(carried + total, mass)
                if code == "ZL":
                    self.assertEqual(
                        tuple(
                            rungs[i][
                                "real_rung_boundary_carried_pairs"
                            ]
                            for i in range(4)
                        ),
                        CARRIED_ZL,
                    )

    def test_mass_match_identity(self) -> None:
        for code in FILES:
            for language in LANGS:
                cuts, plant_cuts = CUT_TABLE[(code, language)]
                frozen_cell = self.frozen["files"][code][language]
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    mass = RUNG_BASES[code][i] - 1
                    self.assertEqual(
                        rungs[i]["match_basis_events"], mass + 1
                    )
                    for block, rows_key, expected in (
                        ("member", "members_profiles", cuts[i]),
                        ("plant", "plants_profiles", plant_cuts[i]),
                    ):
                        cut_rows = 0
                        for row in frozen_cell["rungs"][i][rows_key]:
                            if (
                                row["matched_length"]
                                < row["plant_length"]
                            ):
                                cut_rows += 1
                                self.assertEqual(
                                    row["matched_total_pairs"], mass
                                )
                        self.assertEqual(cut_rows, expected, block)

    def test_anchor_rung_identity(self) -> None:
        for code in FILES:
            for language in LANGS:
                rung = self.artifact["files"][code][language]["rungs"][0]
                matched = self.frozen_matched["files"][code][language]
                frozen_cell = self.frozen["files"][code][language]
                self.assertEqual(
                    rung["real_rung_profile"],
                    matched["real_profile"],
                )
                self.assertEqual(
                    rung["invariants"], frozen_cell["rungs"][0][
                        "invariants"
                    ],
                )
                self.assertEqual(
                    rung["outside_invariants"],
                    frozen_cell["rungs"][0]["outside_invariants"],
                )
                self.assertEqual(
                    rung["verdict"], frozen_cell["rungs"][0]["verdict"]
                )
                self.assertEqual(
                    rung["outside_invariants"],
                    matched["outside_invariants"],
                )

    def test_scalar_descent_pins(self) -> None:
        for (code, language), table in REAL_PIN.items():
            rungs = self.artifact["files"][code][language]["rungs"]
            for i, rung in enumerate(RUNGS):
                tests = rungs[i]["invariants"]
                for key, row in table[rung].items():
                    self.assertEqual(
                        row[0],
                        rungs[i]["real_rung_profile"][key],
                        (code, language, rung, key),
                    )
                    self.assertEqual(
                        (row[1], row[2]),
                        (
                            tests[key]["band_low"],
                            tests[key]["band_high"],
                        ),
                        (code, language, rung, key),
                    )
        for i, rung in enumerate(RUNGS):
            profile = (
                self.artifact["files"]["ZL"]["english"]["rungs"][i][
                    "real_rung_profile"
                ]
            )
            self.assertEqual(
                profile["self_pair_share"],
                (0.065848, 0.068229, 0.073015, 0.083007)[i],
                rung,
            )
            self.assertEqual(
                profile["pair_entropy"],
                (4.010179, 4.014465, 3.982947, 3.904198)[i],
                rung,
            )

    def test_inside_invariant_rotation(self) -> None:
        for (code, language), flags in GC_INSIDE_SHAPE.items():
            rungs = self.artifact["files"][code][language]["rungs"]
            for i, rung in enumerate(RUNGS):
                tests = rungs[i]["invariants"]
                self.assertEqual(
                    tests["self_pair_share"]["real"],
                    GC_SELF[code, language][i][0],
                    rung,
                )
                self.assertEqual(
                    (
                        tests["self_pair_share"]["band_low"],
                        tests["self_pair_share"]["band_high"],
                    ),
                    GC_SELF[code, language][i][1:],
                    rung,
                )
                self.assertEqual(
                    tests["self_pair_share"]["inside"], flags[i]
                )
                inside = [key for key in OUTSIDE_ALL
                          if tests[key]["inside"]]
                self.assertEqual(
                    inside,
                    ["self_pair_share"] if flags[i] else [],
                    (code, language, rung),
                )
        for (code, language) in GC_SELF:
            self.assertIn((code, language), GC_INSIDE_SHAPE)
        # every other cell misses on all eight at every rung
        for code in FILES:
            for language in LANGS:
                if (code, language) in GC_INSIDE_SHAPE:
                    continue
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    self.assertEqual(
                        rungs[i]["outside_invariants"], OUTSIDE_ALL,
                        (code, language, rung),
                    )
        for code in FILES:
            for language in LANGS:
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    self.assertEqual(
                        rungs[i]["verdict"],
                        "shape-outside-analogues",
                        (code, language, rung),
                    )

    def test_vector_outside_counts(self) -> None:
        for (code, language), table in VECTOR_RUNGS.items():
            rungs = self.artifact["files"][code][language]["rungs"]
            for i, rung in enumerate(RUNGS):
                symbols, pairs = table[rung]
                share_out = rungs[i]["invariants"][
                    "symbol_shares"
                ]["outside"]
                pair_out = rungs[i]["invariants"][
                    "pair_shares"
                ]["outside"]
                self.assertEqual(len(share_out), symbols, rung)
                self.assertEqual(len(pair_out), pairs, rung)
                for entry in share_out:
                    self.assertLess(entry["position"], 36)
                for entry in pair_out:
                    self.assertLess(entry["position"], 1296)

    def test_envelope_rederivation(self) -> None:
        for code in FILES:
            for language in LANGS:
                frozen_cell = self.frozen["files"][code][language]
                rungs = self.artifact["files"][code][language]["rungs"]
                for i, rung in enumerate(RUNGS):
                    band = [
                        {"profile": row["matched_profile"]}
                        for row in
                        frozen_cell["rungs"][i]["members_profiles"]
                    ]
                    fresh = homo._search_free_envelope(
                        rungs[i]["real_rung_profile"], band
                    )
                    self.assertEqual(fresh, rungs[i]["invariants"])
                    outside = [
                        key for key, test in fresh.items()
                        if not test["inside"]
                    ]
                    self.assertEqual(
                        outside, rungs[i]["outside_invariants"]
                    )

    def test_one_rung_recompute(self) -> None:
        fresh = homo._real_rung_facts("ZL", "english", 0.5)
        stored = self.artifact["files"]["ZL"]["english"]["rungs"][2]
        self.assertEqual(sorted(fresh), sorted(stored))
        for key in fresh:
            self.assertEqual(fresh[key], stored[key], key)

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
