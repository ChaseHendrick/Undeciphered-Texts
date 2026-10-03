"""Chaotic random search recovers one known Caesar certificate.

The solver is not given the shift. It mutates a Caesar shift or a short
substitution until an English score beats a threshold. This test then
checks the known plaintext.

Random search solved that known Caesar example only. It did not solve
army message Nr. 86, Kryptos K4, or an unknown script.
"""

from __future__ import annotations

import inspect
import json
import unittest
from pathlib import Path

from engine.solvers.chaos_search import (
    CHAOS_SEED,
    ChaosCandidate,
    mutate_candidate,
    solve_chaos_search,
)

CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "caesar_certificate.json"
)


class ChaosSearchScopeTest(unittest.TestCase):
    def test_module_documents_known_example_only(self) -> None:
        import engine.solvers.chaos_search as chaos_mod

        doc = chaos_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("caesar certificate", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("k4", lowered)
        self.assertIn("unknown script", lowered)
        self.assertIn("did not solve", lowered)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class ChaosSearchRecoveryTest(unittest.TestCase):
    def test_recovers_caesar_certificate_without_the_key(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        params = inspect.signature(solve_chaos_search).parameters
        self.assertNotIn("key", params)
        self.assertNotIn("shift", params)
        self.assertNotIn("plaintext", params)

        result = solve_chaos_search(cert["ciphertext"], seed=CHAOS_SEED)
        self.assertEqual(result.plaintext, cert["plaintext"])
        self.assertEqual(result.method, "chaos_search")
        self.assertEqual(result.details["seed"], CHAOS_SEED)
        self.assertEqual(result.details["found_kind"], "caesar")
        self.assertNotEqual(str(cert["keys"]["shift"]), "")
        self.assertEqual(result.key, str(cert["keys"]["shift"]))
        self.assertGreater(result.details["caesar_mutations"], 0)
        self.assertGreater(result.details["short_substitution_mutations"], 0)
        scope = result.details["scope"]
        self.assertIn("known Caesar certificate example only", scope)
        self.assertIn("Nr. 86", scope)
        self.assertIn("K4", scope)
        self.assertIn("unknown script", scope)
        self.assertNotIn("\u2014", scope)
        self.assertNotIn("\u2013", scope)

        again = solve_chaos_search(cert["ciphertext"], seed=CHAOS_SEED)
        self.assertEqual(again.plaintext, result.plaintext)
        self.assertEqual(again.details["trials"], result.details["trials"])
        self.assertEqual(again.key, result.key)

    def test_mutate_emits_both_caesar_and_short_substitution(self) -> None:
        import random

        rng = random.Random(CHAOS_SEED)
        current = ChaosCandidate("caesar", 0, ())
        kinds: set[str] = set()
        for _ in range(40):
            current = mutate_candidate(rng, current)
            kinds.add(current.kind)
            if current.kind == "short_substitution":
                self.assertGreaterEqual(len(current.overrides), 1)
                self.assertLessEqual(len(current.overrides), 3)
                self.assertEqual(len(current.overrides), len(set(pair[0] for pair in current.overrides)))
        self.assertEqual(kinds, {"caesar", "short_substitution"})


if __name__ == "__main__":
    unittest.main()
