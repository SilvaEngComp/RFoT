import os
from src.suport_layer.transaction import Transaction
import json
import random
import sys


class Pool:
    def __init__(self):
        self.pool = []
        self.fileName = 'noBlockchain.json'
        self.selectedPositionsFileName = 'selectedPositions.json'

    @staticmethod
    def getNotAssinedTransactions():
        pool = Pool()
        transactions = pool.get()
        selctedPosition = pool.getSelectedPositions()
        transactionsSize = len(transactions)-1
        if (transactionsSize > 0 and len(selctedPosition)<transactionsSize):
            while True:
                randomProsition = random.randint(0, transactionsSize)
                if(randomProsition not in selctedPosition):
                    notAssigned = transactions[randomProsition]
                    selctedPosition.append(randomProsition)
                    pool.registerSelectedPosition(selctedPosition)
                    return notAssigned;
        else:
            print(f'Limite de dados atingidos: {transactionsSize} pacotes coletados')

        return None

    @staticmethod
    def setCorruptTransactions():
        pool = Pool()
        allTransactions = pool.get()

        if (len(allTransactions) > 0):
            allCorrupted_transactions = []
            cont = 0
            for transactions in allTransactions:
                corrupted = []
                for transaction in transactions:
                    transaction['data'] = random.randint(1, 1000)
                    corrupted.append(transaction)
                allCorrupted_transactions.append(corrupted)
            pool.setPool(allCorrupted_transactions)

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


    def add(self, transactions):
        self.pool = self.get()
        self.pool.append(transactions)
        self.register()

    def register(self, prefix=''):
        fileName = str(prefix + self.fileName)
        with open(self.fileName, "w") as file:
            try:
                print('registring new transaction pool | nº: {} '.format(
                    len(self.pool)))
                json.dump(self.toJson(), file)
            except:
                print('erro in registration')
                
    def registerSelectedPosition(self,selectedPosition, prefix='../current_model/'):
        fileName = str(prefix + self.selectedPositionsFileName)
        with open(fileName, "w") as file:
            try:
                print('registring new selected position | nº: {} '.format(
                    len(selectedPosition)))
                json.dump(selectedPosition, file)
            except:
                print('erro in registration')

    def getPoolStatus(self):
        pool = self.get()
        print("Existem {} blocos de {} transações não assinadas".format(
            len(pool), len(pool[0])))

    def get(self, prefix='../current_model/'):
        fileName = str(prefix + self.fileName)
        
        if os.path.exists(fileName) is False:
            print(f'not found local pool file: {fileName} ')
            return []
        try:
            with open(fileName) as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    return self.fromJson(data)
                else:
                    return []
        except:
            print(f'not found local pool file: {fileName} ')
            return []
        
    def getSelectedPositions(self, prefix='../current_model/'):
        fileName = str(prefix + self.selectedPositionsFileName)
        
        if os.path.exists(fileName) is False:
            print(f'not found local pool file: {fileName} ')
            return []
        try:
            with open(fileName) as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    return data
                else:
                    return []
        except:
            print(f'not found local pool file: {fileName} ')
            return []
