
import datetime
import json
from transaction import Transaction

class Block:
    def __init__(self, transactions=[], index=1, proof=1, previousHash='0', timestamp = str(datetime.datetime.now())):
        self.transactions = transactions
        self.index = index
        self.proof = proof
        self.previousHash = previousHash
        self.timestamp = timestamp
        
        
    
    def __str__(self):
        return str({
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'previousHash': self.previousHash,
            'transactions': self.transactions
            })
    def __repr__(self):
        return str({
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'previousHash': self.previousHash ,
            'transactions': self.transactions
            })
    
    def toJson(self):
        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.toJson())
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'previousHash': self.previousHash, 
            'transactions': transactions
            }
    @classmethod
    def fromJson(self, block):
        if isinstance(block, dict):
            pool = []
            for transaction in block['transactions']:
                pool.append(Transaction.fromJson(transaction))
            return Block(pool, block['index'],block['proof'],block['previousHash'], block['timestamp'])
            
        return block