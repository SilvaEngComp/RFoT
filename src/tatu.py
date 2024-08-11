import paho.mqtt.client as pub
from sensors import Sensor
import json
import multiprocessing
import os

#You don't need to change this file. Just change sensors.py and config.json

from time import sleep


procs = []
pub_client = pub.Client(client_id='', clean_session=True, userdata=None,protocol=pub.MQTTv31)
mqttBroker=""
class sensorProcess (multiprocessing.Process):
    def __init__(self, idP, deviceName, sensorName, met, topic, topicError, pub_client, collectTime, publishTime):
        multiprocessing.Process.__init__(self)
        self.processID = idP
        self.deviceName = deviceName
        self.sensorName = sensorName
        self.met = met
        self.topic = topic
        self.topicError = topicError
        self.pub_client = pub_client
        self.publishTime = publishTime
        self.collectTime = collectTime
    def run(self):
        print ("Starting process " + self.processID)

        if (self.met == "EVENT"):
            buildEventAnwserDevice(self.deviceName, self.sensorName, self.topic, self.topicError, self.pub_client, self.collectTime, self.publishTime)
        elif (self.met == "GET"):
        	buildGetAnwserDevice(self.deviceName, self.sensorName, self.topic, self.topicError, self.pub_client)
        elif (self.met == "flow"):
            buildFlowAnwserDevice(self.deviceName, self.sensorName, self.topic, self.topicError, self.pub_client, self.collectTime, self.publishTime)
        
        print ("Stopping process " + self.processID)

class actuatorProcess (multiprocessing.Process):
    def __init__(self, idP, deviceName, sensorName, met, topic, topicError, pub_client, value):
        multiprocessing.Process.__init__(self)
        self.processID = idP
        self.deviceName = deviceName
        self.sensorName = sensorName
        self.met = met
        self.topic = topic
        self.topicError = topicError
        self.pub_client = pub_client
        self.value = value

    def run(self):
        print ("Starting process " + self.processID)

        if (self.met == "POST"):
            buildPostAnwserDevice(self.deviceName, self.sensorName, self.topic, self.topicError, self.pub_client, self.value)
        
        print ("Stopping process " + self.processID)
        

        
 
def buildFlowAnwserDevice(deviceName, sensorName, topic, topicError, pub_client, collectTime, publishTime):
	value = ""
	t = 0
	try:
		sensor = Sensor(sensorName)
		listValues = []
		
		while True:
			listValues.append(str(sensor.getdataBySensorNode()))
			t = t + collectTime + 1000
			#Request: {"method":"FLOW", "sensor":"sensorName", "time":{"collect":collectTime,"publish":publishTime}}
			responseModel={"code":"post","post":topic,"method":"flow","header":{"sensor":sensorName,"device":deviceName,"time":{"collect":collectTime, "publish": publishTime}}, "data":listValues[0]}
			response = json.dumps(responseModel)
			print('post topic: ',topic)
			pub_client.publish(topic, response)
			t = 0
			listValues = []
			sleep(int(publishTime/1000))
	except:
		print("erro")
		errorMessage = "There is no " + sensorName + " sensor in device " + deviceName
		errorNumber = 1
		responseModel = {"code":"ERROR", "number":errorNumber, "message":errorMessage}
		response = json.dumps(responseModel)
		pub_client.publish(topicError, response)


def buildEventAnwserDevice(deviceName, sensorName, topic, topicError, pub_client, collectTime, publishTime):
    try:
        methodEvent = getattr(sensors, sensorName)
        value = methodEvent()
        #Request: {"method":"EVENT", "sensor":"sensorName", "time":{"collect":collectTime}}
        responseModel = {"CODE":"POST","METHOD":"EVENT","HEADER":{"NAME":deviceName},"BODY":{sensorName:value,"EVENT":{"collect":(collectTime),"publish":(publishTime)}}}
        response = json.dumps(responseModel)
        pub_client.publish(topic, response)

        while True:
            sleep(collectTime)
            publishTime = publishTime + collectTime
            aux = methodEvent()
            if aux!=value:
                value = aux
                #Request: {"method":"EVENT", "sensor":"deviceName", "time":{"collect":collectTime}}
                responseModel = {"CODE":"POST","METHOD":"EVENT","HEADER":{"NAME":deviceName},"BODY":{sensorName:value,"EVENT":{"collect":(collectTime),"publish":(publishTime)}}}
                response = json.dumps(responseModel)
                pub_client.publish(topic, response)
    except:
        errorMessage = "There is no " + sensorName + " sensor in device " + deviceName
        errorNumber = 1
        responseModel = {"code":"ERROR", "number":errorNumber, "message":errorMessage}
        response = json.dumps(responseModel)
        pub_client.publish(topicError, response)


def buildGetAnwserDevice(deviceName, sensorName, topic, topicError, pub_client):
    try:
        methodGet = getattr(sensors, sensorName)
        value = methodGet()

        #Request: {"method":"GET", "sensor":"sensorName"}
        responseModel = {'CODE':'POST','METHOD':'GET','HEADER':{'NAME':deviceName},'BODY':{sensorName:value}}
        response = json.dumps(responseModel)

        pub_client.publish(topic, response)
    except:
        errorMessage = "There is no " + sensorName + " sensor in device " + deviceName
        errorNumber = 1
        responseModel = {"code":"ERROR", "number":errorNumber, "message":errorMessage}
        response = json.dumps(responseModel)
        pub_client.publish(topicError, response)

def buildPostAnwserDevice(deviceName, sensorName, topic, topicError, pub_client, value):
    try:
        #p = "__" + sensorName + "__"
       #methodPost = getattr(sensors, sensorName)
        #methodPost(value)

        #Request: {"method":"POST", "sensor":"sensorName", "value":value}
        responseModel = {"code":"POST","method":"POST", "sensor":sensorName, "value":value}
        response = json.dumps(responseModel)
        print('post topic: ',topic)
        pub_client.publish(topic, response)
    except:
        errorMessage = "There is no " + sensorName + " sensor in device " + deviceName
        errorNumber = 1
        responseModel = {"code":"ERROR", "number":errorNumber, "message":errorMessage}
        response = json.dumps(responseModel)
        pub_client.publish(topicError, response)

#def status ():
#{"method":"EVENT", "sensor":"soundSensor", "status":False}
#{"method":"STOP", "target": "EVENT", "sensor":"soundSensor"}

def on_disconnect(mqttc, obj, rc):
    print("disconnected tatu!")


def main(data, msg):
	global mqttBroker
	#print("oi")
	mqttBroker = data["mqttBroker"]
	mqttPort = data["mqttPort"]
	mqttUsername = data["mqttUsername"]
	mqttPassword = data["mqttPassword"]
	deviceName = data["deviceName"]
	topic = data["topicPrefix"] + deviceName + data["topicRes"]
	topicError = data["topicPrefix"] + deviceName + data["topicErr"]

	if isinstance(msg, str):
		msgJson = json.loads(msg)
	else:
		msgJson = json.loads(msg.payload)

			
	sensorName = msgJson["sensor"]
	met = msgJson["method"]

	idP = met + "_" + deviceName + "_" + sensorName
	print("Metodo "+idP)
	#pub_client = pub.Client(idP,protocol=pub.MQTTv31)
	#pub_client.username_pw_set(mqttUsername, mqttPassword)
	#pub_client.user_data_set(data)
	pub_client.on_disconnect = on_disconnect
	pub_client.connect(mqttBroker, int(mqttPort), 60)
	print("chamad")

	if (met=="STOP"):
		#{"method":"STOP", "target": "EVENT", "sensor":"soundSensor"}
		idP = msgJson["target"] + "_" + deviceName + "_" + sensorName
		stopped = False
		for proc in procs:
			if (proc.processID==idP):
				print ("Stopping process " + proc.processID)
				procs.remove(proc)
				proc.terminate()
				stopped = True
				break
		if not stopped:
			#error in json to /ERR
			errorMessage = "There is no running process named " + idP
			errorNumber = 2
			responseModel = {"code":"ERROR", "number":errorNumber, "message":errorMessage}
			response = json.dumps(responseModel)
			pub_client.publish(topicError, response)
	elif (met=="POST"):
		#{"method":"POST", "sensor":"sensorName", "value":value} 
		value = msgJson["value"]
		print('block topic: ',topic)
		proc = actuatorProcess(idP, deviceName, sensorName, met, topic, topicError, pub_client, value)
		procs.append(proc)
		proc.start()
	else:
		if (met=="GET"):
			collectTime = 0
			publishTime = 0
		elif (met=="flow"):
			time = msgJson["time"]
			collectTime = time["collect"]
			publishTime = time["publish"]
		elif (met=="EVENT"):
			time = msgJson["time"]
			collectTime = time["collect"]
			publishTime = 0

		proc = sensorProcess(idP, deviceName, sensorName, met, topic, topicError, pub_client, collectTime, publishTime)
		procs.append(proc)
		proc.start()