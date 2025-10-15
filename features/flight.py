def show_all_upcoming_flights(cursor):
    cursor.execute("SELECT * FROM FLIGHT WHERE departure_date >= CURDATE()")
    res = cursor.fetchall()

    if not res:
        print("Sorry but no upcoming flights found.")
        return
    
    print("\n" + "#"*100)
    print("UPCOMING FLIGHTS")
    print("#"*100)

    for row in res:
        print(f"Flight Number: {row['flight_number']}")
        print(f"Arrival Date: {row['scheduled_arrival']}")
        print("#"*100)