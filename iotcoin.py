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
    def __init__(self, node):
        self.blockchain = Blockchain(node)
        self.blockchain.node = node
        self.blockWidth = 2
        Node.add(node)
    
    def mineBlock(self, transaction):
        self.blockchain.pool.append(transaction)
        if len(self.blockchain.pool)>=self.blockWidth:
            self.blockchain.createBlock()
            return self.blockchain
        print( len(self.blockchain.pool),'/10')
        return None
     
    
    def blockchainRestart(self):
        print('restarting pool', len(self.blockchain.pool))
        self.blockchain.pool = []
        self.blockchain.chain = []
        print('pool restarted', len(self.blockchain.pool))
  