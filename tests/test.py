import pandas

from src.app import Prototype
from unittest import TestCase
from pandas import Series, DataFrame


class Test(TestCase):
    tests = ["Jéan Pierre", "Hans Günther", "Hans-Werner",
             "Há+s-W[r?er", "ß?6+*#.,-", "Werner, Hans", "Hans", "Mercedes Benz"]
    columns = ['Kontaktperson', 'Speichern unter',
               'Firma', 'Nachname', 'Vorname']
    nums = [221, 299, 300, 834, 2911, 0, 342374623]

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

    def test_modifying_nums(self):
        data = Series(self.nums)
        self.assertEqual([300, 300, 400, 900, 3000, 100, 342374700],
                         Prototype.modifying_numbers(data))
        self.nums[-1] = -46
        other_data = Series(self.nums)
        self.assertEqual([300, 300, 400, 900, 3000, 100, "naN"],
                         Prototype.modifying_numbers(other_data))
