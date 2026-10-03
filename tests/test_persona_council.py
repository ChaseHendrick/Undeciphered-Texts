"""Complementary strategies share work and preserve unverified evidence."""
import unittest
from unittest.mock import patch


class PersonaCouncilTest(unittest.TestCase):
    def test_candidates_with_incompatible_backend_score_units_get_one_shared_score(self):
        from engine.persona_solvers import investigate_personas
        from engine.persona_solver_common import make_report
        good = "THELIBRARIANPLACEDTHESEALEDLETTERBESIDETHEMAPANDWAITEDFORTHENIGHTTRAIN"
        bad = "XZQ" * 22
        def runner(name, plaintext, score):
            def run(text, **kwargs):
                candidate = dict(plaintext=plaintext, family="test", key={}, score=score,
                    forward_consistent=True, crib_match=True, evidence={})
                return make_report(name,name,[candidate],0,kwargs['max_checks'],True,"complete",[],[])
            return run
        modes = dict(emperor=runner("emperor",good,-1000.),
                     inheritance=runner("inheritance",bad,-1.),
                     hallucinogens=runner("hallucinogens",good,-1000.))
        with patch("engine.persona_solvers._strategies", return_value=modes):
            report = investigate_personas("ABCD",max_checks=0,max_candidates=1,
                                          personas=("emperor","inheritance","hallucinogens"))
        self.assertEqual(report['candidates'][0]['plaintext'],good)

    def test_unused_work_is_reallocated_and_agreement_is_not_verification(self):
        from engine.persona_solvers import investigate_personas
        from engine.persona_solver_common import make_report
        observed = []
        def runner(name, spend):
            def run(text, **kwargs):
                observed.append((name, kwargs["max_checks"]))
                candidate = {"plaintext": "ABCD", "family": "affine", "key": {"a": 1},
                             "score": -1., "forward_consistent": True,
                             "crib_match": True, "evidence": {"independent_correctness": False}}
                return make_report(name, name, [candidate] if spend else [],
                                   spend, kwargs["max_checks"], True, "complete", [], [])
            return run
        strategies = {"emperor": runner("emperor", 2),
                      "inheritance": runner("inheritance", 0),
                      "hallucinogens": runner("hallucinogens", 7)}
        with patch("engine.persona_solvers._strategies", return_value=strategies):
            report = investigate_personas("ABCD", max_checks=9,
                                          personas=("emperor","inheritance","hallucinogens"))
        self.assertEqual(observed, [("emperor", 3), ("inheritance", 4), ("hallucinogens", 7)])
        self.assertEqual(report["checks"], 9)
        self.assertEqual(len(report["candidates"]), 1)
        self.assertEqual(report["candidates"][0]["supporting_personas"], ["emperor", "hallucinogens"])
        self.assertFalse(report["correctness_known"])
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["agreement_is_independent_evidence"])

    def test_bad_backend_report_cannot_consume_unbounded_work_or_claim_verified_agreement(self):
        from engine.persona_solvers import investigate_personas
        bad = lambda text, **kwargs: {"checks": kwargs["max_checks"] + 1, "candidates": []}
        with patch("engine.persona_solvers._strategies", return_value={"emperor": bad}):
            with self.assertRaises(RuntimeError):
                investigate_personas("ABCD", max_checks=3,personas=("emperor",))


if __name__ == "__main__":
    unittest.main()
