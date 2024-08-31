# import imp
# import sys
# from pathlib import Path
# file = Path(__file__).resolve()
# parent, root = file.parent, file.parents[1]
# sys.path.append(str(root))

import paho.mqtt.client as mqtt
import json
import argparse

import os
import datetime

from src.current_model.no_blockchain import NoBlockchain
from src.proposed_model.smart_contract_2 import SC2
from src.proposed_model.smart_contract_3 import SC3
from fd_model import FdModel
import numpy as np
from time import sleep
import time
from src.utils.time_register import TimeRegister

#Params to run file
parser = argparse.ArgumentParser(description = 'Params machine learning hosts')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
parser.add_argument('--solution', action='store',
                    dest='solution', required=True)

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

def getdataBlock():
    block = None
    if args.solution == '1':
        block = NoBlockchain.getNotAssinedBlock()
    else:
        block = SC3.getNotAssinedBlock(sub_device)
    return block


def startProcessing():
    print('waitting for a valid blockchain data...')
    while (True):
        block = getdataBlock()
        if block is not None:
            fdModel = FdModel(sub_device, block)
            fdModel.preprocessing()
            if fdModel.hasValidModel():
                return fdModel
            else:
                sleep(5)
        else:
            sleep(5)
	
def on_message(mqttc, obj, msg):
    
    msgJson = json.loads(msg.payload)
    global_host_name = msgJson['fdHost']
    model = msgJson['globalModel']["model"]
    
    print('receiving a new global model by {} at {}'.format(global_host_name, datetime.datetime.now()))
    fdModel = startProcessing()
    if args.solution == '2':
        SC2.minerNotAssinedTransaction(sub_device,fdModel.toJson(),"data_consumer")
        TimeRegister.addTime("Block Consumer minered on BCR")
    TimeRegister.addTime("training and product registration finished")
    sleep(5)
    onPublish(fdModel)
    TimeRegister.addTime("local model published")
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
    if fdModel is None:
        os.system('clear')
        print("Nothing published...")
        return
    sleep(np.random.randint(5))
    resp = None
    os.system("clear")
    responseModel = {"fdHost":sub_device,"fdModel":fdModel.toJson()}	
    resp = json.dumps(responseModel)
    with open('../config.json') as f:
        data = json.load(f)
    pub_client = connect_mqtt(data, pub_broker, pub_device)
    pub_client = on_subscribe(pub_client, pub_topic)
    pub_client.loop_start()
    
    pub_client.publish(pub_topic, resp,0)
    pub_client.loop_stop()
    # print('\n \n Model {} published in: {} on topic: {} at {}' .format(fdModel, pub_broker,pub_topic, datetime.datetime.now()))
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
    with open('../config.json') as f:
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
    os.system('clear')
    isWaiting=True
    fdModel = None
    onSubscribe()

	
		
		
		

	
