# pages/page3.py
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    "Date": pd.date_range(start='1/1/2022', periods=50),
    "Value": np.random.randn(50).cumsum()
})

# Create Plotly figure
fig = px.line(df, x='Date', y='Value')

layout = html.Div([
    html.H1('Page 3 - Line Chart'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
