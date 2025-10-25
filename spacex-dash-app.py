

import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, Input, Output

# Load Data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

# Create the app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}
    ),

    # TASK 1: Launch site dropdown
    html.Div([
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': 'All Sites', 'value': 'ALL'}] +
                    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True,
            clearable=False
        )
    ]),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Payload slider
    html.P("Payload range (Kg):"),
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=min_payload,
            max=max_payload,
            step=1000,
            marks={i: f'{i}' for i in range(min_payload, max_payload + 1, 2000)},
            value=[min_payload, max_payload]
        )
    ]),
    html.Br(),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2 callback: Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(selected_site):
    if selected_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(df, values='class', names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(df, names='class',
                     title=f'Success vs Failure for site: {selected_site}')
    return fig

# TASK 4 callback: Scatter Chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site != 'ALL':
        filtered = filtered[filtered['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        size='Payload Mass (kg)',
        title=f'Payload vs Success for site: {selected_site}'
    )
    return fig

# Run the app
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8060))  # pick any >1024
    app.run(host='0.0.0.0', port=port, debug=True)



