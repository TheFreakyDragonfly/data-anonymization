import pyodbc
import re
import hashlib

# Define the connection string
server = 'sqls-dataanon-dev-001.database.windows.net'
database = 'Northwind'
username = 'data-anon'
password = 'Lantanio13891!'

driver = '{ODBC Driver 18 for SQL Server}'

# Establish the connection
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection_string)

# Identify columns that potentially contain PII using regex patterns
def identify_pii_columns(column_names):
    pii_patterns = [
        re.compile(r'name', re.IGNORECASE),
        re.compile(r'address', re.IGNORECASE),
        re.compile(r'phone', re.IGNORECASE),
        re.compile(r'email', re.IGNORECASE),
        re.compile(r'contact', re.IGNORECASE),
        re.compile(r'title', re.IGNORECASE)
    ]
    pii_columns = [col for col in column_names if any(pattern.search(col) for pattern in pii_patterns)]
    return pii_columns

# Hash function for anonymizing data
def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Masking function for anonymizing data
def mask_value(value, mask_char='X'):
    return mask_char * len(value)

# Generalize address by only showing the city and country
def generalize_address(value):
    parts = value.split(',')
    if len(parts) > 1:
        return parts[-2].strip() + ', ' + parts[-1].strip()
    return value

# Replace phone number with a pattern
def anonymize_phone(value):
    return 'XXX-XXX-XXXX'

# Generalize title
def generalize_title(value):
    return 'Employee'

# Function to anonymize data based on column type
def anonymize_data(rows, column_names, pii_columns):
    anonymized_rows = []
    for row in rows:
        anonymized_row = []
        for i, value in enumerate(row):
            column_name = column_names[i]
            if column_name in pii_columns:
                if 'name' in column_name.lower():
                    anonymized_row.append(mask_value(value))
                elif 'email' in column_name.lower():
                    anonymized_row.append(hash_value(value))
                elif 'address' in column_name.lower():
                    anonymized_row.append(generalize_address(value))
                elif 'phone' in column_name.lower():
                    anonymized_row.append(anonymize_phone(value))
                elif 'title' in column_name.lower():
                    anonymized_row.append(generalize_title(value))
                elif isinstance(value, (int, float)):
                    anonymized_row.append(0)
                else:
                    anonymized_row.append(value)
            else:
                anonymized_row.append(value)
        anonymized_rows.append(anonymized_row)
    return anonymized_rows

def get_tables(cursor):
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    return cursor.fetchall()

def get_columns(cursor, table_name):
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    return cursor.fetchall()

def get_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

def main():
    # Create a cursor object using the connection
    cursor = conn.cursor()

    # Fetch and display the list of tables
    tables = get_tables(cursor)
    print("List of tables:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table.TABLE_NAME}")

    # Ask the user to select a table
    table_index = int(input("Select a table by number: ")) - 1
    selected_table = tables[table_index].TABLE_NAME

    # Fetch and display the list of columns for the selected table
    columns = get_columns(cursor, selected_table)
    column_names = [column.COLUMN_NAME for column in columns]
    print(f"\nList of columns in table '{selected_table}':")
    for column_name in column_names:
        print(column_name)

    # Identify PII columns
    pii_columns = identify_pii_columns(column_names)
    print(f"\nIdentified PII columns in table '{selected_table}': {pii_columns}")

    # Fetch and display all data from the selected table
    rows = get_table_data(cursor, selected_table)
    print(f"\nData in table '{selected_table}':")

    # Print the column names as the header
    print(", ".join(column_names))

    # Print all the rows
    for row in rows:
        print(", ".join(str(value) for value in row))

    # Print out the columns that are being anonymized
    print(f"\nColumns being anonymized: {pii_columns}")

    # Anonymize the data
    anonymized_rows = anonymize_data(rows, column_names, pii_columns)
    print(f"\nAnonymized data in table '{selected_table}':")
    for row in anonymized_rows:
        print(", ".join(str(value) for value in row))

    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
