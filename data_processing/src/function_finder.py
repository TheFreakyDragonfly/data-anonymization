import re
from standalone_anonymization_functions import *
from translate import Translator
from pycountry import countries
from geotext import GeoText
from finance import Finance
from personal import Personal
from LLMInteractor import LLMInteractor
from ExtensionHelper import ext_print
all_countries = [country.name for country in countries]


class FunctionFinder:
    @staticmethod
    def match_function_by_regex_name_and_content(column_name, example_data, allow_llm=True):
        """
        Tries to match a function to a column by examining name and content of column.
        :param column_name: Column name to use.
        :param example_data: Example piece of data.
        :param allow_llm: Yes or no to asking llm for categorization.
        :return: Matched function.
        """
        example_data = str(example_data)
        # TODO Improve existing cases
        # set up useful variables
        c_low = column_name.lower()

        # match different cases
        if re.match(r"\bid\b", c_low) and re.match('([a-zA-Z]+)|([0-9]+)', example_data):
            return anonymize_id
        if 'company' in c_low:
            return anonymize_company_name
        if (re.match('email|e-mail', c_low)
                or re.match(r"[^@]+@[^@]+\.[^@]+", example_data.lower())):
            return anonymize_email
        if 'position' in c_low or 'title' in c_low:
            return anonymize_position
        if 'name' in c_low:
            return anonymize_name
        if 'address' in c_low:
            return generalize_address
        if 'phone' in c_low:
            return anonymize_phone
        if 'fax' in c_low:
            return anonymize_phone
        if (re.match(r"\biban\b", c_low)
                or re.match('[A-Z]{2}\\d{2}\\s?([A-Z0-9]+\\s?)+', str(example_data))
                and len(example_data) >= 16):
            return Finance.anonymize_iban
        if (re.match(r"\bdate\b", c_low)
                or re.match('\\d{2}.\\d{2}.\\d{4}', str(example_data))
                or re.match('\\d{4}.\\d{2}.\\d{2}', str(example_data))):
            return Personal.anonymizing_date
        if re.match(r"\bcountry\b", c_low) or str(Translator(to_lang="en").translate(example_data)) in all_countries:
            return Personal.anonymize_country
        if re.match(r"\bcity\b", c_low) or len(GeoText(str(example_data)).cities) > 0:
            return Personal.anonymize_city
        if re.match('([A-Z][a-zäöüß\\-\\s]+\\s?)+', str(example_data).rstrip()):
            return Personal.anonymize_name
        if re.match('[A-Z0-9]+', str(example_data)):
            return Finance.anonymize_by_replacing
        if re.match(".*,.*", str(example_data).rstrip()):
            return Personal.anonymize_name

        # Ask llm as last measure
        if allow_llm:
            ext_print('Asking LLM about Column "' + column_name + '"')
            llmi = LLMInteractor()
            answer = llmi.ask_about_column_name(column_name)
            ext_print('LLM Answer: ' + str(answer))

            if answer:
                return censor_fully
            else:
                return anonymize_nothing

        # if llm disallowed and no other match found
        return censor_fully
