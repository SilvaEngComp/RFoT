import numpy as np
import pandas as pd
import random
import cv2
import os
from imutils import paths
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from keras import backend as K

#from fl_mnist_implementation_tutorial_utils import *


def preprocessiing():
   
    prep_dataset = pd.read_csv('/content/drive/MyDrive/dissertação/codigos/FL/datasets/dataset_test_02_07.csv', delimiter=",")
    prep_dataset = prep_dataset[(prep_dataset["temperature"] >=15)]
    prep_dataset = prep_dataset[(prep_dataset["temperature"] <=40)]
    df = prep_dataset.iloc[:,1:4]
    #split data into training and test set
    return  train_test_split(df.iloc[:,0],df.iloc[:,1],test_size=0.1, random_state=42)
   

# start = timer()
X_train, X_test, y_train, y_test = preprocessiing()

#X_train[0:size]
# X_train,Y_train = create_dataset(train, train.delay)


def create_clients(mensurement_list, label_list, num_clients=10, initial='clients'):
    ''' return: a dictionary with keys clients' names and value as 
                data shards - tuple of images and label lists.
        args: 
            mensurement_list: a list of numpy arrays of training images
            label_list:a list of binarized labels for each image
            num_client: number of fedrated members (clients)
            initials: the clients'name prefix, e.g, clients_1 
            
    '''

    #create a list of client names
    client_names = ['{}_{}'.format(initial, i+1) for i in range(num_clients)]

    #randomize the data
    data = list(zip(mensurement_list, label_list))
    random.shuffle(data)
    size = len(data)//10
    #shard data and place at each client    
    shards = [data[i:i + size] for i in range(0, size*num_clients, size)]

    #number of clients must equal number of shards
    assert(len(shards) == len(client_names))

    return {client_names[i] : shards[i] for i in range(len(client_names))} 
    
    
    #create clients
clients = create_clients(X_train, y_train, num_clients=10, initial='client')
len(clients)

def batch_data(data_shard, bs=32):
    '''Takes in a clients data shard and create a tfds object off it
    args:
        shard: a data, label constituting a client's data shard
        bs:batch size
    return:
        tfds object'''
    #seperate shard into data and labels lists
    data, label = zip(*data_shard)
    dataset = tf.data.Dataset.from_tensor_slices(list([list(data), list(label)]))
    return dataset.shuffle(len(label)).batch(bs)
    
    def batch_data_dict(data_shard):

    #seperate shard into data and labels lists
    data, label = zip(*data_shard)
    return {'data':np.array(data), 'label':np.array(label)}
    
    
    def weight_scalling_factor(clients_trn_data, client_name):
    client_names = list(clients_trn_data.keys())
    #get the bs
    bs = list(clients_trn_data[client_name])[0][0].shape[0]
    #first calculate the total training data points across clinets
    global_count = sum([tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy() for client_name in client_names])*bs
    # get the total number of data points held by a client
    local_count = tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy()*bs
    return local_count/global_count


def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final



def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)
        
    return avg_grad


def test_model(X_test, Y_test,  model, comm_round):
    cce = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    #logits = model.predict(X_test, batch_size=100)
    logits = model.predict(np.array([X_test]))
    Y_test = np.array(Y_test).reshape(1,-1)
    loss = cce(Y_test, logits)
    acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
    print('comm_round: {} | global_acc: {:.3%} | global_loss: {}'.format(comm_round, acc, loss))
    return acc, loss
    
    
    from tensorflow.python.ops.gen_array_ops import tensor_scatter_sub_eager_fallback

#process and batch the training data for each client
clients_batched = dict()
clients_batched_tf = dict()
for (client_name, data) in clients.items():
    clients_batched[client_name] = batch_data_dict(data)
    clients_batched_tf[client_name] = batch_data(data)
    
#process and batch the test set  
test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))


from numpy.lib import shape_base
class SimpleMLP:
    @staticmethod
    def build(shape, classes):
        model = Sequential([
            Dense(32, activation='relu', input_shape=(shape,)),
            Dense(372, activation='sigmoid')   
        ])
        

        return model
        
        
        learning_rate = 0.01 
comms_round = 100
loss ="categorical_crossentropy"
# optimizer = tf.keras.optimizers.Adam(
# learning_rate)
metrics = ['accuracy']
optimizer = SGD(learning_rate, 
                decay= learning_rate / comms_round, 
                momentum=0.9
               )      
               
               
#initialize global model
shape = clients_batched['client_1']['data'].shape[0]
smlp_global = SimpleMLP()
global_model = smlp_global.build(shape, 10)
        
#commence global training loop
for comm_round in range(comms_round):
            
    # get the global model's weights - will serve as the initial weights for all local models
    global_weights = global_model.get_weights()
    
    #initial list to collect local model weights after scalling
    scaled_local_weight_list = list()

    #randomize client data - using keys
    client_names= list(clients_batched.keys())
    random.shuffle(client_names)
    
    #loop through each client and create new local model
    for client in client_names:
      print('training client: ',client)
      smlp_local = SimpleMLP()
      local_model = smlp_local.build(shape, 10)
      local_model.compile(loss=loss, 
                    optimizer=optimizer, 
                    metrics=metrics)
      
      #set local model weight to the weight of the global model
      local_model.set_weights(global_weights)
      
      #fit local model with client's data
      local_model.fit(np.array([clients_batched[client]['data']]),np.array([clients_batched[client]['label']]), epochs=1, verbose=0)
      
      #scale the model weights and add to list
      scaling_factor = weight_scalling_factor(clients_batched_tf, client)
      scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
      scaled_local_weight_list.append(scaled_weights)
      
      #clear session to free memory after each communication round
      print('cleaning section');
      K.clear_session()
        
    #to get the average over all the local model, we simply take the sum of the scaled weights
    average_weights = sum_scaled_weights(scaled_local_weight_list)
    # print('média dos pesos: ',average_weights)
    
    #update global model 
    global_model.set_weights(average_weights)

    #test global model and print out metrics after each communications round
    for(X_test, Y_test) in test_batched:
        global_acc, global_loss = test_model(X_test[0:shape], Y_test[0:shape], global_model, comm_round)      
  

    
    


