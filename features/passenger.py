def view_passenger_list(cursor):
    """Display passenger manifest for a specific flight"""
    print("\n" + "="*80)
    print("FLIGHT PASSENGER MANIFEST")
    print("="*80)
    
    flight_number = input("\nFlight Number: ").strip().upper()
    flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
    
    try:
        # Get flight details first
        cursor.execute("""
            SELECT f.source_airport, f.destination_airport, f.status,
                   al.name AS airline_name, al.iata_code
            FROM flight f
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE f.flight_number = %s AND f.flight_date = %s
        """, (flight_number, flight_date))
        
        flight = cursor.fetchone()
        
        if not flight:
            print(f"\nFlight {flight_number} on {flight_date} not found.\n")
            return
        
        # Get passenger list
        query = """
            SELECT 
                p.passenger_id, p.first_name, p.last_name, p.nationality,
                t.seat_number, t.class, t.check_in_status, t.ticket_status,
                t.fare_amount
            FROM passenger p
            JOIN ticket t ON p.passenger_id = t.passenger_id
            WHERE t.flight_number = %s AND t.flight_date = %s
            ORDER BY 
                CASE t.class
                    WHEN 'First' THEN 1
                    WHEN 'Business' THEN 2
                    WHEN 'Premium Economy' THEN 3
                    WHEN 'Economy' THEN 4
                    ELSE 5
                END,
                t.seat_number
        """
        
        cursor.execute(query, (flight_number, flight_date))
        res = cursor.fetchall()
        
        # Display results
        print("\n" + "-"*80)
        flight_code = f"{flight['iata_code']}{flight_number}"
        print(f"FLIGHT: {flight_code} | {flight['source_airport']} → {flight['destination_airport']}")
        print(f"DATE: {flight_date} | STATUS: {flight['status']}")
        print("-"*80)
        
        if res:
            # Count by class and check-in status
            class_count = {}
            checked_in = 0
            
            for row in res:
                class_count[row['class']] = class_count.get(row['class'], 0) + 1
                if row['check_in_status'] == 'Checked In':
                    checked_in += 1
            
            print(f"TOTAL PASSENGERS: {len(res)} | CHECKED IN: {checked_in}")
            print("-"*80)
            print(f"{'Seat':<6} {'Passenger':<30} {'Nationality':<15} {'Class':<15} {'Status'}")
            print("-"*80)
            
            current_class = None
            for row in res:
                # Add separator between classes
                if current_class != row['class']:
                    if current_class is not None:
                        print("-"*80)
                    current_class = row['class']
                
                name = f"{row['first_name']} {row['last_name']}"
                seat = row['seat_number'] or 'N/A'
                check_in = 'Checked In' if row['check_in_status'] == 'Checked In' else 'Pending'
                
                print(f"{seat:<6} {name:<30} {row['nationality']:<15} {row['class']:<15} {check_in}")
            
            print("-"*80)
            print("\nCLASS BREAKDOWN:")
            for cls, count in sorted(class_count.items()):
                print(f"  {cls}: {count} passenger(s)")
            print("-"*80 + "\n")
        else:
            print("No passengers booked on this flight")
            print("-"*80 + "\n")
            
    except Exception as e:
        print(f"\nError: Unable to retrieve passenger list. {e}\n")


def search_passenger_by_name(cursor):
    """Search for passengers by name"""
    print("\n" + "="*80)
    print("PASSENGER SEARCH")
    print("="*80)
    print("\nTip: You can search using partial names (e.g., 'John' or 'Sm')")
    
    search_term = input("\nPassenger Name (first or last): ").strip()
    
    if not search_term:
        print("\nSearch term cannot be empty.\n")
        return
    
    try:
        query = """
            SELECT 
                p.passenger_id, p.first_name, p.last_name,
                p.email, p.phone, p.nationality,
                p.passport_number, p.passport_expiry,
                p.frequent_flyer_number, p.date_of_birth,
                COUNT(DISTINCT t.ticket_id) AS total_bookings,
                COUNT(DISTINCT CASE WHEN t.ticket_status = 'Active' THEN t.ticket_id END) AS active_bookings,
                MAX(t.flight_date) AS last_flight_date
            FROM passenger p
            LEFT JOIN ticket t ON p.passenger_id = t.passenger_id
            WHERE p.first_name LIKE %s OR p.last_name LIKE %s
            GROUP BY p.passenger_id
            ORDER BY p.last_name, p.first_name
            LIMIT 50
        """
        
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, search_pattern))
        results = cursor.fetchall()
        
        if results:
            print("\n" + "-"*80)
            print(f"SEARCH RESULTS: {len(results)} passenger(s) found for '{search_term}'")
            print("-"*80)
            
            for idx, row in enumerate(results, 1):
                print(f"\n{idx}. {row['first_name']} {row['last_name']} (ID: {row['passenger_id']})")
                print(f"   DOB: {row['date_of_birth']} | Nationality: {row['nationality']}")
                
                if row['email'] or row['phone']:
                    contact = []
                    if row['email']:
                        contact.append(f"Email: {row['email']}")
                    if row['phone']:
                        contact.append(f"Phone: {row['phone']}")
                    print(f"   {' | '.join(contact)}")
                
                print(f"   Passport: {row['passport_number']}", end="")
                if row['passport_expiry']:
                    print(f" (Expires: {row['passport_expiry']})", end="")
                print()
                
                if row['frequent_flyer_number']:
                    print(f"   Frequent Flyer: {row['frequent_flyer_number']}")
                
                print(f"   Bookings: {row['total_bookings']} total, {row['active_bookings']} active", end="")
                if row['last_flight_date']:
                    print(f" | Last flight: {row['last_flight_date']}")
                else:
                    print()
                
                if idx < len(results):
                    print("   " + "-"*76)
            
            print("-"*80 + "\n")
        else:
            print(f"\nNo passengers found matching '{search_term}'.\n")
            
    except Exception as e:
        print(f"\nError: Unable to search passengers. {e}\n")


def add_new_passenger(cursor):
    """Add a new passenger to the database"""
    print("\n" + "="*80)
    print("ADD NEW PASSENGER")
    print("="*80)
    
    try:
        # Passenger ID
        passenger_id = input("\nPassenger ID (e.g., PAX013): ").strip().upper()
        
        # Check if ID exists
        cursor.execute("SELECT passenger_id FROM passenger WHERE passenger_id = %s", (passenger_id,))
        if cursor.fetchone():
            print(f"\nError: Passenger ID '{passenger_id}' already exists.\n")
            return
        
        # Personal information
        print("\n" + "-"*80)
        print("PERSONAL INFORMATION")
        print("-"*80)
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        date_of_birth = input("Date of Birth (YYYY-MM-DD): ").strip()
        
        print("\nGender:")
        print("  1. Male")
        print("  2. Female")
        print("  3. Other")
        gender_choice = input("Select (1-3): ").strip()
        gender = {'1': 'M', '2': 'F', '3': 'Other'}.get(gender_choice, 'M')
        
        # Travel documents
        print("\n" + "-"*80)
        print("TRAVEL DOCUMENTS")
        print("-"*80)
        nationality = input("Nationality: ").strip()
        passport_number = input("Passport Number: ").strip().upper()
        passport_expiry = input("Passport Expiry (YYYY-MM-DD): ").strip()
        
        # Validate passport expiry
        cursor.execute("SELECT DATEDIFF(%s, CURDATE()) AS days_until_expiry", (passport_expiry,))
        days_result = cursor.fetchone()
        if days_result and days_result['days_until_expiry'] < 180:
            print("\nWarning: Passport expires in less than 6 months.")
            print("Many countries require at least 6 months validity.")
            confirm = input("Continue anyway? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("\nPassenger registration cancelled.\n")
                return
        
        # Contact information
        print("\n" + "-"*80)
        print("CONTACT INFORMATION (Optional)")
        print("-"*80)
        email = input("Email: ").strip() or None
        phone = input("Phone: ").strip() or None
        
        # Frequent flyer
        print("\n" + "-"*80)
        frequent_flyer = input("Frequent Flyer Number (optional, press Enter to skip): ").strip() or None
        
        # Summary
        print("\n" + "="*80)
        print("CONFIRM NEW PASSENGER")
        print("="*80)
        print(f"ID:           {passenger_id}")
        print(f"Name:         {first_name} {last_name}")
        print(f"DOB:          {date_of_birth}")
        print(f"Gender:       {gender}")
        print(f"Nationality:  {nationality}")
        print(f"Passport:     {passport_number} (Expires: {passport_expiry})")
        if email:
            print(f"Email:        {email}")
        if phone:
            print(f"Phone:        {phone}")
        if frequent_flyer:
            print(f"FF Number:    {frequent_flyer}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to add passenger or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nPassenger registration cancelled.\n")
            return
        
        query = """
            INSERT INTO passenger (
                passenger_id, first_name, last_name, date_of_birth, gender,
                nationality, passport_number, passport_expiry, email, phone,
                frequent_flyer_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            passenger_id, first_name, last_name, date_of_birth, gender,
            nationality, passport_number, passport_expiry,
            email, phone, frequent_flyer
        ))
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print(f"SUCCESS: Passenger {passenger_id} registered successfully")
        print("="*80)
        print(f"Name:     {first_name} {last_name}")
        print(f"Passport: {passport_number}")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to add passenger. {e}\n")


def update_passenger_contact(cursor):
    """Update passenger contact information"""
    print("\n" + "="*80)
    print("UPDATE PASSENGER CONTACT")
    print("="*80)
    
    passenger_id = input("\nPassenger ID: ").strip().upper()
    
    try:
        # Get current passenger details
        cursor.execute("""
            SELECT passenger_id, first_name, last_name, email, phone
            FROM passenger
            WHERE passenger_id = %s
        """, (passenger_id,))
        
        passenger = cursor.fetchone()
        
        if not passenger:
            print(f"\nPassenger '{passenger_id}' not found.\n")
            return
        
        # Display current info
        print("\n" + "-"*80)
        print("CURRENT CONTACT INFORMATION")
        print("-"*80)
        print(f"Passenger:  {passenger['first_name']} {passenger['last_name']}")
        print(f"Email:      {passenger['email'] or 'Not set'}")
        print(f"Phone:      {passenger['phone'] or 'Not set'}")
        print("-"*80)
        
        # Get new contact info
        print("\nNEW CONTACT INFORMATION")
        print("(Press Enter to keep current value)")
        print("-"*80)
        
        new_email = input(f"Email [{passenger['email'] or 'none'}]: ").strip()
        new_phone = input(f"Phone [{passenger['phone'] or 'none'}]: ").strip()
        
        # Use current values if nothing entered
        if not new_email:
            new_email = passenger['email']
        if not new_phone:
            new_phone = passenger['phone']
        
        # Check if anything changed
        if new_email == passenger['email'] and new_phone == passenger['phone']:
            print("\nNo changes made.\n")
            return
        
        # Confirmation
        print("\n" + "="*80)
        print("CONFIRM UPDATE")
        print("="*80)
        print(f"Passenger:  {passenger['first_name']} {passenger['last_name']}")
        print(f"New Email:  {new_email or 'Not set'}")
        print(f"New Phone:  {new_phone or 'Not set'}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to update or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nUpdate cancelled.\n")
            return
        
        # Update database
        cursor.execute("""
            UPDATE passenger
            SET email = %s, phone = %s
            WHERE passenger_id = %s
        """, (new_email, new_phone, passenger_id))
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("CONTACT INFORMATION UPDATED")
        print("="*80)
        print(f"Passenger:  {passenger['first_name']} {passenger['last_name']}")
        print(f"Email:      {new_email or 'Not set'}")
        print(f"Phone:      {new_phone or 'Not set'}")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to update contact information. {e}\n")


def view_passenger_travel_history(cursor):
    """View complete travel history for a passenger"""
    print("\n" + "="*80)
    print("PASSENGER TRAVEL HISTORY")
    print("="*80)
    
    passenger_id = input("\nPassenger ID: ").strip().upper()
    
    try:
        # Get passenger details
        cursor.execute("""
            SELECT passenger_id, first_name, last_name, nationality, 
                   frequent_flyer_number
            FROM passenger
            WHERE passenger_id = %s
        """, (passenger_id,))
        
        passenger = cursor.fetchone()
        
        if not passenger:
            print(f"\nPassenger '{passenger_id}' not found.\n")
            return
        
        # Get travel history
        cursor.execute("""
            SELECT 
                t.ticket_id, t.flight_number, t.flight_date,
                f.source_airport, f.destination_airport,
                f.scheduled_departure, f.status AS flight_status,
                t.class, t.seat_number, t.fare_amount,
                t.ticket_status, t.check_in_status,
                al.name AS airline_name, al.iata_code
            FROM ticket t
            JOIN flight f ON t.flight_number = f.flight_number 
                         AND t.flight_date = f.flight_date
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE t.passenger_id = %s
            ORDER BY f.flight_date DESC, f.scheduled_departure DESC
            LIMIT 50
        """, (passenger_id,))
        
        history = cursor.fetchall()
        
        # Display passenger info
        print("\n" + "-"*80)
        print("PASSENGER DETAILS")
        print("-"*80)
        print(f"ID:          {passenger['passenger_id']}")
        print(f"Name:        {passenger['first_name']} {passenger['last_name']}")
        print(f"Nationality: {passenger['nationality']}")
        if passenger['frequent_flyer_number']:
            print(f"FF Number:   {passenger['frequent_flyer_number']}")
        print("-"*80)
        
        if history:
            # Calculate statistics
            total_spent = sum(row['fare_amount'] for row in history if row['fare_amount'])
            completed_flights = sum(1 for row in history if row['flight_status'] == 'Arrived')
            
            print(f"\nTRAVEL STATISTICS")
            print(f"Total Bookings:     {len(history)}")
            print(f"Completed Flights:  {completed_flights}")
            print(f"Total Spent:        ${total_spent:,.2f}")
            print("-"*80)
            
            print("\nFLIGHT HISTORY")
            print("-"*80)
            
            for i, row in enumerate(history, 1):
                flight_code = f"{row['iata_code']}{row['flight_number']}"
                route = f"{row['source_airport']} → {row['destination_airport']}"
                
                print(f"\n{i}. {flight_code} | {row['flight_date']} | {route}")
                print(f"   Airline: {row['airline_name']}")
                print(f"   Class: {row['class']} | Seat: {row['seat_number'] or 'Not assigned'} | Fare: ${row['fare_amount']:.2f}")
                print(f"   Flight Status: {row['flight_status']} | Ticket: {row['ticket_status']} | Check-in: {row['check_in_status']}")
                
                if i < len(history):
                    print("   " + "-"*76)
            
            print("-"*80 + "\n")
        else:
            print("\nNo travel history found for this passenger.\n")
            
    except Exception as e:
        print(f"\nError: Unable to retrieve travel history. {e}\n")