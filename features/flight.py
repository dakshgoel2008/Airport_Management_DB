def show_all_upcoming_flights(cursor):
    """Shows all upcoming flights"""
    query = "SELECT * FROM FLIGHT WHERE flight_date >= CURDATE() ORDER BY flight_date, flight_number"
    cursor.execute(query)
    res = cursor.fetchall()
    if res:
        print("\n" + "#"*100)
        print("UPCOMING FLIGHTS")
        print("#"*100)
        for row in res:
            print(f"Flight Number: {row['flight_number']}, Flight Date: {row['flight_date']}, Source: {row['source_airport']}, Destination: {row['destination_airport']}, Status: {row['status']}")
        print("#"*100)
    else:
        print("No upcoming flights found.")

def cancel_flight(cursor):
    """Cancels a flight by updating its status."""
    flight_number = input("Enter Flight Number to cancel: ")
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    try:
        query = "UPDATE FLIGHT SET status = 'Cancelled' WHERE flight_number = %s AND flight_date = %s"
        cursor.execute(query, (flight_number, flight_date))
        if cursor.rowcount > 0:
            cursor.connection.commit()
            print("Flight cancelled successfully!")
        else:
            print("Flight not found.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error cancelling flight: {e}")

def find_cheapest_flights_on_route(cursor):
    """Finds the cheapest flight between two airports on a specific date."""
    src = input("Enter the source airport code (e.g., JFK): ")
    des = input("Enter the destination airport code (e.g., LAX): ")
    flight_dt = input("Enter the desired flight date (YYYY-MM-DD): ") 

    try:
        query = """
            SELECT F.flight_number, F.flight_date, AL.name, MIN(T.fare_amount) as cheapest_fare
            FROM FLIGHT F
            JOIN TICKET T ON F.flight_number = T.flight_number AND F.flight_date = T.flight_date
            JOIN AIRLINE AL ON F.airline_id = AL.airline_id
            WHERE F.source_airport = %s 
              AND F.destination_airport = %s 
              AND F.flight_date = %s 
              AND F.status = 'Scheduled'
            GROUP BY F.flight_number, F.flight_date, AL.name
            ORDER BY cheapest_fare ASC
            LIMIT 5;
        """
        cursor.execute(query, (src, des, flight_dt))
        res = cursor.fetchall()

        if res:
            print("\n" + "#"*100)
            print(f"CHEAPEST FLIGHTS FOUND ON {flight_dt}")
            print("#"*100)
            for row in res:
                print(f"Flight: {row['flight_number']} on {row['flight_date']}")
                print(f"Airline: {row['name']}")
                print(f"Price: ${row['cheapest_fare']:.2f}")
                print("-" * 50)
            print("#"*100)
        else:
            print("No scheduled flights found for this route on the specified date.")

    except Exception as e:
        print(f"An error occurred: {e}")


def add_new_flight(cursor):
    """Inserts a new flight into the database."""
    try:
        print("\n--- ADD NEW FLIGHT ---")
        
        # Display available airlines
        cursor.execute("SELECT airline_id, name FROM AIRLINE WHERE status = 'Active'")
        airlines = cursor.fetchall()
        print("\nAvailable Airlines:")
        for al in airlines:
            print(f"  {al['airline_id']}: {al['name']}")
        
        flight_number = input("\nEnter Flight Number: ").upper()
        airline_id = input("Enter Airline ID: ").upper()
        
        # Display available airports
        cursor.execute("SELECT airport_code, name, city FROM AIRPORT")
        airports = cursor.fetchall()
        print("\nAvailable Airports:")
        for ap in airports:
            print(f"  {ap['airport_code']}: {ap['name']}, {ap['city']}")
        
        source_airport = input("\nEnter Source Airport Code: ").upper()
        destination_airport = input("Enter Destination Airport Code: ").upper()
        
        if source_airport == destination_airport:
            print("Source and destination cannot be the same!")
            return
        
        scheduled_departure = input("Enter Scheduled Departure (YYYY-MM-DD HH:MM:SS): ")
        scheduled_arrival = input("Enter Scheduled Arrival (YYYY-MM-DD HH:MM:SS): ")
        flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
        
        # Display available aircraft for the airline
        cursor.execute("""
            SELECT aircraft_id, registration, aircraft_type_id 
            FROM AIRCRAFT 
            WHERE airline_id = %s AND status = 'Active'
        """, (airline_id,))
        aircraft_list = cursor.fetchall()
        
        if aircraft_list:
            print("\nAvailable Aircraft:")
            for ac in aircraft_list:
                print(f"  {ac['aircraft_id']}: {ac['registration']} ({ac['aircraft_type_id']})")
            aircraft_id = input("Enter Aircraft ID (or leave blank): ")
            if not aircraft_id:
                aircraft_id = None
        else:
            aircraft_id = None
            print("No aircraft available for this airline.")
        
        query = """
            INSERT INTO FLIGHT (
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
        print(f"\n✓ Flight {flight_number} added successfully!")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error adding flight: {e}")


def update_flight_status(cursor):
    """Updates the status of a flight"""
    flight_number = input("Enter Flight Number: ").upper()
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    
    # Show available statuses
    print("\nAvailable Statuses:")
    print("1. Scheduled")
    print("2. Delayed")
    print("3. Boarding")
    print("4. Departed")
    print("5. Arrived")
    print("6. Cancelled")
    
    status_choice = input("Select status (1-6): ")
    status_map = {
        '1': 'Scheduled',
        '2': 'Delayed',
        '3': 'Boarding',
        '4': 'Departed',
        '5': 'Arrived',
        '6': 'Cancelled'
    }
    
    new_status = status_map.get(status_choice)
    if not new_status:
        print("Invalid status choice!")
        return
    
    delay_minutes = 0
    if new_status == 'Delayed':
        delay_minutes = int(input("Enter delay in minutes: "))

    try:
        query = "UPDATE FLIGHT SET status = %s, delay_minutes = %s WHERE flight_number = %s AND flight_date = %s"
        cursor.execute(query, (new_status, delay_minutes, flight_number, flight_date))
        if cursor.rowcount > 0:
            cursor.connection.commit()
            print("Flight status updated successfully!")
        else:
            print("Flight not found for the given date.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error updating flight status: {e}")




# Assessment - 4 solution:
def update_flight_status(cursor):
    """Updates the status of a flight"""
    flight_number = input("Enter Flight Number: ")
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    new_status = input("Enter new status (e.g., Delayed, Cancelled, Boarding): ")
    delay_minutes = 0
    if new_status.lower() == 'delayed':
        delay_minutes = int(input("Enter delay in minutes: "))

    try:
        query = "UPDATE FLIGHT SET status = %s, delay_minutes = %s WHERE flight_number = %s AND flight_date = %s"
        cursor.execute(query, (new_status, delay_minutes, flight_number, flight_date))
        if cursor.rowcount > 0:
            cursor.connection.commit()
            print("Flight status updated successfully!")
        else:
            print("Flight not found for the given date.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error updating flight status: {e}")