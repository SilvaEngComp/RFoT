# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva
"""

from corruptedBlockchain import CorruptedBlockchain

class Iotcoin:
    def __init__(self, node, blockWidth=20):
        self._node = node
        self._blockWidth = self.checkBlockWidth(blockWidth)
        self._transactions = []
    
    def mineBlock(self, transaction):
        self._transactions.append(transaction)
        print("{}/{}".format(len(self._transactions),self._blockWidth))
       
        if len(self._transactions)>=self._blockWidth:
            pool = Pool()
            pool.add(self._transactions)
            return True
        return False
    
    def checkBlockWidth(self, blockWidth):
        if(blockWidth is None):
                blockWidth=20
        elif isinstance(blockWidth, str):
            blockWidth = int(blockWidth)
        return blockWidth
    def restart(self):
        self._transactions = []        
    
    def corruptData(self, transaction):
        self._transactions.append(transaction)
        print("{}/{}".format(len(self._transactions),self._blockWidth))
        
        if len(self._transactions)>=self._blockWidth:
            CorruptedBlockchain.corruptBlockchain()
            return True
        return False