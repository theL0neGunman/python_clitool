import typer
import sqlite3

con = sqlite3.connect("tutorial.db")

app = typer.Typer()

cur = con.cursor()


def main(
create: str = typer.Option(..., prompt=True)
):
    if create == "create":
        cur.execute("CREATE TABLE movie(title, year, score)")




if __name__ == '__main__':
    typer.run(main)


