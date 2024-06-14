from pathlib import Path
import os
import sys

root_dir = Path(__file__).resolve().parent.parent
file_path = root_dir / "order"

# Section to read the contents of the order
tables = []
with open(file_path) as file:
    lines = [line.rstrip() for line in file]
    if lines[0] != "[Anonymization Order]":
        raise ValueError("Not an anonymization order")
    if lines[1] != "[Config]":
        raise ValueError("No Config given")

    user = lines[2]
    password = lines[3]
    server = lines[4]
    database = lines[5]

    if lines[6] != "[TABLES]":
        raise ValueError("No Config given")

    for table_name in range(7, len(lines)):
        tables.append(lines[table_name])

# output read values for checking functionality
output = ' '.join((user, password, server, database)) + '\n' + '\n'.join(tables)
f = open(root_dir / "output.txt", "w")
f.write(output)
f.close()

# "consume" order after processing
os.remove(file_path)
