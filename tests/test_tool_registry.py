"""One explicit invocation registry connects helpers and bounded searches."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.tool_registry import list_tools, run_tool


class ToolRegistryTest(unittest.TestCase):
    def test_modes_required_parameters_and_metadata(self):
        catalog = {item["name"]: item for item in list_tools()}
        self.assertEqual(catalog["condi"]["mode"], "supplied-key")
        self.assertIn("initial_offset", catalog["condi"]["required_parameters"])
        self.assertEqual(catalog["rsa-wiener"]["mode"], "public-parameter-attack")
        self.assertEqual(catalog["progressive-inference"]["mode"], "crib-constrained")
        self.assertIn("plaintext", catalog["caesar"]["output_fields"])
        self.assertIn("quagmire-iv", catalog)

    def test_dispatch_recovers_independent_published_examples(self):
        data = Path(__file__).resolve().parents[1] / "engine/data"
        for name, params in (("condi", {"keyword":"STRANGE", "initial_offset":25, "alphabet_shift":21}),
                             ("morbit", {"key":"WISECRACK", "terminal_period":True}),
                             ("quagmire-i", None)):
            cert = json.loads((data / (name.replace("-", "_") + "_certificate.json")).read_text())
            if name == "quagmire-i":
                params = {key: cert["keys"][key] for key in ("plaintext_keyword", "indicator", "indicator_under")}
            report = run_tool(name, cert["ciphertext"], params=params)
            self.assertEqual(report["result"]["plaintext"], cert["plaintext"])
            self.assertEqual(report["tool"], name)
            self.assertTrue(report["executed"])

    def test_binary_and_public_integer_adapters(self):
        result = run_tool("rsa-wiener", 1511, params={"modulus":8927, "exponent":2621})
        self.assertEqual(result["result"]["plaintext"], "41")
        result = run_tool("aes", "69c4e0d86a7b0430d8cdb78070b4c55a", params={"key":"000102030405060708090a0b0c0d0e0f"})
        self.assertEqual(result["result"]["plaintext"], "00112233445566778899aabbccddeeff")

    def test_json_cribs_become_typed_constraints(self):
        result = run_tool("progressive-inference", "LXFOPVEFRNHR", params={"cribs":[{"offset":0,"plaintext":"ATTACK"}], "max_period":5, "progressions":[0]})
        self.assertIsNone(result["result"]["claimed_plaintext"])
        self.assertTrue(any(candidate["period"] == 5 for candidate in result["result"]["candidates"]))

    def test_morse_report_preserves_derived_uniqueness_fields(self):
        report = run_tool("morse-constraints", "0", params={
            "families": ["pollux"], "lexicon": ["E"],
            "max_maps": 60000, "timeout_seconds": 60,
        })["result"]
        self.assertTrue(report["search_complete"])
        self.assertTrue(report["unique_plaintext_within_models"])
        self.assertFalse(report["unique_map_within_models"])
        self.assertEqual(report["accepted_map_count"], 18660)

    def test_monome_dinome_accepts_json_merge_pair(self):
        # Q, X, Y, Z become Q, X, Y, Q under Q/Z merging. The independent
        # NOTARIES box places those letters at 39, 35, 34, 39.
        report = run_tool("monome-dinome", "39353439", params={
            "key": "NOTARIES", "digit_order": "6318927054",
            "merge": ["Q", "Z"],
        })
        self.assertEqual(report["result"]["plaintext"], "QXYQ")

    def test_common_modulus_attack_is_registered_and_preserves_byte_length(self):
        catalog = {item["name"]: item for item in list_tools()}
        self.assertEqual(catalog["rsa-common-modulus"]["mode"], "public-parameter-attack")
        self.assertEqual(catalog["rsa-common-modulus"]["input_encoding"], "integer")
        report = run_tool("rsa-common-modulus", 124926563412530274107408452482445848228,
                          params={"c2": 214229972888188659887672188139473134959,
                                  "e1": 17, "e2": 65537,
                                  "n": 340282366920938460843936948965011886881,
                                  "byte_length": 16})
        self.assertEqual(report["result"]["plaintext"], "0000434f4d4d4f4e204d4f44554c5553")

    def test_portfolio_adapter_keeps_bounds_and_never_claims_plaintext(self):
        report = run_tool("transposition-ensemble", "IIWRILCPECLFDHVAEIR",
                          params={"cribs":[{"offset":0,"plaintext":"CIVIL"}], "max_checks":5000})
        self.assertIsNone(report["result"]["claimed_plaintext"])
        self.assertTrue(any(candidate["plaintext"] == "CIVILWARFIELDCIPHER" for candidate in report["result"]["candidates"]))

    def test_invalid_calls_are_rejected_before_execution(self):
        for name, value, params in (("os.system", "x", {}), ("condi", "ABC", {}),
                                   ("caesar", "ABC", {"unknown":1}), ("aes", "zz", {"key":"00"}),
                                   ("rsa-wiener", True, {"modulus":8927,"exponent":2621}),
                                   ("caesar", "A" * 8193, {}), ("substitution", "ABCDE", {"steps":50001}),
                                   ("progressive-inference", "ABCDE", {"cribs":[{"offset":True,"plaintext":"A"}]})):
            with self.subTest(name=name), self.assertRaises((TypeError, ValueError)):
                run_tool(name, value, params=params)


if __name__ == "__main__":
    unittest.main()
