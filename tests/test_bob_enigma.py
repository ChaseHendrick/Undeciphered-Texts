"""The bounded Enigma trial separates Enigma from Bob's other families."""

from __future__ import annotations

import unittest

import numpy as np

from engine.bob_enigma import bob_enigma_report
from engine.neural_enigma_features import FEATURE_COUNT, enigma_trial
from engine.neural_features import feature_tables
from engine.neural_grade import _english_unigram, letters_az, load_training_prose
from engine.solvers.enigma import enigma_encrypt


class BobEnigmaTest(unittest.TestCase):
    def test_a_known_setting_is_found(self) -> None:
        prose = letters_az(load_training_prose())
        training = prose[: int(len(prose) * 0.6)]
        tables = feature_tables(training, _english_unigram(training))
        plain = training[5000:5150]
        cipher = enigma_encrypt(plain, rotors=("I", "II", "III"), reflector="B", rings="AAA",
                                positions="AAD", plugboard=[])
        values = np.array([ord(ch) - 65 for ch in cipher], dtype=np.int64)
        found = enigma_trial(values, tables["logdig"], np.log(np.asarray(tables["english"])))
        # Right rotor at D steps to E before the first letter; III carries from V, at letter 18.
        self.assertEqual(found["setting"], (("I", "II", "III"), (0, 0, 4), 8))
        self.assertGreater(found["pair_z"], 8)
        self.assertEqual(FEATURE_COUNT, 3)

    def test_enigma_stands_apart(self) -> None:
        report = bob_enigma_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["families"], 20)
        self.assertEqual(report["enigma_lowest_z"], 12.62)
        self.assertEqual(report["others_highest_z"], 5.74)
        self.assertTrue(report["separated"])


if __name__ == "__main__":
    unittest.main()
