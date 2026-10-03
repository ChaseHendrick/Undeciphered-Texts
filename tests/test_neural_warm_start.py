"""Pure normalization conversion controls; no optimizer training in this set."""
from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import numpy as np
import engine.neural_router_v2 as router
from engine.neural_router_v2 import warm_start_model


class NeuralWarmStartTest(unittest.TestCase):
    def _model(self):
        return {"mean": [2., -4., .7], "scale": [.5, 7., 2.],
                "parameters": {"w0": [[.3, -.8], [1.2, .4], [-.7, .6]],
                               "b0": [.1, -.2], "w1": [[.5, .2], [-.4, .8]],
                               "b1": [.3, -.1], "w2": [[.7, -.2, .4], [-.3, .9, .5]],
                               "b2": [.2, -.4, .6]}}

    def test_recenter_rescale_and_zero_padding_preserve_independent_logits(self):
        source = self._model()
        before = copy.deepcopy(source)
        converted = warm_start_model(source, [7., 2., -3., 11., 9.], [3., .25, 6., 8., .7])
        raw = np.random.default_rng(7204).normal(size=(80, 5)) * 9
        old = source["parameters"]
        z = (raw[:, :3] - np.array(source["mean"])) / np.array(source["scale"])
        h0 = np.tanh(z @ np.array(old["w0"]) + np.array(old["b0"]))
        expected = (np.tanh(h0 @ np.array(old["w1"]) + np.array(old["b1"])) + h0) @ np.array(old["w2"]) + np.array(old["b2"])
        np.testing.assert_allclose(router.network_logits(raw, converted), expected, rtol=1e-12, atol=1e-12)
        np.testing.assert_array_equal(converted["parameters"]["w0"][3:], np.zeros((2, 2)))
        for name in ("w1", "b1", "w2", "b2"):
            self.assertEqual(converted["parameters"][name], source["parameters"][name])
        self.assertEqual(source, before)

    def test_conversion_without_new_columns_preserves_logits_and_tie_order(self):
        source = self._model()
        converted = warm_start_model(source, [-1., 12., 3.], [4., .1, 9.])
        raw = np.array([[2., 3., 4.], [-10., 12., -2.]])
        np.testing.assert_allclose(router.network_logits(raw, source), router.network_logits(raw, converted),
                                   rtol=1e-12, atol=1e-12)

    def test_invalid_dimensions_scale_parameters_and_unrepresentable_conversion(self):
        source = self._model()
        for mean, scale in (([0., 0.], [1., 1.]), ([0.] * 4, [1.] * 3),
                            ([0.] * 4, [1., 0., 1., 1.]), ([float("nan")] * 4, [1.] * 4),
                            ([0.] * 4, [float("inf")] * 4), ([[0.]] * 4, [1.] * 4)):
            with self.subTest(mean=mean, scale=scale), self.assertRaises(ValueError):
                warm_start_model(source, mean, scale)
        for change in (lambda m: m.update(scale=[0., 1., 1.]),
                       lambda m: m.update(parameters=[]),
                       lambda m: m["parameters"].update(w0=[[1.]]),
                       lambda m: m["parameters"]["b0"].__setitem__(0, float("inf")),
                       lambda m: m.update(scale=[1e-308] * 3)):
            bad = copy.deepcopy(source)
            change(bad)
            with self.assertRaises(ValueError):
                warm_start_model(bad, [0.] * 4, [1e308] * 4)

    def test_warm_start_rejects_incompatible_artifact_before_sampling_or_fitting(self):
        previous = router.load_router()
        mutations = {
            "discarded_features": lambda p: p.update(feature_version="cipher_statistics_v7"),
            "changed_classes": lambda p: p.update(families=p["families"][:-1]),
            "changed_language_tables": lambda p: p.update(training_letters=p["training_letters"][:-1]),
            "different_ensemble": lambda p: p.update(models=p["models"][:-1]),
            "different_hidden": lambda p: p["models"][0]["parameters"].update(b0=[0.] * 8),
        }
        for name, mutate in mutations.items():
            bad = copy.deepcopy(previous)
            mutate(bad)
            with self.subTest(name=name), mock.patch.object(router, "load_router", return_value=bad), \
                 mock.patch.object(router, "_samples", side_effect=AssertionError("no samples for incompatible warm start")) as samples, \
                 mock.patch.object(router, "fit_residual_network", side_effect=AssertionError("no fit")) as fit:
                with self.assertRaises(ValueError):
                    router.train_router(warm_start=True, hidden=96, ensemble_size=3,
                                        epochs=1, train_per_class=8, write=False)
                samples.assert_not_called()
                fit.assert_not_called()

    def test_warm_start_requires_incumbent_and_explicit_boolean(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "missing.json"
            with mock.patch.object(router, "_samples", side_effect=AssertionError("no sampling")):
                with self.assertRaises(ValueError):
                    router.train_router(warm_start=True, weights_path=path, write=False)
        for value in (1, "yes", None):
            with self.assertRaises((TypeError, ValueError)):
                router.train_router(warm_start=value, write=False)

    def test_checkpoint_zero_wins_exact_tie_without_training_gradients(self):
        source = {"mean": [0.], "scale": [1.], "parameters": {
            "w0": [[0., 0.]], "b0": [0., 0.], "w1": [[0., 0.], [0., 0.]],
            "b1": [0., 0.], "w2": [[0., 0.], [0., 0.]], "b2": [0., 0.]}}
        features, labels = np.array([[-1.], [1.]]), np.array([0, 1])
        gradients = {name: np.zeros_like(value, dtype=float) for name, value in source["parameters"].items()}
        with mock.patch.object(router, "residual_gradients", return_value=(0., gradients)):
            result = router.fit_residual_network(features, labels, features, labels,
                initial_model=source, hidden=2, epochs=5)
        self.assertEqual(result["checkpoint_epoch"], 0)
        self.assertTrue(result["warm_start"])
        self.assertEqual(result["optimizer_state"], "fresh")
        self.assertEqual(result["validation_correct"], 1)
        np.testing.assert_array_equal(router.network_logits(features, result), np.zeros((2, 2)))

    def test_checkpoint_zero_survives_worse_trial_and_incompatible_shape_never_updates(self):
        source = {"mean": [0.], "scale": [1.], "parameters": {
            "w0": [[1., 0.]], "b0": [0., 0.], "w1": [[0., 0.], [0., 0.]],
            "b1": [0., 0.], "w2": [[-1., 1.], [0., 0.]], "b2": [0., 0.]}}
        features, labels = np.array([[-1.], [1.]]), np.array([0, 1])
        gradients = {name: np.zeros_like(value, dtype=float) for name, value in source["parameters"].items()}
        gradients["b2"][:] = [-100., 100.]
        with mock.patch.object(router, "residual_gradients", return_value=(0., gradients)):
            result = router.fit_residual_network(features, labels, features, labels,
                initial_model=source, hidden=2, epochs=100)
        self.assertEqual(result["checkpoint_epoch"], 0)
        self.assertEqual(result["validation_correct"], 2)
        np.testing.assert_allclose(router.network_logits(features, result), router.network_logits(features, source),
                                   rtol=1e-12, atol=1e-12)
        with mock.patch.object(router, "residual_gradients", side_effect=AssertionError("no update")) as update:
            for hidden in (3,):
                with self.assertRaises(ValueError):
                    router.fit_residual_network(features, labels, features, labels,
                        initial_model=source, hidden=hidden, epochs=1)
            bad = copy.deepcopy(source)
            bad["parameters"]["w2"] = [[0.] * 3] * 2
            bad["parameters"]["b2"] = [0.] * 3
            with self.assertRaises(ValueError):
                router.fit_residual_network(features, labels, features, labels,
                    initial_model=bad, hidden=2, epochs=1)
            update.assert_not_called()

    def test_learning_rate_is_validated_before_any_gradient_or_sampling(self):
        features, labels = np.array([[-1.], [1.]]), np.array([0, 1])
        for rate in (0, -.01, .10001, float("nan"), float("inf"), True, "0.01", 10**1000):
            with self.subTest(rate=rate), mock.patch.object(router, "residual_gradients",
                    side_effect=AssertionError("no gradient")) as update, \
                 mock.patch.object(router, "_samples", side_effect=AssertionError("no sampling")) as samples:
                with self.assertRaises(ValueError):
                    router.fit_residual_network(features, labels, features, labels,
                        hidden=2, epochs=1, learning_rate=rate)
                with self.assertRaises(ValueError):
                    router.train_router(write=False, learning_rate=rate)
                update.assert_not_called()
                samples.assert_not_called()

    def test_learning_rate_controls_actual_adamw_step_with_mocked_gradients(self):
        features, labels = np.array([[-1.], [1.]]), np.array([0, 1])
        source = router.residual_parameters(1, 2, 2, seed=719)
        gradients = {name: np.zeros_like(value) for name, value in source.items()}
        gradients["b2"][:] = [1., -1.]
        for rate in (.01, .0003):
            with self.subTest(rate=rate), mock.patch.object(router, "residual_parameters",
                    return_value={name: value.copy() for name, value in source.items()}), \
                 mock.patch.object(router, "residual_gradients", return_value=(0., gradients)):
                result = router.fit_residual_network(features, labels, features, labels,
                    hidden=2, epochs=1, learning_rate=rate)
            np.testing.assert_allclose(result["parameters"]["b2"], [-rate / (1 + 1e-8), rate / (1 + 1e-8)],
                                       rtol=1e-12, atol=1e-12)
            np.testing.assert_allclose(result["parameters"]["w0"], source["w0"] * (1 - rate * .01),
                                       rtol=1e-12, atol=1e-12)
            self.assertEqual(result["learning_rate"], rate)


if __name__ == "__main__":
    unittest.main()
