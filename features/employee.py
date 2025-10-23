def view_flight_crew(cursor):
    """For displaying the crew member of particular flight"""
    flight_number = input("Enter flight number: ")
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    query = """
        select e.first_name, e.last_name, fc.role
        from flight_crew fc
        join crew_member cm on fc.crew_id = cm.crew_id
        join employee e on cm.employee_id = e.employee_id
        where fc.flight_number = %s and fc.flight_date = %s
    """

    cursor.execute(query, (flight_number, flight_date))
    res = cursor.fetchall()

    if res:
        print("\n" + "#"*100)
        print(f"CREW FOR FLIGHT {flight_number} ON {flight_date}")
        print("#"*100)
        for row in res:
            print(f"Name: {row['first_name']} {row['last_name']}, Role: {row['role']}")
        print("#"*100)
    else:
        print("No crew information found for this flight.")

def search_employee(cursor):
    "Search for the employees by their ids"
    employee_id = input("Enter employee ID: ")
    query = """
        select * from employee where employee_id = %s
    """
    cursor.execute(query, (employee_id,))
    res = cursor.fetchone()

    if res:
        print("\n" + "#"*100)
        print("EMPLOYEE DETAILS")
        print("#"*100)
        print(f"Name: {res['first_name']} {res['last_name']}, Position: {res['position']}")
        print("#"*100)
    else:
        print("No employee found with the given ID.")

def fire_employee(cursor):
    """Terminate an employee's contract"""
    employee_id = input("Enter employee ID to terminate: ")
    try:
        query = """
            update employee set status = "Terminated" where employee_id = %s
        """
        cursor.execute(query, (employee_id,))
        if cursor.rowcount > 0:
            cursor.connection.commit()
            print("Employee terminated successfully")       # greedy deletion -> reduces the time complexity.
        else:
            print("No employee found with the given ID.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error: {e}")

def add_new_employee(cursor):
    """Inserts a new employee into the database."""
    try:
        print("\n--- ADD NEW EMPLOYEE ---")
        
        employee_id = input("Enter Employee ID (e.g., EMP019): ").upper()
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        phone = input("Enter Phone: ")
        date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ")
        hire_date = input("Enter Hire Date (YYYY-MM-DD): ")
        
        # Choose employment type
        print("\nEmployment Type:")
        print("1. Airport Employee")
        print("2. Airline Employee")
        emp_type = input("Select (1-2): ")
        
        airport_code = None
        airline_id = None
        
        if emp_type == '1':
            cursor.execute("SELECT airport_code, name, city FROM AIRPORT")
            airports = cursor.fetchall()
            print("\nAvailable Airports:")
            for ap in airports:
                print(f"  {ap['airport_code']}: {ap['name']}, {ap['city']}")
            airport_code = input("Enter Airport Code: ").upper()
        else:
            cursor.execute("SELECT airline_id, name FROM AIRLINE WHERE status = 'Active'")
            airlines = cursor.fetchall()
            print("\nAvailable Airlines:")
            for al in airlines:
                print(f"  {al['airline_id']}: {al['name']}")
            airline_id = input("Enter Airline ID: ").upper()
        
        department = input("Enter Department: ")
        position = input("Enter Position: ")
        salary = float(input("Enter Salary: "))
        
        supervisor_id = input("Enter Supervisor ID (optional): ").upper()
        if not supervisor_id:
            supervisor_id = None
        
        query = """
            INSERT INTO EMPLOYEE (
                employee_id, airport_code, airline_id, first_name, last_name,
                email, phone, date_of_birth, hire_date, department, position,
                salary, status, supervisor_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active', %s)
        """
        
        cursor.execute(query, (
            employee_id, airport_code, airline_id, first_name, last_name,
            email, phone, date_of_birth, hire_date, department, position,
            salary, supervisor_id
        ))
        cursor.connection.commit()
        print(f"\n✓ Employee {employee_id} added successfully!")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error adding employee: {e}")


def update_salaries_by_position(cursor):
    """Updates the salary for all employees with a specific position."""
    try:
        # get all the distinct positions of the employees in the database
        cursor.execute("select distinct position from employee order by position")
        positions = cursor.fetchall()       # all the unique positions

        if not positions:
            print("No employees found in the database.")
            return
        
        # now asking the user to choose a position to update
        print("\nPlease choose a position to update: ")
        for i, pos in enumerate(positions):
            print(f"{i + 1}. {pos['position']}")

        choice = int(input("Enter your choice: "))

        if 0 < choice <= len(positions):
            selected_position = positions[choice - 1]['position']
        else:
            print("Invalid choice.")
            return

        # ---showing the current average salary for better user experience---
        cursor.execute("select avg(salary) as current_salary from employee where position = %s", (selected_position,))
        res = cursor.fetchone()
        current_salary = res['current_salary'] if res['current_salary'] else 0

        print("\n" + "#"*50)
        print(f"Position Selected: {selected_position}")
        print(f"Current Average Salary: ${current_salary:,.2f}")
        print("#"*50)

        # enter the new salary indended to be updated.
        new_salary = float(input(f"Enter the new salary for {selected_position}: "))
        query = "update employee set salary = %s where position = %s"
        cursor.execute(query, (new_salary, selected_position))
        cursor.connection.commit()
        print(f"\nSalaries updated for {cursor.rowcount} employees.")

        # new average salary:
        cursor.execute("select avg(salary) as current_salary from employee where position = %s", (selected_position,))
        res = cursor.fetchone()
        new_average_salary = res['current_salary'] if res['current_salary'] else 0

        print("\n" + "#"*50)
        print(f"Position Selected: {selected_position}")
        print(f"New Average Salary: ${new_average_salary:,.2f}")
        print("#"*50)

    except ValueError:
        print("Invalid input. Please enter a number for the choice and salary.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"An error occurred: {e}")