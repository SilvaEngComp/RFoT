import os
import argparse
import json
import paho.mqtt.client as mqtt
from src.proposed_model.smart_contract_3 import SC3
from src.current_model.no_blockchain import NoBlockchain
from fd_model import FdModel
from fd_client import FdClient
from src.suport_layer.block import Block
from integrator_model import IntegratorModel
from time import sleep
import datetime
import sys

# import sys

# sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/proposed_model/data_collector')


# Params to run file
parser = argparse.ArgumentParser(description='Params machine learning hosts')
parser.add_argument('--name', action='store', dest='name', required=True)
parser.add_argument('--clients', action='store', dest='clients', required=True)
parser.add_argument('--solution', action='store',
                    dest='solution', required=True)
args = parser.parse_args()
# You don't need to change this file. Just change sensors.py and config.json


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(separator, "Connection returned successful!", separator)
    else:
        print("Failed to connect, return code %d \n", rc)


def connect_mqtt(data, mqttBroker, deviceName) -> mqtt:
    try:
        data["deviceName"] = deviceName
        data["mqttBroker"] = mqttBroker
        mqttPort = data["mqttPort"]
        mqttUsername = data["mqttUsername"]
        mqttPassword = data["mqttPassword"]

        sub_client = mqtt.Client(deviceName + "_block", protocol=mqtt.MQTTv31)
        sub_client.username_pw_set(mqttUsername, mqttPassword)
        sub_client.on_connect = on_connect
        sub_client.connect(mqttBroker, int(mqttPort), 60)
        return sub_client
    except:
        print("Broker unreachable on " + mqttBroker + " URL!")
        sleep(5)
        return False


def on_disconnect(mqttc, obj, msg):
    # print(str(obj))
    print("disconnected!")
    exit()


def on_subscribe(client: mqtt, topic):
    print('subscribing: ', sub_broker, ' in topic: ', topic)
    try:
        client.subscribe(topic, 1)
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        print(separator, 'subscription successfull!', separator)
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
    if (len(integratorModel.clients) == 2):
        publish(None)


def getLocalHostName():
    return args.name


def onPublish():
    if fdModel is None:
        print("Nothing published...")
        return
    if fdModel.hasValidModel():
        with open('../config.json') as f:
            data = json.load(f)
        responseModel = {"code": "POST", "method": "POST", "fdHost": 'integrator',
                         "globalModel": integragorModel.getGlobalModel()}
        os.system('clear')
        resp = json.dumps(responseModel)
        pub_client = connect_mqtt(data, pub_broker, pub_device)
        pub_client = on_subscribe(pub_client, pub_topic)
        pub_client.loop_start()
        pub_client.publish(pub_topic, resp, 2, True)
        pub_client.loop_stop()
        # print(integragorModel.getGlobalModel())
        print('\n \n Model {} published in: {} on topic: {} at {}' .format(
            getLocalHostName(), pub_broker, pub_topic, datetime.datetime.now()))


def onSubscribe():
    with open('../config.json') as f:
        data = json.load(f)
    sub_client = connect_mqtt(data, sub_broker, sub_device)
    sub_client = on_subscribe(sub_client, topic)
    sub_client.loop_forever()


def getdataBlock():
    block = None
    if args.solution == '1':
        block = NoBlockchain.getNotAssinedBlock()
    else:
        block = SC3.getNotAssinedBlock(sub_device)
    return block




if __name__ == '__main__':
    # variable to main scop
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
    print('waitting for a valid blockchain data...')
    
    
    fdModel = FdModel(sub_device, None)
    integragorModel = IntegratorModel(fdModel, args.clients,True)
    
    if integragorModel.getGlobalModel() is not None:
        os.system('clear')
        onPublish()
        sleep(2)
        onSubscribe()
    while (True):
        # os.system('clear')
        block = getdataBlock()
        if block is not None:
            fdModel = FdModel(sub_device, block)
            fdModel.preprocessing()
            if fdModel.hasValidModel():
                integragorModel = IntegratorModel(fdModel, args.clients)
                os.system('clear')
                onPublish()
                sleep(2)
                onSubscribe()
                break
            else:
                sleep(5)
        else:
            sleep(5)
