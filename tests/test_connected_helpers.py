"""Published newly connected helpers and conditional inference through JSON APIs."""
import hashlib
import json
import unittest
from pathlib import Path
from engine.tool_registry import run_tool

DATA=Path(__file__).resolve().parents[1]/'engine/data'
class ConnectedHelpersTest(unittest.TestCase):
    def test_coordinate_and_row_helpers_match_source_hashes(self):
        for name in ('checkerboard','homophonic'):
            certificate=json.loads((DATA/(name+'_certificate.json')).read_text())
            report=run_tool(name,certificate['ciphertext'],params=certificate['keys'])
            recovered=report['result']['plaintext']
            self.assertEqual(hashlib.sha256(recovered.encode()).hexdigest(),certificate['plaintext_sha256'])

    def test_homophonic_and_interrupted_inference_never_receive_keywords(self):
        certificate=json.loads((DATA/'homophonic_certificate.json').read_text())
        control=certificate['unknown_key_control']
        parameters={name:control[name] for name in ('cribs','max_checks','terminal_period')}
        report=run_tool('homophonic-inference',control['ciphertext'],params=parameters)['result']
        self.assertEqual(report['predicted_plaintext'],certificate['plaintext'])
        self.assertEqual(report['compatible_key_count'],1)
        certificate=json.loads((DATA/'interrupted_key_certificate.json').read_text())
        parameters={**certificate['inference_parameters'],'segment_lengths':certificate['segment_lengths'],'cribs':certificate['cribs']}
        self.assertNotIn('keyword',parameters)
        report=run_tool('interrupted-inference',certificate['ciphertext'],params=parameters)['result']
        self.assertEqual(report['predicted_plaintext'],certificate['plaintext'])
        self.assertTrue(report['search_complete'])
        self.assertIsNone(report['claimed_plaintext'])

if __name__=='__main__':unittest.main()
