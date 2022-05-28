from keras import backend as K
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
class IntegratorModel:
    def __init__(self, fdModel, qtd_clients = 1):
        self._clients = set()
        self._qtd_clients = qtd_clients
        self._globalModel = fdModel
        self._comm_round = 0
        
    def getGlobalModel(self):
        return self._globalModel.toJson()
        
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
        if len(self_clients) == self._qtd_clients:
            return True
        return False
    def weight_scalling_factor(self, client):
        #get the bs
        bs = self._qtd_clients
        print("cardinality: ",client.getFdModel().getCardinality())
        #first calculate the total training data points across clinets
        global_count = sum([client.getFdModel().getCardinality() for client in self._clients])*bs
        print("global_count: ", global_count)
        # get the total number of data points held by a client
        local_count = client.getFdModel().getCardinality()*bs
        print("local_count: ", local_count)
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


    def test_model(self,X_test, Y_test,  model):
        self._comm_round += 1
        cce = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
        #logits = model.predict(X_test, batch_size=100)
        logits = model.predict(np.array([X_test]))
        Y_test = np.array(Y_test).reshape(1,-1)
        loss = cce(Y_test, logits)
        acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
        print('comm_round: {} | global_acc: {:.3%} | global_loss: {}'.format(self._comm_round, acc, loss))
        return acc, loss

    def preprocessing(self, client):     
        datasetFileName = 'dataset_'+client.getName()+'.csv'  
        dataset = pd.read_csv(datasetFileName, delimiter=",")
        print(dataset.head())
        label = dataset.label
        dataset = dataset.drop(columns=['label'])
        local_model = None
        if(dataset.shape[0]>1):
            return train_test_split(dataset, label, test_size=0.1, random_state=42, 
                                                    stratify=label, shuffle=True)
        return None, None, None, None

        #split data into training and test set
        return  train_test_split(df.iloc[:,0],df.iloc[:,1],test_size=0.1, random_state=42)
    
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
            global_acc, global_loss = self.test_model(X_test,
                                                 Y_test,
                                                 self._globalModel.getModel())      
    