import os
import pandas as pd
from collections import *
from scrape_data.queries import *
from scrape_data.mysql_connect import *

def choose_team(country_name):
    """
    This function returns a list of the teams per country and will
    populate a drop down in the callbacks
    :param country_name:
    :return: list of team names per country
    """
    #connecting to DB
    conn = footy_connect()

    #grabbing dataframe
    df = grab_team_names(conn, country_name)

    conn.close()

    return df

def home_vs_away(df, team_name):
    """

    :param df: dataframe containing information to determine home or
    away wins
    :return: df
    """


    outcome = []
    for index, row in df.iterrows():
        if row["home_team"] == team_name and row["full_time_results"] == 'H':
            outcome.append("win")
        elif row['home_team'] == team_name and row['full_time_results'] == 'A':
            outcome.append('lose')
        elif row['away_team'] == team_name and row['full_time_results'] == 'A':
            outcome.append('win')
        elif row['away_team'] == team_name and row['full_time_results'] == 'H':
            outcome.append('lose')
        elif row["away_team_goals"] == row["home_team_goals"]:
            outcome.append("draw")

    df['outcome'] = outcome

    return df

def date_conversion(df):
    """
    converting date column into datetime values as it is
    only a list of strings.
    :param df: dataframe to manipulate
    :return: datatrame
    """
    #changing dataframe series to datetime column
    df['date'] = pd.to_datetime(df['date'])

    #converting dates to years
    df['date'] = df['date'].dt.year

    return df

def run_win_pct(team_name):
    """
    Function that calculates a teams winning percentage Year over Year
    (YoY)
    Calculation:
        number of wins by the total number of competitions.
        Then multiply by 100 = win percentage.
    :param team_name: Takes in the state of the team_names dropdown
    :return:a dataframe That returns winning percentages for specific teams
    """
    print('working')

    conn = footy_connect()
    df = grab_data(conn)

    team_name = team_name.title()

    df_home = df[df['home_team'] == team_name]
    df_away = df[df['away_team'] == team_name]

    frames = [df_home,df_away]
    df_fill = pd.concat(frames)

    df_fill = home_vs_away(df_fill, team_name)
    df = date_conversion(df_fill)

    home_matches = df[df['home_team'] == team_name]
    away_matches = df[df['away_team'] == team_name]

    home_matches = home_matches.drop(columns = ['away_team'])
    away_matches = away_matches.drop(columns = ['home_team'])

    print('calculating pcts')

    #wins per season
    home_team_win = home_matches.groupby(["home_team","date"])["outcome"].apply(
        lambda x: x[x.str.contains("win")].count()).reset_index()
    away_team_win = away_matches.groupby(['away_team','date'])['outcome'].apply(
        lambda x: x[x.str.contains('win')].count()).reset_index()

    home_team_loss = home_matches.groupby(['home_team','date'])['outcome'].apply(
        lambda x: x[x.str.contains('lose')].count()).reset_index()
    away_team_loss = away_matches.groupby(['away_team','date'])['outcome'].apply(
        lambda x: x[x.str.contains('lose')].count()).reset_index()

    home_team_tie = home_matches.groupby(['home_team','date'])['outcome'].apply(
        lambda x: x[x.str.contains('draw')].count()).reset_index()
    away_team_tie = away_matches.groupby(['away_team','date'])['outcome'].apply(
        lambda x: x[x.str.contains('draw')].count()).reset_index()

    #matches played per season
    searchFor = ['win','lose','draw']
    matches_home = home_matches.groupby(['home_team','date'])['outcome'].apply(
        lambda x: x[x.str.contains('|'.join(searchFor))].count()).reset_index()
    matches_away = away_matches.groupby(['away_team', 'date'])['outcome'].apply(
        lambda x: x[x.str.contains('|'.join(searchFor))].count()).reset_index()

    match_numbers = matches_home.merge(matches_away, how='left', left_on='date', right_on='date')

    print('finalizing')
    loss_merge = home_team_loss.merge(away_team_loss, how='left', left_on='date', right_on='date')
    tie_merge = home_team_tie.merge(away_team_tie, how='left', left_on='date', right_on='date')
    fin = home_team_win.merge(away_team_win, how = 'left', left_on='date', right_on='date')

    fin['Total Wins'] = fin['outcome_x'] + fin['outcome_y']
    fin['Total Losses'] = loss_merge['outcome_x'] + loss_merge['outcome_y']
    fin['Total Draws'] = tie_merge['outcome_x'] + tie_merge['outcome_y']
    fin['Total Matches'] = match_numbers['outcome_x'] + match_numbers['outcome_y']

    fin['Win PCT'] = (fin['Total Wins'] / fin['Total Matches'] * 100).round(2)
    fin['Loss PCT'] = (fin['Total Losses'] / fin['Total Matches'] * 100).round(2)
    fin['Draw PCT'] = (fin['Total Draws'] / fin['Total Matches'] * 100).round(2)

    #home match percentage
    fin['Home Win PCT'] = (home_team_win['outcome'] / matches_home['outcome'] * 100).round(2)
    fin['Away Win PCT'] = (away_team_win['outcome'] / matches_away['outcome'] * 100).round(2)

    fin['Home Loss PCT'] = (home_team_loss['outcome'] / matches_home['outcome'] * 100).round(2)
    fin['Away Loss PCT'] = (away_team_loss['outcome'] / matches_away['outcome'] * 100).round(2)

    conn.close()

    return fin


