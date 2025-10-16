def show_all_upcoming_flights(cursor):
    cursor.execute("SELECT * FROM FLIGHT WHERE flight_date >= CURDATE()")
    res = cursor.fetchall()

    if not res:
        print("Sorry but no upcoming flights found.")
        return
    
    print("\n" + "#"*100)
    print("UPCOMING FLIGHTS")
    print("#"*100)

    for row in res:
        print(f"Flight Number: {row['flight_number']}")
        print(f"Airline ID: {row['airline_id']}")
        print(f"From: {row['source_airport']} → To: {row['destination_airport']}")
        print(f"Scheduled Departure: {row['scheduled_departure']}")
        print(f"Scheduled Arrival: {row['scheduled_arrival']}")
        print(f"Status: {row['status']}")
        print(f"Gate: {row['gate_id']} | Terminal: {row['terminal']}")
        print("#"*100)

