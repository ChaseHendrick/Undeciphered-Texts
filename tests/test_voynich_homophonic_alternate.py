"""Tests for the declared alternate reference corpora of family 5.

The frozen artifact pins the measurement; the reproducibility tests
recompute the first cell's facts through the alternate reference and
the language models from the declared alternate streams; the
mechanical tests nail the declared rules on the stored artifact: the
alternate declarations, the bridge gate (116 fields), the models
block, the streams, the roll-up (margins as arithmetic, verdict rule,
floor positions, plant parity, cap flags, selected draws with exact
climbs), the declared question answered (all six margins positive and
their four-decimal deltas against the frozen widened band), the band
members' identity fields replaying the frozen artifact, the leave-
one-out spot check on the alternate stream, the corpus facts roster
with recomputed sha256 provenance, the declared rejections and the
probed-not-selected candidates with cause, the same-work-family
disclosure, and the dash bans. Nothing here reads the manuscript
beyond the frozen artifacts and the declared streams.
"""

from __future__ import annotations

import hashlib
import json
import math
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine.voynich_substitution import DATA_DIR, FILES, LANGS

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-alternate-reference.json"
).resolve()
FROZEN_WIDENED = Path(
    "docs/research-notes/voynich-homophonic-widened-band.json"
).resolve()

# The frozen alternate-reference artifact's headline (code, language)
# -> (real_held, band_min, band_max, margin, verdict, anchor, members),
# pinned from the artifact measured 22 October 2026 with the bridge
# gate verified at 116 fields.
FROZEN = {
    ("ZL", "english"): (-4.3116, -4.7827, -4.6287, 0.4711,
                        "consistent-with-substitution", -5.0298, 7),
    ("ZL", "latin"): (-4.4074, -4.6022, -4.562, 0.1948,
                      "consistent-with-substitution", -5.1053, 8),
    ("IT", "english"): (-4.3023, -4.7151, -4.6315, 0.4128,
                        "consistent-with-substitution", -5.0288, 7),
    ("IT", "latin"): (-4.4059, -4.6022, -4.562, 0.1963,
                      "consistent-with-substitution", -5.1067, 8),
    ("GC", "english"): (-4.2755, -4.6966, -4.642, 0.4211,
                        "consistent-with-substitution", -5.0251, 7),
    ("GC", "latin"): (-4.4062, -4.6635, -4.5575, 0.2573,
                      "consistent-with-substitution", -5.1107, 8),
}

# The frozen widened band's margins, for the declared question's
# delta assertions: the real rebuilt under the alternate references.
WIDENED_MARGINS = {
    ("ZL", "english"): 0.3502,
    ("ZL", "latin"): 0.25,
    ("IT", "english"): 0.3644,
    ("IT", "latin"): 0.2552,
    ("GC", "english"): 0.3591,
    ("GC", "latin"): 0.2255,
}

ALTERNATES = {
    "english": ("substref_english9_pg76.txt", 76,
                "Adventures of Huckleberry Finn (Twain)"),
    "latin": ("substref_latin10_pg60772.txt", 60772,
              "Evagatorium volumen secundum (Fabri)"),
}

STREAM_FACTS = {
    "english": (545629, 427847, 117782, None),
    "latin": (1138187, 968923, 169264, 12),
}


class AlternateReferenceTest(unittest.TestCase):
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

    def test_the_alternate_reference_declaration(self) -> None:
        for language in LANGS:
            name, ebook, label = homo.ALTERNATE_REFERENCE_FILES[language]
            self.assertEqual((name, ebook, label), ALTERNATES[language])
            roster = self.artifact["declared"]["corpus_facts"][language]
            self.assertEqual(len(roster), 1, language)
            self.assertEqual(roster[0]["ebook"], ebook, language)
            # the declared alternates stand outside every wider band
            # membership list, both directions
            band_names = {
                member[0]
                for member in homo._extended_reference_members(language)
            }
            self.assertNotIn(name, band_names, language)
            for member_name in band_names:
                statement = self.artifact["declared"][
                    "corpus_facts"
                ].keys()
                self.assertTrue(statement)
        references = {entry[0] for entry in
                      list(homo.REFERENCE_FILES.values())}
        self.assertTrue(references)

    def test_the_bridge_gate_stands_in_the_artifact(self) -> None:
        check = self.artifact["bridge_gate"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(check["fields_compared"], 116)
        self.assertIn("field for field",
                      self.artifact["declared"]["bridge_gate"])
        self.assertIn("standing reference supplied",
                      self.artifact["declared"]["bridge_gate"])

    def test_the_models_block_carries_the_alternate_facts(self) -> None:
        for language in LANGS:
            name, ebook, _label = ALTERNATES[language]
            stream = homo._reference_stream(language, file=name)
            model = homo._alternate_table(language)
            table = model["table"]
            full = homo._stream_matrix_27(stream)
            stored = self.artifact["declared"]["models"][language]
            clean = float((full * table).sum()) / float(full.sum())
            block_held, block_climb, _bcp, _bsp = (
                homo._block_identity_half_means(stream, table)
            )
            queued, _acm, _acp, _asp = homo._identity_half_means(
                stream, model["add_one_table"]
            )
            self.assertEqual(stored["file"], name)
            self.assertEqual(stored["ebook"], ebook)
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
            self.assertEqual(
                stored["add_one_parity_score_half_mean_nats_per_pair"],
                round(queued, 4),
            )
            self.assertEqual(
                stored["pair_types_present"], model["pair_types_present"]
            )
            self.assertEqual(
                stored["total_pairs"], model["total_pairs"]
            )
            self.assertEqual(
                stored["max_abs_entry_delta"], model["max_abs_entry_delta"]
            )
            self.assertEqual(
                stored["max_delta_type"], model["max_delta_type"]
            )
            self.assertEqual(
                stored["mean_entry_delta_over_present"],
                model["mean_entry_delta_over_present"],
            )

    def test_the_leave_one_out_form_recomputes_from_the_stream(
        self,
    ) -> None:
        name, _ebook, _label = ALTERNATES["english"]
        stream = homo._reference_stream("english", file=name)
        ids = np.array(stream, dtype=np.int64)
        matrix = np.zeros((27, 27))
        np.add.at(matrix, (ids[:-1], ids[1:]), 1.0)
        total = int(matrix.sum())
        self.assertEqual(total, 545628)
        model = homo._alternate_table("english")
        # a present type prices one occurrence removed: log(n/N+728)
        row, col = 1, 12
        present_value = model["table"][row, col]
        self.assertEqual(
            round(present_value, 6),
            round(float(math.log(matrix[row, col] / float(total + 728.0))),
                  6),
        )
        self.assertEqual(
            round(model["add_one_table"][row, col], 6),
            round(float(math.log((matrix[row, col] + 1.0)
                                 / float(total + 729.0))), 6),
        )
        # an absent type keeps the inherited add-one floor
        absent = np.argwhere(matrix == 0.0)[0]
        row, col = int(absent[0]), int(absent[1])
        self.assertEqual(
            round(model["table"][row, col], 6),
            round(float(math.log(1.0 / float(total + 729.0))), 6),
        )
        _add_one, letter_counts = __import__(
            "engine.voynich_substitution",
            fromlist=["table_from_stream"],
        ).table_from_stream(stream)
        self.assertTrue(np.array_equal(model["letter_counts"],
                                       letter_counts))

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
                [name for name, _ebook in
                 homo._extended_reference_members(language)],
            )

    def test_the_margins_answer_the_declared_question(self) -> None:
        # every verdict keeps the frozen widened band's verdict under
        # the alternate references, and every margin stays positive
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
        # the four cells whose margins deepen or hold, declared
        for key in (("ZL", "english"), ("IT", "english"),
                    ("GC", "english"), ("GC", "latin")):
            self.assertGreaterEqual(
                self.artifact["files"][key[0]][key[1]]
                ["real_margin_over_band_min"],
                WIDENED_MARGINS[key], key,
            )
        # the two latin cells that ease stay well above the floors and
        # above every declared concern: 0.1948 and 0.1963
        for key in (("ZL", "latin"), ("IT", "latin")):
            self.assertGreaterEqual(
                self.artifact["files"][key[0]][key[1]]
                ["real_margin_over_band_min"], 0.19, key,
            )
        # the declared headline: the widest margin of this measurement
        self.assertEqual(
            self.artifact["files"]["ZL"]["english"]
            ["real_margin_over_band_min"], 0.4711,
        )

    def test_the_streams_are_the_frozen_streams(self) -> None:
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
                    cell["climb_pairs"] + cell["score_pairs"],
                    cell["counted_pairs"],
                )

    def test_band_members_replay_their_frozen_identity(self) -> None:
        for code in FILES:
            for language in LANGS:
                cell = self.artifact["files"][code][language]
                widened = self.frozen_widened["files"][code][language]
                for index, (fresh, stored) in enumerate(
                    zip(cell["band"], widened["band"])
                ):
                    # the identity fields replay; the draw that wins the
                    # selection is re-priced under the alternate table
                    # and is not expected to stay the same draw
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
                    0.71, (code, language),
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
                    self.assertGreater(excess, 0.32)
                    self.assertLess(excess, 0.55)

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

    def test_one_alternate_cell_recomputes_from_kinds(self) -> None:
        code, language = "ZL", "english"
        name, _ebook, _label = ALTERNATES[language]
        model = homo._alternate_table(language)
        facts = homo._block_cell_facts(
            code, language, model["table"], model["letter_counts"],
            reference_file=name,
        )
        stored = self.artifact["files"][code][language]
        for key, value in facts.items():
            self.assertEqual(
                stored[homo._CELL_FIELD_MAP[key]], value,
                (code, language, key),
            )

    def test_the_corpus_facts_record_the_alternate_provenance(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        for language in LANGS:
            name, _ebook, _label = ALTERNATES[language]
            stream, letters, boundary, hits = STREAM_FACTS[language]
            facts = declared["corpus_facts"][language]
            self.assertEqual(len(facts), 1, language)
            entry = facts[0]
            self.assertEqual(entry["file"], name)
            self.assertEqual(entry["stream_length"], stream)
            self.assertEqual(entry["letter_tokens"], letters)
            self.assertEqual(entry["boundary_tokens"], boundary)
            self.assertEqual(entry["english_scaffold_hits"], hits)
            self.assertEqual(entry["types_present"], 27)
            raw = (Path(DATA_DIR).resolve().parent / name).read_bytes()
            self.assertEqual(
                entry["sha256"], hashlib.sha256(raw).hexdigest(), name
            )
        self.assertIn("Huckleberry",
                      declared["corpus_facts"]["english"][0]["label"])
        self.assertIn("Evagatorium",
                      declared["corpus_facts"]["latin"][0]["label"])

    def test_the_rejected_candidates_are_declared_with_cause(self) -> None:
        rejected = self.artifact["declared"]["rejected_candidates"]
        ebooks = sorted(entry["ebook"] for entry in rejected)
        self.assertEqual(ebooks, sorted([9090, 66595, 16400]))
        for entry in rejected:
            self.assertTrue(entry["cause"].strip(), entry["ebook"])
            self.assertTrue(entry["label"].strip(), entry["ebook"])
        varro = next(entry for entry in rejected if entry["ebook"] == 16400)
        self.assertIn("Most fragments have three elements", varro["cause"])
        tacitus = next(entry for entry in rejected if entry["ebook"] == 9090)
        self.assertIn("5,109", tacitus["cause"])
        ancyranum = next(entry for entry in rejected
                         if entry["ebook"] == 66595)
        self.assertIn("2,813", ancyranum["cause"])

    def test_the_probed_not_selected_are_declared_with_cause(self) -> None:
        probed = self.artifact["declared"]["probed_not_selected"]
        ebooks = sorted(entry["ebook"] for entry in probed)
        self.assertEqual(ebooks, sorted([345, 20771]))
        for entry in probed:
            self.assertTrue(entry["cause"].strip(), entry["ebook"])
            self.assertTrue(entry["label"].strip(), entry["ebook"])
        dracula = next(entry for entry in probed if entry["ebook"] == 345)
        self.assertIn("one alternate reference per language",
                      dracula["cause"])
        linnaeus = next(entry for entry in probed
                        if entry["ebook"] == 20771)
        self.assertIn("terse nominal taxonomic description",
                      linnaeus["cause"])

    def test_the_declared_question_is_answered_in_the_artifact(
        self,
    ) -> None:
        declared = self.artifact["declared"]
        self.assertIn(
            "does the real's held-out score-half value still stand "
            "above the band when the scored tables are rebuilt from "
            "single alternate references outside the band",
            declared["truthful_question"],
        )
        self.assertIn(
            "byte-identical replays", declared["measured_facts_rule"]
        )
        self.assertIn(
            "only the scored tables change",
            declared["measured_facts_rule"],
        )
        self.assertIn("draws_climb_exact", declared["band_record_rule"])
        self.assertIn("unconditional", declared["band_record_rule"])
        self.assertIn("0 to 52", declared["corpus_rule"])
        self.assertIn("rejected with cause", declared["corpus_rule"])
        self.assertIn(
            "carried exactly onto the declared alternate reference's "
            "counts", declared["loo_rule"]
        )
        self.assertIn(
            "do not restate the widened band's verdicts",
            declared["verdict_rule"],
        )
        self.assertIn("not re-scoped", declared["exclusion_rule"])
        self.assertIn(
            "volume two of the same printed travel account",
            declared["same_work_family_rule"],
        )
        self.assertIn(
            "pg58528", declared["same_work_family_rule"]
        )

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
