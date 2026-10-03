"""Structured case intake, source integrity, and bounded hypothesis runs."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.case_workflow import analyze_case, init_case, main, reverse_case, validate_case


class CaseWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "original.txt"
        self.source.write_bytes(b"LXFOPV EFRNHR\n")
        self.case = init_case(
            "fixture", ciphertext_file=self.source,
            source_url="https://example.org/published-fixture", root=self.root / "cases",
        )

    def metadata(self):
        return json.loads((self.case / "case.json").read_text())

    def write_metadata(self, metadata):
        (self.case / "case.json").write_text(json.dumps(metadata), encoding="utf-8")

    def prepare_latin(self, cribs=None):
        metadata = self.metadata()
        metadata["alphabet"] = {
            "kind": "latin", "symbols": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "normalization": "ascii_letters",
        }
        metadata["cribs"] = cribs or [{
            "offset": 0, "plaintext": "ATTACK", "status": "confirmed",
            "source_url": "https://example.org/confirmed-crib", "note": "Test fixture only",
        }]
        self.write_metadata(metadata)

    def test_intake_preserves_exact_bytes_hash_provenance_and_unsolved_state(self):
        metadata = validate_case(self.case)
        self.assertEqual((self.case / "source/ciphertext.txt").read_bytes(), self.source.read_bytes())
        self.assertEqual(metadata["source"]["sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(metadata["provenance"]["source_url"], "https://example.org/published-fixture")
        self.assertEqual(metadata["status"], "unsolved")
        self.assertEqual(metadata["stage"], "intake")
        self.assertEqual(metadata["alphabet"]["kind"], "unknown")
        self.assertTrue((self.case / "source/intake.json").is_file())

    def test_traversal_and_case_collisions_do_not_overwrite_source(self):
        for slug in ("../escape", "/absolute", "a/b", "..", "Bad Name", "a\\b"):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                init_case(slug, ciphertext_file=self.source, source_url="https://example.org/a", root=self.root / "cases")
        before = (self.case / "case.json").read_bytes()
        with self.assertRaises(FileExistsError):
            init_case("fixture", ciphertext_file=self.source, source_url="https://example.org/b", root=self.root / "cases")
        self.assertEqual((self.case / "case.json").read_bytes(), before)

    def test_provenance_urls_reject_embedded_whitespace(self):
        with self.assertRaises(ValueError):
            init_case("bad-url", ciphertext_file=self.source,
                      source_url="https://example.org bad/source", root=self.root / "cases")
        metadata = self.metadata()
        metadata["provenance"]["source_url"] = "https://example.org/source\ntrailing"
        self.write_metadata(metadata)
        with self.assertRaises(ValueError):
            validate_case(self.case)

    def test_timestamps_use_extended_utc_syntax_across_python_versions(self):
        original = self.metadata()
        for value in ("2026-10-03 01:00:00Z", "20261003T010000Z", "2026-10-03T01:00:00-04:00"):
            metadata = json.loads(json.dumps(original))
            metadata["provenance"]["accessed_at_utc"] = value
            self.write_metadata(metadata)
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_case(self.case)
        for value in ("2026-10-03T01:00:00Z", "2026-10-03T01:00:00.123456+00:00"):
            original["provenance"]["accessed_at_utc"] = value
            self.write_metadata(original)
            validate_case(self.case)

    def test_source_tamper_and_updated_metadata_hash_still_fail_intake_anchor(self):
        path = self.case / "source/ciphertext.txt"
        path.chmod(0o644)
        path.write_text("TAMPERED", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash"):
            validate_case(self.case)
        metadata = self.metadata()
        metadata["source"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        metadata["source"]["bytes"] = len(path.read_bytes())
        self.write_metadata(metadata)
        with self.assertRaisesRegex(ValueError, "intake"):
            validate_case(self.case)

    def test_malformed_cases_and_source_paths_fail_explicit_checks(self):
        original = self.metadata()
        for replacement in (
            {**original, "status": "solved"},
            {**original, "stage": "published"},
            {**original, "cribs": [{"offset": True, "plaintext": "A", "status": "confirmed", "source_url": "https://example.org/a", "note": ""}]},
            {**original, "source": {**original["source"], "path": "../original.txt"}},
            {**original, "unknown_field": True},
        ):
            self.write_metadata(replacement)
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                validate_case(self.case)
        (self.case / "case.json").write_text("not JSON", encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_case(self.case)

    def test_unicode_analysis_preserves_tokens_without_latin_normalization(self):
        self.source.write_text("\u03b1\u03b2 \u03b2\u03b1\n\u16a0\u16a2", encoding="utf-8")
        case = init_case("unicode", ciphertext_file=self.source, source_url="https://example.org/unread-script", root=self.root / "cases")
        run = analyze_case(case)
        report = json.loads((run / "report.json").read_text())
        self.assertEqual(report["analysis"]["tokens"], ["\u03b1\u03b2", "\u03b2\u03b1", "\u16a0\u16a2"])
        self.assertIsNone(report["analysis"]["normalized_latin"])
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(validate_case(case)["stage"], "analyzed")

    def test_explicit_latin_baseline_reports_period_clues_and_sampling_bounds(self):
        self.prepare_latin()
        run = analyze_case(self.case, max_period=5)
        report = json.loads((run / "report.json").read_text())
        baseline = report["analysis"]["latin_baseline"]
        self.assertEqual(baseline["analyzed_letters"], 12)
        self.assertFalse(baseline["sampled"])
        self.assertAlmostEqual(baseline["index_of_coincidence"], 1 / 33)
        self.assertEqual([row["period"] for row in baseline["column_ic"]], list(range(1, 6)))
        self.assertIn("3", baseline["top_ngrams"])
        self.assertEqual(baseline["max_period"], 5)
        with self.assertRaises(ValueError):
            analyze_case(self.case, max_period=129)
        self.source.write_text("A" * 8200, encoding="utf-8")
        large = init_case("large", ciphertext_file=self.source, source_url="https://example.org/large", root=self.root / "cases")
        metadata = validate_case(large)
        metadata["alphabet"] = self.metadata()["alphabet"]
        (large / "case.json").write_text(json.dumps(metadata), encoding="utf-8")
        run = analyze_case(large, max_period=2)
        baseline = json.loads((run / "report.json").read_text())["analysis"]["latin_baseline"]
        self.assertTrue(baseline["sampled"])
        self.assertEqual(baseline["analyzed_letters"], 8192)
        self.assertEqual(baseline["total_letters"], 8200)

    def test_analysis_manifest_and_snapshots_record_exact_input_integrity(self):
        run = analyze_case(self.case)
        manifest = json.loads((run / "manifest.json").read_text())
        self.assertEqual(manifest["source_sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(manifest["operation"], "analyze")
        self.assertEqual(manifest["execution_status"], "completed")
        self.assertIn("timestamp_utc", manifest)
        self.assertIn("workflow_version", manifest)
        self.assertIn("code_sha256", manifest)
        self.assertIn("git_dirty", manifest)
        self.assertIn("python_version", manifest["runtime_versions"])
        self.assertIn("z3_solver_distribution", manifest["runtime_versions"])
        self.assertEqual((run / "snapshot/ciphertext.txt").read_bytes(), self.source.read_bytes())
        snapshot = (run / "snapshot/case.json").read_bytes()
        self.assertEqual(hashlib.sha256(snapshot).hexdigest(), manifest["case_snapshot_sha256"])
        self.assertEqual(validate_case(self.case)["status"], "unsolved")

    def test_baseline_reverse_uses_confirmed_cribs_only_and_claims_no_solution(self):
        self.prepare_latin([
            {"offset": 0, "plaintext": "ATTACK", "status": "confirmed", "source_url": "https://example.org/confirmed", "note": ""},
            {"offset": 6, "plaintext": "ZZZZZZ", "status": "tentative", "source_url": None, "note": "Hypothesis only"},
        ])
        run = reverse_case(self.case, max_period=5)
        report = json.loads((run / "report.json").read_text())
        manifest = json.loads((run / "manifest.json").read_text())
        self.assertEqual(report["classification"], "candidates")
        self.assertEqual(report["confirmed_crib_count"], 1)
        self.assertEqual(report["tentative_crib_count_excluded"], 1)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertTrue(any(h["key"] == "LEMON" for h in report["result"]["hypotheses"]))
        self.assertEqual(manifest["parameters"]["max_period"], 5)
        self.assertEqual(validate_case(self.case)["stage"], "hypotheses")

    def test_no_confirmed_crib_or_unknown_alphabet_prevents_inference(self):
        with self.assertRaises(ValueError):
            reverse_case(self.case)
        self.prepare_latin([{"offset": 0, "plaintext": "ATTACK", "status": "tentative", "source_url": None, "note": ""}])
        with self.assertRaisesRegex(ValueError, "confirmed"):
            reverse_case(self.case)

    def test_symbolic_unavailable_is_an_incomplete_unexecuted_run(self):
        self.prepare_latin()
        with patch("engine.case_workflow._symbolic_inference", side_effect=ImportError("optional z3 not installed")):
            run = reverse_case(self.case, symbolic=True, timeout_seconds=0.1, max_period=2)
        report = json.loads((run / "report.json").read_text())
        manifest = json.loads((run / "manifest.json").read_text())
        self.assertEqual(report["classification"], "incomplete")
        self.assertFalse(report["executed"])
        self.assertTrue(report["incomplete"])
        self.assertEqual(report["availability"], "unavailable")
        self.assertEqual(manifest["execution_status"], "incomplete")
        self.assertIsNone(report["claimed_plaintext"])

    def test_symbolic_timeout_report_stays_incomplete_without_claimed_plaintext(self):
        self.prepare_latin()
        result = {"hypotheses": [], "incomplete": True, "timed_out": True, "claimed_plaintext": None}
        with patch("engine.case_workflow._symbolic_inference", return_value=result) as infer:
            run = reverse_case(self.case, symbolic=True, timeout_seconds=0.2, max_period=2, max_checks=3)
        report = json.loads((run / "report.json").read_text())
        self.assertEqual(report["classification"], "incomplete")
        self.assertTrue(report["executed"])
        self.assertTrue(report["incomplete"])
        self.assertEqual(infer.call_args.kwargs["timeout_seconds"], 0.2)
        self.assertEqual(infer.call_args.kwargs["max_checks"], 3)

    def test_actual_missing_symbolic_dependency_is_recorded(self):
        from engine.cipher_synthesis import OptionalSynthesisDependencyError
        self.prepare_latin()
        with patch("engine.cipher_synthesis._load_z3", side_effect=OptionalSynthesisDependencyError("missing z3")):
            run = reverse_case(self.case, symbolic=True)
        report = json.loads((run / "report.json").read_text())
        self.assertFalse(report["executed"])
        self.assertEqual(report["availability"], "unavailable")

    def test_symbolic_complete_models_have_correct_classification(self):
        self.prepare_latin()
        for sat_models, expected in ((1, "candidates"), (0, "failed")):
            result = {"search_complete": True, "sat_models": sat_models, "models": []}
            with patch("engine.case_workflow._symbolic_inference", return_value=result):
                run = reverse_case(self.case, symbolic=True)
            self.assertEqual(json.loads((run / "report.json").read_text())["classification"], expected)
        with self.assertRaises(ValueError):
            reverse_case(self.case, symbolic=True, max_checks=100001)

    def test_verification_snapshots_exact_candidate_and_matches_reference_hash(self):
        from engine.case_workflow import verify_case
        candidate = self.root / "candidate.txt"
        candidate.write_bytes(b"ATTACKATDAWN\n")
        metadata = self.metadata()
        metadata["validation"]["expected_plaintext_sha256"] = hashlib.sha256(candidate.read_bytes()).hexdigest()
        metadata["validation"]["known_plaintext_url"] = "https://example.org/independent-plaintext"
        self.write_metadata(metadata)
        run = verify_case(self.case, candidate_file=candidate)
        report = json.loads((run / "report.json").read_text())
        manifest = json.loads((run / "manifest.json").read_text())
        self.assertEqual(report["classification"], "reference-match")
        self.assertEqual((run / "snapshot/plaintext-candidate.txt").read_bytes(), candidate.read_bytes())
        self.assertEqual(manifest["candidate_sha256"], hashlib.sha256(candidate.read_bytes()).hexdigest())
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(validate_case(self.case)["stage"], "validation")
        self.assertEqual(validate_case(self.case)["status"], "unsolved")

    def test_wrong_reference_hash_is_rejected_and_hash_requires_source_url(self):
        from engine.case_workflow import verify_case
        candidate = self.root / "candidate.txt"
        candidate.write_text("WRONG", encoding="utf-8")
        metadata = self.metadata()
        metadata["validation"]["expected_plaintext_sha256"] = hashlib.sha256(b"ATTACKATDAWN").hexdigest()
        self.write_metadata(metadata)
        with self.assertRaisesRegex(ValueError, "reference URL"):
            validate_case(self.case)
        metadata["validation"]["known_plaintext_url"] = "https://example.org/independent"
        self.write_metadata(metadata)
        run = verify_case(self.case, candidate_file=candidate)
        self.assertEqual(json.loads((run / "report.json").read_text())["classification"], "rejected")

    def test_heldout_confirmed_cribs_are_not_fitted_and_verify_separately(self):
        from engine.case_workflow import verify_case
        self.prepare_latin()
        metadata = self.metadata()
        metadata["validation"]["heldout_cribs"] = [
            {"offset": 6, "plaintext": "ATDAWN", "status": "confirmed", "source_url": "https://example.org/heldout", "note": "Held aside"},
            {"offset": 0, "plaintext": "ZZZZZZ", "status": "tentative", "source_url": None, "note": "Not evidence"},
        ]
        self.write_metadata(metadata)
        run = reverse_case(self.case, max_period=5)
        report = json.loads((run / "report.json").read_text())
        self.assertTrue(any(h["key"] == "LEMON" for h in report["result"]["hypotheses"]))
        self.assertEqual(report["result"]["known_positions"], 6)
        candidate = self.root / "candidate.txt"
        candidate.write_text("ATTACK AT DAWN", encoding="utf-8")
        run = verify_case(self.case, candidate_file=candidate)
        report = json.loads((run / "report.json").read_text())
        self.assertEqual(report["classification"], "crib-supported")
        self.assertEqual(report["tentative_heldout_count_excluded"], 1)
        candidate.write_text("ATTACK AT NOON", encoding="utf-8")
        run = verify_case(self.case, candidate_file=candidate)
        self.assertEqual(json.loads((run / "report.json").read_text())["classification"], "rejected")

    def test_tentative_heldout_alone_leaves_candidate_unchecked(self):
        from engine.case_workflow import verify_case
        metadata = self.metadata()
        metadata["validation"]["heldout_cribs"] = [{"offset": 0, "plaintext": "WRONG", "status": "tentative", "source_url": None, "note": ""}]
        self.write_metadata(metadata)
        candidate = self.root / "candidate.txt"
        candidate.write_text("ANYTHING", encoding="utf-8")
        run = verify_case(self.case, candidate_file=candidate)
        self.assertEqual(json.loads((run / "report.json").read_text())["classification"], "unchecked")

    def test_symlinked_source_and_output_directories_are_rejected(self):
        source = self.case / "source/ciphertext.txt"
        source.unlink()
        source.symlink_to(self.source)
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate_case(self.case)
        source.unlink()
        source.write_bytes(self.source.read_bytes())
        external = self.root / "external-runs"
        external.mkdir()
        (self.case / "runs").symlink_to(external)
        with self.assertRaises(ValueError):
            analyze_case(self.case)

    def test_standalone_cli_init_validate_and_analyze(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(["init", "cli-fixture", "--ciphertext-file", str(self.source), "--source-url", "https://example.org/fixture", "--root", str(self.root / "cases")]), 0)
        case = self.root / "cases/cli-fixture"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["validate", str(case)]), 0)
            self.assertEqual(main(["analyze", str(case)]), 0)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["reverse", str(case)]), 2)

    def test_symbolic_only_cli_options_are_not_silently_ignored(self):
        self.prepare_latin()
        for flag, value in (("--timeout", "1"), ("--max-checks", "3"), ("--model", "caesar"),
                            ("--layout", "identity"), ("--columnar-width", "3")):
            with self.subTest(flag=flag), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["reverse", str(self.case), flag, value]), 2)


if __name__ == "__main__":
    unittest.main()
