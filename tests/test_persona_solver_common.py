"""Shared persona input and unverified-report contracts."""
import unittest
from engine.reverse_engineer import Crib


class PersonaCommonTest(unittest.TestCase):
    def test_crib_coordinates_and_conflict_are_preserved(self):
        from engine.persona_solver_common import validate_inputs
        letters, cribs, known = validate_inputs("AB CD-EF", (Crib(2, "cd"),), 10, 2)
        self.assertEqual(letters, "ABCDEF")
        self.assertEqual(cribs, (Crib(2, "CD"),))
        self.assertEqual(known, {2: "C", 3: "D"})
        with self.assertRaises(ValueError):
            validate_inputs("ABCDEF", (Crib(1, "CD"), Crib(2, "X")), 10, 2)

    def test_unsupported_inputs_and_bounds_fail(self):
        from engine.persona_solver_common import validate_inputs
        for text in ("", "ABC", "ABCD1", "ABCDα", "A" * 513):
            with self.assertRaises((TypeError, ValueError)):
                validate_inputs(text, (), 10, 2)
        for budget, retained in ((True, 2), (-1, 2), (100001, 2), (1, 0), (1, 101)):
            with self.assertRaises((TypeError, ValueError)):
                validate_inputs("ABCD", (), budget, retained)
        for crib in (Crib(True, "A"), Crib(4, "A"), Crib(0, "?")):
            with self.assertRaises((TypeError, ValueError)):
                validate_inputs("ABCD", (crib,), 10, 2)

    def test_personality_does_not_supply_correctness(self):
        from engine.persona_solver_common import make_report
        report = make_report("emperor", "systematic", [], 0, 0, False,
                             "check_budget", [], [])
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["correctness_known"])
        self.assertIsNone(report["happiness"])
        with self.assertRaises(ValueError):
            make_report("emperor", "systematic", [], 2, 1, False,
                        "check_budget", [], [])


if __name__ == "__main__":
    unittest.main()
