

def fetch_data_single(table_name, column_name, cur):
    cur.execute(f"SELECT {column_name} FROM {table_name}")
    col_elements =[]
    flight_id_cols = cur.fetchall()
    for flight_id_col in flight_id_cols:
        print(f"type of olfnskfnak: {type(flight_id_col[0])}")
        col_elements.append(flight_id_col[0])
    return col_elements
    