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
    [Input('countries', 'value')]
)
def populate_teams(country):
    """

    :param countries:
    :return:
    """
    if country is None: return []

    team_names = choose_team(country)

    teams = []

    for x in range(0, len(team_names)): teams.append(
        dict(label=team_names['home_team'][x], value=team_names['home_team'][x].lower()
    ))

    return teams

@app.callback(
    Output('win_pct_graph','figure'),
    [Input('win_pct_button','n_clicks')],
    [State('indi-teams','value')]
)
def win_pct_graph(n_clicks, team_name):
    """

    :param df:
    :param n_clicks:
    :param team_name:
    :return:
    """
    if n_clicks == 0:
        return []

    df = run_win_pct(team_name)

    traces = [go.Scatter(x=df['date'], y=df['Win PCT'], name='Win %',
                         line=dict(color=footy_colors('MAASTRICHT BLUE'))),
              go.Scatter(x=df['date'], y=df['Loss PCT'], name='Loss %',
                         line=dict(color=footy_colors('MIDNIGHT GREEN'))),
              go.Scatter(x=df['date'], y=df['Draw PCT'], name='Draw %',
                         line=dict(color=footy_colors('ILLUMINATING EMERALD')))]

    layout = dict(title=team_name.capitalize() + ' (Win-Tie-Loss) % Throughout the Years.',
                  showlegend = True)

    return (dict(data=traces, layout = layout))
