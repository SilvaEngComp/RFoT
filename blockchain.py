# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
import time
import datetime
import hashlib
import json
import os
import ast
from block import Block
from transaction import Transaction
from node import Node


class Blockchain:
    def __init__(self, node):
        self.node = node
        self.fileName = str('blockchain_'+str(self.node)+'.json')
        self.chain = []
        self.nodes = set()


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
                return chain
        except:
            if isinstance(data, Blockchain(node)):
                return data
            print('That is not a dict object. Try it again!')

    def register(self):
        with open(self.fileName,"w") as blockchainFile:
            print('registring: ',self.fileName)
            json.dump(self.toJson(), blockchainFile)


    def createBlock(self, pool):
        previousBlock = self.getPreviousBlock()
        
        if previousBlock is None:
            block = Block(pool)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(pool,(previousBlock.index+1),proof,previousHash)
        
        self.chain.append(block)
        if(self.isChainValid(self.chain)):
            self.register()
        else:
            self.chain = []
            
        


    def getPreviousBlock(self):
        chain = self.solveBizzantineProblem()
        if chain is None:
            return None
        elif len(chain)>0:            
            self.chain = chain            
            return self.chain[-1]
        return None

    def checkPuzzle(self, hash_test):
        if hash_test[0:4]=='0000':
            return True
            return False                                

    def getHashOperation(self,previous_proof, new_proof):
        return hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
        
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

    def hash(self, value):
        try:
            if isinstance(value, Block):
                value = str(value)
                encoded = json.dumps(value).encode()
                return hashlib.sha256(encoded).hexdigest()
        except:
            print('It can not get the hash of not Block: ',type(value))
            return None

    def isChainValid(self, chain):
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


        
    def getLocalBLockchainFile(self, node = None, prefix = '',  training=False):
        if node is None:
            node = self.node
        
        fileName = str(prefix + 'blockchain_'+node+'.json')   
        
        if os.path.exists(fileName) is False:
            return self.chain
        
        try:
            with open(fileName) as blockchainFile:
                if os.path.getsize(fileName) > 0:
                    data = json.load(blockchainFile)['chain']
                    return Blockchain.fromJson(data)
        except:
            print('not found local blockchain file: blockchain_'+self.node+'.json')
            return self.chain
    
    
    def solveBizzantineProblem(self, prefix='', training=False):
        try:
            nodes = Node.get(prefix)
            longest_chain = None
            
            max_length = 0
            nameNode=None
            for node in nodes:
                chain = self.getLocalBLockchainFile(node,prefix,training)
                length = len(chain)
                isValide = self.isChainValid(chain)
                if length>max_length and isValide:
                    max_length = length
                    longest_chain = chain
                    nameNode = node
            return longest_chain
        except:
            print('Something wrong happen in replaceChain...')