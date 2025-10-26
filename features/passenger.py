def view_passenger_list(cursor):
    """Displays the list of passengers for a specific flight"""
    flight_number = input("Enter flight number: ").upper()
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    
    query = """
        SELECT P.passenger_id, P.first_name, P.last_name, P.nationality,
               T.seat_number, T.class, T.check_in_status, T.ticket_status
        FROM PASSENGER P
        JOIN TICKET T ON P.passenger_id = T.passenger_id
        WHERE T.flight_number = %s AND T.flight_date = %s
        ORDER BY T.class, T.seat_number
    """
    
    cursor.execute(query, (flight_number, flight_date))
    res = cursor.fetchall()
    
    if res:
        print("\n" + "#"*100)
        print(f"PASSENGER LIST FOR FLIGHT {flight_number} ON {flight_date}")
        print("#"*100)
        for row in res:
            print(f"Passenger: {row['first_name']} {row['last_name']} ({row['passenger_id']})")
            print(f"  Nationality: {row['nationality']}")
            print(f"  Seat: {row['seat_number']} | Class: {row['class']}")
            print(f"  Check-in: {row['check_in_status']} | Ticket: {row['ticket_status']}")
            print("-" * 50)
        print("#"*100)
    else:
        print("No passengers found for this flight.")


def search_passenger_by_name(cursor):
    """Search for passengers by first or last name"""
    print("\n TIP: You can even search using any partial name! [for example mes -> James, Messi, etc.]\n")
    search_term = input("Enter passenger's first or last name: ").strip()
    
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    query = """
        SELECT 
            P.passenger_id,
            P.first_name,
            P.last_name,
            P.email,
            P.phone,
            P.nationality,
            P.passport_number,
            P.frequent_flyer_number,
            P.date_of_birth,
            COUNT(DISTINCT T.ticket_id) AS total_bookings,
            COUNT(DISTINCT CASE WHEN T.ticket_status = 'Active' THEN T.ticket_id END) AS active_bookings
        FROM PASSENGER P
        LEFT JOIN TICKET T ON P.passenger_id = T.passenger_id
        WHERE P.first_name LIKE %s OR P.last_name LIKE %s
        GROUP BY P.passenger_id
        ORDER BY P.last_name, P.first_name
    """
    
    search_pattern = f"%{search_term}%"
    cursor.execute(query, (search_pattern, search_pattern))
    results = cursor.fetchall()
    
    if results:
        print("\n" + "="*120)
        print(f"PASSENGER SEARCH RESULTS FOR: '{search_term}'")
        print("="*120)
        for idx, row in enumerate(results, 1):
            print(f"\n{idx}. {row['first_name']} {row['last_name']} ({row['passenger_id']})")
            print(f"   Email: {row['email'] or 'N/A'} | Phone: {row['phone'] or 'N/A'}")
            print(f"   Nationality: {row['nationality']} | DOB: {row['date_of_birth']}")
            print(f"   Passport: {row['passport_number']}")
            if row['frequent_flyer_number']:
                print(f"   Frequent Flyer: {row['frequent_flyer_number']}")
            print(f"   Total Bookings: {row['total_bookings']} | Active Bookings: {row['active_bookings']}")
            print("-" * 120)
        print("="*120)
    else:
        print(f"No passengers found matching '{search_term}'.")


def add_new_passenger(cursor):
    """Adds a new passenger to the database"""
    try:
        print("\n--- ADD NEW PASSENGER ---")
        
        passenger_id = input("Enter Passenger ID (e.g., PAX013): ").upper()
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ")
        
        print("\nGender: 1. M  2. F  3. Other")
        gender_choice = input("Select (1-3): ")
        gender = {'1': 'M', '2': 'F', '3': 'Other'}.get(gender_choice, 'M')
        
        nationality = input("Enter Nationality: ")
        passport_number = input("Enter Passport Number: ")
        passport_expiry = input("Enter Passport Expiry (YYYY-MM-DD): ")
        email = input("Enter Email (optional): ")
        phone = input("Enter Phone (optional): ")
        frequent_flyer = input("Enter Frequent Flyer Number (optional): ")
        
        query = """
            INSERT INTO PASSENGER (
                passenger_id, first_name, last_name, date_of_birth, gender,
                nationality, passport_number, passport_expiry, email, phone,
                frequent_flyer_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            passenger_id, first_name, last_name, date_of_birth, gender,
            nationality, passport_number, passport_expiry,
            email if email else None,
            phone if phone else None,
            frequent_flyer if frequent_flyer else None
        ))
        cursor.connection.commit()
        print(f"\n✓ Passenger {passenger_id} added successfully!")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error adding passenger: {e}")
