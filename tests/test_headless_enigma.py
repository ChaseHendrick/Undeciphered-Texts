"""The headless army Enigma reproduces a known message and claims no open one."""

from __future__ import annotations

import unittest

from engine.headless_enigma import HeadlessEnigma, search_open_messages
from engine.solvers.enigma import WIKIPEDIA_CIPHER, WIKIPEDIA_PLAIN


class HeadlessEnigmaTest(unittest.TestCase):
    def test_known_message_and_a_stepped_hole(self) -> None:
        machine = HeadlessEnigma(("I", "II", "III"), "AAA", "", "B")
        self.assertEqual(machine.feed("AAA", WIKIPEDIA_PLAIN), WIKIPEDIA_CIPHER)
        cipher = machine.feed("AAA", "ABCD")
        self.assertEqual(machine.feed("AAA", cipher[0] + "-" + cipher[2:]), "A?CD")

    def test_published_keys_do_not_read_the_open_messages(self) -> None:
        report = search_open_messages()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["control_start"], "WER")
        self.assertEqual(report["control_text"], "BETRIEBSSPRUQXKUPPLU")
        self.assertEqual(report["rows_beating_control"], 0)
        self.assertEqual(len(report["rows"]), 18)
        by_key = {(row["message"], row["key_date"]): row for row in report["rows"]}
        self.assertEqual(by_key[("LXACA", "1941-07-05")]["start"], "LXI")
        self.assertIsNone(by_key[("KLJBO", "1941-07-05")]["mean_score"])
        self.assertEqual(by_key[("KLJBO", "1941-07-05")]["holes"], 4)
        self.assertFalse(by_key[("JBIYH", "1941-07-09")]["beats_control"])
        self.assertNotIn("1941-07-03", {row["key_date"] for row in report["rows"]})
        self.assertNotIn("1941-07-20", {row["key_date"] for row in report["rows"]})


if __name__ == "__main__":
    unittest.main()
