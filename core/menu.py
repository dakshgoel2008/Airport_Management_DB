def main_menu():
    print("#" * 50)
    print("AIRPORT MANAGEMENT SYSTEM")
    print("#" * 50)
    print("Choose operation type:")
    print("1. View")
    print("2. Insert")
    print("3. Update")
    print("4. Delete / Cancel")
    print("5. Search")
    print("6. Reports")
    print("1000. Exit")
    return input("Enter your choice: ").strip()

def view_menu():
    print("\n-- VIEW / SEARCH MENU --")
    print("1. View all Upcoming Flights")
    print("2. View Passenger Details of a Flight")
    print("3. View Crew Members of a Flight")
    print("4. View Booking details")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()

def insert_menu():
    print("\n-- INSERT MENU --")
    print("1. Insert a New Ticket")
    print("2. Insert a New Flight")
    print("3. Insert a New Employee")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()

def update_menu():
    print("\n-- UPDATE MENU --")
    print("1. Update Flight Status")
    print("2. Update Salaries by Position")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()

def delete_menu():
    print("\n-- DELETE / CANCEL MENU --")
    print("1. Fire an Employee")
    print("2. Cancel a Passenger's Ticket")
    print("3. Cancel a Flight")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()

def search_menu(): 
    print("\n-- SEARCH MENU --")
    print("1. Search Flight by ID")
    print("2. Search Passenger by Name")
    print("3. Search for an Employee's Details")
    print("4. Search for cheapest flights for your route")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()

def reports_menu():
    print("\n-- REPORTS MENU --")
    print("1. Get Flight Duration")
    print("2. Occupancy vs. Price Report")
    print("3. Average Ticket Price on a Route")
    print("4. Generate Flight Revenue report")
    print("5. View Flight Status Change Log")
    print("100. Back to Main Menu")
    return input("Enter your choice: ").strip()