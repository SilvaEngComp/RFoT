
import datetime
import json
from transaction import Transaction

class Block:
    def __init__(self, transactions=[],  hostTrainer=None,typeBlock="data", index=1, proof=1, previousHash='0', timestamp = str(datetime.datetime.now())):
        self.transactions = transactions
        self.index = index
        self.proof = proof
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.hostTrainer = hostTrainer
        self.typeBlock = typeBlock
    
        
    def __getitem__(self, i):
        if i == 'transactions':
            return self.transactions
    
    def __str__(self):
        return str({
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash,
            'hostTrainer': self.hostTrainer,
            'transactions': self.transactions
            })
    def __repr__(self):
        return str({
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash ,
            'hostTrainer': self.hostTrainer,
            'transactions': self.transactions
            })
    
    def toJson(self):
        transactions = []
        for transaction in self.transactions:
            if isinstance(transaction, Transaction):
                transactions.append(transaction.toJson())
            else:
                transactions.append(transaction)
        
        # print('transactions: ',transactions)
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash, 
            'hostTrainer': self.hostTrainer,
            'transactions': transactions
            }
    @classmethod
    def fromJson(self, jsonBlock):
        if isinstance(jsonBlock, dict):
            pool = []
            for transaction in jsonBlock['transactions']:
                pool.append(Transaction.fromJson(transaction))
            block = Block(pool,jsonBlock['hostTrainer'],jsonBlock['typeBlock'], jsonBlock['index'],jsonBlock['proof'],
                          jsonBlock['previousHash'], jsonBlock['timestamp'] )
            return block
            
        return jsonBlock