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

def main_controller(cursor):
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


def handle_submenu(flag, submenu_func, cursor):
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

# view dispatch:
def view_dispatch(choice, cursor):
    if choice == "1":
        show_all_airports(cursor)
    elif choice == "2":
        show_all_upcoming_flights(cursor)
    elif choice == "3":
        view_passenger_list(cursor)
    else:
        print("Invalid option in View menu.")