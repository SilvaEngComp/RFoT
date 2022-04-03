import statistics as st
import numpy as np
import pandas as pd
import csv
import math
class FdModel:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.fileName = 'dataset_'+name+'.csv'
    
    def getAsDict(self):
        return {self.name: self.data}
    
    
    def preprocessing(self, trashoulder=0.2):
        datasetRows = self.getStatistics(trashoulder)
        dataset = self.generateDataset(datasetRows)
        self.saveDataset(dataset)
    
    
    def getStatistics(self,trashoulder=0.2):
        datasetRows = []
        for currencyBlock in self.data:	
            dataMean, transactionValues = self.getMean(currencyBlock.transactions)
            print('transactionValues: ' , transactionValues)
            variance = math.sqrt(st.pvariance(transactionValues))
            standardVariation = np.std(transactionValues)
            print('variance: ',variance)
            if(standardVariation > trashoulder):
                datasetRows.append([dataMean,variance,standardVariation,1])
            else:
                datasetRows.append([dataMean,variance,standardVariation,0])
        
        return datasetRows
    
    def generateDataset(self,datasetRows):
        cols = ['mean','variance','standardVariation','class']
        dataset = pd.DataFrame(datasetRows, columns = cols)
        return dataset
    
    def saveDataset(self,dataset):
        with open(self.fileName,'w') as datasetFile:
            writer = csv.writer(datasetFile)
            for i in np.arange(int(dataset.shape[0])):
                writer.writerow(dataset.iloc[i,])
    
    def getMean(self,transactions):
        transactionValues = []
        for j in self.filter_by_sensor(transactions):
            transactionValues.append(float(j.data))
        return [round(st.mean(transactionValues), 2), transactionValues]
    
    def filter_by_sensor(self,transactions,sensor='temperatureSensor'):
        filtredTransactions = []
        for j in transactions:
            if(j.sensor == sensor):
                filtredTransactions.append(j)
        return filtredTransactions