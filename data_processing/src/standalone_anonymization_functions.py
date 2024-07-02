from faker import Faker
import hashlib
from personal import Personal
from random import choices


# General Functions
def anonymize_nothing(value):
    return value


def mask_value(value, mask_char='X'):
    return mask_char * len(str(value))


def censor_fully(value):
    if value is not None:
        return mask_value(value, 'X')
    else:
        return ""


def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()


# Functions for specific cases
def anonymize_person_name(name):
    return Faker().name()


def anonymize_company_name(company_name):
    return Faker().company()


def anonymize_email(email):
    faker = Faker()

    return faker.email(True)


def anonymize_position(position):
    positions = ["Employee", "Chef", "Assistant Manager", "Intern", "Apprentice"]
    return choices(positions)[0]


def anonymize_phone(phone):
    return Personal.anonymize_something(phone)


def generalize_address(value):
    return Faker().address()


def anonymize_postal_code(value):
    return Personal.anonymize_something(value)
