from flask import Flask
import dash

app = dash.Dash(__name__)
server = app.server