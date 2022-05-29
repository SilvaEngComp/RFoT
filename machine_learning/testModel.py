        

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

class TestModel:
    def __init__(self, fdModel):
        self._globalModel = fdModel
        self._comm_round = 0
        self._results = []
        self.fileName = 'global_train_results.csv'
        self.dataset = None
        
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
            self.graphicGenarete(Y_test,Y_pred)

    def getDatasetsFileNames(self, prefix='..'):
            fileNames = []
            for file in os.listdir(prefix):
                if file.endswith(".csv"):
                    x = re.search("^dataset.*csv$", file)
                    if(x):
                        fileNames.append(file)
            return fileNames
            
    def preprocessing(self):   
        sleep(2)  
        datasetFileNames = self.getDatasetsFileNames() 
        fileName = datasetFileNames[np.random.randint(len(datasetFileNames))]
        print('...... readding {} ......'.format(fileName))
        dataset = pd.read_csv(fileName, delimiter=",")
        label = dataset.label
        dataset = dataset.drop(columns=['label'])
        local_model = None
        if(dataset.shape[0]>1):
            return train_test_split(dataset, label, test_size=0.1, random_state=42, 
                                                    stratify=label, shuffle=True)
        return None, None, None, None    
    def graphicGenarete(self,Y_test,Y_pred):
        fig1 = plt.figure()
        a1 = fig1.add_subplot(1,1,1)
        a1.plot(Y_test.flatten(), marker='.', label='true')
        a1.plot(Y_pred.flatten(),'r',marker='.', label='predicted')
        a1.legend();   
        plt.show()
    def getEvolution(self, loss):
        evolution = 0
        
        if self.dataset is not None:
            min_last_loss = min(self.dataset.global_loss)
            evolution = (min_last_loss - loss)/min_last_loss
        return evolution

    def saveDataset(self):
        cols = ['comm_round','global_acc','global_zol','global_loss', 'evolution']
        self.dataset = pd.DataFrame(self._results, columns = cols)
        with open(self.fileName,'w') as datasetFile:
            writer = csv.writer(datasetFile)
            writer.writerow(self.dataset.columns)
            for i in np.arange(int(self.dataset.shape[0])):
                writer.writerow(self.dataset.iloc[i,])