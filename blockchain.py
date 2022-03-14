# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""

import datetime
import hashlib
import json
import os
import ast
from block import Block
from transaction import Transaction


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
            chain.append(block.toJson())
        return {
        "chain": chain,
        }
    def fromJson(self, data):
        pool = []
        chain = []
        for block in data:
            for transaction in block['transactions']:
                pool.append(Transaction(transaction['sender'],transaction['sensor'],transaction['receiver'],transaction['data']))
        for jsonBlock in data:
            block = Block(jsonBlock['index'], jsonBlock['proof'],
            jsonBlock['previousHash'],pool, jsonBlock['timestamp'])
            chain.append(block)     
        return chain

    def register(self):
        with open(self.fileName,"w") as blockchainFile:
            json.dump(self.toJson(), blockchainFile)


    def createBlock(self):
        previousBlock = self.getPreviousBlock()
        proof = self.proofOfWork(previousBlock.proof)
        previousHash = self.hash(previousBlock)
        block = Block(previousBlock.index+1,proof,previousHash,self.pool)
        self.chain.append(block)
        self.pool = []
        return block


    def getPreviousBlock(self):
        chain = self.getLocalBLockchainFile()
        return chain[-1]

    def check_puzzle(self, hash_test):
        if hash_test[0:4]=='0000':
            return True
            return False                                

    def proofOfWork(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if self.check_puzzle(hash_operation) is True:
                break
            else:
                new_proof +=1
                return new_proof                            

    def hash(self, block):
        encoded_block = json.dumps(str(block),sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def isChainValid(self, chain):
        print('validing chain...')
        previous_block = chain[0]
        block_index=1
        while block_index < len(chain):
            block = chain[block_index]
            if block.previous_hash != self.hash(previous_block):
                return False
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if self.check_puzzle(hash_operation) is False:
                return False
            previous_block = block
            block_index +=1
        return True

    def getLocalBLockchainFile(self, node = None):
        if node is None:
            node = self.node
        fileName = str('blockchain_'+node+'.json')
        if os.path.exists(fileName) is False:
            block = Block()
            self.chain.append(block)
            self.register()
        try:
            chain = None
            with open(fileName) as blockchainFile:
                if os.path.getsize(fileName) > 0:
                    data = json.load(blockchainFile)
                    chain = self.fromJson(data['chain'])
            return chain
        except:
            print('not found local blockchain file: blockchain_'+self.node+'.json')
    
    
    def replaceChain(self):
        with open('nodes.json') as nodeFile:
            data = json.load(nodeFile)
            nodes = data['nodes']
            longest_chain = None
            max_length = len(self.chain)
            for node in nodes:
                print('checking node: ',node)
                chain = self.getLocalBLockchainFile()
                if(chain is None):
                    return None;
                length = len(chain)
                if length>max_length and self.isChainValid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain:
                chain = longest_chain
                return True
            return False