"""Exact multiobjective derivatives, curriculum bounds, and reward controls."""
import unittest
import numpy as np

from engine.neural_training import classification_objective, curriculum_weights, correctness_speed_reward


class ClassificationObjectiveTest(unittest.TestCase):
    def test_supervised_and_paired_view_gradients_match_finite_differences(self):
        logits = np.array([[.2, -.4, .7], [.3, .1, -.2], [.1, .4, -.1], [-.3, .2, .1]])
        labels = np.array([2, 0, 2, 0])
        options = {"smoothing": .07, "paired_rows": ((0, 2), (1, 3)), "consistency_weight": .4,
                   "sample_weights": np.array([1., 2., .5, 1.5])}
        loss, gradient, metrics = classification_objective(logits, labels, **options)
        self.assertTrue(np.isfinite(loss))
        self.assertGreater(metrics["consistency_loss"], 0)
        for index in np.ndindex(logits.shape):
            upper = logits.copy(); upper[index] += 1e-6
            lower = logits.copy(); lower[index] -= 1e-6
            estimate = (classification_objective(upper, labels, **options)[0] - classification_objective(lower, labels, **options)[0]) / 2e-6
            self.assertAlmostEqual(gradient[index], estimate, places=6)
        np.testing.assert_allclose(gradient.sum(axis=1), 0., atol=1e-14)

    def test_shared_pair_rows_and_zero_weight_examples_have_correct_gradients(self):
        logits = np.array([[.4, -.2], [.1, .5], [-.1, .3]])
        labels = np.array([0, 0, 0])
        options = {"paired_rows": ((0, 1), (0, 2)), "consistency_weight": .8, "sample_weights": [0., 1., 2.]}
        _, gradient, _ = classification_objective(logits, labels, **options)
        for index in np.ndindex(logits.shape):
            upper=logits.copy(); upper[index]+=1e-6
            lower=logits.copy(); lower[index]-=1e-6
            estimate=(classification_objective(upper,labels,**options)[0]-classification_objective(lower,labels,**options)[0])/2e-6
            self.assertAlmostEqual(gradient[index],estimate,places=6)

    def test_identical_views_have_zero_consistency_and_row_offsets_are_invariant(self):
        logits = np.array([[10000., 10001., 9999.], [10000., 10001., 9999.]])
        labels = [1, 1]
        loss, gradient, metrics = classification_objective(logits, labels, paired_rows=((0, 1),), consistency_weight=1.)
        self.assertEqual(metrics["consistency_loss"], 0.)
        shifted = logits + np.array([[1234.], [-2345.]])
        other_loss, other_gradient, _ = classification_objective(shifted, labels, paired_rows=((0, 1),), consistency_weight=1.)
        self.assertAlmostEqual(loss, other_loss)
        np.testing.assert_allclose(gradient, other_gradient, atol=1e-14)
        self.assertEqual(metrics["accuracy"], 1.)

    def test_supervised_loss_weights_and_smoothing_are_explicit(self):
        logits = np.array([[0., 0.], [0., 0.]])
        loss, gradient, metrics = classification_objective(logits, [0, 1], smoothing=0., sample_weights=[1., 3.])
        self.assertAlmostEqual(loss, np.log(2))
        np.testing.assert_allclose(gradient, [[-.125, .125], [.375, -.375]])
        self.assertEqual(metrics["paired_rows"], 0)
        self.assertEqual(metrics["consistency_loss"], 0.)

    def test_two_view_expanded_training_batch_fits_row_and_pair_bounds(self):
        base_labels = np.repeat(np.arange(23), 256)
        labels = np.concatenate((base_labels, base_labels))
        logits = np.zeros((len(labels), 23))
        pairs = tuple((row, row + len(base_labels)) for row in range(len(base_labels)))
        loss, gradient, metrics = classification_objective(logits, labels, paired_rows=pairs)
        self.assertTrue(np.isfinite(loss))
        self.assertEqual(gradient.shape, (11776, 23))
        self.assertEqual(metrics["paired_rows"], 5888)
        with self.assertRaises(ValueError):
            classification_objective(np.zeros((20001, 2)), np.zeros(20001, dtype=int))

    def test_invalid_matrices_labels_pairs_weights_and_coefficients(self):
        for logits in ([], [[0.]], [[float("nan"), 1.]], [[float("inf"), 1.]], [1., 2.]):
            with self.assertRaises((ValueError, TypeError)):
                classification_objective(logits, [0])
        for labels in ([0.5, 1.], [True, False], [-1, 0], [0, 2], [[0, 1]], [0]):
            with self.assertRaises((ValueError, TypeError)):
                classification_objective([[0., 1.], [1., 0.]], labels)
        for options in ({"smoothing": 1.}, {"smoothing": -1.}, {"smoothing": True},
                        {"consistency_weight": float("nan")}, {"consistency_weight": -1.},
                        {"paired_rows": ((0, 2),)}, {"paired_rows": ((0, 0),)},
                        {"paired_rows": ((True, 1),)}, {"sample_weights": [0., 0.]},
                        {"sample_weights": [-1., 1.]}, {"sample_weights": [float("inf"), 1.]},
                        {"sample_weights": [1.]}, {"consistency_weight": 1001.}):
            with self.subTest(options=options), self.assertRaises((ValueError, TypeError)):
                classification_objective([[0., 1.], [1., 0.]], [0, 0], **options)


class CurriculumAndRewardTest(unittest.TestCase):
    def test_later_curriculum_emphasizes_errors_without_heldout_inputs(self):
        labels = [0, 1, 0, 1]
        predictions = [0, 0, 0, 0]
        early = curriculum_weights(labels, predictions, 0, 100, easy_mask=[True, False, False, False])
        late = curriculum_weights(labels, predictions, 100, 100, easy_mask=[True, False, False, False])
        np.testing.assert_array_equal(early, np.ones(4))
        self.assertAlmostEqual(float(late.mean()), 1.)
        self.assertGreater(late[1], late[2])
        self.assertLess(late[0], late[2])
        self.assertTrue(np.all((late >= .25) & (late <= 4.)))
        scores = np.array([[2., 1.], [2., 1.], [2., 1.], [2., 1.]])
        np.testing.assert_allclose(late, curriculum_weights(labels, scores, 100, 100, easy_mask=[True, False, False, False]))

    def test_all_correct_and_all_wrong_curricula_keep_unit_mean(self):
        for predictions in ([0, 1], [1, 0]):
            weights = curriculum_weights([0, 1], predictions, 8, 10)
            self.assertAlmostEqual(float(weights.mean()), 1.)
            self.assertTrue(np.all(np.isfinite(weights)))
        for arguments in (([0], [0], -1, 10), ([0], [0], 11, 10), ([0], [0], 1, 0), ([0], [2], True, 10)):
            with self.assertRaises((ValueError, TypeError)):
                curriculum_weights(*arguments)

    def test_correctness_gates_speed_reward(self):
        fast_correct = correctness_speed_reward(True, .1, reference_seconds=1.)
        slow_correct = correctness_speed_reward(True, 10., reference_seconds=1.)
        fast_wrong = correctness_speed_reward(False, 0., reference_seconds=1.)
        self.assertGreater(fast_correct, slow_correct)
        self.assertGreater(slow_correct, fast_wrong)
        self.assertEqual(fast_wrong, -1.)
        self.assertEqual(correctness_speed_reward(False, 100.), -1.)
        self.assertEqual(correctness_speed_reward(True, 1., speed_weight=0.), 1.)
        self.assertLessEqual(correctness_speed_reward(True, 0., speed_weight=1.), 2.)
        for arguments in ((1, 1.), (True, -1.), (True, float("nan"))):
            with self.assertRaises((ValueError, TypeError)):
                correctness_speed_reward(*arguments)


if __name__ == "__main__":
    unittest.main()
