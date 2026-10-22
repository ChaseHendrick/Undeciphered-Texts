"""Tests for the declared block-fold split of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute one top-rung real cell from kind 1 and one band member's
first draw from kinds 28 and 29 under the declared block split; the
mechanical tests nail the declared rules on the stored artifact: the
block split rule, the bridge gate (60 fields), the models block, the
streams byte-identical to the frozen held-out measurement, the roll-up
(margins as arithmetic, verdict rule, floor positions, plant parity,
cap flags, selected draws with exact climbs, recomputed anchors), the
margins widening against the frozen shape measurement, the declared
question, and the dash bans. Nothing here reads the manuscript beyond
the frozen artifacts and the declared streams.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-block-fold.json"
).resolve()
FROZEN_SHAPE = Path(
    "docs/research-notes/voynich-homophonic-shape-priced.json"
).resolve()

# The frozen block-fold artifact's headline (code, language) ->
# (real_held, real_climb, real_full, band_min, band_max, margin,
# verdict, anchor), pinned from the artifact measured 21 October 2026
# with the bridge gate verified at 60 fields.
FROZEN = {
    ("ZL", "english"): (-4.4245, -4.4431, -4.444, -4.7368, -4.6341,
                        0.3123, "consistent-with-substitution", -5.1397),
    ("ZL", "latin"): (-4.3724, -4.387, -4.3786, -4.614, -4.5825,
                      0.2416, "consistent-with-substitution", -5.0686),
    ("IT", "english"): (-4.3735, -4.4071, -4.3897, -4.7366, -4.6354,
                        0.3631, "consistent-with-substitution", -5.1398),
    ("IT", "latin"): (-4.3672, -4.3798, -4.3733, -4.6079, -4.5753,
                      0.2407, "consistent-with-substitution", -5.0681),
    ("GC", "english"): (-4.3421, -4.3644, -4.3532, -4.7012, -4.6373,
                        0.3591, "consistent-with-substitution", -5.1436),
    ("GC", "latin"): (-4.4002, -4.4199, -4.3898, -4.6079, -4.5825,
                      0.2077, "consistent-with-substitution", -5.0658),
}

# Each frozen cell's counted pairs and the block halves.
COUNTED = {("ZL", "english"): 218415, ("ZL", "latin"): 218415,
           ("IT", "english"): 220531, ("IT", "latin"): 220531,
           ("GC", "english"): 183199, ("GC", "latin"): 183199}


class BlockFoldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_shape = json.loads(FROZEN_SHAPE.read_text())

    def test_declared_constants_and_no_new_seed_kinds(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(declared["restarts"], homo.N_RESTARTS)
        self.assertEqual(declared["sweep_cap"], homo.SWEEP_CAP)
        self.assertEqual(declared["plants_per_cell"], homo.N_PLANTS)
        self.assertEqual(declared["floors"], homo.N_FLOORS)
        self.assertEqual(
            declared["seed_kinds"],
            self.frozen_shape["declared"]["seed_kinds"],
        )
        self.assertEqual(
            declared["seed_kinds"],
            {
                "real": homo.KIND_ID["real"],
                "homo_plant": [homo.KIND_ID["homo_plant_enc"],
                               homo.KIND_ID["homo_plant_mach"]],
                "homo_floor": [homo.KIND_ID["homo_floor_perm"],
                               homo.KIND_ID["homo_floor_mach"]],
                "homo_cross": [homo.KIND_ID["homo_cross_enc"],
                               homo.KIND_ID["homo_cross_mach"]],
            },
        )

    def test_the_block_split_rule(self) -> None:
        first = np.arange(9, dtype=np.int64)
        second = np.arange(1, 10, dtype=np.int64)
        cf, cs, sf, ss = homo._block_pairs(first, second)
        self.assertEqual(len(cf), 4)
        self.assertEqual(len(sf), 5)
        np.testing.assert_array_equal(cf, np.arange(4))
        np.testing.assert_array_equal(sf, np.arange(4, 9))
        self.assertEqual(len(cf) + len(sf), len(first))
        self.assertEqual(int(cf.max()), int(sf.min()) - 1)
        for split in (homo._block_pairs(first, second),
                      homo._block_pairs(first, second)):
            self.assertTrue(
                np.all(split[2][:-1] + 2 != split[2][1:])
                or len(split[2]) == 1
            )
        even_first = np.arange(10, dtype=np.int64)
        even_second = np.arange(1, 11, dtype=np.int64)
        cf, cs, sf, ss = homo._block_pairs(even_first, even_second)
        self.assertEqual(len(cf), 5)
        self.assertEqual(len(sf), 5)
        declared = self.artifact["declared"]
        self.assertIn("the first floor(N/2) pairs the climb half",
                      declared["split_rule"])
        self.assertIn("the remaining pairs the score half",
                      declared["split_rule"])
        self.assertIn("for an odd count the climb half takes the "
                      "smaller first block", declared["split_rule"])

    def test_the_bridge_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["bridge_gate"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 60)
        self.assertIn("field for field",
                      self.artifact["declared"]["bridge_gate"])
        self.assertIn("pair-index-parity",
                      self.artifact["declared"]["bridge_gate"])

    def test_the_models_block_carries_the_block_facts(self) -> None:
        for language in LANGS:
            stream = homo._reference_stream(language)
            model = homo._shape_table(language)
            table = model["table"]
            full = homo._stream_matrix_27(stream)
            stored = self.artifact["declared"]["models"][language]
            clean = float((full * table).sum()) / float(full.sum())
            block_held, block_climb, _bcp, _bsp = (
                homo._block_identity_half_means(stream, table)
            )
            add_mean, _acm, _acp, _asp = homo._identity_half_means(
                stream, model["add_one_table"]
            )
            self.assertEqual(
                stored["clean_identity_mean_nats_per_pair"],
                round(clean, 4),
            )
            self.assertEqual(
                stored["block_climb_half_mean_nats_per_pair"],
                round(block_climb, 4),
            )
            self.assertEqual(
                stored["block_score_half_mean_nats_per_pair"],
                round(block_held, 4),
            )
            self.assertEqual(
                stored["add_one_parity_score_half_mean_nats_per_pair"],
                round(add_mean, 4),
            )

    def test_the_headline_numbers_match_the_freeze(self) -> None:
        for (code, language), frozen in FROZEN.items():
            cell = self.artifact["files"][code][language]
            (real, climb, full, band_min, band_max, margin, verdict,
             anchor) = frozen
            self.assertEqual(cell["real_held_mean_nats"], real)
            self.assertEqual(cell["real_climb_mean_nats"], climb)
            self.assertEqual(
                cell["real_full_exact_mean_nats"], full, (code, language)
            )
            self.assertEqual(cell["band_min"], band_min)
            self.assertEqual(cell["band_max"], band_max)
            self.assertEqual(cell["real_margin_over_band_min"], margin)
            self.assertEqual(cell["verdict"], verdict)
            self.assertEqual(
                cell["plant_parity_anchor_mean_nats"], anchor,
                (code, language),
            )

    def test_block_margins_widen_over_the_parity_margins(self) -> None:
        for code in FILES:
            for language in LANGS:
                block_margin = (
                    self.artifact["files"][code][language]
                    ["real_margin_over_band_min"]
                )
                shape_margin = (
                    self.frozen_shape["files"][code][language]
                    ["real_margin_over_band_min"]
                )
                self.assertGreaterEqual(
                    block_margin, shape_margin, (code, language)
                )
                residual = block_margin - shape_margin
                self.assertGreaterEqual(residual, 0.003)
                self.assertLessEqual(residual, 0.06)

    def test_margins_are_arithmetic_on_the_stored_values(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(
                    cell["real_margin_over_band_min"],
                    round(cell["real_held_mean_nats"] - cell["band_min"], 4),
                )

    def test_the_verdict_rule_holds_under_the_block_fold(self) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "do not restate the parity split's verdicts",
            declared["verdict_rule"],
        )
        self.assertIn("not re-scoped", declared["exclusion_rule"])
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                floor_max = max(cell["floors_held_mean_nats"])
                if cell["real_held_mean_nats"] >= cell["band_min"]:
                    verdict = "consistent-with-substitution"
                elif cell["real_held_mean_nats"] <= floor_max:
                    verdict = "not-consistent"
                else:
                    verdict = "below-held-band"
                self.assertEqual(cell["verdict"], verdict)

    def test_every_floor_stays_below_the_real(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                floor_max = max(cell["floors_held_mean_nats"])
                self.assertLess(
                    floor_max, cell["real_held_mean_nats"],
                    (code, language),
                )
                self.assertGreaterEqual(
                    round(cell["real_held_mean_nats"] - floor_max, 4), 0.75,
                    (code, language),
                )

    def test_the_plant_parity_rule_holds(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                anchor = cell["plant_parity_anchor_mean_nats"]
                self.assertTrue(all(cell["self_plants_at_parity"]))
                excesses = [
                    round(value - anchor, 4)
                    for value in cell["self_plants_held_mean_nats"]
                    if value > anchor + 0.0001
                ]
                self.assertEqual(
                    cell["machinery_above_anchor_excesses"], excesses,
                    (code, language),
                )
                for excess in excesses:
                    self.assertGreater(excess, 0.38)
                    self.assertLess(excess, 0.50)

    def test_no_machinery_call_hits_the_cap_anywhere(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                flags = (
                    [cell["real_sweep_budget_hit"]]
                    + [cell["real_full_sweep_budget_hit"]]
                    + cell["self_plants_sweep_budget_hits"]
                    + cell["self_plants_full_sweep_budget_hits"]
                    + cell["floors_sweep_budget_hits"]
                    + cell["floors_full_sweep_budget_hits"]
                )
                for member in cell["band"]:
                    flags = flags + member["draw_sweep_budget_hits"]
                    flags = flags + member["draw_full_sweep_budget_hits"]
                self.assertFalse(any(flags), (code, language))

    def test_the_selected_draw_rule_holds_everywhere(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                for member in cell["band"]:
                    climbs = member["draws_climb_exact"]
                    self.assertEqual(
                        len(climbs), len(member["draws"]),
                        (code, language, member["file"]),
                    )
                    best = climbs[0]
                    selected = 0
                    for position, value in enumerate(climbs):
                        if value > best + 1e-12:
                            best = value
                            selected = position
                    self.assertEqual(
                        member["selected_draw_index"], selected,
                        (code, language, member["file"]),
                    )
                    self.assertEqual(
                        member["recovered_best"],
                        member["draws"][selected],
                    )
                    for rounded, exact in zip(
                        member["draws_climb"], climbs
                    ):
                        self.assertEqual(round(exact, 4), rounded)
                    self.assertEqual(
                        member["spread"],
                        round(max(member["draws"]) - min(member["draws"]),
                              4),
                    )

    def test_the_streams_are_the_frozen_streams(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(cell["counted_pairs"],
                                 COUNTED[(code, language)])
                self.assertEqual(
                    cell["climb_pairs"] + cell["score_pairs"],
                    cell["counted_pairs"],
                )
                self.assertEqual(
                    cell["counted_pairs"],
                    self.frozen_shape["files"][code][language][
                        "counted_pairs"
                    ],
                )

    def test_anchors_recompute_under_the_block_fold(self) -> None:
        code, language = "ZL", "english"
        model = homo._shape_table(language)
        truncated = homo._truncated_reference(code, language)
        anchor, anchor_climb, _cp, _sp = (
            homo._block_identity_half_means(truncated, model["table"])
        )
        cell = self.artifact["files"][code][language]
        self.assertEqual(
            cell["plant_parity_anchor_mean_nats"], round(anchor, 4)
        )
        self.assertEqual(
            cell["plant_climb_identity_mean_nats"], round(anchor_climb, 4)
        )
        shape_cell = self.frozen_shape["files"][code][language]
        self.assertGreater(
            round(anchor, 4),
            shape_cell["plant_parity_anchor_mean_nats"] - 0.001,
        )

    def test_one_top_rung_real_recomputes_under_the_block_split(
        self,
    ) -> None:
        code, language = "ZL", "english"
        model = homo._shape_table(language)
        stream = homo._homo_real_stream(code)
        first, second = homo._kept_pairs(
            stream["event_ids"], stream["kept_mask"]
        )
        climb_first, climb_second, score_first, score_second = (
            homo._block_pairs(first, second)
        )
        climb = homo._matrix_from_pairs(climb_first, climb_second)
        score = homo._matrix_from_pairs(score_first, score_second)
        rng = np.random.default_rng(
            homo._seed(
                homo.CELL_ID[code], homo.KIND_ID["real"],
                homo.LANG_ID[language], 0,
            )
        )
        held, view, hit = homo.machinery_best_held(
            climb, score, model["table"], model["letter_counts"], rng,
            restarts=homo.N_RESTARTS,
        )
        cell = self.artifact["files"][code][language]
        self.assertFalse(hit)
        self.assertEqual(round(held, 4), cell["real_held_mean_nats"])
        self.assertEqual(cell["real_held_mean_nats"], -4.4245)
        self.assertEqual(round(view, 4), cell["real_climb_mean_nats"])
        self.assertEqual(cell["counted_pairs"], 218415)
        self.assertEqual(cell["climb_pairs"], 109207)
        self.assertEqual(cell["score_pairs"], 109208)

    def test_one_band_first_draw_replays_under_the_block_split(
        self,
    ) -> None:
        code, language, seed_index = "ZL", "english", 0
        model = homo._shape_table(language)
        name = homo.CROSS_REFERENCE_FILES[language][0]
        truncated = homo._truncated_reference(code, language, file=name)
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            homo._seed(
                homo.CELL_ID[code], homo.KIND_ID["homo_cross_enc"],
                homo.LANG_ID[language], seed_index,
            )
        )
        encoded = homo._encode(truncated, groups, rng_enc, homo.MAPPED_HOMO)
        enc_first, enc_second = homo._full_pairs(encoded)
        e_climb_first, e_climb_second, e_score_first, e_score_second = (
            homo._block_pairs(enc_first, enc_second)
        )
        e_climb = homo._matrix_from_pairs(e_climb_first, e_climb_second)
        e_score = homo._matrix_from_pairs(e_score_first, e_score_second)
        rng_mach = np.random.default_rng(
            homo._seed(
                homo.CELL_ID[code], homo.KIND_ID["homo_cross_mach"],
                homo.LANG_ID[language], seed_index,
            )
        )
        held, _view, hit = homo.machinery_best_held(
            e_climb, e_score, model["table"], model["letter_counts"],
            rng_mach, restarts=homo.N_RESTARTS,
        )
        self.assertFalse(hit)
        member = (
            self.artifact["files"][code][language]["band"][seed_index]
        )
        self.assertEqual(round(held, 4), member["draws"][0])
        self.assertEqual(member["draws"][0], -4.7368)
        self.assertEqual(member["file"], name)

    def test_the_declared_question_is_answered_in_the_artifact(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's held-out score-half value still stand above "
            "the band when the scored pairs are fresh to the search in "
            "the span sense",
            declared["truthful_question"],
        )
        self.assertIn(
            "the parity geometry's interleaving",
            declared["truthful_question"],
        )
        self.assertIn(
            "draws_climb_exact", declared["band_record_rule"]
        )
        self.assertIn(
            "byte-identical replays", declared["measured_facts_rule"]
        )
        self.assertIn(
            "carried forward unchanged", declared["loo_rule"]
        )

    def test_no_mapping_is_published(self) -> None:
        self.assertIn(
            "No mapping is published", self.artifact["what"]
        )
        self.assertIn(
            "nothing here is a reading", self.artifact["what"]
        )
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertNotIn("mapping", json.dumps(cell))
                self.assertNotIn("plaintext_recovered", json.dumps(cell))

    def test_no_dash_in_the_artifact_or_the_module(self) -> None:
        text = ARTIFACT.read_text()
        self.assertNotIn("\u2013", text)
        self.assertNotIn("\u2014", text)
        module = Path(homo.__file__).read_text()
        self.assertNotIn("\u2013", module)
        self.assertNotIn("\u2014", module)


if __name__ == "__main__":
    unittest.main()
