
# This shows two examples of simulated sensors which can be used to test
# the TATU protocol on SOFT-IoT or with a standalone MQTT broker
#
# There are samples of real sensors implementations in the src/sensorsExamples
# folder. You can adapt those examples to your needs.


# The name of sensors functions should be exactly the same as in config.json
import random
import pandas as pd

def blockchainSensor(pos):
    dataset  = pd.read_csv('intel_lab.csv', delimiter=",")
    if pos>=0 and pos<dataset.shape[0]:
        return dataset.light[pos]
    return False

def lightSensor(pos):
    dataset  = pd.read_csv('intel_lab.csv', delimiter=",")
    if pos>=0 and pos<dataset.shape[0]:
        return dataset.light[pos]
    return False
    
    
def voltageSensor(pos):
    dataset  = pd.read_csv('intel_lab.csv', delimiter=",")
    if pos>=0 and pos<dataset.shape[0]:
        return dataset.voltage[pos]
    return False

def humiditySensor(pos):
    dataset  = pd.read_csv('intel_lab.csv', delimiter=",")
    if pos>=0 and pos<dataset.shape[0]:
        return dataset.humidity[pos]
    return False

def temperatureSensor(pos):
    dataset  = pd.read_csv('intel_lab.csv', delimiter=",")
    if pos>=0 and pos<dataset.shape[0]:
        return dataset.temperature[pos]
    return False

def soilmoistureSensor(pos):
    return random.randint(0,1023)

def solarradiationSensor(pos):
    return random.randint(300, 3000)

def ledActuator(s = None):
    if s==None:
        return bool(random.randint(0, 1))
    else:
        if s:
           rint("1")
        else:
           rint("0")
        return s
