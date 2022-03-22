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
        pint('isinstance: ', isinstance(bloc, Block))
        if isinstance(bloc, Block):
            block = str(block)
        encoded_block = json.dumps(block,sort_keys=True).encode()
        print('encoded_block: ', encoded_block)
        return hashlib.sha256(encoded_block).hexdigest()

    def isChainValid(self, chain):
        print('validing chain...')
        previous_block = chain[0]
        block_index=1
        while block_index < len(chain):
            block = chain[block_index]
            print('pass...')
            if block.previous_hash != self.hash(previous_block):
                print('pass...1')
                return False
            print('pass...1')
            previous_proof = previous_block['proof']
            proof = block['roof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if self.check_puzzle(hash_operation) is False:
                return False
            previous_block = block
            block_index += 1
        return True

    def getLocalBLockchainFile(self, node = None, training=False):
        if node is None:
            node = self.node
        fileName = str('../blockchain_'+node+'.json') if training else  str('blockchain_'+node+'.json') 
        print(fileName)
        
        if os.path.exists(fileName) is False:
            block = Block()
            self.chain.append(block)
            self.register()
        try:
            chain = None
            with open(fileName) as blockchainFile:
                if os.path.getsize(fileName) > 0:
                    chain = json.load(blockchainFile)['chain']
            return chain
        except:
            print('not found local blockchain file: blockchain_'+self.node+'.json')
            return None
    
    
    def replaceChain(self, fileName='nodes.json', training=False):
        try:
            with open(fileName) as nodeFile:
                data = json.load(nodeFile)
                nodes = data['nodes']
                longest_chain = None
                
                max_length = len(self.chain)
                for node in nodes:
                    print('checking node: ',node)
                    chain = self.getLocalBLockchainFile(node,training)
                    if(chain is None):
                        return None;
                    length = len(chain)
                    isValide = self.isChainValid(chain)
                    print(isValide)
                    if length>max_length and self.isChainValid(chain):
                        max_length = length
                        longest_chain = chain
                    
                return longest_chain
        except:
            print('No file ',fileName,' found')