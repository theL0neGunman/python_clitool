import os
import sys
import sqlite3
import typer
sys.path.append(os.path.realpath("."))
import inquirer
from pyfiglet import Figlet
from add_flight import flight_addition
from view_flights import flight_viewing
from update_destination import desitnation_updation
from view_schedule import pilot_schedule
from update_flight_info import flight_info_updation
from assign_pilot import assigning_pilot

app = typer.Typer()

file_db ="planesdb.db"

def mainHeading():
    fig_font = Figlet(font="cosmic")
    heading = fig_font.renderText("Vistara")
    print(heading)
    print("-"*70)


def showMenu():
    path_exists = os.path.exists(file_db)
    if not path_exists:
        choices_arr = [("Create a Database","o"), ("Exit Application", "ex")]
    else:
        choices_arr = [("Add a flight","a"), ("View Flights by...","b"),
                      ("Update flight info","d"),("Assign a Pilot to a flight", "e"),
                      ("View Pilot Schedule", "f"), ("Update Destination", "g"), ("Exit Application", "h")]
    menu_options = [
        inquirer.List("option",
             message="Welcome to Vistara Airlines database, what would you like to do?",
             choices= choices_arr,),

    ]
    main_options = inquirer.prompt(menu_options)
    if main_options is None:
        print("No selection made. Exiting...")
        sys.exit(0) 
    return main_options["option"]


@app.command()
def main():
    mainHeading()
    option = showMenu()
    if option == 'o':
        db_connect = sqlite3.connect("planesdb.db")
        print("Database Created exiting....")
        db_connect.close()
        sys.exit(0)
    elif option == "ex":
        print("No selection made. Exiting...")
        sys.exit(0)
    else:
        db_connect = sqlite3.connect("planesdb.db")
        if option == "a":
            flight_addition(db_connect)
        elif option == "b":
            flight_viewing(db_connect)
        elif option == "d":
            flight_info_updation(db_connect)
        elif option == "e":
            assigning_pilot(db_connect)
        elif option == "f":
            pilot_schedule(db_connect)
        elif option == "g":
            desitnation_updation(db_connect) 
        elif option == "h":
            print("No selection made. Exiting...")
            db_connect.close()
            sys.exit(0)


if __name__ == '__main__':
    typer.run(main)


