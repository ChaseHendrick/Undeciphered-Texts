"""K4 family-net prior: generator round trips, a tiny separable training run, K4 claims nothing."""

from __future__ import annotations

import random
import unittest

import numpy as np

from engine import k4_family_net as fn
from engine.solvers.k4_attempt import K4_CIPHERTEXT


class K4FamilyNetTest(unittest.TestCase):
    def test_round_trips(self) -> None:
        checks = fn.round_trip_checks(seed=3)
        self.assertTrue(all(checks.values()), checks)
        self.assertGreaterEqual(len(checks), 14)

    def test_generator_shapes_and_planted_clues(self) -> None:
        rng = random.Random(1)
        src = fn.region(fn.corpora()["english"], "train")
        plain = fn.plant(src[1000:1097])
        self.assertEqual(plain[21:34], "EASTNORTHEAST")
        self.assertEqual(plain[63:74], "BERLINCLOCK")
        for family in fn.FAMILIES:
            cipher = fn.encrypt_family(family, plain, rng, src[5000:5097])
            self.assertEqual(len(cipher), 97, family)
            self.assertRegex(cipher, "^[A-Z]{97}$")
        # Transposition keeps the letters; a planted periodic key shows in the crib features.
        self.assertEqual(sorted(fn.encrypt_family("columnar", plain, rng, "")), sorted(plain))
        from engine.ciphers import vigenere_encrypt
        F = fn.features([vigenere_encrypt(plain, "KEY")])
        per_start = fn.STAT_FEATURES + 24 + 2
        self.assertEqual(F[0, per_start + 2], 1.0)  # Vigenere key agrees on every period-3 pair

    def test_test_split_is_held_out(self) -> None:
        text = fn.corpora()["english"]
        train, test = fn.region(text, "train"), fn.region(text, "test")
        self.assertEqual(len(train) + len(test), len(text))
        self.assertNotIn(test[:200], train)

    def test_tiny_training_separates_two_easy_classes(self) -> None:
        families = ("random", "monoalphabetic")
        tr, ytr = fn.sample_texts(150, 7, "train", families)
        va, yva = fn.sample_texts(50, 8, "train", families)
        te, yte = fn.sample_texts(60, 9, "test", families)
        Ftr, Fva, Fte = fn.features(tr), fn.features(va), fn.features(te)
        ens, logs = fn.fit_ensemble(Ftr, ytr, Fva, yva, np.arange(Ftr.shape[1]), (1,), families,
                                    hidden=(16, 8), epochs=20, patience=4)
        result = fn.evaluate(ens, Fte, yte)
        self.assertGreaterEqual(result["ensemble_accuracy"], 0.95)
        self.assertEqual(len(logs), 1)

    def test_k4_report_claims_nothing(self) -> None:
        report = fn.run(train_per_class=20, val_per_class=8, test_per_class=8, seeds=(1,), stats_seeds=(1,),
                        hidden=(8, 8), epochs=2, patience=1, verbose=False)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertIs(report["k4"]["solved"], False)
        self.assertIsNone(report["k4"]["claimed_plaintext"])
        post = report["k4"]["full"]["posterior"]
        self.assertEqual(set(post), set(fn.FAMILIES))
        self.assertAlmostEqual(sum(v["mean"] for v in post.values()), 1.0, places=2)
        self.assertNotIn("plaintext", report["k4"]["full"])
        self.assertEqual(len(K4_CIPHERTEXT), 97)
        self.assertIn("not a K4 decipherment", fn.__doc__)
        self.assertTrue(fn.__doc__.rstrip().endswith(
            "This is not a K4 decipherment. solved stays false. claimed_plaintext stays None."))


if __name__ == "__main__":
    unittest.main()
