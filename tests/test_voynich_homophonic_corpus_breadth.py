"""Tests for the declared corpus-breadth search-free instrument of
family 5, the twelfth measurement.

The frozen artifact pins the measurement; the reproducibility tests
recompute one full cell's facts from the declared kinds and the
standing streams and re-derive the three-source bridge gate; the
mechanical tests nail the declared rules on the stored artifact: the
constants and the corpus freeze (the eight accepted files with the
sha256 records, the eight rejected candidates with their verbatim
causes, the two probed-clean extras and the declared roster floor),
the declaration strings (the draw-0 rule for the breadth members, the
position axis extension of the homo_cross_enc kind, the widening
arithmetic, no assignment search anywhere, no split, no score table,
the strict-all verdict rule, no scalar margin, the 399-field
three-source gate), the module docstring's declaration including the
probe disclosures and the claim count, the truthful question, the
block arithmetic and the relabeling invariance on hand matrices, the
envelope arithmetic and the widening monotonicity on hand profiles,
the bridge gate at 399 fields, the six headline verdicts, the vector
outside counts, the scalar band ranges, the sorted envelope heads,
the real block profiles and stream states unchanged from the frozen
boundary-mark artifact, the standing members' replays against both
frozen predecessors, the breadth members' declared draw-0 rows, the
widened bands as weak supersets of the frozen bands with the
recorded pair-position decrements, the plants' identity and the
floors' directions, the plaintext controls unchanged, the measured
direction of every outside invariant, and the dash bans. Nothing
here reads the manuscript beyond the frozen artifacts and the
declared streams.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-corpus-breadth.json"
).resolve()
FROZEN_RESTART = Path(
    "docs/research-notes/voynich-homophonic-restart-budget.json"
).resolve()
FROZEN_SEARCH_FREE = Path(
    "docs/research-notes/voynich-homophonic-search-free.json"
).resolve()
FROZEN_BOUNDARY_MARK = Path(
    "docs/research-notes/voynich-homophonic-boundary-mark.json"
).resolve()

# The frozen artifact's headline, pinned from the artifact measured
# 23 October 2026 with the three-source bridge gate verified at 399
# fields: every cell is a shape-outside-analogue under the declared
# strict-all rule even with the band population widened to twelve
# english and eleven latin members per cell, and the widened roster
# produces the one inside invariant the boundary-mark instrument
# already recorded: the GC latin cell's self_pair_share again inside
# its widened band, so seven of its eight invariant tests sit outside.
OUTSIDE_ALL = [
    "symbol_shares", "pair_shares", "empty_type_count",
    "self_pair_share", "top_1_share", "top_10_share",
    "top_50_share", "pair_entropy",
]
OUTSIDE = {
    ("GC", "latin"): [
        "symbol_shares", "pair_shares", "empty_type_count",
        "top_1_share", "top_10_share", "top_50_share",
        "pair_entropy",
    ],
}

# (code, language) -> (symbol positions outside of 36,
# pair positions outside of 1296). Every symbol count is unchanged
# from the boundary-mark artifact; every pair count only moved
# inward (845 to 834 ZL english, 784 to 780 ZL latin, 832 to 829 GC
# english, 782 to 781 GC latin, 846 to 839 IT english, 788 to 785 IT
# latin), the widening's recorded direction.
VECTOR_COUNTS = {
    ("ZL", "english"): (35, 834),
    ("ZL", "latin"): (36, 780),
    ("GC", "english"): (36, 829),
    ("GC", "latin"): (33, 781),
    ("IT", "english"): (35, 839),
    ("IT", "latin"): (35, 785),
}
PAIR_DECREMENTS = {
    ("ZL", "english"): 11, ("ZL", "latin"): 4,
    ("GC", "english"): 3, ("GC", "latin"): 1,
    ("IT", "english"): 7, ("IT", "latin"): 3,
}

# (code, language) -> the six scalar invariant tests as
# (real, band_low, band_high); the inside flag is False everywhere
# except the GC latin cell's self_pair_share, which sits inside its
# widened band (0.015928 inside [0.013345, 0.023941], deeper inside
# than the boundary-mark instrument's [0.014518, 0.023941]).
SCALARS = {
    ("ZL", "english"): {
        "empty_type_count": (928, 323, 454),
        "self_pair_share": (0.065848, 0.0187, 0.026741),
        "top_1_share": (0.070481, 0.018196, 0.035886),
        "top_10_share": (0.424435, 0.106088, 0.148336),
        "top_50_share": (0.893671, 0.305696, 0.355739),
        "pair_entropy": (4.010179, 5.928491, 6.102864),
    },
    ("ZL", "latin"): {
        "empty_type_count": (928, 240, 503),
        "self_pair_share": (0.065848, 0.011829, 0.023974),
        "top_1_share": (0.070481, 0.013483, 0.02536),
        "top_10_share": (0.424435, 0.09782, 0.131916),
        "top_50_share": (0.893671, 0.268516, 0.336503),
        "pair_entropy": (4.010179, 5.980168, 6.252046),
    },
    ("GC", "english"): {
        "empty_type_count": (642, 317, 453),
        "self_pair_share": (0.015928, 0.018543, 0.027257),
        "top_1_share": (0.051049, 0.018404, 0.035512),
        "top_10_share": (0.373572, 0.106088, 0.15792),
        "top_50_share": (0.8066, 0.305406, 0.370019),
        "pair_entropy": (4.422831, 5.920628, 6.117306),
    },
    ("GC", "latin"): {
        "empty_type_count": (642, 258, 500),
        "self_pair_share": (0.015928, 0.013345, 0.023941),
        "top_1_share": (0.051049, 0.013463, 0.02536),
        "top_10_share": (0.373572, 0.097193, 0.133218),
        "top_50_share": (0.8066, 0.26876, 0.33872),
        "pair_entropy": (4.422831, 5.98016, 6.25487),
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

# (code, language) -> the sorted symbol envelope's first recorded
# entry (real, band_low, band_high); the sorted pair envelope's first
# entry equals the cell's top_1_share test.
HEADS = {
    ("ZL", "english"): (0.155542, 0.076105, 0.093069),
    ("ZL", "latin"): (0.155542, 0.067495, 0.099429),
    ("GC", "english"): (0.19975, 0.076457, 0.092941),
    ("GC", "latin"): (0.19975, 0.067495, 0.099429),
    ("IT", "english"): (0.158109, 0.07601, 0.093121),
    ("IT", "latin"): (0.158109, 0.067495, 0.099429),
}

# code -> (stream events, unmapped events, kept pairs, boundary
# carried pairs, block pairs, block empty types, block self pair
# share, top shares at k 1, 10, 50, block pair entropy, the mark's
# own position in the real alphabet, the real alphabet's width),
# shared by both language cells of a code and unchanged from the
# frozen boundary-mark artifact.
REAL = {
    "ZL": (218663, 126, 218415, 68616, 149799, 928, 0.065848,
           0.070481, 0.424435, 0.893671, 4.010179, 36, 37),
    "GC": (186708, 1769, 183199, 71384, 111815, 642, 0.015928,
           0.051049, 0.373572, 0.8066, 4.422831, 36, 37),
    "IT": (220532, 0, 220531, 72880, 147651, 984, 0.065777,
           0.071689, 0.429316, 0.89868, 3.980621, 23, 24),
}

# (code, language) -> the widened band's twelve (english) or eleven
# (latin) member block totals sorted, the block entropy range and
# the full-width range; the standing rows carry the frozen
# boundary-mark numbers exactly and the breadth rows add the new
# extrema (the scriptural registers drop the english entropy floor,
# the classical latin texts push its ceiling up).
MEMBERS = {
    ("ZL", "english"): (
        [55143, 129435, 130312, 131621, 132035, 132718, 134514,
         135724, 135954, 138578, 143092, 144510],
        5.928491, 6.102864, 91744, 218662,
    ),
    ("ZL", "latin"): (
        [31635, 53244, 54089, 61501, 90930, 102839, 147874, 153490,
         154028, 155874, 158644],
        5.980168, 6.252046, 45490, 218662,
    ),
    ("GC", "english"): (
        [55143, 110409, 111189, 112325, 113101, 113509, 114833,
         116053, 116381, 118135, 122043, 123165],
        5.920628, 6.117306, 91744, 186707,
    ),
    ("GC", "latin"): (
        [31635, 53244, 54089, 61501, 90930, 102839, 126612, 131179,
         131507, 133021, 135185],
        5.98016, 6.25487, 45490, 186707,
    ),
    ("IT", "english"): (
        [55143, 130570, 131420, 132719, 133131, 133884, 135675,
         136837, 137083, 139777, 144345, 145751],
        5.927877, 6.102609, 91744, 220531,
    ),
    ("IT", "latin"): (
        [31635, 53244, 54089, 61501, 90930, 102839, 149195, 154783,
         155331, 157213, 159999],
        5.980406, 6.252202, 45490, 220531,
    ),
}

# The breadth members' rows: (code, language) -> lists of
# (file, ebook, plant_length, block total, block entropy) in the
# declared roster positions english 7 to 11 and latin 8 to 10, every
# row at the declared draw 0. The plant length is the truncated
# stream length (the file's processed stream cut to the real's own
# total events), and the scriptural KJV registers the english cells'
# lowest block entropy while the classical latin texts sit above the
# standing latin band's ceiling.
BREADTH_ROWS = {
    ("ZL", "english"): [
        ("substref_english10_pg10.txt", 10, 218663, 130312,
         5.928491),
        ("substref_english11_pg829.txt", 829, 218663, 135724,
         6.057498),
        ("substref_english12_pg1041.txt", 1041, 91745, 55143,
         6.05617),
        ("substref_english13_pg1404.txt", 1404, 218663, 144510,
         6.011799),
        ("substref_english14_pg1228.txt", 1228, 218663, 143092,
         6.041117),
    ],
    ("ZL", "latin"): [
        ("substref_latin11_pg227.txt", 227, 218663, 154028,
         6.188583),
        ("substref_latin12_pg18837.txt", 18837, 218663, 158644,
         6.252046),
        ("substref_latin13_pg226.txt", 226, 87917, 61501, 6.250311),
    ],
    ("GC", "english"): [
        ("substref_english10_pg10.txt", 10, 186708, 111189,
         5.920628),
        ("substref_english11_pg829.txt", 829, 186708, 116053,
         6.05277),
        ("substref_english12_pg1041.txt", 1041, 91745, 55143,
         6.055976),
        ("substref_english13_pg1404.txt", 1404, 186708, 123165,
         6.009304),
        ("substref_english14_pg1228.txt", 1228, 186708, 122043,
         6.044179),
    ],
    ("GC", "latin"): [
        ("substref_latin11_pg227.txt", 227, 186708, 131507,
         6.185451),
        ("substref_latin12_pg18837.txt", 18837, 186708, 135185,
         6.25487),
        ("substref_latin13_pg226.txt", 226, 87917, 61501, 6.250384),
    ],
    ("IT", "english"): [
        ("substref_english10_pg10.txt", 10, 220532, 131420,
         5.927877),
        ("substref_english11_pg829.txt", 829, 220532, 136837,
         6.057702),
        ("substref_english12_pg1041.txt", 1041, 91745, 55143,
         6.056214),
        ("substref_english13_pg1404.txt", 1404, 220532, 145751,
         6.011739),
        ("substref_english14_pg1228.txt", 1228, 220532, 144345,
         6.041255),
    ],
    ("IT", "latin"): [
        ("substref_latin11_pg227.txt", 227, 220532, 155331,
         6.186259),
        ("substref_latin12_pg18837.txt", 18837, 220532, 159999,
         6.252202),
        ("substref_latin13_pg226.txt", 226, 87917, 61501, 6.250893),
    ],
}

# (code, language) -> the five plants' block totals (one shared
# number per cell) and the five floors' block totals (sorted),
# unchanged from the frozen boundary-mark artifact.
PLANT_BLOCKS = {
    ("ZL", "english"): 137499,
    ("ZL", "latin"): 151003,
    ("GC", "english"): 117398,
    ("GC", "latin"): 128764,
    ("IT", "english"): 138635,
    ("IT", "latin"): 152294,
}
PLANT_FULL = {"ZL": 218662, "GC": 186707, "IT": 220531}
FLOOR_BLOCKS = {
    ("ZL", "english"): [155062, 155115, 155133, 155181, 155329],
    ("ZL", "latin"): [155145, 155163, 155229, 155236, 155274],
    ("GC", "english"): [118389, 118438, 118443, 118448, 118458],
    ("GC", "latin"): [118405, 118418, 118453, 118468, 118540],
    ("IT", "english"): [153622, 153664, 153673, 153690, 153739],
    ("IT", "latin"): [153663, 153680, 153701, 153746, 153751],
}

# (code, language) -> the plaintext control's (empty types, self
# share, top_1 share, top_50 share, pair entropy), all on 729 types
# and all unchanged from both frozen predecessor artifacts.
PLAIN = {
    ("ZL", "english"): (260, 0.019404, 0.033115, 0.567854, 5.139035),
    ("ZL", "latin"): (339, 0.013775, 0.026671, 0.569404, 5.06327),
    ("GC", "english"): (265, 0.019432, 0.033079, 0.568297, 5.139139),
    ("GC", "latin"): (342, 0.013631, 0.026544, 0.569647, 5.063406),
    ("IT", "english"): (260, 0.019439, 0.033079, 0.567712, 5.139068),
    ("IT", "latin"): (339, 0.01373, 0.026695, 0.56958, 5.062979),
}
PLAIN_FULL = {"ZL": 218662, "GC": 186707, "IT": 220531}

# The corpus freeze as probed: accepted (file, ebook, file bytes,
# stream total, token types) and the rejected ebooks in order.
ACCEPTED = [
    ("substref_english10_pg10.txt", 10, 4455950, 4018128, 27),
    ("substref_english11_pg829.txt", 829, 613946, 564687, 27),
    ("substref_english12_pg1041.txt", 1041, 119936, 91745, 27),
    ("substref_english13_pg1404.txt", 1404, 1186849, 1122186, 27),
    ("substref_english14_pg1228.txt", 1228, 970611, 906068, 27),
    ("substref_latin11_pg227.txt", 227, 495876, 431388, 25),
    ("substref_latin12_pg18837.txt", 18837, 255543, 225036, 24),
    ("substref_latin13_pg226.txt", 226, 112390, 87917, 24),
]
REJECTED_EBOOKS = [
    21765, 14945, 16564, 20732, 25861, 20771, 63139, 19635,
]


class CorpusBreadthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_restart = json.loads(FROZEN_RESTART.read_text())
        self.frozen_search_free = json.loads(
            FROZEN_SEARCH_FREE.read_text()
        )
        self.frozen_boundary_mark = json.loads(
            FROZEN_BOUNDARY_MARK.read_text()
        )
        self.declared = self.artifact["declared"]
        self.corpus = self.declared["corpus_facts"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.SEARCH_FREE_TOP_K, (1, 10, 50))
        self.assertEqual(homo.SEARCH_FREE_SHARES, 6)
        self.assertTrue(
            str(homo.SEARCH_FREE_BREADTH_ARTIFACT_PATH).endswith(
                "voynich-homophonic-corpus-breadth.json"
            )
        )
        self.assertEqual(self.declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(self.declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(
            sorted(self.corpus),
            [
                "accepted", "extras_not_selected",
                "fetch_verification", "rejected_breadth_candidates",
                "roster_floor_stream",
            ],
        )
        self.assertEqual(self.corpus["roster_floor_stream"], 45491)
        self.assertEqual(homo.BREADTH_ROSTER_FLOOR_STREAM, 45491)
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
            self.artifact["bridge_gate"],
            {
                "status": "verified",
                "fields_compared": 399,
                "anchor_fields": 288,
                "profile_equality_checks": 111,
            },
        )

    def test_the_corpus_breadth_declaration(self) -> None:
        rule = self.declared["corpus_breadth_rule"]
        self.assertIn(
            "the standing roster replays first, the breadth members "
            "take the listed positions english 7 to 11 and latin 8 to 10",
            rule,
        )
        self.assertIn(
            "the declared homo_cross_enc kind's position axis extends, "
            "no new seed kind",
            rule,
        )
        self.assertIn(
            "each breadth member's processed stream must reach the "
            "standing roster's smallest member stream length (45,491 "
            "tokens, Vulgata Esther)",
            rule,
        )
        self.assertIn(
            "every accepted candidate clears that floor", rule,
        )
        source = self.declared["corpus_source_rule"]
        self.assertIn(
            "the standing fetch verification was rehearsed", source,
        )
        self.assertIn(
            "447,911 bytes, span sha256 "
            "7f95a6c0484513216cffa7d9e1e0314896faa21cb5a713d65c125a86f"
            "1f43695",
            source,
        )
        self.assertIn(
            "bytes 49, 60, 555 and 566", source,
        )
        self.assertIn(
            "recorded as metadata drift the marker span does not "
            "carry",
            source,
        )
        self.assertIn(
            "inside the standing transcriber-note scale's 0 to 52",
            source,
        )
        self.assertIn(
            "ebook 3207 Leviathan, ebook 148 The Autobiography of "
            "Benjamin Franklin",
            source,
        )
        self.assertIn(
            "the breadth members' declared draw-0 sources sit beside "
            "the standing members' frozen selected draws",
            self.declared["state_note"],
        )
        self.assertIn(
            "no assignment search anywhere: no candidate evaluation, "
            "no restarts, no sweep cap, no convergence flags",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "no split applies", self.declared["split_rule"]
        )
        self.assertIn(
            "the homo_cross_enc kind's position axis extends to the "
            "breadth members' listed positions (english 7 to 11, "
            "latin 8 to 10); no new seed kind is consumed",
            self.declared["seed_kinds"],
        )
        self.assertIn(
            "the stream's first draw at their listed positions, "
            "declared in advance with no selection performed",
            self.declared["seed_sharing"],
        )
        self.assertIn(
            "so 12 english and 11 latin member profiles per cell",
            self.declared["band_record_rule"],
        )
        self.assertIn(
            "no parity rule applies because there is no anchor "
            "geometry to exceed",
            self.declared["plants_rule"],
        )
        self.assertIn(
            "not part of any envelope", self.declared["floors_rule"]
        )
        self.assertIn(
            "takes no part in any envelope",
            self.declared["plaintext_rule"],
        )
        self.assertIn(
            "declared strict-all", self.declared["verdict_rule"]
        )
        self.assertIn(
            "every declared invariant of the real's glyph-block "
            "profile sits inside the closed range of that cell's "
            "widened band's glyph-block profiles",
            self.declared["verdict_rule"],
        )
        self.assertIn(
            "so the miss is audited not summarized",
            self.declared["verdict_rule"],
        )
        self.assertIn(
            "no scalar margin is formed", self.declared["closure_rule"]
        )
        gate = self.declared["bridge_gate"]
        self.assertIn(
            "the boundary-mark instrument's 288 anchor fields exactly "
            "as that instrument declared them", gate,
        )
        self.assertIn(
            "111 profile checks total (18 per english cell and 19 "
            "per latin cell times 3 files)",
            gate,
        )
        self.assertIn(
            "the breadth members carry no frozen counterpart", gate,
        )
        self.assertIn(
            "any divergence aborts with nothing written", gate,
        )
        self.assertIn(
            "no score table is built or used",
            self.declared["models_rule"],
        )
        self.assertIn(
            "not re-scoped", self.declared["exclusion_rule"]
        )
        self.assertIn(
            "the band instruments' verdicts stand untouched",
            self.declared["exclusion_rule"],
        )

    def test_fetch_verification_record(self) -> None:
        verif = self.corpus["fetch_verification"]
        self.assertEqual(
            verif["standing_file"], "substref_english2_pg84.txt"
        )
        self.assertEqual(
            verif["frozen_sha256"],
            "7810cd483cffcf2cc8a1d8f0d5807931e69d4f48cd14149b8c76f88a"
            "f82fead3",
        )
        self.assertEqual(
            verif["fresh_sha256"],
            "2b97b7f8aad508649481d8dd4f6b54f9b965ddb3ba634e9151c815f53"
            "7b49e42",
        )
        self.assertEqual(verif["file_bytes"], 448885)
        self.assertEqual(
            verif["marker_span_sha256"],
            "7f95a6c0484513216cffa7d9e1e0314896faa21cb5a713d65c125a86f"
            "1f43695",
        )
        self.assertIn("49, 60, 555 and 566", verif["drift"])
        self.assertIn("byte-identical", verif["drift"])
        self.assertIn("metadata drift", verif["drift"])

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "Twelfth declared measurement, the corpus-breadth "
            "search-free instrument",
            "adding members to a band can only widen the band's "
            "closed ranges and per-position envelopes",
            "the only verdict change this design can produce is a "
            "cell reporting inside under the widened band",
            "whether the interior's separation holds as the roster "
            "grows",
            "each breadth member taking draw 0 of the declared "
            "homo_cross_enc kind at its listed position",
            "45,491 tokens, Vulgata Esther",
            "the gate ran at 399 fields compared, no problem",
            "Probe 2, the corpus freeze facts ahead of the run",
            "Probe 3, the first cell's declared verdict ahead of "
            "the run, ZL english",
            "shape-outside-analogues with every one of the eight "
            "invariant tests outside",
            "Probe 4, the first latin cell's declared verdict "
            "ahead of the run, ZL latin",
            "extend the standing latin band's entropy top end "
            "upward from 6.104489 to 6.252046",
            "Probe 5, the plaintext control recorded unchanged",
            "Probe 6: none",
            "probes' disclosed first-cell verdicts do not "
            "decide the artifact",
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
            "does the real's mark-excluded profile sit inside the "
            "extended band's range on every declared invariant in "
            "every (file, language) cell, or is at least one "
            "invariant outside",
            what,
        )
        self.assertIn(
            "the measured test of whether the interior's separation "
            "holds as the roster grows", what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading.",
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

    def test_band_widening_arithmetic_on_hand_profiles(self) -> None:
        # The declared widening arithmetic, pinned by hand: adding a
        # member to a band can only widen its closed ranges (each
        # extremum is taken over more members), and it is the only
        # verdict change this design can produce - here the third
        # member's flatter structure widens both ends downward and
        # pulls the queried profile's self-pair share and top-1
        # concentration inside the band, exactly the one way a
        # widened cell can report inside its band.
        member_a = homo._profile_facts(
            np.array([[4, 1, 0], [1, 2, 0], [0, 0, 1]],
                     dtype=np.int64)
        )
        member_b = homo._profile_facts(
            np.array([[2, 0, 0], [0, 4, 1], [0, 1, 0]],
                     dtype=np.int64)
        )
        member_c = homo._profile_facts(
            np.array([[1, 1, 0], [1, 1, 2], [0, 2, 0]],
                     dtype=np.int64)
        )
        narrow = homo._search_free_envelope(
            member_c, [{"profile": member_a}, {"profile": member_b}]
        )
        self.assertFalse(narrow["self_pair_share"]["inside"])
        self.assertFalse(narrow["top_1_share"]["inside"])
        wide = homo._search_free_envelope(
            member_c, [{"profile": member_a},
                       {"profile": member_b},
                       {"profile": member_c}]
        )
        for key in ("self_pair_share", "top_1_share", "pair_entropy"):
            self.assertLessEqual(wide[key]["band_low"],
                                 narrow[key]["band_low"])
            self.assertGreaterEqual(wide[key]["band_high"],
                                    narrow[key]["band_high"])
        self.assertTrue(wide["self_pair_share"]["inside"])
        self.assertTrue(wide["top_1_share"]["inside"])
        # No narrowing appears anywhere in the scalar tests: the
        # outside set of a widened band is a subset of its standing
        # counterpart's outside set.
        self.assertLessEqual(
            [key for key, test in wide.items() if not test["inside"]],
            [key for key, test in narrow.items() if not test["inside"]],
        )

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_breadth_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 399)
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

    def test_real_profiles_and_streams(self) -> None:
        for code, row in REAL.items():
            (events, unmapped, pairs, carried, block_pairs, empty,
             self_share, top1, top10, top50, entropy, mark,
             width) = row
            real = homo._homo_real_stream(code)
            self.assertEqual(
                len(real["mapped_chars"]), width
            )
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(cell["stream_events"], events)
                self.assertEqual(cell["unmapped_events"], unmapped)
                self.assertEqual(cell["kept_pairs"], pairs)
                self.assertEqual(
                    cell["boundary_carried_pairs"], carried
                )
                self.assertEqual(
                    cell["real_full_width_total_pairs"], pairs
                )
                self.assertEqual(
                    pairs, block_pairs + carried
                )
                profile = cell["real_profile"]
                self.assertEqual(
                    profile, self.frozen_boundary_mark["files"][code][
                        language]["real_profile"]
                )
                self.assertEqual(profile["total_pairs"], block_pairs)
                self.assertEqual(profile["state_types"], 1296)
                self.assertEqual(
                    len(profile["symbol_counts"]), 36
                )
                self.assertEqual(
                    profile["empty_type_count"], empty
                )
                self.assertEqual(
                    profile["self_pair_share"], self_share
                )
                self.assertEqual(profile["top_1_share"], top1)
                self.assertEqual(profile["top_10_share"], top10)
                self.assertEqual(profile["top_50_share"], top50)
                self.assertEqual(profile["pair_entropy"], entropy)
            self.assertEqual(mark, len(real["mapped_chars"]) - 1)

    def test_members_replay(self) -> None:
        for (code, language), (totals, low, high, width_min,
                               width_max) in MEMBERS.items():
            cell = self.artifact["files"][code][language]
            members = cell["members_profiles"]
            self.assertEqual(
                len(members),
                12 if language == "english" else 11,
            )
            self.assertEqual(
                sorted(m["profile"]["total_pairs"] for m in members),
                totals,
            )
            entropies = sorted(
                m["profile"]["pair_entropy"] for m in members
            )
            self.assertEqual(entropies[0], low)
            self.assertEqual(entropies[-1], high)
            widths = sorted(
                m["full_width_total_pairs"] for m in members
            )
            self.assertEqual(widths[0], width_min)
            self.assertEqual(widths[-1], width_max)
            for member in members:
                self.assertGreater(
                    member["full_width_total_pairs"],
                    member["profile"]["total_pairs"],
                )
                self.assertLess(
                    member["profile"]["empty_type_count"],
                    1296,
                )
            frozen_band = self.frozen_restart["files"][code][
                language
            ]["band"]
            frozen_free = self.frozen_search_free["files"][code][
                language
            ]["members_profiles"]
            frozen_bm = self.frozen_boundary_mark["files"][code][
                language
            ]["members_profiles"]
            for position, member in enumerate(members[:len(
                    frozen_band)]):
                stored = frozen_band[position]
                self.assertEqual(member["file"], stored["file"])
                self.assertEqual(member["ebook"], stored["ebook"])
                self.assertEqual(
                    member["plant_length"], stored["plant_length"]
                )
                self.assertEqual(
                    member["selected_draw_index"],
                    stored["selected_draw_index"],
                )
                self.assertEqual(
                    member["full_width_total_pairs"],
                    frozen_free[position]["profile"]["total_pairs"],
                )
                stored_bm = frozen_bm[position]
                self.assertEqual(
                    {key: member[key] for key in stored_bm},
                    stored_bm,
                )
            for member in members[len(frozen_band):]:
                self.assertEqual(
                    member["draw_rule"], "breadth_declared_draw_0"
                )

    def test_breadth_members(self) -> None:
        for (code, language), rows in BREADTH_ROWS.items():
            members = self.artifact["files"][code][language][
                "members_profiles"
            ]
            standing = len(members) - len(rows)
            for offset, expected in enumerate(rows):
                member = members[standing + offset]
                (name, ebook, plant_length, block_total,
                 entropy) = expected
                self.assertEqual(member["file"], name)
                self.assertEqual(member["ebook"], ebook)
                self.assertEqual(
                    member["plant_length"], plant_length
                )
                self.assertEqual(
                    member["selected_draw_index"], 0
                )
                self.assertEqual(
                    member["draw_rule"], "breadth_declared_draw_0"
                )
                self.assertEqual(
                    member["profile"]["total_pairs"], block_total
                )
                self.assertEqual(
                    member["profile"]["pair_entropy"], entropy
                )
            # The breadth positions of the declared roster: english 7
            # to 11, latin 8 to 10 (five and three members).
            self.assertEqual(
                [m["ebook"] for m in members[standing:]],
                [row[1] for row in rows],
            )
        for code in FILES:
            for language in LANGS:
                members = self.artifact["files"][code][language][
                    "members_profiles"
                ]
                standing = 7 if language == "english" else 8
                self.assertEqual(
                    len(members),
                    standing + (5 if language == "english" else 3),
                )
                for index in range(standing):
                    self.assertNotIn(
                        "draw_rule", self.frozen_boundary_mark["files"][
                            code][language]["members_profiles"][index]
                    )
                    self.assertEqual(
                        members[index]["draw_rule"],
                        "standing_frozen_selected",
                    )

    def test_corpus_freeze(self) -> None:
        accepted = self.corpus["accepted"]
        self.assertEqual(
            [(row["file"], row["ebook"]) for row in accepted],
            [
                (name, ebook) for name, ebook, _label
                in homo.BREADTH_REFERENCE_FILES["english"]
            ]
            + [
                (name, ebook) for name, ebook, _label
                in homo.BREADTH_REFERENCE_FILES["latin"]
            ],
        )
        for row, (name, ebook, file_bytes, stream_total,
                  types) in zip(accepted, ACCEPTED):
            path = (
                Path("engine/data").resolve() / name
            )
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                row["sha256"],
            )
            self.assertEqual(row["file_bytes"], file_bytes)
            self.assertEqual(row["stream_total"], stream_total)
            self.assertEqual(row["types_present"], types)
            self.assertGreaterEqual(
                row["stream_total"], 45491
            )
        self.assertEqual(
            [row["ebook"] for row in self.corpus[
                "rejected_breadth_candidates"]],
            REJECTED_EBOOKS,
        )
        for row in self.corpus["rejected_breadth_candidates"]:
            self.assertTrue(row["cause"])
        by_ebook = {
            row["ebook"]: row["cause"] for row in self.corpus[
                "rejected_breadth_candidates"]
        }
        self.assertIn("404", by_ebook[19635])
        self.assertIn("17,181", by_ebook[21765])
        self.assertIn("54", by_ebook[20771])
        self.assertIn("55", by_ebook[63139])
        self.assertEqual(
            [row["ebook"] for row in self.corpus[
                "extras_not_selected"]],
            [3207, 148],
        )
        # The declared loader's own facts on one probed file.
        stream = homo._reference_stream(
            "english", file="substref_english12_pg1041.txt"
        )
        letters = sum(1 for value in stream if value != 26)
        self.assertEqual(len(stream), 91745)
        self.assertEqual(letters, 73444)
        self.assertEqual(len(stream) - letters, 18301)
        self.assertEqual(len(set(stream)), 27)

    def test_widened_bands_superset_the_frozen_bands(self) -> None:
        # The declared widening arithmetic measured against the
        # frozen boundary-mark artifact: every scalar band here is a
        # weak superset of its standing counterpart, the symbol
        # envelope's outside counts stand unchanged, and the pair
        # envelope's outside count only moved inward, by the
        # recorded decrements.
        for code in FILES:
            for language in LANGS:
                invariants = self.artifact["files"][code][language][
                    "invariants"
                ]
                standing = self.frozen_boundary_mark["files"][code][
                    language
                ]["invariants"]
                for key in ("empty_type_count", "self_pair_share",
                            "top_1_share", "top_10_share",
                            "top_50_share", "pair_entropy"):
                    self.assertLessEqual(
                        invariants[key]["band_low"],
                        standing[key]["band_low"],
                    )
                    self.assertGreaterEqual(
                        invariants[key]["band_high"],
                        standing[key]["band_high"],
                    )
                for key in ("symbol_shares", "pair_shares"):
                    fresh = invariants[key]["outside"]
                    stored = standing[key]["outside"]
                    self.assertLessEqual(len(fresh), len(stored))
                    stored_at = {
                        entry["position"]: entry for entry in stored
                    }
                    for entry in fresh:
                        if entry["position"] in stored_at:
                            other = stored_at[entry["position"]]
                            # Widening direction: the fresh envelope
                            # contains the standing envelope at every
                            # shared position.
                            self.assertLessEqual(
                                entry["band_low"], other["band_low"],
                            )
                            self.assertGreaterEqual(
                                entry["band_high"],
                                other["band_high"],
                            )
                self.assertEqual(
                    PAIR_DECREMENTS[(code, language)],
                    len(standing["pair_shares"]["outside"])
                    - len(invariants["pair_shares"]["outside"]),
                )
                self.assertEqual(
                    len(standing["symbol_shares"]["outside"]),
                    len(invariants["symbol_shares"]["outside"]),
                )

    def test_plants_and_floors(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertIs(
                    cell["plants_at_source_identity"], True
                )
                plants = cell["plants_profiles"]
                floors = cell["floors_profiles"]
                self.assertEqual(len(plants), 5)
                self.assertEqual(len(floors), 5)
                for plant in plants:
                    self.assertEqual(
                        plant["full_width_total_pairs"],
                        PLANT_FULL[code],
                    )
                    self.assertEqual(
                        plant["full_width_total_pairs"],
                        plant["plant_length"] - 1,
                    )
                    self.assertEqual(
                        plant["profile"]["total_pairs"],
                        PLANT_BLOCKS[(code, language)],
                    )
                    self.assertEqual(
                        plant["plant_length"],
                        cell["standing_plant_length"],
                    )
                self.assertEqual(
                    cell["standing_plant_length"],
                    cell["stream_events"],
                )
                floor_totals = sorted(
                    f["profile"]["total_pairs"] for f in floors
                )
                self.assertEqual(
                    floor_totals,
                    FLOOR_BLOCKS[(code, language)],
                )
                for floor in floors:
                    self.assertEqual(
                        floor["full_width_total_pairs"],
                        cell["kept_pairs"],
                    )
                    self.assertGreater(
                        floor["profile"]["pair_entropy"],
                        cell["real_profile"]["pair_entropy"],
                    )
                    self.assertLess(
                        floor["profile"]["top_1_share"],
                        cell["real_profile"]["top_1_share"],
                    )
                    self.assertLess(
                        floor["profile"]["empty_type_count"],
                        cell["real_profile"]["empty_type_count"],
                    )
                    self.assertGreater(
                        floor["profile"]["self_pair_share"],
                        cell["real_profile"]["self_pair_share"],
                    )

    def test_plaintext_controls(self) -> None:
        for (code, language), row in PLAIN.items():
            empty, self_share, top1, top50, entropy = row
            profile = self.artifact["files"][code][language][
                "plaintext_profile"
            ]
            self.assertEqual(profile["state_types"], 729)
            self.assertEqual(profile["total_pairs"], PLAIN_FULL[code])
            self.assertEqual(profile["empty_type_count"], empty)
            self.assertEqual(profile["self_pair_share"], self_share)
            self.assertEqual(profile["top_1_share"], top1)
            self.assertEqual(profile["top_50_share"], top50)
            self.assertEqual(profile["pair_entropy"], entropy)
            stored_free = self.frozen_search_free["files"][code][
                language
            ]["plaintext_profile"]
            self.assertEqual(profile, stored_free)
            stored_bm = self.frozen_boundary_mark["files"][code][
                language
            ]["plaintext_profile"]
            self.assertEqual(profile, stored_bm)

    def test_encodings_above_their_plaintext_sources(self) -> None:
        # Every simulated encoding's block entropy sits above its own
        # plaintext source's entropy, while the real's block entropy
        # sits below every simulated encoding in every cell, even
        # with the band widened to its twelve and eleven members.
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                plaintext_h = cell["plaintext_profile"]["pair_entropy"]
                for member in cell["members_profiles"]:
                    self.assertGreater(
                        member["profile"]["pair_entropy"], plaintext_h
                    )
                self.assertLess(
                    cell["real_profile"]["pair_entropy"],
                    min(
                        m["profile"]["pair_entropy"]
                        for m in cell["members_profiles"]
                    ),
                )

    def test_measured_direction(self) -> None:
        # The recorded direction of every outside invariant against
        # its widened band, the boundary-mark directions unchanged:
        # the real's entropy below the band in all six cells, its
        # top-k shares and its empty type count above the band
        # everywhere, its self-pair share above the band in the ZL
        # and IT cells, below it in the GC english cell, and inside
        # the widened band in the GC latin cell - the one invariant
        # the widened roster has not pushed out.
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
                    # The widened band's floor dropped below the
                    # boundary-mark band's floor, so the share sits
                    # deeper inside, not on the edge.
                    self.assertLess(
                        self_share["band_low"],
                        self.frozen_boundary_mark["files"][code][
                            language]["invariants"][
                            "self_pair_share"]["band_low"],
                    )

    def test_one_cell_recompute(self) -> None:
        fresh = homo._breadth_cell_facts("ZL", "english")
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
