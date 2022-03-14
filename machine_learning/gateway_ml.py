import tensorflow as tf
import paho.mqtt.client as mqtt
import json
#import tatu
import argparse
##import iotcoin
import utils_hosts
utils_hosts.append('../')
from time import sleep



"""parser = argparse.ArgumentParser(description = 'Params sensors')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
parser.add_argument('--broker', action = 'store', dest = 'broker', required = True)
parser.add_argument('--topic', action = 'store', dest = 'topic', required = False)
args = parser.parse_args()
"""
data = None
separator = '-------'
sub_client = None
sub_broker = '10.0.0.6'
sub_device = 'sc01'
topic = 'dev/+/RES'

pub_client = None
pub_broker = '10.0.0.28'
pub_device = 'sc01'
blocktopic = 'dev/sc28'
qtd_hosts = 0
hosts_ml_node = []
#You don't need to change this file. Just change sensors.py and config.json

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print(separator,"Connection returned successful!",separator)
	else:
		print("Failed to connect, return code %d\n", rc)
             
def connect_mqtt(data, mqttBroker, deviceName) -> mqtt: 
	try:
		data["deviceName"]=deviceName
		data["mqttBroker"]=mqttBroker
		mqttPort = data["mqttPort"]
		mqttUsername = data["mqttUsername"]
		mqttPassword = data["mqttPassword"]

		sub_client = mqtt.Client(deviceName + "_block", protocol=mqtt.MQTTv31)
		sub_client.username_pw_set(mqttUsername, mqttPassword)
		sub_client.on_connect = on_connect
		sub_client.connect(mqttBroker, int(mqttPort),60)
		return sub_client
	except :
		print ("Broker unreachable on " + mqttBroker + " URL!")
		sleep(5)

def on_disconnect(mqttc, obj, msg):
	#print(str(obj))
	print("disconnected!")
	exit()
	


			
		
	
def set_blockchain_publication(blockchain):
	responseModel = {"code":"POST","method":"POST", "sensor":'sc28', "value":blockchain}	
	resp = json.dumps(responseModel)

	pub_client = connect_mqtt(data, pub_broker, pub_device)
	pub_client = on_subscribe(pub_client, blocktopic)
	pub_client.loop_start()
	
	pub_client.publish(blocktopic, resp)

	print('chain published in: ',blocktopic,'\n\n')
        
def on_subscribe(client: mqtt, topic): 
	print('subscribing: ',sub_broker,' in topic: ', topic) 
	try:
		client.subscribe(topic,1)
		client.on_message = on_message
		client.on_disconnect = on_disconnect
		print(separator,'subscription successfull!',separator)
		return client
	except:
		print('subscribing error')

def on_message(mqttc, obj, msg):	
	msgJson = json.loads(msg.payload)

	if 'data' in msgJson:
		host_ml_nodes.append(HostMlNode(msgJson['header']['device'], msgJson['data'])
		
		
		responseModel={'sender':msgJson['header']['device'],'sensor':msgJson['header']['sensor'],'receiver':'h28','amount': msgJson['data']}
		response = json.dumps(responseModel)
		blockchain = iotcoin.mine_block(response)	
		if blockchain:
			set_blockchain_publication(blockchain)


def add_client(client, num_clients=10, initial='clients'):
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



if __name__ == '__main__':
	with open('../config.json') as f:
		data = json.load(f)
		
	associations=utils_hosts.return_association()
	qtd_hosts = len(associations)
	sub_client = connect_mqtt(data, sub_broker, sub_device)
	sub_client = on_subscribe(sub_client, topic)
	sub_client.loop_forever()
	
		
		
		

	


