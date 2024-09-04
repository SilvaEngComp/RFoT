import os
from keras.models import model_from_json
from collections import namedtuple
from src.suport_layer.transaction import Transaction
from src.suport_layer.block import Block
import statistics as st
import numpy as np
import pandas as pd
import csv
import math
from simple_MLP import SimpleMLP,SimpleMLP2
from tensorflow.keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import json
import tensorflow as tf
import random

class FdModel:
    def __init__(self, name, dataBlock=None):
        self.name = name
        if dataBlock is None:
            self.dataBlock= []
            transaction = Transaction("c05", "temperatureSensor", "h28", {"temperature":26,"humidity":10})
            transactions = []
            for i in range(20):
                transactions.append(transaction)

            self.dataBlock= Block(transactions)

        else:
            self.dataBlock= dataBlock
        self.fileName = 'dataset.csv'
        self._loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
        self._learningRate = 0.1
        self._metrics = ['accuracy']
        self._epochs = 1
        self._commsRound = 100
        self._momentum = 0.9
        self._optimizer = SGD(self._learningRate,
                              decay=self._learningRate / self._commsRound,
                              momentum=self._momentum
                              )
        self._model = None
        self._cardinality = np.array([])
        self.trashoulder=0.2

    def getAsDict(self):
        return {self.name: self.dataBlock}

    def __str__(self):
        return str({
            "name": self.name,
            "model": self._model.to_json() if (self._model is not None) else '',
            "cardinality": str(self.getCardinality())if (self._model is not None) else '',
        })

    def __repr__(self):
        return str({
            "name": self.name,
            "model": self._model.to_json() if (self._model is not None) else '',
            "cardinality": str(self.getCardinality())if (self._model is not None) else '',
        })

    def toJson(self):
        return {
            "model": self._model.to_json(),
            "cardinality": str(self.getCardinality()),
        }

    def preprocessing(self, trashoulder=0.2):
        self.trashoulder = trashoulder
        dataset = self.getStatistics()
        self.saveDataset(dataset)
        self._model = self.training(dataset)

    def getStatistics(self):
        decryptedTransactions = []
        for block in self.dataBlock:
            decryptedTransactions.append(Transaction.fromJsonDecrypt(block))
        return self.targetDefinition(decryptedTransactions)
        
    
    def fixingData(self,data):
        part1 = data.split('.')
        print(part1)
        if(len(part1[0])>2):
            integerPart = part1[0][:2]
            floatPart =  part1[0][2:]
            realNumber = float(str(integerPart+'.'+floatPart))
        else:
            realNumber = float(data)
        return realNumber

    def arrayToDataFrame(self, transactions):
        filtradTransactions = []
        for transaction in transactions:
            print(isinstance(transaction,dict))
            print(transaction["data"])
            temperature = self.fixingData(transaction["data"]["temperature"])
            humidity = self.fixingData(transaction["data"]["humidity"])
            filtradTransactions.append([temperature,humidity])
        
        cols=["temperature","humidity"]
        dataset = pd.DataFrame(filtradTransactions, columns=cols)
        return dataset
    def  removingOutliers(self, transactions):
        dataset = self.arrayToDataFrame(transactions)
        dataset["temperature"].astype(np.float64)
        dataset["humidity"].astype(np.float64)
        #calcular 1° quartil
        Q1 = np.nanpercentile(dataset["temperature"],25,interpolation="midpoint")
        #calcular 3° quartil
        Q3 = np.nanpercentile(dataset["temperature"],75,interpolation="midpoint")
        #intervalo do quartil
        IQR = Q3-Q1
        df = dataset[dataset["temperature"] <= Q3 + IQR*12]
        df = df[df["temperature"] >= Q3 - IQR*12]

        return df
    def targetDefinition(self, transactions):
        df = self.removingOutliers(transactions)
        
        idt = self.getIDT(df)
        target=[]
        for value in idt:
            if  value<= 26:
                target.append(1)
            else:
                target.append(0)
        df["IDT"]=idt
        df["target"]=target
        
        return df

    def getIDT(self, df):
        return df.temperature.values - (0.55-0.0055*df.humidity.values)*(df.temperature.values-14.5)

    def getTEv(self, df):
        v=10
        return 37-((37-df.temperature.values)/0.68-(0.0014*df.humidity.values) + (1/(1.76*v**(0.75)))) - (0.29*df.temperature.values*(1 - df.humidity.values/100))

    def saveDataset(self, dataset):
        exists = os.path.exists(self.fileName)

        with open(self.fileName, 'a') as datasetFile:
            writer = csv.writer(datasetFile)
            if exists is False:
                writer.writerow(dataset.columns)
            for i in np.arange(int(dataset.shape[0])):
                writer.writerow(dataset.iloc[i,])

    def batch_data(self, dataset, bs=32):
        target = dataset.target
        dataset = dataset.drop(columns=['target'])
        dataset2 = tf.data.Dataset.from_tensor_slices((dataset.values, target))
        return dataset2.shuffle(len(target)).batch(bs)

    def training(self, dataset):
        self.generateCardinality(dataset)
        target = dataset.target
        # dataset = dataset.drop(columns=['IDT'])
        dataset = dataset.drop(columns=['target'])
        
        local_model = None
        try:
            if (dataset.shape[0] > 1):
                X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=0.5, random_state=42,
                                                                    stratify=None, shuffle=False)
                smlp_local = SimpleMLP2()

                local_model = smlp_local.build(X_train.shape[1])
                # local_model.compile(loss=self.getLoss(), optimizer=self.getOptimizer(),
                #                     metrics=self.getMetrics())
                local_model.fit(X_train, y_train)
            return local_model
        except Exception as e:
            print("Treinamento deu erro")
            print(str(e))

    def hasValidModel(self):
        if self._model is None:
            return False
        return True

    def getLoss(self):
        return self._loss

    def getOptimizer(self):
        return self._optimizer

    def getMetrics(self):
        return self._metrics

    def getEpochs(self):
        return self._epochs

    def getLearningRate(self):
        return self._learningRate

    def setLoss(self, loss):
        self._loss = loss

    def setOptimizer(self, optimizer):
        self._optimizer = optimizer

    def setMetrics(self, metrics):
        self._metrics = metrics

    def setEpochs(self, epochs):
        self._epochs = epochs

    def setLearningRate(self, learningRate):
        self._learningRate = learningRate

    def setModel(self, model):
        if isinstance(model, str):
            print('model_from_json')
            self._model = model_from_json(model)
        else:
            print('model_from_dict')
            self._model = model_from_json(model['model'])
            self._cardinality = model['cardinality']

    def getModel(self):
        return self._model

    def getModelWeights(self):
        return np.array(self._model.get_weights())

    def setCardinality(self, cardinality):
        self._cardinality = int(cardinality)

    def generateCardinality(self, dataset):
        self._cardinality = tf.data.experimental.cardinality(
            self.batch_data(dataset)).numpy()

    def getCardinality(self):
        return self._cardinality
