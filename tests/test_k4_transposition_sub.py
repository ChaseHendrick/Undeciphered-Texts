"""Transposition plus periodic substitution on K4: planted controls, K3, kernel checks."""

from __future__ import annotations

import itertools
import random
import unittest

import numpy as np

from engine import k4_transposition_sub as ts
from engine.k4_periodic_bijection import scan_periods
from engine.solvers.myszkowski import myszkowski_encrypt


class K4TranspositionSubTest(unittest.TestCase):
    def test_k3_reproduced_by_rotation_family(self) -> None:
        result = ts.k3_reproduced()
        self.assertTrue(result["encrypt_matches"])
        self.assertTrue(result["decrypt_matches"])

    def test_identity_matches_in_place_bound(self) -> None:
        s = ts.setup(97)
        stats = ts.run_perms(s, np.array([list(range(97))]), threads=1)["stats"]
        blocked = [p for p in range(1, 27) if stats[0, p, 1] == 0]
        self.assertEqual(blocked, [p for p in scan_periods(max_period=26)["blocked"]])

    def test_kernel_matches_reference(self) -> None:
        rng = random.Random(5)
        for n in ts.LENGTHS:
            s = ts.setup(n)
            perms = [rng.sample(range(n), n) for _ in range(40)]
            perms += [ts.columnar_perm(n, rng.sample(range(7), 7), rng.randrange(2)) for _ in range(40)]
            stats = ts.run_perms(s, np.array(perms), threads=1)["stats"]
            for comp in (0, 1):
                for p in range(1, 27):
                    bij = sum(ts.bijection_ok(perm, s, comp, p) for perm in perms)
                    self.assertEqual(stats[comp, p, 1], bij)
                    for v in range(4):
                        strong = sum(ts.bijection_ok(perm, s, comp, p) and ts.strong_key(perm, s, comp, p, v)
                                     is not None for perm in perms)
                        self.assertEqual(stats[comp, p, 2 + v], strong)

    def test_columnar_kernel_enumerates_every_order(self) -> None:
        for n in ts.LENGTHS:
            s = ts.setup(n)
            full = ts.run_columnar(s, widths=(5,), threads=1)
            perms = [ts.columnar_perm(n, o, d) for o in itertools.permutations(range(5)) for d in (0, 1)]
            listed = ts.run_perms(s, np.array(perms), threads=1)
            self.assertEqual(full["orders"], {5: 120})
            self.assertTrue((full["stats"] == listed["stats"]).all())

    def test_myszkowski_perm_matches_solver(self) -> None:
        text = "".join(random.Random(2).choice(ts.LETTERS) for _ in range(97))
        perm = ts.myszkowski_perm(97, "UNDERGRUUND")
        self.assertEqual("".join(ts.apply(perm, text)), myszkowski_encrypt(text, "UNDERGRUUND").replace(" ", ""))

    def test_planted_controls_never_excluded(self) -> None:
        for family, rec in ts.planted_controls(trials=60, seed=11).items():
            self.assertEqual(rec["true_excluded"], 0, family)
            self.assertEqual(rec["strong_true_excluded"], 0, family)
            self.assertEqual(rec["strong_complete_recovered"], rec["strong_complete_keys"], family)

    def test_planted_columnar_found_by_full_enumeration(self) -> None:
        rng = random.Random(3)
        for n in ts.LENGTHS:
            s = ts.setup(n)
            plain = [rng.randrange(26) for _ in range(n)]
            for j, pl in zip(s["cpos"], s["cpl"]):
                plain[j] = pl
            order, direction, p, v = rng.sample(range(6), 6), rng.randrange(2), 7, rng.randrange(4)
            perm = ts.columnar_perm(n, order, direction)
            key = [rng.randrange(26) for _ in range(p)]
            s = dict(s, ct=ts.encipher(plain, perm, 1, ts.shift_alphabets(v, key)))
            found = ts.run_columnar(s, widths=(6,), threads=1)["cands"]
            self.assertIn((1, p, v, (6, direction, *order)), found)

    def test_power_is_real_at_short_periods(self) -> None:
        for family, rec in ts.power(samples=60, texts=4, seed=1).items():
            for comp in ts.COMPOSITIONS:
                self.assertGreaterEqual(min(rec[comp]["excluded_fraction_by_period"][:3]), 0.95, family)

    def test_k4_report_claims_nothing(self) -> None:
        report = ts.k4_report(families=("b-rotation", "c-route", "d-keyword"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        for run in report["runs"]:
            self.assertIs(run["solved"], False)
            self.assertIsNone(run["claimed_plaintext"])
            for summary in run["summary"].values():
                self.assertEqual(sum(summary["strong_any_by_period"][:20]), 0)
            for rec in run["candidates"]:
                self.assertGreaterEqual(rec["period"], 21)
                self.assertLessEqual(rec["clue_checks"], 3)
        keyword = [r for r in report["runs"] if r["family"] == "d-keyword" and r["n"] == 97][0]
        self.assertEqual(keyword["summary"]["transpose-then-substitute"]["bijection_survivors"], 531)
        self.assertEqual(keyword["summary"]["substitute-then-transpose"]["bijection_survivors"], 883)


if __name__ == "__main__":
    unittest.main()
