"""K4 Hill 5 by 5 to 10 by 10: exact row algebra and the 5 by 5 enumeration.

Nothing here reads K4. The checks only rule settings out, and a planted
key must never be ruled out.
"""

from __future__ import annotations

import itertools
import unittest

import numpy as np


class K4HillLargeTest(unittest.TestCase):
    def test_k4_report_claims_nothing(self) -> None:
        from engine.k4_hill_large import scan

        report = scan()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["rows"]), 4 * sum(range(5, 11)))
        excluded = {(r["numbering"], r["alignment"]) for r in report["rows"] if r["status"] == "excluded"}
        self.assertEqual(excluded, {
            ("A-Z", 2), ("A-Z", 3), ("KRYPTOS", 1), ("KRYPTOS", 2), ("KRYPTOS", 3),
            ("PALIMPSEST", 2), ("PALIMPSEST", 3), ("PALIMPSEST", 4),
            ("ABSCISSA", 1), ("ABSCISSA", 2), ("ABSCISSA", 4),
        })
        self.assertTrue(all(r["size"] == 5 for r in report["rows"] if r["status"] == "excluded"))

    def test_algebra_matches_brute_force_rows(self) -> None:
        from engine.k4_hill_large import CRIB_SPANS, K4_CIPHERTEXT, LETTERS, known_blocks, row_system

        # A-Z, alignment 3: 4 known blocks, row 3 has no solution mod 26.
        blocks = known_blocks(5, 3, CRIB_SPANS, K4_CIPHERTEXT, LETTERS)
        c = np.array([b[1] for b in blocks])
        p = np.array([b[2] for b in blocks])
        rest = np.indices((26,) * 4).reshape(4, -1).T.astype(np.int64)
        counts = [0] * 5
        for x in range(26):
            rows = np.hstack([np.full((len(rest), 1), x), rest])
            values = (rows @ c.T) % 26
            for j in range(5):
                counts[j] += int(np.all(values == p[:, j], axis=1).sum())
        self.assertEqual(counts, row_system(5, blocks)["row_counts"])
        self.assertEqual(counts, [52, 52, 52, 0, 52])

    def test_rank_exclusion_has_no_invertible_choice_mod_2(self) -> None:
        from engine.k4_hill_large import CRIB_SPANS, K4_CIPHERTEXT, NUMBERINGS, known_blocks, rank_mod, row_system

        # ABSCISSA, alignment 4: every row fits, yet every fitted matrix is singular mod 2.
        system = row_system(5, known_blocks(5, 4, CRIB_SPANS, K4_CIPHERTEXT, NUMBERINGS["ABSCISSA"]))
        self.assertTrue(all(system["consistent"]))
        self.assertFalse(system["invertible_exists"])
        sol = system["per_prime"][2]
        sets = []
        for j in range(5):
            vectors = [sol["particular"][j]]
            for v in sol["basis"]:
                vectors += [(w + v) % 2 for w in vectors]
            sets.append(vectors)
        self.assertFalse(any(rank_mod(np.array(choice), 2) == 5 for choice in itertools.product(*sets)))

    def test_planted_keys_are_never_excluded(self) -> None:
        from engine.k4_hill_large import NUMBERINGS, SIZES, check, planted

        for numbering in NUMBERINGS:
            for n in SIZES:
                for alignment in range(n):
                    ciphertext, _key = planted(n, alignment, seed=n * 100 + alignment, numbering=numbering)
                    self.assertEqual(check(n, alignment, numbering, ciphertext)["status"], "open",
                                     (numbering, n, alignment))

    def test_planted_control_recovers_the_true_key(self) -> None:
        from engine.k4_hill_large import planted_control

        report = planted_control(4, seed=4000)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["status"], "enumerated")
        self.assertEqual(report["true_rank_quadgram"], 1)
        self.assertTrue(report["true_first_invertible"])

    def test_k4_enumeration_claims_nothing(self) -> None:
        from engine.k4_hill_large import enumerate_keys

        report = enumerate_keys(5, 4, "A-Z", top=3)
        self.assertEqual(report["keys"], 26 ** 5)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
