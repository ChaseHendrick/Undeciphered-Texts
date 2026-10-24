"""Tests for the declared boundary-mark re-instrument of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute one full cell's facts from the declared kinds and the
standing streams and re-derive the two-source bridge gate; the
mechanical tests nail the declared rules on the stored artifact: the
constants, the declaration strings (the mark's row and column excluded
from every profile on both sides, the alphabet-width disclosure, no
assignment search anywhere, no split, no score table, the strict-all
verdict rule, no scalar margin), the module docstring's declaration
including the probe disclosures, the block arithmetic and the
relabeling invariance on hand matrices, the envelope arithmetic on
hand profiles, the bridge gate (288 fields against the restart-budget
artifact's 171 anchors and the search-free artifact's 117 anchors),
the six headline verdicts, the vector outside counts, the scalar band
ranges and sorted envelope heads, the real block profiles and stream
states, the band members' replays against both frozen artifacts, the
plants' full-width source identity and the floors, the plaintext
controls unchanged against the search-free artifact, the one-cell
recompute, the measured direction of every outside invariant, and the
dash bans. Nothing here reads the manuscript beyond the frozen
artifacts and the declared streams.
"""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-boundary-mark.json"
).resolve()
FROZEN_RESTART = Path(
    "docs/research-notes/voynich-homophonic-restart-budget.json"
).resolve()
FROZEN_SEARCH_FREE = Path(
    "docs/research-notes/voynich-homophonic-search-free.json"
).resolve()

# The frozen artifact's headline, pinned from the artifact measured
# 23 October 2026 with the two-source bridge gate verified at 288
# fields: every cell is a shape-outside-analogue under the declared
# strict-all rule, with every one of the eight invariant tests outside
# except the GC latin cell's self-pair share, which entered the band
# when the mark's row and column left the state space, so seven of its
# eight invariant tests sit outside.
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
# pair positions outside of 1296).
VECTOR_COUNTS = {
    ("ZL", "english"): (35, 845),
    ("ZL", "latin"): (36, 784),
    ("GC", "english"): (36, 832),
    ("GC", "latin"): (33, 782),
    ("IT", "english"): (35, 846),
    ("IT", "latin"): (35, 788),
}

# (code, language) -> the six scalar invariant tests as
# (real, band_low, band_high); the inside flag is False everywhere
# except the GC latin cell's self_pair_share, which sits inside its
# band after the mark's exclusion.
SCALARS = {
    ("ZL", "english"): {
        "empty_type_count": (928, 323, 443),
        "self_pair_share": (0.065848, 0.020192, 0.026741),
        "top_1_share": (0.070481, 0.018196, 0.035886),
        "top_10_share": (0.424435, 0.111613, 0.132192),
        "top_50_share": (0.893671, 0.318571, 0.345689),
        "pair_entropy": (4.010179, 5.947039, 6.102864),
    },
    ("ZL", "latin"): {
        "empty_type_count": (928, 240, 503),
        "self_pair_share": (0.065848, 0.014311, 0.023974),
        "top_1_share": (0.070481, 0.017923, 0.02536),
        "top_10_share": (0.424435, 0.114705, 0.131916),
        "top_50_share": (0.893671, 0.300616, 0.336503),
        "pair_entropy": (4.010179, 5.980168, 6.104489),
    },
    ("GC", "english"): {
        "empty_type_count": (642, 317, 450),
        "self_pair_share": (0.015928, 0.020415, 0.027257),
        "top_1_share": (0.051049, 0.018404, 0.035019),
        "top_10_share": (0.373572, 0.112634, 0.126179),
        "top_50_share": (0.8066, 0.31784, 0.344427),
        "pair_entropy": (4.422831, 5.949604, 6.117306),
    },
    ("GC", "latin"): {
        "empty_type_count": (642, 258, 500),
        "self_pair_share": (0.015928, 0.014518, 0.023941),
        "top_1_share": (0.051049, 0.017923, 0.02536),
        "top_10_share": (0.373572, 0.11386, 0.133218),
        "top_50_share": (0.8066, 0.300645, 0.33872),
        "pair_entropy": (4.422831, 5.98016, 6.104621),
    },
    ("IT", "english"): {
        "empty_type_count": (984, 325, 442),
        "self_pair_share": (0.065777, 0.020243, 0.027087),
        "top_1_share": (0.071689, 0.018068, 0.035914),
        "top_10_share": (0.429316, 0.111791, 0.13184),
        "top_50_share": (0.89868, 0.3186, 0.345915),
        "pair_entropy": (3.980621, 5.947066, 6.102609),
    },
    ("IT", "latin"): {
        "empty_type_count": (984, 241, 500),
        "self_pair_share": (0.065777, 0.014124, 0.024029),
        "top_1_share": (0.071689, 0.017923, 0.02536),
        "top_10_share": (0.429316, 0.11467, 0.131821),
        "top_50_share": (0.89868, 0.300304, 0.336358),
        "pair_entropy": (3.980621, 5.980406, 6.104582),
    },
}

# (code, language) -> the sorted symbol envelope's first recorded
# entry (real, band_low, band_high); the sorted pair envelope's first
# entry equals the cell's top_1_share test.
HEADS = {
    ("ZL", "english"): (0.155542, 0.076105, 0.085511),
    ("ZL", "latin"): (0.155542, 0.087023, 0.099429),
    ("GC", "english"): (0.19975, 0.076457, 0.084691),
    ("GC", "latin"): (0.19975, 0.086553, 0.099429),
    ("IT", "english"): (0.158109, 0.07601, 0.085601),
    ("IT", "latin"): (0.158109, 0.087023, 0.099429),
}

# code -> (stream events, unmapped events, kept pairs, boundary
# carried pairs, block pairs, block empty types, block self pair
# share, top shares at k 1, 10, 50, block pair entropy, the mark's
# own position in the real alphabet, the real alphabet's width),
# shared by both language cells of a code.
REAL = {
    "ZL": (218663, 126, 218415, 68616, 149799, 928, 0.065848,
           0.070481, 0.424435, 0.893671, 4.010179, 36, 37),
    "GC": (186708, 1769, 183199, 71384, 111815, 642, 0.015928,
           0.051049, 0.373572, 0.8066, 4.422831, 36, 37),
    "IT": (220532, 0, 220531, 72880, 147651, 984, 0.065777,
           0.071689, 0.429316, 0.89868, 3.980621, 23, 24),
}

# (code, language) -> the band's member block totals (sorted) and
# the block entropy range per cell.
MEMBERS = {
    ("ZL", "english"): ([129435, 131621, 132035, 132718, 134514,
                         135954, 138578], 5.947039, 6.102864),
    ("ZL", "latin"): ([31635, 53244, 54089, 90930, 102839, 147874,
                       153490, 155874], 5.980168, 6.104489),
    ("GC", "english"): ([110409, 112325, 113101, 113509, 114833,
                         116381, 118135], 5.949604, 6.117306),
    ("GC", "latin"): ([31635, 53244, 54089, 90930, 102839, 126612,
                       131179, 133021], 5.98016, 6.104621),
    ("IT", "english"): ([130570, 132719, 133131, 133884, 135675,
                         137083, 139777], 5.947066, 6.102609),
    ("IT", "latin"): ([31635, 53244, 54089, 90930, 102839, 149195,
                       154783, 157213], 5.980406, 6.104582),
}

# (code, language) -> the five plants' block totals (one shared
# number per cell) and the five floors' block totals (sorted),
# with the standing sources' full-width totals beside them:
# plant_full (per code) and each floor's full width equals the
# cell's kept pairs.
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
# and all unchanged from the search-free artifact.
PLAIN = {
    ("ZL", "english"): (260, 0.019404, 0.033115, 0.567854, 5.139035),
    ("ZL", "latin"): (339, 0.013775, 0.026671, 0.569404, 5.06327),
    ("GC", "english"): (265, 0.019432, 0.033079, 0.568297, 5.139139),
    ("GC", "latin"): (342, 0.013631, 0.026544, 0.569647, 5.063406),
    ("IT", "english"): (260, 0.019439, 0.033079, 0.567712, 5.139068),
    ("IT", "latin"): (339, 0.01373, 0.026695, 0.56958, 5.062979),
}
PLAIN_FULL = {"ZL": 218662, "GC": 186707, "IT": 220531}


class BoundaryMarkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_restart = json.loads(FROZEN_RESTART.read_text())
        self.frozen_search_free = json.loads(
            FROZEN_SEARCH_FREE.read_text()
        )
        self.declared = self.artifact["declared"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.SEARCH_FREE_TOP_K, (1, 10, 50))
        self.assertEqual(homo.SEARCH_FREE_SHARES, 6)
        self.assertTrue(str(homo.SEARCH_FREE_BM_ARTIFACT_PATH).endswith(
            "voynich-homophonic-boundary-mark.json"
        ))
        self.assertEqual(self.declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(self.declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(self.declared["corpus_facts"], {})
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
            {"status": "verified", "fields_compared": 288},
        )

    def test_the_boundary_mark_declaration(self) -> None:
        self.assertIn(
            "the word-boundary mark is each side's own mapped "
            "alphabet's last position",
            self.declared["boundary_rule"],
        )
        self.assertIn(
            "its symbol's row and column are excluded from every "
            "profile's state space on both sides",
            self.declared["boundary_rule"],
        )
        self.assertIn(
            "the IT real transcription's glyph inventory holds only "
            "23 ranked glyph types plus the mark",
            self.declared["boundary_rule"],
        )
        self.assertIn(
            "13 of the block's 36 glyph slots are empty by alphabet "
            "width alone on the real side",
            self.declared["boundary_rule"],
        )
        self.assertIn(
            "no boundary-adjusted marginal appears anywhere",
            self.declared["boundary_rule"],
        )
        self.assertIn(
            "13 of its block's 36 glyph slots are empty by width "
            "alone while the simulated alphabets are saturated at "
            "36 in every cell",
            self.declared["state_note"],
        )
        self.assertIn(
            "so the latin envelopes are size-mixed by the roster's "
            "own declared construction",
            self.declared["state_note"],
        )
        self.assertIn(
            "envelope-tested by sorted position over 36 positions",
            self.declared["invariants"]["sorted_symbol_marginals"],
        )
        self.assertIn(
            "the natural entropy of the mark-excluded pair "
            "distribution over the 1296 types",
            self.declared["invariants"]["pair_entropy"],
        )
        self.assertIn(
            "no assignment search anywhere: no candidate evaluation, "
            "no restarts, no sweep cap, no convergence flags",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "the standing budgets are not applicable",
            self.declared["machinery_rule"],
        )
        self.assertIn(
            "no split applies", self.declared["split_rule"]
        )
        self.assertIn(
            "the climb and score halves of the band instruments have "
            "no counterpart here",
            self.declared["split_rule"],
        )
        self.assertIn(
            "no score table is built or used",
            self.declared["models_rule"],
        )
        self.assertIn(
            "no new seed kind and no new position",
            self.declared["seed_kinds"],
        )
        self.assertIn(
            "byte-identical replay", self.declared["seed_sharing"]
        )
        self.assertIn(
            "then reduced to its glyph block",
            self.declared["band_record_rule"],
        )
        self.assertIn(
            "membership unconditional exactly as declared before",
            self.declared["band_record_rule"],
        )
        self.assertIn(
            "checking every plant's full-width total equals its "
            "source length minus one",
            self.declared["plants_rule"],
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
            "its state width differs by declaration and it takes no "
            "part in any envelope",
            self.declared["plaintext_rule"],
        )
        self.assertIn(
            "declared strict-all", self.declared["verdict_rule"]
        )
        self.assertIn(
            "every declared invariant of the real's glyph-block "
            "profile sits inside the closed range",
            self.declared["verdict_rule"],
        )
        self.assertIn(
            "any outside invariant makes the cell "
            "shape-outside-analogues",
            self.declared["verdict_rule"],
        )
        self.assertIn(
            "so the miss is audited not summarized",
            self.declared["verdict_rule"],
        )
        self.assertIn(
            "no scalar margin is formed",
            self.declared["closure_rule"],
        )
        self.assertIn(
            "the recorded distances are the outside entries' band "
            "ranges themselves",
            self.declared["closure_rule"],
        )
        self.assertIn(
            "the restart-budget artifact's 171 anchor fields exactly "
            "as the search-free instrument declared them",
            self.declared["bridge_gate"],
        )
        self.assertIn(
            "the frozen search-free artifact's 117 anchor fields",
            self.declared["bridge_gate"],
        )
        self.assertIn(
            "the plants' full-width identities are verified inside "
            "every cell as well",
            self.declared["bridge_gate"],
        )
        self.assertIn(
            "the selected-draw indexes are read, not re-derived",
            self.declared["bridge_gate"],
        )
        self.assertIn(
            "any divergence aborts with nothing written",
            self.declared["bridge_gate"],
        )
        self.assertIn(
            "not re-scoped", self.declared["exclusion_rule"]
        )
        self.assertIn(
            "the band instruments' verdicts stand untouched",
            self.declared["exclusion_rule"],
        )

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "Eleventh declared measurement, the boundary-mark "
            "re-instrument",
            "the word-boundary mark's symbol's row and column are "
            "excluded from every profile's state space on both sides",
            "the alphabet width is a standing disclosed fact",
            "do the search-free outsides ride the mark's own "
            "concentration, or does the interior pair structure miss "
            "of itself",
            "the mark's own self-pair count riding in the removed "
            "carried mass and disclosed at zero in the real's counts "
            "ahead of the run",
            "Probe 1, the bridge gate rehearsed",
            "the gate ran at 288 fields compared, no problem",
            "Probe 2, the boundary mass ahead of the run",
            "its transcription's glyph inventory holds only 23 "
            "ranked glyph types",
            "Probe 3, the first cell's declared verdict ahead of "
            "the run, ZL english",
            "symbol_shares 35 of 36 sorted positions outside",
            "Probe 4, the first latin cell's declared verdict "
            "ahead of the run, ZL latin",
            "Probe 5, the plaintext control recorded unchanged",
            "Probe 6: none",
            "probes' disclosed first-cell verdicts do not "
            "decide the artifact",
            "the family's declared exclusion format is not "
            "re-scoped by this artifact",
            "nothing here is a reading or a language claim",
        ):
            self.assertIn(phrase, doc)
        self.assertEqual(
            " ".join(doc.split()).count(
                "nothing here is a reading or a language claim"
            ),
            11,
        )

    def test_the_truthful_question(self) -> None:
        what = self.artifact["what"]
        self.assertIn(
            "with the boundary mark excluded on both sides, do the "
            "manuscript's remaining raw pair profiles sit inside the "
            "range of the simulated encodings' remaining profiles on "
            "every declared invariant in every (file, language) "
            "cell, or is at least one invariant outside",
            what,
        )
        self.assertIn(
            "the measured test of whether the search-free "
            "instrument's outsides ride the boundary mark's own "
            "concentration or the interior pair structure",
            what,
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
        self.assertEqual(block_last.shape, (4, 4))
        self.assertEqual(
            homo._boundary_carried_pairs(matrix, 4), 7
        )
        # A short-alphabet-shaped 37 by 37 matrix: the mark at
        # position 23 like the IT files, 24 to 36 empty, and the
        # block keeps 1296 ordered types of which 12 glyph slots
        # are all zero.
        wide = np.zeros((37, 37), dtype=np.int64)
        for i in range(24):
            for j in range(24):
                wide[i, j] = ((i * 7 + j) % 5) + 1
        block_wide = homo._glyph_block_matrix(wide, 23)
        self.assertEqual(block_wide.shape, (36, 36))
        self.assertEqual(int(block_wide.sum()), 1586)
        self.assertEqual(
            homo._boundary_carried_pairs(wide, 23), 142
        )
        marginals = block_wide.sum(axis=1)
        self.assertEqual(
            int((marginals == 0).sum()), 13
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
        for entry in record["symbol_shares"]["outside"]:
            self.assertEqual(
                sorted(entry), ["band_high", "band_low", "position",
                                "real"]
            )
            self.assertGreaterEqual(entry["position"], 0)
            self.assertLess(
                entry["position"], len(real["symbol_counts"])
            )
        exact = homo._search_free_envelope(
            member_a, member_facts
        )
        self.assertTrue(all(
            test["inside"] for test in exact.values()
        ))

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_search_free_bm_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 288)
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
        for (code, language), (totals, low, high) in MEMBERS.items():
            cell = self.artifact["files"][code][language]
            members = cell["members_profiles"]
            self.assertEqual(
                len(members),
                7 if language == "english" else 8,
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
            for position, member in enumerate(members):
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
                    # The floors' declared role is the destroyed
                    # control: the shuffled structure stays flatter
                    # than the real's block in every cell - entropy
                    # above the real's, the top pair share below the
                    # real's, the empty type count below the real's
                    # and the self-pair share above the real's.
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
            stored = self.frozen_search_free["files"][code][
                language
            ]["plaintext_profile"]
            self.assertEqual(profile, stored)

    def test_encodings_above_their_plaintext_sources(self) -> None:
        # The disclosed reading direction after the mark's exclusion:
        # every simulated encoding's block entropy sits above its own
        # plaintext source's entropy, while the real's block entropy
        # sits below every simulated encoding in every cell.
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
        # The recorded direction of every outside invariant after the
        # mark's exclusion: the real's entropy below the band in all
        # six cells, its top-k shares and its empty type count above
        # the band everywhere, its self-pair share above the band in
        # the ZL and IT cells, below it in the GC english cell, and
        # inside the band in the GC latin cell - the one invariant
        # that entered the band when the mark left the state space.
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
                    self.assertGreaterEqual(
                        self_share["real"], self_share["band_low"]
                    )
                    self.assertLessEqual(
                        self_share["real"], self_share["band_high"]
                    )

    def test_one_cell_recompute(self) -> None:
        fresh = homo._search_free_bm_cell_facts("ZL", "english")
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
