import paho.mqtt.client as mqtt
import json
import tatu
import argparse
import iotcoin
from blockchain import Transaction
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
	
def on_message(mqttc, obj, msg):	
	msgJson = json.loads(msg.payload)

	if 'data' in msgJson:
		transaction= Transaction(msgJson['header']['device'],msgJson['header']['sensor'],'h28', msgJson['data'])
		blockchain = iotcoin.mine_block(transaction)	
		if blockchain:
			set_blockchain_publication(blockchain)

			
		
	
def set_blockchain_publication(blockchain):
	responseModel = {"code":"POST","method":"POST", "sensor":'sc28', "value":str(blockchain)}	
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



if __name__ == '__main__':
	with open('config.json') as f:
		data = json.load(f)
		
	
	sub_client = connect_mqtt(data, sub_broker, sub_device)
	sub_client = on_subscribe(sub_client, topic)
	sub_client.loop_forever()

	
		
		
		

	
