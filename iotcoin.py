# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva
"""


from blockchain import Blockchain
from uuid import uuid4
import requests
import json
node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()

def mineBlock(transaction, node):
    print('0')
    blockchain.addNode(node)
    print('1')
    previous_block = blockchain.getPreviousBlock()
    print('2')
    previous_proof = previous_block.proof
    print('3')
    proof = blockchain.proofOfWork(previous_proof)
    print('4')
    previousHash = blockchain.hash(previous_block)
    blockchain.addTransaction(transaction)
    if len(blockchain.transactions)>=2:
        block = blockchain.createBlock(proof,previousHash)
        return getChain()
    print( len(blockchain.transactions),' - ',str(blockchain.transactions))
    return None


def getChain():
    getBlockchainFile()
    response = {'chain':str(blockchain.chain),
                'length': len(blockchain.chain)}
    
    
    return response
    
    
def getBlockchainFile():
	blockchain = Blockchain()
	with open('blockchain.json', 'a+') as blockchainFile:
		print(blockchainFile.readline() == '')
		if blockchainFile.readline() != '':
			data = json.load(blockchainFile)
			data = json.loads(data)
			blockchain.chain = data.chain + blockchain.chain 
                

                
                
                 
def register():
	blockchain.register()

def isValid():
    response = {'isValid':blockchain.is_chain_valid(blockchain.chain)}
    
    return json.dumps(response), 200
    

def connectNode():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No nodes', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message':'Todos os nós conectados. O blockchain contem os seguintes nós',
                'total_nodes':list(blockchain.nodes)}
    
    return json.dumps(response), 201     
        
def replaceChain():
    if blockchain.replaceChain():
        message = 'Cadeia substituida, pois tinham cadeias diferentes'
    else:
        message = 'Não houve substituição'
    
    response = {'message':message,
                    'new_chain':blockchain.chain}
        
    return json.dumps(response), 201
        
        
        
