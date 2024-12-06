
import inquirer
import tabulate
import sys
import sqlite3


def update_dest(cur, con):
    print("Fetching pilot details")
    cur.execute("""
                SELECT * FROM pilot
                """)
    pilot_data = cur.fetchall()
    if not pilot_data:
        print("No pilots found.")
        return None

    headers = ["Pilot ID", "Pilot Name"]
    print(tabulate.tabulate(pilot_data, headers=headers, tablefmt="grid"))
    print("Enter the corresponding flight id from the list of pilots")
    ques = [
        inquirer.Text('pilot_id', message="Enter the pilot id"),
    ]
    answers = inquirer.prompt(ques)
    selected_pilot_id = answers['pilot_id']
    print(f"Selected pilot id: {selected_pilot_id}")
    print("Fetching flight data related to pilot...")
    query_flight = """SELECT f.flight_id, f.flight_name, d.to_loc
                    FROM flight AS f
                    JOIN schedule AS s ON f.flight_id = s.flight_id
                    JOIN destination AS d ON f.flight_id = d.flight_id
                    WHERE s.pilot_id = ?;
                """
                
    cur.execute(query_flight, (selected_pilot_id,))
    flight_data = cur.fetchall()
    if not flight_data:
        print("No flights found for the selected pilot.")
        
    headers_flights = ["Flight ID", "Flight Name", "To Location"]
    print(tabulate.tabulate(flight_data, headers=headers_flights, tablefmt="grid"))

    ques_flight = [
    inquirer.Text('flight_id', message="Enter the flight id from the above list"),
    inquirer.Text('new_destination', message="Enter the new destination (to_loc)")
    ]
    
    flight_answers = inquirer.prompt(ques_flight)
    selected_flight_id = flight_answers['flight_id']
    new_destination = flight_answers['new_destination']
    print("Updating the destination...")
    query_update_destination = """
    UPDATE destination
    SET to_loc = ?
    WHERE flight_id = ?;
    """
    try:
        cur.execute(query_update_destination, (new_destination, selected_flight_id))
        con.commit()
        print("Destination updated successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred while updating the destination: {e}")
           


def update_loc(cur, con):
    print("Fetching pilot details")
    cur.execute("""
                SELECT * FROM pilot
                """)
    pilot_data = cur.fetchall()
    if not pilot_data:
        print("No pilots found.")
        return None

    headers = ["Pilot ID", "Pilot Name"]
    print(tabulate.tabulate(pilot_data, headers=headers, tablefmt="grid"))
    print("Enter the corresponding flight id from the list of pilots")
    ques = [
        inquirer.Text('pilot_id', message="Enter the pilot id"),
    ]
    answers = inquirer.prompt(ques)
    selected_pilot_id = answers['pilot_id']
    print(f"Selected pilot id: {selected_pilot_id}")
    print("Fetching flight data related to pilot...")
    query_flight = """SELECT f.flight_id, f.flight_name, d.from_loc
                    FROM flight AS f
                    JOIN schedule AS s ON f.flight_id = s.flight_id
                    JOIN destination AS d ON f.flight_id = d.flight_id
                    WHERE s.pilot_id = ?;
                """
                
    cur.execute(query_flight, (selected_pilot_id,))
    flight_data = cur.fetchall()
    if not flight_data:
        print("No flights found for the selected pilot.")
        
    headers_flights = ["Flight ID", "Flight Name", "To Location"]
    print(tabulate.tabulate(flight_data, headers=headers_flights, tablefmt="grid"))

    ques_flight = [
    inquirer.Text('flight_id', message="Enter the flight id from the above list"),
    inquirer.Text('new_from', message="Enter the new from location")
    ]
    
    flight_answers = inquirer.prompt(ques_flight)
    selected_flight_id = flight_answers['flight_id']
    new_from = flight_answers['new_from']
    print("Updating the From Location...")
    query_update_destination = """
    UPDATE destination
    SET from_loc = ?
    WHERE flight_id = ?;
    """
    try:
        cur.execute(query_update_destination, (new_from, selected_flight_id))
        con.commit()
        print("From Location Updated updated successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred while updating the From Location: {e}")

def update_sch(cur, con):
    return 0


def flight_info_updation(con):
    cur = con.cursor()
    choices_arr = [("Update destination","a"),
                   ("Update from location", "b"),
                   ("Update pilot schedule","c"), 
                   ("Back to main menu", "d")
                   ]
    
    menu_options = [
        inquirer.List("option",
             message="Selct what to update ",
             choices= choices_arr,),
    ]
    while True:
        opts = inquirer.prompt(menu_options)
        opt = opts['option']
        if opt == "a":
            update_dest(cur,con)
        elif opt == "b":
            update_loc(cur,con)
        elif opt == "c":
            update_sch(cur, con)
        else:
            print("Returning to main menu...")
            break
    if opt is None:
        print("No selection made. Exiting...")
        sys.exit(0) 
    return opt