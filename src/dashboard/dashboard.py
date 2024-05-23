from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from src.proposed_model.smart_contract_3 import SC3
import json
from src.proposed_model.blockchain import Blockchain
import pandas as pd
from src.current_model.pool import Pool
import matplotlib.animation as animation
from time import sleep

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    'position':'fixed',
    'top':0,
    'left':0,
    'bottom':0,
    'width':'16rem',
    'padding':'2rem 1rem',
    'background-color':'#f8f9fa'
}

CONTENT_STYLE={
    'margin-left':'18rem',
    'margin-right':'2rem',
    'padding':'2rem 1rem'
}

sidebar = html.Div(
    [
    html.H2("RFoT", className="display-4"),
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("Intel Lab Dataset "),
            dbc.NavLink("Current IoT Data"),
            dbc.NavLink("Blockchain Data"),
            dbc.NavLink("Consumer Dataset"),
            dbc.NavLink("Comparing Time operation"),
            dbc.NavLink("Training results"),
            
        ],
        vertical=True,
        pills=True
        ),
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id='page-content', style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id='url'), sidebar,content])

app.run_server(port=8888, debug=True)
