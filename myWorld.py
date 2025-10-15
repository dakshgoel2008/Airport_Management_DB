import os
from dotenv import load_dotenv
from core import *

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def myWorld():
    user = DB_USER
    password = DB_PASSWORD
    schema_path = "./sql/airport_management_schema.sql"
    data_path = "./sql/airport_management_data.sql"

    # no need to import the database again and again unless any changes.
    if input("Import schema and data? (y/n): ").lower() == 'y':
        import_sql_files(user, password, schema_path, data_path)

    while True:
        try: 
            connection = get_connection(user, password, "AIRPORT_MANAGEMENT_DB")
            print("Connected to db successfully.....")
            input("\nPress Enter to Continue.......\n")

            with connection.cursor() as cursor:
                main_controller(cursor)

            connection.close()
            break

        except Exception as e:
            print(f"Error: {e}")
            if input("Try again? (y/n): ").lower() != 'y':
                break

if __name__ == "__main__":
    myWorld()