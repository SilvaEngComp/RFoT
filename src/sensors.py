
# This shows two examples of simulated sensors which can be used to test
# the TATU protocol on SOFT-IoT or with a standalone MQTT broker
#
# There are samples of real sensors implementations in the src/sensorsExamples
# folder. You can adapt those examples to your needs.


# The name of sensors functions should be exactly the same as in config.json
import random
import pandas as pd
from src.suport_layer.cipher import Cipher
import json


class Sensor:
    position=900
    listSensors = ['temperature','light','voltage','humidity']
    def __init__(self, sensorName):
        self.sensorName = self._getSensor(sensorName)
        print(self.sensorName)
    
    def getByDataset(self):
        try:
            
            cipher = Cipher()
            dataset = pd.read_csv('intel_lab.csv', usecols=[
                                self.sensorName], delimiter=",")
            currentPosition = self._getPosition(len(dataset))
            
            value = str(dataset[self.sensorName].iloc[currentPosition])
            dataBytes = str.encode(value)
            return cipher.encrypt(dataBytes)
        except:
            return None
        
    def getdataBySensorNode(self):
        try:
            
            cipher = Cipher()
            # dataset = pd.read_csv('intel_lab.csv', usecols=['temperature','humidity'], delimiter=",")
            # currentPosition = self._getPosition(len(dataset))
            
            # temperature = str(dataset['temperature'].iloc[currentPosition])
            # humidity = str(dataset['humidity'].iloc[currentPosition])
            # #sensorNode = {'temperature':temperature,'humidity':humidity}
            sensorNode = {'temperature':'1','humidity':'1'}
            dataBytes = json.dumps(sensorNode).encode("utf-8")
            return cipher.encrypt(dataBytes)
        except:
            return 'error to try read csv sensorName='+self.sensorName

    def _getPosition(self,datasetSize):
        oldPosition = Sensor.position
        Sensor.position +=1
        if Sensor.position>=datasetSize:
                Sensor.position=None
        return oldPosition
    def _getSensor(self,sensorName):
        gen = (x for x in Sensor.listSensors if x in sensorName)
        return next(gen)
            
        
    def ledActuator(s=None):
        if s == None:
            return bool(random.randint(0, 1))
        else:
            if s:
                rint("1")
            else:
                rint("0")
            return s
