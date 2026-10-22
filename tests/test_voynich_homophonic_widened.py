"""Tests for the declared widened band population of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute one widened member's record from kinds 28 and 29 at its
extended position and the language models from the declared streams;
the mechanical tests nail the declared rules on the stored artifact:
the extended member lists, the bridge gate (60 fields), the models
block, the streams, the roll-up (margins as arithmetic, verdict rule,
floor positions, plant parity, cap flags, selected draws with exact
climbs), the margins holding or widening against the frozen block-fold
artifact, the standing members' field-for-field replay, the real,
plants and floors replaying the frozen cell, the corpus facts roster
with recomputed sha256 provenance, the declared rejections with
cause, the declared question, and the dash bans. Nothing here reads
the manuscript beyond the frozen artifacts and the declared streams.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import DATA_DIR, FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-widened-band.json"
).resolve()
FROZEN_BLOCK = Path(
    "docs/research-notes/voynich-homophonic-block-fold.json"
).resolve()

# The frozen widened-band artifact's headline (code, language) ->
# (real_held, band_min, band_max, margin, verdict, anchor, members),
# pinned from the artifact measured 22 October 2026 with the bridge
# gate verified at 60 fields.
FROZEN = {
    ("ZL", "english"): (-4.4245, -4.7747, -4.6085, 0.3502,
                        "consistent-with-substitution", -5.1397, 7),
    ("ZL", "latin"): (-4.3724, -4.6224, -4.5823, 0.25,
                      "consistent-with-substitution", -5.0686, 8),
    ("IT", "english"): (-4.3735, -4.7379, -4.6088, 0.3644,
                        "consistent-with-substitution", -5.1398, 7),
    ("IT", "latin"): (-4.3672, -4.6224, -4.5753, 0.2552,
                      "consistent-with-substitution", -5.0681, 8),
    ("GC", "english"): (-4.3421, -4.7012, -4.6083, 0.3591,
                        "consistent-with-substitution", -5.1436, 7),
    ("GC", "latin"): (-4.4002, -4.6257, -4.5753, 0.2255,
                      "consistent-with-substitution", -5.0658, 8),
}

MEMBERS = {
    "english": ["substref_english2_pg84.txt", "substref_english3_pg2701.txt",
                "substref_english4_pg1251.txt", "substref_english5_pg174.txt",
                "substref_english6_pg1400.txt", "substref_english7_pg120.txt",
                "substref_english8_pg158.txt"],
    "latin": ["substref_latin2_pg218.txt", "substref_latin3_pg828.txt",
              "substref_latin4_pg17859.txt", "substref_latin5_pg27655.txt",
              "substref_latin6_pg23306.txt", "substref_latin7_pg28233.txt",
              "substref_latin8_pg826.txt", "substref_latin9_pg58528.txt"],
}

# The replayed cell fields, key by key against the frozen block fold.
REPLAYED_FIELDS = [
    "real_held_mean_nats", "real_climb_mean_nats",
    "real_full_exact_mean_nats", "counted_pairs", "climb_pairs",
    "score_pairs", "plant_parity_anchor_mean_nats",
    "plant_climb_identity_mean_nats", "self_plants_held_mean_nats",
    "self_plants_full_exact_mean_nats", "self_plants_at_parity",
    "machinery_above_anchor_excesses", "floors_held_mean_nats",
    "floors_full_exact_mean_nats", "real_sweep_budget_hit",
    "real_full_sweep_budget_hit", "self_plants_sweep_budget_hits",
    "self_plants_full_sweep_budget_hits", "floors_sweep_budget_hits",
    "floors_full_sweep_budget_hits",
]

CELL_FIELDS = {"ZL": ("english", "latin"), "IT": ("english", "latin"),
               "GC": ("english", "latin")}


class WidenedBandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_block = json.loads(FROZEN_BLOCK.read_text())

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
            self.frozen_block["declared"]["seed_kinds"],
        )
        self.assertEqual(declared["band_positions"],
                         {"english": 7, "latin": 8})

    def test_the_extended_member_lists(self) -> None:
        for language in LANGS:
            members = homo._extended_reference_members(language)
            self.assertEqual(
                [name for name, _ebook in members], MEMBERS[language],
                language,
            )
            positions = homo._extended_band_positions(language)
            self.assertEqual(len(positions), len(members), language)
        self.assertEqual(
            [entry[1] for entry in
             homo.EXTENDED_WIDENED_REFERENCE_FILES["english"]],
            [174, 1400, 120, 158],
        )
        self.assertEqual(
            [entry[1] for entry in
             homo.EXTENDED_WIDENED_REFERENCE_FILES["latin"]],
            [23306, 28233, 826, 58528],
        )

    def test_the_bridge_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["bridge_gate"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 60)
        self.assertIn("field for field",
                      self.artifact["declared"]["bridge_gate"])
        self.assertIn("extended member list",
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
            frozen_model = self.frozen_block["declared"]["models"][language]
            self.assertEqual(
                stored["clean_identity_mean_nats_per_pair"],
                round(clean, 4),
            )
            self.assertEqual(
                stored["block_score_half_mean_nats_per_pair"],
                round(block_held, 4),
            )
            self.assertEqual(
                stored["block_climb_half_mean_nats_per_pair"],
                round(block_climb, 4),
            )
            # the models are the frozen block artifact's models
            for key in ("clean_identity_mean_nats_per_pair",
                        "block_climb_half_mean_nats_per_pair",
                        "block_score_half_mean_nats_per_pair",
                        "pair_types_present", "total_pairs",
                        "max_abs_entry_delta", "max_delta_type",
                        "mean_entry_delta_over_present"):
                self.assertEqual(stored[key], frozen_model[key], key)

    def test_the_headline_numbers_match_the_freeze(self) -> None:
        for (code, language), frozen in FROZEN.items():
            cell = self.artifact["files"][code][language]
            (real, band_min, band_max, margin, verdict, anchor,
             members) = frozen
            self.assertEqual(cell["real_held_mean_nats"], real)
            self.assertEqual(cell["band_min"], band_min)
            self.assertEqual(cell["band_max"], band_max)
            self.assertEqual(cell["real_margin_over_band_min"], margin)
            self.assertEqual(cell["verdict"], verdict)
            self.assertEqual(
                cell["plant_parity_anchor_mean_nats"], anchor
            )
            self.assertEqual(len(cell["band"]), members)
            self.assertEqual(
                [m["file"] for m in cell["band"]], MEMBERS[language]
            )

    def test_the_widened_margins_hold_or_widen(self) -> None:
        for code in FILES:
            for language in LANGS:
                margin = (
                    self.artifact["files"][code][language]
                    ["real_margin_over_band_min"]
                )
                block_margin = (
                    self.frozen_block["files"][code][language]
                    ["real_margin_over_band_min"]
                )
                self.assertGreaterEqual(
                    margin, block_margin, (code, language)
                )
                residual = margin - block_margin
                self.assertLessEqual(residual, 0.05, (code, language))
        # the held-exact cell: GC english's margin is unchanged because
        # the band's minimum stays the standing english2 member
        self.assertEqual(
            self.artifact["files"]["GC"]["english"]
            ["real_margin_over_band_min"], 0.3591,
        )
        self.assertEqual(
            self.artifact["files"]["GC"]["english"]["band_min"], -4.7012,
        )

    def test_standing_members_replay_the_frozen_band(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                block_cell = self.frozen_block["files"][code][language]
                standing = len(block_cell["band"])
                for index in range(standing):
                    self.assertEqual(
                        cell["band"][index], block_cell["band"][index],
                        (code, language, index),
                    )

    def test_the_real_plants_and_floors_replay_the_frozen_cell(
        self,
    ) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                block_cell = self.frozen_block["files"][code][language]
                for key in REPLAYED_FIELDS:
                    self.assertEqual(
                        cell[key], block_cell[key], (code, language, key)
                    )

    def test_margins_are_arithmetic_on_the_stored_values(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                self.assertEqual(
                    cell["real_margin_over_band_min"],
                    round(cell["real_held_mean_nats"] - cell["band_min"], 4),
                )

    def test_the_verdict_rule_holds_under_the_widened_band(self) -> None:
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
                member_values = [m["recovered_best"] for m in cell["band"]]
                self.assertEqual(min(member_values), cell["band_min"])
                self.assertEqual(max(member_values), cell["band_max"])
                if cell["real_held_mean_nats"] >= cell["band_min"]:
                    verdict = "consistent-with-substitution"
                elif cell["real_held_mean_nats"] <= floor_max:
                    verdict = "not-consistent"
                else:
                    verdict = "below-held-band"
                self.assertEqual(cell["verdict"], verdict)

    def test_the_widened_band_minimum_stays_deep_or_moves_to_a_widened(
        self,
    ) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                block_cell = self.frozen_block["files"][code][language]
                self.assertLessEqual(
                    cell["band_min"], block_cell["band_min"],
                    (code, language),
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
                    self.assertEqual(
                        member["spread"],
                        round(max(member["draws"])
                              - min(member["draws"]), 4),
                    )

    def test_the_streams_are_the_frozen_streams(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                block_cell = self.frozen_block["files"][code][language]
                self.assertEqual(cell["counted_pairs"],
                                 block_cell["counted_pairs"])
                self.assertEqual(
                    cell["climb_pairs"] + cell["score_pairs"],
                    cell["counted_pairs"],
                )

    def test_one_widened_member_recomputes_from_kinds(self) -> None:
        code, language, position = "ZL", "latin", 4
        model = homo._shape_table(language)
        member = homo._block_band_for(
            code, language, position, model["table"],
            model["letter_counts"],
            members=homo._extended_reference_members(language),
        )
        self.assertEqual(member["file"], "substref_latin6_pg23306.txt")
        self.assertEqual(member["ebook"], 23306)
        self.assertEqual(member["plant_length"], 132608)
        self.assertEqual(member["draws"], [-4.5999] * 5)
        self.assertEqual(member["recovered_best"], -4.5999)
        self.assertEqual(member["selected_draw_index"], 0)
        self.assertEqual(member["spread"], 0.0)
        self.assertEqual(member["anchor"], -5.1442)
        self.assertEqual(member["anchor_climb"], -5.1556)
        self.assertFalse(any(member["draw_sweep_budget_hits"]))
        self.assertFalse(any(member["draw_full_sweep_budget_hits"]))
        stored = self.artifact["files"][code][language]["band"][position]
        self.assertEqual(member, stored)

    def test_the_corpus_facts_record_the_widened_provenance(self) -> None:
        declared = self.artifact["declared"]
        roster = {
            "english": [("substref_english5_pg174.txt", 412038, None),
                        ("substref_english6_pg1400.txt", 951754, None),
                        ("substref_english7_pg120.txt", 346442, None),
                        ("substref_english8_pg158.txt", 847001, None)],
            "latin": [("substref_latin6_pg23306.txt", 132608, 2),
                      ("substref_latin7_pg28233.txt", 748514, 19),
                      ("substref_latin8_pg826.txt", 45491, 52),
                      ("substref_latin9_pg58528.txt", 1008988, 12)],
        }
        for language in LANGS:
            facts = declared["corpus_facts"][language]
            self.assertEqual(len(facts), 4, language)
            for entry, (name, stream, hits) in zip(facts, roster[language]):
                self.assertEqual(entry["file"], name)
                self.assertEqual(entry["stream_length"], stream)
                self.assertEqual(entry["english_scaffold_hits"], hits)
                self.assertEqual(entry["types_present"], 27)
                raw = (Path(DATA_DIR).resolve().parent / name).read_bytes()
                self.assertEqual(
                    entry["sha256"], hashlib.sha256(raw).hexdigest(), name
                )
        labels = [entry["label"] for entry in
                  declared["corpus_facts"]["latin"]]
        self.assertIn("Vulgata Esther", labels)
        self.assertIn("Meditationes de prima philosophia (Descartes)",
                      labels)

    def test_the_rejected_candidates_are_declared_with_cause(self) -> None:
        rejected = self.artifact["declared"]["rejected_candidates"]
        ebooks = sorted(entry["ebook"] for entry in rejected)
        self.assertEqual(
            ebooks,
            sorted([47001, 7402, 21827, 13316, 54243, 51812,
                    69275, 19635]),
        )
        for entry in rejected:
            self.assertTrue(entry["cause"].strip(), entry["ebook"])
            self.assertTrue(entry["label"].strip(), entry["ebook"])
        interleaved = [entry["ebook"] for entry in rejected
                       if "interleaved" in entry["cause"]]
        self.assertIn(51812, interleaved)

    def test_the_declared_question_is_answered_in_the_artifact(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's held-out score-half value still stand "
            "above the band as the band's population grows",
            declared["truthful_question"],
        )
        self.assertIn(
            "band's population changes", declared["measured_facts_rule"]
        )
        self.assertIn(
            "byte-identical replays", declared["measured_facts_rule"]
        )
        self.assertIn("draws_climb_exact", declared["band_record_rule"])
        self.assertIn("unconditionally", declared["band_record_rule"])
        self.assertIn("0 to 52", declared["corpus_rule"])
        self.assertIn("rejected with cause", declared["corpus_rule"])
        self.assertIn("carried forward unchanged", declared["loo_rule"])
        self.assertIn("english 3 to 6, latin 4 to 7",
                      declared["seed_sharing"])

    def test_no_mapping_is_published(self) -> None:
        self.assertIn("No mapping is published", self.artifact["what"])
        self.assertIn("nothing here is a reading", self.artifact["what"])
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
