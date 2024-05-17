from functools import partial
from operator import is_not
import pandas

COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6 = (
    'Kontaktperson', 'Speichern unter', "ID", 'Firma', 'Nachname', 'Vorname')


class Prototype:
    def __init__(self):
        self.data = self.read_xlsx()

    def anonymize(self):
        self.modifying_str(self.data)
        self.modifying_numbers(self.data)
        self.write_excel()

    @staticmethod
    def read_xlsx():
        data = pandas.read_excel('../data/data.xlsx')
        pandas.set_option('display.max_columns', None)
        return data

    @staticmethod
    def filter_special_chars(element: list, special_chars: list):
        for single_char in element:
            if not (65 <= ord(single_char) <= 90 or 97 <= ord(single_char) <= 122) and ord(single_char) != 32:
                special_chars.append(single_char)
        return list(filter(partial(is_not, ','), special_chars))

    @staticmethod
    def replace_str(data, special_chars: list, data_obj: str):
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

    def modifying_numbers(self, data: pandas.DataFrame):
        customer_id = data[COLUMN_3]
        id_list = customer_id.tolist()
        manipulated_list = []
        for every_id in id_list:
            generalization = int(every_id / 100) * 100 + 100
            manipulated_list.append(generalization)
        self.data[COLUMN_3] = pandas.Series(manipulated_list)

    """
        Only Use for debugging
    """

    def print_data(self, string):
        print(f"{string} Data was:\n", self.data)

    def write_excel(self):
        self.data.to_excel("anonymized_data.xlsx")


if __name__ == '__main__':
    Prototype().anonymize()
