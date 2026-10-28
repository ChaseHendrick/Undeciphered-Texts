"""Tests for the declared surplus-capacity ladder of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute one narrow-rung real cell from kind 1 and one band member's
first draw from kinds 28 and 29; the mechanical tests nail the rung
rules: the top rung's stream equals the frozen stream, surplus
characters drop exactly across the rungs, the partition rule
conserves slots at every budget, the exact candidates hold at narrow
widths, the reproduction gate stands in the artifact, and the roll-up
(arithmetic on stored values, verdict rule, floor positions, plant
parity, cap flags, selected draws, rung-invariant anchors) matches the
stored numbers. Nothing here reads the manuscript beyond the frozen
artifacts and the declared streams.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import BOUNDARY, FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-ladder.json"
).resolve()
FROZEN_HELD = Path(
    "docs/research-notes/voynich-homophonic-heldout.json"
).resolve()

# The frozen ladder's headline (code, language) -> rung -> (real_held,
# band_min, margin, verdict), pinned from the artifact measured 21
# October 2026 with the reproduction gate verified at 421 fields.
FROZEN = {
    ("ZL", "english"): {
        36: (-4.4252, -4.6997, 0.2745), 33: (-4.4282, -4.7297, 0.3015),
        30: (-4.4251, -4.6712, 0.2461), 27: (-4.4259, -4.7297, 0.3038),
    },
    ("ZL", "latin"): {
        36: (-4.3743, -4.6081, 0.2338), 33: (-4.4242, -4.6081, 0.1839),
        30: (-4.3742, -4.6081, 0.2339), 27: (-4.3748, -4.6081, 0.2333),
    },
    ("GC", "english"): {
        36: (-4.3534, -4.6989, 0.3455), 33: (-4.2869, -4.7271, 0.4402),
        30: (-4.3519, -4.6729, 0.321), 27: (-4.2802, -4.7271, 0.4469),
    },
    ("GC", "latin"): {
        36: (-4.4318, -4.6081, 0.1763), 33: (-4.3901, -4.6081, 0.218),
        30: (-4.4016, -4.6081, 0.2065), 27: (-4.3872, -4.6063, 0.2191),
    },
    ("IT", "english"): {
        36: (-4.3878, -4.6992, 0.3114), 33: (-4.3878, -4.7298, 0.342),
        30: (-4.3878, -4.6713, 0.2835), 27: (-4.3878, -4.7298, 0.342),
    },
    ("IT", "latin"): {
        36: (-4.3707, -4.6081, 0.2374), 33: (-4.3707, -4.6081, 0.2374),
        30: (-4.3707, -4.6063, 0.2356), 27: (-4.3707, -4.6063, 0.2356),
    },
}
FROZEN_COUNTED = {
    "ZL": {36: 218415, 33: 218383, 30: 218347, 27: 218309},
    "GC": {36: 183199, 33: 182403, 30: 181444, 27: 179912},
    "IT": {36: 220531, 33: 220531, 30: 220531, 27: 220531},
}


class LadderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())
        self.frozen_held = json.loads(FROZEN_HELD.read_text())

    def test_declared_constants_and_no_new_seed_kinds(self) -> None:
        self.assertEqual(homo.LADDER_BUDGETS, (36, 33, 30, 27))
        self.assertEqual(
            homo.KIND_ID,
            {
                "real": 1,
                "homo_plant_enc": 24, "homo_plant_mach": 25,
                "homo_floor_perm": 26, "homo_floor_mach": 27,
                "homo_cross_enc": 28, "homo_cross_mach": 29,
                "homo_cut_geom": 30,
            },
        )
        self.assertEqual(
            homo.LADDER_ARTIFACT_PATH.name,
            "voynich-homophonic-ladder.json",
        )

    def test_the_top_rung_streams_are_the_frozen_streams(self) -> None:
        for code in FILES:
            frozen = homo._homo_real_stream(code)
            rung = homo._ladder_real_stream(code, 36)
            self.assertTrue(
                np.array_equal(frozen["event_ids"], rung["event_ids"]),
                code,
            )
            self.assertTrue(
                np.array_equal(frozen["kept_mask"], rung["kept_mask"]),
                code,
            )
            self.assertEqual(
                frozen["mapped_chars"], rung["mapped_chars"], code
            )
            self.assertEqual(
                frozen["total_events"], rung["total_events"], code
            )

    def test_surplus_characters_drop_exactly_across_the_rungs(self) -> None:
        ranked = homo._ladder_raw_stream("ZL")["ranked"]
        for budget in homo.LADDER_BUDGETS:
            stream = homo._ladder_real_stream("ZL", budget)
            self.assertEqual(
                stream["mapped_chars"],
                tuple(char for char, _count in ranked[:budget]) + (BOUNDARY,),
            )
        it = homo._ladder_raw_stream("IT")["ranked"]
        self.assertLess(len(it), 27)
        for budget in homo.LADDER_BUDGETS:
            stream = homo._ladder_real_stream("IT", budget)
            self.assertEqual(len(stream["mapped_chars"]), 24)
            self.assertEqual(
                stream["mapped_chars"],
                tuple(char for char, _count in it) + (BOUNDARY,),
            )
            self.assertEqual(int(stream["kept_ids"].max()), 23)

    def test_partition_conserves_slots_at_every_budget(self) -> None:
        for language in LANGS:
            truncated = homo._truncated_reference("ZL", language)
            present = sorted(set(t for t in truncated if t != 26))
            for budget in (27, 33):
                groups = homo._partition_groups(truncated, budget)
                sizes = [
                    len(groups[index]) for index in present
                ]
                self.assertGreater(min(sizes), 0, (language, budget))
                self.assertEqual(sum(sizes), budget, (language, budget))
                self.assertLessEqual(max(sizes), budget - len(present) + 1)
                for letter in range(27):
                    group = groups[letter]
                    if group:
                        self.assertEqual(
                            group,
                            list(range(group[0], group[0] + len(group))),
                            (language, budget, letter),
                        )

    def test_narrow_width_candidates_are_the_exact_new_totals(self) -> None:
        rng = np.random.default_rng(20261021)
        width = 27 + 1
        counts = rng.integers(0, 40, size=(27, 27))
        table = -np.log((counts + 1.0) / (counts.sum(axis=1) + 27.0))
        matrix = rng.integers(0, 9, size=(width, width)).astype(float)
        f = [int(value) for value in rng.integers(0, 27, size=width)]
        best = homo._score(f, matrix, table)
        diag_table = np.diag(table)
        for symbol in (0, 1, 14, 27):
            outbound = table[:, f] @ matrix[symbol]
            inbound = matrix[:, symbol] @ table[f, :]
            current = f[symbol]
            n = matrix[symbol, symbol]
            hold = (
                outbound[current] + inbound[current]
                - n * table[current, current]
            )
            candidates = (
                best + outbound + inbound - hold
                - n * table[:, current]
                - n * table[current, :]
                + n * diag_table
            )
            candidates[current] = best
            for label in range(27):
                if label == current:
                    self.assertEqual(candidates[label], best)
                    continue
                probe = list(f)
                probe[symbol] = label
                exact_value = homo._score(probe, matrix, table)
                self.assertAlmostEqual(
                    candidates[label], exact_value, delta=1e-9,
                    msg=(symbol, label),
                )
        small = rng.integers(0, 7, size=(8, 8)).astype(float)
        f0 = [0] * 8
        best_small, _sweeps, f_best = homo._held_climb(small, table, f0)
        self.assertAlmostEqual(
            best_small, homo._score(f_best, small, table)
        )

    def test_the_reproduction_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["rung_36_reproduction_check"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 421)
        for language in LANGS:
            frozen_models = self.frozen_held["declared"]["models"][language]
            ladder_models = self.artifact["declared"]["models"][language]
            self.assertEqual(frozen_models, ladder_models, language)

    def test_the_top_rung_cells_match_the_frozen_artifact(self) -> None:
        for code in FILES:
            for language in LANGS:
                frozen_cell = self.frozen_held["files"][code][language]
                rung_cell = (
                    self.artifact["rungs"]["36"]["files"][code][language]
                )
                for key, value in frozen_cell.items():
                    if key == "band":
                        self.assertEqual(len(rung_cell[key]), len(value))
                        for index, member in enumerate(value):
                            for member_key, member_value in (
                                member.items()
                            ):
                                self.assertEqual(
                                    rung_cell[key][index][member_key],
                                    member_value,
                                    (code, language, index, member_key),
                                )
                    else:
                        self.assertEqual(
                            rung_cell[key], value, (code, language, key)
                        )

    def test_margins_are_arithmetic_on_the_stored_values(self) -> None:
        for code in FILES:
            for language in LANGS:
                roll = self.artifact["files"][code][language]
                for budget in homo.LADDER_BUDGETS:
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    expected = round(
                        cell["real_held_mean_nats"]
                        - cell["band_min"], 4
                    )
                    self.assertEqual(
                        cell["real_margin_over_band_min"], expected
                    )
                    self.assertEqual(
                        roll["margins_over_band_min"][str(budget)],
                        expected,
                    )
                    self.assertEqual(
                        roll["verdicts"][str(budget)], cell["verdict"]
                    )
                steps = roll["margin_steps"]
                for before, after in zip(
                    homo.LADDER_BUDGETS[:-1], homo.LADDER_BUDGETS[1:]
                ):
                    expected = round(
                        roll["margins_over_band_min"][str(after)]
                        - roll["margins_over_band_min"][str(before)], 4
                    )
                    self.assertEqual(
                        steps[f"{before}_to_{after}"], expected
                    )

    def test_the_headline_numbers_match_the_freeze(self) -> None:
        for code in FILES:
            for language in LANGS:
                roll = self.artifact["files"][code][language]
                for budget, stored in FROZEN[(code, language)].items():
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    real_held, band_min, margin = stored
                    self.assertEqual(
                        cell["real_held_mean_nats"], real_held,
                        (code, language, budget),
                    )
                    self.assertEqual(
                        cell["band_min"], band_min,
                        (code, language, budget),
                    )
                    self.assertEqual(
                        cell["real_margin_over_band_min"], margin,
                        (code, language, budget),
                    )
                    self.assertEqual(
                        cell["verdict"], "consistent-with-substitution",
                        (code, language, budget),
                    )
                    self.assertEqual(
                        roll["margins_over_band_min"][str(budget)], margin
                    )
        for code, counts in FROZEN_COUNTED.items():
            for budget, counted in counts.items():
                cell = (
                    self.artifact["rungs"][str(budget)][
                        "files"][code]
                )
                language = "english"
                self.assertEqual(
                    cell[language]["counted_pairs"], counted,
                    (code, budget),
                )
                self.assertEqual(
                    cell["latin"]["counted_pairs"], counted, (code, budget)
                )

    def test_the_verdict_rule_holds_and_no_rung_separates(self) -> None:
        for code in FILES:
            for language in LANGS:
                roll = self.artifact["files"][code][language]
                separated = []
                for budget in homo.LADDER_BUDGETS:
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    verdict = cell["verdict"]
                    if cell["real_held_mean_nats"] >= cell["band_min"]:
                        expected = "consistent-with-substitution"
                    elif (
                        cell["real_held_mean_nats"]
                        <= max(cell["floors_held_mean_nats"])
                    ):
                        expected = "not-consistent"
                    else:
                        expected = "below-held-band"
                    self.assertEqual(verdict, expected)
                    if verdict != "consistent-with-substitution":
                        separated.append(str(budget))
                self.assertEqual(
                    roll["rungs_separated_from_the_band"], separated
                )
                self.assertFalse(roll["any_rung_separates"])

    def test_every_floor_stays_below_the_real_at_every_rung(self) -> None:
        for code in FILES:
            for language in LANGS:
                for budget in homo.LADDER_BUDGETS:
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    real = cell["real_held_mean_nats"]
                    for value in cell["floors_held_mean_nats"]:
                        self.assertLess(value, real)
                self.assertTrue(
                    self.artifact["files"][code][language][
                        "floors_below_real_all_rungs"
                    ]
                )

    def test_the_plant_parity_rule_holds_at_every_rung(self) -> None:
        for code in FILES:
            for language in LANGS:
                for budget in homo.LADDER_BUDGETS:
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    anchor = cell["plant_parity_anchor_mean_nats"]
                    for value, flag in zip(
                        cell["self_plants_held_mean_nats"],
                        cell["self_plants_at_parity"],
                    ):
                        self.assertEqual(
                            flag, bool(value >= anchor - 0.0001)
                        )
                    excesses = cell["machinery_above_anchor_excesses"]
                    for value, excess in zip(
                        cell["self_plants_held_mean_nats"], excesses
                    ):
                        self.assertEqual(
                            round(value - anchor, 4), excess
                        )
                self.assertTrue(
                    self.artifact["files"][code][language][
                        "plant_parity_all_rungs"
                    ]
                )

    def test_no_machinery_call_hits_the_cap_anywhere(self) -> None:
        def scan(node: object, path: str) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key.endswith("_hit") or "sweep_budget_hits" in key:
                        flat = [value] if isinstance(value, bool) else value
                        for flag in flat:
                            self.assertFalse(
                                flag, f"{path}/{key}"
                            )
                    scan(value, f"{path}/{key}")
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    scan(item, f"{path}[{index}]")

        scan(self.artifact, "artifact")

    def test_the_selected_draw_rule_holds_everywhere(self) -> None:
        for code in FILES:
            for language in LANGS:
                for budget in homo.LADDER_BUDGETS:
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    for member in cell["band"]:
                        climbs = member["draws_climb_exact"]
                        self.assertEqual(len(climbs), len(member["draws"]))
                        best = climbs[0]
                        selected = 0
                        for position, value in enumerate(climbs):
                            if value > best + 1e-12:
                                best = value
                                selected = position
                        self.assertEqual(
                            member["selected_draw_index"], selected
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
                            round(max(member["draws"])
                                  - min(member["draws"]), 4),
                        )

    def test_anchors_are_rung_invariant(self) -> None:
        for code in FILES:
            for language in LANGS:
                anchors = []
                climbs = []
                for budget in homo.LADDER_BUDGETS:
                    cell = (
                        self.artifact["rungs"][str(budget)][
                            "files"][code][language]
                    )
                    anchors.append(
                        cell["plant_parity_anchor_mean_nats"]
                    )
                    climbs.append(
                        cell["plant_climb_identity_mean_nats"]
                    )
                self.assertEqual(len(set(anchors)), 1)
                self.assertEqual(len(set(climbs)), 1)
                frozen_cell = self.frozen_held["files"][code][language]
                self.assertEqual(
                    anchors[0],
                    frozen_cell["plant_parity_anchor_mean_nats"],
                )
                self.assertEqual(
                    climbs[0],
                    frozen_cell["plant_climb_identity_mean_nats"],
                )

    def test_one_narrow_rung_real_recomputes_from_the_declared_seed(
        self,
    ) -> None:
        code, language, budget = "ZL", "english", 27
        table, letter_counts = homo.table_from_stream(
            homo._reference_stream(language)
        )
        stream = homo._ladder_real_stream(code, budget)
        first, second = homo._kept_pairs(
            stream["event_ids"], stream["kept_mask"]
        )
        climb_first, climb_second, score_first, score_second = (
            homo._split_pairs(first, second)
        )
        climb = homo._ladder_matrix_from_pairs(
            climb_first, climb_second, budget + 1
        )
        score = homo._ladder_matrix_from_pairs(
            score_first, score_second, budget + 1
        )
        rng = np.random.default_rng(
            homo._seed(
                homo.CELL_ID[code], homo.KIND_ID["real"],
                homo.LANG_ID[language], 0,
            )
        )
        held, _view, hit = homo.machinery_best_held(
            climb, score, table, letter_counts, rng,
            restarts=homo.N_RESTARTS,
        )
        cell = (
            self.artifact["rungs"][str(budget)]["files"][code][language]
        )
        self.assertFalse(hit)
        self.assertEqual(round(held, 4), cell["real_held_mean_nats"])
        self.assertEqual(cell["counted_pairs"], 218309)
        self.assertEqual(cell["climb_pairs"], 109155)
        self.assertEqual(cell["score_pairs"], 109154)

    def test_one_narrow_rung_band_first_draw_replays(self) -> None:
        code, language, budget = "ZL", "english", 33
        seed_index = 0
        table, letter_counts = homo.table_from_stream(
            homo._reference_stream(language)
        )
        truncated = homo._truncated_reference(
            code, language,
            file=homo.CROSS_REFERENCE_FILES[language][0],
        )
        groups = homo._partition_groups(truncated, budget)
        rng_enc = np.random.default_rng(
            homo._seed(
                homo.CELL_ID[code], homo.KIND_ID["homo_cross_enc"],
                homo.LANG_ID[language], seed_index,
            )
        )
        encoded = homo._encode(truncated, groups, rng_enc, budget)
        enc_first, enc_second = homo._full_pairs(encoded)
        e_climb_first, e_climb_second, e_score_first, e_score_second = (
            homo._split_pairs(enc_first, enc_second)
        )
        e_climb = homo._ladder_matrix_from_pairs(
            e_climb_first, e_climb_second, budget + 1
        )
        e_score = homo._ladder_matrix_from_pairs(
            e_score_first, e_score_second, budget + 1
        )
        rng_mach = np.random.default_rng(
            homo._seed(
                homo.CELL_ID[code], homo.KIND_ID["homo_cross_mach"],
                homo.LANG_ID[language], seed_index,
            )
        )
        held, _view, hit = homo.machinery_best_held(
            e_climb, e_score, table, letter_counts, rng_mach,
            restarts=homo.N_RESTARTS,
        )
        self.assertFalse(hit)
        member = (
            self.artifact["rungs"][str(budget)]["files"][code][language]
            ["band"][0]
        )
        self.assertEqual(round(held, 4), member["draws"][0])

    def test_the_declared_question_is_answered_in_the_artifact(self) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's margin above the band shrink as the surplus",
            declared["truthful_question"],
        )
        self.assertIn(
            "does any rung separate the real from the band",
            declared["truthful_question"],
        )
        self.assertIn("exclusion format is not re-scoped", declared[
            "exclusion_rule"
        ])
        self.assertEqual(declared["rungs"], [36, 33, 30, 27])
        self.assertIn(
            "glyph characters up to B, ranked by the declared",
            declared["budget_rule"],
        )
        for code in FILES:
            for language in LANGS:
                roll = self.artifact["files"][code][language]
                self.assertFalse(roll["any_rung_separates"])

    def test_no_dash_in_the_artifact_or_the_module(self) -> None:
        text = ARTIFACT.read_text()
        self.assertNotIn("\u2013", text)
        self.assertNotIn("\u2014", text)
        module = Path(homo.__file__).read_text()
        self.assertNotIn("\u2013", module)
        self.assertNotIn("\u2014", module)
