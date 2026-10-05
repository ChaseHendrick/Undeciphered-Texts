"""The substitution drill missed because of the small model, not the steps."""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.ciphers import substitution_encrypt
from engine.cli import build_parser
from engine.language import get_large_model
from engine.neural import load_training_prose
from engine.neural_grade import letters_az
from engine.solver_model import solver_model_report
from engine.solvers.substitution import solve_substitution

_DOYLE = Path(__file__).resolve().parents[1] / "engine" / "data" / "neural_heldout_doyle.txt"


def _right(plaintext: str, original: str) -> int:
    found = "".join(ch for ch in plaintext if ch.isalpha()).upper()
    return sum(left == right for left, right in zip(found, original))


class SolverModelTest(unittest.TestCase):
    def test_the_frozen_drill_blames_the_model(self) -> None:
        report = solver_model_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["default_changed"])
        arms = {(arm["model"], arm["width"]): arm for arm in report["arms"]}
        self.assertEqual(arms[("small", 100)]["nine_tenths_right"], 1)
        self.assertEqual(arms[("small", 100)]["misses_the_model_prefers"], 5)
        self.assertEqual(arms[("small", 200)]["nine_tenths_right"], 5)
        self.assertEqual(arms[("large", 100)]["nine_tenths_right"], 7)
        self.assertEqual(arms[("large", 200)]["nine_tenths_right"], 8)
        for width in (100, 200):
            self.assertEqual(arms[("large", width)]["misses_the_model_prefers"], 0)
        self.assertEqual(arms[("large", 200)]["model_letters"], 1916398)

    def test_the_large_model_reads_a_held_out_window_the_default_misses(self) -> None:
        original = letters_az(load_training_prose(_DOYLE))[3000:3150]
        cipher = substitution_encrypt(original, "QWERTYUIOPASDFGHJKLZXCVBNM")
        large = solve_substitution(cipher, restarts=30, temperature=10.0, model=get_large_model())
        self.assertGreaterEqual(_right(large.plaintext, original), 145)
        self.assertEqual(large.details["model_letters"], 1916398)
        small = solve_substitution(cipher)
        self.assertLess(_right(small.plaintext, original), 100)

    def test_the_cli_passes_the_large_model(self) -> None:
        args = build_parser().parse_args(
            ["solve", "substitution", "ABC", "--model", "large", "--restarts", "30", "--temperature", "10"]
        )
        self.assertEqual((args.model, args.restarts, args.temperature), ("large", 30, 10.0))
        self.assertEqual(build_parser().parse_args(["solve", "substitution", "ABC"]).model, "small")


if __name__ == "__main__":
    unittest.main()
