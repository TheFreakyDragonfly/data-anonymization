from pycountry import countries
from finance import Finance
from personal import Personal
from re import match


def anonymizing_bank_data(data):
    if match('[A-Z]{2}\\d{2}\\s?([A-Z0-9]+\\s?)+', str(data)):
        anonymized = Finance.anonymize_iban(data)
    elif match(".*,.*", str(data).rstrip()):
        anonymized = Finance.anonymize_name(False, data.rstrip())
    elif match('([A-Z][a-zäöüß\\-\\s]+\\s?)+', str(data).rstrip()):
        anonymized = Finance.anonymize_name(True, data.rstrip())
    elif match('[A-Z0-9]+', str(data)):
        anonymized = Finance.anonymize_by_replacing(data)
    elif match('', str(data)):  # HOW TO IDENTIFY COMPANIES
        #anonymized = Finance.anonymize_transaction_recipient(data)
        raise NotImplementedError("No Regex provided")


def anonymizing_personal(data):
    all_countries = [country.name for country in countries]
    if match('\\d{2}.\\d{2}.\\d{4}', str(data)) or match('\\d{4}.\\d{2}.\\d{2}', str(data)):
        anonymized = Personal.anonymizing_date(data)
    elif str(data) in all_countries:
        anonymized = Personal.anonymize_country(data)
        raise NotImplementedError("Need Translation to English from every language...")
    elif match("", str(data)):
        anonymized = Personal.anonymize_city(data)
        raise NotImplementedError("No Regex provided")


if __name__ == '__main__':

    anonymizing_bank_data('DE89 3704 0044 0532 0130 00')
    anonymizing_bank_data('US89 3704 0044 0532 0130 0032 2312 1231')
    anonymizing_bank_data('GR233526252525525552')

    anonymizing_bank_data('123123234234')
    anonymizing_bank_data(35123)
    anonymizing_bank_data('D6483')

    anonymizing_bank_data("Hans Werner Baum")
    anonymizing_bank_data("Günther-Jauch-Der-Top-G")
    anonymizing_bank_data("Hans-Werner Busch")
    anonymizing_bank_data("Hans-Werner Busch ")
    anonymizing_bank_data("Jauch-Günther Hans, Dertop G")
    anonymizing_bank_data("Hans Werner-Busch, Bill Cliton-Der-Juan")

    anonymizing_personal("10.03.2001")
    anonymizing_personal("11-04-2000")
    anonymizing_personal("06-12-2002")
    anonymizing_personal("2003-05-13")
    anonymizing_personal("2004/07/14")
    anonymizing_personal("15/08/2005")
    anonymizing_personal("09/16/2006")

    anonymizing_personal("Afghanistan")
    #anonymizing_personal("Berlin")
