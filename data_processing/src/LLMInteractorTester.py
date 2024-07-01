import unittest
from standalone_anonymization_functions import *
from LLMInteractor import LLMInteractor


class TestFunctionSelection(unittest.TestCase):
    def test_name_selecting(self):
        llmi = LLMInteractor()
        chosen_function = llmi.llm_choose_option(
            column_name='ShipName',
            column_data=[
                'Vins et alcools Chevalier',
                'Toms Spezialitäten',
                'Hanari Carnes',
                'Victuailles en stock',
                'Suprêmes délices'
            ],
            functions=[anonymize_name, anonymize_company_name]
        )
        # Assuming that the expected chosen function is anonymize_company_name
        self.assertEqual(anonymize_company_name.__name__, chosen_function.__name__)


if __name__ == '__main__':
    unittest.main()
