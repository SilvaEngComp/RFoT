# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 23:47:45 2021

@author: silva
"""
import os
import csv

import pandas as pd
import numpy as np
from timeit import default_timer as timer

from sklearn.preprocessing import StandardScaler
from skmultiflow.drift_detection import PageHinkley

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def saveFile(dataset, name='dataset'):
    print('saving: ',name, '......')
    f = open(name,'w')
    try:
        writer = csv.writer(f)
        writer.writerow(dataset.columns)
        for i in np.arange(int(dataset.shape[0])):
            writer.writerow(dataset.iloc[i,])
    finally:
        f.close()
 
def create_window(X, time_steps=5):
    Xs = []
    for i in range(len(X) - time_steps):
        print("\033[H\033[J") 
        print('creating concept window ',round((i/(len(X) - time_steps))*100,2), ('%'))
        v = X.iloc[i: (i+time_steps), 2].to_numpy()
        Xs.append(v)                     
    return np.array(Xs)

def getConceptDrifft(data_stream, dataset):
    ph = PageHinkley(20)

    # Adding stream elements to the PageHinkley drift detector and verifying if drift occurred
    CHANGE = 0
    lastconcept=0
    for i in np.arange(data_stream.shape[0]):  
        DELAY= (dataset.iloc[i, 1] - dataset.iloc[lastconcept, 1])
        for j in np.arange(data_stream[i].shape[0]):  
            ph.add_element(data_stream[i][j])
            if ph.detected_change():
                CHANGE = 1
                print('Change has been detected in data: ' + str(data_stream[i][j]) + ' - delay: '+str(DELAY) +' - of index: '+str(i)+'x'+str(i) )
                break


        init = i*WINDOW  

        if(CHANGE):   
            dataset.iloc[init: (init+WINDOW), 4] =  DELAY
            print('alterou de zero para', DELAY)
            dataset.iloc[init: (init+WINDOW),3] =  CHANGE
            CHANGE = 0
            lastconcept = i

    return dataset
    
def normalizing(dataset):
    print('loading Normalizing')
    #colunas que serão normalizadas
    f_columns = ['temperature','label']
    
    #normalizando train
    scaler1 = StandardScaler().fit(dataset[f_columns])
    scaler2 = StandardScaler().fit(dataset[f_columns])
    
    scaler1= scaler1.fit(dataset[f_columns].to_numpy())
    scaler2 = scaler2.fit(dataset[['delay']])
    
    dataset.loc[:,f_columns] = scaler1.transform(dataset[f_columns].to_numpy())
    dataset['delay'] = scaler2.transform(dataset[['delay']])
    
    return dataset
        
start = timer()
    
#carregando datasets
print('loading dataset')
test  = pd.read_csv('../datasets/sem_concept_drift/sdn_test1.csv', delimiter=",")
train1  = pd.read_csv('../datasets/sem_concept_drift/sdn_train1.csv', delimiter=",")
train2  = pd.read_csv('../datasets/sem_concept_drift/sdn_train2.csv', delimiter=",")
train3  = pd.read_csv('../datasets/sem_concept_drift/sdn_train3.csv', delimiter=",")
WINDOW = 20


#gerando concept drift train
print('loading train concept drift')
data_stream_train1 = create_window(train1, time_steps=WINDOW)
train1 = getConceptDrifft(data_stream_train1, train1)

data_stream_train2 = create_window(train2, time_steps=WINDOW)
train2 = getConceptDrifft(data_stream_train2, train2)

data_stream_train3 = create_window(train3, time_steps=WINDOW)
train3 = getConceptDrifft(data_stream_train3, train3)

#gerando concept drift test
print('loading test concept drift')
data_stream_test = create_window(test, time_steps=WINDOW)
test= getConceptDrifft(data_stream_test, test)


#salvando datasets normalizados
saveFile(train1, name='../datasets/com_concept_drift/sdn_train_unormalized.csv')
saveFile(train2, name='../datasets/com_concept_drift/sdn_train_unormalized.csv')
saveFile(train3, name='../datasets/com_concept_drift/sdn_train_unormalized.csv')
saveFile(test, name='../datasets/com_concept_drift/sdn_test_unormalized.csv')

#normalizando datasets
train1 = normalizing(train1)
train2 = normalizing(train2)
train3 = normalizing(train3)
test = normalizing(test)


#salvando datasets normalizados
saveFile(train1, name='../datasets/com_concept_drift/sdn_train_normalized.csv')
saveFile(train2, name='../datasets/com_concept_drift/sdn_train_normalized.csv')
saveFile(train3, name='../datasets/com_concept_drift/sdn_train_normalized.csv')
saveFile(test, name='../datasets/com_concept_drift/sdn_test_normalized.csv')

print('duração: ', timer() - start) 



