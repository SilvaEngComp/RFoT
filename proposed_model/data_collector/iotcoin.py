# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva
"""

from blockchain import Blockchain
import json
import os
from node import Node

class Iotcoin:
    def __init__(self, node, blockWidth=20):
        self.blockchain = Blockchain(node)
        self.blockchain.node = node
        if(blockWidth is None):
            blockWidth=20
        elif isinstance(blockWidth, str):
            blockWidth = int(blockWidth)
        self.blockWidth = blockWidth
        self.pool = []
        Node.add(node)
        print(self.blockWidth)
    
    def mineBlock(self, transaction):
        self.pool.append(transaction)
        print("{}/{}".format(len(self.pool),self.blockWidth))
       
        if len(self.pool)>=self.blockWidth:
            self.blockchain.createBlock(self.pool)
            return self.blockchain
        
        return None
     
    
    def blockchainRestart(self):
        self.pool = []
        #node = self.blockchain.node
        #self.blockchain = Blockchain(node)
  