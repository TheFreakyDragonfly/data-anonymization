from pathlib import Path
from anonymizer import start_anonymization
from ExtensionHelper import ext_print


def take_order():
    """
    Function that begins the anonymization process by trying to read 'order.order'.
    :return: No return.
    """
    # Order is expected to be at top level
    path_to_order = Path(__file__).resolve().parent.parent.parent / "order.order"

    # set empty variables
    cs = ''  # removed
    server = ''  # removed
    database = ''  # removed
    username = ''  # removed
    password = ''  # removed
    trust = False

    # get content of variables and list of tables from order.order
    with open(path_to_order) as orderFile:
        # get all the lines in the file
        lines = [line.strip() for line in orderFile]

        # begin checking correct format and extract values
        if lines[0] != "[AnonymizationOrder]":
            raise ValueError("Not an order!")

        if lines[1] == "[Connection Config]":
            if lines[2][0:7] == "server=":
                server = lines[2][7:]
            else:
                raise ValueError("No server provided!")
            if lines[3][0:9] == "database=":
                database = lines[3][9:]
            else:
                raise ValueError("No database provided!")
            if lines[4][0:9] == "username=":
                username = lines[4][9:]
            else:
                raise ValueError("No username provided!")
            if lines[5][0:9] == "password=":
                password = lines[5][9:]
            else:
                raise ValueError("No password provided!")
            if lines[6][0:10] == "trust=true":
                trust = True
        elif lines[1] == "[Connection CS]":
            if lines[2][0:3] == "cs=":
                cs = lines[2][3:]
            else:
                raise ValueError("No cs provided!")
        else:
            raise ValueError("No Config or connection string provided!")

        if lines[1] == "[Connection CS]":
            next_line_index = 3
        else:
            next_line_index = 7
        if lines[next_line_index] != "[Limit]":
            raise ValueError("No limit info provided!")
        if lines[next_line_index+1][0:4] == "lim=":
            limit = int(lines[next_line_index+1][4:])
        if lines[next_line_index+2] != "[Mode]":
            raise ValueError("No mode info provided!")
        if lines[next_line_index+3][0:4] == "mod=":
            mode = lines[next_line_index + 3][4:]
        if lines[next_line_index+4] != "[Tables]":
            raise ValueError("No tables provided!")

        tables = []
        for table_name in range(next_line_index + 5, len(lines)):
            tables.append(lines[table_name])

    # call actual anonymization
    if mode != "level1":
        raise NotImplementedError()
    try:
        start_anonymization(cs, server, database, username, password, trust, tables, limit)
    except Exception as e:
        ext_print(str(e))
        raise e


# Main for debugging and testing only
# usually only called from the VSCode extension
if __name__ == "__main__":
    take_order()
