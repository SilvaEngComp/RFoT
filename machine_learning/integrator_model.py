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

class IntegratorModel:
    def __init__(self, fdModel, qtd_clients = 1):
        if isinstance(qtd_clients, str):
            qtd_clients = int(qtd_clients)
            
        self._clients = set()
        self._qtd_clients = qtd_clients
        self._globalModel = fdModel
        self._comm_round = 0
        self._results = []
        self.fileName = 'global_train_results.csv'
        self.dataset = None
        
    def getGlobalModel(self):
        return self._globalModel.toJson()
        
    def getResults(self):
        return self._results
        
    def setGlobalModel(self,fdModel):
        self._globalModel = fdModel
        
    def addClients(self, model):
        self._clients.add(model)   
        
    def toJson(self):
        return {
            "clients": self._clients
        }
    
    def getClients(self):
        return self._clients
    
    def isCompleted(self):
        if len(self._clients) >= self._qtd_clients:
            return True
        return False
    def weight_scalling_factor(self, client):
        #get the bs
        bs = self._qtd_clients
        #first calculate the total training data points across clinets
        global_count = sum([client.getFdModel().getCardinality() for client in self._clients])*bs
        # get the total number of data points held by a client
        local_count = client.getFdModel().getCardinality()*bs
        return local_count/global_count


    def scale_model_weights(self,weight, scalar):
        '''function for scaling a models weights'''
        weight_final = []
        steps = len(weight)
        for i in range(steps):
            weight_final.append(np.dot(np.array(scalar), weight[i]))
        return weight_final



    def sum_scaled_weights(self,scaled_weight_list):
        '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
        avg_grad = list()
        #get the average grad accross all client gradients
        for grad_list_tuple in zip(*scaled_weight_list):
            layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
            avg_grad.append(layer_mean)
            
        return avg_grad


 

    def preprocessing(self, client):   
        sleep(2)  
        datasetFileName = 'dataset_'+client.getName()+'.csv'  
        print('...... readding {} ......'.format(datasetFileName))
        dataset = pd.read_csv(datasetFileName, delimiter=",")
        label = dataset.label
        dataset = dataset.drop(columns=['label'])
        local_model = None
        if(dataset.shape[0]>1):
            return train_test_split(dataset, label, test_size=0.1, random_state=42, 
                                                    stratify=label, shuffle=True)
        return None, None, None, None

        #split data into training and test set
        return  train_test_split(df.iloc[:,0],df.iloc[:,1],test_size=0.1, random_state=42)
    def resetClients(self):
        self._clients.clear()
        
    def globalModelTrain(self):
        #initial list to collect local model weights after scalling
        scaled_local_weight_list = list()
        
        #loop through each client and create new local model
        for client in self._clients:
           
            #scale the model weights and add to list
            scaling_factor = self.weight_scalling_factor(client)
            scaled_weights = self.scale_model_weights(client.getFdModel().getModelWeights(), scaling_factor)
            scaled_local_weight_list.append(scaled_weights)
        
        #clear session to free memory after each communication round
        print('cleaning section');
        K.clear_session()
            
        #to get the average over all the local model, we simply take the sum of the scaled weights
        average_weights = self.sum_scaled_weights(scaled_local_weight_list)
        # print('média dos pesos: ',average_weights)
        
        #update global model 
        self._globalModel.getModel().set_weights(average_weights)

        #test global model and print out metrics after each communications round
        X_train,X_test,y_train,y_test = self.preprocessing(client)
        #process and batch the test set  
        test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))
        for(X_test, Y_test) in test_batched:
            self.test_model(X_test,
                                                 Y_test,
                                                 self._globalModel.getModel())
        self.resetClients()  
        
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