import os
from features import *
from core.menu import *

menu_map = {
    "1": view_menu,
    "2": insert_menu,
    "3": update_menu,
    "4": delete_menu,
    "5": search_menu,
    "6": reports_menu
}

def main_controller(cursor) -> None:
    """Controls main program flow"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        choice = main_menu()

        if choice == "1000":
            print("Goodbye!")
            return

        elif choice in menu_map:
            submenu_func = menu_map[choice]
            handle_submenu(choice, submenu_func, cursor)
        else:
            print("Invalid choice!")
            input("\nPress Enter to continue...\n")


def handle_submenu(flag, submenu_func, cursor) -> None:
    """Handles submenu logic dynamically"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        sub_choice = submenu_func()

        if sub_choice == "100":  # back to main
            break

        # Dispatch based on top-level flag (1=View, 2=Insert, etc.)
        if flag == "1":
            view_dispatch(sub_choice, cursor)
        elif flag == "2":
            insert_dispatch(sub_choice, cursor)
        elif flag == "3":
            update_dispatch(sub_choice, cursor)
        elif flag == "4":
            delete_dispatch(sub_choice, cursor)
        elif flag == "5":
            search_dispatch(sub_choice, cursor)
        elif flag == "6":
            reports_dispatch(sub_choice, cursor)
        else:
            print("Invalid submenu flag.")

        input("\nPress Enter to continue...\n")

# dispatch subwindows:
def view_dispatch(choice, cursor) -> None:
    if choice == "1":
        show_all_upcoming_flights(cursor)
    elif choice == "2":
        view_passenger_list(cursor)
    elif choice == "3":
        view_flight_crew(cursor)
    else:
        print("Invalid option in View menu.")

def insert_dispatch(choice, cursor) -> None:
    if choice == "1":
        add_new_ticket(cursor)
    elif choice == "2":
        add_new_flight(cursor)
    elif choice == "3":
        add_new_employee(cursor)
    else:
        print("Invalid option in Insert menu.")

def update_dispatch(choice, cursor) -> None:
    if choice == "1":
        update_flight_status(cursor)
    elif choice == "2":
        update_salaries_by_position(cursor)
    else:
        print("Invalid option in Update menu.")

def delete_dispatch(choice, cursor) -> None:
    if choice == "1":
        fire_employee(cursor)
    elif choice == "2":
        cancel_ticket(cursor)
    elif choice == "3":
        cancel_flight(cursor)
    else:
        print("Invalid option in Delete menu.")

def search_dispatch(choice, cursor) -> None:
    if choice == "1":
        print("Function to search flight by ID not implemented yet.")
    elif choice == "2":
        print("Function to search passenger by name not implemented yet.")
    elif choice == "3":
        search_employee(cursor) 
    elif choice == "4":
        find_cheapest_flights_on_route(cursor)      # will give the top 5 flights.
    else:
        print("Invalid option in Search menu.")

def reports_dispatch(choice, cursor) -> None:
    if choice == "1":
        get_flight_duration(cursor)
    elif choice == "2":
        occupancy_vs_price_report(cursor)
    elif choice == "3":
        avg_ticket_price_on_route(cursor)
    elif choice == "4":
        show_flight_revenue_report(cursor)
    elif choice == "5":
        view_flight_status_log(cursor)
    else:
        print("Invalid option in Reports menu.")