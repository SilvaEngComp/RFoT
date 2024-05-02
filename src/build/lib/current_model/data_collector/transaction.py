
import json

class Transaction:
    def __init__(self, sender, sensor,receiver, data):
        self.sender = sender
        self.sensor = sensor
        self.receiver = receiver
        self.data = data
        
    def __getitem__(self, i):
        if i == 'sensor':
            return self.sensor
        elif i == 'data':
            return self.data
        
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
    
    @classmethod
    def fromJson(self,data):
        if isinstance(data, dict):
            return Transaction(data['sender'],data['sensor'],data['receiver'],data['data'])
        return data
            

