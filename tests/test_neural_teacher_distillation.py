"""Independent math and training-scope controls for optional incumbent teaching."""

import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

try:
    import numpy as np
    import engine.neural_router_v2 as router
except ImportError:
    np = None
    router = None


@unittest.skipIf(np is None, "optional NumPy dependency is absent")
class TeacherDistillationTests(unittest.TestCase):
    def model(self, width=3, hidden=4, classes=2, seed=19):
        return {"mean": [0.] * width, "scale": [1.] * width,
                "parameters": {name: value.tolist() for name, value in
                    router.residual_parameters(width, hidden, classes, seed=seed).items()}}

    def independent_loss(self, logits, targets, strength, temperature):
        softened = logits / temperature
        shifted = softened - softened.max(axis=1, keepdims=True)
        log_p = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
        normalized = targets / targets.sum(axis=1, keepdims=True)
        total = 0.
        for row in range(len(logits)):
            for column in range(logits.shape[1]):
                q = normalized[row, column]
                if q:
                    total += q * (np.log(q) - log_p[row, column])
        return strength * temperature**2 * total / len(logits)

    def test_teacher_kl_matches_independent_loss_and_finite_differences(self):
        logits = np.array([[.3, -1.4, 2.1], [1.3, -.2, -.8]])
        teacher = np.array([[.6, .3, .1], [0., .25, .75]])
        strength, temperature = .17, 2.3
        loss, gradient = router.teacher_kl_objective(
            logits, teacher, strength=strength, temperature=temperature)
        self.assertAlmostEqual(loss, self.independent_loss(logits, teacher, strength, temperature), places=13)
        epsilon = 1e-6
        for index in np.ndindex(logits.shape):
            plus, minus = logits.copy(), logits.copy()
            plus[index] += epsilon
            minus[index] -= epsilon
            expected = (self.independent_loss(plus, teacher, strength, temperature)
                        - self.independent_loss(minus, teacher, strength, temperature)) / (2 * epsilon)
            self.assertAlmostEqual(gradient[index], expected, places=8)
        np.testing.assert_allclose(gradient.sum(axis=1), 0., atol=1e-15)
        shifted_loss, shifted_gradient = router.teacher_kl_objective(
            logits + np.array([[31.], [-17.]]), teacher, strength=strength, temperature=temperature)
        self.assertAlmostEqual(loss, shifted_loss, places=13)
        np.testing.assert_allclose(gradient, shifted_gradient, atol=1e-15)

    def test_zero_strength_preserves_exact_existing_objective_and_parameters(self):
        logits = np.array([[.3, -.8], [.9, .1]])
        loss, delta = router.teacher_kl_objective(logits, np.array([[1., 0.], [0., 1.]]), strength=0.)
        self.assertEqual(loss, 0.)
        np.testing.assert_array_equal(delta, np.zeros_like(logits))
        x = np.array([[1., -2., .5], [.7, .2, -1.], [-1., .1, .8], [0., .4, -.2]])
        y = np.array([0, 1, 0, 1])
        parameters = router.residual_parameters(3, 4, 2, seed=7)
        ordinary = router.residual_gradients(parameters, x, y)
        disabled = router.residual_gradients(parameters, x, y, distillation_strength=0.)
        self.assertEqual(ordinary[0], disabled[0])
        for name in ordinary[1]:
            np.testing.assert_array_equal(ordinary[1][name], disabled[1][name])
        initial = self.model()
        with patch.object(router, '_frozen_teacher_probabilities', side_effect=AssertionError('teacher called')):
            default = router.fit_residual_network(x, y, x[::-1], y[::-1], initial_model=initial,
                hidden=4, epochs=2, seed=29, learning_rate=.0003)
            zero = router.fit_residual_network(x, y, x[::-1], y[::-1], initial_model=initial,
                hidden=4, epochs=2, seed=29, learning_rate=.0003, distillation_strength=0.)
        self.assertEqual(default, zero)

    def test_combined_network_gradient_and_wrong_teacher_do_not_remove_labels(self):
        x = np.array([[.1, -.4], [.3, .7], [-.5, .2]])
        labels = np.array([0, 1, 0])
        teacher = np.array([[.2, .8], [.75, .25], [.4, .6]])
        parameters = router.residual_parameters(2, 3, 2, seed=31)
        loss, gradients = router.residual_gradients(parameters, x, labels,
            teacher_probabilities=teacher, distillation_strength=.1, distillation_temperature=2.)
        epsilon = 1e-6
        for name in parameters:
            for index in np.ndindex(parameters[name].shape):
                plus, minus = {k: v.copy() for k, v in parameters.items()}, {k: v.copy() for k, v in parameters.items()}
                plus[name][index] += epsilon
                minus[name][index] -= epsilon
                one = router.residual_gradients(plus, x, labels, teacher_probabilities=teacher,
                    distillation_strength=.1, distillation_temperature=2.)[0]
                two = router.residual_gradients(minus, x, labels, teacher_probabilities=teacher,
                    distillation_strength=.1, distillation_temperature=2.)[0]
                self.assertAlmostEqual(gradients[name][index], (one - two) / (2 * epsilon), places=8)
        self.assertGreater(loss, 0.)
        ce, ce_gradient, _ = router.classification_objective(np.zeros((1, 2)), np.array([0]), smoothing=0.)
        kd, kd_gradient = router.teacher_kl_objective(np.zeros((1, 2)), np.array([[0., 1.]]), strength=.1, temperature=2.)
        self.assertLess((ce_gradient + kd_gradient)[0, 0], 0.)
        self.assertGreater((ce_gradient + kd_gradient)[0, 1], 0.)

    def test_teacher_distribution_and_numeric_domains_reject_invalid_inputs(self):
        logits = np.array([[.3, -.8], [.9, .1]])
        valid = np.array([[.6, .4], [.25, .75]])
        for strength in (True, -.01, 1.01, float('nan'), float('inf'), '0.1'):
            with self.subTest(strength=strength), self.assertRaises(ValueError):
                router.teacher_kl_objective(logits, valid, strength=strength)
        for temperature in (True, 0., .49, 10.1, float('nan'), float('inf'), '2'):
            with self.subTest(temperature=temperature), self.assertRaises(ValueError):
                router.teacher_kl_objective(logits, valid, temperature=temperature)
        for value in (np.ones((2, 3)), [[.7, .2], [.25, .75]], [[-.1, 1.1], [.25, .75]],
                      [[float('nan'), 0.], [.25, .75]], [[0., 0.], [.25, .75]], [[True, False], [False, True]]):
            with self.subTest(target=value), self.assertRaises(ValueError):
                router.teacher_kl_objective(logits, value)
        for value in ([], [[1.]], [[float('inf'), 0.]], [['.3', '.7']], [[True, False]]):
            with self.subTest(logits=value), self.assertRaises(ValueError):
                router.teacher_kl_objective(value, [[.5, .5]])
        with self.assertRaises(ValueError):
            router.teacher_kl_objective([[1e308, -1e308]], [[.5, .5]], strength=.1)

    def test_two_view_training_batch_fits_the_explicit_row_bound(self):
        logits = np.zeros((10_240, 2))
        loss, gradient = router.teacher_kl_objective(logits, np.full_like(logits, .5), strength=.1)
        self.assertEqual(loss, 0.)
        np.testing.assert_array_equal(gradient, logits)
        with self.assertRaises(ValueError):
            router.teacher_kl_objective(np.zeros((20_001, 2)), np.full((20_001, 2), .5))

    def test_teacher_is_frozen_and_uses_training_rows_only_for_both_views(self):
        train_x = np.array([[1., -.4, .2, 7.], [-.7, .3, .6, 4.], [.8, .1, -.5, -3.], [0., .5, .4, -2.]])
        train_y = np.array([0, 1, 0, 1])
        validation_x = np.array([[999., 999., 999., 999.], [-999., -999., -999., -999.]])
        validation_y = np.array([0, 1])
        teacher_models = [self.model(seed=11), self.model(seed=17)]
        frozen = copy.deepcopy(teacher_models)
        expected_logits = np.mean([router.network_logits(train_x[:, :3], model) for model in teacher_models], axis=0)
        softened = expected_logits / 2.
        exp = np.exp(softened - softened.max(axis=1, keepdims=True))
        expected = exp / exp.sum(axis=1, keepdims=True)
        with patch.object(router, '_frozen_teacher_probabilities', wraps=router._frozen_teacher_probabilities) as targets, \
             patch.object(router, 'residual_gradients', wraps=router.residual_gradients) as gradients:
            fitted = router.fit_residual_network(train_x, train_y, validation_x, validation_y,
                initial_model=teacher_models[0], teacher_models=teacher_models, hidden=4, epochs=2,
                seed=23, learning_rate=.0003, distillation_strength=.1, distillation_temperature=2.)
        self.assertEqual(targets.call_count, 1)
        np.testing.assert_array_equal(targets.call_args.args[0], train_x)
        self.assertEqual(teacher_models, frozen)
        for call in gradients.call_args_list:
            np.testing.assert_allclose(call.kwargs['teacher_probabilities'], np.concatenate((expected, expected)), atol=1e-15)
        self.assertIn('frozen_incumbent_teacher_kl', fitted['training_types'])
        self.assertEqual(fitted['teacher_scope'], 'generated training rows only')

    def test_positive_distillation_requires_compatible_warm_start_before_training(self):
        with patch.object(router, 'load_training_prose', side_effect=AssertionError('corpus read')), \
             patch.object(router, '_samples', side_effect=AssertionError('samples generated')):
            with self.assertRaises(ValueError):
                router.train_router(distillation_strength=.1, warm_start=False, write=False)
            for value in (True, -.1, 1.1, float('nan')):
                with self.assertRaises(ValueError):
                    router.train_router(distillation_strength=value, write=False)
        x, y = np.array([[0., 1., .3], [.2, -.4, .7]]), np.array([0, 1])
        with patch.object(router, 'residual_gradients', side_effect=AssertionError('gradient called')):
            with self.assertRaises(ValueError):
                router.fit_residual_network(x, y, x, y, hidden=4, epochs=1, distillation_strength=.1)
            for bad in (self.model(width=2), self.model(width=4), self.model(hidden=3), self.model(classes=3)):
                with self.assertRaises(ValueError):
                    router.fit_residual_network(x, y, x, y, hidden=4, epochs=1,
                        initial_model=self.model(), teacher_models=[bad], distillation_strength=.1)

    def test_teacher_artifact_drift_during_loading_is_rejected_before_sampling(self):
        previous = router.load_router()
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'incumbent.json'
            destination.write_bytes(router.WEIGHTS_PATH.read_bytes())

            def changed_while_loading(path):
                path.write_bytes(b'external edit after frozen model was read')
                return previous

            with patch.object(router, 'load_router', side_effect=changed_while_loading), \
                 patch.object(router, '_samples', side_effect=AssertionError('sampling started')) as samples, \
                 patch.object(router, 'fit_residual_network', side_effect=AssertionError('fit started')) as fit:
                with self.assertRaisesRegex(ValueError, 'incumbent changed'):
                    router.train_router(weights_path=destination, warm_start=True, hidden=96,
                        ensemble_size=3, train_per_class=8, epochs=1, write=False, distillation_strength=.1)
            samples.assert_not_called()
            fit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
