"""Tests for the declared split's ratio of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute the first cell's facts through the declared 25/75 block
split and the standing language models from the standing streams; the
mechanical tests nail the declared rules on the stored artifact: the
split declarations, the bridge gate (116 fields), the models block
replaying the frozen widened band's values, the frozen streams with
the quarter fold's arithmetic, the roll-up (margins as arithmetic
with their four-decimal deltas against the frozen widened band,
verdict rule, floor positions, plant parity, cap flags, selected
draws with exact climbs), the band members' identity fields
replaying the frozen artifact, the re-folded anchors, the one-cell
recompute, the module's own split function on a hand-built array, the
declared question answered in the artifact, and the dash bans.
Nothing here reads the manuscript beyond the frozen artifacts and
the declared streams.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-split-ratio.json"
).resolve()
FROZEN_WIDENED = Path(
    "docs/research-notes/voynich-homophonic-widened-band.json"
).resolve()

# The frozen split-ratio artifact's headline (code, language) ->
# (real_held, band_min, band_max, margin, verdict, anchor, members),
# pinned from the artifact measured 22 October 2026 with the bridge
# gate verified at 116 fields.
FROZEN = {
    ("ZL", "english"): (-4.3841, -4.7408, -4.6115, 0.3567,
                        "consistent-with-substitution", -5.1391, 7),
    ("ZL", "latin"): (-4.3827, -4.6373, -4.5761, 0.2546,
                      "consistent-with-substitution", -5.0686, 8),
    ("IT", "english"): (-4.3818, -4.7398, -4.6118, 0.358,
                        "consistent-with-substitution", -5.1392, 7),
    ("IT", "latin"): (-4.378, -4.6374, -4.5761, 0.2594,
                      "consistent-with-substitution", -5.0685, 8),
    ("GC", "english"): (-4.4003, -4.7447, -4.6107, 0.3444,
                        "consistent-with-substitution", -5.1373, 7),
    ("GC", "latin"): (-4.4133, -4.6341, -4.5793, 0.2208,
                      "consistent-with-substitution", -5.0685, 8),
}

# The frozen widened band's margins, for the declared question's
# delta assertions: the same cells re-folded at the quarter mark.
WIDENED_MARGINS = {
    ("ZL", "english"): 0.3502,
    ("ZL", "latin"): 0.25,
    ("IT", "english"): 0.3644,
    ("IT", "latin"): 0.2552,
    ("GC", "english"): 0.3591,
    ("GC", "latin"): 0.2255,
}

# The declared direction of the deltas, read off the frozen artifact:
# three cells' margins deepen, three ease, none flips sign.
DEEPENED = (("ZL", "english"), ("ZL", "latin"), ("IT", "latin"))
EASED = (("IT", "english"), ("GC", "english"), ("GC", "latin"))


class RatioSplitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_widened = json.loads(FROZEN_WIDENED.read_text())

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
            self.frozen_widened["declared"]["seed_kinds"],
        )
        self.assertEqual(declared["band_positions"],
                         {"english": 7, "latin": 8})

    def test_the_split_ratio_declaration(self) -> None:
        declared = self.artifact["declared"]
        self.assertIn("floor(N/4)", declared["split_rule"])
        self.assertIn("quarter mark", declared["split_rule"])
        self.assertIn("consuming no seed", declared["split_rule"])
        self.assertIn("every identity anchor's halves fold by the "
                      "same rule", declared["split_rule"])
        self.assertIn("the split consumes no seed",
                      declared["seed_sharing"])
        self.assertIn("byte-identical replays",
                      declared["measured_facts_rule"])
        self.assertIn("only the split's ratio changes",
                      declared["measured_facts_rule"])
        self.assertIn("re-climbs on the smaller climb part",
                      declared["measured_facts_rule"])
        self.assertIn("carried forward unchanged", declared["loo_rule"])
        self.assertIn("unchanged from the held-out screen",
                      declared["machinery_rule"])
        self.assertIn("no new corpus files",
                      declared["corpus_source_rule"])

    def test_the_bridge_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["bridge_gate"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 116)
        self.assertIn("field for field",
                      self.artifact["declared"]["bridge_gate"])
        self.assertIn("standing split supplied",
                      self.artifact["declared"]["bridge_gate"])

    def test_the_models_block_replays_the_frozen_values(self) -> None:
        declared = self.artifact["declared"]
        # the models are the standing references' shape facts, carried
        # unchanged from the frozen widened band: byte-for-byte
        self.assertEqual(
            declared["models"],
            self.frozen_widened["declared"]["models"],
        )
        # and they recompute from the standing english stream through
        # the standing split
        stream = homo._reference_stream("english")
        model = homo._shape_table("english")
        block_held, block_climb, _cp, _sp = (
            homo._block_identity_half_means(stream, model["table"])
        )
        stored = declared["models"]["english"]
        self.assertEqual(stored["file"], "substref_english_pg1342.txt")
        self.assertEqual(stored["ebook"], 1342)
        self.assertEqual(
            stored["block_score_half_mean_nats_per_pair"],
            round(block_held, 4),
        )
        self.assertEqual(
            stored["block_climb_half_mean_nats_per_pair"],
            round(block_climb, 4),
        )

    def test_the_ratio_split_function_is_declared(self) -> None:
        # the artifact path ends in the declared name
        self.assertEqual(
            Path(homo.RATIO_ARTIFACT_PATH).resolve().name,
            "voynich-homophonic-split-ratio.json",
        )
        self.assertIn("floor(N/4)",
                      homo._quarter_pairs.__doc__)
        # a hand-built stream: 11 counted pairs, floor(11/4) = 2
        first = np.arange(11)
        second = np.arange(100, 111)
        climb_first, climb_second, score_first, score_second = (
            homo._quarter_pairs(first, second)
        )
        self.assertEqual(climb_first.tolist(), [0, 1])
        self.assertEqual(climb_second.tolist(), [100, 101])
        self.assertEqual(score_first.tolist(), list(range(2, 11)))
        self.assertEqual(score_second.tolist(), list(range(102, 111)))
        # an exact quarter: 12 counted pairs take 3 and 9
        first = np.arange(12)
        second = np.arange(50, 62)
        climb_first, _climb_second, score_first, _score_second = (
            homo._quarter_pairs(first, second)
        )
        self.assertEqual(len(climb_first), 3)
        self.assertEqual(len(score_first), 9)
        # the climb part never touches the scored pairs' index range
        self.assertEqual(int(climb_first[-1]), 2)
        self.assertEqual(int(score_first[0]), 3)

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
                [m["file"] for m in cell["band"]],
                [m["file"] for m in
                 self.frozen_widened["files"][code][language]["band"]],
            )

    def test_the_margins_answer_the_declared_question(self) -> None:
        # every verdict keeps the frozen widened band's verdict under
        # the ratio split, and every margin stays positive with its
        # declared four-decimal delta against the frozen widened band
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                widened = self.frozen_widened["files"][code][language]
                self.assertEqual(
                    cell["verdict"], widened["verdict"], (code, language)
                )
                self.assertGreater(
                    cell["real_margin_over_band_min"], 0.0, (code, language)
                )
                delta = round(
                    cell["real_margin_over_band_min"]
                    - widened["real_margin_over_band_min"], 4
                )
                self.assertEqual(
                    delta,
                    round(
                        FROZEN[(code, language)][3]
                        - WIDENED_MARGINS[(code, language)], 4
                    ),
                    (code, language),
                )
        # the three cells whose margins deepen, declared
        for key in DEEPENED:
            self.assertGreaterEqual(
                self.artifact["files"][key[0]][key[1]]
                ["real_margin_over_band_min"],
                WIDENED_MARGINS[key], key,
            )
        # the three cells whose margins ease stay positive and deep
        # into the band: 0.358, 0.3444 and 0.2208
        for key in EASED:
            self.assertGreater(
                self.artifact["files"][key[0]][key[1]]
                ["real_margin_over_band_min"], 0.21, key,
            )
        # the declared headline: the widest margin of this measurement
        # and the largest ease, both four-decimal values
        self.assertEqual(
            self.artifact["files"]["IT"]["english"]
            ["real_margin_over_band_min"], 0.358,
        )
        self.assertEqual(
            self.artifact["files"]["GC"]["english"]
            ["real_margin_over_band_min"], 0.3444,
        )
        self.assertEqual(
            self.artifact["files"]["GC"]["latin"]
            ["real_margin_over_band_min"], 0.2208,
        )

    def test_the_ratio_split_counts_declared(self) -> None:
        # the streams are the frozen streams: the counted pairs
        # replay untouched; the fold moves to the quarter mark
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                widened = self.frozen_widened["files"][code][language]
                self.assertEqual(cell["counted_pairs"],
                                 widened["counted_pairs"])
                self.assertEqual(
                    cell["climb_pairs"],
                    cell["counted_pairs"] // 4, (code, language),
                )
                self.assertEqual(
                    cell["score_pairs"],
                    cell["counted_pairs"] - cell["climb_pairs"],
                    (code, language),
                )
                self.assertNotEqual(
                    cell["climb_pairs"], widened["climb_pairs"],
                    (code, language),
                )

    def test_band_members_replay_their_frozen_identity(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                widened = self.frozen_widened["files"][code][language]
                for index, (fresh, stored) in enumerate(
                    zip(cell["band"], widened["band"])
                ):
                    # the identity fields replay; the draw that wins
                    # the selection is re-priced under the smaller
                    # climb half and is not expected to stay the same
                    self.assertEqual(fresh["file"], stored["file"],
                                     (code, language, index))
                    self.assertEqual(fresh["ebook"], stored["ebook"],
                                     (code, language, index))
                    self.assertEqual(
                        fresh["plant_length"], stored["plant_length"],
                        (code, language, index),
                    )

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

    def test_every_floor_stays_below_the_real(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                floor_max = max(cell["floors_held_mean_nats"])
                self.assertLess(floor_max, cell["real_held_mean_nats"],
                                (code, language))
                self.assertGreaterEqual(
                    round(cell["real_held_mean_nats"] - floor_max, 4),
                    0.75, (code, language),
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
                    self.assertLess(excess, 0.5)

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

    def test_one_ratio_cell_recomputes_from_kinds(self) -> None:
        code, language = "ZL", "english"
        model = homo._shape_table(language)
        facts = homo._block_cell_facts(
            code, language, model["table"], model["letter_counts"],
            split_pairs=homo._quarter_pairs,
        )
        stored = self.artifact["files"][code][language]
        for key, value in facts.items():
            self.assertEqual(
                stored[homo._CELL_FIELD_MAP[key]], value,
                (code, language, key),
            )

    def test_the_anchors_refold_under_the_ratio_rule(self) -> None:
        for code in FILES:
            for language in LANGS:
                truncated = homo._truncated_reference(code, language)
                model = homo._shape_table(language)
                held, climb, _cp, _sp = homo._block_identity_half_means(
                    truncated, model["table"],
                    split_pairs=homo._quarter_pairs,
                )
                cell = self.artifact["files"][code][language]
                self.assertEqual(
                    cell["plant_parity_anchor_mean_nats"],
                    round(held, 4), (code, language),
                )
                self.assertEqual(
                    cell["plant_climb_identity_mean_nats"],
                    round(climb, 4), (code, language),
                )

    def test_the_declared_question_is_answered_in_the_artifact(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's held-out score-half value still stand "
            "above the band when the climb part shrinks to a quarter "
            "of each side's counted pairs",
            declared["truthful_question"],
        )
        self.assertIn(
            "a no records that the margin rode the climb half's size",
            declared["truthful_question"],
        )
        self.assertIn("draws_climb_exact", declared["band_record_rule"])
        self.assertIn("unconditional", declared["band_record_rule"])
        self.assertIn(
            "do not restate the widened band's verdicts",
            declared["verdict_rule"],
        )
        self.assertIn("not re-scoped", declared["exclusion_rule"])
        self.assertIn("split-ratio verdict is split-geometry evidence",
                      declared["exclusion_rule"])
        self.assertIn(
            "the margin is computed from the stored rounded values",
            declared["margin_rule"],
        )
        self.assertEqual(declared["corpus_facts"], {})

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
