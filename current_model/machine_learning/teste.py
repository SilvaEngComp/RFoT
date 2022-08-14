
import os
import datetime
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/current_model/data_collector')

from no_blockchain import NoBlockchain
from block import Block
from fd_model import FdModel
import numpy as np
from time import sleep
import time


node = 'h1'
block = NoBlockchain.getNotAssinedBlock()
fdModel = FdModel(node,block)
fdModel.preprocessing(0.1)
            