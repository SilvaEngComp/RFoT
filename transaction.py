
import json

class Transaction:
	def __init__(self, sender, sensor,receiver, data):
		self.sender = sender
		self.sensor = sensor
		self.receiver = receiver
		self.data = data

		
	def __str__(self):
		return str({
		'sender': self.sender,
        'sensor': self.sensor,
		'receiver':self.receiver,
		'data': self.data ,
		})
		
	def __repr__(self):
		return str({
		'sender': self.sender,
        'sensor': self.sensor,
		'receiver':self.receiver,
		'data': self.data ,
		})
	def toJson(self):
		return {
		'sender': self.sender,
        'sensor': self.sensor,
		'receiver':self.receiver,
		'data': self.data ,
		}

