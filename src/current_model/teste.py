
import random
import pandas as pd
from src.suport_layer.cipher import Cipher
import json
from iotcoin import Iotcoin
from src.suport_layer.transaction import Transaction
from src.utils.time_register import TimeRegister

cipher = Cipher()
dataset = pd.read_csv('../intel_lab.csv', usecols=['temperature','humidity'], delimiter=",")
iotcoin = Iotcoin('h1', 20)
cont=0
for data in dataset.iterrows():
    if cont>20000:
        break
    temperature = str(data[1][0])
    humidity = str(data[1][1])
    sensorNode = {'temperature':temperature,'humidity':humidity}
    dataBytes = json.dumps(sensorNode).encode("utf-8")
    encrypted = cipher.encrypt(dataBytes)
    responseModel={"code":"post","post":'sc01',"method":"flow","header":{"sensor":'node Temperature and Humidity',"device":'h1',"time":{"collect":10000, "publish": 10000}}, "data":encrypted.decode()}

    transaction = Transaction(
        responseModel['header']['device'], responseModel['header']['sensor'], 'h1', responseModel['data'])
    isCompleted = iotcoin.transactionProcess(transaction)
    if isCompleted is True:
        TimeRegister.addTime("transaction registed")
        iotcoin.restart()
    cont+=1