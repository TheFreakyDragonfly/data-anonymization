from faker import Faker
from re import match


class Personal:
    @staticmethod
    def anonymizing_date(date):
        """
            Birth-Date
            Transaction-Date
            Order-Date
            Project End Date
        """
        if match('\\d{4}-\\d{2}-\\d{2}', str(date)):
            random_date = Faker().date('%Y-%m-%d')
        elif match('\\d{2}-\\d{2}-\\d{4}', str(date)):
            random_date = Faker().date('%d-%m-%Y')
        elif match('\\d{2}/\\d{2}/\\d{4}', str(date)):
            random_date = Faker().date('%d/%m/%Y')
        elif match('\\d{4}/\\d{2}/\\d{2}', str(date)):
            random_date = Faker().date('%Y/%m/%d')
        elif match('\\d{2}[.]\\d{2}[.]\\d{4}', str(date)):
            random_date = Faker().date('%d.%m.%Y')

    @staticmethod
    def anonymize_city(data):
        """
            City,
            Delivery City,
            Village etc.
        """
        special_chars_list, special_chars_count = [], 0
        for index in range(len(data)):
            if data[index] == " " or data[index] == "-":
                special_chars_count += 1
                special_chars_list.append(data[index])
        if special_chars_count == 0:
            return Faker().city()
        else:
            city_obj = ""
            for index in range(special_chars_count):
                city_obj += str(Faker().city() + special_chars_list[index])
            return city_obj

    @staticmethod
    def anonymize_country(data):
        """
            Country
        """
        special_chars_list, special_chars_count = [], 0
        for index in range(len(data)):
            if data[index] == " " or data[index] == "-":
                special_chars_count += 1
                special_chars_list.append(data[index])
        if special_chars_count == 0:
            return Faker().country()
        else:
            city_obj = ""
            for index in range(special_chars_count):
                city_obj += str(Faker().country() + special_chars_list[index])
            return city_obj

    @staticmethod
    def anonymize_something():
        """
            Social Security Number
        """
        raise NotImplementedError("Not implemented yet...")
