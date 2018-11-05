import datetime
from datetime import datetime
from datetime import timedelta
from dash import Dash
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input,Output,State
import json
import sqlite3
from flask import Flask

from scrape_data.matches import *
from scrape_data.leagues import *
from scrape_data.news import *
from scrape_data.players import *
from scrape_data.mysql_connect import *


app = dash.Dash(__name__)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([
    html.Link(href= 'style/style.css', rel='stylesheet'),
    html.Div([
        html.H1(children='The Footy Dashboard.'),
        html.Div(children='''An Application to visualize Soccer Statistics''')
    ])
])
