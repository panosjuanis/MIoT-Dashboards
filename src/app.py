# Run this app with `python app_name.py` and
# visit http://127.0.0.1:8888/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Output, Input
from pages.fraility import phase_names, split_participant_names, e4_data_to_df


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


#------------------------------------------------FUNCTIONS------------------------------------------------------- 
def get_hr_fig(experiment_letter, experiment_id):
    # give each phase its name
    phase_names = ['start', 'standup', 'walkingToStore', 'inEntrance', 'walkingToCorrectSection',
                    'pickUpItem', 'walkingToCheckout', 'inTheCheckout', 'inItsTurn', 'goToTheExit',
                    'inTheExit', 'comingBack', 'inTheStartPoint', 'end']
    # read file
    filepath = f"../../FrailtyStudy_Datasets/Cuestionarios y Wearables/Wearable Data/raw_data/{experiment_letter + str(experiment_id)}/es.ugr.frailty.heartrate.csv"
    columns = ['timestamp', 'day_month_year', 'hour_min_sec_ms', 'hr', 'phase']
    hr = pd.read_csv(filepath, names = columns)
    sample_size = 25
    n_samples = hr[::sample_size].shape[0]

    # Plot the data using plotly.express
    fig = px.line(hr[::sample_size], x='hour_min_sec_ms', y='hr', title="Heart rate in fraility experiment by phase", labels={'hour_min_sec_ms':'Time (hours:minutes:seconds)', 'hr':'Heart rate (beats per minute)'})

    # Update x-axis labels
    fig.update_xaxes(tickvals=np.arange(0, n_samples, step=n_samples/hr['phase'].max()),
                     ticktext=phase_names)
    return fig

def getFrailityPage():
    # HTML LAYOUT

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
                dbc.Col(dcc.Graph(id='heartrate-figure', figure=get_hr_fig('CM', 1))),
                dbc.Col(dcc.Graph(id='eda-figure', figure=get_hr_fig('CM', 1)))
            ]),
        ])
    ])

    

    return layout

#Dropdown callback to update the patient id dropdown
@app.callback(
        Output('experiment-number-dropdown', 'options'),
        Output('experiment-number-dropdown', 'value'),
        Input('experiment-letter-dropdown', 'value'))
def update_dropdown(selected_letter):
    print(f"Updating dropdown value! {selected_letter}")

    return experiment_id_dict[selected_letter], experiment_id_dict[selected_letter][0]


#Dropdown callback to update hr graph
@app.callback(
        Output('heartrate-figure', 'figure'),
        Input('experiment-letter-dropdown', 'value'),
        Input('experiment-number-dropdown', 'value'))
def update_hr_graph(selected_letter, selected_number):
    print(f"Updating dropdown value! {selected_letter}, {selected_number}")

    return get_hr_fig(selected_letter, selected_number)


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


#----------------------------DASH APP----------------------------------------------

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
                dbc.NavLink("Sensores en Tiempo real", href="/", active="exact"),
                dbc.NavLink("Experimento Fragilidad", href="/fragilidad", active="exact"),
                dbc.NavLink("Experimento Dependencia", href="/dependencia", active="exact"),
                dbc.NavLink("Experimento Estrés", href="/estres", active="exact"),
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
    elif pathname == "/fragilidad":
        return fraility.layout
    elif pathname == "/dependencia":
        return html.P("Oh cool, this is page 2!")
    elif pathname == "/estres":
        return html.P("Página del experimento del estrés")
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