import os
import pandas as pd
import numpy as np
from collections import *
from scrape_data.queries import *
from scrape_data.mysql_connect import *

def choose_team(country_name, division):
    """
    This function returns a list of the teams per country and will
    populate a drop down in the callbacks
    :param country_name:
    :return: list of team names per country
    """
    #connecting to DB
    conn = footy_connect()

    #grabbing dataframe
    df = grab_team_names(conn, country_name, division)

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

def run_win_pct(team_name, country):
    """
    Function that calculates a teams winning percentage Year over Year
    (YoY)
    Calculation:
        number of wins by the total number of competitions.
        Then multiply by 100 = win percentage.
    :param team_name: Takes in the state of the team_names dropdown
    :return:a dataframe That returns percentages for specific teams
    """
    print('working')

    df = create_seasons_list(country)

    df['home_team'] = df['home_team'].str.lower()
    df['away_team'] = df['away_team'].str.lower()

    team_name = team_name.lower()

    df_home = df[df['home_team'] == team_name]
    df_away = df[df['away_team'] == team_name]

    frames = [df_home,df_away]
    df_fill = pd.concat(frames)

    df = home_vs_away(df_fill, team_name)

    home_matches = df[df['home_team'] == team_name]
    away_matches = df[df['away_team'] == team_name]

    home_matches = home_matches.drop(columns = ['away_team'])
    away_matches = away_matches.drop(columns = ['home_team'])

    print('calculating pcts')

    #wins per season
    home_team_win = home_matches.groupby(["home_team","dateYear"])["outcome"].apply(
        lambda x: x[x.str.contains("win")].count()).reset_index()
    away_team_win = away_matches.groupby(['away_team','dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('win')].count()).reset_index()

    home_team_loss = home_matches.groupby(['home_team','dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('lose')].count()).reset_index()
    away_team_loss = away_matches.groupby(['away_team','dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('lose')].count()).reset_index()

    home_team_tie = home_matches.groupby(['home_team','dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('draw')].count()).reset_index()
    away_team_tie = away_matches.groupby(['away_team','dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('draw')].count()).reset_index()

    #matches played per season
    searchFor = ['win','lose','draw']
    matches_home = home_matches.groupby(['home_team','dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('|'.join(searchFor))].count()).reset_index()
    matches_away = away_matches.groupby(['away_team', 'dateYear'])['outcome'].apply(
        lambda x: x[x.str.contains('|'.join(searchFor))].count()).reset_index()

    #goals for and against

    match_numbers = matches_home.merge(matches_away, how='left', left_on='dateYear', right_on='dateYear')

    print('finalizing')
    loss_merge = home_team_loss.merge(away_team_loss, how='left', left_on='dateYear', right_on='dateYear')
    tie_merge = home_team_tie.merge(away_team_tie, how='left', left_on='dateYear', right_on='dateYear')
    fin = home_team_win.merge(away_team_win, how = 'left', left_on='dateYear', right_on='dateYear')

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

    return fin

def create_seasons_list(country):
    """

    :param country:
    :return:
    """
    conn = footy_connect()
    df = grab_data(conn, country)

    real_dates = []
    import re
    m = '\d+'
    for index, row in df.iterrows():
        x = re.findall(m, row['dates'])
        x = int(x[1])
        if x >= 8:
            year1 = int(row['dates'][-2:]) + 2000
            year2 = year1 + 1
            real_dates.append(str(year1) + "/" + str(year2))
        elif x <= 5:
            year1 = int(row['dates'][-2:]) + 2000
            year2 = year1 - 1
            real_dates.append(str(year2) + "/" + str(year1))
        else:
            real_dates.append(0)

    df['dateYear'] = real_dates
    df = df[df['dateYear'] != 0]
    conn.close()

    return df

def table_per_season(country, division, year):
    """

    :param team_nam:
    :param years:
    :return:
    """

    df = create_seasons_list(country)
    df = df[df['dateYear'] == year]
    df = df[df['division'] == division]

    #creating empty dataframe
    final = pd.DataFrame()

    #matches played
    mp_home = df.groupby(['home_team'])['id'].count().reset_index()
    mp_away = df.groupby(['away_team'])['id'].count().reset_index()

    #resutls
    w_home = df.groupby(['home_team'])['full_time_results'].apply(lambda x: x[x.str.contains('H')].count()).reset_index()
    w_away = df.groupby(['away_team'])['full_time_results'].apply(lambda x: x[x.str.contains('A')].count()).reset_index()

    l_home = df.groupby(['home_team'])['full_time_results'].apply(lambda x: x[x.str.contains('A')].count()).reset_index()
    l_away = df.groupby(['away_team'])['full_time_results'].apply(lambda x: x[x.str.contains('H')].count()).reset_index()

    d_home = df.groupby(['home_team'])['full_time_results'].apply(lambda x: x[x.str.contains('D')].count()).reset_index()
    d_away = df.groupby(['away_team'])['full_time_results'].apply(lambda x: x[x.str.contains('D')].count()).reset_index()

    #gf/ga
    gf_home = df.groupby(['home_team'])['home_team_goals'].sum().reset_index()
    gf_away = df.groupby(['away_team'])['away_team_goals'].sum().reset_index()

    gfh = df.groupby(['home_team'])['away_team_goals'].sum().reset_index()
    gfa = df.groupby(['away_team'])['home_team_goals'].sum().reset_index()

    #calcs
    final['Team'] = mp_home['home_team']
    final['MP'] = mp_home['id'] + mp_away['id']
    final['W'] = w_home['full_time_results'] + w_away['full_time_results']
    final['D'] = d_home['full_time_results'] + d_away['full_time_results']
    final["L"] = l_home['full_time_results'] + l_away['full_time_results']
    final['GF'] = gf_home['home_team_goals'] + gf_away['away_team_goals']
    final['GA'] = gfa['home_team_goals'] + gfh['away_team_goals']
    final['+/-'] = final['GF'] - final['GA']
    final['PTS'] = (final['W'] * 3) + (final['D'] * 1)
    final = final.sort_values(by='PTS', ascending=False)

    return final