"""Planted-run test for the run-slot score.

The corpus is synthetic. A passing rank is not a reading of any ancient script.
"""

from __future__ import annotations

import random
import unittest
from pathlib import Path

from engine.run_slot_score import (
    NOT_A_DECIPHERMENT,
    ORIGINAL_TO_THIS_REPO,
    maximal_runs,
    position_bias,
    rank_run_slot,
    rank_run_slot_stream,
    run_slot_score,
)


PLANTED = "RPT"
BACKGROUND = ("B0", "B1", "B2", "B3", "B4", "B5")


def planted_repeating_corpus() -> list[list[str]]:
    """Twelve lines. RPT repeats four times at column 0. Others never repeat.

    Background labels are a rotation of invented tokens. Adjacent background
    tokens are distinct, and runs do not cross lines, so every background sign
    has repeat length 1. Labels are not a historical sign list.
    """
    spans: list[list[str]] = []
    for i in range(12):
        tail = [BACKGROUND[(i + col) % len(BACKGROUND)] for col in range(4)]
        spans.append([PLANTED, PLANTED, PLANTED, PLANTED, *tail])
    return spans


def _random_background_corpus(seed: int) -> list[list[str]]:
    """Same planted run, with a random non-repeating tail.

    Neighbors in the tail differ, so no background sign can reach repeat
    length 2. The planted run stays length 4 and always starts at column 0.
    """
    rng = random.Random(seed)
    alphabet = [f"N{i}" for i in range(16)]
    spans: list[list[str]] = []
    for _ in range(40):
        tail: list[str] = []
        for _col in range(6):
            choices = [sign for sign in alphabet if not tail or sign != tail[-1]]
            tail.append(rng.choice(choices))
        spans.append([PLANTED, PLANTED, PLANTED, PLANTED, *tail])
    return spans


class RunSlotScoreTest(unittest.TestCase):
    def test_planted_repeating_sign_ranks_above_random_signs(self) -> None:
        ranked = rank_run_slot(planted_repeating_corpus())
        self.assertGreaterEqual(len(ranked), 2)
        top = ranked[0]
        self.assertEqual(top.sign, PLANTED)
        self.assertEqual(top.repeat_length, 4)
        self.assertEqual(top.peak_start_slot, 0)
        self.assertAlmostEqual(top.position_bias, 1.0, places=9)
        self.assertAlmostEqual(top.run_slot_score, 8.0, places=9)
        for other in ranked[1:]:
            self.assertNotEqual(other.sign, PLANTED)
            self.assertEqual(other.repeat_length, 1)
            self.assertLess(other.run_slot_score, top.run_slot_score)

    def test_planted_sign_beats_random_tails_on_every_seed(self) -> None:
        for seed in range(20):
            ranked = rank_run_slot(_random_background_corpus(seed))
            self.assertEqual(ranked[0].sign, PLANTED, msg=f"seed {seed}")
            self.assertGreater(
                ranked[0].run_slot_score,
                ranked[1].run_slot_score,
                msg=f"seed {seed}",
            )

    def test_both_terms_change_the_rank(self) -> None:
        # Every span has width 6. LOCKED repeats twice and always starts at
        # column 0, so its bias is 1 and its score is 4. SPREAD repeats three
        # times, with equal starts at columns 0, 1, and 2. Against six columns
        # that peak share is only 1/3, bias is 0.2, and the score is 3.6.
        # Repeat length alone would rank SPREAD first. The combined score does not.
        spans = [
            ["SPREAD", "SPREAD", "SPREAD", "A0", "B0", "C0"],
            ["SPREAD", "SPREAD", "SPREAD", "A1", "B1", "C1"],
            ["D0", "SPREAD", "SPREAD", "SPREAD", "E0", "F0"],
            ["D1", "SPREAD", "SPREAD", "SPREAD", "E1", "F1"],
            ["LOCKED", "LOCKED", "SPREAD", "SPREAD", "SPREAD", "G0"],
            ["LOCKED", "LOCKED", "SPREAD", "SPREAD", "SPREAD", "G1"],
        ]
        ranked = {row.sign: row for row in rank_run_slot(spans)}
        self.assertEqual(ranked["LOCKED"].repeat_length, 2)
        self.assertAlmostEqual(ranked["LOCKED"].position_bias, 1.0, places=9)
        self.assertAlmostEqual(ranked["LOCKED"].run_slot_score, 4.0, places=9)
        self.assertEqual(ranked["SPREAD"].repeat_length, 3)
        self.assertAlmostEqual(ranked["SPREAD"].peak_share, 1.0 / 3.0, places=9)
        self.assertAlmostEqual(ranked["SPREAD"].position_bias, 0.2, places=9)
        self.assertAlmostEqual(ranked["SPREAD"].run_slot_score, 3.6, places=9)
        self.assertGreater(
            ranked["LOCKED"].run_slot_score,
            ranked["SPREAD"].run_slot_score,
        )

    def test_runs_do_not_cross_span_boundaries(self) -> None:
        spans = [["RPT", "RPT"], ["RPT", "RPT"]]
        grouped = rank_run_slot(spans)
        self.assertEqual(grouped[0].repeat_length, 2)
        self.assertEqual(grouped[0].run_count, 2)
        flat = rank_run_slot_stream([sign for span in spans for sign in span])
        self.assertEqual(flat[0].repeat_length, 4)
        self.assertEqual(flat[0].run_count, 1)

    def test_empty_and_single_column(self) -> None:
        self.assertEqual(rank_run_slot([]), [])
        self.assertEqual(rank_run_slot([[], []]), [])
        self.assertEqual(rank_run_slot_stream([]), [])
        only = rank_run_slot_stream(["S"])
        self.assertEqual(len(only), 1)
        self.assertEqual(only[0].repeat_length, 1)
        self.assertEqual(only[0].slot_count, 1)
        self.assertEqual(only[0].position_bias, 0.0)
        self.assertEqual(only[0].run_slot_score, 1.0)
        runs = maximal_runs(["A", "A", "B", "A"])
        self.assertEqual(
            [(run.sign, run.length, run.start) for run in runs],
            [("A", 2, 0), ("B", 1, 2), ("A", 1, 3)],
        )

    def test_formula_matches_the_definition(self) -> None:
        self.assertAlmostEqual(position_bias(1.0, 8), 1.0, places=9)
        self.assertAlmostEqual(position_bias(0.125, 8), 0.0, places=9)
        self.assertEqual(position_bias(1.0, 1), 0.0)
        self.assertAlmostEqual(run_slot_score(4, 1.0), 8.0, places=9)
        self.assertAlmostEqual(run_slot_score(1, 0.0), 1.0, places=9)

    def test_module_states_original_and_not_a_decipherment(self) -> None:
        import engine.run_slot_score as mod

        doc = mod.__doc__ or ""
        self.assertIn("original to this repository", doc)
        self.assertIn("does not decipher", doc)
        self.assertIn("Voynich", doc)
        self.assertIn("Linear A", doc)
        self.assertIn("original to this repository", ORIGINAL_TO_THIS_REPO)
        self.assertIn("does not decipher", NOT_A_DECIPHERMENT)
        page = Path(__file__).resolve().parents[1] / "docs" / "run-slot-score.md"
        text = page.read_text(encoding="utf-8")
        self.assertIn("original to this repository", text)
        self.assertIn("does not decipher", text)
        self.assertIn("not a decipherment of an ancient script", text.lower())


if __name__ == "__main__":
    unittest.main()
