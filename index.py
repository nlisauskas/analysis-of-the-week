# index.py
from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
import pages.world_cup
import pages.page2
import pages.page3

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        dcc.Link('World Cup', href='/world_cup'),
        dcc.Link('Page 2', href='/page2'),
        dcc.Link('Page 3', href='/page3'),
    ]),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/world_cup':
        return pages.world_cup.layout
    elif pathname == '/page2':
        return pages.page2.layout
    elif pathname == '/page3':
        return pages.page3.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
