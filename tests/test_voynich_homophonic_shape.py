"""Tests for the declared shape-priced re-measure of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute one top-rung real cell from kind 1 and one band member's
first draw from kinds 28 and 29 under the declared leave-one-out
table; the mechanical tests nail the declared rules on the stored
artifact: the leave-one-out formula and its facts, the bridge gate
(57 fields), the models block, the streams byte-identical to the
frozen held-out measurement, the roll-up (margins as arithmetic,
verdict rule, floor positions, plant parity, cap flags, selected
draws with exact climbs, recomputed anchors), the declared answer,
and the dash bans. Nothing here reads the manuscript beyond the
frozen artifacts and the declared streams.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-shape-priced.json"
).resolve()
FROZEN_HELD = Path(
    "docs/research-notes/voynich-homophonic-heldout.json"
).resolve()

# The frozen leave-one-out artifact's headline (code, language) ->
# (real_held, real_climb, real_full, band_min, band_max, margin,
# verdict, anchor), pinned from the artifact measured 21 October 2026
# with the bridge gate verified at 57 fields.
FROZEN = {
    ("ZL", "english"): (-4.4256, -4.4317, -4.444, -4.6999, -4.6714,
                        0.2743, "consistent-with-substitution", -5.1438),
    ("ZL", "latin"): (-4.3744, -4.3828, -4.3786, -4.6082, -4.5789,
                      0.2338, "consistent-with-substitution", -5.076),
    ("IT", "english"): (-4.388, -4.3914, -4.3897, -4.6994, -4.6357,
                        0.3114, "consistent-with-substitution", -5.1439),
    ("IT", "latin"): (-4.3709, -4.3758, -4.3733, -4.6082, -4.5789,
                      0.2373, "consistent-with-substitution", -5.0757),
    ("GC", "english"): (-4.3539, -4.3535, -4.3532, -4.6991, -4.6364,
                        0.3452, "consistent-with-substitution", -5.1451),
    ("GC", "latin"): (-4.4035, -4.4077, -4.3898, -4.6082, -4.5789,
                      0.2047, "consistent-with-substitution", -5.0765),
}


class ShapePricedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_held = json.loads(FROZEN_HELD.read_text())

    def test_declared_constants_and_no_new_seed_kinds(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(declared["restarts"], homo.N_RESTARTS)
        self.assertEqual(declared["sweep_cap"], homo.SWEEP_CAP)
        self.assertEqual(declared["plants_per_cell"], homo.N_PLANTS)
        self.assertEqual(declared["floors"], homo.N_FLOORS)
        held_kinds = self.frozen_held["declared"]["seed_kinds"]
        self.assertEqual(declared["seed_kinds"], held_kinds)
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

    def test_the_loo_table_matches_the_declared_formula(self) -> None:
        for language in LANGS:
            model = homo._shape_table(language)
            table = model["table"]
            add_one, letter_counts = homo.table_from_stream(
                homo._reference_stream(language)
            )
            ids = np.array(homo._reference_stream(language), dtype=np.int64)
            counts = np.zeros((27, 27))
            np.add.at(counts, (ids[:-1], ids[1:]), 1.0)
            total = int(counts.sum())
            self.assertEqual(model["total_pairs"], total)
            self.assertEqual(model["pair_types_present"],
                             int((counts >= 1).sum()))
            present = counts >= 1
            np.testing.assert_array_equal(
                table[present],
                np.log(counts[present] / float(total + 728.0)),
            )
            np.testing.assert_array_equal(
                table[~present],
                np.log(np.ones((~present).sum()) / float(total + 729.0)),
            )
            self.assertFalse(np.any(table[present] >= add_one[present]))
            np.testing.assert_array_equal(
                letter_counts, model["letter_counts"]
            )
            np.testing.assert_array_equal(model["add_one_table"], add_one)

    def test_loo_reprices_only_occurring_types(self) -> None:
        for language in LANGS:
            model = homo._shape_table(language)
            table = model["table"]
            add_one = model["add_one_table"]
            delta = table - add_one
            self.assertLessEqual(
                float(np.abs(delta).max()), float(np.log(2.0))
            )
            self.assertGreater(
                model["max_abs_entry_delta"], float(np.log(2.0)) - 1e-4
            )
            type0, type1 = model["max_delta_type"]
            self.assertEqual(
                (type0, type1),
                (0, 9) if language == "english" else (0, 10),
            )
        self.assertEqual(
            self.artifact["declared"]["models"]["english"][
                "pair_types_present"
            ], 490,
        )
        self.assertEqual(
            self.artifact["declared"]["models"]["latin"][
                "pair_types_present"
            ], 452,
        )

    def test_the_bridge_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["bridge_gate"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 57)
        self.assertIn("field for field",
                      self.artifact["declared"]["bridge_gate"])
        self.assertIn("aborts", self.artifact["declared"]["bridge_gate"])

    def test_the_models_block_carries_the_loo_facts(self) -> None:
        for language in LANGS:
            stream = homo._reference_stream(language)
            model = homo._shape_table(language)
            table = model["table"]
            full = homo._stream_matrix_27(stream)
            stored = self.artifact["declared"]["models"][language]
            clean = float((full * table).sum()) / float(full.sum())
            held_mean, climb_mean, _cp, _sp = homo._identity_half_means(
                stream, table
            )
            add_mean, _acm, _acp, _asp = homo._identity_half_means(
                stream, model["add_one_table"]
            )
            self.assertEqual(
                stored["clean_identity_mean_nats_per_pair"],
                round(clean, 4),
            )
            self.assertEqual(
                stored["identity_climb_half_mean_nats_per_pair"],
                round(climb_mean, 4),
            )
            self.assertEqual(
                stored["identity_score_half_mean_nats_per_pair"],
                round(held_mean, 4),
            )
            self.assertEqual(
                stored["add_one_identity_score_half_mean_nats_per_pair"],
                round(add_mean, 4),
            )
            self.assertEqual(
                stored["mean_entry_delta_over_present"],
                model["mean_entry_delta_over_present"],
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

    def test_loo_margins_match_the_add_one_margins(self) -> None:
        for code in FILES:
            for language in LANGS:
                held_cell = self.frozen_held["files"][code][language]
                add_one_margin = round(
                    held_cell["real_held_mean_nats"] - held_cell["band_min"],
                    4,
                )
                loo_margin = (
                    self.artifact["files"][code][language]
                    ["real_margin_over_band_min"]
                )
                width = abs(loo_margin - add_one_margin)
                if (code, language) == ("GC", "latin"):
                    self.assertGreater(loo_margin, add_one_margin)
                    self.assertLess(width, 0.03)
                else:
                    self.assertLessEqual(width, 0.0005)

    def test_margins_are_arithmetic_on_the_stored_values(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(
                    cell["real_margin_over_band_min"],
                    round(cell["real_held_mean_nats"] - cell["band_min"], 4),
                )

    def test_the_verdict_rule_holds_under_the_loo_form(self) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "do not restate the add-one form's verdicts",
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

    def test_the_loo_rule_declares_the_arithmetic_resolution(self) -> None:
        loo_rule = self.artifact["declared"]["loo_rule"]
        self.assertIn("log((n_ab + 1) / (N + 729))", loo_rule)
        self.assertIn("log(n_ab / (N + 728))", loo_rule)
        self.assertIn("log(1 / (N + 729))", loo_rule)
        self.assertIn("resolves as not needed", loo_rule)
        self.assertIn(
            "unchanged", self.artifact["declared"]["letter_counts_rule"]
        )

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
                    self.assertGreater(excess, 0.39)
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
                held_cell = self.frozen_held["files"][code][language]
                cell = self.artifact["files"][code][language]
                for key in ("counted_pairs", "climb_pairs", "score_pairs"):
                    self.assertEqual(cell[key], held_cell[key],
                                     (code, language, key))

    def test_anchors_recompute_under_the_loo_table(self) -> None:
        code, language = "ZL", "english"
        model = homo._shape_table(language)
        truncated = homo._truncated_reference(code, language)
        anchor, anchor_climb, _cp, _sp = homo._identity_half_means(
            truncated, model["table"]
        )
        cell = self.artifact["files"][code][language]
        self.assertEqual(
            cell["plant_parity_anchor_mean_nats"], round(anchor, 4)
        )
        self.assertEqual(
            cell["plant_climb_identity_mean_nats"], round(anchor_climb, 4)
        )
        held_cell = self.frozen_held["files"][code][language]
        self.assertNotEqual(
            round(anchor, 4),
            held_cell["plant_parity_anchor_mean_nats"],
        )

    def test_one_top_rung_real_recomputes_under_the_loo_table(
        self,
    ) -> None:
        code, language = "ZL", "english"
        model = homo._shape_table(language)
        stream = homo._homo_real_stream(code)
        first, second = homo._kept_pairs(
            stream["event_ids"], stream["kept_mask"]
        )
        climb_first, climb_second, score_first, score_second = (
            homo._split_pairs(first, second)
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
        self.assertEqual(cell["real_held_mean_nats"], -4.4256)
        self.assertEqual(round(view, 4), cell["real_climb_mean_nats"])
        self.assertEqual(cell["counted_pairs"], 218415)
        self.assertEqual(cell["climb_pairs"], 109208)
        self.assertEqual(cell["score_pairs"], 109207)

    def test_one_band_first_draw_replays_under_the_loo_table(self) -> None:
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
            homo._split_pairs(enc_first, enc_second)
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
        self.assertEqual(member["draws"][0], -4.7385)
        self.assertEqual(member["file"], name)

    def test_the_declared_question_is_answered_in_the_artifact(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's margin above the band survive a model the "
            "climb cannot feed on",
            declared["truthful_question"],
        )
        self.assertIn(
            "which instrument carried it", declared["truthful_question"]
        )
        self.assertIn(
            "draws_climb_exact", declared["band_record_rule"]
        )
        self.assertIn(
            "byte-identical replays", declared["measured_facts_rule"]
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
