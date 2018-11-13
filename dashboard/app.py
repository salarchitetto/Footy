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
            html.Img(src=app.get_asset_url('footy_nav.png'), className='topright'),
            ], className='nav navbar-nav')
], className='navbar navbar-inverse navbar-static-top')

# Define layout
app.layout = html.Div([
    nav_menu,
    html.Div([
        html.Img(src=app.get_asset_url('football-stadium-wallpaper.jpg'),className='stadium'),
        html.H1(children='The Footy Dashboard.'),
        html.Blockquote(children='''An Application to visualize Soccer Statistics.
        This website was created using the Plotly Dash package. Feel free to check
        out all the analyses I've created. Special shoutout to FOTMOB and 
        Football-data UK for the data.'''),
        html.Footer(children='Created by Salvatore Architetto: https://github.com/salarchitetto')
    ]),
    # Add bootstrap css
    app.css.append_css({"external_url": [
        "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    ]})
])

