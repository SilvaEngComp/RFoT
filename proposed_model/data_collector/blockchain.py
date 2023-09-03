# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/proposed_model/data_collector')

import time
import datetime
import hashlib
import json
import os
import ast
from block import Block
from transaction import Transaction
from node import Node
import re
from pool import Pool
from cipher import Cipher

class Blockchain:
    def __init__(self, node, blockchainType):
        self.node = node
        self.blockchainType = blockchainType
        self.fileName = str(blockchainType+str(self.node)+'.json')
        self.fileNameNotCript = str('blockchain_notCript_'+str(self.node)+'.json')
        self.chain = []
        self.nodes = set()
        self.cipher = Cipher()


    def __str__(self):

        return str({
        "chain": self.chain,
        })
    def __repr__(self):
        return str({
        "chain": self.chain,
        })
    
    def toJson(self):
        chain = []
        for block in self.chain:
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
                self.chain = chain  
                return chain
        except:
            if isinstance(data, Blockchain(node)):
                return data
            print('That is not a dict object. Try it again!')

    def registerEncripted(self, prefix="../data_collector/"):
        fileName = str(prefix + self.fileName) 
        fileNameNotCript = str(prefix +self.fileNameNotCript)
        with open(fileNameNotCript,'rb') as blockchainEncFile:     
            data = blockchainEncFile.read()
        encrypted = self.cipher.encrypt(data)
        with open(fileName,'wb') as f:              
            f.write(encrypted)

    def register(self, prefix="../data_collector/"):
        fileNameNotCript = str(prefix +self.fileNameNotCript)
        with open(fileNameNotCript,'w') as blockchainFile:            
            print('registring new chain in {} with {} blocks '.format(self.fileName, len(self.chain)))
            json.dump(self.toJson(), blockchainFile)



    def createBlock(self, pool, typeBlock="data"):
        previousBlock = self.getPreviousBlock()
        
        if previousBlock is None:
            block = Block(pool, self.node,typeBlock)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(pool,self.node,typeBlock,(previousBlock.index+1),proof,previousHash)
        self.chain.append(block)
        if(self.isChainValid(self.chain)):
            self.register()
            self.registerEncripted()
        else:
            self.chain = []
        
        return block
            
        


    def getPreviousBlock(self): 
        chain = self.solveBizzantineProblem()
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
        
            
        print("starting solving challenge...")
        while True:
            hashOperation = self.getHashOperation(previous_proof, new_proof)
            if self.checkPuzzle(hashOperation) is True:
                break
            else:
                new_proof +=1
        print("challenge solved...")
        return new_proof                            

    
    def checkPuzzle(self,hash_test):
        if hash_test[0:4]=='0000':
            return True
            return False
    
    def getHashOperation(self,previous_proof, new_proof):
        return hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
        
        
    
    def hash(self,value):
        try:
            if isinstance(value, Block):
                value = str(value)
                encoded = json.dumps(value).encode()
                return hashlib.sha256(encoded).hexdigest()
        except:
            print('It can not get the hash of not Block: ',type(value))
            return None
        
    
    def isChainValid(self,chain):
        previousBlock = chain[0]
        blockIndex=1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            previousBlockHash = self.hash(previousBlock)
            if block.previousHash != previousBlockHash:
                return False
            previousProof = previousBlock.proof
            proof = block.proof
            hashOperation = self.getHashOperation(previousProof, proof)
            if self.checkPuzzle(hashOperation) is False:
                return False
            previousBlock = block
            blockIndex += 1
        return True


          
    def getLocalBLockchainFile(self,node = None, prefix='../data_collector/'):
        if node is not None:
            x = re.search("^"+self.blockchainType+".*json$", node)
            if(x is False):
                fileName = str(prefix + self.blockchainType+node+'.json')   
            else:
                fileName = str(prefix + node) 
            if os.path.exists(fileName) is False:
                return []
            
            
            try:
                with open(fileName, 'rb') as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        cipher = Cipher()
                        data = blockchainFile.read()
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        return Blockchain.fromJson(dataJson['chain'])
            except:
                print('not found local blockchain file: ',node)
                return []
    
      
    def getBlockchainFileNames(self,prefix='../data_collector/'):
        fileNames = []
        for file in os.listdir(prefix):
            if file.endswith(".json"):
                x = re.search("^"+self.blockchainType+".*json$", file)
                if(x):
                    fileNames.append(file)
        return fileNames
                    
              
    def solveBizzantineProblem(self,):
        try:            
            nodes = self.getBlockchainFileNames()
            longest_chain = None
            max_length = 0
            nameNode=None
            if(nodes):
                for node in nodes:
                    chain = self.getLocalBLockchainFile(node)
                    length = len(chain)
                    isValide = self.isChainValid(chain)
                    if length>max_length and isValide:
                        max_length = length
                        longest_chain = chain
                        nameNode = node
            else:
                longest_chain = []
            print('The current biggest chain is {} with {} blocks'.format(nameNode, len(longest_chain)))
            return longest_chain
        except:
            print('Something wrong happen in replaceChain...')
            
    
            
    