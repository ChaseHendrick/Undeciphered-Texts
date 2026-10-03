"""CLI and registry contracts for connected research tools."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch

from engine.cli import main
from engine.tool_registry import list_tools, run_tool


class ResearchToolIntegrationTest(unittest.TestCase):
    def test_composition_tool_recovers_published_autokey_vector_without_key(self):
        # ACA's plaintext-autokey example, with a single aligned known letter.
        report = run_tool("k4-models", "EHPFSFEBHMHPF", params={
            "cribs": [{"offset": 4, "plaintext": "O"}],
            "families": ["plaintext-autokey"],
            "alphabets": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
            "orders": ["substitute-then-transpose"], "max_period": 1,
        })
        identity = next(c for c in report["result"]["candidates"]
                        if c["layout"]["kind"] == "identity")
        self.assertEqual(identity["predicted_plaintext"], "TOBEORNOTTOBE")
        self.assertTrue(identity["re_encryption_matches"])
        self.assertIsNone(report["result"]["claimed_plaintext"])
        self.assertEqual(report["mode"], "conditional-crib-model-compositions")
        self.assertIn("cribs", next(t for t in list_tools()
                                   if t["name"] == "k4-models")["required_parameters"])

    def test_composition_cli_json_preserves_unknown_positions(self):
        output = io.StringIO()
        params = {"cribs": [{"offset": 0, "plaintext": "A"}],
                  "families": ["repeating"], "max_period": 4,
                  "alphabets": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"], "max_candidates": 1000}
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["run", "k4-models", "BCDEFGHI",
                                   "--params", json.dumps(params)]), 0)
        report = json.loads(output.getvalue())["result"]
        candidate = next(c for c in report["candidates"]
                         if c["layout"]["kind"] == "identity" and c["period"] == 4)
        self.assertEqual(candidate["predicted_plaintext"], "A???E???")
        self.assertIsNone(candidate["re_encryption_matches"])
        self.assertEqual(candidate["compatible_key_completions"], 26 ** 3)

    def test_composition_adapter_rejects_missing_clues_and_excessive_budget(self):
        for params in ({}, {"cribs": [{"offset": 0, "plaintext": "A"}],
                            "max_checks": 10001}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                run_tool("k4-models", "ABCD", params=params)

    def test_training_cli_forwards_distillation_without_writing_in_dry_run(self):
        with patch("engine.neural_router_v2.train_router", return_value={"accepted": False}) as train:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["train-router", "--warm-start", "--dry-run",
                                       "--distillation-strength", "0.1",
                                       "--distillation-temperature", "2",
                                       "--learning-rate", "0.0003"]), 0)
        self.assertEqual(train.call_args.kwargs["distillation_strength"], .1)
        self.assertEqual(train.call_args.kwargs["distillation_temperature"], 2)
        self.assertEqual(train.call_args.kwargs["learning_rate"], .0003)
        self.assertTrue(train.call_args.kwargs["warm_start"])
        self.assertFalse(train.call_args.kwargs["write"])


if __name__ == "__main__":
    unittest.main()
