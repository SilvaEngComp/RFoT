import paho.mqtt.client as mqtt
import json
import argparse

import os
import datetime
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/proposed_model/data_collector')

from blockchain import Blockchain
from fd_model import FdModel
import numpy as np
from time import sleep
import time


#Params to run file
parser = argparse.ArgumentParser(description = 'Params machine learning hosts')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
args = parser.parse_args()



#You don't need to change this file. Just change sensors.py and config.json

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connection returned result: ",str(rc))
	else:
		print("Failed to connect, return code %d\n", rc)
             
def connect_mqtt(data, mqttBroker, deviceName) -> mqtt: 
	try:
		data["deviceName"]=deviceName
		data["mqttBroker"]=mqttBroker
		mqttPort = data["mqttPort"]
		mqttUsername = data["mqttUsername"]
		mqttPassword = data["mqttPassword"]

		sub_client = mqtt.Client(deviceName + "_fdl", protocol=mqtt.MQTTv31)
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
	
def on_message(mqttc, obj, msg):
    os.system('clear')
    msgJson = json.loads(msg.payload)
    global_host_name = msgJson['fdHost']
    model = msgJson['globalModel']["model"]
    
    
    print('receiving a new global model by {} at {}'.format(global_host_name, datetime.datetime.now()))
    block = Blockchain.getNotAssinedBlock(sub_device)
    if(block is not None):
        fdModel = FdModel(sub_device,block)
        fdModel.setModel(model)
        fdModel.preprocessing(0.002)
        sleep(5)
        onPublish(fdModel)
# define the countdown func.
def countdown(t=5):    
    while t:
        timer = 'New Publication in {}s ...'.format(t)
        print(timer, end="\r")
        time.sleep(1)
        if(isWaiting is True):
            t -= 1
    onPublish(fdModel)

def onPublish(fdModel, isStarting=False):
    sleep(np.random.randint(5))
    resp = None
    if fdModel is not None:
        responseModel = {"fdHost":sub_device,"fdModel":fdModel.toJson()}	
        resp = json.dumps(responseModel)
    if resp is not None:
        with open('../../config.json') as f:
            data = json.load(f)
        pub_client = connect_mqtt(data, pub_broker, pub_device)
        pub_client = on_subscribe(pub_client, pub_topic)
        pub_client.loop_start()
        
        pub_client.publish(pub_topic, resp,0)
        pub_client.loop_stop()
        print('\n \n Model {} published in: {} on topic: {} at {}' .format(fdModel, pub_broker,pub_topic, datetime.datetime.now()))
        countdown()
        
def on_subscribe(client: mqtt, topic): 
	print('subscribing in topic: ', topic) 
	try:
		client.subscribe(topic,1)
		client.on_message = on_message
		client.on_disconnect = on_disconnect
		return client
	except:
		print('subscribing error')



def onSubscribe():
    with open('../../config.json') as f:
        data = json.load(f)
    
    sub_client = connect_mqtt(data, sub_broker, sub_device)
    sub_client = on_subscribe(sub_client, topic)
    sub_client.loop_forever()

if __name__ == '__main__':
    #variable to main scope
    data = None
    separator = '-------'
    sub_client = None
    sub_broker = '10.0.0.29'
    sub_device = args.name
    topic = 'dev/g04'
    pub_client = None
    pub_broker = '10.0.0.28'
    pub_device = 'g03'
    pub_topic = 'dev/g03'
    prefix = '../data_collector'
    os.system('clear')
    isWaiting=True
    fdModel = None
    onSubscribe()

	
		
		
		

	
