from functools import partial
from operator import is_not
import pandas
import re
import requests


class Prototype:
    def __init__(self, file_path):
        try:
            self.data = self.read_xlsx(file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File can't be opened, cuz not found: {e}")

    def anonymize(self):
        for i, column in enumerate(self.data.columns):
            if 0 <= i < 12:
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

        # pick out function based on regex match
        if re.match(r".*\b(Kontaktperson|kontaktperson|Speichern\sunter|speichern"
                    r"\sunter|Firma|firma|Nachname|nachname|Vorname|vorname)\b.*", column):
            self.manipulate_data(column)
        elif re.match(".*(ID|id|iD|Id).*", column):
            obj_list = self.modifying_numbers(column.upper())
            self.data[column] = pandas.Series(obj_list)
        elif re.match(".*(EMAIL|email|Email|E-Mail|E-mail).*", column):
            function_to_apply = Prototype.anonymize_email
            self.manipulate(function_to_apply, column)
        elif re.match(r".*\b(Position|position|Stelle|stelle)\b.*", column):
            function_to_apply = Prototype.anonymize_position
            self.manipulate(function_to_apply, column)
        elif re.match(".*(Telefon|telefon).*", column):
            if "Mobil" in column or "mobil" in column:
                function_to_apply = Prototype.anonymize_mobile_phone
            else:
                function_to_apply = Prototype.anonymize_phone
            self.manipulate(function_to_apply, column)
        elif re.match(".*(Fax|fax).*", column):
            function_to_apply = Prototype.anonymize_phone
            self.manipulate(function_to_apply, column)
        else:
            self.manipulate(function_to_apply, column)

    def manipulate(self, function_to_apply, column):
        manipulated_list = []
        for index, value in self.data[column].items():
            if isinstance(value, str):
                manipulated_list.append(function_to_apply(value))
            else:
                manipulated_list.append("")
        self.data[str(column)] = pandas.Series(manipulated_list)

    def manipulate_data(self, column):
        obj_list = self.modifying_str(column)
        self.data[column] = pandas.Series(obj_list)

    @staticmethod
    def read_xlsx(file_path: str):
        data = pandas.read_excel(file_path)
        pandas.set_option('display.max_columns', None)
        return data

    @staticmethod
    def default_anonymization_function(value: str):
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
    def anonymize_position(position: str):
        """
        Method to anonymize Position in company.
        :param position: Position to anonymize.
        :return: Anonymized position.
        """
        special_chars = Prototype.filter_special_chars(position, [])
        return "".join(special_chars) + "position"

    @staticmethod
    def anonymize_phone(phonenumber: str):
        if not re.match("\\(\\d{3}\\)\\d{3}-\\d{4}", phonenumber):
            raise Exception("Phonenumber doesn't follow pattern!")

        anonymized_phonenumber = phonenumber[0:5] + "000-0000"

        return anonymized_phonenumber

    @staticmethod
    def anonymize_mobile_phone(mobile: str):
        if not re.match("\\d{3} \\d \\d{3} \\d{3} \\d{4}", mobile):
            raise Exception("Mobile phone number doesn't follow pattern!")

        anonymized_mobile = mobile[0:3] + " 0 000 000 0000"

        return anonymized_mobile

    @staticmethod
    def filter_special_chars(element: str, special_chars: list):
        for single_char in element:
            if not (65 <= ord(single_char) <= 90 or 97 <= ord(single_char) <= 122) and ord(single_char) != 32:
                special_chars.append(single_char)
        return list(filter(partial(is_not, ','), special_chars))

    @staticmethod
    def replace_str(data: str, special_chars: list, data_obj: str):
        if data_obj == "Vorname" or data_obj == "Nachname":
            changed_obj = data_obj
        elif data_obj == "Speichern unter":
            changed_obj = "Nachname, Vorname"
        elif data_obj == "Kontaktperson":
            changed_obj = "Vorname Nachname"
        else:
            changed_obj = data
        for single_special_char in special_chars:
            changed_obj += single_special_char
        return changed_obj

    def modifying_str(self, thing: str):
        series = self.data[thing.capitalize()]
        series_list = series.tolist()

        anon_list = []
        for index in range(len(series_list)):
            special_chars = []
            special_chars = self.filter_special_chars(series_list[index], special_chars)
            data_obj = self.replace_str(series_list[index], special_chars, thing.capitalize())
            anon_list.append(data_obj)
        return anon_list

    '''
        (int(every_id / 10) * 10) + 10      >   0-9  =  10;  10-19  = 20;
        (int(every_id / 100) * 100) + 100   >   0-99 = 100; 100-299 = 200;
    '''
    def modifying_numbers(self, thing: str):
        id_list = self.data[thing.upper()].tolist()
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
        self.data.to_excel("anonymized_data_v2.xlsx")


def only_roman_letters(value):
    """
    Function examining if a bunch of letters contain anything that isn't roman numerals.
    :param value: The value to check for.
    :return: Boolean value saying if only roman numerals were found.
    """
    valid_numerals = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    for letter in value:
        if letter not in valid_numerals:
            return False
    return True


class FakePerson:
    """
    Class containing either fake data or unset data.
    Attribute data_loaded indicates if data was loaded successfully on creation.
    load_data() allows user to attempt loading data again.
    """
    def __init__(self):
        # attempt to load data
        self.json = None
        self.name = None
        self.firstname = None
        self.lastname = None
        self.address = None
        self.date = None
        self.email = None
        self.username = None
        self.password = None
        self.ipv4 = None
        self.macaddress = None
        self.company = None
        self.uuid = None
        self.data_loaded = False
        self.load_data()

    def load_data(self):
        """
        Attempts to load data from API into object.
        :return: Boolean saying if loading of data was successful
        """
        try:
            # Get data from API
            response = requests.get("https://api.namefake.com")

            # Get Json from Response
            json = response.json()

            # Set all attributes including flag for valid filling of data
            self.json = json
            self.name = json['name']

            # isolate first, lastname
            name_parts = self.name.split(' ')
            if len(name_parts) > 2 and not only_roman_letters(name_parts[2]):
                self.firstname = name_parts[1]
                self.lastname = name_parts[2]
            else:
                self.firstname = name_parts[0]
                self.lastname = name_parts[1]

            # continue setting other attributes
            self.address = json['address']
            self.date = json['birth_data']
            self.email = json['email_u'] + '@' + json['email_d']
            self.username = json['username']
            self.password = json['password']
            self.ipv4 = json['ipv4']
            self.macaddress = json['macaddress']
            self.company = json['company']
            self.uuid = json['uuid']

            self.data_loaded = True
            return True
        except ConnectionError:
            self.data_loaded = False
            return False


if __name__ == '__main__':
    path = '../data/data_no_blank_columns.xlsx'
    Prototype(path).anonymize()
