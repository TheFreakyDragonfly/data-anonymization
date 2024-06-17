import unittest
from function_finder import FunctionFinder
from src.finance import Finance
from standalone_anonymization_functions import *


def matcher(cname, cval):
    return FunctionFinder.match_function_by_regex_name_and_content(cname, cval, False)


class TestFunctionFinder(unittest.TestCase):
    def test_finding_id(self):
        self.assertEqual(
            anonymize_id,
            matcher('id', 'AFAIK')
        )
        self.assertNotEqual(
            anonymize_id,
            matcher('kid', 'joseph')
        )

    def test_finding_company(self):
        self.assertEqual(
            anonymize_company_name,
            matcher('company', 'Google')
        )

    # generic case:
    # def test_finding_x(self):
    #     self.assertEqual()

    def test_finding_email(self):
        self.assertEqual(
            anonymize_email,
            matcher('email', 'email@email.com')
        )
        self.assertEqual(
            anonymize_email,
            matcher('xxxxx', 'email@email.com')
        )

    def test_finding_iban(self):
        self.assertEqual(
            Finance.anonymize_iban.__name__,
            matcher('iban', '12').__name__
        )
        self.assertEqual(
            Finance.anonymize_iban.__name__,
            matcher('xxxx', 'NL69ABNA6863597098').__name__
        )
        self.assertEqual(
            Finance.anonymize_iban.__name__,
            matcher('xxxx', 'SA7771894124119856364796').__name__
        )
        self.assertNotEqual(
            Finance.anonymize_iban.__name__,
            matcher('taliban', '12').__name__
        )
        self.assertNotEqual(
            Finance.anonymize_iban.__name__,
            matcher('xxxx', 'DE12345').__name__
        )
