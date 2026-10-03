"""Known plaintext in nested certificate vectors must stay out of training."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.neural_grade import certificate_letter_strings, assert_certificate_plaintexts_excluded
class CertificateExclusionsTest(unittest.TestCase):
    def test_nested_and_expected_answers_are_excluded_including_partial_masks(self):
        phrase='THISFROZENCERTIFICATEANSWERISNOTTRAININGDATA'
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'nested_certificate.json').write_text(json.dumps({'vectors':[{'expected_plaintext':phrase}],
                'control':{'plaintext':phrase,'predicted_plaintext':'NOT?A?COMPLETE?ANSWER'}}))
            with patch('engine.neural_grade._DATA',root):
                self.assertIn(phrase,certificate_letter_strings())
                with self.assertRaises(ValueError):assert_certificate_plaintexts_excluded('PREFIX'+phrase+'SUFFIX')
                self.assertNotIn('NOTACOMPLETEANSWER',certificate_letter_strings())
if __name__=='__main__':unittest.main()
