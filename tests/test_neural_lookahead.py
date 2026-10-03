"""Cipher trial features discard witnesses and preserve affine key invariance."""
import unittest
import numpy as np
from engine.neural_router_v2 import cryptanalytic_features
from engine.neural_features import feature_tables
from engine.neural_grade import _english_unigram
from engine.solvers.affine import affine_encrypt

class CryptanalyticFeaturesTest(unittest.TestCase):
    def test_bounded_finite_vector_is_invariant_under_affine_search_keys(self):
        prose = 'THEHARBORWATCHKEPTTHELANTERNBURNINGWHILETHELASTSHIPRETURNEDEVERYSAILORWAITEDFORTHEBELLS' * 6
        tables = feature_tables(prose,_english_unigram(prose))
        row = cryptanalytic_features(prose[:180],tables)
        self.assertEqual(len(row),44)
        self.assertTrue(np.all(np.isfinite(row)))
        self.assertTrue(all(isinstance(v,float) for v in row))
        for a,b in ((3,7),(5,2),(25,19)):
            changed = cryptanalytic_features(affine_encrypt(prose[:180],a,b),tables)
            self.assertAlmostEqual(row[37],changed[37],places=10)

class RouterCompatibilityTest(unittest.TestCase):
    def test_all_feature_versions_preserve_declared_widths(self):
        from engine.neural_router_v2 import _features
        prose='THEHARBORWATCHKEPTTHELANTERNBURNINGWHILETHELASTSHIPRETURNED' * 8
        english=_english_unigram(prose);tables=feature_tables(prose,english)
        for version,width in ((2,58),(3,82),(4,126),(5,142),(6,222),(7,228)):
            row=_features(prose[:180],english,tables,version='cipher_statistics_v'+str(version))
            self.assertEqual(len(row),width)
            self.assertTrue(np.all(np.isfinite(row)))

    def test_legacy_regression_cannot_hide_behind_original_baseline(self):
        from engine.neural_router_v2 import promotion_allowed
        self.assertFalse(promotion_allowed(189/204,158/204,428/480,428/480,193/204))
        self.assertTrue(promotion_allowed(194/204,158/204,429/480,428/480,193/204))

if __name__ == '__main__': unittest.main()
