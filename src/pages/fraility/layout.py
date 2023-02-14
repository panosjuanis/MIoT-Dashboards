import os
import pandas as pd
import numpy as np
import datetime
import dash_bootstrap_components as dbc

from dash import Dash, html, dcc, Output, Input
from app import app

from functions import experiment_id_dict, get_fig


#------------------------------------------PAGE LAYOUT------------------------------------------------------
# DROPDOWNS
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
            dbc.Col(dcc.Graph(id='heartrate-figure', figure=get_fig('CM', 1))),
            dbc.Col(dcc.Graph(id='eda-figure', figure=get_fig('CM', 1)))
        ]),
    ])
])