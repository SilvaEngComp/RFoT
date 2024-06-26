# import sys
# sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/')
import paho.mqtt.client as mqtt
import json
import argparse

from time import sleep
from src.proposed_model.smart_contract_1 import SC1
from src.utils.time_register import TimeRegister
parser = argparse.ArgumentParser(description = 'Blockchain node params')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
parser.add_argument('--size', action = 'store', dest = 'blockWidth', required = False)
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
    isCompleted = sc1.dataTreating(msg)	
    # print("isCompleted: ",isCompleted)
    if isCompleted is True:
        sc1.restart() 

			

	
def setBlockchainPublication(blockchain):
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

def deviceRunning():
    devices = set()
    flag = 0
    try:
        with open('devices_running.json') as devicesFile:
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

#devices = deviceRunning()
if __name__ == '__main__':
    TimeRegister.fileName = "RFoT_collector_challenge_7"
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
    sc1 = SC1(sub_device, args.blockWidth)
    
    with open('../config.json') as f:
        data = json.load(f)

    sub_client = connect_mqtt(data, sub_broker, sub_device)
    sub_client = on_subscribe(sub_client, topic)
    sub_client.loop_forever()

	
		
		
		

	
