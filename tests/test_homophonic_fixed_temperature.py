"""Fixed-temperature homophonic substitution recovery on a constructed fixture.

Method (fetched 2026-10-02):
https://ep.liu.se/ecp/158/012/ecp19158012.pdf

Nils Kopal, HistoCrypt 2019. The plaintext below is constructed for this
test. It is not printed in the paper. This does not solve army message
Nr. 86, Kryptos K4, or an unknown script.
"""

from __future__ import annotations

import hashlib
import json
import math
import unittest
from pathlib import Path

from engine.solvers.homophonic_fixed_temperature import (
    ACCEPT_FLOOR,
    DEFAULT_SEED,
    DEFAULT_STEPS,
    FIXED_TEMPERATURE,
    PAPER_URL,
    PAPER_YEAR,
    accepts_swap,
    fixture_plaintext,
    flatten_mapping,
    homophone_table,
    homophonic_decrypt,
    homophonic_encrypt,
    solve_homophonic_fixed_temperature,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "homophonic_fixed_temperature_certificate.json"
)


class HomophonicScopeTest(unittest.TestCase):
    def test_module_names_the_paper_and_the_limits(self) -> None:
        import engine.solvers.homophonic_fixed_temperature as mod

        doc = mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("2019", doc)
        self.assertIn(PAPER_URL, doc)
        self.assertIn("nr. 86", lowered)
        self.assertIn("k4", lowered)
        self.assertIn("unknown script", lowered)
        self.assertEqual(PAPER_YEAR, 2019)


class HomophonicAcceptanceTest(unittest.TestCase):
    def test_better_score_is_kept(self) -> None:
        self.assertTrue(accepts_swap(1.0, 0.0, draw=0.99))

    def test_tiny_degradation_can_pass_the_paper_floor(self) -> None:
        # exp(-0.01 / 2) is about 0.995, above the 0.0085 floor.
        self.assertGreater(math.exp(-0.01 / FIXED_TEMPERATURE), ACCEPT_FLOOR)
        self.assertTrue(accepts_swap(-0.01, 0.0, draw=0.5, temperature=FIXED_TEMPERATURE))
        self.assertFalse(accepts_swap(-0.01, 0.0, draw=0.999, temperature=FIXED_TEMPERATURE))

    def test_large_degradation_is_rejected(self) -> None:
        self.assertFalse(accepts_swap(-100.0, 0.0, draw=0.0, temperature=FIXED_TEMPERATURE))


class HomophonicRecoveryTest(unittest.TestCase):
    def test_solver_recovers_constructed_plaintext(self) -> None:
        plain = fixture_plaintext()
        table = homophone_table(plain)
        doubled = [letter for letter, codes in table.items() if len(codes) == 2]
        self.assertEqual(doubled, ["E"])
        cipher = homophonic_encrypt(plain, table)
        self.assertEqual(homophonic_decrypt(cipher, flatten_mapping(table)), plain)
        result = solve_homophonic_fixed_temperature(
            cipher,
            seed=DEFAULT_SEED,
            steps=DEFAULT_STEPS,
        )
        self.assertEqual(result.plaintext, plain)
        self.assertEqual(result.method, "homophonic_fixed_temperature")
        self.assertEqual(result.details["source_url"], PAPER_URL)
        self.assertEqual(result.details["year"], 2019)
        scope = result.details["scope"].lower()
        self.assertIn("nr. 86", scope)
        self.assertIn("k4", scope)
        self.assertIn("unknown script", scope)


class HomophonicCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_hash_source_and_recovery(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "homophonic_fixed_temperature")
        self.assertEqual(self.cert["source_url"], PAPER_URL)
        self.assertEqual(self.cert["year"], 2019)
        plaintext = self.cert["plaintext"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(plaintext, fixture_plaintext())
        mapping = self.cert["keys"]["mapping"]
        self.assertEqual(homophonic_decrypt(self.cert["ciphertext"], mapping), plaintext)
        self.assertEqual(
            homophonic_encrypt(plaintext, homophone_table(plaintext)),
            self.cert["ciphertext"],
        )
        result = solve_homophonic_fixed_temperature(
            self.cert["ciphertext"],
            seed=self.cert["keys"]["seed"],
            steps=self.cert["keys"]["steps"],
        )
        self.assertEqual(result.plaintext, plaintext)
        note = self.cert["note"].lower()
        self.assertIn("2019", self.cert["note"])
        self.assertIn("nr. 86", note)
        self.assertIn("k4", note)
        self.assertIn("unknown script", note)
        self.assertIn(PAPER_URL, self.cert["note"])


if __name__ == "__main__":
    unittest.main()
