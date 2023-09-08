
import datetime
import json
from transaction import Transaction
from hostTrainer import HostTrainer
class Block:
    def __init__(self, transactions=None,typeBlock="data_blockchain", index=None, proof=None, previousHash=None, timestamp = None, hostTrainer=None):
        self.transactions = [] if(transactions is None) else transactions
        self.index = 1 if(index is None) else index
        self.proof =  1 if(proof is None) else proof
        self.previousHash = '0' if(previousHash is None) else previousHash
        self.timestamp = self.configTimestamp(timestamp)
        self.hostTrainer = hostTrainer
        self.typeBlock = "data_blockchain" if(typeBlock is None) else typeBlock
        
    def configTimestamp(self, timestamp):
        if timestamp is None:
            now = datetime.datetime.now()
            dateFormat = "%Y-%m-%d %H:%M:%S"
            return now.strftime(dateFormat)
        return timestamp
        
        
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
        if isinstance(self.transactions, list):
            transactions = []
            for transaction in self.transactions:
                if isinstance(transaction, Transaction):
                    transactions.append(transaction.toJson())
                else:
                    transactions.append(transaction)
        else:
            transactions = [Transaction(self.hostTrainer.hostTrainer,None, None,self.transactions).toJson()]
        
        if(self.typeBlock=='data_blockchain' or self.hostTrainer is None):
            jsonData = {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash, 
            'transactions': transactions
            }
        else:
            hostTrainer = self.hostTrainer.toJson()
            jsonData = {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash, 
            'hostTrainer': hostTrainer,
            'transactions': transactions
            }
        
        return jsonData
        
    @classmethod
    def fromJson(self,jsonBlock):
        if isinstance(jsonBlock, dict):
            pool = []
            for transaction in jsonBlock['transactions']:
                pool.append(Transaction.fromJson(transaction))

            if(jsonBlock['typeBlock']=='data_blockchain'):
                block = Block(pool,jsonBlock['typeBlock'], jsonBlock['index'],jsonBlock['proof'],
                          jsonBlock['previousHash'], jsonBlock['timestamp'] )
            else:    
                hostTrainer = HostTrainer.fromJson(jsonBlock['hostTrainer']) 
                block = Block(pool,jsonBlock['typeBlock'], jsonBlock['index'],jsonBlock['proof'],
                          jsonBlock['previousHash'], jsonBlock['timestamp'],hostTrainer )
            return block
        
        return jsonBlock