# pages/page1.py
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from app import app

# Load data
df = pd.read_csv('data/results_transformed.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Layout with filters
layout = html.Div([
    html.H1('Soccer Tournament History'),
    
    # Filters
    html.Div([
        dcc.DatePickerRange(
            id='date-picker',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD',
            style={'padding': '10px'}
        ),
        dcc.Dropdown(
            id='team-dropdown',
            placeholder='Select Team',
            multi=True,
            style={'padding': '10px', 'width': '200px'}
        ),
        dcc.Dropdown(
            id='opponent-dropdown',
            placeholder='Select Opponent',
            multi=True,
            style={'padding': '10px', 'width': '200px'}
        ),
        dcc.Dropdown(
            id='tournament-dropdown',
            placeholder='Select Tournament',
            multi=True,
            style={'padding': '10px', 'width': '200px'}
        ),
        dcc.Dropdown(
            id='city-dropdown',
            placeholder='Select City',
            multi=True,
            style={'padding': '10px', 'width': '200px'}
        ),
        dcc.Dropdown(
            id='country-dropdown',
            placeholder='Select Country',
            multi=True,
            style={'padding': '10px', 'width': '200px'}
        ),
        dcc.Checklist(
            id='neutral-checkbox',
            options=[{'label': 'Neutral Venue', 'value': True}],
            style={'padding': '10px'}
        )
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-around'}),
    
    dcc.Graph(id='avg-scores-bar'),
    dcc.Graph(id='tournament-pie'),
    dcc.Graph(id='match-scores-scatter'),
    html.H2('Recent Matches'),
    html.Div(id='table-container'),
    dcc.Graph(id='scores-over-time-line')
])

# Callback to update filter options dynamically
@app.callback(
    [Output('team-dropdown', 'options'),
     Output('opponent-dropdown', 'options'),
     Output('tournament-dropdown', 'options'),
     Output('city-dropdown', 'options'),
     Output('country-dropdown', 'options')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('team-dropdown', 'value'),
     Input('opponent-dropdown', 'value'),
     Input('tournament-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('neutral-checkbox', 'value')]
)
def update_filter_options(start_date, end_date, teams, opponents, tournaments, cities, countries, neutral):
    # Filter data based on inputs
    filtered_df = df[
        (df['date'] >= start_date) & 
        (df['date'] <= end_date)
    ]
    if teams:
        filtered_df = filtered_df[filtered_df['team'].isin(teams)]
    if opponents:
        filtered_df = filtered_df[filtered_df['opposing_team'].isin(opponents)]
    if tournaments:
        filtered_df = filtered_df[filtered_df['tournament'].isin(tournaments)]
    if cities:
        filtered_df = filtered_df[filtered_df['city'].isin(cities)]
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    if neutral:
        filtered_df = filtered_df[filtered_df['neutral'] == True]

    # Generate options for each filter based on filtered data
    team_options = [{'label': team, 'value': team} for team in sorted(filtered_df['team'].dropna().unique())]
    opponent_options = [{'label': opposing_team, 'value': opposing_team} for opposing_team in sorted(filtered_df['opposing_team'].dropna().unique())]
    tournament_options = [{'label': tourney, 'value': tourney} for tourney in sorted(filtered_df['tournament'].dropna().unique())]
    city_options = [{'label': city, 'value': city} for city in sorted(filtered_df['city'].dropna().unique())]
    country_options = [{'label': country, 'value': country} for country in sorted(filtered_df['country'].dropna().unique())]

    return team_options, opponent_options, tournament_options, city_options, country_options

# Callback to update graphs and table based on filters
@app.callback(
    [Output('avg-scores-bar', 'figure'),
     Output('tournament-pie', 'figure'),
     Output('match-scores-scatter', 'figure'),
     Output('table-container', 'children'),
     Output('scores-over-time-line', 'figure')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('team-dropdown', 'value'),
     Input('opponent-dropdown', 'value'),
     Input('tournament-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('neutral-checkbox', 'value')]
)
def update_visualizations(start_date, end_date, teams, opponents, tournaments, cities, countries, neutral):
    # Filter data based on inputs
    filtered_df = df[
        (df['date'] >= start_date) & 
        (df['date'] <= end_date)
    ]
    if teams:
        filtered_df = filtered_df[filtered_df['team'].isin(teams)]
    if opponents:
        filtered_df = filtered_df[filtered_df['opposing_team'].isin(opponents)]
    if tournaments:
        filtered_df = filtered_df[filtered_df['tournament'].isin(tournaments)]
    if cities:
        filtered_df = filtered_df[filtered_df['city'].isin(cities)]
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    if neutral:
        filtered_df = filtered_df[filtered_df['neutral'] == True]

    # Create updated figures
    avg_scores = filtered_df.groupby('team').agg({'score': 'mean', 'opponent_score': 'mean'}).reset_index()
    fig_bar = px.bar(avg_scores, x='team', y=['score', 'opponent_score'], barmode='group', title="Average Scores")

    top_n = 5
    tournament_counts = filtered_df['tournament'].value_counts().reset_index()
    tournament_counts.columns = ['tournament', 'count']

    # Split into top N and 'Other'
    top_tournaments = tournament_counts.head(top_n)
    other_tournaments = pd.DataFrame({
        'tournament': ['Other'],
        'count': [tournament_counts['count'][top_n:].sum()]
    })

    # Combine top N and 'Other'
    final_counts = pd.concat([top_tournaments, other_tournaments], ignore_index=True)

    # Plot
    fig_pie = px.pie(final_counts, values='count', names='tournament', title="Tournament Distribution")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    fig_scatter = px.scatter(filtered_df, x='score', y='opponent_score', color='team', title="Match Scores", labels={'score': 'Score', 'opponent_score': 'Opponent Score'})

    recent_matches = filtered_df.sort_values(by='date', ascending=False).head(10)
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in recent_matches.columns],
        data=recent_matches.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        page_size=10
    )

    scores_over_time = filtered_df.groupby('date').agg({'score': 'mean', 'opponent_score': 'mean'}).reset_index()
    fig_line = px.line(scores_over_time, x='date', y=['score', 'opponent_score'], title="Scores Over Time")
    
    return fig_bar, fig_pie, fig_scatter, table, fig_line
