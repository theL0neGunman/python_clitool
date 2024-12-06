import tabulate
import sqlite3
import inquirer
import re


def delete_flight(con):
    cur = con.cursor()
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
        pilot_id_pattern = r"^PR(10[1-9]|1[1-9][0-9]|[2-9][0-9]{2,})$"
        if not re.match(pilot_id_pattern, selected_pilot_id):
            print("Enter the pilot id according to given format")
            return
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
            con.close()
            return

        headers_flight = ["Flight Id", "Flight Name", "Pilot Id", "To Location", "Status"]
        print(tabulate.tabulate(flight_data, headers=headers_flight, tablefmt="grid"))

        ques_flight = [
            inquirer.Text('flight_id', message="Enter the flight Id to delete from the above list")
        ]
        flight_answers = inquirer.prompt(ques_flight)
        selected_flight_id = flight_answers['flight_id']
        flight_id_pattern = r"^VR(10[1-9]|1[1-9][0-9]|[2-9][0-9]{2,})$"
        if not re.match(flight_id_pattern, selected_flight_id):
            print("Enter the flight id according to given format")
            return
        ques_confirm = [
            inquirer.Confirm('confirm_delete', message=f"Are you sure you want to delete the flight rought with Id {selected_flight_id}?", default=False)
        ]
        confirm_answers = inquirer.prompt(ques_confirm)

        if confirm_answers['confirm_delete']:
            query_delete_destination = """
            DELETE FROM destination
            WHERE flight_id = ?;
            """
            cur.execute(query_delete_destination, (selected_flight_id,))

            query_delete_schedule = """
            DELETE FROM schedule
            WHERE flight_id = ? AND pilot_id = ?;
            """
            cur.execute(query_delete_schedule, (selected_flight_id, selected_pilot_id))


            try:
                con.commit()
                print(f"Successfully deleted the flight with ID {selected_flight_id} and its corresponding schedule.")
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
    return