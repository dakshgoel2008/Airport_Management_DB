def cancel_ticket(cursor):
    """Cancels the ticket of the passenger."""
    ticket_id = input("Enter ticket's ID to cancel: ").upper()
    try:
        query = "UPDATE TICKET SET ticket_status = 'Cancelled' WHERE ticket_id = %s"
        cursor.execute(query, (ticket_id,))
        if cursor.rowcount > 0:
            cursor.connection.commit()
            print("Ticket cancelled successfully")
        else:
            print("No ticket found with the given ID.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error cancelling ticket: {e}")


def add_new_ticket(cursor):
    """Inserts a new ticket into the database."""
    try:
        print("\n--- ADD NEW TICKET ---")
        
        # Get or create booking
        create_booking = input("Create new booking? (y/n): ").lower()
        
        if create_booking == 'y':
            booking_id = input("Enter Booking ID (e.g., BK013): ").upper()
            passenger_id = input("Enter Passenger ID: ").upper()
            
            # Verify passenger exists
            cursor.execute("SELECT first_name, last_name FROM PASSENGER WHERE passenger_id = %s", (passenger_id,))
            pax = cursor.fetchone()
            if not pax:
                print("Passenger not found!")
                return
            
            print(f"Passenger: {pax['first_name']} {pax['last_name']}")
            
            booking_ref = input("Enter Booking Reference (8 chars): ").upper()
            total_amount = float(input("Enter total booking amount: "))
            
            booking_query = """
                INSERT INTO BOOKING (
                    booking_id, passenger_id, booking_date, total_amount,
                    booking_reference, payment_status, booking_status
                ) VALUES (%s, %s, NOW(), %s, %s, 'Paid', 'Confirmed')
            """
            cursor.execute(booking_query, (booking_id, passenger_id, total_amount, booking_ref))
        else:
            booking_id = input("Enter existing Booking ID: ").upper()
            cursor.execute("SELECT passenger_id FROM BOOKING WHERE booking_id = %s", (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                print("Booking not found!")
                return
            passenger_id = booking['passenger_id']
        
        # Get flight details
        print("\nFlight Information:")
        flight_number = input("Enter Flight Number: ").upper()
        flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
        
        # Verify flight exists
        cursor.execute("""
            SELECT F.*, AL.name as airline_name
            FROM FLIGHT F
            JOIN AIRLINE AL ON F.airline_id = AL.airline_id
            WHERE F.flight_number = %s AND F.flight_date = %s
        """, (flight_number, flight_date))
        flight = cursor.fetchone()
        
        if not flight:
            print("Flight not found!")
            return
        
        print(f"Flight: {flight['airline_name']} {flight_number}")
        print(f"Route: {flight['source_airport']} → {flight['destination_airport']}")
        
        # Ticket details
        ticket_id = input("\nEnter Ticket ID (e.g., TK013): ").upper()
        seat_number = input("Enter Seat Number (e.g., 12A): ").upper()
        
        print("\nClass: 1. Economy  2. Premium_Economy  3. Business  4. First")
        class_choice = input("Select (1-4): ")
        ticket_class = {
            '1': 'Economy',
            '2': 'Premium_Economy',
            '3': 'Business',
            '4': 'First'
        }.get(class_choice, 'Economy')
        
        fare_amount = float(input("Enter Fare Amount: "))
        baggage_allowance = int(input("Enter Baggage Allowance (kg): "))
        special_requests = input("Special Requests (optional): ")
        
        ticket_query = """
            INSERT INTO TICKET (
                ticket_id, booking_id, flight_number, flight_date, passenger_id,
                seat_number, class, fare_amount, ticket_status, check_in_status,
                baggage_allowance_kg, special_requests
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Active', 'Not_Checked_In', %s, %s)
        """
        
        cursor.execute(ticket_query, (
            ticket_id, booking_id, flight_number, flight_date, passenger_id,
            seat_number, ticket_class, fare_amount, baggage_allowance,
            special_requests if special_requests else None
        ))
        cursor.connection.commit()
        print(f"\n✓ Ticket {ticket_id} created successfully!")
        print(f"   Seat: {seat_number} | Class: {ticket_class}")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error creating ticket: {e}")
