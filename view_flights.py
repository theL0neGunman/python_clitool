
import tabulate
import inquirer
import sys


def view_predefined(cur, con):
    options = [("view by same Destination","a"),
                   ("view by departure date", "b"),
                   ("view by arrival date", "c"),
                   ("view by departure time", "d"),
                   ("view by arrival time", "e"),
                   ("view by  status", "f"),
                   ("view flights with same pilot id", "g"),
                   ("Back to main menu", "h")
                   ]
    
    menu_options = [
        inquirer.List("option",
             message="Please select type of predefined view",
             choices= options),
    ]
    while True:
        opts = inquirer.prompt(menu_options)
        opt = opts['option']
        
        if opt == "a":
            view_same_desti(cur)
        elif opt == "b":
            view_by_dep_date(cur)
        elif opt == "c":
            view_by_arr_date(cur)
        elif opt == "d":
            view_by_dep_time(cur)
        elif opt == "e":
            view_by_arr_time(cur)
        elif opt == "f":
            view_by_status(cur)
        elif opt == "g":
            view_by_pilot_id(cur)
        elif opt == "h":
            print("Returning to main menu...")
            break
        



def tabulate_results(cur):
    results = cur.fetchall()
    print(results)
    if not results:
        print("No Information was found\n")
        return
    else:
        headers = ["Flight ID", "Flight Name", "Pilot ID", "Pilot Name", "Destination ID", 
               "Departure Time", "Arrival Time", "Departure Date", "Arrival Date", "From Location", "To Location", "Status"]
        print(tabulate.tabulate(results, headers=headers, tablefmt="grid"))



def view_same_desti(cur):
    destination = inquirer.prompt([inquirer.Text('to_loc', message="Enter destination to filter by")])['to_loc']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE d.to_loc = ?;
    """
    cur.execute(query, (destination,))
    tabulate_results(cur)



def view_by_dep_date(cur):
    dep_date = inquirer.prompt([inquirer.Text('dep_date', message="Enter departure date to filter by (YYYY-MM-DD):")])['dep_date']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date ,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE d.dep_date = ?;
    """
    cur.execute(query, (dep_date,))
    tabulate_results(cur)
   

def view_by_arr_date(cur):
    arr_date = inquirer.prompt([inquirer.Text('arr_date', message="Enter arrival date to filter by (YYYY-MM-DD):")])['arr_date']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE d.arr_date = ?;
    """
    cur.execute(query, (arr_date,))
    tabulate_results(cur)
   

def view_by_dep_time(cur):
    dep_time = inquirer.prompt([inquirer.Text('dep_time', message="Enter departure time to filter by (HH:MM):")])['dep_time']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE d.dep_time = ?
    """
    cur.execute(query, (dep_time,))
    tabulate_results(cur)

def view_by_arr_time(cur):
    arr_time = inquirer.prompt([inquirer.Text('arr_time', message="Enter arrival time to filter by (HH:MM):")])['arr_time']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE d.arr_time = ?;
    """
    cur.execute(query, (arr_time,))
    tabulate_results(cur)
    

def view_by_status(cur):
    status = inquirer.prompt([inquirer.Text('status', message="Enter status to filter by:")])['status']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE s.status = ?;
    """
    cur.execute(query, (status,))
    tabulate_results(cur)
    

def view_by_pilot_id(cur):
    pilot_id = inquirer.prompt([inquirer.Text('pilot_id', message="Enter pilot ID to view flights:")])['pilot_id']
    
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE s.pilot_id = ?;
    """
    cur.execute(query, (pilot_id,))
    tabulate_results(cur)
    
    
    
    
def view_custom(con, cur):
    cur = con.cursor()
    filter_options = [
        ("Status", "status"),
        ("From location", "from_loc"),
        ("Destination", "to_loc"),
        ("Pilot Id", "pilot_id"),
        ("Arrival Date", "arr_date"),
        ("Departure Date", "dep_date"),
    ]
    
    selected_filters = inquirer.prompt([
        inquirer.Checkbox(
            "filters",
            message="Select filters to apply (2 need to be chose, use spacebar to select)",
            choices=filter_options,
        ),
    ])['filters']
    
    if len(selected_filters) == 0:
        print("You must select at least one choices.")
        return
    elif len(selected_filters) > 2:
        print("You must select a maximum of two choices")
        return

    filter_vals = {}
    for filter_option in selected_filters:
        filter_val = inquirer.prompt([inquirer.Text(filter_option, message=f"Enter value for {filter_option}:")])
        filter_vals[filter_option] = filter_val[filter_option]  
        print(f"filter vlaues: {filter_val}")

    print(filter_vals)
    view_data(cur, filter_vals)



def view_data(cur, filter_vals):
    query = """
    SELECT f.flight_id, f.flight_name, p.pilot_id, p.pilot_name, d.destination_id, 
           d.dep_time, d.arr_time, d.dep_date, d.arr_date,
           d.from_loc, d.to_loc, s.status
    FROM schedule AS s
    JOIN flight AS f ON s.flight_id = f.flight_id
    JOIN pilot AS p ON s.pilot_id = p.pilot_id
    JOIN destination AS d ON f.flight_id = d.flight_id
    WHERE 1=1
    """
    
    params = []
    if 'to_loc' in filter_vals:
        query += " AND d.to_loc = ?"
        params.append(filter_vals['to_loc'])
    if 'from_loc'in filter_vals:
        query += " AND d.from_loc = ?"
        params.append(filter_vals['from_loc'])
    if 'status' in filter_vals:
        query += " AND s.status = ?"
        params.append(filter_vals['status'])
    if 'pilot_id' in filter_vals:
        query += " AND s.pilot_id = ?"
        params.append(filter_vals['pilot_id'])
    if 'dep_date' in filter_vals:
        query += " AND d.dep_date = ?"
        params.append(filter_vals['dep_date'])
    if 'arr_date' in filter_vals:
        query += " AND d.arr_date = ?"
        params.append(filter_vals['arr_date'])
    
    cur.execute(query, tuple(params))
    results = cur.fetchall()

    headers = ["Flight ID", "Flight Name", "Pilot ID", "Pilot Name", "Destination ID", 
               "Departure Time", "Arrival Time", "Departure Date","Arrival Date", "From Location", "To Location", "Status"]
    print(tabulate.tabulate(results, headers=headers, tablefmt="grid"))




def flight_viewing(con):
    cur = con.cursor()
    choices_arr = [
                ("View based on predefined fields","a"),
                ("Custom view", "b"),
                ("Back to main menu", "c")
                   ]
    
    menu_options = [
        inquirer.List("option",
             message="Please select either predefined single field or multi-field viewing options",
             choices= choices_arr,),
    ]
    while True:
        opts = inquirer.prompt(menu_options)
        opt = opts['option']
        if opt == "a":
            view_predefined(cur,con)
        elif opt == "b":
            view_custom(con, cur)
        else:
            print("Returning to main menu...")
            break
        if opt is None:
            print("No selection made. Exiting...")
            sys.exit(0) 
    return opt
    