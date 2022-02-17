import paho.mqtt.client as mqtt
import json
import numpy as np
import statistics as st
import argparse


from time import sleep


"""parser = argparse.ArgumentParser(description = 'Params sensors')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
parser.add_argument('--broker', action = 'store', dest = 'broker', required = True)
parser.add_argument('--topic', action = 'store', dest = 'topic', required = False)
args = parser.parse_args()
"""
data = None

sub_client = None
sub_broker = '10.0.0.28'
sub_device = 'sc25'
topic = 'dev/sc28'

pub_client = None
pub_broker = '10.0.0.8'
pub_device = 'sc25'
blocktopic = 'dev/sc27'

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
	print('calling filter...')
	calcDeltaTemperature(msgJson['value']['chain'])

	
def calcDeltaTemperature(chain):		
	currencyBlock = list(chain)[-1]
	print ('\n block_number: ',currencyBlock['index'],' | timestamp: ', currencyBlock['timestamp'])
	currentyMeanTemperature, currencyTemperatures = calcMean(currencyBlock['transactions'])
	print('currency temperatures: ', currencyTemperatures)
	print('currency média: ',currentyMeanTemperature)
	 
	if(len(chain)>1):
		lastBlock = list(chain)[-2]
		print ('\n block_number: ',lastBlock['index'],' | timestamp: ', lastBlock['timestamp'])
		
		lastMeanTeamperature, lastTemperatures = calcMean(lastBlock['transactions'])
		print('last temperatures: ', lastTemperatures)
		print('last média: ',lastMeanTeamperature)
	
		print('delta T: ',abs(round(currentyMeanTemperature-lastMeanTeamperature, 2)))
		

def calcMean(transactions):
	temperatures = []
	for j in filter_by_sensor(transactions):
		temperatures.append(float(j['amount']))

	return [round(st.mean(temperatures), 2), temperatures]

def filter_by_sensor(transactions,sensor='temperatureSensor'):
	filtredTransactions = []
	for j in transactions:
		if(j['sensor'] == sensor):
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



if __name__ == '__main__':
	with open('../config.json') as f:
		data = json.load(f)

	sub_client = connect_mqtt(data, sub_broker, sub_device)
	sub_client = on_subscribe(sub_client, topic)
	sub_client.loop_forever()

	
		
		
		

	
