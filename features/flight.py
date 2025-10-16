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
    print("Dummy Function")

def update_flight_status(cursor):
    """Updates the status of a flight."""
    print("Dummy Function")




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