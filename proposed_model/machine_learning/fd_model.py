import statistics as st
import numpy as np
import pandas as pd
import csv
import math
from simple_MLP import SimpleMLP
from tensorflow.keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import json
import tensorflow as tf
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/proposed_model/data_collector')
from block import Block
from transaction import Transaction
from collections import namedtuple
from keras.models import model_from_json
import os
class FdModel:
    def __init__(self, name, data=None):
        self.name = name
        if data is None:
            self.data = []
            transaction = Transaction("c05", "temperatureSensor","h28", "26")
            transactions = []
            for i in range(50):
                transactions.append(transaction)
            
            self.data = Block(transactions)                
            
        else:
            self.data = data
        self.fileName = 'dataset.csv'
        self._loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)        
        self._learningRate = 0.01 
        self._metrics = ['accuracy']
        self._epochs = 1
        self._commsRound = 100
        self._momentum = 100
        self._optimizer = SGD(self._learningRate, 
                decay= self._learningRate / self._commsRound, 
                momentum=0.9
               ) 
        self._model = None
        self._cardinality = np.array([]);
    
    def getAsDict(self):
        return {self.name: self.data}
    
    def __str__(self):
        return str(self.name)
    
    def toJson(self):
        return {
            "model":self._model.to_json(),
            "cardinality": str(self.getCardinality()),
        }
    
    def preprocessing(self, trashoulder=0.2):
        datasetRows = self.getStatistics(trashoulder)
        
        if(datasetRows is None):
            return None
        dataset = self.generateDataset(datasetRows)
        self.saveDataset(dataset)
        self._model =self.train(dataset)
    
    def getStatistics(self,trashoulder=0.2):
        datasetRows = []
        try:
            transactionValues = self.dataPartition(self.data.transactions)
            datasetRows = self.getDatasetRows(transactionValues)
            return np.array(datasetRows)
        except:
            print('The transmited data across is not a Block')
            return None
        
    def filter_by_sensor(self,transactions,sensor='temperatureSensor'):
        filtredTransactions = []
        for transaction in transactions:
            if(transaction['sensor'] == sensor):
                filtredTransactions.append(transaction)
        return filtredTransactions
    
    def dataPartition(self,transactions):
      
        transactionValues2 = []
        filtredTransactions = self.filter_by_sensor(transactions)
        for p in range(0,len(filtredTransactions),5):
            j = p+5
            transactionValues1= [float(temp['data']) for temp in filtredTransactions[p:j]]
            transactionValues2.append(transactionValues1)

        return transactionValues2
            
    def setClass(self,standardVariationValue,meanValue,temperatures):
       cont=0
       for temp in temperatures:
           variationEvaluated = abs(meanValue-temp)
           if(variationEvaluated > standardVariationValue):
               cont+=1
       return 1 if(cont > 0) else 0
    
    def getDatasetRows(self,transactionValues):
        i = 0;
        datasetRows = []
        for t in transactionValues:
            meanValue = st.mean(t)
            standardVariationValue = np.std(t)
            validatedClass = self.setClass(standardVariationValue,meanValue,t)
            varianceValue = math.sqrt(np.std(t))
            datasetRows.append(t + [meanValue,varianceValue,standardVariationValue,validatedClass])
            i+=1
        
        return np.array(datasetRows)
    
    def generateDataset(self,datasetRows):
        cols = ['{}_{}'.format('data', i+1) for i in range((datasetRows.shape[1]-4))]
        cols += ['mean','variance','standardVariation','label']
        dataset = pd.DataFrame(datasetRows, columns = cols)
        return dataset
    
    def saveDataset(self,dataset):
        exists = os.path.exists(self.fileName)

        with open(self.fileName,'a') as datasetFile:
            writer = csv.writer(datasetFile)
            if exists is False:
                writer.writerow(dataset.columns)
            for i in np.arange(int(dataset.shape[0])):
                writer.writerow(dataset.iloc[i,])
    
    
    
   
    
    def batch_data(self,dataset, bs=32):
        label = dataset.label
        dataset = dataset.drop(columns=['label'])
        dataset2 = tf.data.Dataset.from_tensor_slices((dataset.values, label))
        return dataset2.shuffle(len(label)).batch(bs)

    def train(self, dataset):
        self.generateCardinality(dataset)
        label = dataset.label
        dataset = dataset.drop(columns=['label'])
        local_model = None
        if(dataset.shape[0]>1):
            X_train,X_test,y_train,y_test = train_test_split(dataset, label, test_size=0.5, random_state=42, 
                                                    stratify=None, shuffle=False)
            smlp_local = SimpleMLP()
            
            local_model = smlp_local.build(X_train.shape[1])
            
            local_model.compile(loss=self.getLoss(), optimizer=self.getOptimizer(),
                                metrics=self.getMetrics())
            local_model.fit(X_train,y_train, epochs=self.getEpochs(), verbose=0)
        return local_model
    
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
            self._model = model_from_json(model)
        else:
            self._model = model
    def getModel(self):
        return self._model
    def getModelWeights(self):
        return np.array(self._model.get_weights())
    def setCardinality(self, cardinality):
        self._cardinality = int(cardinality)
    def generateCardinality(self, dataset):
        self._cardinality = tf.data.experimental.cardinality(self.batch_data(dataset)).numpy()
    def getCardinality(self):
        return self._cardinality
