def show_all_airports(cursor) -> None:
    """Showing all the airports"""
    cursor.execute("SELECT * FROM AIRPORT")
    res = cursor.fetchall()     # fetching all the rows

    if not res:
        print("No Airports found.")
        return
    
    print("\n" + "#"*100)
    print("AIRPORTS IN DATABASE")
    print("#"*100)

    for row in res:
        print(f"Code: {row['airport_code']}")
        print(f"Name: {row['name']}")
        print(f"City: {row['city']}")
        print("#"*100)  