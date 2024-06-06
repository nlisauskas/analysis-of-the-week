import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for deploying with a platform like Heroku
app.title = "South Shore Analytics - Analysis of the Week"  # Set the title of the app

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
])

if __name__ == '__main__':
    app.run_server(debug=True)
