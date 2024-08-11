import os
import argparse
import json
import paho.mqtt.client as mqtt
from src.proposed_model.smart_contract_3 import SC3
from src.current_model.no_blockchain import NoBlockchain
from fd_model import FdModel
from fd_client import FdClient
from src.suport_layer.block import Block
from integrator_model import IntegratorModel
from time import sleep
import datetime
import sys
solution = '1'
sub_device="h_teste"

def getdataBlock():
    block = None
    if solution == '1':
        block = NoBlockchain.getNotAssinedBlock()
    else:
        block = SC3.getNotAssinedBlock(sub_device)
    return block

while (True):
    block = getdataBlock()
    if block is not None:
        fdModel = FdModel(sub_device, block)
        fdModel.preprocessing()
        if fdModel.hasValidModel():
            integragorModel = IntegratorModel(fdModel, args.clients)
            print(f'treinamento completo')
            print(integragorModel)
            break
        else:
            sleep(5)
    else:
        sleep(5)
