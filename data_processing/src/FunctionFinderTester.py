import unittest
from function_finder import FunctionFinder
from standalone_anonymization_functions import *


class TestFunctionFinder(unittest.TestCase):
    def test_finding_id(self):
        self.assertEqual(anonymize_id, FunctionFinder.match_function_by_regex_name_and_content('id', 'AFAIK'))

    def test_finding_company(self):
        self.assertEqual(anonymize_id, FunctionFinder.match_function_by_regex_name_and_content('company', 'Google'))
