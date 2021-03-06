"""
http://www.football-data.co.uk
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

###############
#For Console###
###############

def create_conn(path):
    try:
        conn = sqlite3.connect(path)
        return conn
    except Error as e:
        print(e)
    finally:
        conn.close()
    return None

################

def create_table(conn, create_table_footy):

    try:
        c = conn.cursor()
        c.execute(create_table_footy)
    except Error as e:
        print(e)

def main():


    footy = """
          CREATE TABLE IF NOT EXISTS Scotland (
              date NOT NULL,
              home_team text NOT NULL,
              away_team text NOT NULL,
              home_team_goals integer NOT NULL,
              away_team_goals integer NOT NULL,
              full_time_results text NOT NULL,
              ht_home_goals integer NOT NULL,
              ht_away_goals integer NOT NULL,
              ht_result text NOT NULL,
              home_team_shots integer DEFAULT NULL,
              away_team_shots integer DEFAULT NULL,
              home_team_shot_tar integer DEFAULT NULL,
              away_team_shot_tar integer DEFAULT NULL,
              home_corner integer DEFAULT NULL, 
              away_corner integer DEFAULT NULL, 
              home_foul integer DEFAULT NULL,
              away_foul integer DEFAULT NULL, 
              home_yellow integer DEFAULT NULL, 
              away_yellow integer DEFAULT NULL,
              home_red integer DEFAULT NULL, 
              away_red integer DEFAULT NULL
          );
      """
    conn = create_connection()

    if conn is not None:

        create_table(conn, footy)
        print("table created!")
    else:
        print("Looks like theres something wrong with the connection!")

if __name__ == '__main__':
   main()
