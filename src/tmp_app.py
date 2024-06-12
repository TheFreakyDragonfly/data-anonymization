from finance import Finance
from re import match


def anonymizing_bank_data(data):
    if match('[A-Z]{2}\\d{2}\\s?([A-Z0-9]+\\s?)+', str(data)):
        anonymized = Finance.anonymize_iban(data)
    elif match('[A-Z][a-zäöüß]+\\s?[A-Z][a-zäöüß]+', str(data)):
        anonymized = Finance.anonymize_account_owner(True)
    elif match('[A-Z][a-zäöüß]+,\\s?[A-Z][a-zäöüß]+', str(data)):
        anonymized = Finance.anonymize_account_owner(False)
    elif match('[A-Z0-9]+', str(data)):
        anonymized = Finance.anonymize_transaction_number(data)
    elif match('', str(data)):  # HOW TO IDENTIFY COMPANIES
        anonymized = Finance.anonymize_transaction_recipient(data)
    else:
        print("Föck")


if __name__ == '__main__':
    anonymizing_bank_data('DE89 3704 0044 0532 0130 00')
    anonymizing_bank_data('US89 3704 0044 0532 0130 0032 2312 1231')
    anonymizing_bank_data('GR233526252525525552')

    anonymizing_bank_data('123123234234')
    anonymizing_bank_data(35123)
    anonymizing_bank_data('D6483')

    anonymizing_bank_data("Hans Werner")
    anonymizing_bank_data("Jauch, Günther")
