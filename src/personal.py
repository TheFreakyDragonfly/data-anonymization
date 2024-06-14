from datetime import datetime
from finance import Finance
from faker import Faker
from re import match, search
from random import choices


class Personal:
    @staticmethod
    def anonymizing_date(date, is_birthday=False):
        """
            Birth-Date - Set Second Param
            Transaction-Date
            Order-Date
            Project End Date
        """
        if not is_birthday:
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
        else:
            actual_year = str(search(r'\b\d{4}\b', str(date)).group())
            random_date = Faker().date_between_dates(date_start=datetime(int(actual_year) - 5, 1, 1),
                                                     date_end=datetime(int(actual_year) + 5, 1, 1))
        return random_date

    @staticmethod
    def anonymize_martial_status():
        """
            Martial Status
        """
        status = ['single', 'married', 'divorced', 'widowed']
        return choices(status)

    @staticmethod
    def anonymize_gender():
        """
            Gender
        """
        gender = ['male', 'female', 'divers']
        return choices(gender)

    @staticmethod
    def anonymize_city(data):
        """
            City,
            Delivery City,
            Village,
            Place of birth
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
    def __find_special_chars(data, special_chars, special_list):
        for index in range(len(data)):
            if data[index] == " " or data[index] == "-":
                special_chars += 1
                special_list.append(data[index])
        return special_chars, special_list

    @staticmethod
    def anonymize_name(forward, data):
        """
            Account Owner
            Name
            Full Name
            Contact Person
            Delivery Name etc.
        """
        special_chars, special_list = 0, []
        special_surname, special_surname_chars, special_name, special_name_chars = [], 0, [], 0
        if forward:
            special_chars, special_list = Personal.__find_special_chars(data, special_chars, special_list)
        else:
            last_name, first_name = str(data).split(",")
            special_surname_chars, special_surname = Personal.__find_special_chars(last_name,
                                                                                   special_surname_chars, special_surname)
            special_name_chars, special_name = Personal.__find_special_chars(first_name,
                                                                             special_name_chars, special_name)

        name_obj = ""
        if forward:
            for index in range(special_chars):
                name_obj += str(Faker().first_name() + special_list[index])
            return name_obj + str(Faker().last_name())
        else:
            if len(special_surname) == 0:
                name_obj += str(Faker().last_name())
            else:
                for index in range(special_surname_chars):
                    name_obj += str(Faker().last_name() + special_surname[index])
                name_obj += str(Faker().last_name())

            name_obj += ","
            if len(special_name) == 0:
                name_obj += str(Faker().first_name())
            else:
                for index in range(special_name_chars):
                    name_obj += str(special_name[index] + Faker().first_name())
            return name_obj

    @staticmethod
    def anonymize_something(data):
        """
            Social Security Number,
            Passport Number,
            Driver License,
            Tax Identification Number,
            Age,
        """
        return Finance.anonymize_by_replacing(data)

    @staticmethod
    def anonymize_job():
        return Faker().job()
