
import pandas as pd
from src.suport_layer.cipher import Cipher
import json
from src.suport_layer.transaction import Transaction
from src.utils.time_register import TimeRegister
from src.proposed_model.smart_contract_1 import SC1
from time import sleep
class Msg:
    def __init__(self,payload) -> None:
        self.payload = payload
        
cipher = Cipher()
dataset = pd.read_csv('../intel_lab.csv', usecols=['temperature','humidity'], delimiter=",")
cont=0
sub_device = "h3"
blockWidth=20
sc1 = SC1(sub_device, blockWidth)
for data in dataset.iterrows():
    if cont>20000:
        break
    temperature = str(data[1][0])
    humidity = str(data[1][1])
    sensorNode = {'temperature':temperature,'humidity':humidity}
    dataBytes = json.dumps(sensorNode).encode("utf-8")
    encrypted = cipher.encrypt(dataBytes)
    responseModel = {"code":"post","post":'sc01',"method":"flow","header":{"sensor":'node Temperature and Humidity',"device":'h1',"time":{"collect":10000, "publish": 10000}}, "data":encrypted.decode()}
    responseModel = json.dumps(responseModel)

    msg = Msg(responseModel)


    isCompleted = sc1.dataTreating(msg)
    if isCompleted is True:
        sc1.restart()
        # sleep(5)
    cont+=1

