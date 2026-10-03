"""Crib-constrained model inference, not unsolved-text decipherment."""

import contextlib
import hashlib
import io
import json
import unittest
import tempfile
from pathlib import Path

from engine.cli import main
from engine.reverse_engineer import Crib, infer_cipher_models, predict_plaintext


class ReverseEngineerTest(unittest.TestCase):
    def test_infers_vigenere_from_crib_and_predicts_unseen_suffix(self):
        report = infer_cipher_models("LXFOPVEFRNHR", cribs=[Crib(0, "ATTACK")], max_period=5)
        hit = next(h for h in report.hypotheses if h.family == "vigenere" and h.period == 5)
        self.assertEqual(hit.key, "LEMON")
        self.assertEqual(hit.predicted_plaintext, "ATTACKATDAWN")
        self.assertEqual(hit.confirmations, 1)
        self.assertEqual(hit.unresolved_parameters, 0)
        self.assertEqual(predict_plaintext("EFRNHR", hit, offset=6), "ATDAWN")
        self.assertIsNone(report.claimed_plaintext)

    def test_sparse_crib_retains_unknown_key_slots_and_plaintext(self):
        report = infer_cipher_models("BCDEF", cribs=[Crib(1, "A")], max_period=4)
        hit = next(h for h in report.hypotheses if h.family == "vigenere" and h.period == 4)
        self.assertEqual(hit.key, "?C??")
        self.assertEqual(hit.unresolved_parameters, 3)
        self.assertEqual(hit.confirmations, 0)
        self.assertEqual(hit.predicted_plaintext, "?A???")

    def test_two_disjoint_cribs_constrain_the_same_period(self):
        report = infer_cipher_models("LXFOPVEFRNHR", cribs=[Crib(0, "ATT"), Crib(3, "ACK")], max_period=5)
        self.assertTrue(any(h.family == "vigenere" and h.key == "LEMON" for h in report.hypotheses))

    def test_impossible_constraints_reject_all_tested_models(self):
        report = infer_cipher_models("BC", cribs=[Crib(0, "AA")], max_period=1)
        self.assertEqual(report.hypotheses, ())
        self.assertIsNone(report.claimed_plaintext)

    def test_affine_formula_is_inferred_without_a_key(self):
        report = infer_cipher_models("IHHWVCSWFRCP", cribs=[Crib(0, "AFFINECIPHER")], max_period=1)
        hit = next(h for h in report.hypotheses if h.family == "affine")
        self.assertEqual(hit.parameters, {"multiplier": 5, "offset": 8})
        self.assertEqual(hit.predicted_plaintext, "AFFINECIPHER")
        self.assertEqual(predict_plaintext("I", hit), "A")

    def test_partial_substitution_does_not_invent_unseen_mappings(self):
        report = infer_cipher_models("QWERQZ", cribs=[Crib(0, "ABCD")], max_period=1)
        hit = next(h for h in report.hypotheses if h.family == "substitution")
        self.assertEqual(hit.predicted_plaintext, "ABCDA?")
        self.assertEqual(hit.unresolved_parameters, 22)

    def test_beaufort_known_example_predicts_outside_crib(self):
        report = infer_cipher_models("PAMOPGWSODEKKT", cribs=[Crib(0, "CEQUALSKMI")], max_period=10)
        hit = next(h for h in report.hypotheses if h.family == "beaufort" and h.period == 10)
        self.assertEqual(hit.key, "RECIPROCAL")
        self.assertEqual(hit.predicted_plaintext, "CEQUALSKMINUSP")

    def test_duplicate_cribs_do_not_inflate_confirmations(self):
        report = infer_cipher_models("LXFOPVEFRNHR", cribs=[Crib(0, "ATTACK"), Crib(0, "ATTACK")], max_period=5)
        self.assertEqual(report.known_positions, 6)
        hit = next(h for h in report.hypotheses if h.family == "vigenere" and h.period == 5)
        self.assertEqual(hit.confirmations, 1)

    def test_k4_public_cribs_do_not_become_a_claimed_solution(self):
        from engine.solvers.k4_attempt import CRIBS, K4_CIPHERTEXT

        report = infer_cipher_models(K4_CIPHERTEXT,
                                     cribs=[Crib(start - 1, word) for start, word, _ in CRIBS],
                                     max_period=16)
        self.assertEqual(report.known_positions, 24)
        self.assertEqual(report.hypotheses, ())
        self.assertIsNone(report.claimed_plaintext)

    def test_bad_offsets_conflicts_alphabets_and_bounds_are_rejected(self):
        for cipher, cribs, bound in (
            ("ABC", [], 2), ("ABC", [Crib(-1, "A")], 2),
            ("ABC", [Crib(3, "A")], 2), ("ABC", [Crib(0, "")], 2),
            ("ABC", [Crib(0, "A"), Crib(0, "B")], 2),
            ("caf\u00e9", [Crib(0, "A")], 2), ("ABC", [Crib(0, "\u00df")], 2),
            ("ABC", [Crib(0, "A")], 0), ("ABC", [Crib(0, "A")], 129),
        ):
            with self.subTest(cipher=cipher, cribs=cribs, bound=bound):
                with self.assertRaises(ValueError):
                    infer_cipher_models(cipher, cribs=cribs, max_period=bound)
        with self.assertRaises(ValueError):
            infer_cipher_models("ABC", cribs=iter(()))

    def test_cli_reports_json_hypotheses_without_claiming_plaintext(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["reverse-engineer", "LXFOPVEFRNHR", "--crib", "0:ATTACK", "--max-period", "5"])
        self.assertEqual(status, 0)
        report = json.loads(output.getvalue())
        self.assertIsNone(report["claimed_plaintext"])
        self.assertTrue(any(h["key"] == "LEMON" for h in report["hypotheses"]))
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["reverse-engineer", "ABC", "--crib", "bad"]), 2)

    def test_word_pattern_cli_keeps_ambiguous_results_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            lexicon = Path(directory) / "words.txt"
            lexicon.write_text("AN NA AT TA\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = main(["word-pattern", "AB BA", "--lexicon", str(lexicon)])
            self.assertEqual(status, 0)
            result = json.loads(output.getvalue())
            self.assertEqual(result["plaintext"], "")
            self.assertTrue(result["details"]["ambiguous"])
            self.assertTrue(result["details"]["search_complete"])
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["word-pattern", "AB BA", "--lexicon", str(lexicon) + ".missing"]), 2)


class ReverseEngineerCertificateTest(unittest.TestCase):
    def test_published_vector_recovery_and_heldout_suffix_hash(self):
        path = Path(__file__).resolve().parents[1] / "engine/data/reverse_engineer_certificate.json"
        cert = json.loads(path.read_text(encoding="utf-8"))
        report = infer_cipher_models(cert["ciphertext"], cribs=[Crib(**row) for row in cert["cribs"]],
                                     max_period=cert["max_period"])
        hit = next(h for h in report.hypotheses if h.family == cert["family"] and h.period == cert["period"])
        self.assertEqual(hit.predicted_plaintext, cert["plaintext"])
        self.assertEqual(hashlib.sha256(hit.predicted_plaintext.encode("ascii")).hexdigest(), cert["plaintext_sha256"])
        self.assertLess(report.known_positions, len(cert["plaintext"]))
        self.assertIsNone(report.claimed_plaintext)


if __name__ == "__main__":
    unittest.main()
