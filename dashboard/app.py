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
plotConfig = {'showLink': False,
              'modeBarButtonsToRemove': ['sendDataToCloud'],
              'displaylogo': False}

countryDropdown = [{'label':'England','value':'england'},
                   {'label':'France','value':'france'},
                   {'label':'Germany','value':'germany'},
                   {'label':'Italy','value':'italy'},
                   {'label':'Portugal','value':'portugal'},
                   {'label':'Scotland','value':'scotland'},
                   {'label':'Spain','value':'spain'}]

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'black',
    'color': 'white',
    'padding': '6px'
}

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
            html.Img(src=app.get_asset_url('juve.jpg'),className='stadium'),
            html.H1(children='The Footy Dashboard.', id='h1home'),
            html.Blockquote(children='''
            Welcome to Footy Dash, a Football data visualization website.
            Data has been curated from all parts of the internet to provide 
            you with accurate and concise Football information. 
            ''')],
            id='home'),

        #HTML code for stats
        #add link menu to stats page(I.E = season table per year - shots/goals per year)
        #add twitter/instagram feed to stats page - columns 1/2
        html.Div([
            html.H2(children='Footy Stats', id='h1stats'),
            html.Div([
                html.Div([
                    html.Button(id='win_pct_button', n_clicks=0,children='Show Win PCT for your team.',className='btn btn-primary'),
                    dcc.Dropdown(id='countries', options=countryDropdown, placeholder='Please select a country.'),
                    dcc.Dropdown(id='indi-teams', placeholder='choose a team', options=[]),
                ], className='col-xs-2 left-panel'),
                html.Div([html.Div(className='verticalLine')], className='col-xs-1 left-panel'),
                dcc.Tabs(id='tabs', children=[
                    dcc.Tab(label='Win/Loss PCT', style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            dcc.Graph(id='win_pct_graph', config=plotConfig, style={'height': '50vh'}),
                            # html.Hr(),
                            dcc.Graph(id='home_win_pct_graph', config=plotConfig, style={'height': '40vh'}),
                            dcc.Graph(id='loss_win_pct_graph', config=plotConfig, style={'height': '40vh'})
                        ])]),
                    dcc.Tab(label='League Table', style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            html.H1(children='Test')
                        ])]),
                    dcc.Tab(label='Stats Table', style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            html.H1(children='Stat Creation')
                        ])
                    ]),
                ], className="col-xs-9 right-panel", style=tabs_styles)
            ], className='row'),

        ], id='stats'),

        #HTML code for players
        html.Div([
            html.H1(children='Player Information')
        ], id = 'players'),

        #HTML for general news info
        html.Div([
            html.H1(children='General News')
        ], id = 'news'),
    ], style={'display':'block'}),

    dcc.Store(id='win_pct_store'),
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