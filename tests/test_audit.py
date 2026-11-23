import tempfile
import unittest
from pathlib import Path
from issn_validation_claim_audit.audit import audit, evidence, matches, prose
from issn_validation_claim_audit.phrases import ISSNVALIDATION, NOISSNVALIDATION, GENERIC_NAMES

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        for phrase in ISSNVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(matches(phrase)[0])
        for phrase in NOISSNVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(matches(phrase), ([], [phrase]))
        self.assertEqual(matches('```\nvalidate issn\n```'), ([], []))

    def test_routes(self):
        cases = ['import stdnum\nstdnum.issn.validate(x)', 'import stdnum.issn\nstdnum.issn.is_valid(x)', 'import stdnum.issn as s\ns.validate(x)', 'from stdnum import issn as s\ns.is_valid(x)', 'from stdnum.issn import validate as v\nv(x)', 'from stdnum.issn import is_valid as v\nv(x)']
        cases += ['obj.' + name + '(x)' for name in GENERIC_NAMES]
        cases += ['from x import ' + name + ' as v\nv(x)' for name in GENERIC_NAMES]
        for case in cases:
            with self.subTest(case=case): self.assertTrue(evidence(case))

    def test_not_evidence(self):
        cases = ['import stdnum.issn', 'validate(x)', 'is_valid(x)', 'obj.validate(x)', 'obj.is_valid(x)']
        cases += ['import stdnum.issn\nstdnum.issn.' + n + '(x)' for n in ('compact', 'format', 'calc_check_digit', 'to_ean')]
        cases += ['issn.' + n + '(x)' for n in ('load_data_by_url', 'lookup')]
        cases += ['isbnlib.' + n + '(x)' for n in ('is_isbn10', 'is_isbn13', 'notisbn', 'Isbn')]
        cases += ['barcode.' + n + '(x)' for n in ('ISSN', 'get', 'generate')]
        cases += ['re.' + n + '(pattern, x)' for n in ('match', 'search', 'fullmatch')]
        cases += ['validators.' + n + '(x)' for n in ('url', 'ipv4', 'ipv6', 'email', 'card_number', 'domain')]
        cases += ['urlparse(x)', 'urlsplit(x)', 'subprocess.run("validate issn")', 'payment.process(x)', 'extract.read(x)', '"validate issn"', '# validate issn', 'obj.validate_issn', 'invalid syntax !', 'from x import validate_issn as v\ndef v(): pass\nv()', 'import stdnum\nstdnum = 1\nstdnum.issn.validate(x)', 'from x import validate_issn\nwith x as validate_issn: pass\nvalidate_issn(x)', 'from stdnum import issn', 'issn.validate(x)']
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence(case))

    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'README.md').write_text('validate issn')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')
            (root / 'test_a.py').write_text('obj.validate_issn(x)')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'MEDIUM')
            (root / 'a.py').write_text('obj.validate_issn(x)')
            self.assertFalse(audit(root)['findings'])
            (root / 'README.md').write_text('no issn validation')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')
            self.assertFalse(audit(root, ['a.py'])['findings'])

    def test_self_audit(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse(audit(root)['findings'])
        self.assertFalse(audit(root / 'README.md')['findings'])

    def test_limitations_prose(self):
        root = Path(__file__).resolve().parents[1]
        limitations = (root / 'README.md').read_text().split('## Limitations', 1)[1]
        self.assertEqual(matches(limitations), ([], []))
