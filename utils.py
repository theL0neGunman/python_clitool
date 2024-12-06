import re

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
    number_pattern = r"^(?:10[1-9]|[1-9]\d{3,}|\d{3,})$"
    if not re.match(number_pattern, flight_id):
        is_valid = False
        error_name = 'Enter a number for flight id and it should be greater than 100'
    
    val_int = int(flight_id.strip())
    if val_int in flight_ids:
        error_name = f"Flight ID {flight_id} already exists. Please choose another ID."
        is_valid = False
    return is_valid, error_name


def pilot_table_validation(pilot_id, pilot_name, is_valid, sub_errname, pilot_ids):
    number_pattern = r"^(?:100[1-9]|10[1-9]\d|1[1-9]\d{2}|\d{4,})$"
    if not re.match(number_pattern, pilot_id):
        is_valid = False
        sub_errname = "Enter pilot id in number format and it should be greater than 1000"
    int_val = int(pilot_id.strip())
    if int_val in pilot_ids:
        sub_errname = f"Flight ID {pilot_id} already exists. Please choose another ID."
        is_valid = False
    return is_valid, sub_errname


def destination_table_validation(destination_id,time, date, destination_ids, is_valid, sub_errname):
    dest_id_pattern = r"^UK\w*$"
    time_pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9](:[0-5][0-9])?\s?(AM|PM)$"
    date_pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
    if not re.match(dest_id_pattern, destination_id):
        sub_errname = "Destination ID needs to start with UK.. as per company policy"
    elif not re.match(time_pattern, time):
        is_valid = False
        sub_errname = "Time should be in the format of HH:MM:SS AM/PM"
    elif not re.match(date_pattern, date):
        is_valid =False
        sub_errname = "Date should be in the format of YYYY-MM-DD"
    if destination_id in destination_ids:
        sub_errname = f"Flight ID {destination_id} already exists. Please choose another ID."
        is_valid = False
    return is_valid, sub_errname