# pages/page2.py
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Country": ["USA", "Canada", "France", "Germany", "UK"],
    "Value": [10, 12, 9, 14, 8]
})

# Create Plotly figure
fig = px.pie(df, values='Value', names='Country')

layout = html.Div([
    html.H1('Page 2 - Pie Chart'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
