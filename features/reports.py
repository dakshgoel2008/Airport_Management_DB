def get_flight_duration(cursor):
    """Calculates the duration of a flight."""
    print("\n=== FLIGHT DURATION LOOKUP ===")
    flight_number = input("Enter Flight Number: ").strip().upper()
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ").strip()

    query = """
        SELECT scheduled_departure, scheduled_arrival
        FROM flight
        WHERE flight_number = %s AND flight_date = %s
    """
    cursor.execute(query, (flight_number, flight_date))
    res = cursor.fetchone()

    if not res:
        print("\nNo flight found. Please verify the flight number and date.\n")
        return

    duration = res['scheduled_arrival'] - res['scheduled_departure']
    total_minutes = int(duration.total_seconds() / 60)
    hours, minutes = divmod(total_minutes, 60)

    print("\n----------------------------------------")
    print(" FLIGHT DURATION")
    print("----------------------------------------")
    print(f" Flight Number : {flight_number}")
    print(f" Flight Date   : {flight_date}")
    print(f" Duration      : {hours} hour(s) {minutes} minute(s)")
    print("----------------------------------------\n")


def occupancy_vs_price_report(cursor):
    """Shows flight occupancy and average price per class."""
    print("\n=== OCCUPANCY AND PRICE REPORT ===")
    flight_number = input("Enter Flight Number: ").strip().upper()
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ").strip()

    query = """
        SELECT class, COUNT(*) AS passengers, AVG(fare_amount) AS avg_price
        FROM TICKET
        WHERE flight_number = %s AND flight_date = %s AND ticket_status = 'Active'
        GROUP BY class
    """
    cursor.execute(query, (flight_number, flight_date))
    res = cursor.fetchall()

    if not res:
        print("\nNo active tickets found for this flight.\n")
        return

    print("\n============================================================")
    print(f" FLIGHT: {flight_number}   DATE: {flight_date}")
    print("============================================================")
    for row in res:
        print(f" Class       : {row['class']}")
        print(f" Passengers  : {row['passengers']}")
        print(f" Avg Fare    : ${row['avg_price']:.2f}")
        print("------------------------------------------------------------")
    print()


def avg_ticket_price_on_route(cursor):
    """Calculates the average ticket price for a given route."""
    print("\n=== AVERAGE TICKET PRICE ON ROUTE ===")
    src = input("Enter Source Airport Code: ").strip().upper()
    des = input("Enter Destination Airport Code: ").strip().upper()

    query = """
        SELECT AVG(T.fare_amount) as avg_price
        FROM TICKET T
        JOIN FLIGHT F
        ON T.flight_number = F.flight_number AND T.flight_date = F.flight_date
        WHERE F.source_airport = %s AND F.destination_airport = %s
    """
    cursor.execute(query, (src, des))
    res = cursor.fetchone()

    if not res or not res['avg_price']:
        print("\nNo pricing data available for this route.\n")
        return

    print("\n----------------------------------------")
    print(" AVERAGE TICKET PRICE")
    print("----------------------------------------")
    print(f" Route : {src} → {des}")
    print(f" Price : ${res['avg_price']:.2f}")
    print("----------------------------------------\n")


def show_flight_revenue_report(cursor):
    """Calls the stored procedure to generate a flight revenue report."""
    print("\n=== FLIGHT REVENUE REPORT ===")
    flight_number = input("Enter Flight Number: ").strip().upper()
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ").strip()

    try:
        cursor.callproc('GenerateFlightRevenueReport', [flight_number, flight_date])
        res = cursor.fetchone()

        if not res:
            print("\nNo revenue report available for this flight.\n")
            return

        print("\n============================================================")
        print(" REVENUE SUMMARY")
        print("============================================================")
        print(f" Flight Number : {res['Flight Number']}")
        print(f" Flight Date   : {res['Flight Date']}")
        print(f" Tickets Sold  : {res['Number of Tickets Sold']}")
        print(f" Total Revenue : ${res['Total Revenue']:,.2f}")
        print(f" Profit Status : {res['Profit Status']}")
        print("============================================================\n")

    except Exception as e:
        print(f"\nError occurred while fetching report: {e}\n")


def view_flight_status_log(cursor):
    """Shows the log of status changes for a specific flight."""
    print("\n=== FLIGHT STATUS CHANGE LOG ===")
    flight_number = input("Enter Flight Number: ").strip().upper()
    flight_date = input("Enter Flight Date (YYYY-MM-DD): ").strip()

    query = """
        SELECT *
        FROM FLIGHT_STATUS_LOG
        WHERE flight_number = %s AND flight_date = %s
        ORDER BY changed_at DESC
    """
    try:
        cursor.execute(query, (flight_number, flight_date))
        logs = cursor.fetchall()

        if not logs:
            print("\nNo status logs found for this flight.\n")
            return

        print("\n============================================================")
        print(f" STATUS LOGS FOR {flight_number} ON {flight_date}")
        print("============================================================")
        for log in logs:
            print(f" Timestamp   : {log['changed_at']}")
            print(f" Old Status  : {log['old_status']}")
            print(f" New Status  : {log['new_status']}")
            print(f" Reason      : {log['reason']}")
            print(f" Changed By  : {log['changed_by']}")
            print("------------------------------------------------------------")
        print()

    except Exception as e:
        print(f"\nError occurred while fetching logs: {e}\n")
