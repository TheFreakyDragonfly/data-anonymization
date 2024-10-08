import re
from standalone_anonymization_functions import *
from pycountry import countries
from geotext import GeoText
from finance import Finance
from personal import Personal
from LLMInteractor import LLMInteractor
from ExtensionHelper import ext_print
import translators as ts

all_countries = [country.name for country in countries]  # postalcode customerid

llmi = LLMInteractor()


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
        # set up useful variables
        example_data = str(example_data)
        c_low = column_name.lower()

        if len(column_name) > 250:
            column_name = column_name[:250]
        if len(example_data) > 250:
            example_data = example_data[:250]

        # match different cases
        if ((re.match(r"\bid\b", c_low) or re.match(r".*[a-z]I[dD]\b", column_name))
                and re.match('([a-zA-Z]+)|(\\d+)', example_data)):
            return Personal.anonymize_something

        if re.match(r"\bcompany\b", c_low):
            return anonymize_company_name

        if (re.match(r"\bemail\b|\be-mail\b", c_low)
                or re.match(r"[^@]+@[^@]+\.[^@]+", example_data.lower())):
            return anonymize_email

        if re.match(r"\bposition\b|\btitle\b", c_low):
            return anonymize_position

        if re.match(r".*address\b", c_low):
            return generalize_address

        if (re.match(r".*phone.*", c_low)
                or re.match(r"(\+?\d-)?(\d{3}-)?\d{3}-\d{4}", example_data)):
            return anonymize_phone

        if re.match(r"\bfax", c_low):
            return anonymize_phone

        if (re.match(r"\biban\b", c_low)
                or re.match('[A-Z]{2}\\d{2}\\s?([A-Z0-9]+\\s?)+', str(example_data))
                and len(example_data) >= 16):
            return Finance.anonymize_iban

        if (re.match(r".*date\b", c_low)
                or re.match('\\d{2}([-./])\\d{2}\1\\d{4}', str(example_data))
                or re.match('\\d{4}([-./])\\d{2}\1\\d{2}', str(example_data))):
            return Personal.anonymizing_date

        formatted_country = ts.translate_text(str(example_data)).title()
        # formatted_country = str(Translator(to_lang="en").translate(example_data)).title()
        if (re.match(r"\bcountry\b", c_low)
                or formatted_country in all_countries):
            return Personal.anonymize_country

        if (re.match(r"\bcity\b", c_low)
                or len(GeoText(str(example_data)).cities) > 0):
            return Personal.anonymize_city

        if (re.match(r"[A-Z0-9]{12}", str(example_data))
                or re.match(r".*transaction number.*", c_low)):
            return Finance.anonymize_by_replacing

        if (re.match(r"\bpostal\s?code\b", c_low)
                or re.match(r"([a-zA-Z]-)?\d{4,5}(-\d{3})?", str(example_data))):
            return anonymize_postal_code

        if re.match(r".*name\b", c_low):
            chosen = llmi.llm_choose_option(
                column_name=column_name,
                column_data=[example_data],
                functions=[anonymize_person_name, anonymize_company_name]
            )
            if chosen is not None and chosen.__name__ == anonymize_person_name.__name__:
                if re.match('([A-Z][a-zäöüß\\-\\s]+\\s?)+', str(example_data).rstrip()):
                    return Personal.anonymize_name_forward
                elif re.match("\\D+,\\D+", str(example_data).rstrip()):
                    return Personal.anonymize_name_backwards
            elif chosen is not None and chosen.__name__ == anonymize_company_name.__name__:
                return anonymize_company_name

        if (re.match("\bcontact.?title\b", c_low)):
            return anonymize_position
            
        if (re.match(r".*price\b", c_low)
                or re.match(r".*[$€].*", example_data)):
            return anonymize_nothing

        if re.match(r"(\d+([,.]\d+)?%)|(0[,.]\d+)", example_data):
            return anonymize_nothing

        # Ask llm as last measure
        if allow_llm:
            answer = llmi.ask_about_column_name(column_name)

            if answer:
                return censor_fully
            else:
                return anonymize_nothing

        # if llm disallowed and no other match found
        return censor_fully
