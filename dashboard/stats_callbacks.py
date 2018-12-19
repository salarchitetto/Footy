from .server import app
import os
import pandas as pd
import numpy as np
import json
from dash.dependencies import Input, Output, State
from scrape_data.queries import *
from tools.stats_tools import *

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


