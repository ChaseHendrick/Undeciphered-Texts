"""Router checks: three certified ciphertexts pick the right solver family.

The net may route only ciphers this repository already certifies. It must
not claim a reading of Kryptos K4, Nr. 86, Linear A, Indus, Voynich, or
rongorongo.
"""

from __future__ import annotations

import hashlib
import unittest

from engine.solver_net import KNOWN_SOLVERS, SCOPE, get_solver_net, load_certificate


CASES = (
    ("caesar_certificate.json", "caesar"),
    ("playfair_certificate.json", "playfair"),
    ("adfgvx_certificate.json", "adfgvx"),
)


class SolverNetCatalogTest(unittest.TestCase):
    def test_catalog_lists_every_certified_solver(self) -> None:
        expected = {
            "caesar",
            "vigenere",
            "keyed-vigenere",
            "substitution",
            "playfair",
            "bifid",
            "adfgvx",
            "columnar",
            "two-square",
            "crib",
            "beam-search",
            "lumen-braid",
            "prism-latch",
        }
        self.assertEqual(set(KNOWN_SOLVERS), expected)
        net = get_solver_net()
        self.assertGreaterEqual(len(net.exemplars), len(expected) - 1)


class SolverNetRouteTest(unittest.TestCase):
    def test_three_certificate_ciphertexts_route_and_recover(self) -> None:
        net = get_solver_net()
        for certificate_id, solver in CASES:
            with self.subTest(ciphertext=certificate_id, solver=solver):
                certificate = load_certificate(certificate_id)
                ciphertext = certificate["ciphertext"]
                link = net.route(ciphertext)
                self.assertEqual(link.solver, solver)
                self.assertEqual(link.family, solver)
                self.assertEqual(link.certificate_id, certificate_id)
                self.assertIn("index_of_coincidence", link.features)
                self.assertIn("digraph_repeat_rate", link.features)
                self.assertIn("adfgvx_alphabet_ratio", link.features)
                self.assertIn("even_length", link.features)
                self.assertTrue(link.causing_features)
                self.assertTrue(any(item["contribution"] > 0 for item in link.causing_features))
                self.assertIn("K4", link.scope)
                self.assertIn(SCOPE.split(".")[0], link.scope)
                result = net.recover(ciphertext, link)
                self.assertEqual(result.plaintext, certificate["plaintext"])
                digest = hashlib.sha256(result.plaintext.encode("utf-8")).hexdigest()
                self.assertEqual(digest, certificate["plaintext_sha256"])
                self.assertEqual(result.details["solver_net"]["solver"], solver)
                self.assertEqual(result.details["solver_net"]["certificate_id"], certificate_id)

    def test_vigenere_route_names_the_crib_solver(self) -> None:
        net = get_solver_net()
        certificate = load_certificate("vigenere_certificate.json")
        link = net.route(certificate["ciphertext"])
        self.assertEqual(link.solver, "vigenere")
        self.assertEqual(link.certificate_id, "vigenere_certificate.json")
        self.assertIn("crib", link.related_solvers)


class SolverNetUnreadTest(unittest.TestCase):
    def test_unknown_scripts_stay_unread(self) -> None:
        net = get_solver_net()
        for script in ("K4", "Nr. 86", "Linear A", "Indus", "Voynich", "rongorongo"):
            with self.subTest(script=script):
                link = net.decline(script)
                self.assertEqual(link.family, "unreadable")
                self.assertEqual(link.solver, "")
                self.assertEqual(link.certificate_id, "")
                self.assertTrue(link.unread)
                with self.assertRaises(RuntimeError):
                    net.recover("ATTACK", link)


if __name__ == "__main__":
    unittest.main()
