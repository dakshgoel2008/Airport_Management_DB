from decimal import Decimal
def view_flight_crew(cursor):
    """Display crew members for a specific flight"""
    print("\n" + "="*80)
    print("VIEW FLIGHT CREW")
    print("="*80)
    
    flight_number = input("Flight Number: ").strip().upper()
    flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
    
    query = """
        SELECT e.first_name, e.last_name, fc.role
        FROM flight_crew fc
        JOIN crew_member cm ON fc.crew_id = cm.crew_id
        JOIN employee e ON cm.employee_id = e.employee_id
        WHERE fc.flight_number = %s AND fc.flight_date = %s
        ORDER BY 
            CASE fc.role
                WHEN 'Captain' THEN 1
                WHEN 'First Officer' THEN 2
                WHEN 'Flight Attendant' THEN 3
                ELSE 4
            END
    """
    
    cursor.execute(query, (flight_number, flight_date))
    res = cursor.fetchall()
    
    print("\n" + "-"*80)
    if res:
        print(f"CREW ROSTER - Flight {flight_number} on {flight_date}")
        print("-"*80)
        for i, row in enumerate(res, 1):
            print(f"{i:2d}. {row['first_name']} {row['last_name']:<20} [{row['role']}]")
        print("-"*80)
        print(f"Total Crew Members: {len(res)}")
    else:
        print(f"No crew assigned to Flight {flight_number} on {flight_date}")
    print("-"*80 + "\n")


def search_employee(cursor):
    """Search for an employee by ID"""
    print("\n" + "="*80)
    print("EMPLOYEE SEARCH")
    print("="*80)
    
    employee_id = input("Employee ID: ").strip().upper()
    
    query = """
        SELECT 
            e.*,
            COALESCE(a.city, al.name) AS work_location,
            YEAR(CURDATE()) - YEAR(e.hire_date) AS years_service
        FROM employee e
        LEFT JOIN airport a ON e.airport_code = a.airport_code
        LEFT JOIN airline al ON e.airline_id = al.airline_id
        WHERE e.employee_id = %s
    """
    
    cursor.execute(query, (employee_id,))
    res = cursor.fetchone()
    
    print("\n" + "-"*80)
    if res:
        print("EMPLOYEE DETAILS")
        print("-"*80)
        print(f"ID:           {res['employee_id']}")
        print(f"Name:         {res['first_name']} {res['last_name']}")
        print(f"Position:     {res['position']}")
        print(f"Department:   {res['department']}")
        print(f"Location:     {res['work_location']}")
        print(f"Email:        {res['email']}")
        print(f"Phone:        {res['phone']}")
        print(f"Hire Date:    {res['hire_date']} ({res['years_service']} years)")
        print(f"Salary:       ${res['salary']:,.2f}")
        print(f"Status:       {res['status']}")
    else:
        print(f"Employee ID '{employee_id}' not found")
    print("-"*80 + "\n")


def fire_employee(cursor):
    """Terminate an employee with detailed validation and confirmation"""
    print("\n" + "="*80)
    print("EMPLOYEE TERMINATION")
    print("="*80)
    
    employee_id = input("Employee ID: ").strip().upper()
    
    # Get comprehensive employee details
    query = """
        SELECT 
            e.*,
            COALESCE(a.city, al.country) AS work_location,
            DATEDIFF(CURDATE(), e.hire_date) AS days_employed,
            YEAR(CURDATE()) - YEAR(e.hire_date) AS years_service,
            (SELECT COUNT(*) FROM employee 
             WHERE supervisor_id = e.employee_id AND status = 'Active') AS direct_reports
        FROM employee e
        LEFT JOIN airport a ON e.airport_code = a.airport_code
        LEFT JOIN airline al ON e.airline_id = al.airline_id
        WHERE e.employee_id = %s
    """
    
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    
    if not employee:
        print(f"\nEmployee '{employee_id}' not found.\n")
        return
    
    if employee['status'] == 'Terminated':
        print(f"\nEmployee {employee_id} was already terminated.\n")
        return
    
    # Display employee summary
    print("\n" + "-"*80)
    print("EMPLOYEE INFORMATION")
    print("-"*80)
    print(f"ID:           {employee['employee_id']}")
    print(f"Name:         {employee['first_name']} {employee['last_name']}")
    print(f"Position:     {employee['position']}")
    print(f"Department:   {employee['department']}")
    print(f"Location:     {employee['work_location']}")
    print(f"Hire Date:    {employee['hire_date']}")
    print(f"Service:      {employee['years_service']} years ({employee['days_employed']} days)")
    print(f"Salary:       ${employee['salary']:,.2f}")
    print(f"Status:       {employee['status']}")
    
    # Check for supervisor
    if employee['supervisor_id']:
        cursor.execute(
            "SELECT first_name, last_name FROM employee WHERE employee_id = %s",
            (employee['supervisor_id'],)
        )
        supervisor = cursor.fetchone()
        if supervisor:
            print(f"Supervisor:   {supervisor['first_name']} {supervisor['last_name']}")
    
    # Check special conditions
    warnings = []
    
    cursor.execute(
        "SELECT crew_id, crew_type FROM crew_member WHERE employee_id = %s",
        (employee_id,)
    )
    crew = cursor.fetchone()
    if crew:
        warnings.append(f"Crew Member ({crew['crew_type']}) - affects flight assignments")
    
    if employee['direct_reports'] > 0:
        warnings.append(f"Supervises {employee['direct_reports']} employee(s) - reassignment required")
    
    critical_positions = ['Captain', 'Air Traffic Controller', 'Airport Manager', 'Chief Pilot']
    if employee['position'] in critical_positions:
        warnings.append(f"Critical position ({employee['position']}) - immediate replacement needed")
    
    if warnings:
        print("-"*80)
        print("WARNINGS:")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    # Termination reason
    print("-"*80)
    print("\nTERMINATION REASON:")
    print("  1. Resignation")
    print("  2. Retirement")
    print("  3. Performance Issues")
    print("  4. Misconduct")
    print("  5. Position Elimination")
    print("  6. Contract Completion")
    print("  7. Other")
    
    reason_choice = input("\nSelect reason (1-7): ").strip()
    reasons = {
        '1': 'Resignation',
        '2': 'Retirement',
        '3': 'Performance Issues',
        '4': 'Misconduct',
        '5': 'Position Elimination',
        '6': 'Contract Completion',
    }
    
    if reason_choice == '7':
        reason = input("Enter reason: ").strip()
    else:
        reason = reasons.get(reason_choice, 'Unspecified')
    
    # Final confirmation
    print("\n" + "="*80)
    print("CONFIRM TERMINATION")
    print("="*80)
    print(f"Employee:  {employee['first_name']} {employee['last_name']} ({employee_id})")
    print(f"Position:  {employee['position']}")
    print(f"Reason:    {reason}")
    print("="*80)
    
    confirm = input("\nType 'CONFIRM' to proceed or press Enter to cancel: ").strip().upper()
    
    if confirm != 'CONFIRM':
        print("\nTermination cancelled.\n")
        return
    
    try:
        cursor.execute(
            "UPDATE employee SET status = 'Terminated' WHERE employee_id = %s",
            (employee_id,)
        )
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("TERMINATION COMPLETED")
        print("="*80)
        print(f"Employee:     {employee['first_name']} {employee['last_name']}")
        print(f"ID:           {employee_id}")
        print(f"Position:     {employee['position']}")
        print(f"Service:      {employee['years_service']} years")
        print(f"Final Salary: ${employee['salary']:,.2f}")
        print(f"Reason:       {reason}")
        print("-"*80)
        print("REQUIRED ACTIONS:")
        print("  - Process final paycheck and benefits")
        print("  - Collect company property")
        print("  - Revoke system access")
        if employee['direct_reports'] > 0:
            print(f"  - Reassign {employee['direct_reports']} direct report(s)")
        if crew:
            print("  - Update crew scheduling")
            print("  - Reassign flight duties")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to terminate employee. {e}\n")


def add_new_employee(cursor):
    """Add a new employee to the database"""
    print("\n" + "="*80)
    print("ADD NEW EMPLOYEE")
    print("="*80)
    
    try:
        # Basic information
        employee_id = input("\nEmployee ID (e.g., EMP019): ").strip().upper()
        
        # Check if ID already exists
        cursor.execute("SELECT employee_id FROM employee WHERE employee_id = %s", (employee_id,))
        if cursor.fetchone():
            print(f"\nError: Employee ID '{employee_id}' already exists.\n")
            return
        
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        date_of_birth = input("Date of Birth (YYYY-MM-DD): ").strip()
        hire_date = input("Hire Date (YYYY-MM-DD): ").strip()
        
        # Employment type
        print("\n" + "-"*80)
        print("EMPLOYMENT TYPE:")
        print("  1. Airport Employee")
        print("  2. Airline Employee")
        emp_type = input("\nSelect (1 or 2): ").strip()
        
        airport_code = None
        airline_id = None
        
        if emp_type == '1':
            cursor.execute("SELECT airport_code, name, city FROM airport ORDER BY name")
            airports = cursor.fetchall()
            print("\n" + "-"*80)
            print("AVAILABLE AIRPORTS:")
            print("-"*80)
            for ap in airports:
                print(f"  {ap['airport_code']:<6} {ap['name']:<40} ({ap['city']})")
            print("-"*80)
            airport_code = input("Airport Code: ").strip().upper()
        else:
            cursor.execute("SELECT airline_id, name FROM airline WHERE status = 'Active' ORDER BY name")
            airlines = cursor.fetchall()
            print("\n" + "-"*80)
            print("AVAILABLE AIRLINES:")
            print("-"*80)
            for al in airlines:
                print(f"  {al['airline_id']:<6} {al['name']}")
            print("-"*80)
            airline_id = input("Airline ID: ").strip().upper()
        
        # Position details
        print("\n" + "-"*80)
        department = input("Department: ").strip()
        position = input("Position: ").strip()
        
        while True:
            try:
                salary = float(input("Annual Salary: $").strip().replace(',', ''))
                if salary < 0:
                    print("Salary must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Enter numbers only.")
        
        supervisor_id = input("Supervisor ID (optional, press Enter to skip): ").strip().upper()
        if not supervisor_id:
            supervisor_id = None
        elif supervisor_id:
            # Validate supervisor exists
            cursor.execute("SELECT employee_id FROM employee WHERE employee_id = %s", (supervisor_id,))
            if not cursor.fetchone():
                print(f"Warning: Supervisor ID '{supervisor_id}' not found. Proceeding without supervisor.")
                supervisor_id = None
        
        # Summary and confirmation
        print("\n" + "="*80)
        print("CONFIRM NEW EMPLOYEE")
        print("="*80)
        print(f"ID:           {employee_id}")
        print(f"Name:         {first_name} {last_name}")
        print(f"Email:        {email}")
        print(f"Phone:        {phone}")
        print(f"DOB:          {date_of_birth}")
        print(f"Hire Date:    {hire_date}")
        print(f"Location:     {airport_code or airline_id}")
        print(f"Department:   {department}")
        print(f"Position:     {position}")
        print(f"Salary:       ${salary:,.2f}")
        print(f"Supervisor:   {supervisor_id or 'None'}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to add employee or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nEmployee addition cancelled.\n")
            return
        
        query = """
            INSERT INTO employee (
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
        
        print("\n" + "="*80)
        print(f"SUCCESS: Employee {employee_id} added successfully")
        print("="*80 + "\n")
        
    except ValueError as e:
        print(f"\nError: Invalid input format. {e}\n")
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to add employee. {e}\n")


def update_salaries_by_position(cursor):
    """Update salary for all employees in a specific position"""
    print("\n" + "="*80)
    print("UPDATE SALARIES BY POSITION")
    print("="*80)
    
    try:
        # Get all unique positions with employee counts
        cursor.execute("""
            SELECT position, COUNT(*) as count, AVG(salary) as avg_salary
            FROM employee
            WHERE status = 'Active'
            GROUP BY position
            ORDER BY position
        """)
        positions = cursor.fetchall()
        
        if not positions:
            print("\nNo active employees found.\n")
            return
        
        # Display positions
        print("\nAVAILABLE POSITIONS:")
        print("-"*80)
        print(f"{'#':<4} {'Position':<35} {'Employees':<12} {'Current Avg Salary'}")
        print("-"*80)
        for i, pos in enumerate(positions, 1):
            print(f"{i:<4} {pos['position']:<35} {pos['count']:<12} ${pos['avg_salary']:,.2f}")
        print("-"*80)
        
        # Get user selection
        while True:
            try:
                choice = int(input(f"\nSelect position (1-{len(positions)}): ").strip())
                if 1 <= choice <= len(positions):
                    break
                print(f"Please enter a number between 1 and {len(positions)}")
            except ValueError:
                print("Please enter a valid number")
        
        selected = positions[choice - 1]
        position_name = selected['position']
        employee_count = selected['count']
        current_avg = selected['avg_salary']
        
        # Display current details
        print("\n" + "="*80)
        print("POSITION SALARY UPDATE")
        print("="*80)
        print(f"Position:         {position_name}")
        print(f"Affected Employees: {employee_count}")
        print(f"Current Avg Salary: ${current_avg:,.2f}")
        print("-"*80)
        
        # Get new salary
        while True:
            try:
                new_salary = Decimal(input("New Salary: $").strip().replace(',', ''))
                if new_salary < 0:
                    print("Salary must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Enter numbers only.")
        
        # Calculate change
        change_percent = ((new_salary - current_avg) / current_avg) * 100 if current_avg > 0 else 0
        change_type = "increase" if change_percent > 0 else "decrease"
        
        print("-"*80)
        print(f"New Salary:       ${new_salary:,.2f}")
        print(f"Change:           {abs(change_percent):.1f}% {change_type}")
        print("="*80)
        
        # Confirmation
        confirm = input(f"\nType 'CONFIRM' to update {employee_count} employee(s) or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nSalary update cancelled.\n")
            return
        
        # Execute update
        cursor.execute(
            "UPDATE employee SET salary = %s WHERE position = %s AND status = 'Active'",
            (new_salary, position_name)
        )
        cursor.connection.commit()
        
        rows_updated = cursor.rowcount
        
        # Show results
        print("\n" + "="*80)
        print("UPDATE COMPLETED")
        print("="*80)
        print(f"Position:         {position_name}")
        print(f"Employees Updated: {rows_updated}")
        print(f"New Salary:       ${new_salary:,.2f}")
        print(f"Previous Avg:     ${current_avg:,.2f}")
        print(f"Change:           {abs(change_percent):.1f}% {change_type}")
        print("="*80 + "\n")
        
    except ValueError:
        print("\nError: Invalid input.\n")
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to update salaries. {e}\n")