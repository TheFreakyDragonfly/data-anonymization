import unittest
from function_finder import FunctionFinder
from src.finance import Finance
from standalone_anonymization_functions import *


def matcher(cname, cval):
    """
    Uses match_function_by_regex_name_and_content but always provides allow_llm=False.
    """
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
        self.assertNotEqual(
            anonymize_company_name,
            matcher('badcompany', 'Google')
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
        self.assertNotEqual(
            anonymize_email,
            matcher('name-mail', 'xxxxx')
        )
        self.assertNotEqual(
            anonymize_email,
            matcher('xxxxx', 'email.com')
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

    def test_finding_title(self):
        self.assertEqual(
            anonymize_position,
            matcher('position', 'xxxxx')
        )
        self.assertEqual(
            anonymize_position,
            matcher('title', 'xxxxx')
        )
        self.assertNotEqual(
            anonymize_position,
            matcher('superposition', 'xxxxx')
        )
        self.assertNotEqual(
            anonymize_position,
            matcher('subtitle', 'xxxxx')
        )

    def test_finding_name(self):
        self.assertEqual(
            anonymize_name,
            matcher('name', 'xxxxx')
        )
        self.assertEqual(
            anonymize_name,
            matcher('lastname', 'xxxxx')
        )
        self.assertNotEqual(
            anonymize_name,
            matcher('namesake', 'xxxxx')
        )

    def test_finding_address(self):
        self.assertEqual(
            generalize_address,
            matcher('address', 'xxxxx')
        )
        self.assertEqual(
            generalize_address,
            matcher('home address', 'xxxxx')
        )
        self.assertEqual(
            generalize_address,
            matcher('homeaddress', 'xxxxx')
        )
        self.assertNotEqual(
            generalize_address,
            matcher('addressee', 'xxxxx')
        )

    # continue testing from phone
