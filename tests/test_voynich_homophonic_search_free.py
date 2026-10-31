"""Tests for the declared search-free invariant instrument of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute one full cell's facts from the declared kinds and the
standing streams and re-derive the bridge gate; the mechanical tests
nail the declared rules on the stored artifact: the constants, the
declaration strings (no assignment search anywhere, no split, no
score table, the strict-all verdict rule, no scalar margin), the
module docstring's declaration including the probe disclosures, the
profile arithmetic and the relabeling invariance on hand matrices,
the envelope arithmetic on hand profiles, the bridge gate (171
fields), the six headline verdicts, the vector outside counts, the
scalar band ranges and sorted envelope heads, the real profiles and
stream states, the band members' replays against the frozen
restart-budget artifact, the plants' source identity and the floors,
the plaintext controls, the one-cell recompute, the measured
direction of every outside invariant, and the dash bans. Nothing
here reads the manuscript beyond the frozen artifacts and the
declared streams.
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
    "docs/research-notes/voynich-homophonic-search-free.json"
).resolve()
FROZEN_RESTART = Path(
    "docs/research-notes/voynich-homophonic-restart-budget.json"
).resolve()

# The frozen artifact's headline, pinned from the artifact measured
# 23 October 2026 with the bridge gate verified at 171 fields: every
# cell is a shape-outside-analogue under the declared strict-all rule
# with every one of the eight invariant tests outside.
OUTSIDE_ALL = [
    "symbol_shares", "pair_shares", "empty_type_count",
    "self_pair_share", "top_1_share", "top_10_share",
    "top_50_share", "pair_entropy",
]

# (code, language) -> (symbol positions outside of 37,
# pair positions outside of 1369).
VECTOR_COUNTS = {
    ("ZL", "english"): (37, 902),
    ("ZL", "latin"): (34, 838),
    ("GC", "english"): (34, 904),
    ("GC", "latin"): (34, 854),
    ("IT", "english"): (37, 908),
    ("IT", "latin"): (36, 855),
}

# (code, language) -> the six scalar invariant tests as
# (real, band_low, band_high).
SCALARS = {
    ("ZL", "english"): {
        "empty_type_count": (943, 325, 447),
        "self_pair_share": (0.045162, 0.012192, 0.01645),
        "top_1_share": (0.066625, 0.021142, 0.028199),
        "top_10_share": (0.355937, 0.140788, 0.173894),
        "top_50_share": (0.859602, 0.414205, 0.443301),
        "pair_entropy": (4.203, 5.7732, 5.904914),
    },
    ("ZL", "latin"): {
        "empty_type_count": (943, 241, 510),
        "self_pair_share": (0.045162, 0.009823, 0.01644),
        "top_1_share": (0.066625, 0.021489, 0.034072),
        "top_10_share": (0.355937, 0.129611, 0.15643),
        "top_50_share": (0.859602, 0.341177, 0.378328),
        "pair_entropy": (4.203, 5.923406, 6.050813),
    },
    ("GC", "english"): {
        "empty_type_count": (645, 319, 454),
        "self_pair_share": (0.009722, 0.012367, 0.016764),
        "top_1_share": (0.078745, 0.021258, 0.028151),
        "top_10_share": (0.352327, 0.153069, 0.173159),
        "top_50_share": (0.789781, 0.413675, 0.443213),
        "pair_entropy": (4.500206, 5.778682, 5.922013),
    },
    ("GC", "latin"): {
        "empty_type_count": (645, 259, 507),
        "self_pair_share": (0.009722, 0.009893, 0.016417),
        "top_1_share": (0.078745, 0.021489, 0.034072),
        "top_10_share": (0.352327, 0.129711, 0.15643),
        "top_50_share": (0.789781, 0.341482, 0.378245),
        "pair_entropy": (4.500206, 5.923931, 6.050891),
    },
    ("IT", "english"): {
        "empty_type_count": (1012, 327, 446),
        "self_pair_share": (0.044039, 0.012221, 0.016664),
        "top_1_share": (0.067451, 0.021167, 0.028196),
        "top_10_share": (0.356453, 0.140865, 0.173894),
        "top_50_share": (0.867039, 0.414368, 0.443484),
        "pair_entropy": (4.180814, 5.772971, 5.905219),
    },
    ("IT", "latin"): {
        "empty_type_count": (1012, 242, 507),
        "self_pair_share": (0.044039, 0.009694, 0.016477),
        "top_1_share": (0.067451, 0.021489, 0.034072),
        "top_10_share": (0.356453, 0.129478, 0.15643),
        "top_50_share": (0.867039, 0.341288, 0.377911),
        "pair_entropy": (4.180814, 5.923107, 6.050902),
    },
}

# The sorted envelope's first recorded positions, per cell:
# (real, band_low, band_high) for symbol position 0 and
# pair position 0.
HEADS = {
    ("ZL", "english"): (
        (0.157027, 0.183123, 0.204027),
        (0.066625, 0.021142, 0.028199),
    ),
    ("ZL", "latin"): (
        (0.110643, 0.063247, 0.08061),
        (0.066625, 0.021489, 0.034072),
    ),
    ("GC", "english"): (
        (0.127681, 0.051846, 0.070437),
        (0.078745, 0.021258, 0.028151),
    ),
    ("GC", "latin"): (
        (0.194281, 0.142783, 0.160931),
        (0.078745, 0.021489, 0.034072),
    ),
    ("IT", "english"): (
        (0.165238, 0.18309, 0.203962),
        (0.067451, 0.021167, 0.028196),
    ),
    ("IT", "latin"): (
        (0.165238, 0.142783, 0.161737),
        (0.067451, 0.021489, 0.034072),
    ),
}

# code -> (stream events, unmapped events, kept pairs, empty types,
# self pair share, top shares at k 1, 10, 50, pair entropy), shared
# by both language cells of a code.
REAL = {
    "ZL": (218663, 126, 218415, 943, 0.045162,
           0.066625, 0.355937, 0.859602, 4.203),
    "GC": (186708, 1769, 183199, 645, 0.009722,
           0.078745, 0.352327, 0.789781, 4.500206),
    "IT": (220532, 0, 220531, 1012, 0.044039,
           0.067451, 0.356453, 0.867039, 4.180814),
}

# (code, language) -> the plaintext control's (empty types, self
# share, top_1 share, top_50 share, pair entropy), all on 729 types.
PLAIN = {
    ("ZL", "english"): (260, 0.019404, 0.033115, 0.567854, 5.139035),
    ("ZL", "latin"): (339, 0.013775, 0.026671, 0.569404, 5.06327),
    ("GC", "english"): (265, 0.019432, 0.033079, 0.568297, 5.139139),
    ("GC", "latin"): (342, 0.013631, 0.026544, 0.569647, 5.063406),
    ("IT", "english"): (260, 0.019439, 0.033079, 0.567712, 5.139068),
    ("IT", "latin"): (339, 0.01373, 0.026695, 0.56958, 5.062979),
}

# The band's member totals (sorted) and entropy range per cell.
MEMBERS = {
    ("ZL", "english"): ([218662] * 7, 5.7732, 5.904914),
    ("ZL", "latin"): ([45490, 77528, 77571, 132607, 143946,
                       218662, 218662, 218662], 5.923406, 6.050813),
    ("GC", "english"): ([186707] * 7, 5.778682, 5.922013),
    ("GC", "latin"): ([45490, 77528, 77571, 132607, 143946,
                       186707, 186707, 186707], 5.923931, 6.050891),
    ("IT", "english"): ([220531] * 7, 5.772971, 5.905219),
    ("IT", "latin"): ([45490, 77528, 77571, 132607, 143946,
                       220531, 220531, 220531], 5.923107, 6.050902),
}


class SearchFreeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_restart = json.loads(FROZEN_RESTART.read_text())
        self.declared = self.artifact["declared"]

    def test_declared_constants(self) -> None:
        self.assertEqual(homo.SEARCH_FREE_TOP_K, (1, 10, 50))
        self.assertEqual(homo.SEARCH_FREE_SHARES, 6)
        self.assertTrue(str(homo.SEARCH_FREE_ARTIFACT_PATH).endswith(
            "voynich-homophonic-search-free.json"
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
            {"status": "verified", "fields_compared": 171},
        )

    def test_the_search_free_declaration(self) -> None:
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
            "the instrument prices count structure only",
            self.declared["models_rule"],
        )
        self.assertIn(
            "declared strict-all", self.declared["verdict_rule"]
        )
        self.assertIn(
            "every declared invariant of the real's profile sits "
            "inside the closed range",
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
            "the six cells' counted pairs, all 45 members' file, "
            "ebook and plant_length records, and the 30 floors' pair "
            "totals",
            self.declared["bridge_gate"],
        )
        self.assertIn(
            "the plants' totals are verified inside every cell "
            "instead because their standing source lengths were "
            "never stored frozen",
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
        self.assertIn(
            "each member's profile is its selected draw's encoding "
            "replayed through the declared encoder and partition",
            self.declared["band_record_rule"],
        )
        self.assertIn(
            "membership unconditional exactly as declared before",
            self.declared["band_record_rule"],
        )
        self.assertIn(
            "a plants_at_source_identity boolean",
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
            "it takes no part in any envelope",
            self.declared["plaintext_rule"],
        )
        self.assertIn(
            "no new seed kind and no new position",
            self.declared["seed_kinds"],
        )
        self.assertIn(
            "byte-identical replay", self.declared["seed_sharing"]
        )
        self.assertIn(
            "so the latin envelopes are size-mixed by the roster's "
            "own declared construction",
            self.declared["state_note"],
        )

    def test_module_docstring_declaration(self) -> None:
        doc = " ".join(homo.__doc__.split())
        for phrase in (
            "no split - it prices",
            "declared invariant list, fixed in advance, every "
            "summary",
            "relabeling invariant of a pair-count matrix",
            "the top-k pair concentration at the declared k "
            "values 1, 10 and 50",
            "declared verdict rule, fixed in advance, "
            "strict-all",
            "No scalar margin is formed",
            "shape-outside-analogues, with every outside entry",
            "a miss is audited, not summarized",
            "probes' disclosed first-cell verdicts do not "
            "decide the artifact",
            "nothing here is a reading or a language claim",
            "the repaired gate ran at 171 fields compared, no "
            "problem",
            "Probe 1, the bridge gate rehearsed",
            "Probe 2, the real profiles ahead of the run",
            "Probe 3, the first cell's declared verdict ahead of "
            "the run, ZL english",
            "Probe 4, the plaintext controls recorded not tested",
            "Probe 5, the first latin cell's declared verdict "
            "ahead of the run, ZL latin",
            "Probe 6: none",
        ):
            self.assertIn(phrase, doc)
        self.assertEqual(
            " ".join(doc.split()).count(
                "nothing here is a reading or a language claim"
            ),
             19,
        )

    def test_the_truthful_question(self) -> None:
        what = self.artifact["what"]
        self.assertIn(
            "The declared truthful question: do the manuscript's "
            "raw pair profiles sit inside the range of the simulated "
            "encodings on every declared invariant in every (file, "
            "language) cell, or is at least one invariant outside",
            what,
        )
        self.assertIn(
            "No mapping is published; nothing here is a reading.",
            what,
        )
        self.assertIn(
            "using only relabeling-invariant summaries of the pair "
            "matrices, so that no number here passes through any "
            "assignment search",
            what,
        )

    def test_profile_facts_arithmetic(self) -> None:
        matrix = np.array(
            [[2, 1, 0], [1, 3, 0], [0, 0, 1]], dtype=np.int64
        )
        facts = homo._profile_facts(matrix)
        self.assertEqual(facts["total_pairs"], 8)
        self.assertEqual(facts["state_types"], 9)
        self.assertEqual(facts["symbol_counts"], [4, 3, 1])
        self.assertEqual(
            facts["symbol_shares"], [0.5, 0.375, 0.125]
        )
        self.assertEqual(
            facts["pair_counts"], [3, 2, 1, 1, 1, 0, 0, 0, 0]
        )
        self.assertEqual(facts["empty_type_count"], 4)
        self.assertEqual(facts["self_pair_share"], 0.75)
        self.assertEqual(facts["top_1_share"], 0.375)
        self.assertEqual(facts["top_10_share"], 1.0)
        self.assertEqual(facts["top_50_share"], 1.0)
        entropy = -(
            (3 / 8) * math.log(3 / 8)
            + (2 / 8) * math.log(2 / 8)
            + 3 * (1 / 8) * math.log(1 / 8)
        )
        self.assertEqual(facts["pair_entropy"], round(entropy, 6))

    def test_relabeling_invariance(self) -> None:
        matrix = np.array(
            [[2, 1, 0, 0], [1, 3, 0, 1], [0, 0, 1, 0], [0, 1, 0, 4]],
            dtype=np.int64,
        )
        permutation = [3, 0, 2, 1]
        relabeled = matrix[np.ix_(permutation, permutation)]
        self.assertTrue(
            np.array_equal(
                relabeled.sum(axis=1),
                matrix.sum(axis=1)[permutation],
            )
        )
        self.assertEqual(
            homo._profile_facts(matrix),
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
            self.assertLess(entry["position"], 37)
        exact = homo._search_free_envelope(
            member_a, member_facts
        )
        self.assertTrue(all(
            test["inside"] for test in exact.values()
        ))

    def test_bridge_gate(self) -> None:
        problems, fields = homo._compare_search_free_to_frozen()
        self.assertEqual(problems, [])
        self.assertEqual(fields, 171)
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
                self.assertEqual(
                    cell["outside_invariants"], OUTSIDE_ALL
                )
                self.assertEqual(
                    sorted(cell["invariants"]), sorted(OUTSIDE_ALL)
                )
                for key in OUTSIDE_ALL:
                    self.assertFalse(cell["invariants"][key]["inside"])

    def test_vector_outside_counts(self) -> None:
        for (code, language), (symbols, pairs) in VECTOR_COUNTS.items():
            cell = self.artifact["files"][code][language]
            share_out = cell["invariants"]["symbol_shares"]["outside"]
            pair_out = cell["invariants"]["pair_shares"]["outside"]
            self.assertEqual(len(share_out), symbols)
            self.assertEqual(len(pair_out), pairs)

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
                self.assertFalse(test["inside"])

    def test_sorted_envelope_heads(self) -> None:
        for (code, language), (sym0, pair0) in HEADS.items():
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
            self.assertEqual(
                (pair_entry["real"], pair_entry["band_low"],
                 pair_entry["band_high"]),
                pair0,
            )

    def test_real_profiles_and_streams(self) -> None:
        for code, row in REAL.items():
            events, unmapped, pairs, empty, self_share, top1, \
                top10, top50, entropy = row
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(cell["stream_events"], events)
                self.assertEqual(cell["unmapped_events"], unmapped)
                self.assertEqual(cell["kept_pairs"], pairs)
                profile = cell["real_profile"]
                self.assertEqual(profile["total_pairs"], pairs)
                self.assertEqual(profile["state_types"], 1369)
                self.assertEqual(profile["empty_type_count"], empty)
                self.assertEqual(
                    profile["self_pair_share"], self_share
                )
                self.assertEqual(profile["top_1_share"], top1)
                self.assertEqual(profile["top_10_share"], top10)
                self.assertEqual(profile["top_50_share"], top50)
                self.assertEqual(profile["pair_entropy"], entropy)

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
            frozen_band = self.frozen_restart["files"][code][
                language
            ]["band"]
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
                        plant["profile"]["total_pairs"],
                        plant["plant_length"] - 1,
                    )
                    self.assertEqual(
                        plant["plant_length"],
                        cell["standing_plant_length"],
                    )
                self.assertEqual(
                    cell["standing_plant_length"],
                    cell["stream_events"],
                )
                for floor in floors:
                    self.assertEqual(
                        floor["profile"]["total_pairs"],
                        cell["kept_pairs"],
                    )
                    # The floors' declared role is the destroyed
                    # control: shuffle puts the same total of pairs
                    # into a flatter structure than the real's in
                    # every cell - entropy above the real's, the
                    # top pair share below the real's, the empty
                    # type count below the real's and the self-pair
                    # share above the real's.
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
            self.assertEqual(profile["empty_type_count"], empty)
            self.assertEqual(profile["self_pair_share"], self_share)
            self.assertEqual(profile["top_1_share"], top1)
            self.assertEqual(profile["top_50_share"], top50)
            self.assertEqual(profile["pair_entropy"], entropy)

    def test_encodings_above_their_plaintext_sources(self) -> None:
        # The disclosed reading direction: every simulated encoding's
        # entropy sits above its own plaintext source's entropy,
        # while the real's entropy sits below every simulated
        # encoding in every cell.
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
        # The recorded direction of every outside invariant: the
        # real's entropy below the band everywhere, its top-k shares
        # and its empty type count above the band everywhere, and
        # its self-pair share above the band in the ZL and IT cells
        # while below it in the GC cells.
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
                    self.assertGreater(
                        self_share["real"],
                        self_share["band_high"],
                    )
                else:
                    self.assertLess(
                        self_share["real"],
                        self_share["band_low"],
                    )

    def test_one_cell_recompute(self) -> None:
        fresh = homo._search_free_cell_facts("ZL", "english")
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
