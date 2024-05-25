from dash import html, dash_table

import dash_bootstrap_components as dbc  
import pandas as pd
from dash_app import app
from dash.dependencies import Output, Input



df = pd.read_csv('../intel_lab.csv', delimiter=",")
start=0
end=1000
df=df[start:end]
buttonName = str(start)+' - '+str(end)
# print(df.to_dict('records'))
# return html.Div([
#     html.H1("Temperature from Intel Lab Dataset"),
layout = html.Div([
    dbc.Input(id='start_id', type='hidden',value=start),
    dbc.Input(id='end_id', type='hidden',value=end),
    dash_table.DataTable(
    id="datatable_id",
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    editable=False,
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                row_deletable=False,
                selected_rows=[],
                page_action='native',
                page_current=0,
                page_size=10,),
                    
                    dbc.Button(id='next-button',children=buttonName,n_clicks=0),
                    ],
                
                
                )

@app.callback(
    Output("datatable_id",'data'),
    Output("next-button",'children'),
    Input('next-button', 'n_clicks'),
    )
def next_block(n_clicks):
    start_filtred= start
    end_filtred= end
    start_filtred+=100*n_clicks
    end_filtred+=100*n_clicks
    df_filtred=df[start_filtred:end_filtred]
    buttonName = str(start_filtred)+' - '+str(end_filtred)
    return df_filtred.to_dict('records'),buttonName

    
