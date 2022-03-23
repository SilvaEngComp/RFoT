import paho.mqtt.client as mqtt
import json
import numpy as np
import pandas as pd
import statistics as st
import argparse
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml')

from blockchain import Blockchain

from time import sleep

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
    msgJson = json.loads(msg.payload)
    chain = blockchain.replaceChain(prefix, True)
    #calcDeltaTemperature(blockchain)

	
def calcDeltaTemperature(blockchain, trashoulder=0.2):
    datasetRows = []
    datasetCols = []	
    for currencyBlock in blockchain.chain:	
        print ('\n block_number: ',currencyBlock.index,' | timestamp: ', currencyBlock.timestamp)
        meanTemperature, temperatures = calcMean(currencyBlock['transactions'])
        print('currency temperatures: ', currencyTemperatures)
        print('currency média: ',currentyMeanTemperature)
        
        standard_desviation = st.pvariance(temperatures)
        print('standard desviation: ',standard_desviation)
        if(standard_desviation > trashoulder):
            datasetCols.append([standard_desviation,1])
        else:
            datasetCols.append([standard_desviation,0])
        datasetRows.append(datasetCols)
    
    
    saveDataset(datasetRows)
        
def saveDataset(datasetRows):
    cols = ['delta','class']
    pd.DataFrame(datasetRows, columns = cols)
    
    

def calcMean(transactions):
	temperatures = []
	for j in filter_by_sensor(transactions):
		temperatures.append(float(j.amount))

	return [round(st.mean(temperatures), 2), temperatures]

def filter_by_sensor(transactions,sensor='temperatureSensor'):
	filtredTransactions = []
	for j in transactions:
		if(j.sensor == sensor):
			filtredTransactions.append(j)
	return filtredTransactions
	
def set_blockchain_publication(blockchain):
	responseModel = {"code":"POST","method":"POST", "sensor":'sc28', "value":blockchain}	
	resp = json.dumps(responseModel)

	pub_client = connect_mqtt(data, pub_broker, pub_device)
	pub_client = on_subscribe(pub_client, blocktopic)
	pub_client.loop_start()
	
	pub_client.publish(blocktopic, resp)

	print('chain published in: ',blocktopic,'\n\n')
        
def on_subscribe(client: mqtt, topic): 
	print('subscribing in topic: ', topic) 
	try:
		client.subscribe(topic,1)
		client.on_message = on_message
		client.on_disconnect = on_disconnect
		return client
	except:
		print('subscribing error')


def deviceTraining():
    devices = set()
    flag = 0
    try:
        with open('devices_training.json') as devicesFile:
            data = json.load(devicesFile)
            devices = set(data['devices'])
            if(args.name in data['devices']):
                flag = -1
            devices.add(args.name)
            registerDevice(devices)
    except:
        devices.add(args.name)
        registerDevice(devices)
    
    return devices
    
def registerDevice(devices):
    with open('devices_running.json','w+') as devicesFile:
        devices = {"devices": list(devices)}
        json.dump(devices, devicesFile)

if __name__ == '__main__':
    #variable to main scope
    data = None
    separator = '-------'
    sub_client = None
    sub_broker = '10.0.0.28'
    sub_device = args.name
    topic = 'dev/sc28'
    pub_client = None
    pub_broker = '10.0.0.29'
    pub_device = 'sc01'
    blocktopic = 'dev/sc29'
    prefix = '../'
    blockchain = Blockchain(sub_device)
    blockchain.chain = blockchain.replaceChain(prefix, True)
    #print(blockchain)
    with open('../config.json') as f:
        data = json.load(f)
    
    deviceTraining()
    sub_client = connect_mqtt(data, sub_broker, sub_device)
    sub_client = on_subscribe(sub_client, topic)
    sub_client.loop_forever()

	
		
		
		

	
