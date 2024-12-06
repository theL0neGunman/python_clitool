import inquirer
import os
import sys
import sqlite3
from utils import fetch_data_single, check_if_is_empty,flight_table_validation, destination_table_validation, pilot_table_validation
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
    is_not_empty, error_name = check_if_is_empty(answers, error_name)
    if not is_not_empty:
        is_valid = True
        flight_id = answers["flight_id"]
        flight_name = answers["flight_name"]
        is_valid, error_name = flight_table_validation(flight_id, flight_name, is_valid, error_name, flight_ids)
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
            
        
def get_schedule_id(cur):
    cur.execute('SELECT MAX(schedule_id) FROM schedule')
    res = cur.fetchone()[0]
    if res:
        prefix = res[:3]
        number = int(res[3:])
        next_number = number + 1
        return f"{prefix}{next_number:03}"
    else:
        return "SCH101"
    
    


def write_in_db(option_a,status, tables, con, cur, flight_id, flight_name, destination_id,dep_time, arr_time,dep_date,
                arr_date, from_location, to_location,pilot_id, pilot_name):
    for table in tables:
        if table == 'flight':
            query = "INSERT INTO flight (flight_id, flight_name) VALUES (?, ?);"
            cur.execute(query, (flight_id, flight_name))
        elif table == 'pilot' and not option_a:
                query = "INSERT INTO pilot (pilot_id, pilot_name) VALUES (?, ?);"
                cur.execute(query, (pilot_id, pilot_name))
        elif table == 'destination':
                query = """INSERT INTO destination (flight_id, destination_id,dep_time ,arr_time,dep_date ,arr_date, 
                            from_loc, to_loc) VALUES (?, ? , ?, ?, ?, ?,?, ?);
                         """ 
                cur.execute(query, (flight_id, destination_id,dep_time ,arr_time,dep_date ,arr_date, from_location, to_location))
        elif table == 'schedule':
                schedule_id = get_schedule_id(cur)
                print(f"Schedule id: {schedule_id}")
                query = "INSERT INTO schedule (schedule_id, flight_id, destination_id, pilot_id, status) VALUES (?, ?, ?, ?, ?)"
                cur.execute(query, (schedule_id, flight_id, destination_id, pilot_id, status))
    
    con.commit()
    print("Data successfully added to the table")
    
         
def get_inq_opts(option_a):
    ques = [
                inquirer.Text('flight_id', message="Enter a new Flight Id (format: VR101)",),
                inquirer.Text('flight_name', message="Enter the flight name"),
                inquirer.Text('destination_id', message="Enter a new Route Id (format: UK1001)",),
                inquirer.Text('dep_time', message="Enter the departure time in (format: HH:MM am/pm)"),
                inquirer.Text('arr_time', message="Enter the arrival time in (format: HH:MM am/pm)"),
                inquirer.Text('dep_date', message="Enter the departure date in (format:YYYY-MM-DD)",),
                inquirer.Text('arr_date', message="Enter the arrival date in (format:YYYY-MM-DD)",),
                inquirer.Text('from_loc', message="Enter from location"),
                inquirer.Text('to_loc', message="Enter to location",),
                inquirer.Text('status', message='Enter flight status either ACTIVE, CANCELLED OR DELAYED (case sensitive)')
                 ]
    if not option_a:
        ques.append([inquirer.Text('pilot_id', message="Enter a new Pilot id (format:PR101)",),
                inquirer.Text('pilot_name', message="Enter the Pilot name"),])
    return ques
    

def create_along_with_route(con):
    cur = con.cursor()
    choices_arr = [("Choose pilots from pre-existing list","a"),
                   ("Create by entering a new pilot Name","b")]

    sub_menu_options = [
        inquirer.List("option",
             message="Choose Pilots from preexisting list",
             choices= choices_arr,),
    ]
    options = inquirer.prompt(sub_menu_options)
    while True:
        selected_optn = options["option"]
        if selected_optn == 'a':
            print("Fetching unassigned pilot names")
            cur.execute("""SELECT p.pilot_name, p.pilot_id FROM pilot p LEFT JOIN 
                        schedule s ON p.pilot_id = s.pilot_id WHERE s.schedule_id IS NULL;""")
            res = cur.fetchall()
            print(f"Result {res}")
            pilot_dict = {pilot[0]: pilot[1] for pilot in res}
            options = [inquirer.List('selected_name', message="Select a pilot name", choices=list(pilot_dict.keys()))]
            selec_pilots = inquirer.prompt(options)
            if selec_pilots:
                selected_pilot_name = selec_pilots['selected_name']
                selected_pilot_id = pilot_dict[selected_pilot_name]
                ques = get_inq_opts(True)
                
            answers = inquirer.prompt(ques)
            is_not_empty, error_name = check_if_is_empty(answers, error_name)
            if not is_not_empty:
                sub_errname = ''
                is_valid = True
                flight_ids = fetch_data_single("flight", "flight_id", cur)
                destination_ids = fetch_data_single('destination', "destination_id", cur)
                flight_id = answers["flight_id"]
                flight_name = answers["flight_name"]
                destination_id = answers ["destination_id"]
                dep_time = answers["dep_time"]
                arr_time = answers["dep_time"]
                dep_date = answers["dep_date"]
                status = answers["status"]
                arr_date = answers["arr_date"]
                from_location = answers["from_loc"]
                to_location = answers["to_loc"]
                is_valid, sub_errname = flight_table_validation(flight_id, flight_name, is_valid, sub_errname, flight_ids)
                is_valid, sub_errname = destination_table_validation(destination_id,dep_time, arr_time,dep_date,arr_date,
                                                                     destination_ids, is_valid, sub_errname)

                if not is_valid:
                    print(f"{sub_errname}")
                else:
                    try:
                        tables = ['flight', 'destination', 'schedule']
                        write_in_db(True, status ,tables, con, cur, flight_id, flight_name, destination_id,dep_time, arr_time,dep_date,arr_date,
                                    from_location, to_location, selected_pilot_id)
                        break
                    except sqlite3.Error as e:
                        print(f"Error in writng data to the table: {e}")
                        con.rollback()
            
            break
        elif selected_optn == 'b':
            error_name = ''
            is_not_empty = False
            ques = get_inq_opts(False)
            answers = inquirer.prompt(ques)
            is_not_empty, error_name = check_if_is_empty(answers, error_name)
            if not is_not_empty:
                sub_errname = ''
                is_valid = True
                flight_ids = fetch_data_single("flight", "flight_id", cur)
                pilot_ids = fetch_data_single('pilot', "pilot_id", cur)
                destination_ids = fetch_data_single('destination', "destination_id", cur)
                flight_id = answers["flight_id"]
                flight_name = answers["flight_name"]
                pilot_id = answers["pilot_id"]
                pilot_name = answers["pilot_name"]
                destination_id = answers ["destination_id"]
                dep_time = answers["dep_time"]
                arr_time = answers["dep_time"]
                status = answers["status"]
                dep_date = answers["dep_date"]
                arr_date = answers["arr_date"]
                from_location = answers["from_loc"]
                to_location = answers["to_loc"]
                is_valid, sub_errname = flight_table_validation(flight_id, flight_name, is_valid, sub_errname, flight_ids)
                is_valid, sub_errname = pilot_table_validation(pilot_id, pilot_name, is_valid, sub_errname, pilot_ids)
                is_valid, sub_errname = destination_table_validation(destination_id,dep_time, arr_time,dep_date,arr_date,
                                                                     destination_ids, is_valid, sub_errname)
                if not is_valid:
                    print(f"{sub_errname}")
                else:
                    try:
                        tables = ['flight', 'pilot', 'destination', 'schedule']
                        write_in_db(False, status,tables, con, cur, flight_id, flight_name, destination_id,
                                    dep_time, arr_time,dep_date,arr_date, from_location, to_location,pilot_id, pilot_name)
                        break
                    except sqlite3.Error as e:
                        print(f"Error in writng data to the table: {e}")
                        con.rollback()
            else:
                print(f"{error_name}")
        else:
            print("Something went wrong....")
    
    


def flight_addition(con):
    # Add flight, ask for flight id and flight name
    while True:
        flight_addition_menu_optn = show_flight_menu()
        if flight_addition_menu_optn == "a":
            create_from_scratch(con)
        elif flight_addition_menu_optn == "b":
            create_along_with_route(con)
        elif flight_addition_menu_optn == 'c':
            print("Returning to main menu...")
            break
    return flight_addition_menu_optn
    