"""
    This is a Smart contract wich gets a block from in Data Blockchain
"""
from .blockchain import Blockchain
from src.suport_layer.block import Block
import random
from src.suport_layer.cipher import Cipher
from src.utils.time_register import TimeRegister
import json
import os
class SC2:
    @staticmethod
    def minerNotAssinedTransaction(node, transactions,blockType="data"):
        print("getting transactions")
        # transactions = Pool.getNotAssinedTransactions()      
        blockchain = Blockchain(node)
        before = len(blockchain.chain)
        print("size before = ",before)
        dataBlock = SC2.getLasDataBlock(node)
        
        blockchain.createBlock(transactions,blockType,dataBlock)
        after = len(blockchain.chain)
        print("size after = ",after)
        if(after>before):
            TimeRegister.addTime("data received from sensor")
            return True
        else:
            return False 
    
    @staticmethod
    def getLasDataBlock(node = None):
        if node is not None:
            fileName = str("lastBlockReaded_"+str(node)+'.json')
            try:
                with open(fileName, 'rb') as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        cipher = Cipher()
                        data = blockchainFile.read()
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        dataJson= Block.fromJson(dataJson)
                        return dataJson
            except:
                print('not found local blockchain file: ',fileName)
                return []