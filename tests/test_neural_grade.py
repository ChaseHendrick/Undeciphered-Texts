"""Held-out grade for the trigram letter model and the cipher-family router.

The metrics are recomputed from the Austen / Doyle / Grimm split. The test
fails if the held-out English letter string is inside the training letters,
and if a fit is asked to train on the held-out prose itself.
"""

from __future__ import annotations

import hashlib
import json
import unittest

from engine.neural import load_training_prose
from engine.neural_grade import (
    CERTIFICATE_PATH,
    HELD_DE_PATH,
    HELD_EN_PATH,
    HELD_DE_TEXT_URL,
    HELD_DE_URL,
    HELD_EN_TEXT_URL,
    HELD_EN_URL,
    METRICS_PATH,
    TRAIN_PATH,
    TRAIN_TEXT_URL,
    TRAIN_URL,
    assert_certificate_plaintexts_excluded,
    assert_split,
    certificate_letter_strings,
    evaluate,
    language_preference,
    letters_az,
    metrics_sha256,
    router_chance_baseline,
    sha256_text,
    three_way_chance_baseline,
)


class NeuralGradeTest(unittest.TestCase):
    def test_held_out_metrics_beat_chance_and_match_the_certificate(self) -> None:
        report = evaluate()
        language = report["language_scorer"]
        router = report["solver_router"]
        windows = language["windows"]
        self.assertGreater(windows, 8)
        self.assertGreater(language["beats_shuffled"] / windows, language["shuffled_chance_baseline"])
        self.assertGreater(language["preference_accuracy"], language["chance_baseline"])
        self.assertAlmostEqual(language["chance_baseline"], three_way_chance_baseline(3), places=5)
        self.assertAlmostEqual(router["chance_baseline"], router_chance_baseline(), places=5)
        self.assertGreater(router["accuracy"], router["chance_baseline"])
        self.assertEqual(router["total"], router["test_per_class"] * len(router["families"]))
        shipped = report["shipped_solver_net"]
        self.assertIs(shipped["edited"], False)
        self.assertGreater(shipped["accuracy"], shipped["chance_baseline"])

        train = letters_az(load_training_prose(TRAIN_PATH))
        held = letters_az(load_training_prose(HELD_EN_PATH))
        self.assertGreater(len(train), 1000)
        self.assertGreater(len(held), 1000)
        self.assertNotIn(held, train)
        assert_split(train, held)
        assert_certificate_plaintexts_excluded(train, held)
        self.assertEqual(language["train_letters_sha256"], sha256_text(train))
        self.assertEqual(language["heldout_english_letters_sha256"], sha256_text(held))
        self.assertNotEqual(language["train_letters_sha256"], language["heldout_english_letters_sha256"])
        self.assertEqual(router["train_plaintext_sha256"], sha256_text(train))
        self.assertEqual(router["heldout_plaintext_sha256"], sha256_text(held))
        self.assertEqual(shipped["heldout_plaintext_sha256"], sha256_text(held))
        self.assertEqual(language["train_source"]["url"], TRAIN_URL)
        self.assertEqual(language["train_source"]["text_url"], TRAIN_TEXT_URL)
        self.assertEqual(language["heldout_english_source"]["url"], HELD_EN_URL)
        self.assertEqual(language["heldout_english_source"]["text_url"], HELD_EN_TEXT_URL)
        self.assertEqual(language["heldout_german_source"]["url"], HELD_DE_URL)
        self.assertEqual(language["heldout_german_source"]["text_url"], HELD_DE_TEXT_URL)

        raw = METRICS_PATH.read_bytes()
        saved = json.loads(raw.decode("utf-8"))
        certificate = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(metrics_sha256(METRICS_PATH), hashlib.sha256(raw).hexdigest())
        self.assertEqual(certificate["metrics_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(certificate["metrics_file"], "engine/data/neural_grade_metrics.json")

        if language["backend"] == saved["language_scorer"]["backend"]:
            for key in (
                "preference_correct",
                "windows",
                "beats_shuffled",
                "beats_german",
                "train_events",
            ):
                self.assertEqual(language[key], saved["language_scorer"][key])
            self.assertLess(
                language["mean_log_loss_english"],
                language["mean_log_loss_shuffled"],
            )
            self.assertLess(
                language["mean_log_loss_english"],
                language["mean_log_loss_german"],
            )
            for key in (
                "mean_log_loss_english",
                "mean_log_loss_shuffled",
                "mean_log_loss_german",
                "preference_accuracy",
            ):
                self.assertAlmostEqual(language[key], saved["language_scorer"][key], places=5)
        if router["backend"] == saved["solver_router"]["backend"]:
            self.assertEqual(router["correct"], saved["solver_router"]["correct"])
            self.assertEqual(router["total"], saved["solver_router"]["total"])
            self.assertEqual(router["per_family"], saved["solver_router"]["per_family"])
        self.assertEqual(shipped["correct"], saved["shipped_solver_net"]["correct"])
        self.assertEqual(shipped["total"], saved["shipped_solver_net"]["total"])
        self.assertEqual(shipped["per_family"], saved["shipped_solver_net"]["per_family"])

    def test_training_on_the_held_out_text_is_rejected(self) -> None:
        train = letters_az(load_training_prose(TRAIN_PATH))
        held = letters_az(load_training_prose(HELD_EN_PATH))
        with self.assertRaises(ValueError):
            assert_split(held, held)
        with self.assertRaises(ValueError):
            assert_split(train + held, held)
        with self.assertRaises(ValueError):
            language_preference(
                load_training_prose(HELD_EN_PATH),
                load_training_prose(HELD_EN_PATH),
                load_training_prose(HELD_DE_PATH),
            )

    def test_a_certificate_plaintext_cannot_be_the_grade_corpus(self) -> None:
        banned = certificate_letter_strings()
        self.assertGreater(len(banned), 0)
        with self.assertRaises(ValueError):
            assert_certificate_plaintexts_excluded(banned[0])


if __name__ == "__main__":
    unittest.main()
