"""User input errors stay concise at the main command boundary."""

import contextlib
import io
import json
import unittest
from unittest import mock

from engine.cli import main


class CliControlsTest(unittest.TestCase):
    def test_training_cli_forwards_explicit_warm_start_without_running_training(self):
        for enabled, rate in ((False, .01), (True, .0003)):
            arguments = ["train-router", "--samples", "256", "--epochs", "250",
                         "--hidden", "96", "--ensemble-size", "3", "--dry-run"]
            if enabled:
                arguments.append("--warm-start")
                arguments.extend(("--learning-rate", str(rate)))
            output = io.StringIO()
            with self.subTest(warm_start=enabled), contextlib.redirect_stdout(output), \
                 mock.patch("engine.neural_router_v2.train_router", return_value={"promoted": False}) as fit:
                self.assertEqual(main(arguments), 0)
                fit.assert_called_once_with(epochs=250, train_per_class=256, write=False,
                    expanded_families=False, hidden=96, ensemble_size=3, warm_start=enabled,
                    learning_rate=rate, feature_version=None)
            self.assertEqual(json.loads(output.getvalue()), {"promoted": False})

    def test_unified_registry_and_invocation_commands(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["tools"]), 0)
        self.assertTrue(any(item["name"] == "morse-constraints" for item in json.loads(output.getvalue())))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["run", "rsa-wiener", "1511", "--params", '{"modulus":8927,"exponent":2621}']), 0)
        self.assertEqual(json.loads(output.getvalue())["result"]["plaintext"], "41")

    def test_unified_commands_reject_bad_input_concisely(self):
        for arguments in (["run", "caesar", "ABC", "--params", "[]"],
                          ["run", "caesar", "ABC", "--params", "{"],
                          ["run", "unknown", "ABC"], ["route", "123"],
                          ["train-router", "--epochs", "0"]):
            stderr = io.StringIO()
            with self.subTest(arguments=arguments), contextlib.redirect_stderr(stderr):
                self.assertEqual(main(arguments), 2)
            self.assertNotIn("Traceback", stderr.getvalue())
    def test_empty_caesar_input_returns_an_error_without_a_traceback(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(main(["solve", "caesar", "123 !!!"]), 2)
        self.assertIn("no letters", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_keyed_helper_validation_returns_an_error_without_a_traceback(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(main(["solve", "keyed-vigenere", "ABC", "--key", "123",
                                   "--alphabet", "KRYPTOS"]), 2)
        self.assertTrue(stderr.getvalue().strip())
        self.assertNotIn("Traceback", stderr.getvalue())
