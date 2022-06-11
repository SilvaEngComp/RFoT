

import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml')
from blockchain import Blockchain
from fd_model import FdModel

node = 'h1'
blockchain = Blockchain(node)
prefix = '../'
blockchain.chain = blockchain.solveBizzantineProblem(prefix, True)
print(blockchain.chain)
fdModel = FdModel(node,blockchain.chain)
fdModel.preprocessing(0.5)
print('Model {} published in: ' .format(fdModel))