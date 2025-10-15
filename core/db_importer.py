import os
import pymysql
from core.db_connection import get_connection

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
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
    for stmt in statements:
        try:
            cursor.execute(stmt)
        except Exception as e:
            print(f"Warning: {e}")