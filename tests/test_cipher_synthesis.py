"""Exact bounded constraint synthesis and conditional plaintext consensus."""

from __future__ import annotations

import hashlib
import importlib.util
import contextlib
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.cipher_synthesis import OptionalSynthesisDependencyError, synthesize_cipher_models
from engine.reverse_engineer import Crib


_HAS_Z3 = importlib.util.find_spec("z3") is not None
_CERT_PATH = Path(__file__).resolve().parents[1] / "engine/data/cipher_synthesis_certificate.json"


class CipherSynthesisValidationTest(unittest.TestCase):
    def test_optional_dependency_has_a_clear_setup_error(self) -> None:
        with patch("engine.cipher_synthesis._load_z3", side_effect=OptionalSynthesisDependencyError("Install requirements-synthesis.txt")):
            with self.assertRaisesRegex(OptionalSynthesisDependencyError, "requirements-synthesis"):
                synthesize_cipher_models("ABC", cribs=[Crib(0, "A")])

    def test_cli_missing_optional_dependency_returns_setup_error_status(self) -> None:
        from engine.cli import main

        errors = io.StringIO()
        with patch("engine.cipher_synthesis._load_z3", side_effect=OptionalSynthesisDependencyError("Install requirements-synthesis.txt")):
            with contextlib.redirect_stderr(errors):
                status = main(["reverse-engineer", "ABC", "--crib", "0:A", "--symbolic"])
        self.assertEqual(status, 2)
        self.assertIn("requirements-synthesis.txt", errors.getvalue())

    def test_explicit_symbolic_only_flags_require_symbolic_even_at_defaults(self) -> None:
        from engine.cli import main

        for flags in (
            ("--model", "affine"), ("--layout", "reverse"), ("--columnar-width", "4"),
            ("--timeout-seconds", "5"), ("--max-checks", "10000"),
        ):
            with self.subTest(flags=flags):
                errors = io.StringIO()
                with contextlib.redirect_stderr(errors):
                    status = main(["reverse-engineer", "ABC", "--crib", "0:A", *flags])
                self.assertEqual(status, 2)
                self.assertIn("require --symbolic", errors.getvalue())

    def test_input_and_search_bounds_are_checked_before_loading_z3(self) -> None:
        for overrides in (
            {"max_period": 0}, {"max_period": 129}, {"max_period": True},
            {"timeout_seconds": 0}, {"timeout_seconds": 61}, {"timeout_seconds": float("nan")},
            {"max_checks": 0}, {"max_checks": True}, {"models": ("unknown",)},
            {"models": "affine"}, {"layouts": ("unknown",)}, {"columnar_widths": (1,)},
        ):
            with self.subTest(overrides=overrides):
                with self.assertRaises((ValueError, TypeError)):
                    synthesize_cipher_models("ABC", cribs=[Crib(0, "A")], **overrides)
        for ciphertext, cribs in (
            ("ABC", []), ("ABC", [Crib(-1, "A")]), ("ABC", [Crib(3, "A")]),
            ("caf\u00e9", [Crib(0, "A")]), ("ABC", [Crib(0, "A"), Crib(0, "B")]),
            ("A" * 513, [Crib(0, "A")]),
        ):
            with self.subTest(ciphertext=ciphertext[:10], cribs=cribs):
                with self.assertRaises((ValueError, TypeError)):
                    synthesize_cipher_models(ciphertext, cribs=cribs)


@unittest.skipUnless(_HAS_Z3, "optional z3-solver is not installed")
class CipherSynthesisExactModelTest(unittest.TestCase):
    def test_symbolic_cli_emits_successful_json_and_conditional_heldout_letters(self) -> None:
        from engine.cli import main

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main([
                "reverse-engineer", "GUEXZIZICPZCPVOIXZIGSIZZI", "--crib", "0:ATTACK",
                "--symbolic", "--model", "affine", "--layout", "reverse", "--max-period", "1",
            ])
        self.assertEqual(status, 0)
        report = json.loads(output.getvalue())
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["consensus_plaintext"], "ATTACKATDAWNRETREATATDUSK")
        self.assertIsNone(report["claimed_plaintext"])

    def test_affine_after_reverse_layout_predicts_unseen_plaintext(self) -> None:
        # Independent algebra: ciphertext = 5 * reversed plaintext + 8 mod 26.
        plain = "ATTACKATDAWNRETREATATDUSK"
        cipher = "GUEXZIZICPZCPVOIXZIGSIZZI"
        report = synthesize_cipher_models(
            cipher, cribs=[Crib(0, "ATTACK")], models=("affine",),
            max_period=1, layouts=("identity", "reverse"), timeout_seconds=10,
        )
        self.assertTrue(report.search_complete)
        self.assertEqual(report.consensus_plaintext, plain)
        self.assertIsNone(report.claimed_plaintext)
        self.assertEqual(report.known_positions, 6)
        reverse = next(row for row in report.models if row.layout == "reverse")
        identity = next(row for row in report.models if row.layout == "identity")
        self.assertEqual(identity.status, "unsat")
        self.assertEqual(reverse.status, "sat")
        self.assertEqual(reverse.example_parameters, {"multiplier": 5, "offset": 8})
        self.assertTrue(reverse.parameters_are_example)
        self.assertEqual(reverse.forced_plaintext, plain)

    def test_vigenere_after_reverse_uses_permuted_stream_period_positions(self) -> None:
        plain = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        cipher = "RSPMMLPQVGCIHCFAQGXKZJZKBCFWQVFUQVG"
        report = synthesize_cipher_models(
            cipher, cribs=[Crib(0, "THEQUICKBR")], models=("vigenere",),
            max_period=5, layouts=("reverse",), timeout_seconds=10,
        )
        self.assertTrue(report.search_complete)
        self.assertEqual(report.consensus_plaintext, plain)
        hit = next(row for row in report.models if row.period == 5)
        self.assertEqual(hit.status, "sat")
        self.assertEqual(hit.example_parameters["key"], "LEMON")
        self.assertTrue(all(row.status == "unsat" for row in report.models if row.period != 5))

    def test_known_width_columnar_is_a_layout_stage_before_letter_cipher(self) -> None:
        plain = "ATTACKATDAWNRETREATATDUSK"
        width = 4
        order = [i for column in range(width) for i in range(column, len(plain), width)]
        # Independent row-fill and column-takeoff, followed by affine substitution.
        cipher = "".join(chr(65 + (7 * (ord(plain[i]) - 65) + 3) % 26) for i in order)
        report = synthesize_cipher_models(
            cipher, cribs=[Crib(0, "ATTACKAT")], models=("affine",),
            max_period=1, layouts=(), columnar_widths=(width,), timeout_seconds=10,
        )
        self.assertTrue(report.search_complete)
        self.assertEqual(report.consensus_plaintext, plain)
        self.assertEqual(report.models[0].layout, "columnar:4")

    def test_sparse_unknown_quagmire_alphabets_remain_underdetermined(self) -> None:
        for family in ("quagmire-i", "quagmire-ii", "quagmire-iii"):
            with self.subTest(family=family):
                report = synthesize_cipher_models(
                    "BCDB", cribs=[Crib(0, "A")], models=(family,),
                    max_period=1, layouts=("identity",), timeout_seconds=10,
                )
                row = report.models[0]
                self.assertEqual(row.status, "sat")
                self.assertEqual(row.forced_plaintext, "A??A")
                self.assertEqual(len(set(row.example_parameters["plaintext_alphabet"])), 26)
                self.assertEqual(len(set(row.example_parameters["ciphertext_alphabet"])), 26)
                self.assertTrue(row.parameters_are_example)
                self.assertIsNone(report.claimed_plaintext)

    def test_incompatible_constraints_are_explicitly_unsatisfiable(self) -> None:
        report = synthesize_cipher_models(
            "BC", cribs=[Crib(0, "AA")], models=("affine", "substitution", "vigenere", "beaufort"),
            max_period=1, layouts=("identity",), timeout_seconds=10,
        )
        self.assertTrue(report.search_complete)
        self.assertEqual(report.unsat_models, 4)
        self.assertEqual(report.sat_models, 0)
        self.assertEqual(report.consensus_plaintext, "AA")
        self.assertIsNone(report.claimed_plaintext)

    def test_substitution_keeps_unknown_letters_and_beaufort_predicts_heldout_suffix(self) -> None:
        substitution = synthesize_cipher_models(
            "QWERQZ", cribs=[Crib(0, "ABCD")], models=("substitution",),
            layouts=("identity",), timeout_seconds=10,
        )
        self.assertTrue(substitution.search_complete)
        self.assertEqual(substitution.consensus_plaintext, "ABCDA?")
        beaufort = synthesize_cipher_models(
            "PAMOPGWSODEKKT", cribs=[Crib(0, "CEQUALSKMI")], models=("beaufort",),
            max_period=10, layouts=("identity",), timeout_seconds=10,
        )
        self.assertTrue(beaufort.search_complete)
        self.assertEqual(beaufort.consensus_plaintext, "CEQUALSKMINUSP")

    def test_injected_solver_unknown_is_not_reported_as_no_model(self) -> None:
        with patch("engine.cipher_synthesis._check_solver", return_value=("unknown", "injected timeout")):
            report = synthesize_cipher_models(
                "GUEXZIZICPZCPVOIXZIGSIZZI", cribs=[Crib(0, "ATTACK")],
                models=("affine",), max_period=1, timeout_seconds=10,
            )
        self.assertFalse(report.search_complete)
        self.assertEqual(report.unknown_models, 2)
        self.assertEqual(report.unsat_models, 0)
        self.assertEqual(report.consensus_plaintext, "ATTACK" + "?" * 19)
        self.assertTrue(all(row.reason == "injected timeout" for row in report.models))

    def test_exact_check_budget_keeps_model_and_consensus_state_separate(self) -> None:
        report = synthesize_cipher_models(
            "GUEXZIZICPZCPVOIXZIGSIZZI", cribs=[Crib(0, "ATTACK")],
            models=("affine",), max_period=1, layouts=("reverse",),
            timeout_seconds=10, max_checks=1,
        )
        self.assertEqual(report.solver_checks, 1)
        self.assertEqual(report.models[0].status, "sat")
        self.assertFalse(report.models[0].consensus_complete)
        self.assertFalse(report.search_complete)
        self.assertEqual(report.consensus_plaintext, "ATTACK" + "?" * 19)

    def test_an_unknown_consensus_query_reason_survives_later_successful_checks(self) -> None:
        calls = 0

        def one_unknown(solver, budget):
            nonlocal calls
            calls += 1
            return ("unknown", "injected timeout") if calls == 2 else budget.check(solver)

        with patch("engine.cipher_synthesis._check_solver", side_effect=one_unknown):
            report = synthesize_cipher_models(
                "GUEXZIZICPZCPVOIXZIGSIZZI", cribs=[Crib(0, "ATTACK")],
                models=("affine",), layouts=("reverse",), timeout_seconds=10,
            )
        self.assertEqual(report.models[0].status, "sat")
        self.assertEqual(report.models[0].unknown_queries, 1)
        self.assertIn("injected timeout", report.models[0].reason)
        self.assertFalse(report.search_complete)
        self.assertEqual(report.consensus_plaintext, "ATTACK" + "?" * 19)

    def test_global_deadline_exhaustion_leaves_models_unknown(self) -> None:
        # Time expires between the initial timestamp and model construction.
        with patch("engine.cipher_synthesis.monotonic", side_effect=[0.0] + [2.0] * 20):
            report = synthesize_cipher_models(
                "ABC", cribs=[Crib(0, "A")], models=("affine",),
                max_period=1, timeout_seconds=1,
            )
        self.assertEqual(report.solver_checks, 0)
        self.assertEqual(report.unknown_models, 2)
        self.assertFalse(report.search_complete)
        self.assertEqual(report.consensus_plaintext, "A??")

    def test_certificate_hashes_conditional_recovery_beyond_supplied_crib(self) -> None:
        cert = json.loads(_CERT_PATH.read_text(encoding="utf-8"))
        report = synthesize_cipher_models(
            cert["ciphertext"], cribs=[Crib(**row) for row in cert["cribs"]],
            models=cert["models"], max_period=cert["max_period"],
            layouts=cert["layouts"], timeout_seconds=10,
        )
        self.assertTrue(report.search_complete)
        self.assertEqual(report.consensus_plaintext, cert["plaintext"])
        self.assertEqual(hashlib.sha256(report.consensus_plaintext.encode("ascii")).hexdigest(), cert["plaintext_sha256"])
        self.assertLess(report.known_positions, report.ciphertext_length)
        self.assertEqual(cert["instance"], "synthetic")
        self.assertNotIn("cipher_name", cert)
        self.assertIsNone(report.claimed_plaintext)


if __name__ == "__main__":
    unittest.main()
