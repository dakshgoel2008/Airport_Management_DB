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

def view_booking_details(cursor):
    """View complete booking details"""
    booking_id = input("Enter Booking ID: ").upper()
    
    query = """ 
        SELECT 
            B.*,
            P.first_name,
            P.last_name,
            P.email AS passenger_email,
            P.phone AS passenger_phone,
            TA.name AS travel_agent_name
        FROM BOOKING B
        JOIN PASSENGER P ON B.passenger_id = P.passenger_id
        LEFT JOIN TRAVEL_AGENT TA ON B.travel_agent_id = TA.travel_agent_id
        WHERE B.booking_id = %s
    """
    cursor.execute(query, (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        print("No booking found with the given ID.")
        return
    
    ticket_query = """
        SELECT 
            T.*,
            F.source_airport,
            F.destination_airport,
            F.scheduled_departure,
            F.scheduled_arrival,
            AL.name AS airline_name
        FROM TICKET T
        JOIN FLIGHT F ON T.flight_number = F.flight_number AND T.flight_date = F.flight_date
        JOIN AIRLINE AL ON F.airline_id = AL.airline_id
        WHERE T.booking_id = %s
        ORDER BY F.scheduled_departure
    """

    cursor.execute(ticket_query, (booking_id,))
    tickets = cursor.fetchall()

    print("\n" + "="*120)
    print("BOOKING DETAILS")
    print("="*120)
    print(f"Booking ID: {booking['booking_id']}")
    print(f"Booking Reference: {booking['booking_reference']}")
    print(f"Booking Date: {booking['booking_date']}")
    print(f"Booking Status: {booking['booking_status']}")
    print(f"Payment Status: {booking['payment_status']}")
    print(f"\nPassenger: {booking['first_name']} {booking['last_name']}")
    print(f"Contact: {booking['passenger_email'] or 'N/A'} | {booking['passenger_phone'] or 'N/A'}")
    if booking['travel_agent_name']:
        print(f"Booked via: {booking['travel_agent_name']}")
    print(f"\nTotal Amount: ${booking['total_amount']:,.2f} ({booking['currency']})")
    
    print("\n" + "-"*120)
    print("TICKETS IN THIS BOOKING:")
    print("-"*120)
    
    if tickets:
        for idx, ticket in enumerate(tickets, 1):
            print(f"\n{idx}. Ticket ID: {ticket['ticket_id']}")
            print(f"   Flight: {ticket['flight_number']} on {ticket['flight_date']}")
            print(f"   Airline: {ticket['airline_name']}")
            print(f"   Route: {ticket['source_airport']} → {ticket['destination_airport']}")
            print(f"   Departure: {ticket['scheduled_departure']} | Arrival: {ticket['scheduled_arrival']}")
            print(f"   Class: {ticket['class']} | Seat: {ticket['seat_number'] or 'Not Assigned'}")
            print(f"   Fare: ${ticket['fare_amount']:,.2f}")
            print(f"   Status: {ticket['ticket_status']} | Check-in: {ticket['check_in_status']}")
            if ticket['special_requests']:
                print(f"   Special Requests: {ticket['special_requests']}")
    else:
        print("No tickets found for this booking.")
    
    print("="*120)

