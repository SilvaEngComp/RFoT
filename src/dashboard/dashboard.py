from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from src.proposed_model.smart_contract_3 import SC3
import json
from src.proposed_model.blockchain import Blockchain
import pandas as pd
from src.current_model.pool import Pool
import matplotlib.animation as animation
from time import sleep
import pages
from dash_app import app

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
            dbc.NavLink("home", href="/", active="exact"),
            dbc.NavLink("Intel Lab Dataset", href="/intel_lab", active="exact"),
            dbc.NavLink("Current IoT Data", href="/current_iot", active="exact"),
            dbc.NavLink("Blockchain Data", href="/blockhain", active="exact"),
            dbc.NavLink("Consumer Dataset", href="/consumer_dataset", active="exact"),
            dbc.NavLink("Comparing Time operation", href="/time_comparing", active="exact"),
            dbc.NavLink("Training results", href="/training_results", active="exact"),
            
        ],
        vertical=True,
        pills=True
        ),
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id='page-content', style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id='url'), sidebar,content])

@app.callback(Output("page-content", "children"),[Input("url", "pathname")])
def render_page_content(pathname):
   
    if pathname == "/":
        return pages.dash_home.layout
    if pathname == "/intel_lab":
        return pages.dash_intel_lab.layout
    if pathname == "/blockhain":
        return pages.dash_blockchain.layout

if __name__=="__main__":
    app.run_server(debug=True)
