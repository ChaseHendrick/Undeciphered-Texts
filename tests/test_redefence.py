"""ACA Redefence vector, independent fence oracle, and bounded blind search."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import unittest

from engine.solvers.redefence import (
    parse_redefence_key, redefence_decrypt, redefence_encrypt,
    search_redefence, solve_redefence,
)

PLAIN = "CIVILWARFIELDCIPHER"
CIPHER = "IIWRILCPECLFDHVAEIR"
BLIND_PLAIN = "THEHARBORBELLRANGTWICEBEFOREDAWNANDTHESMALLBOATSLEFTTHEQUAYWITHNETSFOLDEDONTHEDECKATHINMISTHIDTHEFARSHOREBUTTHECREWKNEWTHECHANNELBYTHESOUNDOFWATERAGAINSTSTONE"
# Independently laid out from engine.fixtures.CAESAR_PLAIN, ranks 2413, offset 3.
BLIND_CIPHER = "HROLRTIEOANTELBSEHQWTTFEOEETISHHFHRTHEKTENETENOTRISOEHBNEENMATANLTKMDRBCEHBOWGSTBLWFWHLLEISDDHTEOTWHNHDENNEAREAGCBRDADSAOTFTUYHEODNHCANIITASEUERNWCALYSUFAAATT"


def oracle(text, ranks, offset):
    # Walk the fence by direction changes, independent of modular row indexing.
    row, direction = 0, 1
    steps = []
    for _ in range(len(text) + offset):
        steps.append(row)
        if row == len(ranks) - 1:
            direction = -1
        elif row == 0:
            direction = 1
        row += direction
    buckets = [[] for _ in ranks]
    for letter, row in zip(text, steps[offset:]):
        buckets[row].append(letter)
    return "".join("".join(buckets[ranks.index(rank)]) for rank in range(1, len(ranks) + 1))


class RedefenceTest(unittest.TestCase):
    def test_literal_aca_example_and_equivalent_key(self):
        self.assertEqual(redefence_decrypt(CIPHER, "213", offset=0), PLAIN)
        self.assertEqual(redefence_encrypt("Civil war field cipher.", "213", offset=0), CIPHER)
        self.assertEqual(redefence_decrypt(CIPHER, "312", offset=2), PLAIN)
        self.assertEqual(redefence_encrypt(PLAIN, "312", offset=2), CIPHER)
        result = solve_redefence(CIPHER, key="213", offset=0)
        self.assertEqual(result.plaintext, PLAIN)
        self.assertEqual(result.details["mode"], "supplied_key")

    def test_independent_oracle_every_offset_and_order(self):
        for count in (3, 4):
            for ranks in itertools.permutations(range(1, count + 1)):
                for offset in range(2 * (count - 1)):
                    for plain in ("A", "ABCDEFGHIJK", "THERAINFELLBEFORETHESUNROSE"):
                        cipher = oracle(plain, ranks, offset)
                        self.assertEqual(redefence_encrypt(plain, ranks, offset=offset), cipher)
                        self.assertEqual(redefence_decrypt(cipher, ranks, offset=offset), plain)

    def test_rejects_malformed_keys_offsets_and_text(self):
        for key in ("12", "112", "124", "12345678", "１２３", 213, True, [1, 2, True]):
            with self.subTest(key=key), self.assertRaises((ValueError, TypeError)):
                parse_redefence_key(key)
        for offset in (-1, 4, True, "0"):
            with self.assertRaises((ValueError, TypeError)):
                redefence_decrypt(CIPHER, "213", offset=offset)
        with self.assertRaises(TypeError):
            solve_redefence(CIPHER, offset=0.0)
        for text in ("", "123", "CAFÉ", None, "A" * 4097):
            with self.assertRaises((ValueError, TypeError)):
                redefence_encrypt(text, "213")

    def test_candidate_and_key_bounds_are_explicit(self):
        result = search_redefence(CIPHER, min_rails=3, max_rails=4, max_keys=7, max_candidates=2)
        self.assertEqual(result.keys_examined, 7)
        self.assertEqual(result.total_keys, 168)
        self.assertFalse(result.search_complete)
        self.assertEqual(result.stop_reason, "key_limit")
        self.assertLessEqual(len(result.candidates), 2)
        self.assertEqual(result.uniqueness, "not_established")
        for values in ({"min_rails": 2}, {"max_rails": 8}, {"min_rails": 5, "max_rails": 3},
                       {"max_keys": 0}, {"max_candidates": True}, {"max_candidates": 101}):
            with self.assertRaises((ValueError, TypeError)):
                search_redefence(CIPHER, **values)

    def test_unknown_key_search_recovers_independent_literal_fixture(self):
        result = search_redefence(BLIND_CIPHER)
        self.assertTrue(result.search_complete)
        self.assertEqual(result.keys_examined, 1128)
        self.assertEqual(result.candidates[0].plaintext, BLIND_PLAIN)
        self.assertEqual(result.uniqueness, "not_established")
        for candidate in result.candidates:
            self.assertEqual(redefence_encrypt(candidate.plaintext, candidate.key, offset=candidate.offset), BLIND_CIPHER)
        solved = solve_redefence(BLIND_CIPHER)
        self.assertEqual(solved.plaintext, BLIND_PLAIN)
        self.assertEqual(solved.details["mode"], "score_ranked_search")
        self.assertFalse(solved.details["verified_historical_solve"])

    def test_equivalent_keys_and_tied_scores_do_not_claim_uniqueness(self):
        result = search_redefence("AAAAAA", min_rails=3, max_rails=3, max_candidates=2)
        self.assertTrue(result.search_complete)
        self.assertTrue(result.top_score_tied)
        self.assertEqual(result.uniqueness, "not_established")
        self.assertEqual(result.keys_examined, 24)
        self.assertEqual(len(result.candidates), 2)

    def test_short_or_oversized_blind_search_rejected(self):
        for text in ("ABC", "A" * 1025):
            with self.assertRaises(ValueError):
                search_redefence(text)

    def test_certificate_hash_is_of_recovered_published_output(self):
        path = Path(__file__).parents[1] / "engine/data/redefence_certificate.json"
        cert = json.loads(path.read_text())
        recovered = redefence_decrypt(cert["ciphertext"], cert["keys"]["key"], offset=cert["keys"]["offset"])
        self.assertEqual(cert["ciphertext"], CIPHER)
        self.assertEqual(recovered, PLAIN)
        self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(), cert["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
