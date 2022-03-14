
import datetime
import json




class Block:
	def __init__(self, index=1, proof=1, previousHash='0', transactions=[], timestamp = str(datetime.datetime.now())):
		self.index = index
		self.timestamp = timestamp
		self.proof = proof
		self.previousHash = previousHash
		self.transactions = transactions
		
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
		'previousHash': self.previousHash ,
		'transactions': transactions
		}
