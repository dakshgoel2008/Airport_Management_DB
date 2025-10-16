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
        print(f"Error updating flight status: {e}")s