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

def mine_block(transaction):
	previous_block = blockchain.get_previous_block()    

	previous_proof = previous_block.proof

	proof = blockchain.proof_of_work(previous_proof)

	previous_hash = blockchain.hash(previous_block)
	blockchain.add_transaction(transaction)
	if len(blockchain.transactions)>=10:
		block = blockchain.create_block(proof,previous_hash)
		return get_chain()
	print( len(blockchain.transactions),' - ',str(blockchain.transactions))
	return None


def get_chain():
    response = {'chain':str(blockchain.chain),
                'length': len(blockchain.chain)}
    
    return response


def is_valid():
    response = {'is_valid':blockchain.is_chain_valid(blockchain.chain)}
    
    return json.dumps(response), 200
    

def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No nodes', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message':'Todos os nós conectados. O blockchain contem os seguintes nós',
                'total_nodes':list(blockchain.nodes)}
    
    return json.dumps(response), 201     
        
def replace_chain():
    if blockchain.replace_chain():
        message = 'Cadeia substituida, pois tinham cadeias diferentes'
    else:
        message = 'Não houve substituição'
    
    response = {'message':message,
                    'new_chain':blockchain.chain}
        
    return json.dumps(response), 201
        
        
        
