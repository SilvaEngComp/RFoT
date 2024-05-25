from dash import html, dash_table

import dash_bootstrap_components as dbc  
import pandas as pd
from dash_app import app

layout =  html.Div([
        html.H1("Temperature from Intel Lab Dataset"),
    # return    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ])
