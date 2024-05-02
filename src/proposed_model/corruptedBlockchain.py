# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
import random
import time
import datetime
import hashlib
import json
import os
import ast
from src.suport_layer.block import Block
from src.suport_layer.transaction import Transaction
import re


class CorruptedBlockchain:
    def __init__(self, node):
        self.node = node
        self.chain = []


    def __str__(self):

        return str({
        "chain": self.chain,
        })
    def __repr__(self):
        return str({
        "chain": self.chain,
        })
    
    @staticmethod 
    def toJson(corruptedChain):
        chain = []
        for block in corruptedChain:
            chain.append(Block.toJson(block))
        return {
        "chain": chain,
        }
        
    @classmethod
    def fromJson(self, data):
        try:
            if isinstance(data, list):
                chain = []
                for jsonBlock in data:
                    chain.append(Block.fromJson(jsonBlock))  
                return chain
        except:
            if isinstance(data, CorruptedBlockchain(node)):
                return data
            print('That is not a dict object. Try it again!')

    


    def getPreviousBlock(self)->Block: 
        chain = CorruptedBlockchain.solveBizzantineProblem()
        if chain is None:
            return None
        elif len(chain)>0:            
            self.chain = chain          
            return self.chain[-1]
        return None
                                    

    def proofOfWork(self, previous_proof, new_proof = 1):
        if isinstance(previous_proof,str):
            previous_proof = int(previous_proof)
        if isinstance(new_proof,str):
            new_proof = int(new_proof)
        
        while True:
            hashOperation = self.getHashOperation(previous_proof, new_proof)
            if self.checkPuzzle(hashOperation) is True:
                break
            else:
                new_proof +=1
        return new_proof                            

    @staticmethod
    def checkPuzzle(hash_test):
        if hash_test[0:4]=='0000':
            return True
            return False
    @staticmethod
    def getHashOperation(previous_proof, new_proof):
        return hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
        
        
    @staticmethod
    def hash(value):
        try:
            if isinstance(value, Block):
                value = str(value)
                encoded = json.dumps(value).encode()
                return hashlib.sha256(encoded).hexdigest()
        except:
            print('It can not get the hash of not Block: ',type(value))
            return None
        
    @staticmethod
    def isChainValid(chain):
        previousBlock = chain[0]
        blockIndex=1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            previousBlockHash = CorruptedBlockchain.hash(previousBlock)
            if block.previousHash != previousBlockHash:
                return False
            previousProof = previousBlock.proof
            proof = block.proof
            hashOperation = CorruptedBlockchain.getHashOperation(previousProof, proof)
            if CorruptedBlockchain.checkPuzzle(hashOperation) is False:
                return False
            previousBlock = block
            blockIndex += 1
        return True


    @staticmethod      
    def getLocalBLockchainFile(node = None, prefix='../data_collector/'):
        if node is not None:
            x = re.search("^blockchain.*json$", node)
            if(x is False):
                fileName = str(prefix + 'blockchain_'+node+'.json')   
            else:
                fileName = str(prefix + node) 
            if os.path.exists(fileName) is False:
                return []
            try:
                with open(fileName) as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        data = json.load(blockchainFile)['chain']
                        return CorruptedBlockchain.fromJson(data)
            except:
                print('not found local blockchain file: ',node)
                return []
    
    @staticmethod  
    def getBlockchainFileNames(prefix='../data_collector/'):
        fileNames = []
        for file in os.listdir(prefix):
            if file.endswith(".json"):
                x = re.search("^blockchain.*json$", file)
                if(x):
                    fileNames.append(file)
        return fileNames
    
    @staticmethod 
    def register(corruptedBlockchain):
        with open(corruptedBlockchain.node,"w") as blockchainFile:
            print('corrupting {}...  '.format(corruptedBlockchain.node))
            json.dump(CorruptedBlockchain.toJson(corruptedBlockchain.chain), blockchainFile)
            
    @staticmethod          
    def corruptBlockchain():
        try:            
            nodes = CorruptedBlockchain.getBlockchainFileNames()
            longest_chain = None
            max_length = 0
            nameNode=None
            cont=0
            if(nodes):
                for node in nodes:
                    if("blockchain_h3.json" == node):
                        continue
                        
                    chain = CorruptedBlockchain.getLocalBLockchainFile(node)
                    if(len(chain)>0):
                        corruptedChain=[]
                        for block in chain:
                            corruptedTransactions=[]
                            for transaction in block['transactions']:
                                newTransaction = Transaction(transaction.sender, transaction.sensor, transaction.receiver, random.randint(1,1000))
                                corruptedTransactions.append(newTransaction)
                            
                            
                            corruptedBlock = Block(corruptedTransactions,block.hostTrainer,block.typeBlock, block.index,block.proof,block.previousHash, block.timestamp)
                            corruptedChain.append(corruptedBlock)
                        corruptedBlockchain = CorruptedBlockchain(node)
                        corruptedBlockchain.chain = corruptedChain
                        CorruptedBlockchain.register(corruptedBlockchain)
                        
        except:
            print('Something wrong happen in replaceChain...')
    
          
    