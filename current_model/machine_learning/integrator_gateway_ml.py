import paho.mqtt.client as mqtt
import json
import argparse
import sys
import os
from time import sleep
import time
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/current_model/data_collector')

from no_blockchain import NoBlockchain
from fd_model import FdModel
from fd_client import FdClient
from integrator_model import IntegratorModel

from time import sleep
import datetime

#Params to run file
parser = argparse.ArgumentParser(description = 'Params machine learning hosts')
parser.add_argument('--name', action = 'store', dest = 'name', required = True)
parser.add_argument('--clients', action = 'store', dest = 'clients', required = True)
args = parser.parse_args()

#You don't need to change this file. Just change sensors.py and config.json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(separator,"Connection returned successful!",separator)
    else:
        print("Failed to connect, return code %d \n", rc)


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
        return False


def on_disconnect(mqttc, obj, msg):
    #print(str(obj))
    print("disconnected!")
    exit()
	
       
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
    if 'fdModel' in msgJson:
        cardinality = msgJson['fdModel']['cardinality']
        model = msgJson['fdModel']["model"]
        local_host_name = msgJson['fdHost']
        fdModel = FdModel(local_host_name)
        fdModel.setModel(model)
        fdModel.setCardinality(cardinality)
        fdClient = FdClient(local_host_name, fdModel)
        integragorModel.addClients(fdClient)
        print('{} clients - receiving by {} at {} \n It is ready: {}'.
            format(len(integragorModel.getClients()), local_host_name,
                    datetime.datetime.now(), integragorModel.isCompleted()))
        
        if (integragorModel.isCompleted() is True):
            os.system('clear')
            integragorModel.globalModelTrain()
            onPublish()
    


def add_client(client):
    if integragorModel is None:
        return
    integratorModel.clients.append(client)
    if(len(integratorModel.clients)==2):
        publish()

def getLocalHostName():
    return  args.name
            
def onPublish():
    if(fdModel):
        if fdModel.hasValidModel():
            with open('../../config.json') as f:
                data = json.load(f)
            responseModel = {"code":"POST","method":"POST", "fdHost":'integrator',
                            "globalModel":integragorModel.getGlobalModel()}	
            resp = json.dumps(responseModel)
            pub_client = connect_mqtt(data, pub_broker, pub_device)
            pub_client = on_subscribe(pub_client, pub_topic)
            pub_client.loop_start()
            pub_client.publish(pub_topic, resp, 2, True)
            pub_client.loop_stop()
            
            print('\n \n Model {} published in: {} on topic: {} at {}' .format(getLocalHostName(), pub_broker,pub_topic, datetime.datetime.now()))
    else:
        print('fdModel is not defined')
def onSubscribe():
    with open('../../config.json') as f:
        data = json.load(f)
    
    sub_client = connect_mqtt(data, sub_broker, sub_device)
    sub_client = on_subscribe(sub_client, topic)
    sub_client.loop_forever()
    
# define the countdown func.
def countdown(t=5):    
    while t:
        timer = 'New Publication in {}s ...'.format(t)
        print(timer, end="\r")
        time.sleep(1)
        if(isWaiting is True):
            t -= 1
def initGlobalModel():
    print('waitting for a valid blockchain data...')
    while(True):
        block = NoBlockchain.getNotAssinedBlock()
        if block is not None:
            fdModel = FdModel(sub_device,block)
            print(fdModel)
            fdModel.preprocessing(treshould)
            print(fdModel.hasValidModel())
            if fdModel.hasValidModel():
                integragorModel = IntegratorModel(fdModel, args.clients)
                os.system('clear')
                onPublish()
                sleep(2)
                onSubscribe()   
                break
            else:
                print('Model could not be generated...') 
        
        countdown()

if __name__ == '__main__':
	#variable to main scop
    if args.name is None:
        args.name = 'integrator'
    data = None
    separator = '-------'
    sub_client = None
    sub_broker = '10.0.0.28'
    sub_device = args.name
    topic = 'dev/g03'
    pub_client = None
    pub_broker = '10.0.0.29'
    pub_device = 'sc02'
    pub_topic = 'dev/g04'
    prefix = '../data_collector'
    treshould = 0.02
    isWaiting = True
    initGlobalModel()
    fdModel = None

		
		
		

	


