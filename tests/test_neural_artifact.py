"""Router artifact integration controls with a mocked fitter, never training."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import numpy as np

import engine.neural_router_v2 as router


class RouterArtifactTest(unittest.TestCase):
    def _run_candidate(self, directory, *, destination=None, large=False, previous=None,
                       fit_probe=None):
        """Exercise selection and writing with independent synthetic predictions."""
        destination = destination or directory / "router.json"
        families = list(router.FAMILIES) + list(router.EXTRA_FAMILIES[:3])
        all_families = list(router.FAMILIES) + list(router.EXTRA_FAMILIES)
        full, held = "A" * 600 + "B" * 200 + "C" * 200, "D" * 1000
        events, fits = [], []
        hidden = 256 if large else 2
        width = router.FEATURE_WIDTHS[router.FEATURE_VERSION]
        value = .12345678901234567
        model = {
            "mean": [0.] * width, "scale": [1.] * width,
            "parameters": {
                "w0": [[value] * hidden for _ in range(width)], "b0": [0.] * hidden,
                "w1": [[value] * hidden for _ in range(hidden)], "b1": [0.] * hidden,
                "w2": [[value] * len(families) for _ in range(hidden)],
                "b2": [0.] * len(families),
            },
            "training_types": ["supervised_label_smoothing", "curriculum_hard_examples",
                               "paired_dropout_consistency"],
            "family_names": families,
        }
        baseline = {
            "mean": [0.], "scale": [1.], "w1": [[0.]], "b1": [0.],
            "w2": [[0.] * len(router.FAMILIES)], "b2": [0.] * len(router.FAMILIES),
            "families": list(router.FAMILIES),
        }
        (directory / "neural_router_weights.json").write_text(json.dumps(baseline))

        def samples(corpus, names, count, seed, english, tables, **options):
            events.append(("samples", corpus[0], seed))
            labels = np.repeat(np.arange(len(names)), count)
            # Distinct split markers make a misplaced row detectable at fitting.
            marker = {"A": 0, "B": 100, "C": 200, "D": 300}[corpus[0]]
            features = [[marker + all_families.index(names[int(label)])] for label in labels]
            return np.asarray(features, dtype=float), labels

        def fit(train_x, train_y, validation_x, validation_y, **options):
            if fit_probe is not None:
                fit_probe()
            events.append(("fit", options["seed"]))
            fits.append(tuple(np.asarray(a).copy() for a in
                              (train_x, train_y, validation_x, validation_y)))
            return copy.deepcopy(model)

        def logits(features, fitted):
            names = fitted["family_names"]
            predictions = np.full((len(features), len(names)), -10.)
            for row, feature in enumerate(features):
                family = all_families[int(feature[0]) % 100]
                if family in names:
                    predictions[row, names.index(family)] = 10.
            return predictions

        def legacy_samples(corpus, english, count, seed, names, tables):
            return np.zeros((len(names) * count, 1)), np.repeat(np.arange(len(names)), count)

        with ExitStack() as patches:
            replacements = {
                "DATA": directory,
                "load_training_prose": lambda path: full if path == router.TRAIN_PATH else held,
                "assert_split": lambda left, right: None,
                "assert_certificate_plaintexts_excluded": lambda *corpora: None,
                "discover_solver_labels": lambda: all_families,
                "_english_unigram": lambda corpus: np.full(26, 1 / 26),
                "feature_tables": lambda corpus, english: {"source": corpus[0]},
                "_samples": samples,
                "fit_residual_network": fit,
                "network_logits": logits,
                "_router_samples": legacy_samples,
                "encrypt_family": lambda family, plaintext, draw: family,
                "_features": lambda ciphertext, *args, **kwargs: [all_families.index(ciphertext)],
            }
            for name, value in replacements.items():
                patches.enter_context(mock.patch.object(router, name, value))
            if previous is not None:
                patches.enter_context(mock.patch.object(router, "load_router", return_value=previous))
            result = router.train_router(epochs=1, train_per_class=8, weights_path=destination,
                                         hidden=hidden, ensemble_size=5 if large else 1)
        return result, events, fits

    def test_custom_destination_keeps_model_and_metrics_distinct_and_hashes_written_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            destination = directory / "candidate.json"
            metrics, _, _ = self._run_candidate(directory, destination=destination)
            self.assertTrue(metrics["promoted"])
            payload = router.load_router(destination)
            self.assertIn("models", payload)
            saved_metrics = json.loads((directory / "candidate.metrics.json").read_text())
            self.assertEqual(saved_metrics, metrics)
            raw = destination.read_bytes()
            self.assertLessEqual(len(raw), 4 * 1024 * 1024)
            self.assertTrue(raw.endswith(b"\n"))
            self.assertEqual(metrics["artifact_bytes"], len(raw))
            self.assertEqual(metrics["model_sha256"], hashlib.sha256(raw).hexdigest())

    def test_oversized_loadable_shape_cannot_replace_incumbent_or_metrics(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            destination = directory / "candidate_weights.json"
            first, _, _ = self._run_candidate(directory, destination=destination)
            self.assertTrue(first["promoted"])
            before = destination.read_bytes()
            metrics_path = directory / "candidate_metrics.json"
            previous_metrics = metrics_path.read_bytes()
            incumbent = router.load_router(destination)
            before_paths = set(directory.iterdir())
            with mock.patch.object(router, "_atomic_json", wraps=router._atomic_json) as writer:
                rejected, _, _ = self._run_candidate(directory, destination=destination,
                                                      large=True, previous=incumbent)
            self.assertEqual(rejected["correct"], rejected["total"])
            self.assertGreater(rejected["artifact_bytes"], 4 * 1024 * 1024)
            self.assertFalse(rejected["promoted"])
            self.assertEqual(rejected["model_policy"]["status"], "rejected")
            self.assertIn("size bound", rejected["model_policy"]["action"])
            writer.assert_not_called()
            self.assertEqual(destination.read_bytes(), before)
            self.assertEqual(metrics_path.read_bytes(), previous_metrics)
            self.assertEqual(set(directory.iterdir()), before_paths)
            self.assertEqual(router.load_router(destination), incumbent)

    def test_only_training_and_validation_splits_reach_fitter(self):
        with tempfile.TemporaryDirectory() as temporary:
            metrics, events, fits = self._run_candidate(Path(temporary))
        self.assertTrue(metrics["promoted"])
        self.assertEqual(len(fits), 1)
        train_x, train_y, validation_x, validation_y = fits[0]
        self.assertTrue(np.all((train_x >= 0) & (train_x < 100)))
        self.assertTrue(np.all((validation_x >= 100) & (validation_x < 200)))
        self.assertEqual(len(train_y), len(train_x))
        self.assertEqual(len(validation_y), len(validation_x))
        self.assertEqual([event[0] for event in events[:3]], ["samples", "samples", "fit"])
        self.assertEqual([event[1] for event in events if event[0] == "samples"],
                         ["A", "B", "C", "D"])
        for split, corpus in (("train", "A" * 600), ("validation", "B" * 200),
                              ("calibration", "C" * 200), ("heldout", "D" * 1000)):
            self.assertEqual(metrics[split + "_sha256"], hashlib.sha256(corpus.encode()).hexdigest())

    def test_expanded_or_reordered_incumbent_is_rejected_before_fitting(self):
        families = list(router.FAMILIES) + list(router.EXTRA_FAMILIES[:3])
        cases = {
            "expanded": list(router.FAMILIES) + list(router.EXTRA_FAMILIES),
            "reordered": families[1:2] + families[:1] + families[2:],
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            destination = directory / "candidate_weights.json"
            destination.write_text("{}")
            before = destination.read_bytes()
            for name, incompatible in cases.items():
                fit_probe = mock.Mock()
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "prefix"):
                    self._run_candidate(directory, destination=destination,
                                        previous={"families": incompatible}, fit_probe=fit_probe)
                fit_probe.assert_not_called()
                self.assertEqual(destination.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
