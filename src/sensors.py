
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
    position=0
    listSensors = ['temperature','light','voltage','humidity']
    def __init__(self, sensorName):
        self.sensorName = self._getSensor(sensorName)
        print(self.sensorName)
    
    def _getPosition(self):
        oldPosition = Sensor.position
        Sensor.position +=1
        return oldPosition
    def _getSensor(self,sensorName):
        gen = (x for x in Sensor.listSensors if x in sensorName)
        return next(gen)
            
        
    def getByDataset(self):
        try:
            currentPosition = self._getPosition()
            cipher = Cipher()
            dataset = pd.read_csv('intel_lab.csv', usecols=[
                                self.sensorName], delimiter=",")
            value = str(dataset[self.sensorName].iloc[currentPosition])
            dataBytes = str.encode(value)
            return cipher.encrypt(dataBytes)
        except:
            return 'error to try read csv sensorName='+self.sensorName

    def ledActuator(s=None):
        if s == None:
            return bool(random.randint(0, 1))
        else:
            if s:
                rint("1")
            else:
                rint("0")
            return s
