
from src.proposed_model.smart_contract_3 import SC3
from src.current_model.no_blockchain import NoBlockchain
from fd_model import FdModel
from fd_client import FdClient
from src.suport_layer.block import Block
from integrator_model import IntegratorModel


def getdataBlock():
    block = None
    if solution == '1':
        block = NoBlockchain.getNotAssinedBlock()
    else:
        block = SC3.getNotAssinedBlock(sub_device)
    return block



solution= '1'
sub_device = "h2"
clients = 2
fdModel = FdModel(sub_device, None)
integragorModel = IntegratorModel(fdModel, clients,True)

if integragorModel.getGlobalModel() is None:
    while (True):
        # os.system('clear')
        block = getdataBlock()
        if block is not None:
            fdModel = FdModel(sub_device, block)
            fdModel.preprocessing()
            if fdModel.hasValidModel():
                integragorModel = IntegratorModel(fdModel,clients)
                break
            else:
                sleep(5)
        else:
            sleep(5)