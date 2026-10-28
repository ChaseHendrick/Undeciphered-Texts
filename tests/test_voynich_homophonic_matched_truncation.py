# The matched-truncation interior-shape suite: the thirteenth
# measurement's declared artifact against its frozen predecessor.
# Hand tests pin the matched band arithmetic both ways (a cut can
# move a closed range down or up, and both verdict directions are
# open), and the artifact pins are read from the frozen run of 26
# October 2026 with the bridge gate verified at 540 fields (the
# corpus-breadth instrument's 399 anchors and the 141 standing-row
# replay checks).
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-matched-truncation.json"
).resolve()
FROZEN_BREADTH = Path(
    "docs/research-notes/voynich-homophonic-corpus-breadth.json"
).resolve()

# The frozen artifact's headline, pinned from the artifact measured
# 26 October 2026 with the bridge gate verified at 540 fields: every
# cell is a shape-outside-analogue under the declared strict-all rule
# with the band's streams matched to the real's own counted pair
# mass, and the outside-invariant set is the corpus-breadth
# instrument's exactly, GC latin's self_pair_share again the one
# invariant inside, now deeper inside its matched band.
OUTSIDE_ALL = [
    "symbol_shares", "pair_shares", "empty_type_count",
    "self_pair_share", "top_1_share", "top_10_share",
    "top_50_share", "pair_entropy",
]
OUTSIDE = {
    ("GC", "latin"): [
        key for key in OUTSIDE_ALL if key != "self_pair_share"
    ],
}

# (code, language) -> (symbol positions outside, pair positions
# outside), identical to the corpus-breadth artifact's counts in
# every cell.
VECTOR_COUNTS = {
    ("ZL", "english"): (35, 834),
    ("ZL", "latin"): (36, 780),
    ("GC", "english"): (36, 829),
    ("GC", "latin"): (33, 781),
    ("IT", "english"): (35, 839),
    ("IT", "latin"): (35, 785),
}

# (code, language) -> the six scalar summaries' (real, band_low,
# band_high), the matched bands of the run.
SCALARS = {
    ("ZL", "english"): {
        "empty_type_count": (928, 323, 454),
        "self_pair_share": (0.065848, 0.018692, 0.026719),
        "top_1_share": (0.070481, 0.018187, 0.035877),
        "top_10_share": (0.424435, 0.106088, 0.148334),
        "top_50_share": (0.893671, 0.305696, 0.355757),
        "pair_entropy": (4.010179, 5.928491, 6.102985),
    },
    ("ZL", "latin"): {
        "empty_type_count": (928, 240, 503),
        "self_pair_share": (0.065848, 0.011829, 0.023974),
        "top_1_share": (0.070481, 0.013486, 0.02536),
        "top_10_share": (0.424435, 0.09782, 0.132009),
        "top_50_share": (0.893671, 0.268516, 0.336674),
        "pair_entropy": (4.010179, 5.980168, 6.252),
    },
    ("GC", "english"): {
        "empty_type_count": (642, 318, 453),
        "self_pair_share": (0.015928, 0.018513, 0.027183),
        "top_1_share": (0.051049, 0.018386, 0.035403),
        "top_10_share": (0.373572, 0.106088, 0.15809),
        "top_50_share": (0.8066, 0.305406, 0.370289),
        "pair_entropy": (4.422831, 5.919417, 6.116692),
    },
    ("GC", "latin"): {
        "empty_type_count": (642, 262, 500),
        "self_pair_share": (0.015928, 0.011979, 0.023941),
        "top_1_share": (0.051049, 0.013384, 0.02536),
        "top_10_share": (0.373572, 0.097128, 0.133145),
        "top_50_share": (0.8066, 0.26876, 0.338741),
        "pair_entropy": (4.422831, 5.98016, 6.254936),
    },
    ("IT", "english"): {
        "empty_type_count": (984, 325, 449),
        "self_pair_share": (0.065777, 0.018701, 0.027087),
        "top_1_share": (0.071689, 0.018068, 0.035914),
        "top_10_share": (0.429316, 0.106088, 0.148471),
        "top_50_share": (0.89868, 0.30546, 0.35595),
        "pair_entropy": (3.980621, 5.927877, 6.102609),
    },
    ("IT", "latin"): {
        "empty_type_count": (984, 241, 500),
        "self_pair_share": (0.065777, 0.013217, 0.024029),
        "top_1_share": (0.071689, 0.013525, 0.02536),
        "top_10_share": (0.429316, 0.098044, 0.131821),
        "top_50_share": (0.89868, 0.268841, 0.336358),
        "pair_entropy": (3.980621, 5.980406, 6.252202),
    },
}

# (code, language) -> the first sorted symbol-position outside
# entry's (real, band_low, band_high); the pair entries' heads equal
# the top_1_share scalars per cell.
HEADS = {
    ("ZL", "english"): (0.155542, 0.076092, 0.093032),
    ("ZL", "latin"): (0.155542, 0.067495, 0.099429),
    ("GC", "english"): (0.19975, 0.076425, 0.09309),
    ("GC", "latin"): (0.19975, 0.067495, 0.099429),
    ("IT", "english"): (0.158109, 0.07601, 0.093121),
    ("IT", "latin"): (0.158109, 0.067495, 0.099429),
}

# code -> the real record's (stream_events, unmapped_events,
# kept_pairs, standing_plant_length, match_basis_events), the basis
# kept + 1 tokens everywhere.
REAL = {
    "ZL": (218663, 126, 218415, 218663, 218416),
    "GC": (186708, 1769, 183199, 186708, 183200),
    "IT": (220532, 0, 220531, 220532, 220532),
}

# (code, language) -> the matched roster's (members cut, members
# whole): eleven cut and the Sonnets whole in every english cell of
# ZL and GC, five cut and six whole in every latin cell, and the IT
# cells degenerate with nothing cut anywhere.
CUT_WHOLE = {
    ("ZL", "english"): (11, 1),
    ("ZL", "latin"): (5, 6),
    ("GC", "english"): (11, 1),
    ("GC", "latin"): (5, 6),
    ("IT", "english"): (0, 12),
    ("IT", "latin"): (0, 11),
}

# The member row's declared key layout: standing-basis anchors first,
# matched facts beside them.
MEMBER_KEYS = [
    "draw_rule", "ebook", "file", "full_width_total_pairs",
    "matched_length", "matched_profile", "matched_total_pairs",
    "plant_length", "selected_draw_index",
]

# (code, language) -> the matched member profiles' block-total and
# entropy ranges.
MEMBER_BLOCKS = {
    ("ZL", "english"): (55143, 144349, 5.928491, 6.102985),
    ("ZL", "latin"): (31635, 158458, 5.980168, 6.252),
    ("GC", "english"): (55143, 120869, 5.919417, 6.116692),
    ("GC", "latin"): (31635, 132619, 5.98016, 6.254936),
    ("IT", "english"): (55143, 145751, 5.927877, 6.102609),
    ("IT", "latin"): (31635, 159999, 5.980406, 6.252202),
}

# The plant row's declared key layout.
PLANT_KEYS = [
    "full_width_total_pairs", "index", "matched_length",
    "matched_profile", "matched_total_pairs", "plant_length",
]

# (code, language) -> the matched plant block total, one number per
# cell (all five plants share the matched length and price one
# block).
PLANT_BLOCKS = {
    ("ZL", "english"): 137339,
    ("ZL", "latin"): 150839,
    ("GC", "english"): 115215,
    ("GC", "latin"): 126301,
    ("IT", "english"): 138635,
    ("IT", "latin"): 152294,
}

# (code, language) -> the plaintext control's standing pair
# entropy, unchanged from all three frozen predecessor artifacts.
PLAIN = {
    ("ZL", "english"): 5.139035,
    ("ZL", "latin"): 5.06327,
    ("GC", "english"): 5.139139,
    ("GC", "latin"): 5.063406,
    ("IT", "english"): 5.139068,
    ("IT", "latin"): 5.062979,
}

# (code, language) -> the matched control's pair entropy, the ratio
# of the same standing profile re-cut to the basis; the IT controls
# identical by the degenerate case.
MATCHED_PLAIN = {
    ("ZL", "english"): 5.13911,
    ("ZL", "latin"): 5.063378,
    ("GC", "english"): 5.139014,
    ("GC", "latin"): 5.063275,
    ("IT", "english"): 5.139068,
    ("IT", "latin"): 5.062979,
}

# The recorded both-ways movements against the frozen bands: (
# code, language, scalar, end, matched value, direction), the cut
# can move a closed range down or up and the artifact records both.
MOVEMENTS = [
    ("ZL", "latin", "pair_entropy", "high", 6.252, "below"),
    ("ZL", "english", "top_50_share", "high", 0.355757, "above"),
    ("ZL", "english", "self_pair_share", "low", 0.018692, "below"),
    ("ZL", "english", "top_1_share", "low", 0.018187, "below"),
    ("GC", "latin", "self_pair_share", "low", 0.011979, "below"),
    ("GC", "english", "empty_type_count", "low", 318, "above"),
]


class MatchedTruncationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_breadth = json.loads(FROZEN_BREADTH.read_text())
        self.declared = self.artifact["declared"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.SEARCH_FREE_TOP_K, (1, 10, 50))
        self.assertEqual(homo.SEARCH_FREE_SHARES, 6)
        self.assertTrue(
            str(homo.SEARCH_FREE_MATCHED_ARTIFACT_PATH).endswith(
                "voynich-homophonic-matched-truncation.json"
            )
        )
        self.assertEqual(
            homo.MATCHED_REAL_RECORD_KEYS,
            (
                "stream_events", "kept_pairs", "unmapped_events",
                "boundary_carried_pairs", "real_profile",
                "real_full_width_total_pairs", "standing_plant_length",
                "plants_at_source_identity",
            ),
        )
        self.assertEqual(self.declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(self.declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(
            sorted(self.declared),
            [
                "base_seed", "boundary_rule", "bridge_gate",
                "closure_rule", "exclusion_rule", "floors_rule",
                "invariants", "machinery_rule", "mapped",
                "matched_band_record_rule", "matched_truncation_rule",
                "models_rule", "plaintext_rule", "plants_rule",
                "roster_rule", "seed_kinds", "seed_sharing",
                "split_rule", "state_note", "verdict_rule",
            ],
        )
        self.assertEqual(
            sorted(self.declared["invariants"]),
            [
                "empty_type_count",
                "pair_entropy",
                "self_pair_share",
                "sorted_pair_multiset",
                "sorted_symbol_marginals",
                "top_k_shares",
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
                "fields_compared": 540,
                "anchor_fields": 399,
                "breadth_replay_checks": 141,
            },
        )

    def test_the_matched_truncation_declaration(self) -> None:
        rule = self.declared["matched_truncation_rule"]
        self.assertIn(
            "its counted pair total is ZL 218,415, GC 183,199 and "
            "IT 220,531 pairs",
            rule,
        )
        self.assertIn(
            "the basis is that total + 1 tokens "
            "(ZL 218,416, GC 183,200, IT 220,532)",
            rule,
        )
        self.assertIn(
            "a cut stream's full width equals the real's counted "
            "pair total exactly (ZL 218,415, GC 183,199, IT 220,531)",
            rule,
        )
        self.assertIn(
            "the same mass the floors already price by construction",
            rule,
        )
        self.assertIn(
            "while a stream at or below the basis stays whole", rule,
        )
        self.assertIn(
            "ZL 247 of the standing 218,662 full-width pairs "
            "(0.11296 percent), GC 3,508 of 186,707 "
            "(1.87888 percent), IT 0",
            rule,
        )
        self.assertIn(
            "no new corpus files, no roster change, no new seed kind "
            "and no new selection anywhere",
            rule,
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
            "the IT cells carry the declared degenerate case exactly",
            state,
        )
        self.assertIn(
            "the matched member streams run 45,490 pairs upward",
            state,
        )
        self.assertIn(
            "the IT matched verdict is the corpus-breadth verdict "
            "replayed",
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
            "verify against the frozen corpus-breadth artifact field "
            "for field under the gate",
            self.declared["seed_sharing"],
        )
        self.assertIn(
            "the matched facts run the same seeds over the matched "
            "streams from draw 0 upward",
            self.declared["seed_sharing"],
        )
        band_rule = self.declared["matched_band_record_rule"]
        self.assertIn(
            "the matched total an exact identity, matched length - 1",
            band_rule,
        )
        self.assertIn(
            "the corpus-breadth roster's twelve english and eleven "
            "latin members, unconditional",
            band_rule,
        )
        plants = self.declared["plants_rule"]
        self.assertIn(
            "recorded at the matched basis like the band", plants,
        )
        self.assertIn(
            "each matched row carries the same identity at its "
            "matched length",
            plants,
        )
        floors = self.declared["floors_rule"]
        self.assertIn(
            "the floors already sit at the matched scale everywhere "
            "and nothing here re-cuts them",
            floors,
        )
        plaintext = self.declared["plaintext_rule"]
        self.assertIn("plaintext_matched_profile", plaintext)
        self.assertIn(
            "neither control takes part in any envelope", plaintext,
        )
        verdict = self.declared["verdict_rule"]
        self.assertIn(
            "inside the closed range of that cell's matched band's "
            "glyph-block profiles",
            verdict,
        )
        self.assertIn(
            "the miss is audited not summarized", verdict,
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
            "the standing add-one and leave-one-out tables play no "
            "part anywhere in this artifact",
            self.declared["models_rule"],
        )
        boundary = self.declared["boundary_rule"]
        self.assertIn(
            "the standing alphabet-width disclosure carries unchanged",
            boundary,
        )
        self.assertIn(
            "the IT real transcription ranks only 23 glyph types "
            "plus the mark, so 13 of its block's 36 glyph slots are "
            "empty by width alone on the real side",
            boundary,
        )
        gate = self.declared["bridge_gate"]
        self.assertIn(
            "the corpus-breadth instrument's 399 anchor fields", gate,
        )
        self.assertIn("141 row checks total", gate)

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "Thirteenth declared measurement, the matched-truncation",
            "cut every simulated encoding to the real's own counted "
            "pair mass and re-price the same declared question "
            "unchanged",
            "this cut can move a band's closed ranges both ways - a "
            "cut tail removes pair mass the standing profile priced",
            "both verdict directions are open in this design",
            "the cell's real counted pair total + 1 tokens "
            "(ZL 218,416, GC 183,200, IT 220,532)",
            "the same mass the floors already price by construction",
            "Probe 1, the bridge gate rehearsed: the gate ran at "
            "540 fields compared, no problem",
            "0.11296 percent",
            "1.87888 percent",
            "Probe 3, the first cell's declared verdict ahead of the "
            "run, ZL english: shape-outside-analogues with every one "
            "of the eight invariant tests outside",
            "Probe 4, the first latin cell's declared verdict ahead "
            "of the run, ZL latin",
            "the latin entropy ceiling eased down from the standing "
            "6.252046 to 6.252",
            "its top-50 ceiling up (0.355739 to 0.355757)",
            "Probe 5, the plaintext controls recorded ahead",
            "Probe 6: none",
            "the artifact run prices all six cells through the same "
            "declared code",
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
            "re-priced with every simulated stream cut to the real's "
            "own counted pair mass",
            what,
        )
        self.assertIn(
            "the same twelve english and eleven latin member roster",
            what,
        )
        self.assertIn(
            "with the band's streams matched to the real's own pair "
            "mass under the declared cut, does the real's "
            "mark-excluded profile sit inside the matched band's "
            "range on every declared invariant in every (file, "
            "language) cell, or is at least one invariant outside",
            what,
        )
        self.assertIn(
            "the measured test of whether the interior's separation "
            "is a length artifact of the real's own counted mass or "
            "holds as the masses match",
            what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading",
            what,
        )

    def test_glyph_block_matrix_arithmetic(self) -> None:
        matrix = np.array(
            [[1, 2, 3, 0, 1],
             [4, 5, 6, 0, 1],
             [7, 8, 9, 0, 1],
             [0, 0, 0, 2, 0],
             [1, 1, 1, 0, 1]],
            dtype=np.int64,
        )
        block = homo._glyph_block_matrix(matrix, 2)
        self.assertEqual(block.shape, (4, 4))
        self.assertEqual(int(block.sum()), 19)
        self.assertEqual(int(matrix.sum()), 54)
        self.assertEqual(
            homo._boundary_carried_pairs(matrix, 2), 35
        )
        block_last = homo._glyph_block_matrix(matrix, 4)
        self.assertEqual(
            homo._boundary_carried_pairs(matrix, 4), 7
        )

    def test_glyph_block_relabeling_invariance(self) -> None:
        matrix = np.array(
            [[1, 2, 3, 0, 1],
             [4, 5, 6, 0, 1],
             [7, 8, 9, 0, 1],
             [0, 0, 0, 2, 0],
             [1, 1, 1, 0, 1]],
            dtype=np.int64,
        )
        block = homo._glyph_block_matrix(matrix, 2)
        permutation = [2, 0, 3, 1]
        relabeled = block[np.ix_(permutation, permutation)]
        self.assertEqual(
            homo._profile_facts(block),
            homo._profile_facts(relabeled),
        )

    def test_envelope_arithmetic(self) -> None:
        member_a = homo._profile_facts(
            np.array([[4, 1, 0], [1, 2, 0], [0, 0, 1]],
                     dtype=np.int64)
        )
        member_b = homo._profile_facts(
            np.array([[2, 0, 0], [0, 4, 1], [0, 1, 0]],
                     dtype=np.int64)
        )
        member_facts = [
            {"profile": member_a}, {"profile": member_b},
        ]
        real = homo._profile_facts(
            np.array([[2, 1, 1], [1, 3, 0], [1, 0, 0]],
                     dtype=np.int64)
        )
        record = homo._search_free_envelope(real, member_facts)
        scalar = record["self_pair_share"]
        self.assertFalse(scalar["inside"])
        self.assertEqual(
            (scalar["real"], scalar["band_low"], scalar["band_high"]),
            (0.555556, 0.75, 0.777778),
        )

    def test_matched_band_arithmetic_on_hand_profiles(self) -> None:
        # The declared matched-truncation arithmetic, pinned by
        # hand: cutting a member's stream removes the pair mass its
        # standing profile priced, so a matched band's closed
        # ranges can move down or up - a flatter cut widens an end
        # downward, a concentrated cut can lift an end upward - and
        # both verdict directions are open: an invariant the
        # standing band excluded can be pulled inside its matched
        # range, and an invariant the standing band contained can
        # be left outside, here on hand profiles against the
        # unchanged real.
        real = homo._profile_facts(
            np.array([[2, 1, 1], [1, 3, 0], [1, 0, 0]],
                     dtype=np.int64)
        )
        member_a = homo._profile_facts(
            np.array([[4, 1, 0], [1, 2, 0], [0, 0, 1]],
                     dtype=np.int64)
        )
        member_b = homo._profile_facts(
            np.array([[2, 0, 0], [0, 4, 1], [0, 1, 0]],
                     dtype=np.int64)
        )
        cut_a = homo._profile_facts(
            np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]],
                     dtype=np.int64)
        )
        cut_b = homo._profile_facts(
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                     dtype=np.int64)
        )
        standing = homo._search_free_envelope(
            real, [{"profile": member_a}, {"profile": member_b}]
        )
        self.assertEqual(
            (standing["self_pair_share"]["real"],
             standing["self_pair_share"]["band_low"],
             standing["self_pair_share"]["band_high"]),
            (0.555556, 0.75, 0.777778),
        )
        self.assertFalse(standing["self_pair_share"]["inside"])
        matched = homo._search_free_envelope(
            real, [{"profile": cut_a}, {"profile": cut_b}]
        )
        self.assertEqual(
            (matched["self_pair_share"]["real"],
             matched["self_pair_share"]["band_low"],
             matched["self_pair_share"]["band_high"]),
            (0.555556, 0.0, 1.0),
        )
        self.assertTrue(matched["self_pair_share"]["inside"])
        # The second direction: a standing band that contains the
        # real can reprice to a matched band whose floor moves up
        # past it.
        member_x = homo._profile_facts(
            np.array([[2, 1, 1], [1, 2, 0], [1, 0, 0]],
                     dtype=np.int64)
        )
        member_y = homo._profile_facts(
            np.array([[3, 0, 1], [1, 3, 0], [0, 1, 1]],
                     dtype=np.int64)
        )
        cut_x = homo._profile_facts(
            np.array([[4, 0, 1], [0, 2, 0], [1, 0, 0]],
                     dtype=np.int64)
        )
        standing_in = homo._search_free_envelope(
            real, [{"profile": member_x}, {"profile": member_y}]
        )
        self.assertEqual(
            (standing_in["self_pair_share"]["band_low"],
             standing_in["self_pair_share"]["band_high"]),
            (0.5, 0.7),
        )
        self.assertTrue(standing_in["self_pair_share"]["inside"])
        matched_out = homo._search_free_envelope(
            real, [{"profile": cut_x}, {"profile": cut_b}]
        )
        self.assertEqual(
            (matched_out["self_pair_share"]["band_low"],
             matched_out["self_pair_share"]["band_high"]),
            (0.75, 1.0),
        )
        self.assertFalse(matched_out["self_pair_share"]["inside"])

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_matched_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 540)
        self.assertEqual(
            self.artifact["bridge_gate"]["fields_compared"], fields
        )
        self.assertEqual(
            self.artifact["bridge_gate"]["status"], "verified"
        )

    def test_headline_verdicts(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(
                    cell["verdict"], "shape-outside-analogues"
                )
                expected = OUTSIDE.get((code, language), OUTSIDE_ALL)
                self.assertEqual(
                    cell["outside_invariants"], expected
                )
                for key in OUTSIDE_ALL:
                    test = cell["invariants"][key]
                    self.assertEqual(
                        test["inside"],
                        key not in expected,
                    )

    def test_vector_outside_counts(self) -> None:
        for (code, language), (symbols, pairs) in VECTOR_COUNTS.items():
            cell = self.artifact["files"][code][language]
            share_out = cell["invariants"]["symbol_shares"]["outside"]
            pair_out = cell["invariants"]["pair_shares"]["outside"]
            self.assertEqual(len(share_out), symbols)
            self.assertEqual(len(pair_out), pairs)
            for entry in share_out:
                self.assertLess(entry["position"], 36)
            for entry in pair_out:
                self.assertLess(entry["position"], 1296)
        # The matched re-pricing left the vector outside counts
        # identical to the frozen corpus-breadth counts.
        for code in FILES:
            for language in LANGS:
                standing = self.frozen_breadth["files"][code][
                    language
                ]["invariants"]
                for key, count in zip(
                    ("symbol_shares", "pair_shares"),
                    VECTOR_COUNTS[(code, language)],
                ):
                    self.assertEqual(
                        len(standing[key]["outside"]), count
                    )

    def test_scalar_band_ranges(self) -> None:
        for (code, language), table in SCALARS.items():
            invariants = self.artifact["files"][code][language][
                "invariants"
            ]
            for key, (real, low, high) in table.items():
                test = invariants[key]
                self.assertEqual(test["real"], real)
                self.assertEqual(test["band_low"], low)
                self.assertEqual(test["band_high"], high)
                inside = (
                    key == "self_pair_share"
                    and (code, language) == ("GC", "latin")
                )
                self.assertEqual(test["inside"], inside, key)

    def test_sorted_envelope_heads(self) -> None:
        for (code, language), sym0 in HEADS.items():
            invariants = self.artifact["files"][code][language][
                "invariants"
            ]
            sym_entry = invariants["symbol_shares"]["outside"][0]
            pair_entry = invariants["pair_shares"]["outside"][0]
            self.assertEqual(
                (sym_entry["real"], sym_entry["band_low"],
                 sym_entry["band_high"]),
                sym0,
            )
            top1 = SCALARS[(code, language)]["top_1_share"]
            self.assertEqual(
                (pair_entry["real"], pair_entry["band_low"],
                 pair_entry["band_high"]),
                top1,
            )

    def test_real_records(self) -> None:
        for code, row in REAL.items():
            events, unmapped, kept, standing_length, basis = row
            real = homo._homo_real_stream(code)
            self.assertEqual(real["total_events"], events)
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen_breadth["files"][code][language]
                self.assertEqual(cell["stream_events"], events)
                self.assertEqual(cell["unmapped_events"], unmapped)
                self.assertEqual(cell["kept_pairs"], kept)
                self.assertEqual(
                    cell["boundary_carried_pairs"],
                    frozen["boundary_carried_pairs"],
                )
                self.assertEqual(
                    cell["real_profile"], frozen["real_profile"]
                )
                self.assertEqual(
                    cell["real_full_width_total_pairs"], kept
                )
                self.assertEqual(
                    cell["standing_plant_length"], standing_length
                )
                self.assertEqual(
                    cell["match_basis_events"], basis
                )
                self.assertEqual(basis, kept + 1)
                self.assertTrue(cell["plants_at_source_identity"])
                for key in homo.MATCHED_REAL_RECORD_KEYS:
                    self.assertIn(key, cell, key)

    def test_members_replay(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen_breadth["files"][code][language]
                rows = cell["members_profiles"]
                basis = cell["match_basis_events"]
                kept = cell["kept_pairs"]
                cut, whole = CUT_WHOLE[(code, language)]
                self.assertEqual(
                    len(rows), 12 if language == "english" else 11
                )
                self.assertEqual(
                    cell["matched_members_cut"], cut
                )
                self.assertEqual(len(rows) - cut, whole)
                for row, stored_row in zip(rows, frozen[
                    "members_profiles"
                ]):
                    self.assertEqual(sorted(row), MEMBER_KEYS)
                    for key in (
                        "file", "ebook", "plant_length",
                        "selected_draw_index", "draw_rule",
                        "full_width_total_pairs",
                    ):
                        self.assertEqual(
                            row[key], stored_row[key], key
                        )
                    self.assertEqual(
                        row["matched_total_pairs"],
                        row["matched_length"] - 1,
                    )
                    self.assertEqual(
                        row["matched_length"],
                        min(row["plant_length"], basis),
                    )
                    if row["matched_length"] < row["plant_length"]:
                        self.assertEqual(
                            row["matched_total_pairs"], kept
                        )
                    else:
                        self.assertEqual(
                            row["matched_profile"],
                            stored_row["profile"],
                        )
                totals = [
                    row["matched_profile"]["total_pairs"]
                    for row in rows
                ]
                entropies = [
                    row["matched_profile"]["pair_entropy"]
                    for row in rows
                ]
                low, high, low_en, high_en = MEMBER_BLOCKS[
                    (code, language)
                ]
                self.assertEqual(min(totals), low)
                self.assertEqual(max(totals), high)
                self.assertEqual(min(entropies), low_en)
                self.assertEqual(max(entropies), high_en)

    def test_it_degenerate_identity(self) -> None:
        for language in LANGS:
            cell = self.artifact["files"]["IT"][language]
            standing = self.frozen_breadth["files"]["IT"][language]
            self.assertEqual(cell["match_basis_events"], 220532)
            self.assertEqual(cell["matched_members_cut"], 0)
            self.assertEqual(cell["matched_plants_cut"], 0)
            for row, stored_row in zip(
                cell["members_profiles"],
                standing["members_profiles"],
            ):
                self.assertEqual(
                    row["matched_length"], row["plant_length"]
                )
                self.assertEqual(
                    row["matched_total_pairs"],
                    stored_row["full_width_total_pairs"],
                )
                self.assertEqual(
                    row["matched_profile"], stored_row["profile"]
                )
            for row, stored_row in zip(
                cell["plants_profiles"],
                standing["plants_profiles"],
            ):
                self.assertEqual(
                    row["matched_length"], row["plant_length"]
                )
                self.assertEqual(
                    row["matched_total_pairs"],
                    stored_row["full_width_total_pairs"],
                )
                self.assertEqual(
                    row["matched_profile"], stored_row["profile"]
                )
            self.assertEqual(
                cell["plaintext_matched_profile"],
                cell["plaintext_profile"],
            )
            self.assertEqual(
                cell["invariants"], standing["invariants"]
            )
            self.assertEqual(
                cell["outside_invariants"],
                standing["outside_invariants"],
            )
            self.assertEqual(
                cell["verdict"], standing["verdict"]
            )

    def test_plants_matched(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen_breadth["files"][code][language]
                rows = cell["plants_profiles"]
                basis = cell["match_basis_events"]
                kept = cell["kept_pairs"]
                self.assertEqual(len(rows), 5)
                self.assertEqual(
                    cell["matched_plants_cut"],
                    0 if code == "IT" else 5,
                )
                for row, stored_row in zip(rows, frozen[
                    "plants_profiles"
                ]):
                    self.assertEqual(sorted(row), PLANT_KEYS)
                    for key in (
                        "index", "plant_length",
                        "full_width_total_pairs",
                    ):
                        self.assertEqual(
                            row[key], stored_row[key], key
                        )
                    self.assertEqual(
                        row["matched_total_pairs"],
                        row["matched_length"] - 1,
                    )
                    self.assertEqual(
                        row["matched_length"],
                        min(row["plant_length"], basis),
                    )
                    if row["matched_length"] < row["plant_length"]:
                        self.assertEqual(
                            row["matched_total_pairs"], kept
                        )
                    else:
                        self.assertEqual(
                            row["matched_profile"],
                            stored_row["profile"],
                        )
                blocks = {
                    row["matched_profile"]["total_pairs"]
                    for row in rows
                }
                self.assertEqual(
                    blocks, {PLANT_BLOCKS[(code, language)]}
                )

    def test_floors_matched(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen_breadth["files"][code][language]
                floors = cell["floors_profiles"]
                self.assertEqual(len(floors), 5)
                for row, stored_row in zip(
                    floors, frozen["floors_profiles"]
                ):
                    self.assertEqual(row, stored_row)
                    self.assertEqual(
                        row["full_width_total_pairs"],
                        cell["kept_pairs"],
                    )

    def test_plaintext_controls(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                frozen = self.frozen_breadth["files"][code][language]
                profile = cell["plaintext_profile"]
                self.assertEqual(profile["state_types"], 729)
                self.assertEqual(
                    profile["pair_entropy"], PLAIN[(code, language)]
                )
                self.assertEqual(profile, frozen["plaintext_profile"])
                matched = cell["plaintext_matched_profile"]
                self.assertEqual(
                    matched["pair_entropy"],
                    MATCHED_PLAIN[(code, language)],
                )
                self.assertEqual(
                    matched["total_pairs"], cell["kept_pairs"]
                )

    def test_encodings_above_their_matched_plaintext_sources(self) -> None:
        # Every matched encoding's block entropy sits above its own
        # matched plaintext source's entropy, while the real's block
        # entropy sits below every matched encoding in every cell,
        # with the band's streams held at the real's own counted
        # pair mass.
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                matched_h = cell["plaintext_matched_profile"][
                    "pair_entropy"
                ]
                for member in cell["members_profiles"]:
                    self.assertGreater(
                        member["matched_profile"]["pair_entropy"],
                        matched_h,
                    )
                for plant in cell["plants_profiles"]:
                    self.assertGreater(
                        plant["matched_profile"]["pair_entropy"],
                        matched_h,
                    )
                self.assertLess(
                    cell["real_profile"]["pair_entropy"],
                    min(
                        m["matched_profile"]["pair_entropy"]
                        for m in cell["members_profiles"]
                    ),
                )

    def test_measured_direction(self) -> None:
        # The recorded direction of every outside invariant against
        # its matched band, the search-free directions unchanged
        # under the matched basis: the real's entropy below the band
        # in all six cells, its top-k shares and its empty type
        # count above the band everywhere, its self-pair share above
        # the band in the ZL and IT cells, below it in the GC
        # english cell, and inside the matched band in the GC latin
        # cell - the one invariant the matched basis has not pushed
        # out.
        for code in FILES:
            for language in LANGS:
                invariants = self.artifact["files"][code][language][
                    "invariants"
                ]
                self.assertLess(
                    invariants["pair_entropy"]["real"],
                    invariants["pair_entropy"]["band_low"],
                )
                for key in (
                    "top_1_share", "top_10_share", "top_50_share",
                    "empty_type_count",
                ):
                    self.assertGreater(
                        invariants[key]["real"],
                        invariants[key]["band_high"],
                    )
                self_share = invariants["self_pair_share"]
                if code in ("ZL", "IT"):
                    self.assertFalse(self_share["inside"])
                    self.assertGreater(
                        self_share["real"],
                        self_share["band_high"],
                    )
                elif language == "english":
                    self.assertFalse(self_share["inside"])
                    self.assertLess(
                        self_share["real"],
                        self_share["band_low"],
                    )
                else:
                    self.assertTrue(self_share["inside"])
                    # The matched band's floor dropped below the
                    # frozen corpus-breadth band's floor, so the
                    # share sits deeper inside, not on the edge.
                    self.assertLess(
                        self_share["band_low"],
                        self.frozen_breadth["files"][code][
                            language]["invariants"][
                            "self_pair_share"]["band_low"],
                    )

    def test_both_ways_movements_against_the_frozen_bands(self) -> None:
        # The declared both-ways design, measured: the cut can move
        # a matched band's closed range down or up against its
        # frozen standing counterpart, and the artifact records
        # both. Here the ZL latin entropy ceiling moved down while
        # the ZL english top-50 ceiling moved up, floors moved down
        # in the ZL english top-1 and self-pair tests and the GC
        # latin self-pair test, and the GC english empty-type floor
        # moved up.
        for code, language, key, end, matched_value, direction in \
                MOVEMENTS:
            standing = self.frozen_breadth["files"][code][language][
                "invariants"
            ][key]
            matched = self.artifact["files"][code][language][
                "invariants"
            ][key]
            if end == "low":
                self.assertEqual(
                    matched["band_low"], matched_value, key
                )
                if direction == "below":
                    self.assertLess(
                        matched["band_low"], standing["band_low"]
                    )
                else:
                    self.assertGreater(
                        matched["band_low"], standing["band_low"]
                    )
            else:
                self.assertEqual(
                    matched["band_high"], matched_value, key
                )
                if direction == "below":
                    self.assertLess(
                        matched["band_high"], standing["band_high"]
                    )
                else:
                    self.assertGreater(
                        matched["band_high"], standing["band_high"]
                    )

    def test_one_cell_recompute(self) -> None:
        fresh = homo._matched_cell_facts("ZL", "english")
        stored = self.artifact["files"]["ZL"]["english"]
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
