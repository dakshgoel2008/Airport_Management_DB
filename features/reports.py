def get_flight_duration(cursor):
    """Calculates the duration of a flight"""
    flight_number = input("Enter flight number: ")
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    query = """
        select scheduled_departure, scheduled_arrival from flight where flight_number = %s and flight_date = %s
    """
    cursor.execute(query, (flight_number, flight_date))
    res = cursor.fetchone()

    if res:
        duration = res['scheduled_arrival'] - res['scheduled_departure']
        total_minutes = int(duration.total_seconds() / 60)
        hours, minutes = divmod(total_minutes, 60)
        print(f"The duration of flight {flight_number} on {flight_date} is {hours} hours and {minutes} minutes.")
    else:
        print("No flight found with the given details.")






# Assessment 4 - Solutions:
def show_flight_revenue_report(cursor):
    """Calls the stored procedure to generate a flight revenue report"""
    flight_number = input("Enter Flight Number for the report: ")
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")

    try:
        # calling the stored procedure:
        cursor.callproc('GenerateFlightRevenueReport', [flight_number, flight_date])

        res = cursor.fetchone()
        if res:
            print("\n" + "#"*100)
            print("FLIGHT REVENUE REPORT")
            print("#"*100)
            print(f"Flight Number: {res['Flight Number']}")
            print(f"Flight Date: {res['Flight Date']}")
            print(f"Tickets Sold: {res['Number of Tickets Sold']}")
            print(f"Total Revenue: ${res['Total Revenue']:,.2f}")
            print(f"Profit Status: {res['Profit Status']}")
            print("#"*100)
        else:
            print("Could not generate a report for this flight. Please check the details.")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_flight_status_log(cursor):
    """Shows the log of status changes for a specific flight."""
    flight_number = input("Enter Flight Number to view log: ")
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
    try:
        query = """
            SELECT * FROM FLIGHT_STATUS_LOG WHERE flight_number = %s AND flight_date = %s ORDER BY changed_at DESC
        """
        cursor.execute(query, (flight_number, flight_date))
        logs = cursor.fetchall()

        if not logs:
            print("No status change logs found for this flight.")
            return

        print("\n" + "#"*100)
        print(f"STATUS CHANGE LOG FOR FLIGHT {flight_number} ON {flight_date}")
        print("#"*100)
        for log in logs:
            print(f"Timestamp: {log['changed_at']}")
            print(f"From Status: '{log['old_status']}' → To Status: '{log['new_status']}'")
            print(f"Reason: {log['reason']}")
            print(f"Changed By: {log['changed_by']}")
            print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")