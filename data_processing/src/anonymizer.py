import pyodbc
import csv
from pathlib import Path
from ExtensionHelper import ext_print
from TableProgress import TableProgress
from function_finder import FunctionFinder
from standalone_anonymization_functions import censor_fully
from configuration import *
import configuration


def config_from_cs(cs):
    config_list = []
    server_start = cs.find('Server=tcp:')
    server_end = cs.find(';', server_start, len(cs))
    server = cs[server_start+11:server_end-5]

    db_start = cs.find('Initial Catalog=')
    db_end = cs.find(';', db_start, len(cs))
    db = cs[db_start+16:db_end]

    user_start = cs.find('User ID=')
    user_end = cs.find(';', user_start, len(cs))
    user = cs[user_start + 8:user_end]

    pw_start = cs.find('Password=')
    pw_end = cs.find(';', pw_start, len(cs))
    pw = cs[pw_start + 9:pw_end]

    trust_start = cs.find('TrustServerCertificate=')
    trust_end = cs.find(';', trust_start, len(cs))
    trust = cs[trust_start + 23:pw_end] == "True"

    config_list.append(server)
    config_list.append(db)
    config_list.append(user)
    config_list.append(pw)
    config_list.append(trust)
    return config_list


def start_anonymization(cs, server, database, username, password, trust, tables, row_cap=0):
    """
    Begins the actual anonymization.
    :param cs: connection string or None.
    :param server: server or None.
    :param database: database or None.
    :param username: username or None.
    :param password: password or None.
    :param trust: TrustServerCertificate.
    :param tables: list of tables.
    :param row_cap: Amount of rows to put out or 0 for all.
    :return: no return.
    """

    # construct other data from cs if necessary and possible
    if cs != '' and server == '':
        extracted_config = config_from_cs(cs)
        server = extracted_config[0]
        database = extracted_config[1]
        username = extracted_config[2]
        password = extracted_config[3]
        trust = extracted_config[4]

    ext_print("Starting Anonymization")

    # use config details to connect
    driver = '{ODBC Driver 18 for SQL Server}'
    if trust:
        odbc_connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'
    else:
        odbc_connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    connection = pyodbc.connect(odbc_connection_string)

    ext_print("Established Connection")

    # get tables from db
    cursor = connection.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")  # WHERE TABLE_TYPE = 'BASE TABLE'
    db_tables = cursor.fetchall()

    ext_print("Fetched Tables")

    # go through tables of db
    progress = TableProgress(len(tables))
    progress.print_progress()
    for table in db_tables:
        # launch anonymization when it matches tables in anonymization order
        if table.TABLE_NAME in tables:
            ext_print('[CurrentTable] ' + table.TABLE_NAME)
            anonymize_table(cursor, table, row_cap, progress)
            progress.increase_progress(share_per_table_after)

    ext_print('[LLMAmt] ' + str(configuration.llm_calls))

    ext_print('[CurrentTable] ...')
    ext_print('[CurrentStep] ...')
    ext_print("Finished all tables")


def anonymize_table(cursor, table, row_cap, progress: TableProgress):
    """
    Anonymizes a given table.
    :param table:
    :param cursor:
    :param row_cap:
    :param progress:
    :return:
    """

    ext_print('Anonymizing "' + table.TABLE_NAME + '"')

    # get column names
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table.TABLE_NAME}'")
    columns = cursor.fetchall()

    # get one dataset
    cursor.execute(f'SELECT TOP 1 * FROM "{table.TABLE_NAME}"')
    row_one = cursor.fetchone()

    # match a function to the column
    # try first using column name, then column content, then using llm
    ext_print('[CurrentStep] Matching Functions')
    progress_step = share_matching / len(columns)
    matching = []
    for column_index, column in enumerate(columns):
        if row_one is None or len(row_one) == 0:  # exit if no data is in table
            return
        ext_print('[CurrentStep] Matching Functions (' + str(column_index+1) + '/' + str(len(columns)) + ')')
        progress.increase_progress(progress_step)
        matched_function = FunctionFinder.match_function_by_regex_name_and_content(column.COLUMN_NAME, row_one[column_index])

        # select matched_function for all values in this column
        matching.append(matched_function)

    ext_print('Determined Matching for "' + table.TABLE_NAME + '"')
    ext_print('[CurrentStep] Getting Full Table')

    # get full table
    cursor.execute(f'SELECT * FROM "{table.TABLE_NAME}"')
    full_table = cursor.fetchall()

    # write non-anonymized to csv
    ext_print('[CurrentStep] Writing non-anonymized')
    path_to_csv = Path(__file__).resolve().parent.parent.parent / (table.TABLE_NAME.replace(" ", "_") + "-non.csv")
    write_to_csv(path_to_csv, columns, full_table, row_cap)
    progress.increase_progress(share_non_anonymized_csv)

    # write anonymized to csv
    ext_print('[CurrentStep] Writing anonymized')
    path_to_csv = Path(__file__).resolve().parent.parent.parent / (table.TABLE_NAME.replace(" ", "_") + ".csv")
    write_to_csv(path_to_csv, columns, full_table, row_cap, True, matching)
    progress.increase_progress(share_anonymized_csv)


def write_to_csv(path_to_csv, columns, full_table, row_cap, anonymize=False, matching=None):
    full_count = len(full_table)
    update_interval = max(100, full_count // 100)  # at most, update every 100 rows
    with open(path_to_csv, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        list_columns = []
        for column in columns:
            list_columns.append(column.COLUMN_NAME)
        spamwriter.writerow(list_columns)
        if row_cap == 0:
            row_cap = len(full_table)
        for i, row in enumerate(full_table[:row_cap]):
            list_content = []
            for index, item in enumerate(row):
                if anonymize:
                    if item is None:
                        anonymized = ""
                    else:
                        try:
                            anonymized = matching[index](item)
                        except Exception:
                            anonymized = censor_fully(item)
                    list_content.append(anonymized)
                else:
                    list_content.append(item)
            spamwriter.writerow(list_content)
            # give updates sometimes
            if i % update_interval == 0 or i == full_count - 1:
                ext_print(str(i+1) + '/' + str(full_count))


# Main for debugging and testing only
if __name__ == "__main__":
    start_anonymization('cs', 'serv', 'db', 'un', 'pw', False, [])
