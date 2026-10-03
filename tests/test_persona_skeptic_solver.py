"""Reserved evidence is compared only after generation or explicit review."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.persona_skeptic import investigate_skeptic

PLAIN = "THEHEIRREADTHESEALEDLETTERANDMOVEDTHEGOLDTOTHEESTATEBEFORESUNRISE"
CIPHER = "AOLOLPYYLHKAOLZLHSLKSLAALYHUKTVCLKAOLNVSKAVAOLLZAHALILMVYLZBUYPZL"
HASH = "c418192d13583f9b0d4f482baad3cbbc210d8746b76b0f232aa1697f9469b432"


class SkepticSolverTest(unittest.TestCase):
    def test_literal_unknown_key_control_verified_after_generation(self):
        report = investigate_skeptic(CIPHER, cribs=(Crib(0, "THE"),),
            verification_cribs=(Crib(11, "THESEALEDLETTER"),), expected_plaintext_sha256=HASH)
        self.assertTrue(any(c["plaintext"] == PLAIN for c in report["candidates"]))
        review = next(r for r in report["reviews"] if r["plaintext"] == PLAIN)
        self.assertEqual(review["status"], "exact-reference-match")
        self.assertFalse(report["correctness_known"])
        self.assertIsNone(report["claimed_plaintext"])

    def test_reserved_content_and_hash_never_enter_search_and_wrong_high_score_rejects(self):
        from engine.solver_reasoning import investigate_cipher
        wrong = PLAIN[:10] + "A" * (len(PLAIN) - 10)
        class Controlled:
            def to_dict(self):
                ledger = investigate_cipher(CIPHER, cribs=(Crib(0, "THE"),), max_checks=500, max_candidates=2).to_dict()
                true = next(c for c in ledger["candidates"] if c["plaintext"] == PLAIN)
                false = dict(true, plaintext=wrong, score=1000000.0)
                ledger["candidates"] = [false, true]
                return ledger
        with patch("engine.solvers.persona_skeptic.investigate_cipher", return_value=Controlled()) as run:
            report = investigate_skeptic(CIPHER, cribs=(Crib(0, "THE"),),
                verification_cribs=(Crib(11, "THESEALEDLETTER"),), expected_plaintext_sha256=HASH)
        self.assertEqual(run.call_args.kwargs["cribs"], (Crib(0, "THE"),))
        self.assertNotIn("verification_cribs", run.call_args.kwargs)
        self.assertNotIn("expected_plaintext_sha256", run.call_args.kwargs)
        self.assertEqual([c["plaintext"] for c in report["candidates"]], [PLAIN])
        self.assertEqual(next(r for r in report["reviews"] if r["plaintext"] == wrong)["status"], "contradicted")

    def test_review_only_does_not_search_or_assert_unkeyed_forward_consistency(self):
        with patch("engine.solvers.persona_skeptic.investigate_cipher", side_effect=AssertionError("no new search")):
            report = investigate_skeptic(CIPHER, candidate_plaintexts=(PLAIN, "A" * len(PLAIN)), expected_plaintext_sha256=HASH)
        self.assertEqual(report["checks"], 2)
        self.assertEqual(report["candidates"], [])
        self.assertFalse(report["search_executed"])
        self.assertEqual([r["status"] for r in report["reviews"]], ["exact-reference-match", "contradicted"])
        self.assertTrue(all(r["forward_consistent"] is None for r in report["reviews"]))

    def test_crib_support_hash_mismatch_and_missing_reference_have_distinct_verdicts(self):
        supported = investigate_skeptic(CIPHER, candidate_plaintexts=(PLAIN,), verification_cribs=(Crib(11, "THESEALEDLETTER"),))
        self.assertEqual(supported["reviews"][0]["status"], "crib-supported")
        unchecked = investigate_skeptic(CIPHER, candidate_plaintexts=(PLAIN,))
        self.assertEqual(unchecked["reviews"][0]["status"], "unchecked")
        rejected = investigate_skeptic(CIPHER, candidate_plaintexts=(PLAIN,), expected_plaintext_sha256="0" * 64)
        self.assertEqual(rejected["reviews"][0]["status"], "contradicted")

    def test_strict_combined_budget_and_review_only_exhaustion(self):
        for budget in (0, 1, 2, 26, 500):
            report = investigate_skeptic(CIPHER, cribs=(Crib(0, "THE"),), expected_plaintext_sha256=HASH,
                max_checks=budget, max_candidates=3)
            self.assertLessEqual(report["checks"], budget)
            self.assertEqual(report["checks"], report["search_checks"] + report["verification_checks"])
        report = investigate_skeptic(CIPHER, candidate_plaintexts=(PLAIN, "A" * len(PLAIN)), max_checks=1)
        self.assertEqual(report["checks"], 1)
        self.assertEqual(len(report["reviews"]), 1)
        self.assertFalse(report["search_complete"])
        self.assertEqual(report["unreviewed_candidates"], 1)

    def test_reserved_cribs_must_be_separate_from_fitted_evidence(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            investigate_skeptic(CIPHER, cribs=(Crib(0, "THE"),), verification_cribs=(Crib(0, "THE"),))

    def test_optional_neural_fallback_preserves_post_validation(self):
        with patch.dict("sys.modules", {"numpy": None}):
            report = investigate_skeptic(CIPHER, expected_plaintext_sha256=HASH)
        self.assertEqual(report["ledger"]["neural_advice"]["status"], "unavailable")
        self.assertTrue(any(r["status"] == "exact-reference-match" for r in report["reviews"]))

    def test_invalid_hash_review_types_coordinates_and_bounds(self):
        for digest in (123, "", "x" * 64, "0" * 63):
            with self.assertRaises((TypeError, ValueError)):
                investigate_skeptic(CIPHER, expected_plaintext_sha256=digest)
        for values in (PLAIN, (1,), ("A" * 64,), ("α" * 65,), tuple(PLAIN for _ in range(101))):
            with self.assertRaises((TypeError, ValueError)):
                investigate_skeptic(CIPHER, candidate_plaintexts=values)
        with self.assertRaises(ValueError):
            investigate_skeptic(CIPHER, verification_cribs=(Crib(64, "TOOLONG"),))

    def test_voice_changes_only_narration_not_any_answer_or_evidence(self):
        for mode in ({"candidate_plaintexts": (PLAIN, "A" * len(PLAIN))}, {}):
            reports = []
            for voice in ("dale", "plain"):
                report = investigate_skeptic(CIPHER, expected_plaintext_sha256=HASH, voice=voice, **mode)
                del report["voice"], report["narration"]
                if report["ledger"] is not None:
                    del report["ledger"]["elapsed_seconds"]
                reports.append(report)
            self.assertEqual(reports[0], reports[1])
        with self.assertRaises(ValueError):
            investigate_skeptic(CIPHER, voice="paranoia-as-proof")

    def test_certificate_hashes_recovered_plaintext_after_comparison(self):
        path = Path(__file__).resolve().parents[1] / "engine/data/persona_skeptic_solver_certificate.json"
        vector = json.loads(path.read_text())
        report = investigate_skeptic(vector["ciphertext"], cribs=tuple(Crib(**c) for c in vector["training_cribs"]),
            verification_cribs=tuple(Crib(**c) for c in vector["verification_cribs"]),
            expected_plaintext_sha256=vector["plaintext_sha256"])
        review = next(r for r in report["reviews"] if r["status"] == "exact-reference-match")
        self.assertEqual(hashlib.sha256(review["plaintext"].encode("ascii")).hexdigest(), vector["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
