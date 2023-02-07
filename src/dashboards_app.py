# Run this app with `python app_name.py` and
# visit http://127.0.0.1:8888/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Output, Input


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def getFrailityPage():
    filepath = "../../FrailtyStudy_Datasets/Cuestionarios y Wearables/Wearable Data/raw_data/CM1/es.ugr.frailty.heartrate.csv"
    columns = ['timestamp', 'day_month_year', 'hour_min_sec_ms', 'hr', 'phase']
    hr = pd.read_csv(filepath, names = columns)
    sample_size = 25
    n_samples = hr[::sample_size].shape[0]
    # Plot the data using plotly.express
    fig = px.line(hr[::sample_size], x='hour_min_sec_ms', y='hr', title="Heart rate in fraility experiment by phase")

    # Update x-axis labels
    fig.update_xaxes(tickvals=np.arange(0, n_samples, step=n_samples/hr['phase'].max()),
                    ticktext=hr['phase'].unique())

    # fig.show()
    layout = html.Div([
        dcc.Graph(
            id='example-figure',
            figure=fig
        )
    ])

    return layout





def getStreamingPage():

    layout = html.Div(className='row', children=[
    html.H1("Datos en streaming de sensores"),
    dcc.Dropdown(['TicWatch', 'Empatica', 'Fitbit'], 'TicWatch', id='sensor-dropdown'),
    html.Div(children=[
        dcc.Graph(id="graph1", style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", style={'display': 'inline-block'})
    ])
])






    return layout

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("MIoT", className="display-4"),
        html.Hr(),
        html.P(
            "Seleccione el experimento que desea visualizar", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Sensores en tiempo real", href="/", active="exact"),
                dbc.NavLink("Experimento Fragilidad", href="/fragilidad", active="exact"),
                dbc.NavLink("Experimento Dependencia", href="/dependencia", active="exact"),
                dbc.NavLink("Otros experimentos", href="/otros", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return getStreamingPage()
    elif pathname == "/page-1":
        return getFrailityPage()
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888)