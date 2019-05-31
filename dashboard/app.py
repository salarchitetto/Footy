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
from dash.dependencies import Input, Output, State
import dash_table
import json
import sqlite3
from flask import Flask
from scrape_data.queries import *

app.config['suppress_callback_exceptions'] = True
from . import stats_callbacks

# HTML layout for the app.
plotConfig = {'showLink': False,
              'modeBarButtonsToRemove': ['sendDataToCloud'],
              'displaylogo': False}

countryDropdown = [{'label': 'England', 'value': 'england'},
                   {'label': 'France', 'value': 'france'},
                   {'label': 'Germany', 'value': 'germany'},
                   {'label': 'Italy', 'value': 'italy'},
                   {'label': 'Spain', 'value': 'spain'}]

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #D2D2D2',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#D2D2D2'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'black',
    'color': 'white',
    'padding': '6px'
}

colors = {
    'background': 'black'
}

# Configure navbar menu
nav_menu = html.Div([
    html.Ul([
        html.Li([
            dcc.Link('Home', href='/')
        ]),
        html.Li([
            dcc.Link('Statistics & Analysis', href='/stats')
        ]),
        html.Li([
            dcc.Link('Player Analysis', href='/players')
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
        # HTML code for the homepage
        html.Div([
            html.Img(src=app.get_asset_url('juve.jpg'), className='stadium'),
            html.H1(children='Footy Dash.', id='h1home'),
            html.Blockquote(children='''
            Welcome to Footy Dash, a football data visualization website.
            The data displayed has been curated from various parts of the web,
            in order to provide readers accurate and concise Football information.

            *Under Construction*
            '''),
            html.Footer(children='Created by Salvatore Architetto: https://github.com/salarchitetto', id='home-footer')],
            id='home'),
        html.Div([
            html.Div([
                html.Div([
                    html.P(children='Choose Criteria Here', id='h4stats'),
                    html.Button(id='win_pct_button', n_clicks=0, children='Show win-tie-loss % for your team.',
                                className='btn btn-primary'),
                    dcc.Dropdown(id='countries', options=countryDropdown, placeholder='Please select a country.'),
                    dcc.Dropdown(id='divisions', placeholder='Choose a division', options =[]),
                    dcc.Dropdown(id='indi-teams', placeholder='choose a team', options=[]),
                    html.Br(),
                    html.Button(id='table-button', n_clicks=0, children='Display table for specific year.',
                                className='btn btn-primary'),
                    dcc.Dropdown(id='seasonlist', placeholder='choose a season', options=[])
                ], className='col-md-2 offset-md-9', id='test'),
                html.Br(),
                dcc.Tabs(id='tabs', children=[
                    dcc.Tab(label='Scores', id='live_score', style=tab_style,selected_style=tab_selected_style, children=[
                        html.Div([

                        ], className='col-xs-1 right-panel'),
                        html.Div([
                            dcc.Tabs(id='score-tabs', children=[
                                dcc.Tab(label='Today', id='score-today', style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=[
                                            html.H1(children='Todays Scores for the Day'),
                                            html.Div(
                                                dash_table.DataTable(id='today', columns=[
                                                    {'name': 'Game Start', 'id': 'Game Start'},
                                                    {'name': 'Country', 'id': 'Country'},
                                                    {'name': 'Home Team', 'id': 'Home Team'},
                                                    {'name': 'Score', 'id': 'Score'},
                                                    {'name': 'Away Team', 'id': 'Away Team'},
                                            ], data=[],
                                             style_as_list_view=True,
                                             style_cell={'backgroundColor': 'rgb(30, 30, 30)',
                                                         'padding': '5px',
                                                         'color': 'white',
                                                         'whiteSpace': 'no-wrap',
                                                         'maxWidth': 0, },
                                             ), className='col-xs-offset-1 col-xs-9')
                                        ]),
                                dcc.Tab(label='Live Scores', id='score-live', style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=[
                                            html.H1(children='Current Live Games'),
                                            html.Div(
                                                dash_table.DataTable(id='live', columns=[
                                                    {'name': 'Game Start', 'id': 'Game Start'},
                                                    {'name': 'Country / Live Time', 'id': 'Country / Live Time'},
                                                    {'name': 'Home Team', 'id': 'Home Team'},
                                                    {'name': 'Score', 'id': 'Score'},
                                                    {'name': 'Away Team', 'id': 'Away Team'},
                                                ], data=[],
                                                 style_as_list_view=True,
                                                 style_cell={'backgroundColor': 'rgb(30, 30, 30)',
                                                             'padding': '5px',
                                                             'color': 'white',
                                                             'whiteSpace': 'no-wrap',
                                                             'maxWidth': 0, },
                                                 ), className='col-xs-offset-1 col-xs-9'),
                                            dcc.Interval(
                                                id='interval',
                                                interval=5 * 1000,
                                                n_intervals=0
                                            ),
                                        ]),
                                dcc.Tab(label='Yesterday', id='score-yesterday', style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=[
                                            html.H1(children='Yesterdays Games'),
                                            html.Div(
                                                dash_table.DataTable(id='yesterday', columns=[
                                                    {'name': 'Game Start', 'id': 'Game Start'},
                                                    {'name': 'Country', 'id': 'Country'},
                                                    {'name': 'Home Team', 'id': 'Home Team'},
                                                    {'name': 'Score', 'id': 'Score'},
                                                    {'name': 'Away Team', 'id': 'Away Team'},
                                                ], data=[],
                                                 style_as_list_view=True,
                                                 style_cell={'backgroundColor': 'rgb(30, 30, 30)',
                                                             'padding': '5px',
                                                             'color': 'white',
                                                             'whiteSpace': 'no-wrap',
                                                             'maxWidth': 0, },
                                                 ), className='col-xs-offset-1 col-xs-9')
                                        ]),
                                dcc.Tab(label='Tomorrow', id='score-tomorrow', style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=[
                                            html.H1(children='Tomorrows Games'),
                                            html.Div(
                                                dash_table.DataTable(id='tomorrow', columns=[
                                                    {'name': 'Game Start', 'id': 'Game Start'},
                                                    {'name': 'Country', 'id': 'Country'},
                                                    {'name': 'Home Team', 'id': 'Home Team'},
                                                    {'name': 'Score', 'id': 'Score'},
                                                    {'name': 'Away Team', 'id': 'Away Team'},
                                                ], data=[],
                                                     style_as_list_view=True,
                                                     style_cell={'backgroundColor': 'rgb(30, 30, 30)',
                                                                 'padding': '5px',
                                                                 'color': 'white',
                                                                 'whiteSpace': 'no-wrap',
                                                                 'maxWidth': 0, },
                                                     ), className='col-xs-offset-1 col-xs-9')
                                        ])
                            ], className="col-xs-9 right-panel", style=tabs_styles),
                        ], className='row')
                    ]),
                    dcc.Tab(label='Win/Loss PCT', style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            dcc.Graph(id='win_pct_graph', config=plotConfig, style={'height': '50vh'}),
                            dcc.Graph(id='home_win_pct_graph', config=plotConfig, style={'height': '40vh'}),
                            dcc.Graph(id='loss_win_pct_graph', config=plotConfig, style={'height': '40vh'})
                        ])]),
                    dcc.Tab(label='League Table', style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            html.Br(),
                            html.H2(id='table-name', children=[],),
                            html.Div(
                                dash_table.DataTable(id='perseason',columns=[
                                    {'name': 'Team', 'id':'Team'},
                                    {'name': 'MP', 'id':'MP'},
                                    {'name': 'W', 'id':'W'},
                                    {'name': 'D', 'id': 'D'},
                                    {'name': 'L', 'id': 'L'},
                                    {'name': 'GF', 'id': 'GF'},
                                    {'name': 'GA', 'id': 'GA'},
                                    {'name': '+/-', 'id': '+/-'},
                                    {'name': 'PTS', 'id': 'PTS'}
                                    ], data=[],
                                style_as_list_view=True,
                                 style_cell={'backgroundColor': 'rgb(30, 30, 30)',
                                         'padding': '5px',
                                         'color': 'white',
                                         'whiteSpace':'no-wrap',
                                         'maxWidth':0,},
                                 style_cell_conditional=[
                                     {'if': {'column_id': 'Team'},
                                      'width': '10%'},
                                     {'if': {'column_id': 'PTS'},
                                      'width': '5%'},
                                     {'if': {'column_id': 'MP'},
                                      'width': '5%'},
                                     {'if': {'column_id': 'W'},
                                      'width': '5%'},
                                     {'if': {'column_id': 'D'},
                                      'width': '5%'},
                                     {'if': {'column_id': 'L'},
                                      'width': '5%'},
                                     {'if': {'column_id': 'GF'},
                                      'width': '5%'},
                                     {'if': {'column_id': 'GA'},
                                      'width': '5%'},
                                     {'if': {'column_id': '+/-'},
                                      'width': '5%'},
                                 ],
                                 sorting=True,
                                 sorting_type="multi",
                                 ),  className='col-xs-offset-1 col-xs-9')
                        ])
                    ]),
                    dcc.Tab(label='Stats Table', style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            html.H1(children='Team Statistics'),
                            html.Div([
                                dcc.Graph(id='goals-scored', config=plotConfig),
                                dcc.Graph(id='shot-stats', config=plotConfig),
                                dcc.Graph(id='foul-stats', config=plotConfig)
                            ])
                        ]),
                    ]),
                    dcc.Tab(label='League Stats', id='league-tab',style=tab_style, selected_style=tab_selected_style, children=[
                        # html.H1(children='Overall league statistics'),
                        html.H2(id='tab-update', children=[],),
                        dcc.Graph(id='per_league_wins'),
                        dcc.Graph(id='per_league_goals'),
                        dcc.Graph(id='avgGoals_perSeason'),
                        dcc.Graph(id='top_team_goals')
                    ])
                ], className="col-xs-9 right-panel", style=tabs_styles)
            ], className='row', id='test2'),

        ], id='stats'),

        # HTML code for players
        html.Div([
            html.H1(children='Player Information')
        ], id='players'),

        # HTML for general news info
        html.Div([
            html.H1(children='General News')
        ], id='news'),
    ], style={'display': 'block'}),

    dcc.Store(id='pct_store'),
    dcc.Store(id='team_stats'),
    dcc.Store(id='overall_download'),
    # Add bootstrap css
    app.css.append_css({"external_url": [
        "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    ]})
])


# Adding callbacks for the various links
@app.callback(
    Output(component_id='home', component_property='style'),
    [Input('url', 'pathname')]
)
def display_home(pathname):
    if pathname == '/':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='stats', component_property='style'),
    [Input('url', 'pathname')]
)
def display_stats(pathname):
    if pathname == '/stats':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='players', component_property='style'),
    [Input('url', 'pathname')]
)
def display_players(pathname):
    if pathname == '/players':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='news', component_property='style'),
    [Input('url', 'pathname')]
)
def display_players(pathname):
    if pathname == '/news':
        return {'display': 'block'}
    else:
        return {'display': 'none'}