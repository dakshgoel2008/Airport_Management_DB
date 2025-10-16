def cancel_ticket(cursor):
    """Cancels the ticket of the passenger."""
    ticket_id = input("Enter ticket's ID to cancel: ")
    try:
        query = """
            update ticket set status = "Cancelled" where ticket_id = %s
        """
        if cursor.rowcount > 0:
            cursor.execute(query, (ticket_id,))
            cursor.connection.commit()
            print("Ticket cancelled successfully")
        else:
            print("No ticket found with the given ID.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error cancelling ticket: {e}")

def add_new_ticket(cursor):
    """Inserts a new ticket into the database."""
    print("Dummy function")
    r