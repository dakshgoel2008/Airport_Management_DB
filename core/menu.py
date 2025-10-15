def main_menu():
    print("#" * 50)
    print("AIRPORT MANAGEMENT SYSTEM")
    print("#" * 50)
    print("Choose operation type:")
    print("1. View")
    print("2. Insert")
    print("3. Update")
    print("4. Delete")
    print("5. Search")
    print("6. Reports")
    print("1000. Exit")
    return input("Enter your choice: ").strip()


def view_menu():
    print("\n-- VIEW MENU --")
    print("1. View all airports available")
    print("2. View all upcoming flights")
    print("3. View passenger list of a particular flight")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()


def insert_menu():
    print("\n-- INSERT MENU --")
    print("1. Add new airport")
    print("2. Add new flight")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()


def update_menu():
    print("\n-- UPDATE MENU --")
    print("1. Update airport details")
    print("2. Update flight schedule")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()


def delete_menu():
    print("\n-- DELETE MENU --")
    print("1. Delete an airport")
    print("2. Delete a flight")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()


def search_menu():
    print("\n-- SEARCH MENU --")
    print("1. Search flight by ID")
    print("2. Search passenger by name")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()


def reports_menu():
    print("\n-- REPORTS MENU --")
    print("1. Daily Flight Report")
    print("2. Passenger Summary")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()