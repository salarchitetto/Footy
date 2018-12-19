from .server import app

import datetime
from datetime import datetime
from datetime import timedelta
from dash import Dash
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_renderer
import dash_table_experiments as dt
from dash.dependencies import Input,Output,State
import json
import sqlite3
from flask import Flask
from scrape_data.queries import *
app.config['suppress_callback_exceptions']=True
from . import stats_callbacks

#HTML layout for the app.

countryDropdown = [{'label':'England','value':'england'},
                   {'label':'France','value':'france'},
                   {'label':'Germany','value':'germany'},
                   {'label':'Italy','value':'italy'},
                   {'label':'Portugal','value':'portugal'},
                   {'label':'Scotland','value':'scotland'},
                   {'label':'Spain','value':'spain'}]

# Configure navbar menu
nav_menu = html.Div([
    html.Ul([
            html.Li([
                    dcc.Link('Home', href='/')
                    ], className='active'),
            html.Li([
                    dcc.Link('Statistics & Analysis', href='/stats')
                    ]),
            html.Li([
                    dcc.Link('Players', href='/players')
                    ]),
            html.Li([
            dcc.Link('News', href='/news')
                    ]),
            html.Img(src=app.get_asset_url('footy_nav.png'), className='topright'),
            ], className='nav navbar-nav'),
    html.Div(id='page-content'),
], className='navbar navbar-inverse navbar-static-top')

# Define layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav_menu,
    html.Div([
        #HTML code for the homepage
        html.Div([
            html.Div(html.Img(src=app.get_asset_url('football-stadium-wallpaper.jpg'),className='stadium')),
            html.H1(children='The Footy Dashboard.', id='h1home'),
            html.Blockquote(children='''
            An Application to visualize Soccer Statistics.
            This website was created using the Plotly Dash package. Feel free to check
            out all the analyses I've created. Special shoutout to FOTMOB and 
            Football-data UK for the data.
            '''),
            html.Footer(children='Created by Salvatore Architetto: https://github.com/salarchitetto')],
            id = 'home'),

        ##HTML code for stats
        html.Div([
            html.H2(children='Footy Stats', id = 'h1stats'),
            html.Div([
                html.Div([
                    dcc.Dropdown(id='countries', options=countryDropdown, placeholder='Please select a country.'),
                    dcc.Dropdown(id='indi-teams', placeholder='choose a team', options=[])
                ], className='col-xs-2 left-panel'),
                html.Div([html.Div(className='verticalLine')], className='col-xs-2 left-panel')
            ], className='row'),
        ], id = 'stats'),

        #HTML code for players
        html.Div([
            html.H1(children='Player Information')
        ], id = 'players'),

        #HTML for general news info
        html.Div([
            html.H1(children='General News')
        ], id = 'news'),
    ], style={'display':'block'}),
    # Add bootstrap css
    app.css.append_css({"external_url": [
        "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    ]})
])

#Adding callbacks for the various links
@app.callback(
    Output(component_id= 'home', component_property='style'),
    [Input('url', 'pathname')]
)
def display_home(pathname):
    if pathname == '/':
        return {'display':'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id= 'stats', component_property='style'),
    [Input('url', 'pathname')]
)
def display_stats(pathname):
    if pathname == '/stats':
        return {'display':'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id= 'players', component_property='style'),
    [Input('url', 'pathname')]
)
def display_players(pathname):
    if pathname == '/players':
        return {'display':'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id= 'news', component_property='style'),
    [Input('url', 'pathname')]
)
def display_players(pathname):
    if pathname == '/news':
        return {'display':'block'}
    else:
        return {'display': 'none'}
