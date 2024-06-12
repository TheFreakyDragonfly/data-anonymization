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
    def anonymize_something():
        """
            Social Security Number
        """
        raise NotImplementedError("Not implemented yet...")
