# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva
"""

from blockchain import Blockchain
import json
import os

class Iotcoin:
    def __init__(self, node):
        self.blockchain = Blockchain(node)
        self.nodesFileName = 'nodes.json'
        self.addNode()
    
    def mineBlock(self, transaction):
        self.blockchain.pool.append(transaction)
        if len(self.blockchain.pool)>=10:
            print('pool before', len(self.blockchain.pool))
            self.blockchain.createBlock()
            print('pool after', len(self.blockchain.pool))
            return self.getChain()
        print( len(self.blockchain.pool),'/10')
        return None
    
    def getChain(self):
        self.replaceFileChain()
        response =  {'chain':str(self.blockchain.chain),
        'length': len(self.blockchain.chain)}
        self.blockchainRestart()   
        return response
    
    def blockchainRestart(self):
        self.blockchain.replaceChain()
        self.blockchain.chain = []
    
    def replaceFileChain(self):
        #try:
        with open(self.blockchain.fileName) as blockchainFile:
            if os.path.getsize(self.blockchain.fileName) > 0:
                data = json.load(blockchainFile)
                chain = self.blockchain.fromJson(data['chain'])
                if(len(chain) > 0):
                    for block in self.blockchain.chain:
                        print('transactions: ', len(block.transactions))
                        
                        chain.append(block)
                    self.blockchain.chain = chain
                    print('blockchain: ', len(self.blockchain.chain))
                self.blockchain.register()
                
        #except:
           # print('Iotcoin: not found ',self.blockchain.fileName)

    def addNode(self):
        nodes = set()
        try:
            with open(self.nodesFileName) as nodeFile:
                data = json.load(nodeFile)
                nodes = set(data['nodes'])
                nodes.add(self.blockchain.node)
        except:
            nodes.add(self.blockchain.node)
            with open(self.nodesFileName,'w+') as nodeFile:
                nodes = {"nodes": list(nodes)}
                json.dump(nodes, nodeFile)