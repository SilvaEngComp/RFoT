
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""

import datetime
import hashlib
import json

from urllib.parse import urlparse
import requests


class Transaction:
	def __init__(self, sender, sensor,receiver, data):
		self.sender = sender
		self.sensor = sensor
		self.receiver = receiver
		self.data = data

		
	def __str__(self):
		return str({
		'sender': self.sender,
        'sensor': self.sensor,
		'receiver':self.receiver,
		'data': self.data ,
		})
		
	def __repr__(self):
		return str({
		'sender': self.sender,
        'sensor': self.sensor,
		'receiver':self.receiver,
		'data': self.data ,
		})

class Block:
	def __init__(self, index, proof, previus_hash, transactions):
		self.index = index
		self.timestamp = str(datetime.datetime.now())
		self.proof = proof
		self.previous_hash = previus_hash
		self.transactions = transactions
		
	def __str__(self):
		return str({
		'index': self.index,
        'timestamp': self.timestamp,
		'proof':self.proof,
		'previus_hash': self.previous_hash ,
		'transactions': self.transactions
		})
		
	def __repr__(self):
		return str({
		'index': self.index,
        'timestamp': self.timestamp,
		'proof':self.proof,
		'previus_hash': self.previous_hash ,
		'transactions': self.transactions
		})

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previus_hash='0')
        self.nodes = set()
        self.pool = []
        
    def __str__(self):
        return str({
		'chain': self.chain,
        'transactions': self.transactions,
		'nodes':self.nodes,
		'previus_hash': self.previous_hash ,
		'pool': self.pool
		})
		
    def __repr__(self):
        return str({
		'chain': self.chain,
        'transactions': self.transactions,
		'nodes':self.nodes,
		'previus_hash': self.previous_hash ,
		'pool': self.pool
		})
        
    def create_block(self, proof, previus_hash):
        block = Block(len(self.chain)+1,proof,previus_hash,self.transactions)
        self.transactions = []
        self.chain.append(block)
        return block 
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        previous_block = self.get_previous_block()
        return previous_block.index + 1
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def check_puzzle(self, hash_test):
        if hash_test[0:4]=='0000':
            return True
        return False
    
    def proof_of_work(self, previous_proof):
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
    
    def is_chain_valid(self, chain):
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
    
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response  = requests.get(f'http://{node}/get_chain')
            if response.status_code==200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length>max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        
        if longest_chain:
            self.chain = longest_chain
            return True
        return False




