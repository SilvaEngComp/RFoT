import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/')
import paho.mqtt.client as mqtt
import json
import src.tatu
import argparse
from iotcoin import Iotcoin
from transaction import Transaction
from pool import Pool
from time import sleep
import numpy as np

parser = argparse.ArgumentParser(description = 'Blockchain node params')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
parser.add_argument('--time', action = 'store', dest = 'time', required = False)
args = parser.parse_args()  


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
    print("disconnected!")
    exit()
""" try:
        devices.remove(args.name)
    except:
        print(devices)"""
    
	
def on_message(mqttc, obj, msg):	
    msgJson = json.loads(msg.payload)
    if 'data' in msgJson:
        #corrupted_data = float(msgJson['data'])*np.random.randint(1000)
            
        transaction= Transaction(msgJson['header']['device'],msgJson['header']['sensor'],args.name, msgJson['data'])
        isCompleted = iotcoin.corruptData(transaction)	
        if isCompleted is True:
            iotcoin.restart()
           

			
        
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


   

#devices = deviceRunning()
if __name__ == '__main__':
    
    data = None
    separator = '-------'
    sub_client = None
    sub_broker = '10.0.0.6'
    sub_device = args.name
    topic = 'dev/+/RES'
    
    pub_client = None
    pub_broker = '10.0.0.28'
    pub_device = 'sc01'
    blocktopic = 'dev/sc28'
    iotcoin = Iotcoin(args.name, args.time)
    timeToCorrupt=5;
    with open('../../config.json') as f:
        data = json.load(f)
    
    #deviceRunning()
        
    
    sub_client = connect_mqtt(data, sub_broker, sub_device)
    sub_client = on_subscribe(sub_client, topic)
    sub_client.loop_forever()

	
		
		
		

	
