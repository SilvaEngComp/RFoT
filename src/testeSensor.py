from sensors import Sensor

sensor = Sensor("temperatureSensor")
for i in range(10):
   print(sensor.getdataBySensorNode())
