from dash import html, dash_table

import dash_ag_grid as dag

import dash_bootstrap_components as dbc  
import pandas as pd
from dash_app import app
from dash.dependencies import Output, Input
from src.proposed_model.smart_contract_3 import SC3
from src.proposed_model.smart_contract_3 import Blockchain
import dash_mantine_components as dmc

blockchain = SC3.getBCD("h1")
size=0
if blockchain.chain is not None:
    data = blockchain.toJsonDecrypted()
    size =str(len(data['chain']))

else:
    b1 = Blockchain()
    data = b1.chain
    
def create_accordion_label(label):
    return dmc.AccordionControl(
        dmc.Group(
            [
                html.Div([
                    dmc.Text(label)
                ])
            ]
        )
    )

def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content,size='sm'))

print(data['chain'])
layout = html.Div([
    html.H1("This is the data collected and registred in BCD (Data Blockchain)"),
    html.H2("# There are "+str(size)+" blocks"),
    dmc.Accordion(
        chevronPosition='right',
        variant='container',
        children=[
            dmc.AccordionItem(
                [
                    create_accordion_label(block['index']),
                    create_accordion_content(block['typeBlock'])
                ],
                 value=block['proof'],
            )
           for block in data['chain']
        ]
    )
     
                    ],
              )

    
