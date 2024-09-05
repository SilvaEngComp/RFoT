import os
from src.suport_layer.transaction import Transaction
import json
import random
import sys
from src.suport_layer.cipher import Cipher

class Pool:
    def __init__(self):
        self.chain = []
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
        cipher = Cipher()
        allTransactions = pool.getDecrypted()
        if (len(allTransactions) > 0):
            allCorrupted_transactions = []
            cont = 0
            for transactions in allTransactions:
                corrupted = []
                for item in transactions:
                    if item is not None:
                        temperature = str(random.randint(1, 1000))
                        humidity = str(random.randint(1, 1000))
                        
                        sensorNode = {"temperature":temperature,"humidity":humidity}
                        # print(sensorNode)
                        dataBytes = json.dumps(sensorNode).encode("utf-8")
                        # print(dataBytes)
                        encrypted= cipher.encrypt(dataBytes)
                        # print(encrypted)
                        newItem = Transaction(item["sender"],item["sensor"], item["receiver"],encrypted.decode())
                        print(newItem)
                        corrupted.append(newItem)
                allCorrupted_transactions.append(corrupted)
            pool.chain = allCorrupted_transactions
            pool.register()

    def toJson(self):
        jsonPool = []
        for transactions in self.chain:
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
        except Exception as e:
            print(e)
            print('That is not a list object. Try it again!')

    def fromJsonDecripted(self, data):
        try:
            if isinstance(data, list):
                transactions = []
                for jsonTransaction in data:
                    if isinstance(jsonTransaction, list):
                        transactionBlock = []
                        for transaction in jsonTransaction:
                            transactionBlock.append(Transaction.fromJsonDecrypt(transaction))
                        transactions.append(transactionBlock)
                    else:
                        transactions.append(Transaction.fromJsonDecrypt(jsonTransaction))
                return transactions
        except Exception as e:
            print(f'fromJsonDecripted {e}')


    def add(self, transactions):
        self.chain = self.get()
        self.chain.append(transactions)
        self.register()

    def register(self, prefix='../current_model/'):
        fileName = str(prefix + self.fileName)
        with open(fileName, "w") as file:
            try:
                print('registring new transaction pool | nº: {} '.format(
                    len(self.chain)))
                json.dump(self.toJson(), file)
            except Exception as e:
                print(e)
                print('erro in registration')
                
    def registerSelectedPosition(self,selectedPosition, prefix='../current_model/'):
        fileName = str(prefix + self.selectedPositionsFileName)
        with open(fileName, "w") as file:
            try:
                print('registring new selected position | nº: {} '.format(
                    len(selectedPosition)))
                json.dump(selectedPosition, file)
            except Exception as e:
                print(e)
                print('erro in registration')

    def getPoolStatus(self):
        pool = self.get()
        print("Existem {} blocos de {} transações não assinadas".format(
            len(pool), len(pool[0])))

    def get(self, translate=False,prefix='../current_model/'):
        fileName = str(prefix + self.fileName)
        pasta = os.listdir(prefix)
        if os.path.exists(fileName) is False:
            print(f'107 - not found local pool file: {fileName} ')
            return []
        try:
            with open(fileName) as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    return self.fromJson(data)
                else:
                    return []
        except Exception as e:
            print(e)
            print(f'118 - not found local pool file: {fileName} ')
            return []

    def getDecrypted(self, prefix='../current_model/'):
        fileName = str(prefix + self.fileName)
        if os.path.exists(fileName) is False:
            print(f'107 - not found local pool file: {fileName} ')
            return []
        try:
            with open(fileName) as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    return self.fromJsonDecripted(data)
                else:
                    return []
        except Exception as e:
            print(f'getDecrypted: {e}')
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
        except Exception as e:
            print(e)
            print(f'not found local pool file: {fileName} ')
            return []
