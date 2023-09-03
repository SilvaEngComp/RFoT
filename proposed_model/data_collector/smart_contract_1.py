# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva

This is a Smart contract wich receive data collected by sensor and received by gateway
and call for SC2 to miner a block for a transaction
"""

from corruptedBlockchain import CorruptedBlockchain
from pool import Pool
from smart_contract_2 import SC2
from transaction import Transaction
import json
class SC1:
    def __init__(self, node, blockWidth=20):
        self._node = node
        self._blockWidth = self.checkBlockWidth(blockWidth)
        self._transactions = []
    
    

    def dataTreating(self,msg):
        msgJson = json.loads(msg.payload)
        if 'data' in msgJson:
            if self.validTemp(msgJson['data']) is True:
                transaction = Transaction(msgJson['header']['device'],msgJson['header']['sensor'],self._node, msgJson['data'])
                return self.mineBlock(transaction)
        return False
            
    def validTemp(self,temp):
        if float(temp)>16 and float(temp)<40:
            return True
        return False
    
    def mineBlock(self, transaction):  
        self._transactions.append(transaction)
        print("{}/{} - {}".format(len(self._transactions),self._blockWidth,transaction.data))
       
        if len(self._transactions)>=self._blockWidth:
            print("A new Block was minner? = ",SC2.minerNotAssinedTransaction(self._node,self._transactions))
            # pool = Pool()
            # pool.add(self._transactions)
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