
import os
import datetime
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/proposed_model/data_collector')

from blockchain import Blockchain
from block import Block
from fd_model import FdModel
import numpy as np
from time import sleep
import time


node = 'h1'
block = Blockchain.getNotAssinedBlock(node)
fdModel = FdModel(node,block)
fdModel.preprocessing(0.002)
if fdModel.getModel() is not None:
    Blockchain.setAssinedBlockModel(node,"localModel",fdModel.toJson())