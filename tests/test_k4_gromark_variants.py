"""Gromark variants on K4: the generalized digit bound and Periodic Gromark as SAT."""

from __future__ import annotations

import importlib.util
import unittest

_HAS_SAT = importlib.util.find_spec("pysat") is not None

BLOCKED = ("F", "K", "P")


class K4DigitBoundTest(unittest.TestCase):
    def test_k4_blocks_the_same_letters_under_both_senses(self) -> None:
        from engine.k4_gromark_variants import digit_bound

        for sense in ("add", "subtract"):
            report = digit_bound(sense=sense)
            self.assertEqual(report["blocked_letters"], list(BLOCKED), sense)
            self.assertTrue(report["blocked"], sense)
            self.assertIs(report["solved"], False)
            self.assertIsNone(report["claimed_plaintext"])

    def test_the_bound_rejects_an_unknown_sense(self) -> None:
        from engine.k4_gromark_variants import digit_bound

        with self.assertRaises(ValueError):
            digit_bound(sense="rotate")

    def test_planted_gromark_texts_never_block(self) -> None:
        from engine.k4_gromark_variants import controls_digit_bound

        report = controls_digit_bound(trials=4)
        self.assertEqual(report["blocked"], 0)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


class K4PeriodicExhaustiveTest(unittest.TestCase):
    def test_two_head_lengths_exhaust_zero_relaxed_configs(self) -> None:
        from engine.k4_gromark_variants import excavate

        for k in (2, 3):
            report = excavate(k)
            self.assertEqual(report["fitting_configs"], 0, k)
            self.assertIs(report["solved"], False)
            self.assertIsNone(report["claimed_plaintext"])

    def test_excavate_refuses_large_head_lengths(self) -> None:
        from engine.k4_gromark_variants import excavate

        with self.assertRaises(ValueError):
            excavate(6)


@unittest.skipUnless(_HAS_SAT, "optional python-sat not installed")
class K4PeriodicSatTest(unittest.TestCase):
    def test_sample_head_lengths_are_unsat_for_both_clues(self) -> None:
        from engine.k4_gromark_variants import check

        for k in (2, 5, 9):
            self.assertEqual(check(k), "unsat", k)

    def test_planted_periodic_texts_are_never_blocked(self) -> None:
        from engine.k4_gromark_variants import check, planted

        for trial in range(3):
            k = (2, 5, 9)[trial]
            self.assertEqual(check(k, planted(k, seed=700 + trial)), "sat", k)

    def test_true_key_is_accepted_when_pinned(self) -> None:
        from engine.k4_gromark_variants import (planted, planted_key, relaxed_cnf,
                                                spec_of)
        from engine.k4_gromark_obstruction import CRIB_SPANS
        from engine.solvers.gromark import gromark_keyword
        from engine.solvers.periodic_gromark import (periodic_gromark_alphabet,
                                                     periodic_gromark_running_key)
        from pysat.solvers import Solver

        for k, seed in ((2, 701), (5, 702), (9, 704)):
            cipher = planted(k, seed)
            keyword = gromark_keyword(planted_key(k, seed))
            alphabet = periodic_gromark_alphabet(keyword)
            starts = [alphabet.index(ch) for ch in keyword]
            chain = [int(c) for c in periodic_gromark_running_key(keyword, len(cipher))]
            cnf = relaxed_cnf(k, cipher, spec_of(cipher, CRIB_SPANS), (0, 1))
            pins = [cnf["s"][g][starts[g]] for g in range(k)]
            pins += [cnf["r"][i][chain[i]] for i in range(len(cipher))]
            with Solver(name="cadical153", bootstrap_with=cnf["f"].clauses) as solver:
                self.assertTrue(solver.solve(assumptions=pins), (k, seed))

    def test_planted_reserved_letters_are_never_forced_wrong(self) -> None:
        from engine.k4_gromark_variants import fit_fold, planted

        for trial, k in enumerate((3, 6)):
            fit = trial % 2
            report = fit_fold(k, fit, planted(k, seed=800 + trial))
            self.assertTrue(report["fit_sat"], (k, fit))
            self.assertEqual(report["wrong"], 0, (k, fit))

    def test_k4_folds_contradict_at_sample_head_lengths(self) -> None:
        from engine.k4_gromark_variants import fit_fold

        # head length 2 cannot place either clue alone
        for fit in (0, 1):
            report = fit_fold(2, fit)
            self.assertFalse(report["fit_sat"], fit)
        # head length 7 fits EASTNORTHEAST alone but forces reserved letters wrong
        report = fit_fold(7, 0)
        self.assertTrue(report["fit_sat"])
        self.assertGreater(report["wrong"], 0)

    def test_report_claims_nothing(self) -> None:
        from engine.k4_gromark_variants import scan

        report = scan(head_lengths=(2, 3), workers=1)
        self.assertEqual(report["excluded_head_lengths"], [2, 3])
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
