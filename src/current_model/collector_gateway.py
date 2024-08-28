import sys
import paho.mqtt.client as mqtt
import json
import argparse
from iotcoin import Iotcoin
from src.suport_layer.transaction import Transaction
from time import sleep
from src.suport_layer.cipher import Cipher
from src.utils.time_register import TimeRegister

parser = argparse.ArgumentParser(description='NoBlockchain node params')
parser.add_argument('--name', action='store', dest='name', required=True)
parser.add_argument('--size', action='store',
                    dest='blockWidth', required=False)
args = parser.parse_args()


# You don't need to change this file. Just change sensors.py and config.json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(separator, "Connection returned successful!", separator)
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt(data, mqttBroker, deviceName) -> mqtt:
    try:
        data["deviceName"] = deviceName
        data["mqttBroker"] = mqttBroker
        mqttPort = data["mqttPort"]
        mqttUsername = data["mqttUsername"]
        mqttPassword = data["mqttPassword"]
        
        sub_client = mqtt.Client(deviceName + "_block", protocol=mqtt.MQTTv31)
        print(sub_client)
        sub_client.username_pw_set(mqttUsername, mqttPassword)
        print("38")
        sub_client.on_connect = on_connect
        print(f'40 {mqttBroker} - port {mqttPort}')
        sub_client.connect(mqttBroker, int(mqttPort), 60)
        print(sub_client)
        return sub_client
    except:
        print("Broker unreachable on " + mqttBroker + " URL!")
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
        data = decryptData(msgJson['data'])
        transaction = Transaction(
            msgJson['header']['device'], msgJson['header']['sensor'], args.name, msgJson['data'])
        isCompleted = iotcoin.transactionProcess(transaction)
        if isCompleted is True:
            TimeRegister.addTime("transaction registed")
            iotcoin.restart()


def decryptData(temp):
    cipher = Cipher()
    temp = temp.replace("b'", "'")
    temp = str.encode(temp)
    decriptedTemp = cipher.decrypt(temp)
    dataJson = json.loads(decriptedTemp)
    return dataJson


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


def deviceRunning():
    devices = set()
    flag = 0
    try:
        with open('devices_running.json') as devicesFile:
            data = json.load(devicesFile)
            devices = set(data['devices'])
            if (args.name in data['devices']):
                flag = -1
            devices.add(args.name)
            registerDevice(devices)
    except:
        devices.add(args.name)
        registerDevice(devices)

    return devices


def registerDevice(devices):
    with open('devices_running.json', 'w+') as devicesFile:
        devices = {"devices": list(devices)}
        json.dump(devices, devicesFile)


# devices = deviceRunning()
if __name__ == '__main__':
    TimeRegister.fileName = "commom_IoT_collector"
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

    iotcoin = Iotcoin(args.name, args.blockWidth)
    if (iotcoin is not None):
        with open('../config.json') as f:
            data = json.load(f)

        # deviceRunning()
        print(data)
        sub_client = connect_mqtt(data, sub_broker, sub_device)
        sub_client = on_subscribe(sub_client, topic)
        print(sub_client)
        sub_client.loop_forever()
