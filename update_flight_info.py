
import inquirer
import tabulate
import sys
import sqlite3
from utils import get_full_schedule

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
    print("Showing full schedule of pilots...")
    query_for_schedule = """
        SELECT 
        f.flight_id,
        f.flight_name,
        p.pilot_id,
        p.pilot_name,
        d.destination_id,
        d.dep_time,
        d.arr_time,
        d.dep_date || ' to ' || d.arr_date AS dep_arr_date,
        d.from_loc,
        d.to_loc,
        s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id;
    """
    cur.execute(query_for_schedule)
    schedule_data = cur.fetchall()

    if not schedule_data:
        print("No schedule data found.")
        return
    else:
        headers_schedule = [
            "Flight Id", "Flight Name", "Pilot Id", "Pilot Name",
            "Destination ID", "Dep Time", "Arr Time", "Dep to Arr Date", 
            "From Location", "To Location", "Status"
        ]

        print(tabulate.tabulate(schedule_data, headers=headers_schedule, tablefmt="grid"))
    ques_pilot = [
            inquirer.Text('pilot_id', message="Enter the pilot ID")
        ]
    pilot_answers = inquirer.prompt(ques_pilot)
    selected_pilot_id = pilot_answers['pilot_id']
    query_flights = """
        SELECT 
        f.flight_id,
        f.flight_name,
        s.pilot_id,
        d.to_loc,
        s.status
        FROM flight AS f
        JOIN schedule AS s ON f.flight_id = s.flight_id
        JOIN destination AS d ON f.flight_id = d.flight_id
        WHERE s.pilot_id = ?;
        """
    cur.execute(query_flights, (selected_pilot_id,))
    flight_data = cur.fetchall()

    if not flight_data:
        print(f"No flights found for pilot ID {selected_pilot_id}.")
        return

    headers_flight = ["Flight Id", "Flight Name", "Pilot Id", "To ", "Status"]
    print(tabulate.tabulate(flight_data, headers=headers_flight, tablefmt="grid"))

    ques_flight = [
        inquirer.Text('flight_id', message="Enter the flight ID to modify from the above list")
    ]
    flight_answers = inquirer.prompt(ques_flight)
    selected_flight_id = flight_answers['flight_id']

    fields = [
            "arr_date", "dep_date", "arr_time", "dep_time",
            "from_loc", "to_loc", "flight_name", "status"
        ]

    ques_field = [
        inquirer.List(
                'field',
                message="Which field would you like to update?",
                choices=fields
            ),
        inquirer.Text('new_value', message="Enter the new value for the selected field")
        ]
    field_answers = inquirer.prompt(ques_field)
    selected_field = field_answers['field']
    new_value = field_answers['new_value']

    if selected_field in ["arr_date", "dep_date", "arr_time", "dep_time", "from_loc", "to_loc"]:
            query_update = f"""
            UPDATE destination
            SET {selected_field} = ?
            WHERE flight_id = ?;
            """
    elif selected_field == 'status':
        query_update = """UPDATE schedule SET status = ? WHERE flight_id = ?"""
    elif selected_field == "flight_name":
            # Update the flight table
            query_update = """
            UPDATE flight
            SET flight_name = ?
            WHERE flight_id = ?;
            """
    else:
        print("Invalid field selected.")
        return

    try:
        cur.execute(query_update, (new_value, selected_flight_id))
        con.commit()
        print(f"Successfully updated {selected_field} to '{new_value}' for flight ID {selected_flight_id}.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


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