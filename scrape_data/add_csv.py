import pandas as pd
import sqlite3
from scrape_data.create_db import *
import csv

conn = create_connection()
def grab_data(conn):
    """

    :param conn: connection used to get into footy db
    :return: pandas dataframe
    """

    matches = """
        SELECT *
        FROM footy_matches
    """

    df = pd.read_sql(matches, conn)

    return df

def add_data(database, file_path):
    """

    :param database:
    :param file_path:
    :return:
    """
    db = sqlite3.connect(database)
    print(db)
    with open(file_path, 'r') as file, db:
        content = csv.DictReader(file, delimiter =',')

        cursor = db.cursor()

        for column in content:
            home_team = str(column["HomeTeam"])
            away_team = str(column["AwayTeam"])
            home_team_goals = int(column['FTHG'])
            away_team_goals = int(column['FTAG'])
            full_time_result = str(column['FTR'])
            ht_home_goals = int(column['HTHG'])
            ht_away_goals = int(column['HTAG'])
            ht_result = str(column['HTR'])
            home_team_shots = int(column['HS'])
            away_team_shots = int(column['AS'])
            home_team_shot_tar = int(column['HST'])
            away_team_shot_tar = int(column['AST'])
            home_corner = int(column['HC'])
            away_corner = int(column['AC'])
            home_foul = int(column['HF'])
            away_foul = int(column['AF'])
            home_yellow = int(column['HY'])
            away_yellow = int(column['AY'])
            home_red = int(column['HR'])
            away_red = int(column["AR"])

            cursor.execute('''insert into footy_matches values ( :home_team, :away_team, :home_team_goals, :away_team_goals,
            :full_time_results, :ht_home_goals, :ht_away_goals, :ht_result, :home_team_shots,
            :away_team_shots, :home_team_shot_tar, :away_team_shot_tar, :home_corner, :away_corner,
            :home_foul, :away_foul, :home_yellow, :away_yellow, :home_red, :away_red)''',\

                {'home_team' :home_team, 'away_team' :away_team, 'home_team_goals': home_team_goals,
                 'away_team_goals' :away_team_goals, 'full_time_results' :full_time_result,
                 'ht_home_goals' :ht_home_goals, 'ht_away_goals' :ht_away_goals, 'ht_result' :ht_result,
                 'home_team_shots' :home_team_shots, 'away_team_shots' :away_team_shots,
                 'home_team_shot_tar' :home_team_shot_tar, 'away_team_shot_tar' : away_team_shot_tar,
                 'home_corner' :home_corner , 'away_corner' :away_corner, 'home_foul' : home_foul,
                 'away_foul' :away_foul, 'home_yellow' :home_yellow, 'away_yellow' :away_yellow,
                 'home_red' :home_red, 'away_red' :away_red})


insert_data = add_data("add db", "add path")

test = grab_data(conn)
print(test)
