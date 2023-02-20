# app.py
# Follow the steps to execute app:
# >python app.py 
# -visit http://127.0.0.1:8888/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

from dash import html, dcc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)


#----------------------------DASH APP----------------------------------------------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


navbar = html.Div(
    [
        html.H2("MIoT", className="display-4"),
        html.Hr(),
        html.P(
            "Seleccione el experimento que desea visualizar", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Link(f"{page['name']}", href=page["relative_path"])
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = dbc.Container(
    [
        dbc.Row([
                     dbc.Col([navbar], xs=3, sm=3, md=3, lg=3, xl=3, xxl=3), #Navbar column
                     dbc.Col([dash.page_container], xs=9, sm=9, md=9, lg=9, xl=9, xxl=9) #Content column
                ])
    ],
    fluid=True
)

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)