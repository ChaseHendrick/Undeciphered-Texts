"""Actual registry, council and case evidence routes, including no-site execution."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from engine.case_workflow import init_case, investigate_case, validate_case
from engine.language import get_model
from engine.persona_solvers import investigate_personas
from engine.reverse_engineer import Crib
from engine.tool_registry import run_tool

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "engine/data"
NAMES = ("emperor", "inheritance", "hallucinogens", "pacifist", "detective",
         "cartographer", "mechanic", "normal-man", "adversary", "skeptic")


def certificate(name):
    return json.loads((DATA / name).read_text())


class PersonaIntegrationTest(unittest.TestCase):
    def test_every_registered_mode_recovers_literal_unknown_key_controls(self):
        emperor = certificate("persona_emperor_solver_certificate.json")["controls"][0]
        inherited = next(v for v in certificate("persona_inheritance_solver_certificate.json")["vectors"]
                         if v["name"].startswith("crib-only"))
        hallucinogens = certificate("persona_hallucinogens_solver_certificate.json")
        pacifist = certificate("persona_pacifist_solver_certificate.json")["vectors"][0]
        detective = certificate("persona_detective_solver_certificate.json")
        cartographer = certificate("persona_cartographer_solver_certificate.json")
        mechanic = certificate("persona_mechanic_solver_certificate.json")["vectors"][0]
        adversary = certificate("persona_adversary_solver_certificate.json")
        skeptic = certificate("persona_skeptic_solver_certificate.json")
        rows = (
            ("emperor", emperor, {}),
            ("inheritance", inherited, {"cribs": inherited["cribs"]}),
            ("hallucinogens", hallucinogens, {"max_rotations": 0}),
            ("pacifist", pacifist, {"cribs": pacifist["cribs"]}),
            ("detective", detective, {"crib": detective["crib"]}),
            ("cartographer", cartographer, {}),
            ("mechanic", mechanic, {"cribs": mechanic["cribs"]}),
            ("normal-man", emperor, {}),
            ("adversary", adversary, {"candidate": adversary["proposed_plaintext"]}),
            ("skeptic", skeptic, {"cribs": skeptic["training_cribs"],
                "verification_cribs": skeptic["verification_cribs"],
                "expected_plaintext_sha256": skeptic["plaintext_sha256"]}),
        )
        for name, vector, params in rows:
            with self.subTest(persona=name):
                self.assertFalse(any(k in params for k in ("key", "keyword", "primer", "matrix", "a", "b")))
                invoked = run_tool(name, vector["ciphertext"], params=params)
                self.assertTrue(invoked["executed"])
                self.assertEqual(invoked["tool"], name)
                report = invoked["result"]
                self.assertTrue(any(sha256(c["plaintext"].encode("ascii")).hexdigest() == vector["plaintext_sha256"]
                                    for c in report["candidates"]))
                self.assertLessEqual(report["checks"], 5000)
                self.assertFalse(report["correctness_known"])
                self.assertIsNone(report["claimed_plaintext"])
                json.dumps(invoked, allow_nan=False)

    def test_actual_ten_mode_council_uses_uniform_scores_without_legacy_bias(self):
        vector = certificate("persona_emperor_solver_certificate.json")["controls"][0]
        plain = vector["expected_plaintext"]
        targets = ("engine.solvers.persona_court_notice.choose", "engine.solvers.persona_inheritance.choose",
                   "engine.solvers.persona_hallucinogens.choose", "engine.solvers.pacifist.pacifist_score")
        patches = [patch(t, side_effect=AssertionError("legacy word bias must not run")) for t in targets]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        report = investigate_personas(vector["ciphertext"], cribs=(Crib(0, plain[:12]),),
            verification_cribs=(Crib(27, "LETTERBESIDE"),), expected_plaintext_sha256=vector["plaintext_sha256"],
            personas=NAMES, max_checks=9000, max_candidates=5)
        self.assertEqual(report["selected_personas"], list(NAMES))
        self.assertEqual(set(report["persona_reports"]), set(NAMES))
        self.assertEqual(report["checks"], sum(r["checks"] for r in report["persona_reports"].values()))
        self.assertLessEqual(report["checks"], 9000)
        self.assertTrue(any(c["plaintext"] == plain for c in report["candidates"]))
        for candidate in report["candidates"]:
            expected = get_model().score([ord(ch) - 65 for ch in candidate["plaintext"]])
            self.assertEqual(candidate["score"], expected)
            self.assertEqual(candidate["skeptic_review"]["status"], "exact-reference-match")
            self.assertTrue(candidate["supporting_personas"])
        critic = report["persona_reports"]["skeptic"]
        self.assertFalse(critic["search_executed"])
        self.assertEqual(critic["checks"], len(critic["reviews"]))
        self.assertFalse(report["agreement_is_independent_evidence"])
        self.assertFalse(report["correctness_known"])

    def test_actual_council_respects_one_global_budget_including_critic(self):
        vector = certificate("persona_emperor_solver_certificate.json")["controls"][0]
        for limit in (0, 1, 10, 32, 100, 1500):
            with self.subTest(max_checks=limit):
                report = investigate_personas(vector["ciphertext"], cribs=(Crib(0, "THELIBRARIAN"),),
                    personas=NAMES, max_checks=limit, max_candidates=2)
                self.assertEqual(report["checks"], sum(r["checks"] for r in report["persona_reports"].values()))
                self.assertEqual(report["checks"], sum(a["executed_checks"] for a in report["actions"]))
                self.assertLessEqual(report["checks"], limit)
                for a in report["actions"]:
                    self.assertLessEqual(a["executed_checks"], a["allocated_checks"])
                self.assertFalse(report["correctness_known"])

    def test_actual_rejected_shortlist_cannot_backfill_unreviewed_lower_witness(self):
        vector = certificate("persona_emperor_solver_certificate.json")["controls"][0]
        report = investigate_personas(vector["ciphertext"], personas=("normal-man", "pacifist", "skeptic"),
            expected_plaintext_sha256="0" * 64, max_candidates=1, max_checks=1000)
        self.assertTrue(report["contradicted_candidates"])
        self.assertEqual(report["candidates"], [])
        self.assertEqual(len(report["persona_reports"]["skeptic"]["reviews"]), 1)

    def test_selected_mode_is_lazy_and_reserved_evidence_requires_critic(self):
        with patch.dict("sys.modules", {"engine.solvers.persona_adversary": None,
                                       "engine.solvers.persona_skeptic": None}):
            report = investigate_personas("ABCD", personas=("normal-man",), max_checks=0)
        self.assertEqual(report["selected_personas"], ["normal-man"])
        self.assertEqual(report["checks"], 0)
        with self.assertRaisesRegex(ValueError, "Skeptic"):
            investigate_personas("ABCD", personas=("normal-man",), verification_cribs=(Crib(0, "A"),))

    def test_registry_keeps_modern_binary_helper_separate_from_persona_search(self):
        vector = certificate("aes_certificate.json")
        result = run_tool("aes", vector["ciphertext_hex"], params={"key": vector["key_hex"]})
        self.assertEqual(result["mode"], "supplied-key")
        raw = bytes.fromhex(result["result"]["plaintext"])
        self.assertEqual(sha256(raw).hexdigest(), vector["plaintext_sha256"])
        self.assertNotIn("persona", result["result"])

    def test_real_case_council_routes_only_confirmed_training_clues(self):
        vector = certificate("persona_emperor_solver_certificate.json")["controls"][0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "cipher.txt"
            source.write_text(vector["ciphertext"])
            case_dir = init_case("council-control", ciphertext_file=source,
                source_url="https://example.org/constructed-test", root=root / "cases")
            case = validate_case(case_dir)
            case["alphabet"] = {"kind": "latin", "normalization": "ascii_letters", "symbols": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
            case["cribs"] = [dict(offset=0, plaintext="THELIBRARIAN", status="confirmed", source_url="https://example.org/constructed-test", note=""),
                dict(offset=27, plaintext="XXXXXXXXXXXX", status="tentative", source_url=None, note="untrusted guess")]
            case["validation"].update(known_plaintext_url="https://example.org/constructed-test",
                expected_plaintext_sha256=vector["plaintext_sha256"],
                heldout_cribs=[dict(offset=27, plaintext="LETTERBESIDE", status="confirmed",
                    source_url="https://example.org/constructed-test", note="reserved")])
            (case_dir / "case.json").write_text(json.dumps(case))
            with patch("engine.persona_solvers.investigate_personas", wraps=investigate_personas) as council:
                run = investigate_case(case_dir, solver_profile="council", max_checks=3000, max_candidates=3)
            self.assertEqual(council.call_args.kwargs["cribs"], [Crib(0, "THELIBRARIAN")])
            self.assertNotIn("verification_cribs", council.call_args.kwargs)
            self.assertNotIn("expected_plaintext_sha256", council.call_args.kwargs)
            report = json.loads((run / "report.json").read_text())
            manifest = json.loads((run / "manifest.json").read_text())
            self.assertEqual(report["tentative_crib_count_excluded"], 1)
            self.assertEqual(report["heldout_crib_count_not_fitted"], 1)
            self.assertTrue(any(c["plaintext"] == vector["expected_plaintext"] for c in report["result"]["candidates"]))
            self.assertTrue(all(r["status"] == "unchecked" for r in report["result"]["persona_reports"]["skeptic"]["reviews"]))
            self.assertEqual(manifest["report_sha256"], sha256((run / "report.json").read_bytes()).hexdigest())
            self.assertIn("engine/persona_solvers.py", manifest["code_sha256"])
            self.assertEqual(validate_case(case_dir)["status"], "unsolved")

    def test_actual_python_no_site_mode_recovers_without_optional_dependencies(self):
        vector = certificate("persona_emperor_solver_certificate.json")["controls"][0]
        code = """import json,sys
from engine.persona_solvers import investigate_personas
from engine.reverse_engineer import Crib
payload=json.loads(sys.stdin.read())
report=investigate_personas(payload['ciphertext'],cribs=(Crib(0,'THELIBRARIAN'),),max_checks=3000,max_candidates=3)
assert 'numpy' not in sys.modules and 'z3' not in sys.modules
print(json.dumps({'checks':report['checks'],'names':report['selected_personas'],'neural':report['neural_advice']['status'],'plain':any(c['plaintext']==payload['expected_plaintext'] for c in report['candidates'])}))
"""
        result = subprocess.run([sys.executable, "-S", "-c", code], cwd=ROOT,
            input=json.dumps(vector), text=True, capture_output=True, timeout=30, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report["names"], list(NAMES))
        self.assertEqual(report["neural"], "unavailable")
        self.assertTrue(report["plain"])
        self.assertLessEqual(report["checks"], 3000)


if __name__ == "__main__":
    unittest.main()
