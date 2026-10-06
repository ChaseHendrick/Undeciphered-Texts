"""Residual router gradients, calibration, provenance, and routing limits."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from engine.neural_router_v2 import (
    fit_residual_network, network_logits, residual_gradients, residual_parameters,
    calibrated_probabilities, load_router, route_probabilities, promotion_allowed,
)


class ResidualNetworkTest(unittest.TestCase):
    def test_gradients_match_central_finite_differences(self):
        x = np.array([[.2, -.4], [1., .1], [-.3, .2]])
        labels = np.array([0, 1, 0])
        parameters = residual_parameters(2, 3, 2, seed=9)
        loss, gradients = residual_gradients(parameters, x, labels, smoothing=0.)
        self.assertTrue(np.isfinite(loss))
        for name, parameter in parameters.items():
            for index in np.ndindex(parameter.shape):
                with self.subTest(name=name, index=index):
                    before = parameter[index]
                    parameter[index] = before + 1e-6
                    upper = residual_gradients(parameters, x, labels, smoothing=0.)[0]
                    parameter[index] = before - 1e-6
                    lower = residual_gradients(parameters, x, labels, smoothing=0.)[0]
                    parameter[index] = before
                    self.assertAlmostEqual(gradients[name][index], (upper - lower) / 2e-6, places=5)

    def test_adamw_fit_learns_separable_data_and_is_reproducible(self):
        x = np.array([[-2., -1.], [-1., -2.], [-2., -2.], [1., 2.], [2., 1.], [2., 2.]])
        labels = np.array([0, 0, 0, 1, 1, 1])
        one = fit_residual_network(x, labels, x, labels, hidden=8, epochs=50, seed=42)
        two = fit_residual_network(x, labels, x, labels, hidden=8, epochs=50, seed=42)
        self.assertEqual(one, two)
        predicted = np.argmax(network_logits(x, one), axis=1)
        np.testing.assert_array_equal(predicted, labels)
        self.assertEqual(one["optimizer"], "adamw")

    def test_softmax_is_stable_and_temperature_preserves_ranking(self):
        logits = np.array([[10000., 10001., 9999.]])
        cold = calibrated_probabilities(logits, 1.)
        warm = calibrated_probabilities(logits, 2.)
        self.assertTrue(np.all(np.isfinite(cold)))
        self.assertAlmostEqual(float(cold.sum()), 1.)
        self.assertEqual(int(cold.argmax()), int(warm.argmax()))
        self.assertLess(float(warm.max()), float(cold.max()))
        for temperature in (0, -1, 1e-320, float("nan"), float("inf"), 10**1000):
            with self.assertRaises(ValueError):
                calibrated_probabilities(logits, temperature)

    def test_extreme_finite_logits_produce_finite_normalized_probabilities(self):
        logits = np.array([[1e308, -1e308], [1e308, 1e308], [-1e308, -1e308]])
        with np.errstate(all="raise"):
            probabilities = calibrated_probabilities(logits, .05)
        np.testing.assert_array_equal(probabilities, [[1., 0.], [.5, .5], [.5, .5]])
        self.assertTrue(np.all(np.isfinite(probabilities)))
        np.testing.assert_array_equal(probabilities.sum(axis=1), np.ones(3))

    def test_promotion_requires_same_benchmark_non_regression(self):
        self.assertTrue(promotion_allowed(.8, .7, .6, None))
        self.assertTrue(promotion_allowed(.8, .7, .6, .6))
        self.assertFalse(promotion_allowed(.6, .7, .6, None))
        self.assertFalse(promotion_allowed(.8, .7, .5, .6))
        self.assertFalse(promotion_allowed(189 / 204, 158 / 204, 428 / 480, 428 / 480, 193 / 204))


class ShippedResidualRouterTest(unittest.TestCase):
    def test_shipped_artifact_is_valid_and_probabilities_are_complete(self):
        payload = load_router()
        versions = {3: ("cipher_statistics_v3", 82),
                    4: ("cipher_statistics_v4", 126),
                    5: ("cipher_statistics_v5", 142),
                    6: ("cipher_statistics_v6", 222),
                    7: ("cipher_statistics_v7", 228),
                    8: ("cipher_statistics_v8", 148),
                    9: ("cipher_statistics_v9", 154),
                    10: ("cipher_statistics_v10", 145)}
        self.assertIn(payload["format_version"], versions)
        self.assertGreaterEqual(len(payload["families"]), 17)
        self.assertEqual((payload["feature_version"], len(payload["mean"])),
                         versions[payload["format_version"]])
        base_types = ["supervised_label_smoothing", "curriculum_hard_examples", "paired_dropout_consistency"]
        teacher = ["frozen_incumbent_teacher_kl"] if "distillation" in payload else []
        for model in payload["models"]:
            self.assertEqual(model["training_types"], base_types + teacher)
        source = json.loads((Path(__file__).resolve().parents[1] / "engine/data/caesar_certificate.json").read_text())
        report = route_probabilities(source["ciphertext"])
        self.assertEqual(len(report["candidates"]), len(payload["families"]))
        self.assertAlmostEqual(sum(c["probability"] for c in report["candidates"]), 1.)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["kind"], "family_ranking")
        for c in report["candidates"]:
            self.assertFalse(c["family"] in {"k4", "voynich", "nr86"})

    def test_input_and_corrupt_artifact_rejections(self):
        for text in ("ABC", "12345678901234567890", "α" * 100, "A" * 8193):
            with self.assertRaises(ValueError):
                route_probabilities(text)
        payload = load_router()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "weights.json"
            for mutate in (lambda d: d.update(format_version=99),
                           lambda d: d.update(families=["k4"]),
                           lambda d: d.update(scale=[0.]),
                           lambda d: d.update(temperature=float("nan")),
                           lambda d: d["models"][0]["parameters"].update(b0=[float("nan")])):
                bad = copy.deepcopy(payload)
                mutate(bad)
                path.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):
                    load_router(path)

    def test_artifact_class_order_and_model_containers_are_validated(self):
        payload = load_router()
        mutations = {
            "unordered_family_object": lambda d: d.update(families={f: None for f in d["families"]}),
            "ensemble_object": lambda d: d.update(models={"first": d["models"][0]}),
            "null_model": lambda d: d["models"].__setitem__(0, None),
            "null_parameters": lambda d: d["models"][0].update(parameters=None),
            "array_parameters": lambda d: d["models"][0].update(parameters=[]),
            "unrepresentable_temperature": lambda d: d.update(temperature=10**1000),
            "unrepresentable_accuracy": lambda d: d.update(heldout_accuracy=10**1000),
            "unrepresentable_parameter": lambda d: d["models"][0]["parameters"]["b0"].__setitem__(0, 10**1000),
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "weights.json"
            for name, mutate in mutations.items():
                bad = copy.deepcopy(payload)
                mutate(bad)
                path.write_text(json.dumps(bad))
                with self.subTest(name=name), self.assertRaises(ValueError):
                    load_router(path)


if __name__ == "__main__":
    unittest.main()
