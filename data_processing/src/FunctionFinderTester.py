import unittest
from function_finder import FunctionFinder
from src.finance import Finance
from src.personal import Personal
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
        self.assertEqual(
            anonymize_id,
            matcher('CustomerID', '121')
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
        self.assertEqual(
            anonymize_name,
            matcher('xxxx', 'John Doe')
        )
        self.assertEqual(
            anonymize_name,
            matcher('xxxx', 'Max Mustermann')
        )
        self.assertEqual(
            anonymize_name,
            matcher('xxxx', 'Martin Luther King Jr.')
        )
        self.assertEqual(
            anonymize_name,
            matcher('xxxx', 'Johannes Paul II.')
        )
        self.assertEqual(
            anonymize_name,
            matcher('xxxx', 'John, Elton')
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

    def test_finding_phone(self):
        self.assertEqual(
            anonymize_phone,
            matcher('telephone', 'xxxxx')
        )
        self.assertEqual(
            anonymize_phone,
            matcher('phonenumber', 'xxxxx')
        )
        self.assertEqual(
            anonymize_phone,
            matcher('phone', 'xxxxx')
        )
        self.assertEqual(
            anonymize_phone,
            matcher('xxxxx', '123-123-1234')
        )
        self.assertEqual(
            anonymize_phone,
            matcher('xxxxx', '+1-123-123-1234')
        )
        self.assertEqual(
            anonymize_phone,
            matcher('xxxxx', '123-1234')
        )

    def test_finding_fax(self):
        self.assertEqual(
            anonymize_phone,
            matcher('fax', 'xxxxx')
        )
        self.assertEqual(
            anonymize_phone,
            matcher('faxnumber', 'xxxxx')
        )
        self.assertNotEqual(
            anonymize_phone,
            matcher('halifax', 'xxxxx')
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

    def test_finding_date(self):  # TODO continue HERE
        self.assertEqual(
            Personal.anonymizing_date.__name__,
            matcher('date', 'xxxxx').__name__
        )
        self.assertEqual(
            Personal.anonymizing_date.__name__,
            matcher('xxxx', '01.01.2000').__name__
        )
        self.assertEqual(
            Personal.anonymizing_date.__name__,
            matcher('xxxx', '01.01.2000').__name__
        )
        self.assertEqual(
            Personal.anonymizing_date.__name__,
            matcher('xxxx', '2000-01-01').__name__
        )
        self.assertEqual(
            Personal.anonymizing_date.__name__,
            matcher('xxxx', '01/01/2000').__name__
        )

    def test_finding_country(self):
        self.assertEqual(
            Personal.anonymize_country.__name__,
            matcher('country', 'xxxxx').__name__
        )
        self.assertEqual(
            Personal.anonymize_country.__name__,
            matcher('xxxxx', 'germany').__name__
        )
        self.assertEqual(
            Personal.anonymize_country.__name__,
            matcher('xxxxx', 'deutschland').__name__
        )
        self.assertEqual(
            Personal.anonymize_country.__name__,
            matcher('xxxxx', 'Lietuva').__name__ # Lithuania in Lithuanian
        )
        self.assertNotEqual(
            Personal.anonymize_country.__name__,
            matcher('xxxxx', 'xxxxx').__name__
        )

    def test_finding_city(self):
        self.assertEqual(
            Personal.anonymize_city.__name__,
            matcher('city', 'xxxxx').__name__
        )
        self.assertEqual(
            Personal.anonymize_city.__name__,
            matcher('xxxx', 'London').__name__
        )
        self.assertEqual(
            Personal.anonymize_city.__name__,
            matcher('xxxx', 'Derry').__name__
        )
        self.assertEqual(
            Personal.anonymize_city.__name__,
            matcher('xxxx', 'Stuttgart').__name__
        )
        self.assertNotEqual(
            Personal.anonymize_city.__name__,
            matcher('xxxx', 'xxxxx').__name__
        )

    def test_finding_transaction_number(self):
        self.assertEqual(
            Finance.anonymize_by_replacing.__name__,
            matcher('transaction number', 'xxxxx').__name__
        )
        self.assertEqual(
            Finance.anonymize_by_replacing.__name__,
            matcher('xxxxx', 'VADE0B248932').__name__
        )
        self.assertEqual(
            Finance.anonymize_by_replacing.__name__,
            matcher('xxxxx', 'ACRAF23DB3C4').__name__
        )
        self.assertNotEqual(
            Finance.anonymize_by_replacing.__name__,
            matcher('xxxxx', 'xxxxx').__name__
        )

    def test_finding_postal_code(self):
        self.assertEqual(
            anonymize_postal_code,
            matcher('postal code', 'xxxxx')
        )
        self.assertEqual(
            anonymize_postal_code,
            matcher('xxxxx', '12345')
        )
        self.assertEqual(
            anonymize_postal_code,
            matcher('xxxxx', 'B-6000')
        )
