
# This shows two examples of simulated sensors which can be used to test
# the TATU protocol on SOFT-IoT or with a standalone MQTT broker
#
# There are samples of real sensors implementations in the src/sensorsExamples
# folder. You can adapt those examples to your needs.


# The name of sensors functions should be exactly the same as in config.json
import random
import pandas as pd



def getByDataset(pos, sensorName):
	try:
		dataset  = pd.read_csv('intel_lab.csv', usecols=[sensorName], delimiter=",")
		return dataset[sensorName].iloc[pos]
	except:
		return 'error to try read csv'
		
def lightSensor(pos):
	return getByDataset(pos, 'light')    
    
def voltageSensor(pos):
    return getByDataset(pos, 'voltage')

def humiditySensor(pos):
    return getByDataset(pos, 'humidity')

def temperatureSensor(pos):
    return getByDataset(pos, 'temperature')

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
