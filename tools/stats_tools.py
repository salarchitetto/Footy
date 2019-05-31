import os
import pandas as pd
import datetime
from scrape_data.queries import *
from scrape_data.mysql_connect import *

def choose_team(country_name, division):
    """
    This function returns a list of the teams per country and will
    populate a drop down in the callbacks
    :param country_name:
    :return: list of team names per country
    """

    from datetime import datetime
    #connecting to DB
    conn = footy_connect()

    #grabbing dataframe
    df = grab_team_names(conn, division, country_name)

    df = create_seasons_list(df)

    today_year = datetime.now().year
    full = str(today_year-1) + '/' + str(today_year)

    df = df.loc[df['dateYear'] == full]
    df = df.drop_duplicates(subset='home_team')

    conn.close()

    return df

def home_vs_away(df, team_name):
    """
    Helper function to check out wins loses and draws for a given team.

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

def run_win_pct(team_name, df):
    """
    Function that calculates a teams winning percentage Year over Year (YoY)
    Calculation:
        Number of wins by the total number of competitions.
        Then multiply by 100 = win percentage.
        Number of loses by the total number of competitions.
        Then multiply by 100 = loss percentage

        this function also takes into account the home and away win/loss
        percentages.

    :param team_name: Takes in the state of the team_names dropdown
    :return:a dataframe That returns percentages for specific teams
    """

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

def create_seasons_list(df=None, country = None):
    """
    This function pretty much breaks down the date of a given match
    then buckets that information to a particular season. I.E: a match played
    on 02/07/2018 would be bucketed in the 2017/2018 season.

    :param df: takes in a dataframe
    :return: a dataframe
    """

    if country is not None:

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

    else:
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

    return df

def table_per_season(df, division, year):
    """
    Function that returns a complete dataframe with what you would normally
    see as a soccer league table. It contains the matches played, wins, draws,
    loses, goals for/against,  the difference, and the overall points a team
    earned throughout the season.

    :param country: an option from the countries dropdown
    :param division: an option from the divsions dropdown
    :param year: an option from the seasons dropdown
    :return: a dataframe with the information for a specific season
    """

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

def goal_stats(df, team):
    """
    This function looks at the % of goals scored home and away
    relative to the shots taken in each game by season.
    """

    df_fin = pd.DataFrame()

    df['home_team'] = df['home_team'].str.lower()
    df['away_team'] = df['away_team'].str.lower()

    # df = df[df['division'] == division]

    df_home = df[df['home_team'] == team]
    df_away = df[df['away_team'] == team]

    home_goals = df_home.groupby(['home_team', 'dateYear'])['home_team_goals', 'home_team_shots'].sum().reset_index()
    home_goals['pct_per_season'] = (home_goals['home_team_goals'] / home_goals['home_team_shots']) * 100
    away_goals = df_away.groupby(['away_team', 'dateYear'])['away_team_goals', 'away_team_shots'].sum().reset_index()
    away_goals['pct_per_season'] = (away_goals['away_team_goals'] / away_goals['away_team_shots']) * 100

    df_fin['season'] = home_goals['dateYear']
    df_fin['overall_pct'] = (home_goals['pct_per_season'] + away_goals['pct_per_season']).round(2)
    df_fin['home_pct'] = home_goals['pct_per_season'].round(2)
    df_fin['away_pct'] = away_goals['pct_per_season'].round(2)

    return df_fin

def shot_stats(df, team):

    df_fin = pd.DataFrame()

    df['home_team'] = df['home_team'].str.lower()
    df['away_team'] = df['away_team'].str.lower()

    df_home = df[df['home_team'] == team]
    df_away = df[df['away_team'] == team]

    home_shots = df_home.groupby(['home_team', 'dateYear'])['home_team_shot_tar', 'home_team_shots'].sum().reset_index()
    home_shots['pct_per_season'] = (home_shots['home_team_shot_tar'] / home_shots['home_team_shots']) * 100
    away_shots = df_away.groupby(['away_team', 'dateYear'])['away_team_shot_tar', 'away_team_shots'].sum().reset_index()
    away_shots['pct_per_season'] = (away_shots['away_team_shot_tar'] / away_shots['away_team_shots']) * 100

    df_fin['season'] = home_shots['dateYear']
    df_fin['overall_pct'] = (home_shots['pct_per_season'] + away_shots['pct_per_season'])
    df_fin['total_shots'] = (home_shots['home_team_shots'] + away_shots['away_team_shots'])
    df_fin['home_pct'] = (home_shots['home_team_shot_tar'] / df_fin['total_shots'] * 100).round(2)
    df_fin['away_pct'] =(away_shots['away_team_shot_tar'] / df_fin['total_shots'] * 100).round(2)

    return df_fin

def foul_stats(df, team):

    df_fin = pd.DataFrame()

    df['home_team'] = df['home_team'].str.lower()
    df['away_team'] = df['away_team'].str.lower()

    df_home = df[df['home_team'] == team]
    df_away = df[df['away_team'] == team]

    home_foul = df_home.groupby(['home_team', 'dateYear'])['home_foul','home_yellow','home_red'].sum().reset_index()
    home_foul['yellow_pct'] = (home_foul['home_yellow'] / home_foul['home_foul'] * 100).round(2)
    home_foul['red_pct'] = (home_foul['home_red'] / home_foul['home_foul'] * 100).round(2)
    away_foul = df_away.groupby(['away_team', 'dateYear'])['away_foul', 'away_yellow', 'away_red'].sum().reset_index()
    away_foul['yellow_pct'] = (away_foul['away_yellow'] / away_foul['away_foul'] * 100).round(2)
    away_foul['red_pct'] = (away_foul['away_red'] / away_foul['away_foul'] * 100).round(2)

    df_fin['season'] = home_foul['dateYear']
    df_fin['home_yellow_pct'] = home_foul['yellow_pct']
    df_fin['home_red_pct'] = home_foul['red_pct']
    df_fin['away_yellow_pct'] = away_foul['yellow_pct']
    df_fin['away_red_pct'] = away_foul['red_pct']

    return df_fin

#start of league stats

def past_five_years():

    year = datetime.datetime.today().year
    ranges = list(range(year, year - 6, -1))
    ranges = ' '.join(str(x) for x in ranges).split()

    return ranges

def top_leagues():
    return ['Bundesliga', 'La Liga', 'Ligue 1', 'Premier League', 'Serie A']

def home_win_per_league(df):

    h_win = df.groupby(['division', 'dateYear',])['full_time_results'].apply(
        lambda x: x[x.str.contains('H')].count()).reset_index()

    h_win = h_win[h_win['division'].str.contains('|'.join(top_leagues()))]
    h_win = h_win[h_win['division'] != 'Bundesliga Two']

    return h_win

def total_goals_per_season(df):

    goals = df.groupby(['division', 'dateYear'])['home_team_goals', 'away_team_goals'].sum().reset_index()
    goals = goals[goals['division'].str.contains('|'.join(top_leagues()))]
    goals = goals[goals['division'] != 'Bundesliga Two']

    goals['all_goals'] = goals['home_team_goals'] + goals['away_team_goals']

    return goals

def  full_league_conversion(df):

    bundes = df[df['division'] == 'Bundesliga']
    bundes = bundes[2:]
    liga = df[df['division'] == 'La Liga']
    liga = liga[1:]
    ligue = df[df['division'] == 'Ligue 1']
    prem = df[df['division'] == 'Premier League']
    prem = prem[6:]
    serie = df[df['division'] == 'Serie A']
    serie = serie[1:]

    return bundes, liga, ligue, prem, serie

def average_goals_per_season(df):

    avg_goals = df.groupby(['division', 'dateYear'])['home_team_goals', 'away_team_goals'].mean().reset_index()
    avg_goals = avg_goals[avg_goals['division'].str.contains('|'.join(top_leagues()))]
    avg_goals = avg_goals[avg_goals['division'] != 'Bundesliga Two']

    avg_goals['all_goals'] = avg_goals['home_team_goals'] + avg_goals['away_team_goals']

    return avg_goals

def top_team_goals(df):

    topTeamsHome = df.groupby(['home_team', 'dateYear'])['home_team_goals'].sum().reset_index()
    topTeamsAway = df.groupby(['away_team', 'dateYear'])['away_team_goals'].sum().reset_index()

    topTeam = topTeamsHome.merge(topTeamsAway, how='left', left_on= ['home_team', 'dateYear'], right_on= ['away_team', 'dateYear'])
    topTeam = topTeam.groupby(['home_team', 'dateYear'])['home_team_goals', 'away_team_goals'].sum().reset_index()

    home_team = []
    overall = []
    dateYear = []

    dates = ['2000/2001', '2001/2002', '2002/2003', '2003/2004', '2004/2005', '2005/2006']
    for index, row in topTeam.iterrows():
        if row['dateYear'] in dates:
            pass
        else:
            home_team.append(row['home_team'])
            overall.append(row['home_team_goals'] + row['away_team_goals'])
            dateYear.append(row['dateYear'])

    tt = pd.DataFrame()
    tt['home_team'] = home_team
    tt['overall'] = overall
    tt['dateYear'] = dateYear

    ntt = tt.groupby(['home_team'])['overall'].sum().reset_index()
    ntt = ntt.sort_values(by='overall', ascending=False).head(10)

    return ntt
