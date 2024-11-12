import pandas as pd
import plotly.express as px
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Creating options for Dropdown
sites = spacex_df['Launch Site'].unique()
options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in sites:
    options.append({'label': site, 'value': site})

app = dash.Dash(__name__)

app.layout = html.Div(children = [
    html.H1('SpaceX Launch Records Dashboard',
            style = {'textAlign': 'center',
                     'color': '#503D36',
                     'font-size': 40}),
    
    # TASK 1
    
    dcc.Dropdown(
        id = 'site-dropdown',
        options = options,
        value = 'ALL',
        placeholder = 'Select Launch Site',
        searchable = True,
    ),
    
    html.Br(),

    
    # TASK 2
    
    html.Div(dcc.Graph(id = 'success-pie-chart')),
    html.Br(),   
    
    # TASK 3
    
    html.P('Payload Range (kg):'),
    dcc.RangeSlider(
        id = 'payload-slider',
        min = 0, max = 10000, step = 1000,
        value = [min_payload, max_payload]
    ),
    
    # TASK 4
    
    html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
])

# Task 2 Callback Function

@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        fig = px.pie(data_frame = spacex_df, values = 'class',
                     names = 'Launch Site', title = 'Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site][['class']]
        fig = px.pie(data_frame = filtered_df, names = 'class',
                     title = "Total Success Launches for Site {site}".format(site = entered_site))
    
    return fig


# Task 4 Callback Function

@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'), 
    [
        Input(component_id = 'site-dropdown', component_property = 'value'),
        Input(component_id = 'payload-slider', component_property = 'value')
    ], 
)

def get_scatter_chart(site_, range_):
    
    ranged_df = spacex_df[spacex_df['Payload Mass (kg)'].between(range_[0], range_[1])]
    
    if site_ == 'ALL':
        fig = px.scatter(
            data_frame = ranged_df,
            x = 'Payload Mass (kg)',
            y = 'class',
            color = 'Booster Version Category',
            range_x = [range_[0], range_[1]],
            title = "Correlation between Payload and Success for All Sites"
            
        )
    else:
        filtered_df = ranged_df[ranged_df['Launch Site'] == site_]
        fig = px.scatter(
            data_frame = filtered_df,
            x = 'Payload Mass (kg)',
            y = 'class',
            color = 'Booster Version Category',
            range_x = [range_[0], range_[1]],
            title = "Correlation between Payload and Success for Site {site_}".format(site_ = site_)
        )
    
    return fig

if __name__ == '__main__':
    app.run_server()