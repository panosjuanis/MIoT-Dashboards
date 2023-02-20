import os
import pandas as pd
import numpy as np
import datetime
import dash_bootstrap_components as dbc
import dash
import plotly.express as px

from dash import Dash, html, dcc, Output, Input, callback
from pages.fraility_functions import get_figure, experiment_id_dict, E4_EDA, E4_HEARTRATE

dash.register_page(__name__, name="Fraility Experiment")

#------------------------------------------PAGE LAYOUT------------------------------------------------------
layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(['CM', 'E', 'Z'], 'CM', id='experiment-letter-dropdown')),
            dbc.Col(dcc.Dropdown(experiment_id_dict['CM'], experiment_id_dict['CM'][0], id='experiment-number-dropdown'))
        ]),
    ],
    style={
        
        "width": "20%"
    }),

    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id='heartrate-figure', figure=get_figure('CM5', E4_EDA))),
            dbc.Col(dcc.Graph(id='eda-figure', figure=get_figure('CM5', E4_HEARTRATE)))
        ]),
    ])
])


#---------------------------------------------CALLBACKS----------------------------------------------------
#Dropdown callback to update the patient id dropdown
@callback(
        Output('experiment-number-dropdown', 'options'),
        Output('experiment-number-dropdown', 'value'),
        Input('experiment-letter-dropdown', 'value'))
def update_dropdown(selected_letter):
    print(f"Updating dropdown value! {selected_letter}")

    return experiment_id_dict[selected_letter], experiment_id_dict[selected_letter][0]

#Figure callback to update the figure
@callback(
        Output('heartrate-figure', 'figure'),
        Output('eda-figure', 'figure'),
        Input('experiment-letter-dropdown', 'value'),
        Input('experiment-number-dropdown', 'value'))
def update_figure(selected_letter, selected_number):
    print(f"Updating figure! {selected_letter}, {selected_number}")
    participant = str(selected_letter) + str(selected_number)
    return get_figure(participant, E4_EDA), get_figure(participant, E4_HEARTRATE)