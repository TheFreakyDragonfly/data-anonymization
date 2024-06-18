from faker import Faker
import hashlib


# General Functions
def anonymize_nothing(value):
    return value


def mask_value(value, mask_char='X'):
    return mask_char * len(value)


def censor_fully(value):
    if value is not None:
        return mask_value(value, 'X')
    else:
        return ""


def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()


# Functions for specific cases
def anonymize_name(name):
    return Faker().name()


def anonymize_id(given_id):
    return (int(given_id) / 100) * 100 + 100


def anonymize_company_name(company_name):
    return Faker().company()


def anonymize_email(email):
    faker = Faker()

    splits = email.split(".")
    domain = splits[len(splits)-1]

    return faker.email(True, domain)


def anonymize_position(position):
    return "Employee"


def anonymize_phone(phone):
    return 'XXX-XXX-XXXX'


def generalize_address(value):
    parts = value.split(',')
    if len(parts) > 1:
        return parts[-2].strip() + ', ' + parts[-1].strip()
    return value

def anonymize_postal_code(value):
    return 0
