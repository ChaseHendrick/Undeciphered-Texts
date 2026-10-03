"""Bounded composition of existing transforms, independently checked controls."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.transposition_ensemble import search_transposition_ensemble, reencrypt_transposition
from engine.solvers.columnar import KRYPTOS_K3_CIPHERTEXT

PLAIN = "THEHARBORBELLRANGTWICEBEFOREDAWNANDTHESMALLBOATSLEFTTHEQUAYWITHNETSFOLDEDONTHEDECKATHINMISTHIDTHEFARSHOREBUTTHECREWKNEWTHECHANNELBYTHESOUNDOFWATERAGAINSTSTONE"
CIPHER = "HROLRTIEOANTELBSEHQWTTFEOEETISHHFHRTHEKTENETENOTRISOEHBNEENMATANLTKMDRBCEHBOWGSTBLWFWHLLEISDDHTEOTWHNHDENNEAREAGCBRDADSAOTFTUYHEODNHCANIITASEUERNWCALYSUFAAATT"


class TranspositionEnsembleTest(unittest.TestCase):
    def test_blind_literal_redefence_fixture_and_uniform_contract(self):
        result = search_transposition_ensemble(CIPHER)
        self.assertEqual(result.candidates[0].plaintext, PLAIN)
        self.assertTrue(result.search_complete)
        self.assertEqual(result.checks, result.total_checks)
        self.assertEqual(result.uniqueness, "not_established")
        self.assertIsNone(result.claimed_plaintext)
        self.assertEqual(set(result.family_checks), {"rail-fence", "route", "columnar", "redefence"})
        self.assertEqual(len({c.plaintext for c in result.candidates}), len(result.candidates))
        for candidate in result.candidates:
            self.assertTrue(candidate.re_encryption_matches)
            self.assertEqual(reencrypt_transposition(candidate), CIPHER)
        json.dumps(result.to_dict())

    def test_existing_rail_and_route_examples_with_cribs_not_keys(self):
        controls = [("DNETLHSEEDHESWLOTEATEFTAAFCL", "DEFENDTHEEASTWALLOFTHECASTLE", "DEFEND", "rail-fence"),
                    ("ITAHEVONOGBRHND", "BRIGHTONANDHOVE", "BRIGHTON", "route")]
        for cipher, plain, crib, family in controls:
            report = search_transposition_ensemble(cipher, cribs=(Crib(0, crib),))
            self.assertEqual(report.candidates[0].plaintext, plain)
            self.assertEqual(report.crib_positions, len(crib))
            self.assertTrue(any(key["family"] == family for key in report.candidates[0].equivalent_keys))

    def test_existing_published_k3_under_explicit_width_bound(self):
        report = search_transposition_ensemble(KRYPTOS_K3_CIPHERTEXT, max_width=28,
                                              max_rails=3, cribs=(Crib(0, "SLOWLY"),))
        self.assertTrue(report.search_complete)
        recovered = report.candidates[0]
        self.assertTrue(recovered.plaintext.startswith("SLOWLYDESPARATLYSLOWLY"))
        self.assertEqual(reencrypt_transposition(recovered), KRYPTOS_K3_CIPHERTEXT)
        self.assertTrue(any(x["family"] == "columnar" and tuple(x["key"].get("widths", ())) == (21, 28)
                            for x in recovered.equivalent_keys))

    def test_round_robin_budget_and_zero_budget(self):
        report = search_transposition_ensemble("ABCDEFGHIJKL", max_checks=4, max_candidates=2)
        self.assertEqual(report.checks, 4)
        self.assertEqual(report.family_checks, {"rail-fence": 1, "route": 1, "columnar": 1, "redefence": 1})
        self.assertFalse(report.search_complete)
        self.assertEqual(report.stop_reason, "check_limit")
        self.assertLessEqual(len(report.candidates), 2)
        report = search_transposition_ensemble("ABCDEFGHIJKL", max_checks=0)
        self.assertEqual(report.candidates, ())
        self.assertEqual(report.checks, 0)
        self.assertFalse(report.search_complete)

    def test_all_identical_plaintexts_deduplicate_and_bound_key_aliases(self):
        report = search_transposition_ensemble("AAAAAA")
        self.assertEqual(len(report.candidates), 1)
        self.assertTrue(report.search_complete)
        self.assertEqual(report.duplicate_candidates, report.checks - 1)
        self.assertEqual(report.candidates[0].equivalent_keys_seen, report.checks)
        self.assertLessEqual(len(report.candidates[0].equivalent_keys), 8)
        self.assertEqual(report.uniqueness, "not_established")

    def test_forward_check_rejects_an_injected_broken_decrypt(self):
        with patch("engine.transposition_ensemble.rail_fence_decrypt", return_value="A" * 12):
            report = search_transposition_ensemble("ABCDEFGHIJKL", max_checks=4)
        self.assertEqual(report.re_encryption_mismatches, 1)
        self.assertFalse(any(c.family == "rail-fence" for c in report.candidates))
        self.assertTrue(all(c.re_encryption_matches for c in report.candidates))

    def test_crib_rejection_and_duplicate_confirmations(self):
        report = search_transposition_ensemble(CIPHER, cribs=(Crib(0, "THE"), Crib(0, "THE")))
        self.assertEqual(report.crib_positions, 3)
        self.assertEqual(report.candidates[0].plaintext, PLAIN)
        self.assertGreater(report.crib_rejections, 0)
        report = search_transposition_ensemble("ABCDEFGHIJKL", cribs=(Crib(0, "ZZ"),))
        self.assertEqual(report.candidates, ())
        self.assertTrue(report.search_complete)

    def test_rejects_invalid_types_limits_and_crib_alignment(self):
        for values in ({"max_candidates": 0}, {"max_candidates": True}, {"max_checks": -1},
                       {"max_checks": 100001}, {"max_width": 33}, {"max_rails": 2},
                       {"max_rails": 8}, {"cribs": (Crib(-1, "A"),)},
                       {"cribs": (Crib(12, "A"),)}, {"cribs": (Crib(0, "A"), Crib(0, "B"))},
                       {"cribs": (Crib(0, "CAFÉ"),)}, {"cribs": ((0, "A"),)}):
            with self.subTest(values=values), self.assertRaises((ValueError, TypeError)):
                search_transposition_ensemble("ABCDEFGHIJKL", **values)
        for text in ("ABC", "A" * 1025, "CAFÉ", None):
            with self.assertRaises((ValueError, TypeError)):
                search_transposition_ensemble(text)

    def test_certificate_hashes_an_actual_blind_candidate(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/transposition_ensemble_certificate.json").read_text())
        report = search_transposition_ensemble(cert["ciphertext"], **cert["search_limits"])
        self.assertEqual(report.candidates[0].plaintext, PLAIN)
        self.assertEqual(hashlib.sha256(report.candidates[0].plaintext.encode("ascii")).hexdigest(), cert["plaintext_sha256"])
        self.assertNotIn("cipher_name", cert)


if __name__ == "__main__":
    unittest.main()
