def cancel_ticket(cursor):
    """Cancel a passenger ticket"""
    print("\n" + "="*80)
    print("CANCEL TICKET")
    print("="*80)
    
    ticket_id = input("\nTicket ID: ").strip().upper()
    
    try:
        # Get ticket details
        query = """
            SELECT 
                t.ticket_id, t.ticket_status, t.seat_number, t.class, 
                t.fare_amount, t.check_in_status,
                t.flight_number, t.flight_date,
                p.first_name, p.last_name, p.passenger_id,
                f.source_airport, f.destination_airport, f.status AS flight_status,
                al.name AS airline_name
            FROM ticket t
            JOIN passenger p ON t.passenger_id = p.passenger_id
            JOIN flight f ON t.flight_number = f.flight_number 
                         AND t.flight_date = f.flight_date
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE t.ticket_id = %s
        """
        cursor.execute(query, (ticket_id,))
        ticket = cursor.fetchone()
        
        if not ticket:
            print(f"\nTicket '{ticket_id}' not found.\n")
            return
        
        if ticket['ticket_status'] == 'Cancelled':
            print(f"\nTicket {ticket_id} is already cancelled.\n")
            return
        
        if ticket['flight_status'] in ['Departed', 'Arrived']:
            print(f"\nCannot cancel ticket for a flight that has {ticket['flight_status'].lower()}.\n")
            return
        
        # Display ticket details
        print("\n" + "-"*80)
        print("TICKET DETAILS")
        print("-"*80)
        print(f"Ticket ID:   {ticket['ticket_id']}")
        print(f"Passenger:   {ticket['first_name']} {ticket['last_name']} ({ticket['passenger_id']})")
        print(f"Flight:      {ticket['flight_number']} on {ticket['flight_date']}")
        print(f"Airline:     {ticket['airline_name']}")
        print(f"Route:       {ticket['source_airport']} → {ticket['destination_airport']}")
        print(f"Class:       {ticket['class']}")
        print(f"Seat:        {ticket['seat_number'] or 'Not assigned'}")
        print(f"Fare:        ${ticket['fare_amount']:,.2f}")
        print(f"Status:      {ticket['ticket_status']}")
        print(f"Check-in:    {ticket['check_in_status']}")
        print("-"*80)
        
        # Get cancellation reason
        print("\nCANCELLATION REASON:")
        print("  1. Customer Request")
        print("  2. Flight Cancelled")
        print("  3. Schedule Change")
        print("  4. Medical Emergency")
        print("  5. Other")
        
        reason_choice = input("\nSelect reason (1-5): ").strip()
        reasons = {
            '1': 'Customer Request',
            '2': 'Flight Cancelled',
            '3': 'Schedule Change',
            '4': 'Medical Emergency',
        }
        
        if reason_choice == '5':
            reason = input("Enter reason: ").strip()
        else:
            reason = reasons.get(reason_choice, 'Unspecified')
        
        # Confirmation
        print("\n" + "="*80)
        print("CONFIRM TICKET CANCELLATION")
        print("="*80)
        print(f"Ticket:     {ticket_id}")
        print(f"Passenger:  {ticket['first_name']} {ticket['last_name']}")
        print(f"Flight:     {ticket['flight_number']} on {ticket['flight_date']}")
        print(f"Fare:       ${ticket['fare_amount']:,.2f}")
        print(f"Reason:     {reason}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to cancel ticket or press Enter to abort: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nTicket cancellation aborted.\n")
            return
        
        # Cancel ticket
        cursor.execute(
            "UPDATE ticket SET ticket_status = 'Cancelled' WHERE ticket_id = %s",
            (ticket_id,)
        )
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("TICKET CANCELLED")
        print("="*80)
        print(f"Ticket ID:  {ticket_id}")
        print(f"Passenger:  {ticket['first_name']} {ticket['last_name']}")
        print(f"Reason:     {reason}")
        print("-"*80)
        print("NEXT STEPS:")
        print("  - Process refund according to fare rules")
        print("  - Send cancellation confirmation to passenger")
        print("  - Release seat for rebooking")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to cancel ticket. {e}\n")


def add_new_ticket(cursor):
    """Create a new ticket booking"""
    print("\n" + "="*80)
    print("CREATE NEW TICKET")
    print("="*80)
    
    try:
        # Booking creation or selection
        print("\n" + "-"*80)
        print("BOOKING SELECTION")
        print("-"*80)
        print("  1. Create new booking")
        print("  2. Add to existing booking")
        
        booking_choice = input("\nSelect option (1 or 2): ").strip()
        
        if booking_choice == '1':
            # Create new booking
            booking_id = input("\nBooking ID (e.g., BK013): ").strip().upper()
            
            # Check for duplicate
            cursor.execute("SELECT booking_id FROM booking WHERE booking_id = %s", (booking_id,))
            if cursor.fetchone():
                print(f"\nBooking ID '{booking_id}' already exists.\n")
                return
            
            passenger_id = input("Passenger ID: ").strip().upper()
            
            # Verify passenger
            cursor.execute(
                "SELECT first_name, last_name, email FROM passenger WHERE passenger_id = %s",
                (passenger_id,)
            )
            pax = cursor.fetchone()
            
            if not pax:
                print(f"\nPassenger '{passenger_id}' not found.\n")
                return
            
            print(f"\nPassenger: {pax['first_name']} {pax['last_name']}")
            if pax['email']:
                print(f"Email: {pax['email']}")
            
            booking_ref = input("\nBooking Reference (6-8 chars): ").strip().upper()
            
            while True:
                try:
                    total_amount = float(input("Total Booking Amount: $").strip().replace(',', ''))
                    if total_amount < 0:
                        print("Amount must be positive.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid amount.")
            
            # Create booking
            booking_query = """
                INSERT INTO booking (
                    booking_id, passenger_id, booking_date, total_amount,
                    booking_reference, payment_status, booking_status
                ) VALUES (%s, %s, NOW(), %s, %s, 'Paid', 'Confirmed')
            """
            cursor.execute(booking_query, (booking_id, passenger_id, total_amount, booking_ref))
            print(f"\nBooking {booking_id} created successfully.")
            
        else:
            # Use existing booking
            booking_id = input("\nExisting Booking ID: ").strip().upper()
            
            cursor.execute("""
                SELECT b.booking_id, b.passenger_id, b.booking_status,
                       p.first_name, p.last_name
                FROM booking b
                JOIN passenger p ON b.passenger_id = p.passenger_id
                WHERE b.booking_id = %s
            """, (booking_id,))
            
            booking = cursor.fetchone()
            
            if not booking:
                print(f"\nBooking '{booking_id}' not found.\n")
                return
            
            if booking['booking_status'] == 'Cancelled':
                print(f"\nCannot add ticket to cancelled booking.\n")
                return
            
            passenger_id = booking['passenger_id']
            print(f"\nBooking found: {booking['first_name']} {booking['last_name']}")
        
        # Flight selection
        print("\n" + "-"*80)
        print("FLIGHT INFORMATION")
        print("-"*80)
        
        flight_number = input("Flight Number: ").strip().upper()
        flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
        
        # Verify flight
        cursor.execute("""
            SELECT 
                f.*, 
                al.name AS airline_name, al.iata_code,
                (SELECT COUNT(*) FROM ticket 
                 WHERE flight_number = f.flight_number 
                   AND flight_date = f.flight_date 
                   AND ticket_status = 'Active') AS booked_seats
            FROM flight f
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE f.flight_number = %s AND f.flight_date = %s
        """, (flight_number, flight_date))
        
        flight = cursor.fetchone()
        
        if not flight:
            print(f"\nFlight {flight_number} on {flight_date} not found.\n")
            return
        
        if flight['status'] not in ['Scheduled', 'Delayed']:
            print(f"\nCannot book ticket for flight with status '{flight['status']}'.\n")
            return
        
        print(f"\nFlight: {flight['iata_code']}{flight_number} - {flight['airline_name']}")
        print(f"Route:  {flight['source_airport']} → {flight['destination_airport']}")
        print(f"Date:   {flight['flight_date']}")
        print(f"Status: {flight['status']}")
        print(f"Booked: {flight['booked_seats']} seats")
        
        # Ticket details
        print("\n" + "-"*80)
        print("TICKET DETAILS")
        print("-"*80)
        
        ticket_id = input("Ticket ID (e.g., TK013): ").strip().upper()
        
        # Check for duplicate
        cursor.execute("SELECT ticket_id FROM ticket WHERE ticket_id = %s", (ticket_id,))
        if cursor.fetchone():
            print(f"\nTicket ID '{ticket_id}' already exists.\n")
            return
        
        seat_number = input("Seat Number (e.g., 12A): ").strip().upper()
        
        # Check if seat is taken
        cursor.execute("""
            SELECT seat_number FROM ticket
            WHERE flight_number = %s AND flight_date = %s 
              AND seat_number = %s AND ticket_status = 'Active'
        """, (flight_number, flight_date, seat_number))
        
        if cursor.fetchone():
            print(f"\nSeat {seat_number} is already assigned on this flight.\n")
            return
        
        print("\nCLASS:")
        print("  1. Economy")
        print("  2. Premium Economy")
        print("  3. Business")
        print("  4. First")
        
        class_choice = input("\nSelect (1-4): ").strip()
        ticket_class = {
            '1': 'Economy',
            '2': 'Premium Economy',
            '3': 'Business',
            '4': 'First'
        }.get(class_choice, 'Economy')
        
        while True:
            try:
                fare_amount = float(input("Fare Amount: $").strip().replace(',', ''))
                if fare_amount < 0:
                    print("Fare must be positive.")
                    continue
                break
            except ValueError:
                print("Please enter a valid amount.")
        
        while True:
            try:
                baggage_allowance = int(input("Baggage Allowance (kg): ").strip())
                if baggage_allowance < 0:
                    print("Baggage allowance must be positive.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        special_requests = input("Special Requests (optional, press Enter to skip): ").strip() or None
        
        # Summary and confirmation
        print("\n" + "="*80)
        print("CONFIRM TICKET BOOKING")
        print("="*80)
        print(f"Ticket ID:   {ticket_id}")
        print(f"Booking:     {booking_id}")
        print(f"Passenger:   {passenger_id}")
        print(f"Flight:      {flight_number} on {flight_date}")
        print(f"Route:       {flight['source_airport']} → {flight['destination_airport']}")
        print(f"Seat:        {seat_number}")
        print(f"Class:       {ticket_class}")
        print(f"Fare:        ${fare_amount:,.2f}")
        print(f"Baggage:     {baggage_allowance} kg")
        if special_requests:
            print(f"Requests:    {special_requests}")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to create ticket or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nTicket creation cancelled.\n")
            return
        
        # Create ticket
        ticket_query = """
            INSERT INTO ticket (
                ticket_id, booking_id, flight_number, flight_date, passenger_id,
                seat_number, class, fare_amount, ticket_status, check_in_status,
                baggage_allowance_kg, special_requests
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Active', 'Not_Checked_In', %s, %s)
        """
        
        cursor.execute(ticket_query, (
            ticket_id, booking_id, flight_number, flight_date, passenger_id,
            seat_number, ticket_class, fare_amount, baggage_allowance,
            special_requests
        ))
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("TICKET CREATED SUCCESSFULLY")
        print("="*80)
        print(f"Ticket ID:  {ticket_id}")
        print(f"Flight:     {flight_number} on {flight_date}") 
        print(f"Seat:       {seat_number}")
        print(f"Class:      {ticket_class}")
        print(f"Fare:       ${fare_amount:,.2f}")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to create ticket. {e}\n")


def view_booking_details(cursor):
    """View complete booking information"""
    print("\n" + "="*80)
    print("VIEW BOOKING DETAILS")
    print("="*80)
    
    booking_id = input("\nBooking ID: ").strip().upper()
    
    try:
        # Get booking details
        query = """
            SELECT 
                b.*,
                p.first_name, p.last_name, p.email AS passenger_email,
                p.phone AS passenger_phone, p.passport_number,
                ta.name AS travel_agent_name
            FROM booking b
            JOIN passenger p ON b.passenger_id = p.passenger_id
            LEFT JOIN travel_agent ta ON b.travel_agent_id = ta.travel_agent_id
            WHERE b.booking_id = %s
        """
        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            print(f"\nBooking '{booking_id}' not found.\n")
            return
        
        # Get tickets
        ticket_query = """
            SELECT 
                t.*,
                f.source_airport, f.destination_airport,
                f.scheduled_departure, f.scheduled_arrival, f.status AS flight_status,
                al.name AS airline_name, al.iata_code
            FROM ticket t
            JOIN flight f ON t.flight_number = f.flight_number 
                         AND t.flight_date = f.flight_date
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE t.booking_id = %s
            ORDER BY f.scheduled_departure
        """
        cursor.execute(ticket_query, (booking_id,))
        tickets = cursor.fetchall()
        
        # Display booking information
        print("\n" + "-"*80)
        print("BOOKING INFORMATION")
        print("-"*80)
        print(f"Booking ID:        {booking['booking_id']}")
        print(f"Booking Reference: {booking['booking_reference']}")
        print(f"Booking Date:      {booking['booking_date']}")
        print(f"Status:            {booking['booking_status']}")
        print(f"Payment:           {booking['payment_status']}")
        print(f"Total Amount:      ${booking['total_amount']:,.2f} {booking.get('currency', 'USD')}")
        
        if booking['travel_agent_name']:
            print(f"Travel Agent:      {booking['travel_agent_name']}")
        
        print("-"*80)
        print("PASSENGER INFORMATION")
        print("-"*80)
        print(f"Name:        {booking['first_name']} {booking['last_name']}")
        print(f"Passenger ID: {booking['passenger_id']}")
        print(f"Email:       {booking['passenger_email'] or 'Not provided'}")
        print(f"Phone:       {booking['passenger_phone'] or 'Not provided'}")
        print(f"Passport:    {booking['passport_number']}")
        
        # Display tickets
        if tickets:
            print("-"*80)
            print(f"TICKETS ({len(tickets)})")
            print("-"*80)
            
            total_fare = sum(t['fare_amount'] for t in tickets if t['fare_amount'])
            
            for idx, ticket in enumerate(tickets, 1):
                flight_code = f"{ticket['iata_code']}{ticket['flight_number']}"
                route = f"{ticket['source_airport']} → {ticket['destination_airport']}"
                
                print(f"\nTicket {idx}: {ticket['ticket_id']}")
                print(f"  Flight:    {flight_code} on {ticket['flight_date']}")
                print(f"  Airline:   {ticket['airline_name']}")
                print(f"  Route:     {route}")
                print(f"  Departure: {ticket['scheduled_departure']}")
                print(f"  Arrival:   {ticket['scheduled_arrival']}")
                print(f"  Class:     {ticket['class']}")
                print(f"  Seat:      {ticket['seat_number'] or 'Not assigned'}")
                print(f"  Fare:      ${ticket['fare_amount']:,.2f}")
                print(f"  Baggage:   {ticket['baggage_allowance_kg']} kg")
                print(f"  Status:    Ticket: {ticket['ticket_status']} | Flight: {ticket['flight_status']} | Check-in: {ticket['check_in_status']}")
                
                if ticket['special_requests']:
                    print(f"  Requests:  {ticket['special_requests']}")
            
            print("-"*80)
            print(f"Total Fare: ${total_fare:,.2f}")
            print("-"*80 + "\n")
        else:
            print("-"*80)
            print("No tickets found for this booking")
            print("-"*80 + "\n")
            
    except Exception as e:
        print(f"\nError: Unable to retrieve booking details. {e}\n")


def check_in_passenger(cursor):
    """Check in a passenger for their flight"""
    print("\n" + "="*80)
    print("PASSENGER CHECK-IN")
    print("="*80)
    
    ticket_id = input("\nTicket ID: ").strip().upper()
    
    try:
        # Get ticket details
        query = """
            SELECT 
                t.ticket_id, t.ticket_status, t.check_in_status,
                t.seat_number, t.class, t.baggage_allowance_kg,
                t.flight_number, t.flight_date,
                p.first_name, p.last_name, p.passport_number,
                f.source_airport, f.destination_airport, 
                f.scheduled_departure, f.status AS flight_status,
                al.name AS airline_name
            FROM ticket t
            JOIN passenger p ON t.passenger_id = p.passenger_id
            JOIN flight f ON t.flight_number = f.flight_number 
                         AND t.flight_date = f.flight_date
            JOIN airline al ON f.airline_id = al.airline_id
            WHERE t.ticket_id = %s
        """
        cursor.execute(query, (ticket_id,))
        ticket = cursor.fetchone()
        
        if not ticket:
            print(f"\nTicket '{ticket_id}' not found.\n")
            return
        
        if ticket['ticket_status'] == 'Cancelled':
            print(f"\nCannot check in - ticket is cancelled.\n")
            return
        
        if ticket['check_in_status'] == 'Checked In':
            print(f"\nPassenger is already checked in for this flight.\n")
            return
        
        if ticket['flight_status'] in ['Departed', 'Arrived', 'Cancelled']:
            print(f"\nCannot check in - flight status is '{ticket['flight_status']}'.\n")
            return
        
        # Display ticket details
        print("\n" + "-"*80)
        print("FLIGHT INFORMATION")
        print("-"*80)
        print(f"Passenger:   {ticket['first_name']} {ticket['last_name']}")
        print(f"Passport:    {ticket['passport_number']}")
        print(f"Flight:      {ticket['flight_number']} on {ticket['flight_date']}")
        print(f"Airline:     {ticket['airline_name']}")
        print(f"Route:       {ticket['source_airport']} → {ticket['destination_airport']}")
        print(f"Departure:   {ticket['scheduled_departure']}")
        print(f"Class:       {ticket['class']}")
        print(f"Seat:        {ticket['seat_number'] or 'Not assigned'}")
        print(f"Baggage:     {ticket['baggage_allowance_kg']} kg")
        print("-"*80)
        
        # Baggage check
        print("\nBAGGAGE INFORMATION")
        while True:
            try:
                checked_bags = int(input("Number of checked bags: ").strip())
                if checked_bags < 0:
                    print("Cannot be negative.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        while True:
            try:
                baggage_weight = float(input(f"Total baggage weight (kg, allowance: {ticket['baggage_allowance_kg']} kg): ").strip())
                if baggage_weight < 0:
                    print("Cannot be negative.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        excess_weight = max(0, baggage_weight - ticket['baggage_allowance_kg'])
        
        if excess_weight > 0:
            print(f"\nWarning: Excess baggage of {excess_weight:.1f} kg")
            print("Additional charges may apply.")
        
        # Confirmation
        print("\n" + "="*80)
        print("CONFIRM CHECK-IN")
        print("="*80)
        print(f"Passenger:      {ticket['first_name']} {ticket['last_name']}")
        print(f"Flight:         {ticket['flight_number']} on {ticket['flight_date']}")
        print(f"Seat:           {ticket['seat_number'] or 'Not assigned'}")
        print(f"Checked Bags:   {checked_bags}")
        print(f"Baggage Weight: {baggage_weight:.1f} kg")
        if excess_weight > 0:
            print(f"Excess Weight:  {excess_weight:.1f} kg")
        print("="*80)
        
        confirm = input("\nType 'CONFIRM' to check in or press Enter to cancel: ").strip().upper()
        
        if confirm != 'CONFIRM':
            print("\nCheck-in cancelled.\n")
            return
        
        # Check in passenger
        cursor.execute(
            "UPDATE ticket SET check_in_status = 'Checked In' WHERE ticket_id = %s",
            (ticket_id,)
        )
        cursor.connection.commit()
        
        print("\n" + "="*80)
        print("CHECK-IN SUCCESSFUL")
        print("="*80)
        print(f"Passenger:   {ticket['first_name']} {ticket['last_name']}")
        print(f"Flight:      {ticket['flight_number']} on {ticket['flight_date']}")
        print(f"Seat:        {ticket['seat_number'] or 'Not assigned'}")
        print(f"Departure:   {ticket['scheduled_departure']}")
        print(f"Gate:        Check departure boards")
        print("-"*80)
        print("Boarding pass issued - Have a pleasant flight!")
        print("="*80 + "\n")
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"\nError: Unable to check in passenger. {e}\n")