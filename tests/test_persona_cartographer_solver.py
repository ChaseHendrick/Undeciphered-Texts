"""Layout-focused search reuses bounded transforms without a supplied key."""
import hashlib
import json
from pathlib import Path
import unittest
from engine.reverse_engineer import Crib


class CartographerTest(unittest.TestCase):
    def test_published_k3_is_recovered_under_declared_widths_with_no_supplied_key(self):
        from engine.solvers.persona_cartographer import investigate_cartographer
        from engine.solvers.columnar import KRYPTOS_K3_CIPHERTEXT
        report = investigate_cartographer(KRYPTOS_K3_CIPHERTEXT, cribs=(Crib(0,"SLOWLY"),))
        self.assertTrue(report['candidates'][0]['plaintext'].startswith('SLOWLYDESPARATLYSLOWLY'))
        self.assertTrue(report['candidates'][0]['forward_consistent'])
        self.assertIsNone(report['claimed_plaintext'])
        self.assertLessEqual(report['checks'],5000)

    def test_blind_frozen_control_and_actual_hash(self):
        from engine.solvers.persona_cartographer import investigate_cartographer
        path = Path(__file__).parents[1]/'engine/data/transposition_ensemble_certificate.json'
        cert=json.loads(path.read_text())
        report=investigate_cartographer(cert['ciphertext'])
        self.assertEqual(hashlib.sha256(report['candidates'][0]['plaintext'].encode()).hexdigest(),cert['plaintext_sha256'])
        self.assertTrue(report['search_complete'])

    def test_limits_and_unresolved_empty_search(self):
        from engine.solvers.persona_cartographer import investigate_cartographer
        report=investigate_cartographer('ABCDEFGHIJKL',max_checks=0)
        self.assertEqual(report['checks'],0)
        self.assertEqual(report['candidates'],[])
        self.assertFalse(report['search_complete'])
        for params in ({'max_width':33},{'max_rails':8},{'max_checks':-1}):
            with self.assertRaises((ValueError,TypeError)):
                investigate_cartographer('ABCDEFGHIJKL',**params)


if __name__=='__main__': unittest.main()
