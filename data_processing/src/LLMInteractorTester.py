import unittest
from standalone_anonymization_functions import *
from LLMInteractor import LLMInteractor


class TestFunctionSelection(unittest.TestCase):
    def test_name_selecting(self):
        llmi = LLMInteractor()
        self.assertEqual(anonymize_name,
                         llmi.llm_choose_option(
                             'ShipName',
                             [
                                 'Vins et alcools Chevalier',
                                 'Toms Spezialitäten',
                                 'Hanari Carnes',
                                 'Victuailles en stock',
                                 'Suprêmes délices'
                             ],
                             [
                                 anonymize_name,
                                 anonymize_company_name
                             ]))


if __name__ == '__main__':
    unittest.main()
