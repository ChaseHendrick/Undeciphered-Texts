"""Investigation integration excludes validation evidence and preserves model bytes."""
from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.case_workflow import init_case, investigate_case, validate_case

class CaseInvestigationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / 'input.txt'
        source.write_text('LXFOPVEFRNHR', encoding='utf-8')
        self.case = init_case('sample', ciphertext_file=source,
            source_url='https://example.org/fixture', root=self.root / 'cases')

    def prepare(self):
        case = validate_case(self.case)
        case['alphabet'] = {'kind':'latin','normalization':'ascii_letters','symbols':list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
        case['cribs'] = [dict(offset=0,plaintext='ATTACK',status='confirmed',source_url='https://example.org/crib',note=''),
            dict(offset=6,plaintext='ZZZZZZ',status='tentative',source_url=None,note='guess')]
        case['validation']['heldout_cribs'] = [dict(offset=6,plaintext='ATDAWN',status='confirmed',source_url='https://example.org/heldout',note='')]
        (self.case / 'case.json').write_text(json.dumps(case))

    def test_unknown_alphabet_is_rejected_before_investigation(self):
        with self.assertRaisesRegex(ValueError, 'Latin'):
            investigate_case(self.case, max_checks=100)
        self.assertFalse((self.case / 'runs').exists())

    def test_confirmed_only_bounded_investigation_preserves_unverified_status(self):
        self.prepare()
        run = investigate_case(self.case, max_checks=400, max_candidates=4)
        report = json.loads((run/'report.json').read_text())
        manifest = json.loads((run/'manifest.json').read_text())
        self.assertEqual(report['confirmed_crib_count'],1)
        self.assertEqual(report['tentative_crib_count_excluded'],1)
        self.assertEqual(report['heldout_crib_count_not_fitted'],1)
        self.assertIsNone(report['claimed_plaintext'])
        self.assertEqual(report['verification_status'],'unverified')
        self.assertLessEqual(report['result']['checks'],400)
        self.assertEqual(manifest['report_sha256'],hashlib.sha256((run/'report.json').read_bytes()).hexdigest())
        self.assertIn('engine/solver_reasoning.py',manifest['code_sha256'])
        self.assertIn('engine/solvers/redefence.py',manifest['code_sha256'])
        self.assertEqual(validate_case(self.case)['status'],'unsolved')
        self.assertEqual(validate_case(self.case)['stage'],'hypotheses')

    def test_exact_router_artifact_is_snapshotted_when_used(self):
        self.prepare()
        source = self.root / 'model.json'
        model_bytes = b'{"fixture":true}\n'
        source.write_bytes(model_bytes)
        model_hash = hashlib.sha256(model_bytes).hexdigest()
        class Report:
            def to_dict(self):
                return dict(candidates=[],checks=0,search_complete=False,
                    neural_advice={'model_sha256':model_hash},claimed_plaintext=None)
        with patch('engine.solver_reasoning.investigate_cipher',return_value=Report()) as investigate, \
             patch('engine.case_workflow._REPO',self.root):
            target = self.root / 'engine/data/neural_router_v2_weights.json'
            target.parent.mkdir(parents=True)
            target.write_bytes(model_bytes)
            run = investigate_case(self.case, max_checks=40)
        passed = investigate.call_args.kwargs['cribs']
        self.assertEqual([(c.offset,c.plaintext) for c in passed],[(0,'ATTACK')])
        self.assertNotIn('expected_plaintext_sha256',investigate.call_args.kwargs)
        manifest = json.loads((run/'manifest.json').read_text())
        self.assertEqual(manifest['model_snapshot_sha256'],model_hash)
        self.assertEqual((run/'snapshot/router_weights.json').read_bytes(),model_bytes)

    def test_council_profile_receives_only_training_evidence(self):
        self.prepare()
        outcome=dict(candidates=[],checks=0,search_complete=False,
                     claimed_plaintext=None,neural_advice={'status':'not_used'})
        with patch('engine.persona_solvers.investigate_personas',return_value=outcome) as investigate:
            run=investigate_case(self.case,solver_profile='council',max_checks=40)
        kwargs=investigate.call_args.kwargs
        self.assertEqual([(c.offset,c.plaintext) for c in kwargs['cribs']],[(0,'ATTACK')])
        self.assertNotIn('verification_cribs',kwargs)
        self.assertNotIn('expected_plaintext_sha256',kwargs)
        manifest=json.loads((run/'manifest.json').read_text())
        self.assertEqual(manifest['parameters']['solver_profile'],'council')
        self.assertEqual(validate_case(self.case)['status'],'unsolved')

if __name__ == '__main__':
    unittest.main()
