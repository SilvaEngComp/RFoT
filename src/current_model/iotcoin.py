# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva
"""
from time import sleep
from src.current_model.pool import Pool
from src.utils.time_register import TimeRegister
class Iotcoin:
    def __init__(self, node, blockWidth=20):
        
        self._node = node
        self._blockWidth = self.checkBlockWidth(blockWidth)
        self._transactions = []
    
    def transactionProcess(self, transaction):
        self._transactions.append(transaction)
        print("{}/{}".format(len(self._transactions),self._blockWidth))
       
        if len(self._transactions)>=self._blockWidth:
            TimeRegister.addTime("Transaction completed - initing storing")
            pool = Pool()
            pool.add(self._transactions)
            return True
        elif len(self._transactions)==1:
            TimeRegister.addTime("Starting collection")
            
        return False
    
    def corruptData(self, transaction):
        self._transactions.append(transaction)
        print("{}/{}".format(len(self._transactions),self._blockWidth))
       
        if len(self._transactions)>=self._blockWidth:
            Pool.setCorruptTransactions()
            return True
        return False
    
    def checkBlockWidth(self, blockWidth):
        if(blockWidth is None):
                blockWidth=20
        elif isinstance(blockWidth, str):
            blockWidth = int(blockWidth)
        if blockWidth<10:
            raise Exception('The minimum size is 10 samples')
        return blockWidth
    def restart(self):
        self._transactions = []        