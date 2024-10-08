from random import choices
from faker import Faker


class Finance:
    @staticmethod
    def anonymize_iban(data: str):
        """
            Test-Cases:
            "DE89 3704 0044 0532 0130 00"
            "DE89370400440532013000"
            "US89 3704 0044 0532 0130 00"
        """
        iban_structures = {
            'AL': (0, 12),
            'AD': (0, 8),  # Andorra
            'AZ': (0, 8),  # Aserbaidschan
            'BH': (0, 8),  # Bahrain
            'BE': (0, 7),  # Belgium
            'BA': (0, 7),  # Bosnia
            'BR': (0, 12),  # Brasil
            # 'VG': (0, 0),   # Virgin Islands
            'BG': (0, 12),  # Bulgarien
            'CR': (0, 8),  # Costa Rica
            'DK': (0, 8),  # Denmark
            'DE': (0, 12),  # Germany
            'DO': (0, 8),  # Dominican Republic
            # 'SV': (0, 0),  # Costa Rica
            'EE': (0, 6),  # Estland
            'FO': (0, 8),  # Färöer Isles
            'FI': (0, 10),  # Finnland
            'FR': (0, 9),  # France
            'GE': (0, 6),  # Georgia
            'GI': (0, 8),  # Gibraltar
            'GR': (0, 7),  # Greece
            'GL': (0, 8),  # Grönland
            'GB': (0, 10),  # Britain
            # 'GT': (0, 0),  # Guatemala
            'IQ': (0, 8),  # Iraq
            'IE': (0, 10),  # Irland
            'IS': (0, 8),  # Island
            'IL': (0, 7),  # Israel
            'JO': (0, 8),  # Jordanien
            'KZ': (0, 7),  # Kazakhstan
            'QA': (0, 8),  # Katar
            'XK': (0, 6),  # Kosovo
            'HR': (0, 11),  # Croatia
            # 'KW': (0, 0),  # Kuwait
            'LV': (0, 8),  # Lettland
            'LB': (0, 8),  # Lebanon
            'LI': (0, 9),  # Liechtenstein
            'LT': (0, 9),  # Litauen
            'LU': (0, 7),  # Luxemburg
            'MT': (0, 9),  # Malta
            # 'MR': (0, 0),  # Mauretanien
            'MU': (0, 12),  # Mauritius
            # 'MK': (0, 0),  # Mazedonien
            'MD': (0, 6),  # Moldawien
            'MC': (0, 9),  # Monaco
            # 'ME': (0, 0),  # Montenegro
            'NL': (0, 8),  # Netherlands
            # 'NO': (0, 0),  # Norwegen
            'AT': (0, 9),  # Austria
            'PK': (0, 8),  # Pakistan
            'PS': (0, 8),  # Palästina
            'PL': (0, 12),  # Poland
            'PT': (0, 8),  # Portugal
            'RO': (0, 8),  # Romania
            # 'LC': (0, 0),  # Saint Lucia
            'SM': (0, 9),  # San Marino
            # 'ST': (0, 0),  # Sao Tome und Principe
            'SA': (0, 6),  # Saudi-Arabien
            # 'SE': (0, 0),  # Sweden
            'CH': (0, 9),  # Swiss
            'RS': (0, 7),  # Serbia
            # 'SC': (0, 0),  # Seychellen
            'SK': (0, 8),  # Slovakia
            'SI': (0, 9),  # Slovenia
            'ES': (0, 8),  # Spain
            # 'TL': (0, 0),  # Timor-Leste
            'TR': (0, 9),  # Türkei
            'CZ': (0, 8),  # Czech
            'TN': (0, 6),  # Tunisia
            'UA': (0, 10),  # Ukraine
            'HU': (0, 7),  # Hungary
            'AE': (0, 7),  # United Arabic Emirates
            'BY': (0, 8),  # Weissrussland
            'CY': (0, 7),  # Cypher
        }

        structure_elements, positions, found_element = 0, [], ""

        code = data[:2]
        start, end = iban_structures.get(code, (0, 5))

        for element in range(end):
            if data[element] == ' ' or data[element] == '-':
                structure_elements += 1
                positions.append(element)
                found_element = data[element]

        final_iban = data[start:(end + structure_elements)]
        for index in range(len(final_iban), len(data), 1):
            if data[index] == found_element:
                final_iban += found_element
            else:
                final_iban += choices('1234567890')[0]
        return final_iban

    @staticmethod
    def anonymize_by_replacing(data):
        """
            Transaction Number,
            Credit Card Number,
            Customer Number,
            Employee Number
        """
        length, transaction_num = len(str(data)), ""
        valid_chars, valid_nums, valid_special_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '1234567890', ".-:,;() "
        actual_data = str(data)
        for index in range(length):
            if actual_data[index] in valid_chars:
                transaction_num += choices(valid_chars)[0]
            elif actual_data[index] in valid_special_chars:
                transaction_num += actual_data[index]
            else:
                transaction_num += choices(valid_nums)[0]

        return transaction_num

    @staticmethod
    def anonymize_company(data):
        """
            Supplier,
            Company,
            Shipping company etc.
        """
        company_identifier = [
            "GmbH & Co. KG",
            "GmbH & Co. OHG",
            "GmbH & Co. KGaA",
            "Group",
            "GmbH",
            "Söhne",
            "Sons",
            "KGaA",
            "OHG",
            "e.K.",
            "eG",
            "KG",
            "Kommanditgesellschaft",
            "SE",
            "KGaA",
            "KGaA & Co.",
            "LLP",
            "PLC",
            "Co.",
            "Co",
            "Corp.",
            "Ltda.",
            "Pty. Ltd.",
            "SARL",
            "SAS",
            "SA",
            "BV",
            "NV"
        ]
        for element in range(len(company_identifier)):
            if company_identifier[element] in data:
                anonymized = Faker().company()
                return anonymized
