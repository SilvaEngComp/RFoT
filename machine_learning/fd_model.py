import statistics as st
import numpy as np
import pandas as pd
import csv
import math
from simple_MLP import SimpleMLP
from tensorflow.keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import json
class FdModel:
    def __init__(self, name, data=None):
        self.name = name
        if data is None:
            print('setting default data...')
            
            self.data = [
                {'transactions': [
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"}
                ]},
                {'transactions': [
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"},
                {"sender": "sc05", "sensor": "temperatureSensor", "data": "26"}
                ]},
                ]
            
        else:
            self.data = data
        self.fileName = 'dataset_'+name+'.csv'
        self._loss = 'categorical_crossentropy'        
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
    
    def getAsDict(self):
        return {self.name: self.data}
    
    def __str__(self):
        return str(self.name)
    
    def toJson(self):
        return self.model.to_json()
    
    def preprocessing(self, trashoulder=0.2):
        datasetRows = self.getStatistics(trashoulder)
        dataset = self.generateDataset(datasetRows)
        #self.saveDataset(dataset)
        self._model =self.train(dataset)
    
    
    def getStatistics(self,trashoulder=0.2):
        datasetRows = []
        
        for currencyBlock in self.data:	
            dataMean, transactionValues = self.getMean(currencyBlock['transactions'])
            
            variance = math.sqrt(st.pvariance(transactionValues))
            standardVariation = np.std(transactionValues)
            validatedClass = 1 if(standardVariation > trashoulder) else 0
            values = transactionValues + [dataMean,variance,standardVariation,validatedClass]
            datasetRows.append(values)
        
        return np.array(datasetRows)
    
    def generateDataset(self,datasetRows):
        
        cols = ['{}_{}'.format('data', i+1) for i in range(datasetRows.shape[1]-4)]
        cols += ['mean','variance','standardVariation','classe']
        dataset = pd.DataFrame(datasetRows, columns = cols)
        return dataset
    
    def saveDataset(self,dataset):
        with open(self.fileName,'w') as datasetFile:
            writer = csv.writer(datasetFile)
            for i in np.arange(int(dataset.shape[0])):
                writer.writerow(dataset.iloc[i,])
    
    def getMean(self,transactions):
        transactionValues = []
        for transaction in self.filter_by_sensor(transactions):
            transactionValues.append(float(transaction['data']))
        return [round(st.mean(transactionValues), 2), transactionValues]
    
    def filter_by_sensor(self,transactions,sensor='temperatureSensor'):
        filtredTransactions = []
        for transaction in transactions:
            if(transaction['sensor'] == sensor):
                filtredTransactions.append(transaction)
        return filtredTransactions
    
    def train(self, dataset):
        classe = dataset.classe
        dataset = dataset.drop(columns=['classe'])
        
        X_train,X_test,y_train,y_test = train_test_split(dataset, classe, test_size=0.1, random_state=42, 
                                                 stratify=classe, shuffle=True)
        smlp_local = SimpleMLP()
        local_model = smlp_local.build(X_train.shape[1], 10)

        local_model.compile(loss=self.getLoss(), optimizer=self.getOptimizer(),
                            metrics=self.getMetrics())
        local_model.fit(X_train,y_train, epochs=self.getEpochs(), verbose=0)
        return local_model
    

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
        self._model = json.loads(model)
    def getModel(self):
        return self._model.to_json()
