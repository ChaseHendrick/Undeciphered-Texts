"""Plain baseline tests obvious keys with no sentence-personality filter."""
import unittest
from tests.test_persona_emperor_solver import PLAIN,CAESAR,RAIL


class NormalManTest(unittest.TestCase):
    def test_literal_caesar_and_fence_controls_recover_without_a_key(self):
        from engine.solvers.persona_normal_man import investigate_normal_man
        for cipher in (CAESAR,RAIL):
            report=investigate_normal_man(cipher)
            self.assertEqual(report['candidates'][0]['plaintext'],PLAIN)
            self.assertTrue(report['candidates'][0]['forward_consistent'])
            self.assertEqual(report['checks'],32)
            self.assertIsNone(report['claimed_plaintext'])

    def test_zero_and_partial_budgets_are_honest(self):
        from engine.solvers.persona_normal_man import investigate_normal_man
        for budget in (0,1,10,31):
            report=investigate_normal_man(CAESAR,max_checks=budget)
            self.assertEqual(report['checks'],budget)
            self.assertFalse(report['search_complete'])
        self.assertTrue(investigate_normal_man(CAESAR,max_checks=32)['search_complete'])


if __name__=='__main__':unittest.main()
