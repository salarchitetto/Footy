from .server import app
import os
import pandas as pd
import numpy as np
import json
from dash.dependencies import Input, Output, State
from scrape_data.queries import *
from tools.stats_tools import *
import plotly.graph_objs as go
from tools.footy_tools import *
import dash_html_components as html
import dash_table


try:
    import MySQLdb
except:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb

plotConfig = {'showLink': False,
              'modeBarButtonsToRemove': ['sendDataToCloud'],
              'displaylogo': False}
legendConfig = dict(orientation='h', x=0, y=1.1)

@app.callback(
    Output('indi-teams','options'),
    [Input('divisions', 'value')],
    [State('countries', 'value')]
)
def populate_teams(country, division):
    """

    :param country:
    :param division:
    :return:
    """
    if country is None: return []

    team_names = choose_team(country, division)

    teams = []

    print(teams)
    for x in range(0, len(team_names)): teams.append(
        dict(label=team_names['home_team'][x], value=team_names['home_team'][x].lower()
    ))

    return teams

@app.callback(
    Output('pct_store','data'),
    [Input('win_pct_button','n_clicks')],
    [State('indi-teams','value'),
     State('countries','value')]
)
def store_pct_data(n_clicks, team_name,country):
    """

    :param n_clicks:
    :param team_name:
    :param country:
    :return:
    """
    if n_clicks == 0:
        return []

    df = run_win_pct(team_name, country)

    return df.to_json()

@app.callback(
    Output('win_pct_graph','figure'),
    [Input('pct_store','data')],
    [State('indi-teams','value'),
     State('win_pct_button','n_clicks')]
)
def win_pct_graph(data, team_name, n_clicks):
    """

    :param df:
    :param n_clicks:
    :param team_name:
    :return:
    """
    if n_clicks == 0:
        return {'display':'none'}

    df = pd.read_json(data)
    df = df.sort_values(by='dateYear', ascending=True)
    # df = df.iloc[1:]

    traces = [go.Scatter(x=df['dateYear'], y=df['Win PCT'], name='Win %',
                         line=dict(color=footy_colors('MAASTRICHT BLUE'))),
              go.Scatter(x=df['dateYear'], y=df['Loss PCT'], name='Loss %',
                         line=dict(color=footy_colors('MIDNIGHT GREEN'))),
              go.Scatter(x=df['dateYear'], y=df['Draw PCT'], name='Draw %',
                         line=dict(color=footy_colors('ILLUMINATING EMERALD')))]

    layout = dict(title=team_name.title() + ' (Win-Tie-Loss) %.',
                  showlegend = True,
                  xaxis=dict(tickvals=df.dateYear, ticktext=df.dateYear),
                  paper_bgcolor='#EEEEEE',
                  plot_bgcolor='#EEEEEE'
                  )

    return (dict(data=traces, layout = layout))

@app.callback(
    Output('home_win_pct_graph', 'figure'),
    [Input('pct_store','data')],
    [State('indi-teams', 'value'),
     State('win_pct_button','n_clicks')]
)
def win_home_loss_pct(data, team_name, n_clicks):
    """

    :param n_clicks:
    :param team_name:
    :return:
    """
    if n_clicks == 0:
        return []

    df = pd.read_json(data)
    df = df.sort_values(by='dateYear', ascending=True)
    # df = df.iloc[1:]

    traces = [go.Scatter(x=df['dateYear'], y=df['Home Win PCT'], name='Home Win %',
                        line=(dict(color=footy_colors('ILLUMINATING EMERALD')))),
              go.Scatter(x=df['dateYear'], y=df['Away Win PCT'], name='Away Win %',
                         line=dict(color=footy_colors('YANKEES BLUE')))]
    layout = dict(title=team_name.title() + ' Home-Away Win %.',
                  showlegend=True,
                    paper_bgcolor = '#EEEEEE',
                    plot_bgcolor = '#EEEEEE'
    )

    return (dict(data=traces, layout=layout))


@app.callback(
    Output('loss_win_pct_graph', 'figure'),
    [Input('pct_store','data')],
    [State('indi-teams', 'value'),
     State('win_pct_button','n_clicks')]
)
def loss_home_pct(data, team_name, n_clicks):
    """

    :param n_clicks:
    :param team_name:
    :return:
    """
    if n_clicks == 0:
        return []

    df = pd.read_json(data)
    df = df.sort_values(by='dateYear', ascending=True)
    # df = df.iloc[1:]

    traces = [go.Scatter(x=df['dateYear'], y=df['Home Loss PCT'], name='Home Loss %'),
              go.Scatter(x=df['dateYear'], y=df['Away Loss PCT'], name='Away Loss %')]
    layout = dict(title=team_name.title() + ' Home-Away Loss %',
                  showlegend=True,
                  paper_bgcolor='#EEEEEE',
                  plot_bgcolor='#EEEEEE'
                  )

    return (dict(data=traces, layout=layout))

@app.callback(
    Output('seasonlist','options'),
    [Input('countries','value')]
)
def season_list(country):
    """

    :param n_clicks:
    :param country:
    :return:
    """
    if country is None: return []

    df = create_seasons_list(country)
    season = list(df['dateYear'].unique())
    season.sort()

    seasons = []

    for x in range(0, len(season)): seasons.append(
        dict(label=season[x], value=season[x]
    ))

    return seasons

@app.callback(
    Output('divisions', 'options'),
    [Input('countries', 'value')]
)

def division_list(country):
    """

    :param country:
    :return:
    """
    if country is None: return []

    conn = footy_connect()
    divisions = grab_divisions(conn, country)

    divs = []

    for x in range(0, len(divisions)): divs.append(
        dict(label=divisions['division'][x], value=divisions['division'][x]
    ))

    return divs

@app.callback(
    Output('table-name','children'),
    [Input('seasonlist', 'value')],
    [State('divisions', 'value')]
)
def table_name(season, division):
    """

    :param n_clicks:
    :param division:
    :param season:
    :return:
    """

    if season is None:
        return str('Please enter a League and Table Year!')
    else:
        return str(division) + " Table for the Season of " + str(season)

    # return str(table)

@app.callback(
    Output('perseason','data'),
    [Input('table-button','n_clicks')],
    [State('countries','value'),
     State('divisions', 'value'),
     State('seasonlist', 'value')]
)
def show_league_tables(n_clicks, country, division, season):
    """

    :param n_clicks:
    :param country:
    :param division:
    :param season:
    :return:
    """
    if n_clicks == 0:
        return [{}]

    df = table_per_season(country, division, season)

    return df.to_dict(orient='records')
