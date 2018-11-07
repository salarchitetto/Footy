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

#HTML layout for the app.


app = dash.Dash(__name__)
server = app.server

# Configure navbar menu
nav_menu = html.Div([
    html.Ul([
            html.Li([
                    dcc.Link('Home', href='/home')
                    ], className='active'),
            html.Li([
                    dcc.Link('Statistics & Analysis', href='stats')
                    ]),
            html.Li([
                    dcc.Link('Players', href='/players')
                    ]),
            html.Li([
            dcc.Link('News', href='/news')
                    ]),
            ], className='nav navbar-nav')
], className='navbar navbar-inverse navbar-static-top')

# Define layout
app.layout = html.Div([
    nav_menu,
    html.Div([
        html.H1(children='The Footy Dashboard.'),
        html.Div(children='''An Application to visualize Soccer Statistics'''),
]),

# Add bootstrap css
app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})])

