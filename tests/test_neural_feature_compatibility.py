"""Frozen pre-upgrade features and the compact V5 plus M209 V8 contract."""
from __future__ import annotations

from hashlib import sha256
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from engine.neural_grade import _english_unigram
from engine.neural_features import feature_tables
from engine.neural_m209_features import m209_pair_features
from engine.neural_router_v2 import _features, load_router
from tests.test_persona_detective_solver import CIPHER, PLAIN


class NeuralFeatureCompatibilityTest(unittest.TestCase):
    def setUp(self):
        self.english = _english_unigram(PLAIN * 12)
        self.tables = feature_tables(PLAIN * 12, self.english)

    def test_prior_feature_vectors_match_frozen_pre_upgrade_values(self):
        frozen = {
            2: (58, "fc6278de7353a0a6a7bde8ac4cf7a96d054eb3711165cb02e98ad923aeb7ba43"),
            3: (82, "ab79c09ef40469c64fafb2d7aa3602be065b92c006ed0624bde71a3179cd39eb"),
            4: (126, "7ed1f8f0d7508c076879dfdd796432a06d1dbec33142f45231c6f5ce3e939ab4"),
            5: (142, "293c89b9b9c1d5c689fe2142baa93a3f4dc6a07c23222fefab3363dcc0ef4f4e"),
            6: (222, "c528a93daaefadef4e12c08f9817513abcfc19e3f0b873c4202eefde20069fb5"),
            7: (228, "308c81da0ffc8092cc9bcfe99993c73bcb155e320dfdfb58f1d764c84592d4d5"),
        }
        for version, (width, expected_hash) in frozen.items():
            with self.subTest(version=version):
                row = _features(CIPHER, self.english, self.tables, version=f"cipher_statistics_v{version}")
                raw = json.dumps([round(float(v), 10) for v in row], separators=(",", ":")).encode()
                self.assertEqual(len(row), width)
                self.assertEqual(sha256(raw).hexdigest(), expected_hash)

    def test_v8_is_exact_v5_prefix_plus_six_conditional_m209_values(self):
        before = _features(CIPHER, self.english, self.tables, version="cipher_statistics_v5")
        current = _features(CIPHER, self.english, self.tables, version="cipher_statistics_v8")
        self.assertEqual(len(current), 148)
        np.testing.assert_array_equal(current[:142], before)
        np.testing.assert_array_equal(current[142:], m209_pair_features(CIPHER, self.tables))
        self.assertTrue(np.all(np.isfinite(current)))

    def test_all_serialized_formats_remain_loadable_with_their_exact_widths(self):
        training = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 14
        widths = {2: 58, 3: 82, 4: 126, 5: 142, 6: 222, 7: 228, 8: 148}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "compatibility.json"
            for version, width in widths.items():
                model = {"mean": [0.] * width, "scale": [1.] * width,
                    "parameters": {"w0": [[0., 0.]] * width, "b0": [0., 0.],
                        "w1": [[0., 0.]] * 2, "b1": [0., 0.],
                        "w2": [[0., 0.]] * 2, "b2": [0., 0.]}}
                payload = {"format_version": version, "feature_version": f"cipher_statistics_v{version}",
                    "families": ["caesar", "vigenere"], "models": [model],
                    "mean": model["mean"], "scale": model["scale"], "temperature": 1.,
                    "heldout_accuracy": .5, "training_letters": training,
                    "train_sha256": sha256(training.encode()).hexdigest()}
                path.write_text(json.dumps(payload))
                with self.subTest(version=version):
                    self.assertEqual(load_router(path), payload)


if __name__ == "__main__":
    unittest.main()
