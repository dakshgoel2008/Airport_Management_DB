def show_all_upcoming_flights(cursor):
    """Display all upcoming flights"""
    print("\n" + "="*80)
    print("UPCOMING FLIGHTS")
    print("="*80)
    
    query = """
        SELECT 
            f.flight_number, f.flight_date, f.scheduled_departure,
            f.source_airport, f.destination_airport, f.status,
            al.name AS airline_name, al.iata_code
        FROM flight f
        JOIN airline al ON f.airline_id = al.airline_id
        WHERE f.flight_date >= CURDATE()
        ORDER BY f.flight_date, f.scheduled_departure
        LIMIT 100
    """
    
    cursor.execute(query)
    res = cursor.fetchall()
    
    if res:
        print(f"\nShowing next {len(res)} flights")
        print("-"*80)
        print(f"{'Flight':<12} {'Date':<12} {'Departure':<10} {'Route':<30} {'Status':<12}")
        print("-"*80)
        
        for row in res:
            flight_code = f"{row['iata_code']}{row['flight_number']}"
            route = f"{row['source_airport']} → {row['destination_airport']}"
            departure_time = str(row['scheduled_departure']).split()[1][:5] if row['scheduled_departure'] else "N/A"
            
            print(f"{flight_code:<12} {row['flight_date']!s:<12} {departure_time:<10} {route:<30} {row['status']:<12}")
        
        print("-"*80)
        print(f"Total: {len(res)} flights")
        print("-"*80 + "\n")
    else:
        print("\nNo upcoming flights scheduled.\n")


def cancel_flight(cursor):
    """Cancel a scheduled flight"""
    print("\n" + "="*80)
    print("CANCEL FLIGHT")
    print("="*80)
    
    flight_number = input("\nFlight Number: ").strip().upper()
    flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
    
    try:
        # Get flight details first
        query = """
            SELECT 
                f.flight_number, f.flight_date, f.status,
                f.source_airport, f.destination_airport,
                f.scheduled_departure, al.name AS airline_name
            FROM flight f
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE f.flight_number = %s AND f.flight_date = %s
        """
        cursor.execute(query, (flight_number, flight_date))
        flight = cursor.fetchone()
        
        if not flight:
            print(f"\nFlight {flight_number} on {flight_date} not found.\n")
            return
        
        if flight['status'] == 'Cancelled':
            print(f"\nFlight {flight_number} is already cancelled.\n")
            return
        
        if flight['status'] in ['Departed', 'Arrived']:
            print(f"\nCannot cancel a flight with status '{flight['status']}'.\n")
            return
        
        # Display flight details
        print("\n" + "-"*80)
        print("FLIGHT DETAILS")
        print("-"*80)
        print(f"Flight:     {flight_number}")
        print(f"Date:       {flight['flight_date']}")
        print(f"Airline:    {flight['airline_name']}")
        print(f"Route:      {flight['source_airport']} → {flight['destination_airport']}")
        print(f"Departure:  {flight['scheduled_departure']}")
        print(f"Status:     {flight['status']}")
        print("-"*80)
        
        # Get cancellation reason
        print("\nCANCELLATION REASON:")
        print("  1. Weather Conditions")
        print("  2. Technical Issues")
        print("  3. Crew Unavailability")
        print("  4. Low Bookings")
        print("  5. Airport Closure")
        print("  6. Other")
        
        reason_choice = input("\nSelect reason (1-6): ").strip()
        reasons = {
            '1': 'Weather Conditions',
            '2': 'Technical Issues',
            '3': 'Crew Unavailability',
            '4': 'Low Bookings',
            '5': 'Airport Closure',
        }
        
        if reason_choice == '6':
            reason = input("Enter reason: ").strip()
        else:
            reason = reasons.get(reason_choice, 'Unspecified')
        
        # Confirmation
        print("\n" + "="*80)
        print("CONFIRM CANCELLATION")
        print("="*80)
        print(f"Flight:  {flight_number} on {flight['flight_date']}")
        print(f"Route:   {flight['source_airport']} → {flight['destination_airport']}")
        print(f"Reason:  {reason}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to cancel flight or press Enter to abort: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nCancellation aborted.\n")
            return
        
        # Update flight status
        update_query = "UPDATE flight SET status = 'Cancelled' WHERE flight_number = %s AND flight_date = %s"
        cursor.execute(update_query, (flight_number, flight_date))
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("FLIGHT CANCELLED")
        print("="*80)
        print(f"Flight:  {flight_number}")
        print(f"Date:    {flight['flight_date']}")
        print(f"Reason:  {reason}")
        print("-"*80)
        print("REQUIRED ACTIONS:")
        print("  - Notify all passengers")
        print("  - Process refunds/rebookings")
        print("  - Notify crew members")
        print("  - Update gate assignments")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to cancel flight. {e}\n")


def find_cheapest_flights_on_route(cursor):
    """Find the cheapest flights between two airports"""
    print("\n" + "="*80)
    print("FIND CHEAPEST FLIGHTS")
    print("="*80)
    
    src = input("\nSource Airport Code (e.g., JFK): ").strip().upper()
    des = input("Destination Airport Code (e.g., LAX): ").strip().upper()
    
    if src == des:
        print("\nSource and destination cannot be the same.\n")
        return
    
    flight_dt = input("Flight Date (YYYY-MM-DD): ").strip()
    
    try:
        query = """
            SELECT 
                f.flight_number, f.flight_date, f.scheduled_departure,
                al.name AS airline_name, al.iata_code,
                MIN(t.fare_amount) AS cheapest_fare,
                COUNT(DISTINCT t.ticket_id) AS available_seats
            FROM flight f
            JOIN ticket t ON f.flight_number = t.flight_number AND f.flight_date = t.flight_date
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE f.source_airport = %s 
              AND f.destination_airport = %s 
              AND f.flight_date = %s 
              AND f.status = 'Scheduled'
              AND t.booking_id IS NULL
            GROUP BY f.flight_number, f.flight_date, al.name, al.iata_code, f.scheduled_departure
            ORDER BY cheapest_fare ASC
            LIMIT 10
        """
        
        cursor.execute(query, (src, des, flight_dt))
        res = cursor.fetchall()
        
        if res:
            print("\n" + "-"*80)
            print(f"AVAILABLE FLIGHTS: {src} → {des} on {flight_dt}")
            print("-"*80)
            print(f"{'Flight':<12} {'Airline':<25} {'Departure':<10} {'Price':<12} {'Seats'}")
            print("-"*80)
            
            for row in res:
                flight_code = f"{row['iata_code']}{row['flight_number']}"
                departure_time = str(row['scheduled_departure']).split()[1][:5]
                
                print(f"{flight_code:<12} {row['airline_name']:<25} {departure_time:<10} ${row['cheapest_fare']:>8.2f}   {row['available_seats']}")
            
            print("-"*80)
            print(f"Showing {len(res)} flight(s) | Lowest fare: ${res[0]['cheapest_fare']:.2f}")
            print("-"*80 + "\n")
        else:
            print(f"\nNo available flights found for {src} → {des} on {flight_dt}")
            print("Try searching for a different date.\n")
            
    except Exception as e:
        print(f"\nError: Unable to search flights. {e}\n")


def add_new_flight(cursor):
    """Add a new flight to the schedule"""
    print("\n" + "="*80)
    print("ADD NEW FLIGHT")
    print("="*80)
    
    try:
        # Display airlines
        cursor.execute("SELECT airline_id, name, iata_code FROM airline WHERE status = 'Active' ORDER BY name")
        airlines = cursor.fetchall()
        
        if not airlines:
            print("\nNo active airlines found.\n")
            return
        
        print("\n" + "-"*80)
        print("AVAILABLE AIRLINES:")
        print("-"*80)
        for al in airlines:
            print(f"  {al['airline_id']:<6} {al['name']:<40} ({al['iata_code']})")
        print("-"*80)
        
        airline_id = input("\nAirline ID: ").strip().upper()
        
        # Validate airline
        cursor.execute("SELECT airline_id FROM airline WHERE airline_id = %s AND status = 'Active'", (airline_id,))
        if not cursor.fetchone():
            print(f"\nAirline '{airline_id}' not found or inactive.\n")
            return
        
        flight_number = input("Flight Number: ").strip().upper()
        flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
        
        # Check for duplicate
        cursor.execute(
            "SELECT flight_number FROM flight WHERE flight_number = %s AND flight_date = %s",
            (flight_number, flight_date)
        )
        if cursor.fetchone():
            print(f"\nFlight {flight_number} already exists on {flight_date}.\n")
            return
        
        # Display airports
        cursor.execute("SELECT airport_code, name, city, country FROM airport ORDER BY name")
        airports = cursor.fetchall()
        
        print("\n" + "-"*80)
        print("AVAILABLE AIRPORTS:")
        print("-"*80)
        for ap in airports:
            print(f"  {ap['airport_code']:<6} {ap['name']:<35} ({ap['city']}, {ap['country']})")
        print("-"*80)
        
        source_airport = input("\nSource Airport Code: ").strip().upper()
        destination_airport = input("Destination Airport Code: ").strip().upper()
        
        if source_airport == destination_airport:
            print("\nSource and destination cannot be the same.\n")
            return
        
        # Validate airports
        cursor.execute("SELECT airport_code FROM airport WHERE airport_code IN (%s, %s)", 
                      (source_airport, destination_airport))
        if len(cursor.fetchall()) != 2:
            print("\nOne or both airport codes are invalid.\n")
            return
        
        scheduled_departure = input("Scheduled Departure (YYYY-MM-DD HH:MM:SS): ").strip()
        scheduled_arrival = input("Scheduled Arrival (YYYY-MM-DD HH:MM:SS): ").strip()
        
        # Display available aircraft
        cursor.execute("""
            SELECT ac.aircraft_id, ac.registration, at.model, at.manufacturer
            FROM aircraft ac
            JOIN aircraft_type at ON ac.aircraft_type_id = at.aircraft_type_id
            WHERE ac.airline_id = %s AND ac.status = 'Active'
            ORDER BY at.model
        """, (airline_id,))
        aircraft_list = cursor.fetchall()
        
        aircraft_id = None
        if aircraft_list:
            print("\n" + "-"*80)
            print("AVAILABLE AIRCRAFT:")
            print("-"*80)
            for ac in aircraft_list:
                print(f"  {ac['aircraft_id']:<6} {ac['registration']:<12} {ac['manufacturer']} {ac['model']}")
            print("-"*80)
            aircraft_id = input("\nAircraft ID (optional, press Enter to skip): ").strip().upper()
            if not aircraft_id:
                aircraft_id = None
        else:
            print("\nNo aircraft available for this airline.")
        
        # Summary
        print("\n" + "="*80)
        print("CONFIRM NEW FLIGHT")
        print("="*80)
        print(f"Flight:     {flight_number}")
        print(f"Airline:    {airline_id}")
        print(f"Date:       {flight_date}")
        print(f"Route:      {source_airport} → {destination_airport}")
        print(f"Departure:  {scheduled_departure}")
        print(f"Arrival:    {scheduled_arrival}")
        print(f"Aircraft:   {aircraft_id or 'Not assigned'}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to add flight or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nFlight addition cancelled.\n")
            return
        
        query = """
            INSERT INTO flight (
                flight_number, airline_id, aircraft_id, source_airport, 
                destination_airport, scheduled_departure, scheduled_arrival, 
                status, flight_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'Scheduled', %s)
        """
        
        cursor.execute(query, (
            flight_number, airline_id, aircraft_id, source_airport,
            destination_airport, scheduled_departure, scheduled_arrival, flight_date
        ))
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print(f"SUCCESS: Flight {flight_number} added successfully")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to add flight. {e}\n")


def update_flight_status(cursor):
    """Update the status of a flight"""
    print("\n" + "="*80)
    print("UPDATE FLIGHT STATUS")
    print("="*80)
    
    flight_number = input("\nFlight Number: ").strip().upper()
    flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
    
    try:
        # Get current flight details
        query = """
            SELECT 
                f.flight_number, f.flight_date, f.status, f.delay_minutes,
                f.source_airport, f.destination_airport, f.scheduled_departure,
                al.name AS airline_name
            FROM flight f
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE f.flight_number = %s AND f.flight_date = %s
        """
        cursor.execute(query, (flight_number, flight_date))
        flight = cursor.fetchone()
        
        if not flight:
            print(f"\nFlight {flight_number} on {flight_date} not found.\n")
            return
        
        # Display current status
        print("\n" + "-"*80)
        print("CURRENT FLIGHT STATUS")
        print("-"*80)
        print(f"Flight:     {flight_number}")
        print(f"Date:       {flight['flight_date']}")
        print(f"Airline:    {flight['airline_name']}")
        print(f"Route:      {flight['source_airport']} → {flight['destination_airport']}")
        print(f"Status:     {flight['status']}")
        if flight['delay_minutes'] and flight['delay_minutes'] > 0:
            print(f"Delay:      {flight['delay_minutes']} minutes")
        print("-"*80)
        
        # Status options
        print("\nNEW STATUS:")
        print("  1. Scheduled")
        print("  2. Delayed")
        print("  3. Boarding")
        print("  4. Departed")
        print("  5. In Flight")
        print("  6. Arrived")
        print("  7. Cancelled")
        
        status_choice = input("\nSelect status (1-7): ").strip()
        status_map = {
            '1': 'Scheduled',
            '2': 'Delayed',
            '3': 'Boarding',
            '4': 'Departed',
            '5': 'In Flight',
            '6': 'Arrived',
            '7': 'Cancelled'
        }
        
        new_status = status_map.get(status_choice)
        if not new_status:
            print("\nInvalid status selection.\n")
            return
        
        delay_minutes = 0
        if new_status == 'Delayed':
            while True:
                try:
                    delay_minutes = int(input("Delay duration (minutes): ").strip())
                    if delay_minutes < 0:
                        print("Delay must be positive.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
        
        # Confirmation
        print("\n" + "="*80)
        print("CONFIRM STATUS UPDATE")
        print("="*80)
        print(f"Flight:      {flight_number}")
        print(f"Date:        {flight['flight_date']}")
        print(f"Current:     {flight['status']}")
        print(f"New Status:  {new_status}")
        if delay_minutes > 0:
            print(f"Delay:       {delay_minutes} minutes")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to update or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nStatus update cancelled.\n")
            return
        
        update_query = """
            UPDATE flight 
            SET status = %s, delay_minutes = %s 
            WHERE flight_number = %s AND flight_date = %s
        """
        cursor.execute(update_query, (new_status, delay_minutes, flight_number, flight_date))
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("STATUS UPDATED")
        print("="*80)
        print(f"Flight:     {flight_number}")
        print(f"New Status: {new_status}")
        if delay_minutes > 0:
            print(f"Delay:      {delay_minutes} minutes")
            print("-"*80)
            print("ACTION REQUIRED:")
            print("  - Notify passengers of delay")
            print("  - Update departure boards")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to update flight status. {e}\n")


def search_flight_by_id(cursor):
    """Search for flight details by flight number"""
    print("\n" + "="*80)
    print("FLIGHT SEARCH")
    print("="*80)
    
    flight_number = input("\nFlight Number: ").strip().upper()
    flight_date = input("Flight Date (YYYY-MM-DD, optional - press Enter to skip): ").strip()
    
    try:
        if flight_date:
            query = """
                SELECT 
                    f.*,
                    al.name AS airline_name, al.iata_code,
                    ac.registration AS aircraft_registration,
                    at.model AS aircraft_model, at.manufacturer,
                    src.name AS source_airport_name, src.city AS source_city,
                    dest.name AS dest_airport_name, dest.city AS dest_city
                FROM flight f
                JOIN airline al ON f.airline_id = al.airline_id
                LEFT JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id
                LEFT JOIN aircraft_type at ON ac.aircraft_type_id = at.aircraft_type_id
                JOIN airport src ON f.source_airport = src.airport_code
                JOIN airport dest ON f.destination_airport = dest.airport_code
                WHERE f.flight_number = %s AND f.flight_date = %s
            """
            cursor.execute(query, (flight_number, flight_date))
        else:
            query = """
                SELECT 
                    f.*,
                    al.name AS airline_name, al.iata_code,
                    ac.registration AS aircraft_registration,
                    at.model AS aircraft_model, at.manufacturer,
                    src.name AS source_airport_name, src.city AS source_city,
                    dest.name AS dest_airport_name, dest.city AS dest_city
                FROM flight f
                JOIN airline al ON f.airline_id = al.airline_id
                LEFT JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id
                LEFT JOIN aircraft_type at ON ac.aircraft_type_id = at.aircraft_type_id
                JOIN airport src ON f.source_airport = src.airport_code
                JOIN airport dest ON f.destination_airport = dest.airport_code
                WHERE f.flight_number = %s
                ORDER BY f.flight_date DESC
                LIMIT 10
            """
            cursor.execute(query, (flight_number,))
        
        res = cursor.fetchall()
        
        if res:
            print("\n" + "-"*80)
            print(f"SEARCH RESULTS: {len(res)} flight(s) found")
            print("-"*80)
            
            for i, flight in enumerate(res, 1):
                if len(res) > 1:
                    print(f"\nFlight {i} of {len(res)}")
                    print("-"*80)
                
                flight_code = f"{flight['iata_code']}{flight['flight_number']}"
                print(f"Flight:     {flight_code} - {flight['airline_name']}")
                print(f"Date:       {flight['flight_date']}")
                print(f"Route:      {flight['source_airport_name']} ({flight['source_airport']}, {flight['source_city']})")
                print(f"            → {flight['dest_airport_name']} ({flight['destination_airport']}, {flight['dest_city']})")
                print(f"Departure:  {flight['scheduled_departure']}")
                print(f"Arrival:    {flight['scheduled_arrival']}")
                
                if flight['aircraft_registration']:
                    aircraft_info = f"{flight['manufacturer']} {flight['aircraft_model']}" if flight['manufacturer'] else flight['aircraft_model']
                    print(f"Aircraft:   {aircraft_info} ({flight['aircraft_registration']})")
                
                status_display = flight['status']
                if flight['delay_minutes'] and flight['delay_minutes'] > 0:
                    status_display += f" - Delayed {flight['delay_minutes']} min"
                print(f"Status:     {status_display}")
                
                if flight['gate_id']:
                    print(f"Gate:       {flight['gate_id']} (Terminal {flight['terminal']})")
                
                if i < len(res):
                    print("-"*80)
            
            print("-"*80 + "\n")
        else:
            search_criteria = f"{flight_number} on {flight_date}" if flight_date else flight_number
            print(f"\nNo flights found matching '{search_criteria}'.\n")
            
    except Exception as e:
        print(f"\nError: Unable to search flights. {e}\n")