import os
from transaction import Transaction
import json

class Pool:
    def __init__(self):
        self.pool = []
        self.fileName = 'pool.json'
    
    @staticmethod
    def getNotAssinedTransactions():
        pool = Pool()
        transactions = pool.get()
        
        if(len(transactions)>0):
            notAssigned = transactions[0]
            pool.setPool(transactions[1:])
            return notAssigned;
             
        return None
       
    def toJson(self):
        jsonPool = []
        for transactions in self.pool:
            jsonTransactions = []
            for transaction in transactions:
                if isinstance(transaction, Transaction):
                    jsonTransactions.append(transaction.toJson())
                else:
                    jsonTransactions.append(transaction)
            jsonPool.append(jsonTransactions)
        return jsonPool
        
    def fromJson(self, data):
        try:
            if isinstance(data, list):
                transactions = []
                for jsonTransaction in data:
                    transactions.append(Transaction.fromJson(jsonTransaction))  
                return transactions
        except:
            print('That is not a list object. Try it again!')
    
    def setPool(self,transactions):
        self.pool = transactions
        self.register()
        
    def add(self,transactions):
        self.pool = self.get()
        self.pool.append(transactions)
        self.register()
    
    
    def register(self):
        with open(self.fileName,"w") as file:
            try:
                print('registring new transaction pool ')
                json.dump(self.toJson(), file)
            except:
                print('erro in registration')
            
    def getPoolStatus(self):
        pool = self.get()
        print("Existem {} blocos de {} transações não assinadas".format(len(pool), len(pool[0])))
    
    
    def get(self, prefix='../data_collector/'):
        fileName = str(prefix + self.fileName) 
        if os.path.exists(fileName) is False:
            return []
        try:
            with open(fileName) as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    return self.fromJson(data)
                else:
                    return []
        except:
            print('not found local pool file: ')
            return []
        
    