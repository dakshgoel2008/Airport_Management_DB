import os
import pymysql
import re

def import_sql_files(user: str, password: str, schema_path: str, data_path: str):
    if not os.path.isfile(schema_path) or not os.path.isfile(data_path):
        raise FileNotFoundError(f"Missing SQL files:\n  {schema_path}\n  {data_path}")

    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

    with connection.cursor() as cursor:
        print("Importing schema...")
        execute_sql_file(cursor, schema_path)
        print("Importing data...")
        execute_sql_file(cursor, data_path)
    
    connection.close()
    print("✓ Database setup complete!")

def execute_sql_file(cursor, file_path):
    """
    Executes an SQL file, correctly handling DELIMITER commands.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_file = f.read()

    # Split the file by the DELIMITER command
    commands = re.split(r'DELIMITER\s*\S+', sql_file)
    delimiters = re.findall(r'DELIMITER\s*(\S+)', sql_file)
    delimiters.insert(0, ';') # The default delimiter is a semicolon

    for i, command_block in enumerate(commands):
        # Split each block by its specific delimiter
        statements = command_block.split(delimiters[i])
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f"Warning: {e}")