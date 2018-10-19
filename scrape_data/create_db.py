"""

http://www.football-data.co.uk
multitude of CSV's to grab data from.
Create some form of a loop to grab each sheet
and create either a mysql db or sqlite db to
store the data into.

"""

import sqlite3
from sqlite3 import Error
import os

#Creating DB to specific directory

#code to create table

def create_connection(path=eval(os.environ['CONN'])['path']):
    """"
    Attemptin to create the DB in SQLite
    """
    try:
        conn = sqlite3.connect(path)
        print("Connection Made.")
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_footy):

    try:
        c = conn.cursor()
        c.execute(create_table_footy)
    except Error as e:
        print(e)

def main():
    path = "path"

    footy = """
          CREATE TABLE IF NOT EXISTS matches (
              id integer PRIMARY KEY,
              home_team text NOT NULL,
              away_team text NOT NULL,
              home_team_goals integer NOT NULL,
              away_team_goals integer NOT NULL,
              full_time_results text NOT NULL,
              ht_home_goals integer NOT NULL,
              ht_away_goals integer NOT NULL,
              ht_result text NOT NULL,
              attendance integer NULL,
              home_team_shots integer,
              away_team_shots integer,
              home_team_shot_tar integer,
              away_team_shot_tar integer,
              home_woodwork integer,
              away_woodwork integer, 
              home_corner integer, 
              away_corner integer, 
              home_foul integer,
              away_foul integer, 
              home_yellow integer, 
              away_yellow integer,
              home_red integer, 
              away_red integer
          );
      """
    conn = create_connection(path)

    if conn is not None:

        create_table(conn, footy)
    else:
        print("Looks like theres something wrong with the connection!")

if __name__ == '__main__':
   main()
