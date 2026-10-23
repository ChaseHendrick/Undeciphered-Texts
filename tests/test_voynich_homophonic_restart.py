"""Tests for the declared restart budget of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute the first cell's facts at the declared 48 restarts from the
declared kinds and the standing language models from the standing
streams; the mechanical tests nail the declared rules on the stored
artifact: the restart declarations (the budget's stream
continuation, the recording, the convergence lens), the bridge gate
(116 fields), the models block re-playing the frozen widened band's
values, the frozen streams under the standing block fold, the
roll-up (margins as arithmetic, verdict rule, floor positions, plant
parity, cap flags, selected draws with recorded climb bests), the
band members' identity fields replaying the frozen artifact, the
re-folded anchors, the one-cell recompute, the declared question
answered in the artifact, and the dash bans. Nothing here reads the
manuscript beyond the frozen artifacts and the declared streams.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import engine.voynich_homophonic as homo
from engine.voynich_substitution import FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-restart-budget.json"
).resolve()
FROZEN_WIDENED = Path(
    "docs/research-notes/voynich-homophonic-widened-band.json"
).resolve()

# The frozen restart-budget artifact's headline (code, language) ->
# (real_held, band_min, band_max, margin, verdict, anchor, members),
# pinned from the artifact measured 23 October 2026 with the bridge
# gate verified at 116 fields.
FROZEN = {
    ("ZL", "english"): (-4.3747, -4.7262, -4.6085, 0.3515,
                        "consistent-with-substitution", -5.1397, 7),
    ("ZL", "latin"): (-4.3724, -4.6224, -4.5823, 0.25,
                      "consistent-with-substitution", -5.0686, 8),
    ("IT", "english"): (-4.3735, -4.7379, -4.6088, 0.3644,
                        "consistent-with-substitution", -5.1398, 7),
    ("IT", "latin"): (-4.3672, -4.6224, -4.5753, 0.2552,
                      "consistent-with-substitution", -5.0681, 8),
    ("GC", "english"): (-4.2642, -4.7012, -4.6083, 0.437,
                        "consistent-with-substitution", -5.1436, 7),
    ("GC", "latin"): (-4.3798, -4.6257, -4.5753, 0.2459,
                      "consistent-with-substitution", -5.0658, 8),
}

# The frozen widened band's margins, for the declared question's
# delta assertions: the same cells re-searched at 48 restarts.
WIDENED_MARGINS = {
    ("ZL", "english"): 0.3502,
    ("ZL", "latin"): 0.25,
    ("IT", "english"): 0.3644,
    ("IT", "latin"): 0.2552,
    ("GC", "english"): 0.3591,
    ("GC", "latin"): 0.2255,
}

# The three cells whose margins are exactly the frozen widened band's
# (the deeper search re-priced nothing that survived the 1e-12 rule),
# and the declared deepening headline.
HELD_EXACT = (("ZL", "latin"), ("IT", "english"), ("IT", "latin"))
DEEPENED_HEADLINE = ("GC", "english")


class RestartBudgetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_widened = json.loads(FROZEN_WIDENED.read_text())

    def test_declared_constants_and_budget(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(declared["base_seed"], homo.BASE_SEED)
        self.assertEqual(declared["mapped"], homo.MAPPED_HOMO)
        self.assertEqual(declared["restarts"], 48)
        self.assertEqual(declared["restarts"], homo.RESTART_BUDGET)
        self.assertEqual(
            declared["restarts_inherited"], homo.N_RESTARTS
        )
        self.assertEqual(declared["restarts_inherited"], 16)
        self.assertEqual(declared["sweep_cap"], homo.SWEEP_CAP)
        self.assertEqual(declared["plants_per_cell"], homo.N_PLANTS)
        self.assertEqual(declared["floors"], homo.N_FLOORS)
        self.assertEqual(
            declared["seed_kinds"],
            self.frozen_widened["declared"]["seed_kinds"],
        )
        self.assertEqual(declared["band_positions"],
                         {"english": 7, "latin": 8})
        self.assertEqual(homo.CONVERGENCE_TOLERANCE, 0.0001)

    def test_the_restart_budget_declaration(self) -> None:
        declared = self.artifact["declared"]
        self.assertIn("48 per machinery call", declared["restarts_rule"])
        self.assertIn(
            "restarts 1 to 15 replaying the inherited budget's "
            "permutation draws exactly", declared["restarts_rule"]
        )
        self.assertIn("restarts 16 to 47", declared["restarts_rule"])
        self.assertIn(
            "byte-identical replays of the frozen widened band's "
            "declared draws", declared["restarts_rule"]
        )
        self.assertIn("consuming no new seed",
                      declared["restarts_rule"])
        self.assertIn("0.0001", declared["convergence_rule"])
        self.assertIn(
            "no verdict, margin, membership or exclusion depends on "
            "any flag", declared["convergence_rule"]
        )
        self.assertIn(
            "only the restart budget's depth changes",
            declared["measured_facts_rule"],
        )
        self.assertIn(
            "every restart's exact total recorded",
            declared["machinery_rule"],
        )
        self.assertIn("carried forward unchanged", declared["loo_rule"])
        self.assertIn("floor(N/2)", declared["split_rule"])
        self.assertIn(
            "25/75 variant is not this measurement's split",
            declared["split_rule"],
        )
        self.assertIn("inherited 16 restarts supplied",
                      declared["bridge_gate"])
        self.assertIn("field for field", declared["bridge_gate"])
        self.assertIn("no new corpus files",
                      declared["corpus_source_rule"])

    def test_the_bridge_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["bridge_gate"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 116)

    def test_the_models_block_replays_the_frozen_values(self) -> None:
        declared = self.artifact["declared"]
        # the models are the standing references' shape facts, carried
        # unchanged from the frozen widened band: byte-for-byte
        self.assertEqual(
            declared["models"],
            self.frozen_widened["declared"]["models"],
        )
        # and they recompute from the standing english stream
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

    def test_every_machinery_call_records_its_restart_totals(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                # the cell's recorded calls: 48 totals each; the real's
                # best climb total equals the stored climb value, and
                # every full call's best total equals its stored exact
                # value (the full call's total IS its exact pricing)
                for key, stored_key in (
                    ("real_restart_totals", "real_climb_mean_nats"),
                    ("real_full_restart_totals",
                     "real_full_exact_mean_nats"),
                ):
                    totals = cell[key]
                    self.assertEqual(len(totals), 48, (code, language))
                    self.assertEqual(
                        round(max(totals), 4), cell[stored_key],
                        (code, language, key),
                    )
                for key, stored_key in (
                    ("plants_full_restart_totals",
                     "self_plants_full_exact_mean_nats"),
                    ("floors_full_restart_totals",
                     "floors_full_exact_mean_nats"),
                ):
                    for index, totals in enumerate(cell[key]):
                        self.assertEqual(
                            len(totals), 48,
                            (code, language, key, index),
                        )
                        self.assertEqual(
                            round(max(totals), 4),
                            cell[stored_key][index],
                            (code, language, key, index),
                        )
                # the climb-half totals of the plants and floors have
                # no stored scalar (only their held results are
                # stored), so their record is the arrays themselves:
                # 48 totals each, re-verified cell wide below
                for key in ("plants_restart_totals",
                            "floors_restart_totals"):
                    for totals in cell[key]:
                        self.assertEqual(len(totals), 48,
                                         (code, language, key))
                for member in cell["band"]:
                    for index, totals in enumerate(
                        member["draws_restart_totals"]
                    ):
                        self.assertEqual(
                            len(totals), 48,
                            (code, language, member["file"], index),
                        )
                        self.assertEqual(
                            round(max(totals), 4),
                            member["draws_climb"][index],
                            (code, language, member["file"], index),
                        )
                    for index, totals in enumerate(
                        member["draws_full_restart_totals"]
                    ):
                        self.assertEqual(
                            len(totals), 48,
                            (code, language, member["file"], index),
                        )
                        self.assertEqual(
                            round(max(totals), 4),
                            member["draws_full"][index],
                            (code, language, member["file"], index),
                        )

    def test_the_convergence_lens_is_recorded_and_gates_nothing(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                flags = (
                    [cell["real_convergence"],
                     cell["real_full_convergence"]]
                    + cell["plants_convergence"]
                    + cell["plants_full_convergence"]
                    + cell["floors_convergence"]
                    + cell["floors_full_convergence"]
                )
                for member in cell["band"]:
                    flags = flags + member["draws_convergence"]
                    flags = flags + member["draws_full_convergence"]
                # the recorded lens: no call's restarts agreed to
                # within 0.0001 at the deeper budget
                self.assertFalse(any(flags), (code, language))
                # the flags re-derive from the recorded totals
                self.assertEqual(
                    homo._restart_convergence(
                        cell["real_restart_totals"]
                    ),
                    cell["real_convergence"], (code, language),
                )
        # the lens' boundary behaviour on a hand-built call
        self.assertTrue(homo._restart_convergence([0.0, 0.0001]))
        self.assertFalse(homo._restart_convergence([0.0, 0.0002]))
        self.assertTrue(homo._restart_convergence([1.0, 1.0, 1.0]))

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
            self.assertEqual(
                cell["plant_parity_anchor_mean_nats"],
                self.frozen_widened["files"][code][language]
                ["plant_parity_anchor_mean_nats"],
            )
            self.assertEqual(len(cell["band"]), members)

    def test_the_margins_answer_the_declared_question(self) -> None:
        # every verdict keeps the frozen widened band's verdict under
        # the deeper budget, and no margin eases: the deeper search
        # holds five of six margins exactly or above and deepens two
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
                self.assertGreaterEqual(delta, 0.0, (code, language))
        # the three cells whose deeper search re-priced nothing that
        # survived the tie rule: margins exactly the frozen band's
        for key in HELD_EXACT:
            self.assertEqual(
                self.artifact["files"][key[0]][key[1]]
                ["real_margin_over_band_min"],
                WIDENED_MARGINS[key], key,
            )
        # the declared headline: GC english's margin deepens from
        # 0.3591 to 0.437, the widest of this measurement
        self.assertEqual(
            self.artifact["files"]["GC"]["english"]
            ["real_margin_over_band_min"], 0.437,
        )
        self.assertEqual(
            self.artifact["files"]["GC"]["latin"]
            ["real_margin_over_band_min"], 0.2459,
        )

    def test_the_streams_are_the_frozen_streams(self) -> None:
        # the standing block fold is this measurement's split: the
        # counted and folded pairs replay the frozen widened band's
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                widened = self.frozen_widened["files"][code][language]
                self.assertEqual(cell["counted_pairs"],
                                 widened["counted_pairs"])
                self.assertEqual(cell["climb_pairs"],
                                 widened["climb_pairs"])
                self.assertEqual(cell["score_pairs"],
                                 widened["score_pairs"])
                self.assertEqual(
                    cell["climb_pairs"], cell["counted_pairs"] // 2,
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
                    # the identity fields replay; the winning draw is
                    # re-priced under the deeper budget and need not
                    # stay the same draw
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
                    0.78, (code, language),
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

    def test_one_restart_cell_recomputes_from_kinds(self) -> None:
        code, language = "ZL", "english"
        model = homo._shape_table(language)
        facts = homo._restart_cell_facts(
            code, language, model["table"], model["letter_counts"],
            restarts=homo.RESTART_BUDGET,
        )
        stored = self.artifact["files"][code][language]
        for key, cell_key in homo._CELL_FIELD_MAP.items():
            self.assertEqual(
                stored[cell_key], facts[key],
                (code, language, key),
            )
        self.assertEqual(stored["real_restart_totals"],
                         facts["real_totals"])
        self.assertEqual(stored["real_full_restart_totals"],
                         facts["real_full_totals"])
        self.assertEqual(stored["plants_restart_totals"],
                         facts["plants_totals"])
        self.assertEqual(stored["floors_restart_totals"],
                         facts["floors_totals"])
        self.assertEqual(stored["plants_full_restart_totals"],
                         facts["plants_full_totals"])
        self.assertEqual(stored["floors_full_restart_totals"],
                         facts["floors_full_totals"])
        self.assertEqual(stored["real_convergence"],
                         facts["real_convergence"])
        self.assertEqual(stored["plants_convergence"],
                         facts["plants_convergence"])
        self.assertEqual(stored["floors_convergence"],
                         facts["floors_convergence"])

    def test_the_anchors_are_the_frozen_anchors(self) -> None:
        truncated = homo._truncated_reference("ZL", "english")
        model = homo._shape_table("english")
        held, climb, _cp, _sp = homo._block_identity_half_means(
            truncated, model["table"]
        )
        cell = self.artifact["files"]["ZL"]["english"]
        self.assertEqual(
            cell["plant_parity_anchor_mean_nats"], round(held, 4)
        )
        self.assertEqual(
            cell["plant_climb_identity_mean_nats"], round(climb, 4)
        )

    def test_the_declared_question_is_answered_in_the_artifact(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's held-out score-half value still stand "
            "above the band when every machinery call draws three "
            "times the inherited restart budget",
            declared["truthful_question"],
        )
        self.assertIn(
            "a no records that the margin rode the inherited "
            "budget's depth", declared["truthful_question"],
        )
        self.assertIn("membership unconditional",
                      declared["band_record_rule"])
        self.assertIn(
            "no convergence criterion is applied to any member",
            declared["band_record_rule"],
        )
        self.assertIn(
            "do not restate the widened band's verdicts",
            declared["verdict_rule"],
        )
        self.assertIn("not re-scoped", declared["exclusion_rule"])
        self.assertIn("restart-budget verdict is search-depth "
                      "evidence", declared["exclusion_rule"])
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
