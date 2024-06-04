import pyodbc

# Define the connection string
server = 'sqls-dataanon-dev-001.database.windows.net'
database = 'Northwind'  # Replace with your actual database name
username = 'data-anon'
password = 'Lantanio13891!'

# Make sure to use the correct driver name here
driver = '{ODBC Driver 18 for SQL Server}'

# Establish the connection
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection_string)

# Create a cursor object using the connection
cursor = conn.cursor()

# Fetch and display the list of tables
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = cursor.fetchall()

print("List of tables:")
for i, table in enumerate(tables, start=1):
    print(f"{i}. {table.TABLE_NAME}")

# Ask the user to select a table
table_index = int(input("Select a table by number: ")) - 1
selected_table = tables[table_index].TABLE_NAME

# Fetch and display the list of columns for the selected table
cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}'")
columns = cursor.fetchall()

print(f"\nList of columns in table '{selected_table}':")
column_names = [column.COLUMN_NAME for column in columns]
for column_name in column_names:
    print(column_name)

# Fetch and display all data from the selected table
cursor.execute(f"SELECT * FROM {selected_table}")
rows = cursor.fetchall()

print(f"\nData in table '{selected_table}':")

# Print the column names as the header
print(", ".join(column_names))

# Print all the rows
for row in rows:
    print(", ".join(str(value) for value in row))




# Close the cursor and connection
cursor.close()
conn.close()
