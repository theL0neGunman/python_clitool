import os
import sys
import sqlite3
import typer
sys.path.append(os.path.realpath("."))
import inquirer
from pyfiglet import Figlet
from add_flight import flight_addition
from view_flights import flight_viewing
from view_schedule import pilot_schedule
from update_flight_info import flight_info_updation
from delete_func import delete_flight

app = typer.Typer()

file_db ="flightdata.db"

def mainHeading():
    fig_font = Figlet(font="cosmic")
    heading = fig_font.renderText("Vistara")
    print(heading)
    print("-"*70)


def showMenu():
    choices_arr = [  ("Add a flight", "a"),
        ("View Flights by...", "b"),
        ("Update flight info", "c"),
        ("View Pilot Schedule", "d"),
        ("Delete a flight route", "e"),
        ("Exit Application", "f")]
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
    db_connect = sqlite3.connect(file_db)
    while True:
        option = showMenu()
        if option == "a":
            flight_addition(db_connect)
        elif option == "b":
            flight_viewing(db_connect)
        elif option == 'c':
            flight_info_updation(db_connect)
        elif option == "d":
            pilot_schedule(db_connect)
        elif option == 'e':
            delete_flight(db_connect)
        elif option == "f":
            print("No selection made. Exiting...")
            db_connect.close()
            sys.exit(0)
            break


if __name__ == '__main__':
    typer.run(main)


