"""The new attacks remain accessible through the same bounded CLI gateway."""
import contextlib
import hashlib
import io
import json
import unittest

from engine.cli import main
from engine.tool_registry import list_tools, run_tool


class DorabellaToolsTest(unittest.TestCase):
    def test_both_search_contracts_are_discoverable(self):
        catalog = {entry['name']: entry for entry in list_tools()}
        self.assertEqual(catalog['substitution-tempering']['mode'], 'score-ranked-search')
        self.assertIn('max_proposals', catalog['substitution-tempering']['optional_parameters'])
        self.assertEqual(catalog['unspaced-substitution']['mode'], 'lexicon-constrained-unspaced-search')
        self.assertIn('lexicon', catalog['unspaced-substitution']['required_parameters'])

    def test_unspaced_cli_recovers_a_literal_hidden_key_control(self):
        # Independently encoded with QWERTYUIOPASDFGHJKLZXCVBNM. This key
        # is absent from CLI inputs; word breaks must also be recovered.
        output = io.StringIO()
        params = {'lexicon': ['MEET', 'AT', 'THE', 'GATE'], 'max_nodes': 10000}
        with contextlib.redirect_stdout(output):
            code = main(['run', 'unspaced-substitution', 'DTTZQZZITUQZT',
                         '--params', json.dumps(params)])
        self.assertEqual(code, 0)
        report = json.loads(output.getvalue())['result']
        candidates = report['candidates']
        recovered = next(c for c in candidates if c['plaintext_letters'] == 'MEETATTHEGATE')
        self.assertEqual(recovered['plaintext'], 'MEET AT THE GATE')
        self.assertEqual(hashlib.sha256(recovered['plaintext_letters'].encode('ascii')).hexdigest(),
                         hashlib.sha256(b'MEETATTHEGATE').hexdigest())
        self.assertIsNone(report['claimed_plaintext'])

    def test_tempering_dispatch_preserves_work_cap_and_forward_mapping(self):
        cipher = 'CEIQDVKAIKXNPQIGCEIXPKQINHIRAGICEIMPCIPFGTPACIGVFGIKCEIXDKQEVFCANCEIEIPSWKPAFEPGRCDXXIG'
        result = run_tool('substitution-tempering', cipher, params={'max_proposals': 17})['result']
        self.assertEqual(result['details']['proposals'], 17)
        encoded = ''.join(result['key'][ord(ch) - 65] for ch in result['plaintext'])
        self.assertEqual(encoded, cipher)
        self.assertFalse(result['details']['exhaustive_key_search'])
        self.assertIsNone(result['details']['claimed_plaintext'])


if __name__ == '__main__':
    unittest.main()
