import inquirer
import os
import sys
import sqlite3
from utils import fetch_data_single
import re




def show_flight_menu():
    choices_arr = [("Create a new flight entry","a"),
                   ("Create a new flight route along with flight entry","b"), ("Back to main menu", "c")]
    menu_options = [
        inquirer.List("option",
             message="Choose type of flight to create",
             choices= choices_arr,),

    ]
    main_options = inquirer.prompt(menu_options)
    if main_options is None:
        print("No selection made. Exiting...")
        sys.exit(0) 
    return main_options["option"]



def create_from_scratch(con):
    cur = con.cursor()
    print("Creating a flight entry....")
    print("Enter the following details")
    ques = [
        inquirer.Text('flight_id', message="Enter the flight ID",),
        inquirer.Text('flight_name', message="Enter the flight name"),
    ]
    error_name = ''
    is_not_empty = False
    answers = inquirer.prompt(ques)
    flight_ids = fetch_data_single("flight", "flight_id", cur)
    print(flight_ids)
    for _, val in  answers.items():
        if val is None or val.strip() == '':
            error_name ="No input was recorded in one or all of the prompts. Returning to the menu..."
            is_not_empty = True
            break
    if not is_not_empty:
        is_valid = True
        flight_id = answers["flight_id"]
        flight_name = answers["flight_name"]
        number_pattern = r"^-?\d+(\.\d+)?$"
        if not re.match(number_pattern, flight_id):
            is_valid = True
        error_name = 'Enter a number for flight id'
    
        val_int = int(flight_id.strip())
        if val_int in flight_ids:
            error_name = f"Flight ID {flight_id} already exists. Please choose another ID."
            is_valid = False
            
    
        if not is_valid:
            print(f"{error_name}")
        else:
            try:
                query = "INSERT INTO flight (flight_id, flight_name) VALUES (?, ?);"
                cur.execute(query, (flight_id, flight_name))
                con.commit()
                print("Data successfully added to the table")
            except sqlite3.Error as e:
                print(f"Error in writng data to the table: {e}")
                con.rollback()
    else:
        print(f"{error_name}")
            
            
            
    
    

def flight_viewing():
    return 0


def flight_info_updation():
    return 0



def flight_addition(con):
    # Add flight, ask for flight id and flight name
    while True:
        flight_addition_menu_optn = show_flight_menu()
        if flight_addition_menu_optn == "a":
            create_from_scratch(con)
        elif flight_addition_menu_optn == "b":
            flight_viewing(con)
        elif flight_addition_menu_optn == 'c':
            print("Returning to main menu...")
            break
    return flight_addition_menu_optn
    