"""User input errors stay concise at the main command boundary."""

import contextlib
import io
import unittest

from engine.cli import main


class CliControlsTest(unittest.TestCase):
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
