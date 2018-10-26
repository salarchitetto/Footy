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

def add_data(database, directory):
    """

    :param database:
    :param file_path:
    :return:
    """
    db = sqlite3.connect(database)
    # directory = str(directory, 'utf-8')
    print(directory)
    print(type(directory))
    files = os.listdir(directory)
    file_path = []

    for x in files:
        file_path.append(directory + "\\" + x)

    for x in file_path:
        with open(x, 'r') as file, db:
            content = csv.DictReader(file, delimiter =',')
            print('***************************************')
            print('Working on uploading data for: ' + str(x))
            cursor = db.cursor()


            for column in content:
                date = str(column['Date'])
                home_team = str(column["HomeTeam"])
                away_team = str(column["AwayTeam"])
                home_team_goals =column['FTHG']
                away_team_goals = column['FTAG']
                full_time_result = str(column['FTR'])
                ht_home_goals = column['HTHG']
                ht_away_goals = column['HTAG']
                ht_result = str(column['HTR'])
                home_team_shots = column['HS']
                away_team_shots = column['AS']
                home_team_shot_tar = column['HST']
                away_team_shot_tar = column['AST']
                home_corner = column['HC']
                away_corner = column['AC']
                home_foul = column['HF']
                away_foul = column['AF']
                home_yellow = column['HY']
                away_yellow = column['AY']
                home_red = column['HR']
                away_red = column["AR"]

                cursor.execute('''insert into footy_matches values (:date, :home_team, :away_team, :home_team_goals, :away_team_goals,
                :full_time_results, :ht_home_goals, :ht_away_goals, :ht_result, :home_team_shots,
                :away_team_shots, :home_team_shot_tar, :away_team_shot_tar, :home_corner, :away_corner,
                :home_foul, :away_foul, :home_yellow, :away_yellow, :home_red, :away_red)''',\

                    {'date' :date,'home_team' :home_team, 'away_team' :away_team, 'home_team_goals': home_team_goals,
                     'away_team_goals' :away_team_goals, 'full_time_results' :full_time_result,
                     'ht_home_goals' :ht_home_goals, 'ht_away_goals' :ht_away_goals, 'ht_result' :ht_result,
                     'home_team_shots' :home_team_shots, 'away_team_shots' :away_team_shots,
                     'home_team_shot_tar' :home_team_shot_tar, 'away_team_shot_tar' : away_team_shot_tar,
                     'home_corner' :home_corner , 'away_corner' :away_corner, 'home_foul' : home_foul,
                     'away_foul' :away_foul, 'home_yellow' :home_yellow, 'away_yellow' :away_yellow,
                     'home_red' :home_red, 'away_red' :away_red})

            print('Finished uploading data for ' + str(x))
            print('***************************************')

