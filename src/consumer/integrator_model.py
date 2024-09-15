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
import json
class IntegratorModel:
    def __init__(self, fdModel=None, qtd_clients = 1, isStarting=None):
        if isinstance(qtd_clients, str):
            qtd_clients = int(qtd_clients)
            
        self._clients = set()
        self._qtd_clients = qtd_clients
        self._globalModel = self.start(fdModel,isStarting)
        self._comm_round = 0
        self._results = []
        self.fileName = 'global_train_results.csv'
        self.dataset = None
        
    def getGlobalModel(self):
        if self._globalModel.getModel() is None:
            return None
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
        self.resetClients() 
        self.register() 
    def register(self):
        fileName = "global_model.json"
        with open(fileName, "w") as file:
            try:
                print('registring new global model version')
                json.dump(self.getGlobalModel(), file)
            except:
                print('erro in global model registration')
        
    def start(self,fdModel,isStarting):
        if isStarting is None:
            return fdModel
        fileName = "global_model.json"
        if os.path.exists(fileName) is False:
            print(f'not found local pool file: {fileName} ')
            return fdModel
        try:
            print('try')
            with open(fileName) as file:
                if os.path.getsize(fileName) > 0:
                    data = json.load(file)
                    fdModel.setModel(data)
                    return fdModel
                else:
                    return fdModel
        except:
            print('erro in global model registration')
    