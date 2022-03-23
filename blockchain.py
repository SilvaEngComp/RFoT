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
        self.pool = []


    def __str__(self):

        return str({
        "chain": self.chain,
        "node":self.node,
        "pool": self.pool
        })
    def __repr__(self):
        return str({
        "chain": self.chain,
        "node":self.node,
        "pool": self.pool
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
            json.dump(self.toJson(), blockchainFile)


    def createBlock(self):
        previousBlock = self.getPreviousBlock()
        
        if previousBlock is None:
            block = Block(self.pool)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(self.pool,(previousBlock.index+1),proof,previousHash)
        
        self.chain.append(block)
        self.register()
        return block


    def getPreviousBlock(self):
        print('getting previous block')
        chain = self.solveBizzantineProblem()
        
        if chain is None:
            return None
        elif len(chain)>0:            
            self.chain = chain            
            return self.chain[-1]
        return None

    def check_puzzle(self, hash_test):
        if hash_test[0:4]=='0000':
            return True
            return False                                

    def proofOfWork(self, previous_proof):
        new_proof = 1
        previous_proof = int(previous_proof)
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if self.check_puzzle(hash_operation) is True:
                break
            else:
                new_proof +=1
                return new_proof                            

    def hash(self, block):
        if isinstance(block, Block):
            block = str(block)
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def isChainValid(self, chain):
        print('validating chain...')
        previousBlock =Block.fromJson(chain[0])
        print('pass..')
        blockIndex=1
        while blockIndex < len(chain):
            block = Block.fromJson(chain[blockIndex])
            if block.previousHash != self.hash(previousBlock):
                return False
            previousProof = previousBlock.proof
            proof = block.proof
            hashOperation = hashlib.sha256(str(proof**2-previousProof**2).encode()).hexdigest()
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
            print('solving Bizzantine Problem')
            nodes = Node.get(prefix)
            longest_chain = None
            
            max_length = 0
            for node in nodes:
                print('checking node: ',node)
                chain = self.getLocalBLockchainFile(node,prefix,training)
                length = len(chain)
                isValide = self.isChainValid(chain)
                print('length: ', length, 'max_length: ',max_length)
                print('isValid: ', isValide )
                print(length>max_length and isValide)
                if length>max_length and self.isChainValid(chain):
                    max_length = length
                    longest_chain = chain
            return longest_chain
        except:
            print('Something wrong happen in replaceChain...')