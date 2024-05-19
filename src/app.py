from functools import partial
from operator import is_not
import pandas
import re

COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6 = (
    'Kontaktperson', 'Speichern unter', "ID", 'Firma', 'Nachname', 'Vorname')

COLUMN_7, COLUMN_8, COLUMN_9, COLUMN_10, COLUMN_11, COLUMN_12 = (
    'E-Mail-Adresse', 'Position', 'Telefon (geschäftlich)', 'Telefon privat', 'Mobiltelefon', 'Faxnummer'
)


class Prototype:
    def __init__(self, file_path):
        try:
            self.data = self.read_xlsx(file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File can't be opened, cuz not found: {e}")

    def anonymize(self):
        self.modifying_str(self.data)
        manipulated_list = self.modifying_numbers(self.data[COLUMN_3])
        self.data[COLUMN_3] = pandas.Series(manipulated_list)

        # Handle columns 6-12
        for i, column in enumerate(self.data.columns):
            if 6 <= i <= 12:
                self.anonymize_column(column)

        self.write_excel()
        print("Executed Anonymization...")

    def anonymize_column(self, column):
        """
        Method that handles individual columns by deciding based on regex.

        :param column: Column to determine and apply anonymization for.
        :return: nothing
        """
        function_to_apply = self.default_anonymization_function

        # pick out function
        if re.match(".*(EMAIL|email|Email|E-Mail|E-mail).*", column):
            function_to_apply = Prototype.anonymize_email

        # apply function to all values in column
        manipulated_list = []
        for index, value in self.data[column].items():
            if isinstance(value, str):
                manipulated_list.append(function_to_apply(value))
            else:
                manipulated_list.append("")
        self.data[str(column)] = pandas.Series(manipulated_list)

    @staticmethod
    def read_xlsx(file_path: str):
        data = pandas.read_excel(file_path)
        pandas.set_option('display.max_columns', None)
        return data

    @staticmethod
    def default_anonymization_function(value:str):
        return "".join("*" for _ in value)

    @staticmethod
    def anonymize_email(email: str):
        """
        Performs various techniques to generate anonymized email addresses. Keeps domain at the end intact.

        :param email: Email address to be anonymized
        :return: Anonymized email address
        """
        sections = email.split("@")

        # Raise exceptions when most basic email format is violated
        if len(sections) != 2:
            raise Exception("Email doesnt contain EXACTLY one @!")
        if "." not in sections[1]:
            raise Exception("Email does not provide a domain, such as '.com'!")

        # prepare first and second half
        subsections_in_first_section = sections[0].split(".")
        subsections_in_first_section_len = len(subsections_in_first_section)
        subsections_in_second_section = sections[1].split(".")
        subsections_in_second_section_len = len(subsections_in_second_section)

        # Construct anonymized email from subsections of original email, keeping domain at the end intact
        anonymized_email_construction = ""
        for i, subsection in enumerate(subsections_in_first_section):
            special_characters = Prototype.filter_special_chars(subsection, [])
            anonymized_email_construction += "".join(special_characters)
            anonymized_email_construction += "prefix"
            if i != subsections_in_first_section_len-1:
                anonymized_email_construction += "."

        anonymized_email_construction += "@"

        for i, subsection in enumerate(subsections_in_second_section):
            if i != subsections_in_second_section_len - 1:
                special_characters = Prototype.filter_special_chars(subsection, [])
                anonymized_email_construction += "".join(special_characters)
                anonymized_email_construction += "domain"
                if i != subsections_in_second_section_len - 2:
                    anonymized_email_construction += "."
            else:
                anonymized_email_construction += "." + subsection

        return anonymized_email_construction

    @staticmethod
    def filter_special_chars(element: str, special_chars: list):
        for single_char in element:
            if not (65 <= ord(single_char) <= 90 or 97 <= ord(single_char) <= 122) and ord(single_char) != 32:
                special_chars.append(single_char)
        return list(filter(partial(is_not, ','), special_chars))

    @staticmethod
    def replace_str(data: str, special_chars: list, data_obj: str):
        if data_obj == COLUMN_6 or data_obj == COLUMN_5:
            changed_obj = data_obj
        elif data_obj == COLUMN_2:
            changed_obj = "Nachname, Vorname"
        elif data_obj == COLUMN_1:
            changed_obj = "Vorname Nachname"
        else:
            changed_obj = data
        for single_special_char in special_chars:
            changed_obj += single_special_char
        return changed_obj

    def modifying_str(self, data: pandas.DataFrame):
        contacts, save_name, company, surname, name = (
            data[COLUMN_1], data[COLUMN_2], data[COLUMN_4], data[COLUMN_5], data[COLUMN_6])

        all_contacts, all_save_name, all_company, all_surnames, all_names = (
            contacts.tolist(), save_name.tolist(), company.tolist(), surname.tolist(), name.tolist())
        all_objects = [all_contacts, all_save_name, all_company, all_surnames, all_names]

        elements = [COLUMN_1, COLUMN_2, COLUMN_4, COLUMN_5, COLUMN_6]

        for index in range(len(all_objects)):
            special_chars, anon_list = [], []
            for element in all_objects[index]:
                special_chars = self.filter_special_chars(element, special_chars)
                data_obj = self.replace_str(element, special_chars, elements[index])
                anon_list.append(data_obj)
            self.data[elements[index]] = pandas.Series(anon_list)

    '''
        (int(every_id / 10) * 10) + 10      >   0-9  =  10;  10-19  = 20;
        (int(every_id / 100) * 100) + 100   >   0-99 = 100; 100-299 = 200;
    '''
    @staticmethod
    def modifying_numbers(data: pandas.Series):
        id_list = data.tolist()
        manipulated_list = []
        for every_id in id_list:
            if isinstance(every_id, int) and every_id >= 0:
                generalization = int(every_id / 100) * 100 + 100
                manipulated_list.append(generalization)
            else:
                manipulated_list.append("naN")
        return manipulated_list

    """
        Only Use for debugging
    """
    def print_data(self, string):
        print(f"{string} Data was:\n", self.data)

    '''
        Change name and path to original file, 
        so it overwrites the data
    '''
    def write_excel(self):
        self.data.to_excel("anonymized_data.xlsx")


if __name__ == '__main__':
    path = '../data/data_+email.xlsx'
    Prototype(path).anonymize()
