        

from keras import backend as K
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from time import sleep
from sklearn.metrics import zero_one_loss
import csv
import matplotlib.pyplot as plt
import os
import re
import time
from threading import Thread
import matplotlib.animation as animation

from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import roc_curve
##https://matplotlib.org/stable/gallery/lines_bars_and_markers/psd_demo.html#sphx-glr-gallery-lines-bars-and-markers-psd-demo-py

#import seaborn as sns
class TestModel:
    def __init__(self):
        self._globalModel = None
        self._comm_round = 0
        self._results = []
        self.fileName = 'global_train_results.csv'
        self.dataset = None
        self.fig1 = plt.figure()
        self.fig1.set_size_inches(10.5,8.5)

        self.a1 = self.fig1.add_subplot(513)
        self.a2 = self.fig1.add_subplot(515)
        self.a3 = self.fig1.add_subplot(511)
    def setGlobalModel(self, fdModel):
        self.evolution = 0
        self._globalModel = fdModel
    def runTest(self):
        #test global model and print out metrics after each communications round
        X_train,X_test,y_train,y_test = self.preprocessing()
        #process and batch the test set  
        test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))
        for(X_test, Y_test) in test_batched:
            self.test_model(X_test,Y_test,self._globalModel.getModel())       
    
    def test_model(self,X_test, Y_test,  model):
            self._comm_round += 1
            #BinaryCrossentropy: Computes the crossentropy loss between the labels and predictions.
            bce = tf.keras.losses.BinaryCrossentropy(from_logits=True)
            Y_pred = model.predict(X_test, batch_size=100)
            Y_test = np.array(Y_test).reshape(len(Y_test),1)
            loss = bce(Y_test, Y_pred).numpy()
            #accuracy_score: In multilabel classification, the function returns the 
            # subset accuracy. If the entire set of predicted labels for a sample 
            # strictly match with the true set of labels, then the subset accuracy 
            # is 1.0; otherwise it is 0.0.
            acc = accuracy_score(tf.argmax(Y_pred, axis=1), tf.argmax(Y_test, axis=1))
            #zero_one_loss: If normalize is True, return the fraction of misclassifications (float), 
            # else it returns the number of misclassifications (int). The best performance is 0.
            zol = zero_one_loss(tf.argmax(Y_pred, axis=1), tf.argmax(Y_test, axis=1))
            evolution = self.getEvolution(loss)
            self._results.append([self._comm_round, acc,zol, loss, evolution])
            print('comm_round: {} | global_acc: {:.3%}   | global_zol: {} \n | global_loss: {} | evolution: {:.3%} '.format(self._comm_round, acc,zol,loss, evolution))
            self.saveDataset()
            animation.FuncAnimation(self.fig1, self.graphicGenarete1(Y_test,Y_pred), interval=1000)
            animation.FuncAnimation(self.fig1, self.graphicGenarete2(Y_test,Y_pred), interval=1000)
            animation.FuncAnimation(self.fig1, self.graphicGenarete3(Y_test,Y_pred), interval=1000)
            plt.show(block=False)
            plt.pause(3)
            ##plt.close()
            print('graphic printed...')
            
    def graphicGenarete1(self,Y_test,Y_pred):
        print('preparing graphic...')
        self.a1.clear()
        self.a1.set_title("Predito Vs Real")
        self.a1.plot(Y_test.flatten(), marker='.', label='true')
        self.a1.plot(Y_pred.flatten(),'r',marker='.', label='predicted')
        self.a1.legend();   
        # print('graphic prepered...')
        
    def graphicGenarete2(self,Y_test,Y_pred):
        size = np.min([Y_pred.shape[0],Y_test.shape[0] ])
        rmse =  mean_squared_error(Y_test.flatten()[0:size], Y_pred.flatten()[0:size], squared=False)
        mae =  mean_absolute_error(Y_test.flatten()[0:size], Y_pred.flatten()[0:size])
        median_mae = median_absolute_error(Y_test.flatten()[0:size], Y_pred.flatten()[0:size])
        evs = explained_variance_score(Y_test.flatten()[0:size], Y_pred.flatten()[0:size])
        
        objects = ['rmse', 'mae', 
                   'median-mae']
        y_pos = np.arange(3)
        performance = [rmse,mae,median_mae]

        self.a2.clear()
        self.a2.set_title("Métricas")
        self.a2.bar(objects, performance, align='center')
        self.a2.legend(); 
        
    def graphicGenarete3(self,Y_test,Y_pred):
        fper, tper, tresholds = roc_curve(Y_test.flatten(),Y_pred.flatten())
        self.a3.clear()
        self.a3.set_title("ROC")
        self.a3.plot(fper, marker='.', label='False Positive Rate')
        self.a3.plot(tper,'r',marker='.', label='True Positive Rate')
        self.a3.plot(tresholds,'g',marker='.', label='treshold')
        self.a3.legend(); 
    def getDatasetsFileNames(self, prefix='.'):
            fileNames = []
            for file in os.listdir(prefix):
                if file.endswith(".csv"):
                    x = re.search("^dataset.*csv$", file)
                    if(x):
                        fileNames.append(file)
            return fileNames
            
    def preprocessing(self):   
        sleep(2)  
        fileName = 'dataset.csv'
        print('...... readding {} ......'.format(fileName))
        dataset = pd.read_csv(fileName, delimiter=",")
        label = dataset.label
        dataset = dataset.drop(columns=['label'])
        local_model = None
        if(dataset.shape[0]>1):
            return train_test_split(dataset, label, test_size=1/3, random_state=10, 
                                                    stratify=label, shuffle=True)
        return None, None, None, None          


   
        
    def getEvolution(self, loss):
        evolution = 0
        if self.dataset is None:
            pass
        else:
            min_last_loss = min(self.dataset.global_loss)
            print('min_last_loss: ',min_last_loss)
            evolution = (min_last_loss - loss)/min_last_loss
        if(self.evolution < evolution):
            self.evolution = evolution
            self._globalModel.getModel().save('/saved_model')
        return evolution

    def saveDataset(self):
        cols = ['comm_round','global_acc','global_zol','global_loss', 'evolution']
        self.dataset = pd.DataFrame(self._results, columns = cols)
        with open(self.fileName,'w') as datasetFile:
            writer = csv.writer(datasetFile)
            writer.writerow(self.dataset.columns)
            for i in np.arange(int(self.dataset.shape[0])):
                writer.writerow(self.dataset.iloc[i,])