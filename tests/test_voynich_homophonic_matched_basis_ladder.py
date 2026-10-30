# The matched-basis ladder suite: the fourteenth measurement's
# declared artifact against its frozen predecessor. Hand constants
# pin the ladder's rung bases and the roster's cuts per rung; the
# artifact pins are read from the frozen run of 27 October 2026
# with the bridge gate verified at 657 fields (the matched
# truncation instrument's 540 anchors plus the 117 anchor-rung
# replay checks) and all 24 rung-cell verdicts
# shape-outside-analogues.
import json
import unittest
from pathlib import Path

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
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
# declared strict-all rule; 20 of the 24 rung-cells miss on all
# eight invariant tests and GC latin's self_pair_share, the family's
# one standing inside invariant, stays inside the band at every
# rung while its cell still misses on the other seven.
OUTSIDE_ALL = [
    "symbol_shares", "pair_shares", "empty_type_count",
    "self_pair_share", "top_1_share", "top_10_share",
    "top_50_share", "pair_entropy",
]

# The six scalar summaries carry closed [min, max] bands; the two
# vector summaries carry per-position envelopes the movements test
# does not price.
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

# (code, language) -> (members cut per rung, plants cut per rung):
# ZL and GC english cut eleven members and keep the Sonnets whole
# until the 25 percent rung cuts it too, the latin cells cut five,
# five, seven and ten, the IT cells degenerate at the anchor and
# cut like every other cell below it, the plants cut five at every
# rung except the IT anchor rung, where nothing can be cut.
CUT_TABLE = {
    ("ZL", "english"): ((11, 11, 11, 12), (5, 5, 5, 5)),
    ("ZL", "latin"): ((5, 5, 7, 10), (5, 5, 5, 5)),
    ("GC", "english"): ((11, 11, 12, 12), (5, 5, 5, 5)),
    ("GC", "latin"): ((5, 6, 7, 10), (5, 5, 5, 5)),
    ("IT", "english"): ((0, 11, 11, 12), (0, 5, 5, 5)),
    ("IT", "latin"): ((0, 5, 7, 10), (0, 5, 5, 5)),
}

# GC latin's self_pair_share, the one invariant inside its band, at
# the four rungs: real 0.015928 against each rung's (low, high).
GC_LATIN_SELF_BANDS = (
    (0.011979, 0.023941),
    (0.012489, 0.023941),
    (0.013329, 0.023837),
    (0.01295, 0.021521),
)

# (code, language) -> the matched plaintext control's pair entropy
# at the four rungs, the ratio of the standing control re-cut to
# each rung; the IT controls identical at their degenerate anchor.
CONTROLS = {
    ("ZL", "english"): (5.13911, 5.13898, 5.138153, 5.139435),
    ("ZL", "latin"): (5.063378, 5.063174, 5.068902, 5.077888),
    ("GC", "english"): (5.139014, 5.138704, 5.135251, 5.144321),
    ("GC", "latin"): (5.063275, 5.061239, 5.07202, 5.078094),
    ("IT", "english"): (5.139068, 5.138764, 5.138225, 5.139379),
    ("IT", "latin"): (5.062979, 5.063274, 5.068993, 5.077053),
}

# (code, language) -> the standing plaintext control's pair
# entropy, unchanged from all four frozen predecessor artifacts.
PLAIN = {
    ("ZL", "english"): 5.139035,
    ("ZL", "latin"): 5.06327,
    ("GC", "english"): 5.139139,
    ("GC", "latin"): 5.063406,
    ("IT", "english"): 5.139068,
    ("IT", "latin"): 5.062979,
}

# code -> the real record's (stream_events, unmapped_events,
# kept_pairs, standing_plant_length, anchor basis = kept + 1).
REAL = {
    "ZL": (218663, 126, 218415, 218663, 218416),
    "GC": (186708, 1769, 183199, 186708, 183200),
    "IT": (220532, 0, 220531, 220532, 220532),
}

# The declared both-ways record, measured: (code, language) ->
# {rung: (ends down, ends up, ends stayed)} of the six scalar
# summaries' two ends against the anchor rung's bands. The bands
# move both ways per the declared design, no rung anywhere flips a
# verdict, and the 25 percent rungs moved all twelve ends.
MOVES = {
    ("ZL", "english"): {0.75: (4, 6, 2), 0.5: (4, 7, 1),
                        0.25: (5, 7, 0)},
    ("ZL", "latin"): {0.75: (2, 5, 5), 0.5: (2, 6, 4),
                      0.25: (4, 8, 0)},
    ("GC", "english"): {0.75: (8, 3, 1), 0.5: (5, 7, 0),
                        0.25: (5, 7, 0)},
    ("GC", "latin"): {0.75: (2, 5, 5), 0.5: (3, 7, 2),
                      0.25: (4, 8, 0)},
    ("IT", "english"): {0.75: (3, 7, 2), 0.5: (4, 7, 1),
                        0.25: (6, 6, 0)},
    ("IT", "latin"): {0.75: (3, 4, 5), 0.5: (2, 7, 3),
                      0.25: (4, 8, 0)},
}
RUNG_SCALARS = {
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
            "empty_type_count": (928, 318, 464),
            "self_pair_share": (0.065848, 0.01884, 0.027095),
            "top_1_share": (0.070481, 0.018173, 0.035196),
            "top_10_share": (0.424435, 0.106088, 0.157183),
            "top_50_share": (0.893671, 0.305696, 0.368859),
            "pair_entropy": (4.010179, 5.92046, 6.115742),
        },
        0.5: {
            "empty_type_count": (928, 341, 495),
            "self_pair_share": (0.065848, 0.01878, 0.027796),
            "top_1_share": (0.070481, 0.015177, 0.034405),
            "top_10_share": (0.424435, 0.100396, 0.157691),
            "top_50_share": (0.893671, 0.305696, 0.370604),
            "pair_entropy": (4.010179, 5.90532, 6.108939),
        },
        0.25: {
            "empty_type_count": (928, 376, 505),
            "self_pair_share": (0.065848, 0.018805, 0.027025),
            "top_1_share": (0.070481, 0.014518, 0.03463),
            "top_10_share": (0.424435, 0.100414, 0.160534),
            "top_50_share": (0.893671, 0.309486, 0.372217),
            "pair_entropy": (4.010179, 5.883769, 6.098317),
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
            "empty_type_count": (928, 283, 503),
            "self_pair_share": (0.065848, 0.012506, 0.023974),
            "top_1_share": (0.070481, 0.01335, 0.02536),
            "top_10_share": (0.424435, 0.097045, 0.134341),
            "top_50_share": (0.893671, 0.268516, 0.339127),
            "pair_entropy": (4.010179, 5.980168, 6.254451),
        },
        0.5: {
            "empty_type_count": (928, 360, 503),
            "self_pair_share": (0.065848, 0.013366, 0.024518),
            "top_1_share": (0.070481, 0.013618, 0.025917),
            "top_10_share": (0.424435, 0.09782, 0.132131),
            "top_50_share": (0.893671, 0.268516, 0.335977),
            "pair_entropy": (4.010179, 5.980168, 6.250767),
        },
        0.25: {
            "empty_type_count": (928, 399, 537),
            "self_pair_share": (0.065848, 0.013527, 0.021909),
            "top_1_share": (0.070481, 0.013764, 0.025031),
            "top_10_share": (0.424435, 0.098316, 0.138755),
            "top_50_share": (0.893671, 0.272333, 0.348076),
            "pair_entropy": (4.010179, 5.951767, 6.248471),
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
            "empty_type_count": (642, 335, 473),
            "self_pair_share": (0.015928, 0.018404, 0.027769),
            "top_1_share": (0.051049, 0.015821, 0.034743),
            "top_10_share": (0.373572, 0.103071, 0.157186),
            "top_50_share": (0.8066, 0.305406, 0.368975),
            "pair_entropy": (4.422831, 5.916585, 6.10912),
        },
        0.5: {
            "empty_type_count": (642, 359, 502),
            "self_pair_share": (0.015928, 0.018849, 0.027852),
            "top_1_share": (0.051049, 0.017005, 0.034804),
            "top_10_share": (0.373572, 0.106112, 0.158851),
            "top_50_share": (0.8066, 0.305386, 0.372036),
            "pair_entropy": (4.422831, 5.899352, 6.109574),
        },
        0.25: {
            "empty_type_count": (642, 399, 520),
            "self_pair_share": (0.015928, 0.018382, 0.025854),
            "top_1_share": (0.051049, 0.01885, 0.033087),
            "top_10_share": (0.373572, 0.109712, 0.164276),
            "top_50_share": (0.8066, 0.307336, 0.377631),
            "pair_entropy": (4.422831, 5.863478, 6.087147),
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
            "empty_type_count": (642, 307, 500),
            "self_pair_share": (0.015928, 0.012489, 0.023941),
            "top_1_share": (0.051049, 0.013366, 0.02536),
            "top_10_share": (0.373572, 0.097737, 0.136046),
            "top_50_share": (0.8066, 0.26876, 0.341342),
            "pair_entropy": (4.422831, 5.98016, 6.253207),
        },
        0.5: {
            "empty_type_count": (642, 376, 500),
            "self_pair_share": (0.015928, 0.013329, 0.023837),
            "top_1_share": (0.051049, 0.013609, 0.025776),
            "top_10_share": (0.373572, 0.098063, 0.134714),
            "top_50_share": (0.8066, 0.26876, 0.338778),
            "pair_entropy": (4.422831, 5.978656, 6.250384),
        },
        0.25: {
            "empty_type_count": (642, 414, 547),
            "self_pair_share": (0.015928, 0.01295, 0.021521),
            "top_1_share": (0.051049, 0.014424, 0.024548),
            "top_10_share": (0.373572, 0.099777, 0.140588),
            "top_50_share": (0.8066, 0.269632, 0.347807),
            "pair_entropy": (4.422831, 5.943103, 6.233837),
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
            "empty_type_count": (984, 318, 462),
            "self_pair_share": (0.065777, 0.018887, 0.027333),
            "top_1_share": (0.071689, 0.018112, 0.035253),
            "top_10_share": (0.429316, 0.106088, 0.157263),
            "top_50_share": (0.89868, 0.30546, 0.369102),
            "pair_entropy": (3.980621, 5.920093, 6.116071),
        },
        0.5: {
            "empty_type_count": (984, 338, 491),
            "self_pair_share": (0.065777, 0.018939, 0.027767),
            "top_1_share": (0.071689, 0.015138, 0.034458),
            "top_10_share": (0.429316, 0.100656, 0.157543),
            "top_50_share": (0.89868, 0.30546, 0.369888),
            "pair_entropy": (3.980621, 5.906326, 6.11015),
        },
        0.25: {
            "empty_type_count": (984, 383, 507),
            "self_pair_share": (0.065777, 0.018882, 0.026675),
            "top_1_share": (0.071689, 0.014318, 0.034724),
            "top_10_share": (0.429316, 0.098647, 0.160437),
            "top_50_share": (0.89868, 0.309421, 0.372346),
            "pair_entropy": (3.980621, 5.885832, 6.098799),
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
            "empty_type_count": (984, 280, 500),
            "self_pair_share": (0.065777, 0.012518, 0.024029),
            "top_1_share": (0.071689, 0.013365, 0.02536),
            "top_10_share": (0.429316, 0.097707, 0.134148),
            "top_50_share": (0.89868, 0.268841, 0.338867),
            "pair_entropy": (3.980621, 5.980406, 6.254241),
        },
        0.5: {
            "empty_type_count": (984, 353, 500),
            "self_pair_share": (0.065777, 0.013268, 0.024498),
            "top_1_share": (0.071689, 0.013587, 0.025896),
            "top_10_share": (0.429316, 0.098177, 0.131964),
            "top_50_share": (0.89868, 0.268841, 0.336261),
            "pair_entropy": (3.980621, 5.980406, 6.250893),
        },
        0.25: {
            "empty_type_count": (984, 404, 535),
            "self_pair_share": (0.065777, 0.013499, 0.022046),
            "top_1_share": (0.071689, 0.013812, 0.025113),
            "top_10_share": (0.429316, 0.098242, 0.138286),
            "top_50_share": (0.89868, 0.27285, 0.34743),
            "pair_entropy": (3.980621, 5.951559, 6.248481),
        },
    },
}
VECTOR_RUNGS = {
    ("ZL", "english"): {
        1.0: (35, 834),
        0.75: (36, 824),
        0.5: (36, 792),
        0.25: (36, 783),
    },
    ("ZL", "latin"): {
        1.0: (36, 780),
        0.75: (35, 779),
        0.5: (35, 778),
        0.25: (35, 744),
    },
    ("GC", "english"): {
        1.0: (36, 829),
        0.75: (36, 810),
        0.5: (36, 780),
        0.25: (36, 764),
    },
    ("GC", "latin"): {
        1.0: (33, 781),
        0.75: (32, 781),
        0.5: (33, 781),
        0.25: (34, 733),
    },
    ("IT", "english"): {
        1.0: (35, 839),
        0.75: (35, 824),
        0.5: (35, 798),
        0.25: (35, 782),
    },
    ("IT", "latin"): {
        1.0: (35, 785),
        0.75: (34, 785),
        0.5: (34, 785),
        0.25: (34, 749),
    },
}


class MatchedBasisLadderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen = json.loads(FROZEN_MATCHED.read_text())
        self.declared = self.artifact["declared"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.LADDER_RUNGS, (1.0, 0.75, 0.5, 0.25))
        self.assertEqual(
            homo.LADDER_RUNG_FACT_KEYS,
            (
                "match_basis_events", "matched_members_cut",
                "matched_plants_cut", "members_profiles",
                "plants_profiles", "plaintext_matched_profile",
                "invariants", "outside_invariants", "verdict",
            ),
        )
        self.assertTrue(
            str(homo.SEARCH_FREE_LADDER_ARTIFACT_PATH).endswith(
                "voynich-homophonic-matched-basis-ladder.json"
            )
        )
        self.assertEqual(self.declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(self.declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(
            sorted(self.declared),
            [
                "base_seed", "boundary_rule", "bridge_gate",
                "closure_rule", "exclusion_rule", "floors_rule",
                "invariants", "ladder_rung_rule", "machinery_rule",
                "mapped", "models_rule", "plaintext_rule",
                "plants_rule", "roster_rule", "rung_record_rule",
                "seed_kinds", "seed_sharing", "split_rule",
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
                "fields_compared": 657,
                "anchor_fields": 399,
                "breadth_replay_checks": 141,
                "ladder_replay_checks": 117,
            },
        )

    def test_the_ladder_declaration(self) -> None:
        rule = self.declared["ladder_rung_rule"]
        self.assertIn(
            "the cell's real counted pair total + 1 tokens "
            "(ZL 218,416, GC 183,200, IT 220,532)",
            rule,
        )
        self.assertIn(
            "descend at floor(p x the anchor basis) tokens for p "
            "0.75, 0.50 and 0.25 (ZL 163,812, 109,208 and 54,604; "
            "GC 137,400, 91,600 and 45,800; IT 165,399, 110,266 "
            "and 55,133)",
            rule,
        )
        self.assertIn(
            "a cut can move a band's closed ranges both ways, both "
            "verdict directions are open at every rung",
            rule,
        )
        self.assertIn(
            "the real is priced once, unchanged across rungs", rule,
        )
        roster = self.declared["roster_rule"]
        self.assertIn(
            "the corpus-breadth roster stands unchanged", roster,
        )
        self.assertIn(
            "no corpus file is re-fetched, re-probed or re-hashed "
            "here",
            roster,
        )
        state = self.declared["state_note"]
        self.assertIn(
            "the IT cells are degenerate only at the anchor rung",
            state,
        )
        self.assertIn(
            "the real is priced once at its own kept-adjacent mass "
            "and is not re-cut anywhere",
            state,
        )
        self.assertIn(
            "contains no assignment search anywhere",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "no machinery recording appears",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "no split applies", self.declared["split_rule"],
        )
        self.assertIn(
            "no new seed is consumed and no draw selection is "
            "performed",
            self.declared["seed_kinds"],
        )
        self.assertIn(
            "verify against the frozen matched-truncation artifact "
            "field for field under the gate",
            self.declared["seed_sharing"],
        )
        record = self.declared["rung_record_rule"]
        self.assertIn(
            "four rungs in declared order (the anchor rung first, "
            "then 75, 50 and 25 percent)",
            record,
        )
        plants = self.declared["plants_rule"]
        self.assertIn(
            "the plant encodings recorded at every rung like the "
            "band",
            plants,
        )
        floors = self.declared["floors_rule"]
        self.assertIn(
            "recorded once at the cell, unchanged across the rungs",
            floors,
        )
        plaintext = self.declared["plaintext_rule"]
        self.assertIn(
            "each rung's matched control re-cut to that rung beside "
            "it",
            plaintext,
        )
        verdict = self.declared["verdict_rule"]
        self.assertIn(
            "priced per rung", verdict,
        )
        self.assertIn(
            "over all 24 rung-cell verdicts together", verdict,
        )
        self.assertIn(
            "no scalar margin is formed",
            self.declared["closure_rule"],
        )
        self.assertIn(
            "the band instruments' verdicts stand untouched by this "
            "artifact's numbers",
            self.declared["exclusion_rule"],
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
        gate = self.declared["bridge_gate"]
        self.assertIn(
            "the matched-truncation instrument's gate exactly as "
            "that instrument declared it (the corpus-breadth "
            "instrument's 399 anchor fields and the 141 "
            "standing-row replay checks, 540 fields)",
            gate,
        )
        self.assertIn(
            "20 checks per english cell and 19 per latin cell, 117 "
            "checks total, 657 fields compared",
            gate,
        )

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "Fourteenth declared measurement, the matched-basis "
            "ladder",
            "declared after the matched-truncation instrument cut "
            "every simulated stream to the real's own counted pair "
            "mass and no cell reported the inside verdict that "
            "matching granted",
            "the anchors 218,416 (ZL), 183,200 (GC) and 220,532 "
            "(IT)",
            "make the rung bases ZL 218,416, 163,812, 109,208 and "
            "54,604; GC 183,200, 137,400, 91,600 and 45,800; IT "
            "220,532, 165,399, 110,266 and 55,133",
            "the gate ran at 657 fields compared, no problem",
            "ZL english: every rung's verdict shape-outside-analogues "
            "with every one of the eight invariant tests outside",
            "Probe 4, the first latin cell's declared portraits "
            "ahead of the run, ZL latin: every rung's verdict "
            "shape-outside-analogues",
            "Probe 5, the matched plaintext controls recorded ahead "
            "at the four rungs against their standing profiles",
            "Probe 6: none; the four remaining cells are unseen "
            "until the declared run",
            "the artifact run prices all 24 rung-cells through the "
            "same declared code",
            "the IT cells are degenerate only at the anchor rung",
            "the real is priced once and never re-cut",
            "the floors replay unchanged (a floor's shuffled "
            "kept-adjacency already prices exactly the real's "
            "counted pair total)",
            "nothing here is a reading or a language claim",
        ):
            self.assertIn(phrase, doc)
        self.assertEqual(
            " ".join(doc.split()).count(
                "nothing here is a reading or a language claim"
            ),
             17,
        )

    def test_the_truthful_question(self) -> None:
        what = self.artifact["what"]
        self.assertIn(
            "re-priced with the truncation basis swept at declared "
            "rungs: the real's own mass anchor rung first",
            what,
        )
        self.assertIn(
            "the same twelve english and eleven latin member roster",
            what,
        )
        self.assertIn(
            "does any rung's matched band admit the real's "
            "mark-excluded profile inside on every declared "
            "invariant in every (file, language) cell, or do every "
            "rung's verdicts stand",
            what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading",
            what,
        )

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_ladder_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 657)
        self.assertEqual(
            self.artifact["bridge_gate"]["fields_compared"], fields
        )
        self.assertEqual(
            self.artifact["bridge_gate"]["status"], "verified"
        )

    def test_rung_bases_and_the_real_record(self) -> None:
        for code, row in REAL.items():
            events, unmapped, kept, standing, anchor = row
            real = homo._homo_real_stream(code)
            self.assertEqual(real["total_events"], events)
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen["files"][code][language]
                rungs = cell["rungs"]
                self.assertEqual(len(rungs), len(RUNGS))
                for i, rung in enumerate(RUNGS):
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
                # the real record priced once, verified against the
                # frozen matched-truncation cell, and the
                # rung-independent facts recorded once
                self.assertEqual(cell["stream_events"], events)
                self.assertEqual(cell["unmapped_events"], unmapped)
                self.assertEqual(cell["kept_pairs"], kept)
                self.assertEqual(
                    cell["real_profile"], frozen["real_profile"]
                )
                self.assertEqual(
                    cell["standing_plant_length"], standing
                )
                self.assertEqual(
                    cell["floors_profiles"], frozen["floors_profiles"]
                )
                self.assertEqual(
                    cell["plaintext_profile"],
                    frozen["plaintext_profile"],
                )
                self.assertEqual(
                    cell["rungs"][0]["match_basis_events"], anchor
                )
                for key in homo.LADDER_RUNG_FACT_KEYS:
                    self.assertIn(key, rungs[0], key)

    def test_anchor_rung_equals_the_frozen_matched_artifact(
        self,
    ) -> None:
        for code in FILES:
            for language in LANGS:
                rung = self.artifact["files"][code][language][
                    "rungs"
                ][0]
                stored = self.frozen["files"][code][language]
                for key in homo.LADDER_RUNG_FACT_KEYS:
                    self.assertEqual(rung[key], stored[key], key)

    def test_scalar_band_ranges(self) -> None:
        for (code, language), table in RUNG_SCALARS.items():
            rungs = self.artifact["files"][code][language]["rungs"]
            inside_key = None
            if (code, language) == ("GC", "latin"):
                inside_key = "self_pair_share"
            for i, rung in enumerate(RUNGS):
                invariants = rungs[i]["invariants"]
                for key, (real, low, high) in table[rung].items():
                    test = invariants[key]
                    self.assertEqual(test["real"], real, key)
                    self.assertEqual(test["band_low"], low, key)
                    self.assertEqual(test["band_high"], high, key)
                    self.assertEqual(
                        test["inside"], key == inside_key, key
                    )
        for i, rung in enumerate(RUNGS):
            self.assertEqual(
                self.artifact["files"]["GC"]["latin"]["rungs"][i][
                    "invariants"
                ]["self_pair_share"]["band_low"],
                GC_LATIN_SELF_BANDS[i][0],
            )
            self.assertEqual(
                self.artifact["files"]["GC"]["latin"]["rungs"][i][
                    "invariants"
                ]["self_pair_share"]["band_high"],
                GC_LATIN_SELF_BANDS[i][1],
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

    def test_members_cut_per_rung(self) -> None:
        for code in FILES:
            for language in LANGS:
                cuts, plant_cuts = CUT_TABLE[(code, language)]
                rungs = self.artifact["files"][code][
                    language
                ]["rungs"]
                rows_n = 12 if language == "english" else 11
                for i, rung in enumerate(RUNGS):
                    basis = RUNG_BASES[code][i]
                    rg = rungs[i]
                    self.assertEqual(
                        rg["matched_members_cut"], cuts[i]
                    )
                    self.assertEqual(
                        rg["matched_plants_cut"], plant_cuts[i]
                    )
                    self.assertEqual(len(rg["members_profiles"]),
                                     rows_n)
                    cut_rows = 0
                    for row in rg["members_profiles"]:
                        self.assertEqual(
                            row["matched_length"],
                            min(row["plant_length"], basis),
                        )
                        self.assertEqual(
                            row["matched_total_pairs"],
                            row["matched_length"] - 1,
                        )
                        if row["matched_length"] < row["plant_length"]:
                            cut_rows += 1
                            self.assertEqual(
                                row["matched_total_pairs"],
                                basis - 1,
                            )
                    self.assertEqual(cut_rows, cuts[i])
                    plant_rows = 0
                    for row in rg["plants_profiles"]:
                        self.assertEqual(
                            row["matched_length"],
                            min(row["plant_length"], basis),
                        )
                        if row["matched_length"] < row["plant_length"]:
                            plant_rows += 1
                            self.assertEqual(
                                row["matched_total_pairs"],
                                basis - 1,
                            )
                    self.assertEqual(plant_rows, plant_cuts[i])

    def test_it_degenerate_only_at_the_anchor(self) -> None:
        for language in LANGS:
            rungs = self.artifact["files"]["IT"][language]["rungs"]
            frozen = self.frozen["files"]["IT"][language]
            self.assertEqual(rungs[0]["matched_members_cut"], 0)
            self.assertEqual(rungs[0]["matched_plants_cut"], 0)
            self.assertEqual(
                rungs[0]["invariants"], frozen["invariants"]
            )
            self.assertEqual(
                rungs[0]["plaintext_matched_profile"],
                frozen["plaintext_matched_profile"],
            )
            self.assertEqual(rungs[0]["verdict"], frozen["verdict"])
            self.assertEqual(rungs[0]["match_basis_events"], 220532)
            # the descended rungs cut like every other cell's
            cuts = CUT_TABLE[("IT", language)][0]
            for i, rung in enumerate(RUNGS[1:], start=1):
                self.assertEqual(
                    rungs[i]["matched_members_cut"], cuts[i]
                )
                self.assertEqual(
                    rungs[i]["matched_plants_cut"], 5
                )
                self.assertGreater(
                    rungs[i]["matched_members_cut"], 0
                )

    def test_movements_against_the_anchor_rung(self) -> None:
        # The declared both-ways record priced from the stored
        # bands: the cut can move a descended rung's closed range
        # down or up against the anchor rung's bands, the ladder
        # records every movement's count per rung, and no movement
        # anywhere flips a verdict - every rung-cell stays a
        # shape-outside-analogue.
        for code in FILES:
            for language in LANGS:
                rungs = self.artifact["files"][code][
                    language
                ]["rungs"]
                self.assertEqual(
                    rungs[0]["verdict"],
                    "shape-outside-analogues",
                )
                for i, rung in enumerate(RUNGS[1:], start=1):
                    self.assertEqual(
                        rungs[i]["verdict"],
                        "shape-outside-analogues",
                    )
                    down = up = stayed = 0
                    for key in SCALAR_KEYS:
                        for end in ("band_low", "band_high"):
                            a = rungs[0]["invariants"][key][end]
                            b = rungs[i]["invariants"][key][end]
                            if b == a:
                                stayed += 1
                            elif b < a:
                                down += 1
                            else:
                                up += 1
                    expected = MOVES[(code, language)][rung]
                    self.assertEqual(
                        (down, up, stayed), expected,
                        (code, language, rung),
                    )
                    self.assertGreater(down, 0)
                    self.assertGreater(up, 0)

    def test_plaintext_controls_per_rung(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen["files"][code][language]
                self.assertEqual(
                    cell["plaintext_profile"]["state_types"], 729
                )
                self.assertEqual(
                    cell["plaintext_profile"]["pair_entropy"],
                    PLAIN[(code, language)],
                )
                self.assertEqual(
                    cell["plaintext_profile"],
                    frozen["plaintext_profile"],
                )
                for i, rung in enumerate(RUNGS):
                    matched = cell["rungs"][i][
                        "plaintext_matched_profile"
                    ]
                    self.assertEqual(
                        matched["pair_entropy"],
                        CONTROLS[(code, language)][i],
                        rung,
                    )
                if code == "IT":
                    # the degenerate anchor rung's matched control
                    self.assertEqual(
                        cell["rungs"][0][
                            "plaintext_matched_profile"
                        ],
                        cell["plaintext_profile"],
                    )

    def test_encodings_above_their_rung_controls(self) -> None:
        # Every rung's matched encoding sits above its own matched
        # plaintext control's entropy, while the real's unchanged
        # full-mass block entropy sits below every matched member
        # at every rung - the standing geometry carried down the
        # ladder.
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                for i, rung in enumerate(RUNGS):
                    rg = cell["rungs"][i]
                    control = rg[
                        "plaintext_matched_profile"
                    ]["pair_entropy"]
                    for member in rg["members_profiles"]:
                        self.assertGreater(
                            member["matched_profile"]["pair_entropy"],
                            control,
                        )
                    for plant in rg["plants_profiles"]:
                        self.assertGreater(
                            plant["matched_profile"]["pair_entropy"],
                            control,
                        )
                    self.assertLess(
                        cell["real_profile"]["pair_entropy"],
                        min(
                            member["matched_profile"]["pair_entropy"]
                            for member in rg["members_profiles"]
                        ),
                    )

    def test_one_rung_recompute(self) -> None:
        fresh = homo._ladder_rung_facts("ZL", "english", 0.5)
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
            self.assertNotIn("\u2013", source)
            self.assertNotIn("\u2014", source)


if __name__ == "__main__":
    unittest.main()
