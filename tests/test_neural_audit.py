"""Independent corpus evaluation cannot silently reuse development or training text."""
import unittest
from engine.neural_router_v2 import evaluate_router
from engine.neural_grade import load_training_prose,TRAIN_PATH,HELD_EN_PATH
class IndependentRouterAuditTest(unittest.TestCase):
    def test_reused_corpora_and_invalid_controls_are_rejected(self):
        for path in (TRAIN_PATH,HELD_EN_PATH):
            with self.assertRaisesRegex(ValueError,'overlap'):
                evaluate_router(load_training_prose(path),samples_per_class=1)
        for value in ('A'*100, 'α'*1000, 'A'*100001):
            with self.assertRaises(ValueError):evaluate_router(value,samples_per_class=1)
        with self.assertRaises(ValueError):evaluate_router('ABCDEFGHIJ'*100,samples_per_class=0)
if __name__=='__main__':unittest.main()
