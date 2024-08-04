
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
import os

class Sensor:
    position=0
    listSensors = ['temperature','light','voltage','humidity']
    fileName = 'physic-manager.json'
    def __init__(self, sensorName):
        self.sensorName = self._getSensor(sensorName)
        self.dataset = pd.read_csv('intel_lab.csv', usecols=[
                                self.sensorName], delimiter=",")
    
    def _getPosition(self):
        oldPosition = Sensor.position
        Sensor.position = oldPosition+1
        if Sensor.position >= len(self.dataset):
                Sensor.position=0
        # self.register(Sensor.position)
        return oldPosition
    
    def _getSensor(self,sensorName):
        gen = (x for x in Sensor.listSensors if x in sensorName)
        return next(gen)
            
        
    def getByDataset(self):
        try:
            cipher = Cipher()
            
            currentPosition = self._getPosition()
            
            value = str(self.dataset[self.sensorName].iloc[currentPosition])
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
        
    def register(self, position):
        with open(Sensor.fileName, "w") as file:
            try:
                json_position = {
                    'position':position
                }
                # print('registring physic data number | nº: {} '.format(
                #     json_position))
                json.dump(json_position, file)
            except:
                print('erro in position registration')

    def get(self):
        print(os.path.exists(Sensor.fileName) )
        if os.path.exists(Sensor.fileName) is False:
            return 0
        try:
            with open(Sensor.fileName) as file:
                data = json.load(file)
                return data["position"]
        except:
            print('not found local pool file: ')
            return 0
