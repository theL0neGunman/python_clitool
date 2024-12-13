import re
import tabulate

def fetch_data_single(table_name, column_name, cur):
    cur.execute(f"SELECT {column_name} FROM {table_name}")
    col_elements =[]
    flight_id_cols = cur.fetchall()
    for flight_id_col in flight_id_cols:
        col_elements.append(flight_id_col[0])
    return col_elements
    
def check_if_is_empty(answers, error_name):
    is_not_empty = False
    for _, val in  answers.items():
        if val is None or val.strip() == '':
            error_name ="No input was recorded in one or all of the prompts. Returning to the menu..."
            is_not_empty = True
    return is_not_empty, error_name


def flight_table_validation(flight_id, flight_name, is_valid, error_name, flight_ids):
    flight_id_pattern = r"^VR(10[1-9]|1[1-9][0-9]|[2-9][0-9]{2,})$"
    if not re.match(flight_id_pattern, flight_id):
        error_name = "Flight id should follow format and numbering should be greater than 100"
        is_valid = False
    if flight_id in flight_ids:
        error_name = f"Flight ID {flight_id} already exists. Please choose another ID."
        is_valid = False
    return is_valid, error_name


def pilot_table_validation(pilot_id, pilot_name, is_valid, sub_errname, pilot_ids):
    pilot_id_pattern = r"^PR(10[1-9]|1[1-9][0-9]|[2-9][0-9]{2,})$"
    if not re.match(pilot_id_pattern, pilot_id):
        is_valid = False
        sub_errname = "Pilot id should follow format and numbering should be greater than 100"
    if pilot_id in pilot_ids:
        sub_errname = f"Flight ID {pilot_id} already exists. Please choose another ID."
        is_valid = False
    return is_valid, sub_errname


def destination_table_validation(destination_id,dep_time, arr_time,dep_date,arr_date,destination_ids, is_valid, sub_errname):
    dest_id_pattern = r"^UK(100[1-9]|10[1-9][0-9]|1[1-9][0-9]{2,}|[2-9][0-9]{3,})$"
    time_pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9]\s?(am|pm)$"
    date_pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
    if not re.match(dest_id_pattern, destination_id):
        sub_errname = "Destination ID needs to start with UK.. as per company policy and not numbering should not be less than 1000"
        is_valid = False
    elif not re.match(time_pattern, arr_time) or not re.match(time_pattern, dep_time):
        is_valid = False
        sub_errname = "Time should be in the format of HH:MM:SS am/pm"
    elif not re.match(date_pattern, dep_date) or not re.match(date_pattern, arr_date):
        is_valid =False
        sub_errname = "Date should be in the format of YYYY-MM-DD"
    if destination_id in destination_ids:
        sub_errname = f"Flight ID {destination_id} already exists. Please choose another ID."
        is_valid = False
    return is_valid, sub_errname





def get_full_schedule(cur):
    print("Showing full schedule...")
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
    else:
        headers_schedule = [
            "Flight Id", "Flight Name", "Pilot Id", "Pilot Name",
            "Destination ID", "Dep Time", "Arr Time", "Dep to Arr Date", 
            "From Location", "To Location", "Status"
        ]

        print(tabulate.tabulate(schedule_data, headers=headers_schedule, tablefmt="grid"))