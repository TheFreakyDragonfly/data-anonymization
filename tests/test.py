from src.app import Prototype
from unittest import TestCase
from pandas import Series, DataFrame
from src.app import FakePerson


class Test(TestCase):
    tests = ["Jéan Pierre", "Hans Günther", "Hans-Werner",
             "Há+s-W[r?er", "ß?6+*#.,-", "Werner, Hans", "Hans", "Mercedes Benz"]
    columns = ['Kontaktperson', 'Speichern unter',
               'Firma', 'Nachname', 'Vorname']

    def test_reading_file(self):
        not_existing_file = '../data/dat.xlsx'
        with self.assertRaises(FileNotFoundError):
            Prototype(not_existing_file)
        existing_path = '../data/data.xlsx'
        obj = Prototype(existing_path)
        self.assertIsInstance(obj.data, DataFrame)

    def test_filter(self):
        self.assertEqual(["é"], Prototype.filter_special_chars(self.tests[0], []))
        self.assertEqual(["ü"], Prototype.filter_special_chars(self.tests[1], []))
        self.assertEqual(["-"], Prototype.filter_special_chars(self.tests[2], []))
        self.assertEqual(["á", "+", "-", "[", "?"],
                         Prototype.filter_special_chars(self.tests[3], []))
        self.assertEqual(['ß', '?', '6', '+', '*', '#', '.', '-'],
                         Prototype.filter_special_chars(self.tests[4], []))
        self.assertEqual([], Prototype.filter_special_chars(self.tests[5], []))

    def test_replacement(self):
        self.assertEqual("Vorname Nachname",
                         Prototype.replace_str(self.tests[5], [], self.columns[0]))
        self.assertEqual("Nachname, Vorname",
                         Prototype.replace_str(self.tests[1], [], self.columns[1]))
        self.assertEqual("Mercedes Benz",
                         Prototype.replace_str(self.tests[7], [], self.columns[2]))
        self.assertEqual("Nachname",
                         Prototype.replace_str(self.tests[6], [], self.columns[3]))
        self.assertEqual("Vorname",
                         Prototype.replace_str(self.tests[6], [], self.columns[4]))

        self.assertEqual("Vorname-é",
                         Prototype.replace_str(self.tests[6], ["-", "é"], self.columns[4]))

    def test_modifying_email(self):
        self.assertEqual(
            'prefix.prefix@domain.domain.com',
            Prototype.anonymize_email(
                'john.smith@mail.example.com'
            )
        )
        self.assertEqual(
            '^äöü-?`´*+prefix.^äöü-?`´*+prefix@^äöü-?`´*+domain.^äöü-?`´*+domain.^äöü-?`´*+com',
            Prototype.anonymize_email(
                '^äöü-?`´*+john.^äöü-?`´*+smith@^äöü-?`´*+mail.^äöü-?`´*+example.^äöü-?`´*+com'
            )
        )

    def test_modifying_position(self):
        self.assertEqual(
            'position',
            Prototype.anonymize_position(
                'Einkaufsmitarbeiter'
            )
        )
        self.assertEqual(
            'äüöposition',
            Prototype.anonymize_position(
                'Einkäüfsmitarbeiterö'
            )
        )

    def test_modifying_phone(self):
        self.assertEqual(
            '(123)000-0000',
            Prototype.anonymize_phone(
                '(123)123-1234'
            )
        )
        self.assertEqual(
            '(768)000-0000',
            Prototype.anonymize_phone(
                '(768)545-2894'
            )
        )

    def test_modifying_mobile_phone(self):
        self.assertEqual(
            '010 0 000 000 0000',
            Prototype.anonymize_mobile_phone(
                '010 1 123 123 1234'
            )
        )
        self.assertEqual(
            '726 0 000 000 0000',
            Prototype.anonymize_mobile_phone(
                '726 7 321 321 4321'
            )
        )


class TestFakeName(TestCase):
    def testCreationAndData(self):
        print("Anwendungsbeispiel!")
        fake_person_dataset = FakePerson()
        print(fake_person_dataset.json)
        print(fake_person_dataset.name)
        print(fake_person_dataset.firstname)
        print(fake_person_dataset.lastname)
        print(fake_person_dataset.email)
