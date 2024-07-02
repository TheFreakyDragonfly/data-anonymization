import unittest
from finance import Finance
from personal import Personal
from standalone_anonymization_functions import *
from faker import Faker
import re


class TestAnonymization(unittest.TestCase):

    def test_anonymize_iban(self):
        """
        Tests the anonymization of an IBAN (International Bank Account Number).
        Verifies that the original IBAN and the anonymized IBAN are different
        and that the anonymized IBAN matches the expected format.
        """
        fake = Faker()
        original_iban = "DE89 3704 0044 0532 0130 00"
        anonymized_iban = Finance.anonymize_iban(original_iban)
        self.assertNotEqual(original_iban, anonymized_iban)
        self.assertTrue(re.match(r'[A-Z]{2}\d{2}\s?([A-Z0-9]+\s?)+', anonymized_iban))

    def test_anonymize_email(self):
        """
        Tests the anonymization of an email address.
        Verifies that the original email and the anonymized email are different
        and that the anonymized email matches the expected email format.
        """
        original_email = "test@example.com"
        anonymized_email = anonymize_email(original_email)
        print(f"Original Email: {original_email}, Anonymized Email: {anonymized_email}")  # Debug print
        self.assertNotEqual(original_email, anonymized_email)
        self.assertTrue(re.match(r'[^@]+@[^@]+\.[^@]+', anonymized_email))

    def test_anonymize_company(self):
        """
        Tests the anonymization of a company name.
        Verifies that the original company name and the anonymized company name are different.
        """
        fake = Faker()
        original_company = "Example GmbH"
        anonymized_company = Finance.anonymize_company(original_company)
        self.assertNotEqual(original_company, anonymized_company)

    def test_anonymize_phone(self):
        """
        Tests the anonymization of a phone number.
        Verifies that the original phone number and the anonymized phone number are different
        and that the anonymized phone number matches a valid phone number format.
        """
        original_phone = "+1-800-555-5555"
        anonymized_phone = anonymize_phone(original_phone)
        print(f"Original Phone: {original_phone}, Anonymized Phone: {anonymized_phone}")  # Debug print
        self.assertNotEqual(original_phone, anonymized_phone)
        self.assertTrue(re.match(r'(\+?\d-)?(\d{3}-)?\d{3}-\d{4}', anonymized_phone))

    def test_anonymizing_date(self):
        """
        Tests the anonymization of a date.
        Verifies that the original date and the anonymized date are different
        and that the anonymized date matches the YYYY-MM-DD format.
        """
        fake = Faker()
        original_date = "2023-01-01"
        anonymized_date = Personal.anonymizing_date(original_date)
        self.assertNotEqual(original_date, anonymized_date)
        self.assertTrue(re.match(r'\d{4}-\d{2}-\d{2}', anonymized_date))

    def test_anonymize_name_forward(self):
        """
        Tests the anonymization of a person's name.
        Verifies that the original name and the anonymized name are different.
        """
        original_name = "John Doe"
        anonymized_name = Personal.anonymize_name_forward(original_name)
        self.assertNotEqual(original_name, anonymized_name)

    def test_anonymize_country(self):
        """
        Tests the anonymization of a country name.
        Verifies that the original country name and the anonymized country name are different.
        """
        original_country = "Germany"
        anonymized_country = Personal.anonymize_country(original_country)
        self.assertNotEqual(original_country, anonymized_country)

    def test_anonymize_city(self):
        """
        Tests the anonymization of a city name.
        Verifies that the original city name and the anonymized city name are different.
        """
        original_city = "Berlin"
        anonymized_city = Personal.anonymize_city(original_city)
        self.assertNotEqual(original_city, anonymized_city)

    def test_anonymize_postal_code(self):
        """
        Tests the anonymization of a postal code.
        Verifies that the original postal code and the anonymized postal code are different.
        """
        original_postal_code = "12345"
        anonymized_postal_code = anonymize_postal_code(original_postal_code)
        self.assertNotEqual(original_postal_code, anonymized_postal_code)

    def test_anonymize_position(self):
        """
        Tests the anonymization of a job position.
        Verifies that the original position and the anonymized position are different.
        """
        original_position = "Manager"
        anonymized_position = anonymize_position(original_position)
        self.assertNotEqual(original_position, anonymized_position)

    def test_anonymize_transaction_number(self):
        """
        Tests the anonymization of a transaction number.
        Verifies that the original transaction number and the anonymized transaction number are different.
        """
        original_transaction_number = "123456789012"
        anonymized_transaction_number = Finance.anonymize_by_replacing(original_transaction_number)
        self.assertNotEqual(original_transaction_number, anonymized_transaction_number)


if __name__ == '__main__':
    unittest.main()